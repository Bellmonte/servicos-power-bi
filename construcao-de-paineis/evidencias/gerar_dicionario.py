"""Gera o dicionário de medidas do painel comercial a partir do modelo semântico.

Lê painel/painel-comercial.SemanticModel/definition/tables/Medidas.tmdl e grava
dicionario-de-medidas.md na pasta do caso. O modelo é a fonte: o dicionário nunca
é editado à mão, e qualquer mudança de regra entra no TMDL e o arquivo é regerado.

Uso, a partir da pasta construcao-de-paineis:
    python evidencias/gerar_dicionario.py

Só biblioteca padrão. Para quando a descrição de uma medida visível não segue o
contrato de três partes (o que é, "Use ...", "Não use ..."), em vez de gerar um
dicionário incompleto em silêncio.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

CASO = Path(__file__).resolve().parent.parent
DEFINICAO = CASO / "painel" / "painel-comercial.SemanticModel" / "definition"
MEDIDAS = DEFINICAO / "tables" / "Medidas.tmdl"
FATO = DEFINICAO / "tables" / "Fact_Vendas.tmdl"
SAIDA = CASO / "dicionario-de-medidas.md"
COMANDO = "python evidencias/gerar_dicionario.py"

# Nome técnico em ASCII para nome de negócio: troca palavra a palavra e passa para
# caixa de frase. Palavra nova sem acento que precise de um entra aqui.
ACENTOS = {
    "Liquida": "Líquida",
    "Medio": "Médio",
    "Participacao": "Participação",
    "Variacao": "Variação",
    "Periodo": "Período",
    "Regiao": "Região",
    "Mes": "Mês",
}

# Unidade pelo sufixo do nome; sem sufixo, pelo formato.
UNIDADE_POR_SUFIXO = {
    "(R$)": "reais (R$)",
    "(%)": "percentual",
    "(un)": "unidades",
    "(p.p.)": "pontos percentuais",
}
UNIDADE_POR_FORMATO = {
    "#,0": "contagem",
    "0": "contagem",
}


@dataclass
class Medida:
    nome: str
    descricao: str = ""
    expressao: list[str] = field(default_factory=list)
    formato: str = ""
    pasta: str = ""
    oculta: bool = False


def ler_nome(cabecalho: str) -> tuple[str, str]:
    """Separa o nome da medida e o que vem depois do '='."""
    resto = cabecalho[len("measure "):]
    if resto.startswith("'"):
        i, nome = 1, []
        while i < len(resto):
            if resto[i] == "'":
                if i + 1 < len(resto) and resto[i + 1] == "'":
                    nome.append("'")
                    i += 2
                    continue
                break
            nome.append(resto[i])
            i += 1
        nome_txt, depois = "".join(nome), resto[i + 1:]
    else:
        nome_txt, _, depois = resto.partition(" ")
        depois = " " + depois
    depois = depois.strip()
    if depois.startswith("="):
        depois = depois[1:].strip()
    return nome_txt, depois


def ler_medidas(caminho: Path) -> list[Medida]:
    linhas = caminho.read_text(encoding="utf-8-sig").splitlines()
    medidas: list[Medida] = []
    descricao: list[str] = []
    atual: Medida | None = None
    na_expressao = False
    for linha in linhas:
        if linha.startswith("\t///"):
            descricao.append(linha.strip()[3:].strip())
            continue
        if linha.startswith("\tmeasure "):
            nome, depois = ler_nome(linha[1:])
            atual = Medida(nome=nome, descricao=" ".join(descricao).strip())
            if depois:
                atual.expressao.append(depois)
                na_expressao = False
            else:
                na_expressao = True
            medidas.append(atual)
            descricao = []
            continue
        if linha.startswith("\t") and not linha.startswith("\t\t") and linha.strip():
            # outro objeto no nível da tabela (partição, anotação): fecha a medida
            atual, na_expressao, descricao = None, False, []
            continue
        if atual is None:
            continue
        if na_expressao and linha.startswith("\t\t\t"):
            atual.expressao.append(linha[3:])
            continue
        if linha.startswith("\t\t") and not linha.startswith("\t\t\t"):
            na_expressao = False
            prop = linha.strip()
            if prop.startswith("formatString:"):
                atual.formato = prop.split(":", 1)[1].strip()
            elif prop.startswith("displayFolder:"):
                atual.pasta = prop.split(":", 1)[1].strip()
            elif prop == "isHidden":
                atual.oculta = True
            elif prop.startswith("formatStringDefinition"):
                atual.formato = atual.formato or "formato dinâmico"
    return medidas


def partes_da_descricao(m: Medida) -> tuple[str, str, str]:
    """Quebra a descrição em definição, quando usar e quando não usar."""
    achado = re.search(r"^(.*?\.)\s+(Use\s.*?\.)\s+(Não use\s.*)$", m.descricao)
    if not achado:
        raise SystemExit(
            f"ERRO: a descrição de '{m.nome}' não segue o contrato de três partes "
            f"(o que é. Use ... . Não use ... .). Corrija o Medidas.tmdl e rode de novo."
        )
    return tuple(p.strip() for p in achado.groups())  # type: ignore[return-value]


def nome_de_negocio(tecnico: str) -> str:
    palavras = [ACENTOS.get(p, p) for p in tecnico.split(" ")]
    frase = [palavras[0]] + [
        p if p.startswith("(") or p.isupper() or any(c.isdigit() for c in p) else p.lower()
        for p in palavras[1:]
    ]
    return " ".join(frase)


def unidade(m: Medida) -> str:
    for sufixo, texto in UNIDADE_POR_SUFIXO.items():
        if m.nome.endswith(sufixo):
            return texto
    if m.formato in UNIDADE_POR_FORMATO:
        return UNIDADE_POR_FORMATO[m.formato]
    raise SystemExit(f"ERRO: sem unidade para '{m.nome}' (formato '{m.formato}'). Ajuste o mapa no script.")


def grao_da_fato() -> str:
    """Primeira frase da descrição da tabela de fato, que declara o grão."""
    if not FATO.exists():
        return ""
    desc = []
    for linha in FATO.read_text(encoding="utf-8-sig").splitlines():
        if linha.startswith("///"):
            desc.append(linha[3:].strip())
        elif linha.startswith("table "):
            break
    return " ".join(desc)


def celula(texto: str) -> str:
    return texto.replace("|", "\\|")


def montar(medidas: list[Medida]) -> str:
    visiveis = [m for m in medidas if not m.oculta]
    suporte = [m for m in medidas if m.oculta]
    pastas: dict[str, list[Medida]] = {}
    for m in visiveis:
        if not m.pasta:
            raise SystemExit(f"ERRO: medida visível '{m.nome}' sem pasta de exibição.")
        pastas.setdefault(m.pasta, []).append(m)

    saida: list[str] = []
    s = saida.append
    s("# Dicionário de medidas do painel comercial")
    s("")
    s("> Arquivo gerado a partir do modelo semântico "
      "(`painel/painel-comercial.SemanticModel/definition/tables/Medidas.tmdl`). "
      "Não edite à mão: a regra muda no modelo e este arquivo é regerado, a partir da pasta "
      f"`construcao-de-paineis`, com `{COMANDO}`.")
    s("")
    grao = grao_da_fato()
    texto_grao = f" {grao}" if grao else ""
    s(f"Todas as medidas partem da tabela de fato `Fact_Vendas`.{texto_grao} Cada número respeita os "
      "filtros e segmentações que estiverem na tela, e as razões são sempre refeitas sobre as somas do "
      f"recorte. São {len(visiveis)} medidas de negócio em {len(pastas)} pastas, na ordem em que aparecem "
      "no painel de campos do Power BI.")
    s("")
    s("| Pasta | Medidas |")
    s("|---|---|")
    for pasta, lista in pastas.items():
        s(f"| {celula(pasta)} | {', '.join(nome_de_negocio(m.nome) for m in lista)} |")
    s("")
    for pasta, lista in pastas.items():
        s(f"## {pasta}")
        s("")
        for m in lista:
            definicao, quando, quando_nao = partes_da_descricao(m)
            s(f"### {nome_de_negocio(m.nome)}")
            s("")
            s("| Campo | Conteúdo |")
            s("|---|---|")
            s(f"| Nome técnico | `{celula(m.nome)}` |")
            s(f"| Unidade | {unidade(m)} |")
            s(f"| Formato | `{celula(m.formato)}` |")
            s("")
            s(f"**Definição.** {definicao}")
            s("")
            s(f"**Quando usar.** {quando}")
            s("")
            s(f"**Quando não usar.** {quando_nao}")
            s("")
            s("```dax")
            s("\n".join(m.expressao).rstrip())
            s("```")
            s("")
    if suporte:
        s("## Medidas de suporte de tela")
        s("")
        s("As medidas abaixo ficam ocultas, começam com ponto e devolvem texto pronto para um elemento de "
          "tela, como o valor abreviado de um cartão ou o rodapé. Elas não entram em cálculo, comparação, "
          "exportação nem na conferência de paridade, e por isso aparecem aqui só pelo nome e pela função.")
        s("")
        s("| Nome técnico | Pasta | Para que serve |")
        s("|---|---|---|")
        for m in suporte:
            definicao = partes_da_descricao(m)[0]
            s(f"| `{celula(m.nome)}` | {celula(m.pasta)} | {celula(definicao)} |")
        s("")
    return "\n".join(saida)


def main() -> int:
    if not MEDIDAS.exists():
        print(f"ERRO: não achei {MEDIDAS}", file=sys.stderr)
        return 1
    medidas = ler_medidas(MEDIDAS)
    if not medidas:
        print("ERRO: nenhuma medida lida do Medidas.tmdl", file=sys.stderr)
        return 1
    texto = montar(medidas)
    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    visiveis = sum(1 for m in medidas if not m.oculta)
    print(f"{SAIDA.name}: {visiveis} medidas de negócio, {len(medidas) - visiveis} de suporte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
