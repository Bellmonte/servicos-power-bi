"""Cruza as duas pontas da paridade, a base e o painel, com as tolerâncias do levantamento.

Cada ponta é uma pasta com um arquivo `<corte>.csv` por corte, com as colunas `corte`, `chave` e
uma por medida. Nome de coluna com colchete, como sai do motor, é normalizado. Uma linha que existe
numa ponta e falta na outra conta como divergência.

Uso: python comparar.py <saida.csv> base=<pasta> painel=<pasta>
Sai com código 1 se houver qualquer divergência.
"""
import csv
import itertools
import math
import re
import sys
from pathlib import Path

from medidas import CORTES, MEDIDAS

TOLERANCIA = {"contagem": 0.0, "valor": 0.01, "razao": 1e-6}


def nome(c):
    return re.sub(r"^.*\[(.+)\]$", r"\1", c.strip())


def numero(v):
    if v is None:
        return None
    v = str(v).strip()
    if v == "" or v.lower() in ("nan", "null", "none"):
        return None
    try:
        x = float(v.replace(",", ".")) if re.fullmatch(r"-?[\d.,]+(e[-+]?\d+)?", v, re.I) else None
    except ValueError:
        return None
    return None if x is None or math.isnan(x) else x


def chave(v):
    v = str(v).strip()
    return re.sub(r"(?<![\d.])(\d+)\.0(?![\d])", r"\1", v)


def ler(pasta, corte):
    arq = Path(pasta) / f"{corte}.csv"
    if not arq.exists():
        return None
    with open(arq, encoding="utf-8-sig", newline="") as fh:
        linhas = [{nome(k): v for k, v in r.items()} for r in csv.DictReader(fh)]
    return {chave(r["chave"]): r for r in linhas}


def diverge(medida, a, b):
    x, y = numero(a), numero(b)
    if x is None or y is None:
        return (x is None) != (y is None)
    return abs(x - y) > TOLERANCIA[MEDIDAS[medida][1]]


saida = Path(sys.argv[1])
pontas = dict(a.split("=", 1) for a in sys.argv[2:])
detalhe, resumo = [], []
for corte, (nomes, _) in CORTES.items():
    dados = {p: ler(pasta, corte) for p, pasta in pontas.items()}
    dados = {p: d for p, d in dados.items() if d is not None}
    if len(dados) < 2:
        resumo.append((corte, 0, 0, 0, "falta ponta"))
        continue
    n = div = 0
    for p1, p2 in itertools.combinations(dados, 2):
        d1, d2 = dados[p1], dados[p2]
        for k in sorted(set(d1) | set(d2)):
            if k not in d1 or k not in d2:
                div += 1
                detalhe.append([corte, k, "(linha)", p1, p2, k in d1, k in d2, "", False])
                continue
            for m in nomes:
                n += 1
                ruim = diverge(m, d1[k].get(m), d2[k].get(m))
                div += ruim
                x, y = numero(d1[k].get(m)), numero(d2[k].get(m))
                dif = "" if x is None or y is None else f"{x - y:.9g}"
                detalhe.append([corte, k, m, p1, p2, d1[k].get(m), d2[k].get(m), dif, not ruim])
    resumo.append((corte, len(next(iter(dados.values()))), n, div, " x ".join(dados)))

saida.parent.mkdir(parents=True, exist_ok=True)
with open(saida, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["corte", "chave", "medida", "ponta_1", "ponta_2", "valor_1", "valor_2", "diferenca", "dentro_tolerancia"])
    w.writerows(detalhe)
print(f"{'corte':<16}{'linhas':>8}{'comparações':>13}{'divergências':>14}  pontas")
for corte, linhas, n, div, pts in resumo:
    print(f"{corte:<16}{linhas:>8}{n:>13}{div:>14}  {pts}")
total = sum(r[3] for r in resumo)
print(f"\ntotal: {sum(r[2] for r in resumo)} comparações, {total} divergências. Detalhe em {saida}")
sys.exit(1 if total else 0)
