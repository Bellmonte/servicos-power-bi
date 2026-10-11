"""Gera as consultas DAX de paridade da v1 e da v2 (seção 6 da metodologia.md).

As duas pontas devolvem exatamente as mesmas colunas: `corte`, `chave` e uma coluna por medida.
Cada consulta começa com uma linha `// corte: <nome>`, que é o separador usado por `rodar.ps1` e
o nome do CSV esperado por `comparar.py`.

Uso: python gera_consultas.py   (grava consultas_v1.dax e consultas_v2.dax nesta pasta)
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# Medida de paridade -> expressão em cada ponta. Na v1, o que era agregação implícita no visual
# vira uma medida local da consulta, com a mesma conta que o visual fazia.
#
# A v2 segue o padrão de desenvolvimento desde 10-10-2026: tabelas Fact_ e Dim_, todas as medidas
# na tabela Medidas, com a unidade no nome. O lado v1 não muda.
MEDIDAS = {
    "receita_bruta": ("SUM(Vendas[receita_bruta])", "[Receita Bruta (R$)]"),
    "receita_liquida": ("SUM(Vendas[receita_liquida])", "[Receita Liquida (R$)]"),
    "custo": ("SUM(Vendas[custo_total])", "[Custo (R$)]"),
    "margem": ("SUM(Vendas[Lucro])", "[Margem (R$)]"),
    "margem_pct": ("[Margem %]", "[Margem (%)]"),
    "quantidade": ("SUM(Vendas[quantidade])", "[Quantidade (un)]"),
    "linhas": ("COUNTROWS(Vendas)", "[Linhas de Venda]"),
    "pedidos": ("DISTINCTCOUNT(Vendas[numero_pedido])", "[Pedidos]"),
    "ticket_medio": ("[Ticket Médio]", "[Ticket Medio (R$)]"),
    "clientes_com_compra": ("[Clientes com Compra]", "[Clientes com Compra]"),
    "receita_premium": ("[Receita Linha Premium]", "[Receita Linha Premium (R$)]"),
    "receita_ano_anterior": ("[Receita Ano Anterior]", "[Receita Ano Anterior (R$)]"),
    "receita_acumulada_ano": ("[Receita Acumulada no Ano]", "[Receita Acumulada no Ano (R$)]"),
    "crescimento_pct": ("[Crescimento sobre Ano Anterior %]", "[Crescimento sobre Ano Anterior (%)]"),
    "participacao": ("[Participação na Receita]", "[Participacao na Receita (%)]"),
    "peso_mercado": ("SUM(Regioes[peso_mercado])", "[Peso de Mercado (%)]"),
}
# Tabela onde a consulta define as medidas locais de cada ponta.
TABELA_MEDIDAS = {0: "Vendas", 1: "Medidas"}
# Chave de ano-mês no formato AAAA-MM nas duas pontas. Na v1 ela é a coluna ano_mes; na v2 o
# calendário vem da função do padrão, sem essa coluna, e a chave é montada de Ano e Mes.
ANO_MES_V2 = 'Dim_Calendario[Ano] & "-" & FORMAT(Dim_Calendario[Mes], "00")'
TEMPO = ["receita_ano_anterior", "receita_acumulada_ano", "crescimento_pct"]
TODAS = list(MEDIDAS)
SEM_TEMPO = [m for m in TODAS if m not in TEMPO]
ADITIVAS = ["receita_bruta", "receita_liquida", "custo", "margem", "quantidade", "linhas", "pedidos",
            "clientes_com_compra"]

# corte -> (medidas, chaves na v1, chaves na v2, expressão da chave na v2 quando ela não é a
# simples concatenação das colunas). Chave vazia = total.
CORTES = {
    "total": (TODAS, [], [], None),
    "ano_mes": (TODAS, ["Vendas[ano_mes]"], ["Dim_Calendario[Ano]", "Dim_Calendario[Mes]"], ANO_MES_V2),
    "regiao": (SEM_TEMPO, ["Vendas[regiao]"], ["Dim_Regiao[Regiao]"], None),
    "categoria": (SEM_TEMPO, ["Vendas[categoria]"], ["Dim_Produto[Linha de Produto]"], None),
    "porte": (SEM_TEMPO, ["Vendas[porte]"], ["Dim_Cliente[Porte]"], None),
    "vendedor": (ADITIVAS, ["Vendas[vendedor_id]"], ["Dim_Vendedor[ID Vendedor]"], None),
    "cliente": (ADITIVAS, ["Vendas[cliente_id]"], ["Dim_Cliente[ID Cliente]"], None),
    "ano_mes_regiao": (TODAS, ["Vendas[ano_mes]", "Vendas[regiao]"],
                       ["Dim_Calendario[Ano]", "Dim_Calendario[Mes]", "Dim_Regiao[Regiao]"],
                       ANO_MES_V2 + ' & "|" & Dim_Regiao[Regiao]'),
    "estado_b": (TODAS, [], [], None),
}
# Estado B da seção 5: região Sudeste e o último ano da janela.
ESTADO_B = {0: 'Vendas[regiao] = "Sudeste", Vendas[ano] = 2026',
            1: 'Dim_Regiao[Regiao] = "Sudeste", Dim_Calendario[Ano] = 2026'}


def consulta(corte, ponta):
    medidas, chaves_a, chaves_d, chave_v2 = CORTES[corte]
    chaves = chaves_a if ponta == 0 else chaves_d
    tabela = TABELA_MEDIDAS[ponta]
    define = "\n".join(f"    MEASURE {tabela}[par_{m}] = {MEDIDAS[m][ponta]}" for m in medidas)
    colunas = ",\n".join(f'        "{m}", [par_{m}]' for m in medidas)
    if not chaves:
        corpo = f'ROW(\n        "corte", "{corte}",\n        "chave", "{corte}",\n{colunas}\n    )'
        if corte == "estado_b":
            corpo = f"CALCULATETABLE(\n    {corpo},\n    {ESTADO_B[ponta]}\n)"
        return f"// corte: {corte}\nDEFINE\n{define}\nEVALUATE\n    {corpo}\n"
    if ponta == 1 and chave_v2:
        chave = chave_v2
    else:
        chave = " & \"|\" & ".join(chaves) if len(chaves) > 1 else chaves[0]
    # Nas colunas intermediárias o prefixo v_ evita que [margem] seja lida como a medida [Margem],
    # porque nome em DAX não distingue maiúscula de minúscula.
    colunas_v = ",\n".join(f'        "v_{m}", [par_{m}]' for m in medidas)
    extras = ",\n".join(f'    "{m}", [v_{m}]' for m in medidas)
    return (f"// corte: {corte}\nDEFINE\n{define}\nEVALUATE\nSELECTCOLUMNS(\n"
            f"    SUMMARIZECOLUMNS(\n        {', '.join(chaves)},\n{colunas_v}\n    ),\n"
            f'    "corte", "{corte}",\n    "chave", {chave},\n{extras}\n)\nORDER BY [chave]\n')


for ponta, nome in ((0, "v1"), (1, "v2")):
    texto = "\n".join(consulta(c, ponta) for c in CORTES)
    (AQUI / f"consultas_{nome}.dax").write_text(texto, encoding="utf-8")
    print(f"consultas_{nome}.dax: {len(CORTES)} cortes")
