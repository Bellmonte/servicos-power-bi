# Paridade de 11-10-2026

Rodada que fecha o critério 3 do [levantamento](../../levantamento-de-indicadores.md): os 20 indicadores
calculados pela conta direta nos arquivos da base e pelo modelo do painel aberto no Power BI Desktop
2.158, comparados em nove cortes.

**Base:** 1 milhão de linhas de venda, gerada com `--hoje 2026-08-31 --meses 36 --linhas 1000000
--clientes 20000 --produtos 1500 --vendedores 150 --colunas-origem`. O manifesto registra receita
líquida de R$ 2.121.440.181,12, e o modelo carregou o mesmo valor e as mesmas 1.000.000 de linhas.

## Resultado

| Corte | Linhas | Comparações | Divergências |
|---|---|---|---|
| total | 1 | 20 | 0 |
| ano-mês | 36 | 720 | 0 |
| região | 5 | 100 | 0 |
| linha de produto | 3 | 60 | 0 |
| porte | 3 | 60 | 0 |
| vendedor | 150 | 3.000 | 0 |
| cliente | 20.000 | 160.000 | 0 |
| ano-mês por região | 180 | 3.600 | 0 |
| linha de produto em 2026 | 3 | 60 | 0 |
| **total** | | **167.620** | **0** |

A maior diferença encontrada foi de R$ 0,0000005, no acumulado do ano, que é ordem de soma em ponto
flutuante e fica muito abaixo da tolerância de R$ 0,01. As contagens bateram exatamente, e as
diferenças em razões e pontos percentuais ficaram abaixo de 0,000000000001.

Das comparações, 960 são vazio dos dois lados, e todas são esperadas pela regra escrita na seção 3 do levantamento:
936 vêm das quatro medidas de ano anterior (234 cada) nas linhas em que o período deslocado não
está inteiro na base, e 24 vêm das duas medidas de clientes sem compra há 90 dias (12 cada) no
começo da base, quando todo cliente com compra no ano também tinha comprado no trimestre. As
medidas de ano anterior têm 147 comparações com valor nos dois lados cada uma, o que prova o
deslocamento de calendário e a regra do período incompleto ao mesmo tempo.

A rodada foi repetida no mesmo dia com o painel na forma final, depois dos ajustes de layout e das
medidas de texto dos cartões, e deu o mesmo resultado: zero divergência em 167.620 comparações.

## Como refazer

O passo a passo está no [guia técnico](../README.md#paridade). O detalhe célula a célula sai no CSV
indicado pelo `comparar.py`, fora do repositório, porque o `.gitignore` não versiona CSV.
