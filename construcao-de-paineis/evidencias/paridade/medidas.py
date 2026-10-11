"""Lista única das medidas e dos cortes da paridade, lida pelo `fonte.py`, pelo `gera_consultas.py`
e pelo `comparar.py`, para as três ferramentas nunca divergirem entre si.

Cada medida tem o nome curto usado nos CSV, o nome no modelo e o tipo, que define a tolerância:
contagem precisa ser igual, valor em reais pode diferir até R$ 0,01 e razão até 0,000001.
"""

MEDIDAS = {
    "receita_bruta": ("Receita Bruta (R$)", "valor"),
    "receita_liquida": ("Receita Liquida (R$)", "valor"),
    "participacao": ("Participacao na Receita (%)", "razao"),
    "desconto": ("Desconto Concedido (R$)", "valor"),
    "desconto_pct": ("Desconto Medio (%)", "razao"),
    "custo": ("Custo (R$)", "valor"),
    "margem": ("Margem (R$)", "valor"),
    "margem_pct": ("Margem (%)", "razao"),
    "pedidos": ("Pedidos", "contagem"),
    "quantidade": ("Quantidade (un)", "contagem"),
    "ticket_medio": ("Ticket Medio (R$)", "valor"),
    "clientes_ativos": ("Clientes Ativos", "contagem"),
    "base_clientes_12m": ("Base de Clientes 12 Meses", "contagem"),
    "clientes_sem_compra_90d": ("Clientes sem Compra 90 Dias", "contagem"),
    "clientes_sem_compra_90d_pct": ("Clientes sem Compra 90 Dias (%)", "razao"),
    "receita_ano_anterior": ("Receita Ano Anterior (R$)", "valor"),
    "crescimento_pct": ("Crescimento sobre Ano Anterior (%)", "razao"),
    "margem_ano_anterior_pct": ("Margem Ano Anterior (%)", "razao"),
    "variacao_margem_pp": ("Variacao Margem sobre Ano Anterior (p.p.)", "razao"),
    "receita_acumulada_ano": ("Receita Acumulada no Ano (R$)", "valor"),
}

TODAS = list(MEDIDAS)
# Por cliente só entram as somas e contagens que têm leitura num cliente isolado.
POR_CLIENTE = ["receita_bruta", "receita_liquida", "desconto", "custo", "margem", "pedidos", "quantidade",
               "clientes_ativos"]

# corte -> (medidas, agrupamento). O agrupamento é a lista de atributos do corte, na ordem da chave;
# "ano_mes" vira AAAA-MM. O filtro do corte, quando existe, está em FILTROS.
CORTES = {
    "total": (TODAS, []),
    "ano_mes": (TODAS, ["ano_mes"]),
    "regiao": (TODAS, ["regiao"]),
    "linha": (TODAS, ["linha"]),
    "porte": (TODAS, ["porte"]),
    "vendedor": (TODAS, ["vendedor_id"]),
    "cliente": (POR_CLIENTE, ["cliente_id"]),
    "ano_mes_regiao": (TODAS, ["ano_mes", "regiao"]),
    "ano_2026_linha": (TODAS, ["linha"]),
}
FILTROS = {"ano_2026_linha": {"ano": 2026}}
