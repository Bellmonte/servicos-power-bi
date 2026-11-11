# Medição final, painel de partida (v1) contra painel reestruturado (v2)

Sessão de medição final, em 06-10-2026, sobre a base de 5 milhões de linhas, na máquina declarada em
[`maquina.md`](maquina.md), com o plano de energia em alto desempenho e o Power BI Desktop 2.155.756.
O método é o da seção 5 da [metodologia](../metodologia.md), com os desvios declarados no
`maquina.md`. Cada célula traz a mediana e, entre parênteses, a faixa das cinco execuções. Uma
diferença só é afirmada quando as faixas da v1 e da v2 não se sobrepõem.

## Resumo

| Grandeza | v1 | v2 | Variação |
|---|---|---|---|
| tamanho do modelo | 515,2 MB | 134,8 MB | **−74%** |
| tempo de atualização | 84,2 s (82,8 a 85,5) | 61,9 s (60,1 a 68,0) | **−27%** |
| Visão geral, tela, estado A | 432 ms (419 a 452) | 254 ms (245 a 264) | **−41%** |
| Visão geral, tela, estado B | 373 ms (338 a 384) | 233 ms (220 a 253) | **−38%** |
| Visão geral, consulta a frio, estado A | 594 ms (572 a 680) | 109 ms (104 a 111) | **−82%** |
| Visão geral, consulta a quente, estado A | 236 ms (229 a 238) | 20 ms (20 a 21) | **−92%** |
| Visão geral, consulta a frio, estado B | 207 ms (205 a 217) | 81 ms (81 a 83) | **−61%** |
| Visão geral, consulta a quente, estado B | 94 ms (90 a 96) | 22 ms (21 a 22) | **−77%** |
| Detalhe de vendas, tela, estado A | 6.735 ms (6.606 a 7.480) | 6.066 ms (6.006 a 7.279) | sem diferença mensurável |
| Detalhe de vendas, tela, estado B | 465 ms (445 a 476) | 486 ms (470 a 499) | sem diferença mensurável |
| Detalhe de vendas, consulta a frio, estado A | 7.742 ms (7.717 a 8.354) | 7.697 ms (7.598 a 7.821) | sem diferença mensurável |
| Detalhe de vendas, consulta a quente, estado A | 6.038 ms (5.837 a 6.191) | 5.718 ms (5.660 a 5.753) | −5% |
| Detalhe de vendas, consulta a frio, estado B | 510 ms (476 a 526) | 460 ms (455 a 464) | −10% |
| Detalhe de vendas, consulta a quente, estado B | 375 ms (367 a 407) | 346 ms (344 a 366) | −8%, com as faixas encostando |

"Tela" é a renderização a quente lida do analisador de desempenho, do início da ação ao fim do
último visual. "Consulta" é a soma das consultas DAX da página medida por script, com o cache
limpo imediatamente antes de cada execução a frio.

## Leitura

O modelo encolheu a um quarto e atualiza um quarto mais rápido. O tamanho caiu quase todo no
dicionário, de 246 MB para 15 MB, porque as colunas calculadas de lucro e margem saíram (D3), as
colunas de alta cardinalidade sem uso saíram ou mudaram de tipo (D2) e os atributos das dimensões
deixaram de se repetir em cada linha do fato (D1).

A Visão geral é onde quem usa o painel sente a diferença. A página passou de 22 visuais e 19 consultas
para 13 visuais e 6 consultas (D6), e as consultas que sobraram são explícitas e baratas (D4 e
D5). Na tela, a página abre em cerca de 40% menos tempo nos dois estados de filtro.

O Detalhe de vendas, a página mais lenta e por isso a de referência, praticamente não mudou. O
ensaio de 27-09-2026 já previa isso: a tabela no grão de linha custa o mesmo para ler cinco
milhões de linhas, com ou sem refatoração, e o que poderia mudar ali é o desenho da página, com
paginação ou filtro obrigatório, o que fica fora do escopo de uma refatoração que preserva o
comportamento. Isso entra no README como limite declarado do serviço.

## Notas da sessão

**Duas noites.** O estado A da v1 foi lido no analisador em 05-10-2026. Como o Desktop foi
reaberto em 06-10-2026, o tamanho, a atualização e as consultas da v1 foram refeitos nesse dia, e
os números da tabela são todos de 06-10, exceto a tela da v1 no estado A, que é de 05-10, na mesma
máquina e na mesma versão do Desktop. A atualização e as consultas medidas nas duas noites
ficaram dentro da mesma faixa.

**Tamanho depois da atualização.** Logo depois de reabrir o arquivo, antes de atualizar, a v1
mediu 474,6 MB, porque o dicionário volta do disco mais compacto. O protocolo lê o tamanho depois
de uma atualização completa, conferida por uma segunda, e as duas pontas seguiram esse critério.

**Execução sem consulta.** Uma das atualizações de visuais do Detalhe de vendas da v2 no estado A
voltou sem consulta, porque o Desktop reaproveitou o resultado, e ficou fora da mediana, como no
ensaio.

**Três consultas a mais na v2.** As segmentações sincronizadas do Detalhe de vendas da v2 não
geraram consulta nas execuções a quente, porque as listas já estavam em cache, e por isso a página
mede uma consulta nas duas pontas.

O detalhe de cada execução está em [`resultados.csv`](resultados.csv). Os JSON exportados pelo
analisador e as consultas extraídas da sessão ficaram fora do repositório, e saem de novo pelo
roteiro de medição do guia técnico.
