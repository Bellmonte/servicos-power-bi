"""Compara as pontas da paridade (fonte, v1, v2) com as tolerâncias da seção 6.

Cada ponta é uma pasta com um arquivo por corte (`<corte>.csv` ou `<corte>.json`, lista de linhas),
com as colunas `corte`, `chave` e uma por medida. Nome de coluna com colchete ou prefixo de tabela,
como sai do motor, é normalizado. Duas pontas bastam; com três, todas são cruzadas duas a duas.

Uso: python comparar.py <saida.csv> fonte=<pasta> v1=<pasta> v2=<pasta>
Sai com código 1 se houver qualquer divergência.
"""
import csv
import itertools
import json
import math
import re
import sys
from pathlib import Path

CONTAGEM = {"quantidade", "linhas", "pedidos", "clientes_com_compra"}
RAZAO = {"margem_pct", "crescimento_pct", "participacao", "peso_mercado"}
TOL_VALOR, TOL_RAZAO = 0.01, 1e-6
CORTES = ["total", "ano_mes", "regiao", "categoria", "porte", "vendedor", "cliente", "ano_mes_regiao", "estado_b"]


def nome(c):
    c = re.sub(r"^.*\[(.+)\]$", r"\1", c.strip())
    return c.split(".")[-1].strip()


def numero(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return None if isinstance(v, float) and math.isnan(v) else float(v)
    v = str(v).strip()
    if v == "" or v.lower() in ("nan", "null", "none"):
        return None
    return float(v.replace(",", ".")) if re.fullmatch(r"-?[\d.,]+(e-?\d+)?", v, re.I) else None


def chave(v):
    n = numero(v)
    return str(int(n)) if n is not None and n == int(n) and not re.search(r"[A-Za-z|-]", str(v)) else str(v).strip()


def ler(pasta, corte):
    for ext in ("csv", "json"):
        arq = Path(pasta) / f"{corte}.{ext}"
        if arq.exists():
            if ext == "csv":
                with open(arq, encoding="utf-8-sig", newline="") as fh:
                    linhas = list(csv.DictReader(fh))
            else:
                linhas = json.loads(arq.read_text(encoding="utf-8-sig"))
            return {chave(r.get("chave") or next(v for k, v in r.items() if nome(k) == "chave")):
                    {nome(k): v for k, v in r.items()} for r in linhas}
    return None


def divergem(medida, a, b):
    x, y = numero(a), numero(b)
    if x is None or y is None:
        return (x is None) != (y is None)
    if medida in CONTAGEM:
        return x != y
    return abs(x - y) > (TOL_RAZAO if medida in RAZAO else TOL_VALOR)


saida = Path(sys.argv[1])
pontas = dict(a.split("=", 1) for a in sys.argv[2:])
resultado, resumo = [], []
for corte in CORTES:
    dados = {p: ler(pasta, corte) for p, pasta in pontas.items()}
    dados = {p: d for p, d in dados.items() if d is not None}
    if len(dados) < 2:
        resumo.append((corte, 0, 0, "falta ponta"))
        continue
    n = div = 0
    for p1, p2 in itertools.combinations(dados, 2):
        d1, d2 = dados[p1], dados[p2]
        for k in sorted(set(d1) | set(d2)):
            if k not in d1 or k not in d2:
                div += 1
                resultado.append([corte, k, "(linha)", p1, p2, k in d1, k in d2, "", False])
                continue
            for m in (c for c in d1[k] if c not in ("corte", "chave")):
                if m not in d2[k]:
                    continue
                n += 1
                ruim = divergem(m, d1[k][m], d2[k][m])
                div += ruim
                x, y = numero(d1[k][m]), numero(d2[k][m])
                dif = "" if x is None or y is None else f"{x - y:.9g}"
                resultado.append([corte, k, m, p1, p2, d1[k][m], d2[k][m], dif, not ruim])
    resumo.append((corte, n, div, " x ".join(dados)))

saida.parent.mkdir(parents=True, exist_ok=True)
with open(saida, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["corte", "chave", "medida", "ponta_1", "ponta_2", "valor_1", "valor_2", "diferenca", "dentro_tolerancia"])
    w.writerows(resultado)
print(f"{'corte':<16}{'comparações':>12}{'divergências':>14}  pontas")
for corte, n, div, pts in resumo:
    print(f"{corte:<16}{n:>12}{div:>14}  {pts}")
total_div = sum(r[2] for r in resumo)
print(f"\ntotal: {sum(r[1] for r in resumo)} comparações, {total_div} divergências. Detalhe em {saida}")
sys.exit(1 if total_div else 0)
