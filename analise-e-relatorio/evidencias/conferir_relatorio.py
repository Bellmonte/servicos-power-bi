"""Confere que todo número do relatório sai do notebook.

Uso, na pasta do caso, depois de executar o notebook:
    python evidencias/conferir_relatorio.py

Para cada parágrafo ou linha de tabela do relatorio.md, lê as células citadas entre colchetes
([C21] ou [C18, C21]) e exige que cada número escrito ali seja um dos valores que essas células
gravaram em evidencias/resultados.json, na mesma forma impressa. Linha de tabela herda as células
do parágrafo que a apresenta. Ficam de fora só o aviso de dado 100% fictício e os parâmetros
declarados no enquadramento (tetos, largura das faixas, nível de confiança, tamanho das janelas e
anos), listados em PARAMETROS. Termina com erro se algum número não tiver origem ou se alguma
célula citada não existir no notebook.
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PARAMETROS = {"100%", "2%", "10%", "12%", "14%", "18%", "95%", "0", "1", "6", "12", "24", "36", "2023", "2026"}
NUMERO = re.compile(r"R\$ [\d.]+(?:,\d+)? (?:milhões|milhão|mil)|[+-]?\d[\d.]*(?:,\d+)?%?")
CITACAO = re.compile(r"\[(C\d+(?:, C\d+)*)\]")


def blocos(texto):
    # Parágrafos separados por linha em branco; cada linha de tabela vira um bloco próprio que
    # herda as citações do último parágrafo comum.
    herdadas = set()
    for paragrafo in re.split(r"\n\s*\n", texto):
        linhas = paragrafo.strip().splitlines()
        if not linhas or linhas[0].startswith(("![", "<!--", "#")):
            continue
        if linhas[0].startswith("|"):
            for linha in linhas[2:]:
                yield linha, herdadas | citadas(linha)
        else:
            herdadas = citadas(paragrafo)
            yield paragrafo, herdadas


def citadas(texto):
    return {c.strip() for grupo in CITACAO.findall(texto) for c in grupo.split(",")}


def main():
    relatorio = (RAIZ / "relatorio.md").read_text(encoding="utf-8")
    resultados = json.loads((RAIZ / "evidencias" / "resultados.json").read_text(encoding="utf-8"))
    notebook = json.loads((RAIZ / "analise.ipynb").read_text(encoding="utf-8"))
    tags = {t for c in notebook["cells"] for t in c.get("metadata", {}).get("tags", [])}
    por_celula = {}
    for item in resultados.values():
        por_celula.setdefault(item["celula"], set()).add(item["texto"])

    erros, conferidos = [], 0
    for celula in sorted(citadas(relatorio) - tags):
        erros.append(f"célula citada que não existe no notebook: {celula}")
    for bloco, celulas in blocos(relatorio):
        corpo = CITACAO.sub("", re.sub(r"`[^`]*`", "", bloco))
        validos = set().union(*(por_celula.get(c, set()) for c in celulas)) if celulas else set()
        for numero in NUMERO.findall(corpo):
            limpo = numero.lstrip("+")
            if limpo in PARAMETROS:
                continue
            conferidos += 1
            if limpo not in validos and limpo.rstrip("%") not in validos:
                trecho = " ".join(bloco.split())[:70]
                erros.append(f"{numero} sem origem nas células {sorted(celulas) or '-'}: {trecho}")
    for erro in erros:
        print(erro)
    print(f"{conferidos} números conferidos, {len(erros)} problemas.")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
