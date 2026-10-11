"""Gera `consultas.dax`, uma consulta por corte da paridade, contra o modelo do painel.

Cada consulta começa com a linha `// corte: <nome>`, que é o separador usado pelo `rodar.ps1` e o
nome do CSV que o `comparar.py` espera. As colunas de saída são `corte`, `chave` e o nome curto de
cada medida, as mesmas que o `fonte.py` grava a partir da base. O filtro de um corte entra como
argumento do SUMMARIZECOLUMNS, do mesmo jeito que o Power BI passa a segmentação de um visual.

Uso: python gera_consultas.py   (grava consultas.dax nesta pasta)
"""
from pathlib import Path

from medidas import CORTES, FILTROS, MEDIDAS

AQUI = Path(__file__).resolve().parent

COLUNAS = {
    "ano_mes": ["Dim_Calendario[Ano]", "Dim_Calendario[Mes]"],
    "regiao": ["Dim_Regiao[Regiao]"],
    "linha": ["Dim_Produto[Linha de Produto]"],
    "porte": ["Dim_Cliente[Porte]"],
    "vendedor_id": ["Dim_Vendedor[ID Vendedor]"],
    "cliente_id": ["Dim_Cliente[ID Cliente]"],
}
CHAVE = {
    "ano_mes": 'Dim_Calendario[Ano] & "-" & FORMAT ( Dim_Calendario[Mes], "00" )',
    "regiao": "Dim_Regiao[Regiao]",
    "linha": "Dim_Produto[Linha de Produto]",
    "porte": "Dim_Cliente[Porte]",
    "vendedor_id": "Dim_Vendedor[ID Vendedor]",
    "cliente_id": "Dim_Cliente[ID Cliente]",
}
FILTRO_DAX = {"ano": "TREATAS ( {{ {0} }}, Dim_Calendario[Ano] )"}


def consulta(corte, nomes, grupo):
    medidas = [f'"{n}", [{MEDIDAS[n][0]}]' for n in nomes]
    if not grupo:
        corpo = ",\n        ".join([f'"corte", "{corte}"', '"chave", "total"'] + medidas)
        return f"// corte: {corte}\nEVALUATE\n    ROW (\n        {corpo}\n    )\n"
    colunas = [c for a in grupo for c in COLUNAS[a]]
    filtros = [FILTRO_DAX[k].format(v) for k, v in FILTROS.get(corte, {}).items()]
    chave = ' & "|" & '.join(CHAVE[a] for a in grupo)
    resumo = ",\n            ".join(colunas + filtros + medidas)
    saida = ",\n        ".join([f'"corte", "{corte}"', f'"chave", {chave}'] + [f'"{n}", [{n}]' for n in nomes])
    return (f"// corte: {corte}\nEVALUATE\n    SELECTCOLUMNS (\n        SUMMARIZECOLUMNS (\n            {resumo}\n"
            f"        ),\n        {saida}\n    )\n")


texto = "\n".join(consulta(c, nomes, grupo) for c, (nomes, grupo) in CORTES.items())
(AQUI / "consultas.dax").write_text(texto, encoding="utf-8", newline="\n")
print(f"consultas.dax: {len(CORTES)} cortes")
