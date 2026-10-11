# Parecer de revisão do notebook

**Data:** 11-10-2026

## Escopo

Revisão do `analise.ipynb` já executado, com as saídas gravadas, contra o padrão de notebook adotado
(padrão de notebook da B&B, na parte que vale para pandas local) e contra a prática de mercado em análise
econométrica e desenho de experimento. A leitura cobriu as 33 células de código, as células de
texto, o enquadramento com o adendo, o registro de decisões, o relatório e o script de conferência.
O trabalho está na etapa 1 da régua de entrega, e a revisão cobra só o que vale para ela.

A ordem de prioridade é correção da análise, reprodutibilidade, aderência ao padrão e, por último,
desempenho. O notebook é pandas local de um milhão de linhas, então a parte de desempenho não
produziu achado.

## Veredito

**Aprovado com uma correção obrigatória antes de publicar.** O núcleo da análise está correto:
não há vazamento entre a janela de estimação e a de confirmação, a decisão sai só dos 24 meses
iniciais, a função do ganho do teto e a busca do ponto de equilíbrio estão certas, e o erro padrão
agrupado em duas dimensões está bem especificado. A decisão de recomendar o teto se sustenta.

O problema bloqueante está no dimensionamento do piloto (C32). A queda detectável é medida sobre o
volume total por cliente, e o limite que zeraria o ganho (12%) é medido só sobre o volume das linhas
afetadas pelo teto. Na mesma unidade, o limite fica perto de 5% do volume do cliente, e o piloto de
seis meses só enxerga quedas a partir de cerca de 10%. A frase do relatório de que o piloto enxerga
uma queda abaixo da que zeraria o ganho não se sustenta como está.

## Achados

| Severidade | Célula | Achado | Correção sugerida |
|---|---|---|---|
| bloqueante | C32, C28 | A queda detectável (13,5% em três meses, 9,6% em seis) é calculada sobre o volume total por cliente grande, e é comparada no relatório com `teto_perda_equilibrio` (12%), que é a perda sobre o volume das linhas afetadas, cerca de 44% das linhas do porte. Como a quantidade não depende do desconto, essas linhas carregam perto de 44% do volume, e 12% delas equivalem a algo em torno de 5% do volume do cliente. Se a perda vier espalhada pelo cliente inteiro, o limite é o próprio `teto_saida_equilibrio`, de 4,8%. Nas duas leituras o piloto de seis meses tem metade da sensibilidade necessária, e a recomendação de seis meses perde o fundamento. | Expressar o limite que zera o ganho na mesma unidade da métrica do piloto, calculado no código, e comparar os dois na própria célula. Se o piloto não alcançar o limite, registrar isso e avaliar alternativas: métrica de margem por cliente, ajuste pela quantidade do período anterior (CUPED ou ANCOVA), prazo maior, ou declarar no relatório que o piloto só detecta perdas grandes. |
| importante | C32 | A regra de decisão do relatório ("se o volume do grupo com teto não cair além do que o piloto consegue medir, o teto vale para todos") toma ausência de diferença significativa como prova de ausência de perda. O teste que responde à pergunta é de não inferioridade, com a margem igual ao limite que zera o ganho. A comparação entre a queda detectável e esse limite também não existe em código: a célula termina num comentário solto. | Desenhar o piloto como teste de não inferioridade sobre a métrica da decisão (margem ou volume por cliente), com a margem de não inferioridade declarada, e colocar a comparação em código, com o resultado registrado por `registrar()`. |
| importante | C25 | `vezes_abaixo_equilibrio` divide o equilíbrio (3,2% por ponto) pelo maior limite superior (0,007%). Com o denominador colado em zero, o número é instável: um limite de 0,0007% daria 4.500 vezes, e um limite negativo daria infinito. O "439 vezes" do relatório depende quase só do ruído em torno de zero. | Trocar por diferença em pontos percentuais entre o equilíbrio e o limite superior, ou pela distância em erros padrão. |
| importante | célula de texto da seção 1 | O resumo do enquadramento no notebook descreve o desenho anterior ao adendo: erro agrupado só por cliente, efeito em variação percentual do logaritmo e equilíbrio marginal `0,01 × receita bruta ÷ margem` como critério. O código segue o adendo (Poisson, cliente mais vendedor, equilíbrio pela função do ganho). Quem lê o notebook encontra um método e executa outro. | Reescrever o resumo pelo adendo, mantendo a menção de que o desenho original foi revisado antes da execução. |
| importante | C17, C19, C23, C32 | Parâmetros de método fora da célula C01: `Z_PODER`, os prazos do piloto (3 e 6 meses) e a divisão em metades em C32, `AGRUPAMENTO` e `COLUNAS_MODELO` em C17, o limiar de 1.000 linhas em C19 e a tolerância de 2% do diagnóstico em C23. O padrão pede parâmetros num lugar só (padrão de notebook da B&B). | Levar esses valores para C01, com o porquê de cada um em comentário. |
| menor | C32 | A população do piloto é definida pelos clientes grandes ativos no ano de confirmação, que é atividade observada depois do ponto de sorteio. O cálculo também ignora o agrupamento por vendedor, que o modelo principal trata como choque comum. | Definir a população elegível por atividade anterior ao início do piloto e incluir o efeito de desenho do vendedor, ou sortear por vendedor. |
| menor | C25, C22 | A especificação da carteira inteira, com efeito fixo de porte, vota na decisão contra o equilíbrio do cliente grande. É outra grandeza, dominada por linhas com desconto até 10%. Como ela só pode rebaixar, não muda o resultado, mas mistura estimandos. | Deixar essa especificação fora dos votos e mantê-la só como linha de base corrigida. |
| menor | C21, C22, C24, C25 | O dicionário `tabela` é criado em C21 e alterado em C22 e C24, e `maior_sup` é calculado em C21, antes dessas inclusões. O relatório fala em "maior limite superior entre todas as variações" (0,007%), e o gráfico 3 mostra a confirmação com 0,027%. Reexecutar C21 sozinha apaga as entradas de C22 e C24 e muda os votos de C25. | Montar a tabela de votos numa célula só e nomear `maior_sup` pelo que ele cobre, ajustando a frase do relatório. |
| menor | C28 | A faixa junta o percentil 2,5 do cenário pior com o 97,5 do cenário sem perda. O resultado é a envoltória de dois cenários, sem a cobertura de 95% que o leitor tende a supor. A reamostragem por cliente ignora o agrupamento por vendedor usado no erro padrão. | Nomear a faixa como envoltória no texto e considerar reamostragem em blocos de vendedor. |
| menor | C15, C19 | A leitura simples e o índice por porte usam os 36 meses, inclusive a janela de confirmação, e são citados no mesmo parágrafo de decisão que os números da estimação. Em C19, `dentro_amplitude_indice` é a amplitude entre a maior e a menor faixa, e o relatório o descreve como afastamento em relação à primeira faixa, que além disso vai de 0 a 2% e não é "sem desconto". | Declarar a janela das leituras descritivas e alinhar a frase ao que a métrica mede. |
| menor | C09, C13, C27, C28 | Colunas sem prefixo: `MES`, `FAIXA_DESCONTO`, `JANELA`. `PCT_DESCONTO_PP` vai de 0 a 18 e contraria a convenção declarada no próprio notebook de `PCT` entre 0 e 1. As tabelas agregadas (`por_porte`, `base_12m`, `recompra`, `por_cli`) usam nomes em minúsculo sem prefixo, inclusive as variáveis do modelo de recompra. O prefixo `PCT` também não consta da lista do padrão (padrão de notebook da B&B, seção 2). | `DT_MES` ou `CLAS_MES`, `CLAS_FAIXA_DESCONTO`, `CLAS_JANELA`, `QTD_PP_DESCONTO` ou equivalente fora de `PCT`, prefixo também nas agregadas, e registrar `PCT` como extensão aceita do padrão. |
| menor | C05, C13, C18, C24 | `df_cliente` e `df_produto` são dimensões e pediriam `df_dim_cliente` e `df_dim_produto`. `g_est`, `g_conf`, `recompra`, `por_cli` e `calibracao` são DataFrames sem o prefixo `df_`. Em C12, `g` de uma letra convive com `g_est` e `g_conf`. | Aplicar a nomenclatura de DataFrame do padrão (seção 2). |
| menor | C01, C09, C28 | Células que fazem mais de uma coisa: C01 junta importação, parâmetros, funções de formatação e estilo de gráfico. C09 faz a junção e deriva cinco colunas. C28 calcula o ganho, a reamostragem e a robustez. | Separar parâmetros de funções auxiliares e de estilo, e dividir C09 e C28 por etapa. |
| menor | C01, C09, C11, C06 | Comentário desatualizado ou óbvio. Em C11, "por isso o efeito é estimado em logaritmo" ficou da versão anterior, e o principal hoje é Poisson. Em C01, `Z` diz ser "para o intervalo de 95%", mas os intervalos vêm de `confint()` e `Z` só entra no poder do piloto. Em C09 e C06, os comentários repetem o que o código já diz. | Corrigir o de C11 e o de `Z`, e trocar os óbvios pelo porquê. |
| menor | C01, C17 | `np.random.seed(SEMENTE)` fixa o gerador global, que nenhuma célula usa (a reamostragem usa `default_rng`). `m._N` lê atributo privado da biblioteca, que pode mudar entre versões. | Retirar a semente global ou declarar que ela é só proteção, e usar o atributo público de número de observações. |
| menor | C05, C09 | `del df_bz` e `del df_silver` impedem reexecutar C04 e C06 a C08 depois de C09. A ordem de cima a baixo funciona, e a liberação de memória se justifica. | Comentar o porquê da liberação e avisar que essas células não são reexecutáveis isoladamente. |
| menor | C07 | A coluna `natureza` é uma lista posicional. Se a ordem das colunas mudar, a classificação sai errada sem erro. | Montar a classificação por dicionário indexado pelo nome da coluna. |
| menor | C01, textos | Caminho padrão fixo em formato Windows, com a variável de ambiente como saída. O guia pede Python 3.12 ou mais novo e as versões foram testadas em 3.14, sem confirmação de que instalam em 3.12. Os gráficos são gravados com `Agg` e não aparecem no notebook executado. Há duas seções numeradas como 7. | Caminho relativo à pasta do caso como padrão, versão de Python alinhada entre guia e dependências, `display` das figuras e numeração corrigida. |

## O que está conforme

**Correção da análise.** As janelas não se sobrepõem e são conferidas por asserção em C13. A decisão
sai só da estimação de 24 meses, o equilíbrio usado no critério também, e a confirmação é uma
reestimação independente nos 12 meses seguintes que só pode rebaixar o resultado, como o adendo
pede. O efeito pior plausível aplicado ao ano seguinte vem da janela anterior, sem informação do
futuro. A leitura de recompra usa desconto do passado para explicar pedido do futuro, com os pedidos
anteriores como controle.

**Conta do equilíbrio.** `ganho_do_teto` escala receita e custo juntos pelo fator de volume, mexe
só nas linhas acima do teto e trunca o efeito em zero. A função é decrescente no efeito, o intervalo
de busca do `brentq` tem sinais opostos nas pontas, e efeito e equilíbrio são comparados na mesma
escala de pontos de log. As fórmulas de `teto_perda_equilibrio` e `teto_saida_equilibrio` estão
algebricamente corretas para o que cada uma declara.

**Inferência.** O Poisson por pseudo-máxima verossimilhança mede o efeito na quantidade média, que é
a escala da conta de margem, e tolera a sobredispersão observada. O agrupamento `CRV1` em cliente e
vendedor está na sintaxe correta da biblioteca, e 150 vendedores bastam para a dimensão menor. O
erro padrão obtido é coerente com a variância da quantidade e do desconto no porte grande. O
diagnóstico de calibração por faixa (C23) confere que a forma linear não esconde efeito concentrado
acima de 10%.

**Reamostragem.** A reamostragem inclui os clientes sem linha afetada, com ganho zero, e usa gerador
com semente declarada.

**Reprodutibilidade.** A base é conferida pelo manifesto do gerador, com semente, data de corte,
contagens e somas de controle. Execução sequencial de 1 a 33, dependências com versão fixada, dado
fora do repositório, e todo número do relatório passa por `registrar()` e é conferido pelo script
de conferência. Nenhum segredo, nenhum dado real e nenhum identificador de pessoa no código ou nas
saídas.

**Padrão.** Tipagem declarada na leitura, junção com `validate="many_to_one"` e contagem antes e
depois, asserções de domínio e de coerência entre as colunas de valor, camadas `df_bz`, `df_silver`
e `df_fato`, prefixos aplicados na maior parte das colunas, rótulo `[Cnn]` em toda célula de código
e cabeçalho de padrões no topo.

## Correções aplicadas depois do parecer

Feitas em 11-10-2026. Os rótulos de célula citados acima são os da versão revisada. A correção
dividiu três células e o notebook passou de 33 para 36 células de código, então a tabela abaixo
traz o rótulo novo de cada ponto.

| Achado | O que mudou | Célula nova |
|---|---|---|
| piloto medido em unidade diferente do equilíbrio | o equilíbrio passou a ser expresso na unidade de cada métrica de guarda (4,8% da margem do porte, que vale tanto para saída de clientes quanto para queda uniforme de volume por cliente); a métrica principal do piloto passou a ser a parcela de clientes grandes sem compra, que em seis meses detecta 3,2 pontos, abaixo dos 4,8; a queda uniforme de volume, que nem em 12 meses fica detectável abaixo do equilíbrio, foi declarada como risco residual no relatório | C30, C35 |
| ausência de diferença tratada como prova | o piloto virou teste de não inferioridade, unilateral a 5% e com poder de 80%, com margem igual ao equilíbrio, e a célula compara em código a piora detectável com o equilíbrio | C35 |
| "439 vezes abaixo" instável | trocado pela distância em erros padrão da especificação principal (176) | C27 |
| texto da seção 1 com o desenho anterior ao adendo | reescrito com o desenho do adendo | seção 1 |
| parâmetros fora da primeira célula | agrupamento, limiar de linhas por faixa, tolerância de calibração, quantis, fração e prazos do piloto foram para a C01, que agora só tem parâmetros; bibliotecas e funções de apoio ficaram na C02 | C01, C02 |
| população do piloto e efeito do vendedor | a população passou a ser o cadastro de clientes grandes, e a ausência do efeito de desenho do vendedor está declarada no texto da seção 7 | C35 |
| carteira inteira votando contra o equilíbrio do cliente grande | a carteira saiu da votação e ficou só no gráfico, como referência | C27, C28 |
| `tabela` alterada em três células e "entre todas as variações" | as especificações que votam ficam num dicionário montado numa célula só; o maior limite superior é calculado só entre elas, e o relatório passou a dizer "entre as especificações do cliente grande, na mesma janela" | C23, C27 |
| faixa sem cobertura nominal de 95% | descrita no notebook e no relatório como envoltória de dois cenários, do percentil 2,5 do pessimista ao 97,5 do otimista, e separada numa célula própria | C31 |
| leituras descritivas nos 36 meses e "faixa sem desconto" | o texto deixa claro que o perfilamento e a leitura por porte usam os 36 meses, e a amplitude passou a ser descrita contra a primeira faixa, de 0 a 2% | C21, relatório |
| nomes de coluna | `DT_MES`, `CLAS_FAIXA_DESCONTO`, `CLAS_JANELA` e `PP_DESCONTO`, com os prefixos `PCT` e `PP` declarados no cabeçalho; tabelas de resumo impressas ficam em minúsculas por decisão declarada no cabeçalho, porque são saída de leitura | C11, C15 |
| nomes de DataFrame | `df_dim_cliente`, `df_dim_produto`, `df_grande_est`, `df_grande_conf`, `df_recompra`, `df_ganho_cliente`, `df_calibracao` e `linha_grande` | várias |
| células com mais de uma coisa | parâmetros separados das bibliotecas, integração separada das colunas derivadas, ganho do teto separado da faixa | C01, C02, C10, C11, C30, C31 |
| comentários | o de escala da quantidade em C13 fala de Poisson, os quantis ficaram nomeados pelo uso, e os comentários óbvios saíram | C01, C07, C13 |
| semente global e `m._N` | a semente global saiu, porque só a reamostragem sorteia e ela tem gerador próprio; `m._N` ficou, agora como conferência de que a regressão não descartou linha, já que a biblioteca não expõe a contagem em atributo público | C01, C19 |
| `del` sem explicação | comentado o porquê da liberação de memória e o aviso de reexecução | C06, C10 |
| classificação posicional | montada por dicionário indexado pelo nome da coluna, com asserção de que nenhuma coluna ficou de fora | C08 |
| reprodutibilidade | os gráficos passaram a aparecer no notebook executado; o guia declara Python 3.14 como a versão testada; a numeração das seções foi corrigida. O caminho padrão continua em formato Windows, porque é o caminho que o guia usa e o comando do gerador grava, e a variável de ambiente cobre os demais sistemas | C02, guia |

Depois das correções, o notebook roda do zero sem erro, e o script de conferência termina com zero
problemas.

## Segunda passada (11-10-2026)

A segunda leitura cobriu as 36 células da versão reconstruída, com as saídas da nova execução, o
relatório reescrito e a tabela de correções acima. Os rótulos citados nesta seção são os da versão
nova.

### Veredito final

**Sem bloqueante. Uma pendência importante e cinco menores.** O bloqueante da primeira passada está
resolvido na parte que ele apontava: o volume por cliente agora é comparado com o equilíbrio na
mesma unidade, e o relatório declara que a queda uniforme de volume não é detectável pelo piloto. A
álgebra de `saida_equilibrio = G/(G+M)` em C30 está correta para as duas leituras que o texto dá a
ela, a saída de clientes com margem média e a queda uniforme de volume, porque nas duas a margem do
porte vira `(M+G)(1-L)` e o ganho zera em `L = G/(G+M)`. A fórmula de não inferioridade em C35, com
`z` unilateral de 5% somado ao de 80% de poder e a variância da proporção de referência nos dois
grupos, também está correta, e a comparação com o equilíbrio agora acontece em código.

A pendência importante está na métrica de saída, que mede menos saída do que o relatório supõe.

### O que ainda pende

| Severidade | Célula | Achado | Correção sugerida |
|---|---|---|---|
| importante | C35, relatório seção 4 e resumo | A métrica de saída é a parcela de clientes **sem nenhuma compra** nos seis meses. Ela só registra a saída do cliente que para de comprar logo no início do piloto. Hoje 12% dos clientes grandes ficam seis meses sem comprar, o que corresponde a cerca de 2,1 pedidos por cliente no semestre. Mesmo com saída imediata, uma saída de 4,8% da carteira sobe a métrica em cerca de 4,2 pontos (4,8% vezes os 88% que comprariam), abaixo dos 4,8 usados como margem. Se as saídas se espalharem pelo semestre, boa parte dos clientes que saem ainda compra antes de sair, e o aumento esperado fica perto de 1,4 ponto, abaixo dos 3,2 que o piloto detecta. A frase "detecta a saída de clientes antes de ela chegar a esse ponto" vale só para a saída imediata. O registro `equilibrio_em_pontos` também apresenta uma fração da margem como pontos percentuais de clientes, o que supõe que quem sai tem margem média. | Calcular em código a margem de não inferioridade na unidade da métrica, com a hipótese sobre o momento da saída escrita. Avaliar uma métrica que pegue a saída em qualquer momento do piloto, como a parcela sem compra no último trimestre ou a taxa de pedidos por cliente, e refazer a conta de poder com ela. Se a métrica atual ficar, o relatório precisa dizer que ela detecta a saída que acontece logo depois da entrada do teto. |
| menor | relatório, resumo | "Nenhum piloto viável com esse número de clientes a enxerga" é uma afirmação mais forte do que a conta sustenta. C35 testa dois prazos sem ajuste pelo período anterior e sem a margem por cliente como métrica. | Restringir a frase ao piloto desenhado, por exemplo "o piloto de seis ou doze meses, sem ajuste pelo período anterior, não enxerga". |
| menor | relatório, seção 4 | O acompanhamento depois da adoção compara a margem do cliente grande mês a mês com a dos últimos 12 meses. É uma comparação antes e depois sem grupo de controle. A margem sobe cerca de 5% pelo próprio teto e mascara a queda de volume que se quer ver, e a sazonalidade e a tendência se confundem com o efeito. Se o piloto com controle não enxerga 4,8%, essa comparação também não enxerga. | Acompanhar o volume em vez da margem e manter uma parcela pequena de clientes na política anterior por mais tempo, como grupo de controle, ou comparar com uma projeção que tenha intervalo. |
| menor | C34, relatório seção 3 | O título do gráfico 4 diz que o ganho "resiste a uma perda grande de volume". Os 12% são perda só nas linhas afetadas e equivalem a cerca de 4,8% do volume do cliente, que o próprio relatório trata como pequena e não detectável. A coluna "Perda de volume que zera o ganho" da tabela de tetos também não diz que a perda é medida só nas linhas afetadas. | Título neutro, como "Quanto volume nas linhas afetadas zeraria o ganho", e acrescentar "nas linhas afetadas" ao cabeçalho da coluna. |
| menor | relatório, gráfico 3 | O texto alternativo do gráfico 3 fala em seis especificações, e o gráfico desenha sete: as cinco que votam, a carteira inteira e a confirmação. | Corrigir para sete, ou dizer quais entram. |
| menor | C29, C31, C25 | `df_recompra`, `df_ganho_cliente` e `df_calibracao` têm colunas em minúsculo e sem prefixo. A exceção declarada no cabeçalho cobre tabela de resumo impressa, e `df_recompra` alimenta uma regressão. | Aplicar os prefixos nesses três DataFrames, ou ampliar a exceção do cabeçalho de forma explícita. |

### Resolvidos e aceitos

Os demais achados da primeira passada estão resolvidos na versão nova: a distância em erros padrão
(176) substitui a razão instável, o texto da seção 1 segue o adendo, os parâmetros estão em C01, a
votação ficou só com as especificações do cliente grande montadas numa célula, a faixa é descrita
como envoltória, a janela das leituras descritivas está declarada, e a nomenclatura, a divisão de
células, os comentários, a classificação por dicionário e a exibição dos gráficos foram ajustados.
A população do piloto agora vem do cadastro, sem condicionar em atividade futura.

Ficam aceitos como estão, com a justificativa registrada: `m._N`, usado como conferência de que a
regressão não descartou linha, o caminho padrão em formato Windows coberto pela variável de ambiente,
e a ausência do agrupamento por vendedor no piloto, declarada no texto da seção 7. A reamostragem da
faixa continua sem blocos de vendedor, e isso não muda o resultado, porque o limite superior do
efeito é praticamente zero e a faixa depende quase só da variação entre clientes.

Nenhum problema novo de correção apareceu com a reestruturação. As janelas, o ponto de equilíbrio,
a decisão e os números do relatório continuam os mesmos da primeira execução, o que é o esperado
para uma mudança que não tocou o método.

## Correções aplicadas depois da segunda passada

| Achado | O que mudou |
|---|---|
| métrica de saída diluída | o piloto passou a durar 12 meses, e a saída é lida pela parcela de clientes grandes sem compra no segundo semestre, o que pega inteira a saída ocorrida nos primeiros seis meses; a margem de não inferioridade é calculada em código na unidade da métrica, `equilíbrio × (1 − parcela sem compra)`, e dá 4,2 pontos contra 3,2 detectáveis; a hipótese de margem média de quem sai e o limite da saída que começa no segundo semestre estão escritos no notebook e no relatório (C35, seção 7, relatório seção 4) |
| "nenhum piloto viável" | a frase do resumo ficou restrita ao piloto desenhado, que enxerga queda de volume de 6% em 12 meses |
| acompanhamento antes e depois pela margem | trocado por um grupo de controle sorteado mantido na política atual depois da adoção, com o volume por cliente como métrica |
| título do gráfico 4 e coluna da tabela de tetos | o título diz que o ganho só some com 12% de perda no volume afetado, e a coluna passou a "perda de volume nas linhas afetadas" |
| texto alternativo do gráfico 3 | corrigido para sete especificações |
| colunas sem prefixo | `df_recompra`, `df_ganho_cliente` e `df_calibracao` passaram a usar `VLR_`, `QTD_`, `PP_` e `CLAS_` |

O notebook foi reexecutado do zero depois dessas mudanças, e a conferência do relatório terminou
com zero problemas.

## Terceira passada (11-10-2026)

**Veredito: sem pendência bloqueante nem importante. Fica uma observação menor, que não impede a
publicação.**

A conta da C35 se sustenta. Com o piloto de 12 meses e a saída lida no segundo semestre, todo
cliente que deixa de comprar nos primeiros seis meses aparece com compra zero na leitura, e o
aumento esperado da parcela sem compra é a fração de saída vezes a parcela que compraria de
qualquer jeito: 4,8% vezes 88%, ou 4,2 pontos. A piora detectável, com teste unilateral a 5%, poder
de 80% e 1.284 clientes por grupo, é de 3,2 pontos, e a comparação entre as duas está em código. A
hipótese de margem média de quem sai e o limite da saída que começa só no segundo semestre estão
escritos no notebook e no relatório. O volume por cliente em 12 meses detecta 6,1%, acima dos 4,8%
do equilíbrio, e o relatório diz isso no resumo e na seção 4 sem exagerar o alcance do piloto.

As cinco menores da segunda passada estão fechadas. A frase do resumo ficou restrita ao piloto
desenhado. O acompanhamento depois da adoção passou a usar um grupo de controle e o volume por
cliente, e o texto explica por que a margem e a comparação de antes e depois não servem. O título
do gráfico 4 e a coluna da tabela de tetos dizem que a perda é nas linhas afetadas. O texto
alternativo do gráfico 3 fala em sete especificações. `df_recompra`, `df_ganho_cliente` e
`df_calibracao` usam os prefixos, e a junção da recompra continua correta com os nomes novos.

| Severidade | Onde | Observação | Sugestão |
|---|---|---|---|
| menor | relatório, seção 4 | O grupo de controle permanente aparece como o meio de cobrir a queda pequena e uniforme de volume. Como ele é uma parte menor da carteira, tem menos poder que o piloto meio a meio, que já não enxerga 4,8% em 12 meses, e só chega lá com mais tempo de comparação. O texto não diz isso. | Acrescentar que o tamanho e a duração do grupo de controle precisam de dimensionamento próprio, e que a cobertura desse risco vem com o tempo de acompanhamento. |

## Quarta passada (11-10-2026)

A quarta leitura cobriu as mudanças da rodada nova: a votação em C23 e C27, o ganho como ponto com
cenários de saída em C31, o desenho estratificado do piloto em C35, os gráficos refeitos e os
trechos reescritos do relatório. O notebook foi lido com as saídas da execução nova.

### Veredito

**Sem bloqueante. Uma pendência importante, de registro e não de conta, e quatro menores.** As
contas da C31 e da C35 estão corretas, e a decisão continua a mesma.

**C31.** O ganho líquido com saída de clientes de margem média é `G(1 − x) − xM`, que é o ganho
`G` menos a margem pós-teto `x(M + G)` de quem sai, e zera em `x = G/(G + M)`, coerente com a C30.
Com `G` de R$ 5,52 milhões e `M` de R$ 110,5 milhões, os cenários de 1%, 2% e 3% dão R$ 4,4, R$ 3,2
e R$ 2,0 milhões, que são os números impressos e citados no relatório. O ganho com o pior efeito
plausível usa o maior limite superior entre as Poisson que votam (0,008%) e fica em R$ 5,5 milhões.

**C35.** Com 12% de clientes sem compra no semestre e 1.284 por grupo, o erro padrão da diferença é
cerca de 1,28 ponto. A margem de não inferioridade é 4,8% vezes 88%, ou 4,19 pontos. O poder sem
saída real é `Φ(margem/ep − z_α)`, que dá `Φ(3,27 − 1,645)`, cerca de 95%, e a maior alta real que
ainda deixa 80% de poder é `margem − (z_α + z_β)·ep`, cerca de 1,0 ponto. As duas leituras são as
corretas para não inferioridade, e o texto da seção 4 as descreve sem exagero. O sorteio
estratificado usa semente, sai com 1.285 e 1.284 clientes, e o erro padrão sem crédito pela
estratificação deixa a conta conservadora. A métrica de volume continua declarada como fora do
alcance do piloto, com 6,1% detectáveis contra 4,8% do equilíbrio.

### O que pende

| Severidade | Onde | Achado | Correção sugerida |
|---|---|---|---|
| importante | enquadramento, C23, C27, C31, relatório seção 2 | Duas mudanças desta rodada alteram o que o adendo do enquadramento fixou antes da execução. O logaritmo por MQO, que o adendo punha entre as robustezes que podem rebaixar a decisão, saiu da votação. A faixa por reamostragem de clientes, que o adendo previa para a incerteza do ano seguinte, saiu do resultado. Também entrou uma especificação nova na votação. Os motivos são defensáveis e estão no registro de decisões, e nenhuma mudança altera a decisão, porque o logaritmo também recomenda o teto e a faixa removida ia de R$ 5,4 a R$ 5,7 milhões. Mas o próprio enquadramento diz que mudança entra no fim dele, com data e motivo, e a única emenda lá é de forma e afirma que nada no método mudou. O relatório continua dizendo que o critério foi fixado antes para não ser ajustado ao número. Sem a emenda, a prova de pré-registro que sustenta o caso fica incompleta. | Acrescentar ao enquadramento uma emenda de método, datada e marcada como posterior à execução, com as três mudanças, o motivo de cada uma e a frase de que a versão pré-registrada leva à mesma decisão. Atualizar o hash no registro de decisões. |
| menor | relatório, seção 3 e resumo; C31 | "Conta sobre todos os clientes do período, sem margem de erro a declarar" vale para o que o teto teria rendido no ano passado. A decisão olha para o ano seguinte, que varia de um ano para o outro mesmo sem saída de clientes. A variação é pequena perto dos cenários de saída, e é por isso que a mudança se sustenta, mas o texto a apresenta como inexistente. | Dizer que o número descreve o ano realizado e que a variação de um ano para o outro é pequena perto do risco de saída, citando a ordem de grandeza. |
| menor | C35, relatório seção 4 | "O vendedor principal explica 5% da variação da métrica" lê como efeito real um número que o acaso já produz. Com cerca de 17 clientes por vendedor, a variância das médias por vendedor responde por perto de 6% da variância total mesmo sem nenhum efeito de vendedor, então 5% é compatível com efeito nulo. | Usar uma medida corrigida pelo acaso, como a correlação intraclasse pela análise de variância, ou dizer que a parcela não se distingue do esperado por acaso. |
| menor | C23, C27, relatório seção 2 e anexo A | A justificativa de que o logaritmo por MQO "mede a mediana" é imprecisa. O coeficiente volta como efeito na média geométrica, que coincide com a mediana só se o erro em log for simétrico. O motivo sólido para ele ficar fora é que, com variância que muda com o nível, o MQO em log não estima o efeito sobre a média, que é a escala do equilíbrio. | Trocar a frase pela justificativa da escala da média e da heterocedasticidade. |
| menor | C35 | O grupo começa como "controle" para todos, e só cliente com vendedor principal entra no sorteio. Hoje todo cliente grande do cadastro tem compra, então ninguém fica de fora, mas nada garante isso numa base nova. | Acrescentar asserção de que todo cliente do cadastro tem vendedor principal antes do sorteio. |

Os pontos da terceira passada continuam fechados, e a observação dela sobre o grupo de controle
permanente foi atendida na seção 4. O texto alternativo do gráfico 3 fala em oito especificações,
que é o que o gráfico desenha agora.

## Correções aplicadas depois da quarta passada

| Achado | O que mudou |
|---|---|
| mudanças de método sem registro no enquadramento | emenda de método datada no fim do enquadramento, posterior à execução, com as quatro mudanças e a constatação de que a versão anterior leva à mesma decisão; o hash novo está em `decisoes.md` |
| "sem margem de erro" | o relatório diz que isso vale para o ano realizado, e que num ano seguinte o valor varia pouco perto do risco de saída |
| parcela explicada pelo vendedor | a C35 calcula também o que o acaso explicaria, (k − 1) / (n − 1), que dá 6% contra os 5% medidos; o texto diz que o sorteio por vendedor serve ao equilíbrio dos grupos e não muda o tamanho necessário |
| motivo de o logaritmo sair | trocado para a escala: com variância crescendo junto com a quantidade, o efeito no logaritmo não se traduz no efeito sobre a média |
| cliente sem vendedor principal | asserção antes do sorteio |

O notebook foi reexecutado do zero, e a conferência do relatório terminou com zero problemas.
