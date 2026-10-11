# Paridade em 1 milhão de linhas, 27-09-2026

As 16 medidas da seção 4 da especificação foram conferidas nos 9 cortes da seção 6, em três pontas:
a base de origem (calculada direto dos CSV por `fonte.py`), o painel de partida (v1) e o painel
reestruturado (v2), cada modelo aberto no Power BI Desktop e consultado por `rodar.ps1`. A comparação foi feita por `comparar.py`, com
tolerância exata para contagem, R$ 0,01 para valor e 1e-6 para razão.

| Corte | Comparações | Divergências |
|---|---|---|
| total | 48 | 0 |
| ano_mes | 1.728 | 0 |
| regiao | 195 | 0 |
| categoria | 117 | 0 |
| porte | 117 | 0 |
| vendedor | 3.600 | 0 |
| cliente | 480.000 | 0 |
| ano_mes_regiao | 8.640 | 0 |
| estado_b | 48 | 0 |
| **total** | **494.493** | **0** |

A v2 dá os mesmos números da v1 e da origem em todos os cortes acordados. O detalhe linha a
linha ficou fora do repositório, numa pasta local, e sai de novo pelos scripts desta pasta.

## O defeito que a refatoração encontrou

Fora dos cortes acordados, a v1 tem um erro que ninguém plantou. As medidas de tempo usam
`SAMEPERIODLASTYEAR` sobre a data do próprio fato, e com filtro de vendedor, cliente ou produto os
dias do período deixam de ser contínuos, porque nem todo vendedor vende todo dia. Nesse caso o
motor recusa o cálculo.

Conferido nos dois modelos abertos, com o vendedor 74 em agosto de 2026, mês em que ele vendeu em
23 dos 31 dias:

| Ponta | Receita do ano anterior |
|---|---|
| v1 | erro de cálculo: a função espera uma seleção contígua de datas |
| v2 | R$ 269.893,41 |

Na v1, isso aparece como visual com erro assim que alguém escolhe um vendedor na
segmentação da Visão geral junto com um mês. Na v2, o calendário marcado como tabela de data
resolve o período completo, que é a regra escrita na seção 4. Esse é o argumento mais forte do
episódio: a refatoração, além de deixar o painel mais leve, corrigiu um número que quem usava a v1 não
conseguia ver.
