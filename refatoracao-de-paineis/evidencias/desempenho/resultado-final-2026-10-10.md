# Medição final, painel de partida (v1) contra painel reestruturado (v2)

A v2 foi medida em 10-10-2026, já padronizada, sobre a base de 5 milhões de linhas, na máquina
declarada em [`maquina.md`](maquina.md), com o plano de energia em alto desempenho e o Power BI
Desktop 2.158.1304. A v1 não mudou desde a medição de 06-10-2026, feita na mesma máquina e na mesma
base com o Desktop 2.155.756, e os números dela vêm de
[`resultado-final-2026-10-06.md`](resultado-final-2026-10-06.md). O método é o da seção 5 da
[especificação](../metodologia.md), com os desvios declarados no `maquina.md`. Cada célula traz a
mediana e, entre parênteses, a faixa das cinco execuções, e uma diferença só é afirmada quando as
faixas não se sobrepõem.

## Resultado

| Grandeza | v1 | v2 | Variação |
|---|---|---|---|
| tamanho do modelo | 515,2 MB | 134,8 MB | **−74%** |
| tempo de atualização | 84,2 s (82,8 a 85,5) | 59,4 s (58,9 a 62,5) | **−29%** |
| Visão geral, tela, estado A | 432 ms (419 a 452) | 335 ms (313 a 372) | **−22%** |
| Visão geral, tela, estado B | 373 ms (338 a 384) | 389 ms (374 a 408) | sem diferença mensurável |
| Visão geral, consulta a frio, estado A | 594 ms (572 a 680) | 145 ms (139 a 150) | **−76%** |
| Visão geral, consulta a quente, estado A | 236 ms (229 a 238) | 28 ms (28 a 29) | **−88%** |
| Visão geral, consulta a frio, estado B | 207 ms (205 a 217) | 162 ms (159 a 172) | **−22%** |
| Visão geral, consulta a quente, estado B | 94 ms (90 a 96) | 58 ms (54 a 79) | **−38%** |

"Tela" é a renderização a quente lida do analisador de desempenho. "Consulta" é a soma das
consultas DAX da página medida por script, com o cache limpo imediatamente antes de cada execução
a frio.

## Leitura

O modelo encolheu a um quarto e atualiza quase um terço mais rápido. As consultas da Visão geral
ficaram de quatro a oito vezes mais baratas, porque a página passou de 19 consultas sobre uma
tabela plana para 7 consultas sobre um esquema estrela com medidas explícitas. Na tela o ganho é
menor, e no estado B ele desaparece, porque a v2 ganhou a faixa de indicadores com o mês anterior
e a variação, e o chassi novo com cabeçalho e rodapé. Parte do tempo economizado nas consultas foi
reinvestida em informação na tela.

## Limites declarados

A v1 foi medida no Desktop 2.155 e a v2 no 2.158. O protocolo pede as duas na mesma sessão, porque o
Desktop muda a cada versão. O tamanho do modelo é medido no motor e quase não depende da versão, e
a atualização e as consultas da Visão geral mostram diferenças muito maiores que a variação entre
sessões observada nas rodadas de 05-10 e 06-10. Ainda assim, os números de tempo são lidos como
ordem de grandeza.

O Detalhe de vendas fica fora desta tabela de propósito. É uma tabela no grão de linha que lê os 5 milhões de
linhas com ou sem refatoração, e na rodada de 06-10, com as duas pontas na mesma versão, já não
tinha mostrado diferença mensurável. Sem as duas pontas na mesma versão, a comparação dele não se
sustenta.

O detalhe de cada execução está em [`resultados.csv`](resultados.csv). Os JSON exportados pelo
analisador e as consultas extraídas da sessão ficaram fora do repositório, e saem de novo pelo
roteiro de medição do guia técnico.
