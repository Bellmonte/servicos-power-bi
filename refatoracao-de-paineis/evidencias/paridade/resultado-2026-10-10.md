# Paridade em 5 milhões de linhas depois da padronização, 10-10-2026

A v2 foi reconstruída no padrão de desenvolvimento da B&B: modelo em estrela com `Fact_` e `Dim_`,
tabela `Medidas`, calendário gerado por função e ano anterior por `DATEADD`. As 16 medidas da seção 4
da especificação mudaram de nome, de tabela e, em duas delas, de forma. Esta rodada confere que
nenhum resultado mudou com isso, comparando a base de origem, calculada direto dos CSV por
`fonte.py`, com a v2 aberta e atualizada no Power BI Desktop 2.158 e consultada por `rodar.ps1`.
É a primeira rodada na base de 5 milhões, que é a base da medição final. As tolerâncias são as da
seção 6.

| Corte | Comparações | Divergências |
|---|---|---|
| total | 16 | 0 |
| ano_mes | 576 | 0 |
| regiao | 65 | 0 |
| categoria | 39 | 0 |
| porte | 39 | 0 |
| vendedor | 1.200 | 0 |
| cliente | 160.000 | 0 |
| ano_mes_regiao | 2.880 | 0 |
| estado_b | 16 | 0 |
| **total** | **164.831** | **0** |

A v2 padronizada dá os mesmos números da origem em todos os cortes acordados, inclusive na chave de
ano e mês, que agora é montada a partir do calendário novo. O painel de partida (v1) não mudou e
segue com a equivalência das rodadas anteriores. O detalhe linha a linha ficou fora do
repositório, numa pasta local, e sai de novo pelos scripts desta pasta.
