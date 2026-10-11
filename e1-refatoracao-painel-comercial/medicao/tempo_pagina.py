"""Tempo de página a partir do JSON exportado pelo analisador de desempenho do Power BI Desktop.

Cada ação do usuário (atualizar visuais, trocar de página) abre um bloco. O tempo do bloco é o fim
do último evento menos o início da ação. O script também soma o tempo das consultas DAX e conta
quantas consultas o bloco disparou.

Uso: python tempo_pagina.py <arquivo.json>
"""
import json
import sys
from collections import Counter
from datetime import datetime


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def blocos(eventos):
    acoes = sorted((e for e in eventos if e["name"] == "User Action"), key=lambda e: e["start"])
    acoes = [a for a in acoes if a["metrics"].get("sourceLabel") != "UserAction_StartedMonitoring"]
    resto = [e for e in eventos if e["name"] != "User Action" and "end" in e]
    for i, a in enumerate(acoes):
        ini = ts(a["start"])
        fim_janela = ts(acoes[i + 1]["start"]) if i + 1 < len(acoes) else None
        dentro = [e for e in resto
                  if ts(e["start"]) >= ini and (fim_janela is None or ts(e["start"]) < fim_janela)]
        if not dentro:
            continue
        fim = max(ts(e["end"]) for e in dentro)
        visuais = {e["metrics"].get("visualId") for e in dentro
                   if e["name"] == "Visual Container Lifecycle"}
        prefixos = Counter((v or "")[:2] for v in visuais)
        dax = [e for e in dentro if e["name"] == "Execute DAX Query"]
        yield {
            "acao": a["metrics"].get("sourceLabel", "").replace("UserAction_", ""),
            "inicio": a["start"],
            "prefixo_visual": prefixos.most_common(1)[0][0] if prefixos else "",
            "visuais": len(visuais),
            "tempo_ms": round((fim - ini).total_seconds() * 1000),
            "consultas_dax": len(dax),
            "dax_ms": round(sum((ts(e["end"]) - ts(e["start"])).total_seconds() * 1000 for e in dax)),
        }


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8-sig") as f:
        dados = json.load(f)
    print("acao;inicio;prefixo_visual;visuais;tempo_ms;consultas_dax;dax_ms")
    for b in blocos(dados["events"]):
        print(";".join(str(b[k]) for k in
                       ("acao", "inicio", "prefixo_visual", "visuais", "tempo_ms", "consultas_dax", "dax_ms")))
