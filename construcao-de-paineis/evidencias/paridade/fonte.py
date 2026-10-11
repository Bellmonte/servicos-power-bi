"""Ponta da base: as 20 medidas do levantamento nos 9 cortes, calculadas direto dos CSV do gerador.

Não usa Power BI. Aplica a regra de negócio de cada indicador, como está escrita no levantamento,
sobre os arquivos da base, e grava um CSV por corte no mesmo formato que o `rodar.ps1` grava a partir
do modelo, para o `comparar.py` cruzar as duas pontas.

Regras de tempo, iguais às do calendário do modelo: o período de cada linha é o conjunto de meses
do corte (todos os meses da base quando o corte não filtra data); o ano anterior é o mesmo conjunto
deslocado doze meses, e fica vazio quando esse conjunto não está inteiro na base; o acumulado no ano vai de 1º de janeiro até a última data do período; e a
referência das medidas de clientes é a última data do período, que é o fim do mês ou o fim da base.

Uso: python fonte.py <pasta-comercial-da-base> <pasta-de-saida>
"""
import csv
import json
import math
import sys
from pathlib import Path

import pandas as pd

from medidas import CORTES, FILTROS, MEDIDAS

base, saida = Path(sys.argv[1]), Path(sys.argv[2])
saida.mkdir(parents=True, exist_ok=True)

manifesto = json.loads((base / "_manifesto.json").read_text(encoding="utf-8"))
FIM_BASE = pd.Timestamp(manifesto["parametros"]["hoje"])

f = pd.read_csv(base / "fato_vendas.csv", parse_dates=["data"],
                usecols=["data", "produto_id", "cliente_id", "vendedor_id", "regiao", "quantidade",
                         "receita_bruta", "receita_liquida", "custo_total", "margem", "numero_pedido"])
f = f.merge(pd.read_csv(base / "dim_produto.csv", usecols=["produto_id", "categoria"]), on="produto_id")
f = f.merge(pd.read_csv(base / "dim_cliente.csv", usecols=["cliente_id", "porte"]), on="cliente_id")
f = f.rename(columns={"categoria": "linha"})
f["ano"] = f["data"].dt.year
f["mes_idx"] = f["ano"] * 12 + f["data"].dt.month - 1
f["ano_mes"] = f["data"].dt.strftime("%Y-%m")
TODOS_MESES = sorted(f["mes_idx"].unique())


def soma(s):
    return math.fsum(s.tolist()) if len(s) else None


def fim_do_mes(mes_idx):
    ano, mes = divmod(mes_idx, 12)
    return min(pd.Timestamp(ano, mes + 1, 1) + pd.offsets.MonthEnd(0), FIM_BASE)


def mascara(filtros):
    m = pd.Series(True, index=f.index)
    for col, val in filtros.items():
        m &= f[col] == val
    return m


def receita(g, meses):
    s = g[g["mes_idx"].isin(meses)]
    return soma(s["receita_liquida"])


def margem_pct(g, meses):
    s = g[g["mes_idx"].isin(meses)]
    rl = soma(s["receita_liquida"])
    return soma(s["margem"]) / rl if rl else None


def medidas(fora_data, meses, escopo_receita):
    """fora_data: linhas que passam pelos filtros que não são de data; meses: meses do período;
    escopo_receita: receita líquida de tudo o que está selecionado, denominador da participação."""
    g = fora_data[fora_data["mes_idx"].isin(meses)]
    r = {}
    rb, rl = soma(g["receita_bruta"]), soma(g["receita_liquida"])
    r["receita_bruta"], r["receita_liquida"] = rb, rl
    r["participacao"] = rl / escopo_receita if rl is not None and escopo_receita else None
    r["desconto"] = rb - rl if rb is not None else None
    r["desconto_pct"] = r["desconto"] / rb if rb else None
    r["custo"] = soma(g["custo_total"])
    r["margem"] = soma(g["margem"])
    r["margem_pct"] = r["margem"] / rl if rl else None
    r["pedidos"] = g["numero_pedido"].nunique() if len(g) else None
    r["quantidade"] = int(g["quantidade"].sum()) if len(g) else None
    r["ticket_medio"] = rl / r["pedidos"] if r["pedidos"] else None
    r["clientes_ativos"] = g["cliente_id"].nunique() if len(g) else None

    ref = fim_do_mes(max(meses))
    ano12 = fora_data[(fora_data["data"] > ref - pd.Timedelta(days=365)) & (fora_data["data"] <= ref)]
    dias90 = ano12[ano12["data"] > ref - pd.Timedelta(days=90)]
    base12 = set(ano12["cliente_id"])
    sem90 = base12 - set(dias90["cliente_id"])
    r["base_clientes_12m"] = len(base12) or None
    r["clientes_sem_compra_90d"] = len(sem90) or None
    r["clientes_sem_compra_90d_pct"] = len(sem90) / len(base12) if base12 and sem90 else None

    # o ano anterior só existe quando o período deslocado está inteiro dentro da base
    anteriores = [m - 12 for m in meses] if all(m - 12 in TODOS_MESES for m in meses) else []
    aa = receita(fora_data, anteriores) if anteriores else None
    r["receita_ano_anterior"] = aa
    r["crescimento_pct"] = (((rl or 0) - aa) / aa) if aa else None
    maa = margem_pct(fora_data, anteriores) if anteriores else None
    r["margem_ano_anterior_pct"] = maa
    r["variacao_margem_pp"] = (r["margem_pct"] - maa) * 100 if maa is not None and r["margem_pct"] is not None else None
    ultimo = max(meses)
    r["receita_acumulada_ano"] = receita(fora_data, list(range(ultimo // 12 * 12, ultimo + 1)))
    return r


def grava(corte, linhas, nomes):
    with open(saida / f"{corte}.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["corte", "chave"] + nomes)
        for chave, r in linhas:
            w.writerow([corte, chave] + ["" if r[n] is None else repr(float(r[n])) for n in nomes])
    print(f"{corte}: {len(linhas)} linhas")


for corte, (nomes, grupo) in CORTES.items():
    filtro = FILTROS.get(corte, {})
    meses_filtro = sorted(f.loc[mascara(filtro), "mes_idx"].unique()) if "ano" in filtro else TODOS_MESES
    fora_filtro = {k: v for k, v in filtro.items() if k != "ano"}
    escopo = f[mascara(fora_filtro)]
    escopo_receita = receita(escopo, meses_filtro)
    linhas = []
    if corte == "cliente":
        # 20 mil clientes: só somas e contagens, calculadas de uma vez por agrupamento
        g = f.groupby("cliente_id")
        tab = pd.DataFrame({
            "receita_bruta": g["receita_bruta"].apply(lambda s: math.fsum(s.tolist())),
            "receita_liquida": g["receita_liquida"].apply(lambda s: math.fsum(s.tolist())),
            "custo": g["custo_total"].apply(lambda s: math.fsum(s.tolist())),
            "margem": g["margem"].apply(lambda s: math.fsum(s.tolist())),
            "pedidos": g["numero_pedido"].nunique(),
            "quantidade": g["quantidade"].sum(),
        })
        tab["desconto"] = tab["receita_bruta"] - tab["receita_liquida"]
        tab["clientes_ativos"] = 1
        linhas = [(str(k), r) for k, r in tab.to_dict("index").items()]
    elif not grupo:
        linhas = [("total", medidas(escopo, meses_filtro, escopo_receita))]
    else:
        temporal = "ano_mes" in grupo
        atributos = [c for c in grupo if c != "ano_mes"]
        chaves = (escopo[grupo].drop_duplicates().sort_values(grupo).itertuples(index=False, name=None))
        for chave in chaves:
            valores = dict(zip(grupo, chave))
            fora_data = escopo[mascara({c: valores[c] for c in atributos})] if atributos else escopo
            if temporal:
                ano, mes = map(int, valores["ano_mes"].split("-"))
                meses = [ano * 12 + mes - 1]
            else:
                meses = meses_filtro
            linhas.append(("|".join(str(v) for v in chave), medidas(fora_data, meses, escopo_receita)))
    grava(corte, linhas, nomes)
