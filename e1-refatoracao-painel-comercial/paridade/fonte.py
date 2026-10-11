"""Terceira ponta da paridade: as 16 medidas nos 9 cortes, calculadas direto dos CSV do gerador.

Não usa Power BI. Aplica as regras da seção 4 da ESPECIFICACAO.md sobre a base e grava um CSV por
corte, no mesmo formato que `rodar.ps1` grava para a v1 e a v2, para `comparar.py` cruzar as
três pontas. A inteligência de tempo segue o calendário completo: ano anterior é o mesmo período um
ano antes, e acumulado no ano vai de 1º de janeiro até a última data do contexto.

Uso: python fonte.py <pasta-comercial-da-base> <pasta-de-saida>
"""
import math
import sys
from pathlib import Path

import pandas as pd

base, saida = Path(sys.argv[1]), Path(sys.argv[2])
saida.mkdir(parents=True, exist_ok=True)

f = pd.read_csv(base / "fato_vendas.csv", parse_dates=["data"])
f = f.merge(pd.read_csv(base / "dim_produto.csv")[["produto_id", "categoria"]], on="produto_id")
f = f.merge(pd.read_csv(base / "dim_cliente.csv")[["cliente_id", "porte"]], on="cliente_id")
reg = pd.read_csv(base / "dim_regiao.csv").set_index("regiao")["peso_mercado"]
f["ano_mes"] = f["data"].dt.strftime("%Y-%m")
f["ano"] = f["data"].dt.year
f["mes_idx"] = f["ano"] * 12 + f["data"].dt.month
FIM = f["data"].max()


def soma(s):
    return round(math.fsum(s.tolist()), 6) if len(s) else None


def receita_em(filtros, meses):
    """Receita líquida no conjunto de meses, respeitando os filtros que não são de data."""
    g = f
    for c, v in filtros.items():
        g = g[g[c] == v]
    return soma(g[g["mes_idx"].isin(meses)]["receita_liquida"]) if len(g[g["mes_idx"].isin(meses)]) else None


def medidas(g, filtros, meses, todas_regioes):
    """g: linhas do contexto; filtros: filtros não temporais; meses: meses do contexto."""
    r = {}
    rl = soma(g["receita_liquida"])
    r["receita_bruta"] = soma(g["receita_bruta"])
    r["receita_liquida"] = rl
    r["custo"] = soma(g["custo_total"])
    r["margem"] = soma(g["margem"])
    r["margem_pct"] = r["margem"] / rl if rl else None
    r["quantidade"] = int(g["quantidade"].sum())
    r["linhas"] = len(g)
    r["pedidos"] = g["numero_pedido"].nunique()
    r["ticket_medio"] = rl / r["pedidos"] if r["pedidos"] else None
    r["clientes_com_compra"] = g["cliente_id"].nunique()
    prem = g[g["categoria"] == "Linha Premium"]
    r["receita_premium"] = soma(prem["receita_liquida"]) if len(prem) else None
    aa = receita_em(filtros, [m - 12 for m in meses])
    r["receita_ano_anterior"] = aa
    ultimo = max(meses)
    ytd = [m for m in range((ultimo - 1) // 12 * 12 + 1, ultimo + 1)]
    r["receita_acumulada_ano"] = receita_em(filtros, ytd)
    r["crescimento_pct"] = (rl - aa) / aa if aa else None
    sem_regiao = {k: v for k, v in filtros.items() if k != "regiao"}
    total_regioes = receita_em(sem_regiao, meses)
    r["participacao"] = rl / total_regioes if total_regioes else None
    r["peso_mercado"] = float(reg.sum()) if todas_regioes else float(reg[filtros["regiao"]])
    return r


TODOS_MESES = sorted(f["mes_idx"].unique())
linhas = {c: [] for c in ["total", "ano_mes", "regiao", "categoria", "porte", "vendedor", "cliente",
                          "ano_mes_regiao", "estado_b"]}
linhas["total"].append({"chave": "total", **medidas(f, {}, TODOS_MESES, True)})
for am, g in f.groupby("ano_mes"):
    linhas["ano_mes"].append({"chave": am, **medidas(g, {}, sorted(g["mes_idx"].unique()), True)})
for rg, g in f.groupby("regiao"):
    linhas["regiao"].append({"chave": rg, **medidas(g, {"regiao": rg}, TODOS_MESES, False)})
for cat, g in f.groupby("categoria"):
    linhas["categoria"].append({"chave": cat, **medidas(g, {"categoria": cat}, TODOS_MESES, True)})
for pt, g in f.groupby("porte"):
    linhas["porte"].append({"chave": pt, **medidas(g, {"porte": pt}, TODOS_MESES, True)})
for (am, rg), g in f.groupby(["ano_mes", "regiao"]):
    linhas["ano_mes_regiao"].append({"chave": f"{am}|{rg}", **medidas(g, {"regiao": rg}, sorted(g["mes_idx"].unique()), False)})
gb = f[(f["regiao"] == "Sudeste") & (f["ano"] == 2026)]
linhas["estado_b"].append({"chave": "estado_b", **medidas(gb, {"regiao": "Sudeste"}, sorted(gb["mes_idx"].unique()), False)})

ADITIVAS = ["receita_bruta", "receita_liquida", "custo", "margem", "quantidade", "linhas", "pedidos", "clientes_com_compra"]
for chave_col, corte in (("vendedor_id", "vendedor"), ("cliente_id", "cliente")):
    agg = f.groupby(chave_col).agg(receita_bruta=("receita_bruta", soma), receita_liquida=("receita_liquida", soma),
                                   custo=("custo_total", soma), margem=("margem", soma), quantidade=("quantidade", "sum"),
                                   linhas=("receita_liquida", "size"), pedidos=("numero_pedido", "nunique"),
                                   clientes_com_compra=("cliente_id", "nunique")).reset_index()
    agg = agg.rename(columns={chave_col: "chave"})
    linhas[corte] = agg[["chave"] + ADITIVAS].to_dict("records")

TEMPO = ["receita_ano_anterior", "receita_acumulada_ano", "crescimento_pct"]
for corte, regs in linhas.items():
    df = pd.DataFrame(regs)
    if corte in ("regiao", "categoria", "porte"):
        df = df.drop(columns=TEMPO)
    df.insert(0, "corte", corte)
    df.sort_values("chave").to_csv(saida / f"{corte}.csv", index=False)
    print(f"{corte}: {len(df)} linhas")
print(f"fonte: janela ate {FIM.date()}, {len(f)} linhas de venda")
