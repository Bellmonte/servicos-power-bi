# Paridade em 1 milhão de linhas depois do redesenho, 05-10-2026

O redesenho visual mexeu no tema, nos formatos do modelo e no layout das páginas, e a base
foi regerada com os rótulos acentuados. Esta rodada confere que nenhum número mudou com isso. As 16
medidas da seção 4 da especificação foram conferidas nos 9 cortes da seção 6 entre a base de origem,
calculada direto dos CSV por `fonte.py`, e o painel reestruturado (v2), aberto e atualizado no Power BI Desktop e
consultado por `rodar.ps1`. As tolerâncias são as mesmas da rodada de 27-09-2026.

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

A v2 redesenhada dá os mesmos números da origem em todos os cortes acordados. O painel de partida (v1)
ficou fora desta rodada porque o redesenho não tocou nele e a regeração da base mudou só rótulo, sem mexer em
valor, e a equivalência entre a v1 e a origem segue a da rodada de 27-09-2026. O detalhe linha a linha
ficou fora do repositório, numa pasta local, e sai de novo pelos scripts desta pasta.
