"""Extrai as consultas DAX de uma página a partir do JSON do analisador de desempenho do Desktop.

O evento "Execute DAX Query" traz o texto da consulta, e o visual que a disparou é achado subindo a
cadeia de parentId até o evento "Visual Container Lifecycle". Fica a última consulta de cada visual.
A página é reconhecida pelo prefixo do nome do visual (vg Visão geral, cv Clientes e vendedores,
ct Clientes por trimestre, dv Detalhe de vendas). A saída é o arquivo que medir_consultas.ps1 lê.

Uso: python extrai_consultas.py <analisador.json> <prefixo> <saida.dax>
"""
import sys
from pathlib import Path
import json

arq, prefixo, saida = sys.argv[1], sys.argv[2], Path(sys.argv[3])
ev = json.loads(Path(arq).read_text(encoding="utf-8-sig"))["events"]
por_id = {e.get("id"): e for e in ev}


def visual_de(e):
    while e is not None:
        vid = e.get("metrics", {}).get("visualId")
        if e["name"] == "Visual Container Lifecycle" and vid:
            return vid
        e = por_id.get(e.get("parentId"))
    return None


ultima = {}
for e in sorted((e for e in ev if e["name"] == "Execute DAX Query"), key=lambda e: e["start"]):
    texto = e.get("metrics", {}).get("QueryText")
    vid = visual_de(e)
    if texto and vid and vid.startswith(prefixo):
        ultima[vid] = texto.strip()

saida.parent.mkdir(parents=True, exist_ok=True)
saida.write_text("\n\n".join(f"// consulta: {vid}\n{txt}" for vid, txt in sorted(ultima.items())) + "\n", encoding="utf-8")
print(f"{saida.name}: {len(ultima)} consultas de visuais com prefixo {prefixo}")
