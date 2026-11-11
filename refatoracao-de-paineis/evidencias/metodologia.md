# Metodologia: especificação do painel de partida (v1) e do protocolo de comprovação

Escrita em 27-09-2026, antes da construção do painel de partida, e mantida como referência do serviço.
Ela orientou a ampliação do gerador, a construção da v1, a refatoração e a medição.

## 1. Objetivo

A demonstração é um entregável que roda na máquina de quem abre, com base sintética, README que sobe do
zero e custo declarado. Custo: zero, porque todas as ferramentas são gratuitas e nada fica
hospedado.

A peça mostra o serviço de refatoração e, pelo registro de mudanças, o de manutenção. A v1 é a
versão de partida do painel comercial, montada de propósito com defeitos comuns de mercado, e ela
é refatorada para esquema estrela no painel reestruturado (v2). A prova é dupla: os
números de negócio batem entre a v1 e a v2, e três medições (tamanho do modelo, tempo de
atualização e tempo de renderização da página mais pesada) melhoram medidas do mesmo jeito nas
duas pontas. O README declara que a v1 foi construída para representar esses defeitos.

## 2. A base

### O que o gerador entrega hoje

Perfil feito sobre a cópia local de `gerador-de-dados/dados/comercial/` (semente 42, janela
encerrada em 10-08-2026), com contagem, cardinalidade, nulos, faixa de data, duplicata por chave
candidata e distribuição das colunas de valor.

**Grão de `fato_vendas`:** uma linha é um item de venda, isto é, um produto vendido a um cliente
por um vendedor numa data.

| Item | Achado |
|---|---|
| volume | 48.000 linhas, 12 colunas, nenhum nulo, `venda_id` único |
| janela | 1.075 datas distintas em 36 meses; a janela termina sempre no dia da execução |
| dimensões | 24 produtos em 3 categorias, 140 clientes, 16 vendedores, 5 regiões |
| cardinalidade das colunas de valor | `receita_bruta` e `custo_total` com 943 valores distintos, `receita_liquida` com 27.151, `margem` com 25.689 |
| região | `fato_vendas.regiao` é a região do cliente em 100% das linhas |
| margem | a soma de `margem` é igual à soma de `receita_liquida` menos `custo_total`, sem resíduo de arredondamento |
| **nome de cliente** | **140 clientes e só 128 nomes distintos.** O `faker.company()` repete sobrenome, e qualquer visual agrupado por nome junta clientes diferentes |

Não há outlier plantado: quantidade vem de Poisson e desconto de uniforme limitado. Se algum
cenário passar a ter, o tratamento é declarado antes de qualquer número ser publicado.

O que o gerador não expõe hoje: número de linhas do fato (fixo em 48.000 dentro de
`_fato_vendas`), tamanho das dimensões (fixo nas assinaturas das funções) e a data de corte da
janela (o `criar_contexto` aceita `hoje`, mas a linha de comando não).

### Volume necessário

Em 48.000 linhas o modelo inteiro cabe em poucos megabytes e atualiza em segundos nas duas
pontas, então tamanho e atualização ficariam dentro do ruído e a peça provaria pouco. As
dimensões minúsculas pioram o quadro, porque 24 produtos e 140 clientes comprimem quase de graça
no VertiPaq e escondem justamente o custo da tabela plana.

O volume recomendado é o de uma distribuidora de médio porte, que é o perfil plausível de quem
contrata o serviço:

| Parâmetro | Hoje | Este caso | Leitura de negócio |
|---|---|---|---|
| linhas de venda | 48.000 | 5.000.000 | cerca de 4.560 itens por dia em 36 meses |
| clientes | 140 | 20.000 | carteira de médio porte |
| produtos | 24 | 1.500 | catálogo com SKU de verdade |
| vendedores | 16 | 150 | equipe comercial regional |
| meses | 36 | 36 | três anos fechados, suficiente para ano anterior |

Medido com o gerador já ampliado, com as versões pinadas e as colunas de origem ligadas:
5 milhões de linhas saem em cerca de 35 segundos, com o `fato_vendas.csv` em 554 MB; 1 milhão
sai em cerca de 7 segundos, com o fato em 110 MB. Esse volume é o menor em que se espera que as
três diferenças saiam do ruído com folga, e ainda cabe na máquina de medição, de 15,8 GB. A expectativa, sem promessa, é atualização da v1 na casa de minutos e renderização da
página pesada acima de alguns segundos a frio. O volume fica congelado antes da medição da
v2 e não muda depois de ver o resultado (ver seção 7).

Como passa de 100 MB, a base deste caso **não passa pelo feed** do GitHub e não entra em
repositório. Quem abre o caso roda o gerador com o comando do README e aponta o painel para a
pasta local. O feed diário continua com 48.000 linhas.

### Mudança no gerador

Tudo dentro do `gerador-de-dados`, no cenário `comercial`, sem script paralelo, para o gerador continuar sendo a fonte única do dado. Com os
valores padrão, a saída tem que continuar idêntica à de hoje.

| # | Mudança | Por quê |
|---|---|---|
| 1 | `--hoje AAAA-MM-DD` na linha de comando, repassado ao `criar_contexto` | a janela móvel muda o dado a cada execução, e o número publicado no README precisa ser reproduzível |
| 2 | `--linhas`, `--clientes`, `--produtos`, `--vendedores`, com padrão 48.000, 140, 24 e 16, levados pelo `Contexto` até o cenário | volume deste caso sem mexer no feed |
| 3 | `--colunas-origem`, desligado por padrão. Ligado, gera o fato a partir de pedidos com vários itens e acrescenta `numero_pedido` (texto no formato `PV-000000123`, numerado na ordem de emissão) e `data_hora_emissao` (data e hora com segundos, entre 07:00 e 19:59). Todas as linhas de um pedido têm a mesma data, o mesmo cliente, o mesmo vendedor e o mesmo carimbo, e nenhum produto se repete dentro do pedido | uma extração de ERP real traz pedido com vários itens, número de pedido em texto e carimbo de hora, e são essas colunas que produzem o defeito D2. Desligada, o caminho de código do fato padrão não muda. Redesenhada em 27-09-2026 (opção A), porque agrupar o fato padrão em pedidos exigia mexer nas colunas originais |
| 4 | nome de cliente e de vendedor único, com sufixo numérico determinístico nos repetidos, em toda saída | cliente aprovado na seção 9 e vendedor aprovado depois, ambos em 27-09-2026. No padrão, 12 dos 140 nomes de cliente ganham sufixo, nenhum dos 16 de vendedor muda, e nenhum número muda |
| 5 | `_manifesto.json` na pasta de saída com parâmetros, contagem de linhas por tabela e soma das colunas de valor do fato | registro de quantas linhas saíram, e terceira perna da paridade (a fonte) |

Comando deste caso, com a data de corte no último mês fechado:

```
python gerar.py comercial --hoje 2026-08-31 --meses 36 --linhas 5000000 --clientes 20000 --produtos 1500 --vendedores 150 --colunas-origem --saida <pasta-local-da-base>
```

**Itens por pedido.** Com `--colunas-origem`, o número de itens de cada pedido é 1 mais uma
binomial negativa com dispersão 1,5 e probabilidade 1/3, o que dá média de 4 itens e desvio de 3,
com teto de 40 (ou o número de produtos, se for menor). A escolha imita a carteira de uma
distribuidora: muita reposição pequena, com um a três itens, e uma cauda de pedido grande de
cliente de porte, que a Poisson não produziria porque concentra tudo perto da média. O total de
linhas fecha exatamente em `--linhas`, cortando o último pedido.

Teste de aceite da ampliação, reescrito em 27-09-2026 quando a mudança 3 passou a gerar o fato por
pedido: (a) com `--hoje` fixo, a saída padrão tem o mesmo hash de uma geração feita antes da ampliação,
com exceção declarada dos nomes de cliente corrigidos; (b) a saída sem `--colunas-origem` é
idêntica byte a byte à da rodada anterior da ampliação; (c) duas execuções do comando deste caso geram
arquivos com o mesmo hash; (d) o feed diário segue verde; (e) com a opção ligada, em 1 e em 5
milhões: distribuição de itens por pedido, coerência dentro do pedido, produto sem repetição no
pedido, sazonalidade mensal preservada e manifesto batendo com o CSV. A tolerância da
sazonalidade foi fixada antes de medir: correlação de Pearson de pelo menos 0,95 entre as séries
mensais de receita líquida com e sem a opção, e nenhum mês com diferença relativa acima de 10%.

**Resultado da ampliação, em 27-09-2026.**

| Teste | Resultado |
|---|---|
| (a) | passou. Cinco dos seis CSV idênticos byte a byte à geração de antes da ampliação; em `dim_cliente`, só a coluna `cliente` mudou, em 12 linhas, todas com o nome original mais sufixo |
| (b) | passou. Os oito arquivos da saída padrão, manifesto incluído, idênticos byte a byte à rodada anterior |
| (c) | passou. Duas execuções em 5 milhões com o mesmo hash em todos os arquivos |
| (d) | verificado localmente, sem execução remota. O comando do workflow roda sem alteração; o efeito no feed é o `_manifesto.json` a mais e os 12 nomes de cliente com sufixo |
| (e) | passou nas duas escalas, detalhe abaixo |

| Com `--colunas-origem` | 1 milhão | 5 milhões |
|---|---|---|
| pedidos | 249.858 | 1.249.812 |
| itens por pedido: média, mediana, p90, p99, máximo | 4,00; 3; 8; 14; 32 | 4,00; 3; 8; 14; 39 |
| pedidos com 1, 2, 3, 4 e 5 itens | 19,2%, 19,2%, 16,1%, 12,5%, 9,4% | iguais |
| pedidos com 6 a 10, 11 a 20 e 21 a 40 itens | 19,7%, 3,9%, 0,1% | 19,6%, 3,9%, 0,1% |
| uma data, um cliente, um vendedor e um carimbo por pedido | sim | sim |
| produto repetido dentro do pedido | nenhum | nenhum |
| vendedor da região do cliente | 100% | 100% |
| correlação mensal da receita com e sem a opção | 0,9886 | 0,9981 |
| maior diferença mensal de receita | 4,47% | 2,41% |
| receita total com a opção sobre sem a opção | 0,9995 | 1,0008 |
| manifesto contra o CSV (linhas e cinco somas) | bate | bate |
| tempo de geração e tamanho do fato | 6,8 s; 110 MB | cerca de 35 s; 554 MB |

A base de construção, de 1 milhão, com a opção ligada, fica numa pasta local, fora do git, e sai
igual pelo comando do guia técnico.

Com 20 mil clientes, 14.479 nomes recebem sufixo, porque o sorteio de nome de empresa tem poucas
combinações; os nomes ficam únicos, mas com cara de lista numerada. A dimensão de vendedores
repetia nome em escala (148 nomes para 150) e recebeu a mesma correção; no padrão de 16
vendedores nenhum nome muda.

Na rodada anterior, o pedido era a combinação de data, cliente e vendedor sobre o fato padrão, e
isso dava quase um item por pedido (média de 1,004 em 5 milhões), porque o fato sorteia cliente e
vendedor linha a linha. Agrupar exigia mexer nas colunas originais, e por isso a opção A
trocou o caminho: com a opção ligada, o fato nasce do pedido. A consequência para o
caso é que `numero_pedido` passa a ter cerca de 1,25 milhão de valores distintos em 5 milhões de
linhas, e não quase 5 milhões. O D2 continua sendo coluna de texto de alta cardinalidade, mas o
peso dela no tamanho da v1 fica menor do que o previsto.

### Como a v1 recebe o dado

A v1 lê os seis CSV do gerador numa pasta local e, no Power Query, mescla fato com produto,
cliente, vendedor e calendário até virar uma tabela única. É o caminho mais comum que se encontra:
o time exporta um arquivo por cadastro e um de vendas, e o analista junta tudo numa tabela só
porque não conhece relacionamento. A vantagem para a prova é que a v1 e a v2 leem
**exatamente os mesmos arquivos**, então a diferença de atualização vem só do que cada modelo faz
com eles. Um CSV já achatado pelo gerador foi descartado, porque obrigaria a v2 a reconstruir
dimensão a partir da tabela plana e a comparação mediria outra coisa.

As duas pontas leem a pasta por um parâmetro do Power Query, `PastaDados` na v1 e `pPastaDados` na
v2, que ganhou o prefixo de parâmetro na padronização de 10-10-2026, e declaram a cultura `en-US` na
mudança de tipo, porque o CSV usa ponto como separador decimal (seção 7). Desde a padronização, a v2
também lê o `_manifesto.json` da mesma pasta, de onde o calendário tira a primeira e a última data da
base; os nomes de tabela e de medida da v2 estão no [README da v2](../painel-depois/README.md).

## 3. Defeitos da v1

Nove defeitos. Cada um existe porque aparece em painel de empresa de verdade e porque produz
diferença mensurável ou um efeito fácil de explicar para quem usa o painel.

| # | Defeito | Tamanho | Atualização | Renderização | Manutenibilidade |
|---|---|---|---|---|---|
| D1 | tabela plana montada por mesclagem no Power Query | piora | piora | neutro ou até favorável à v1 | piora |
| D2 | colunas de alta cardinalidade sem uso ou com tipo errado | **maior efeito** | piora | | |
| D3 | colunas calculadas no papel de medida | piora | piora | | piora |
| D4 | medidas implícitas | | | | piora |
| D5 | DAX com iteração cara | | | piora | piora |
| D6 | página sobrecarregada de visuais e segmentações | | | **maior efeito** | piora |
| D7 | inteligência de tempo sobre a data do fato, sem tabela de calendário | | | | piora |
| D8 | relação bidirecional sem necessidade, com relação inativa por ambiguidade | | | possível, sem promessa | piora |
| D9 | consulta por referência que relê a fonte e refaz as mesclagens | | **maior efeito** | | piora |

**D1, tabela plana por mesclagem.** É o primeiro modelo de quase todo mundo que aprendeu Power BI
vindo do Excel: se a planilha era uma só, o modelo também é. Quem usa o painel vê um arquivo grande, uma
atualização lenta e um modelo em que qualquer atributo novo exige remexer na consulta gigante. As
mesclagens rodam sobre 5 milhões de linhas a cada atualização e cada atributo de dimensão vira
coluna repetida no grão do fato. A refatoração separa fato e dimensões lidas direto de seus CSV,
com chave inteira no fato. Vale registrar com honestidade que tabela plana nem sempre renderiza
mais devagar, e o ganho de renderização da peça vem de D5 e D6.

**D2, alta cardinalidade.** A v1 carrega `venda_id` (único por linha, sem uso),
`data_hora_emissao` (quase única, sem uso em visual) e `numero_pedido` em texto. Acontece porque
a extração traz tudo e ninguém remove coluna "para o caso de precisar". O sintoma é o arquivo
pesado sem motivo aparente, e o VertiPaq Analyzer aponta essas três como as maiores do modelo. A
refatoração remove `venda_id` e `data_hora_emissao` e converte o pedido para inteiro, com a
string de formato recompondo o `PV-` na exibição.

**D3, coluna calculada no papel de medida.** `Lucro` (receita líquida menos custo, duplicando a
`margem` que já vem da fonte), `Margem % Linha` (razão linha a linha, decimal de alta
cardinalidade, sem uso em visual) e `Mês Ano` via `FORMAT`, com `Ordem Mês` para classificar. Quem
vem do Excel pensa em coluna, e a coluna "funciona". Quem usa o painel vê atualização mais longa e número
que ninguém sabe se vem da fonte ou de conta própria. A refatoração troca por medidas e usa os
atributos de mês da `dim_calendario`.

**D4, medidas implícitas.** Os visuais usam "Soma de receita_liquida" e "Contagem distinta de
numero_pedido" arrastadas direto da coluna. É o padrão de quem arrasta campo e o Power BI soma
sozinho. O sintoma é o mesmo indicador com formato e agregação diferentes em cada visual, e a
impossibilidade de reaproveitar. Não muda medição; aparece na contagem de violações do Best
Practice Analyzer. A refatoração cria medida explícita com nome de negócio e desliga a
sumarização das colunas numéricas.

**D5, DAX com iteração cara.** Três medidas corretas e caras: `Receita Linha Premium` com
`FILTER(Vendas, ...)` sobre a tabela inteira, `Clientes com compra` com
`COUNTROWS(FILTER(VALUES(...), CALCULATE(...) > 0))` e `Ticket médio` com `AVERAGEX` sobre cada
pedido com transição de contexto. São fórmulas copiadas de fórum que dão o número certo. Quem usa o painel
vê o cartão girando ao filtrar. A refatoração usa predicado de coluna com `KEEPFILTERS`,
`DISTINCTCOUNT` e `DIVIDE([Receita líquida], [Pedidos])`, que dão o mesmo número.

**D6, página sobrecarregada.** A página Visão geral tem por volta de 22 visuais, entre eles oito
cartões, seis segmentações e uma matriz de cliente por trimestre. Painel cresce por pedido
("põe mais um cartão aqui") e ninguém tira nada. O sintoma é a página que demora a abrir e trava
ao filtrar, porque cada visual dispara a sua consulta. A refatoração consolida os cartões num
cartão de várias linhas, leva parte das segmentações para o painel de filtros e move a matriz
para uma página de detalhamento, **sem tirar nenhum número do alcance do usuário** (seção 5,
paridade de conteúdo).

**D7, inteligência de tempo sobre a data do fato.** Revisto em 27-09-2026: a data e hora
automáticas ficaram desligadas, e o defeito passou a ser a ausência de tabela de calendário.
As três medidas de tempo usam `SAMEPERIODLASTYEAR` e `DATESYTD` direto sobre `Vendas[data]`, e
como a tabela não é marcada como de data, cada uma carrega um remendo com `ALL` em nove colunas de
calendário (`ano`, `mes`, `nome_mes`, `ano_mes`, `trimestre`, `dia_semana`, `fim_de_semana`,
`Mês Ano`, `Ordem Mês`). Sem o remendo, qualquer segmentação por ano ou mês zera o ano anterior.
O número sai certo, mas qualquer coluna de data nova que entrar sem ir para a lista quebra as três
medidas em silêncio. A refatoração marca a `dim_calendario` como tabela de data e as medidas
perdem o remendo. Não há efeito em medição: o defeito entra pela manutenção e pela história. A
conferência de 27-09-2026 contra somas diretas bateu em quatro cortes (ano cheio, mês, mês com
região e categoria, e 2023 sem ano anterior). A paridade feita depois mostrou que, em corte fino,
como um vendedor num mês, o cálculo da v1 quebra; ver a exceção 1 do [registro de mudanças](../registro-de-mudancas.md).

**D8, relação bidirecional sem necessidade.** Tabelas `Regioes` (para o peso de mercado) e
`Clientes` ligadas à `Vendas` com filtro nos dois sentidos, "para a segmentação funcionar". A
relação entre `Regioes` e `Clientes` fica inativa porque o Desktop recusa o caminho ambíguo, e
ninguém sabe dizer por quê. Quem usa o painel vê lista de segmentação encolhendo sem motivo e medida que
muda conforme a página. A refatoração deixa todas as relações de um para muitos em direção única.
O efeito em renderização é possível pelas segmentações, mas não é prometido.

**D9, consulta por referência que relê a fonte.** A tabela `Clientes` da v1 é criada por
referência à consulta `Vendas`, com remoção de duplicadas. Quase todo mundo acredita que
referência reaproveita o resultado; na prática o Power Query avalia a cadeia de novo, relendo os
5 milhões de linhas e refazendo as mesclagens. Quem usa o painel vê a atualização dobrar de tempo sem
nenhuma tabela nova grande. A refatoração lê `dim_cliente.csv` direto.

**Cortados e por quê.** Consulta sem dobra de consulta saiu, porque fonte CSV não dobra em
nenhuma das pontas e o defeito não teria como aparecer; o D9 ocupa o lugar dele no tempo de
atualização (decidido em 27-09-2026, seção 9). Filtros de página e segmentações em excesso entraram
dentro do D6, porque o mecanismo é o mesmo. Ordenação no Power Query antes de carregar saiu
porque altera a compressão e confundiria a medição de tamanho. Coluna calculada com transição de
contexto sobre 5 milhões de linhas saiu por ser caricata e poder levar horas. Mapa saiu de todas as
páginas, porque depende de serviço de rede e contamina o tempo de renderização.

## 4. Páginas da v1 e medidas de paridade

| Página | O que mostra |
|---|---|
| Visão geral | oito cartões (receita líquida, margem, margem %, quantidade, pedidos, ticket médio, clientes com compra, crescimento sobre ano anterior %), cartão de receita da Linha Premium, seis segmentações (ano, mês, região, categoria, porte, vendedor), linha de receita e receita do ano anterior por mês, colunas de receita acumulada no ano, barras por região e por categoria, rosca por porte, matriz de cliente por trimestre com receita e margem %, tabela dos 20 produtos de maior receita. É a candidata a página mais pesada |
| Clientes e vendedores | matriz de vendedor por mês, ranking de clientes, receita e participação por região ao lado do peso de mercado, segmentação de região vinda da tabela `Regioes` |
| Detalhe de vendas | tabela no grão de linha com pedido, data, cliente, produto, quantidade e valores, a página de exportação que todo painel acaba tendo |

As medidas de paridade, com a regra escrita sobre as colunas da fonte. Na v1, algumas existem
só como agregação implícita no visual, e é esse valor que entra na comparação.

| Medida | Regra |
|---|---|
| Receita bruta | soma de `receita_bruta` |
| Receita líquida | soma de `receita_liquida` |
| Custo | soma de `custo_total` |
| Margem | soma de `margem` (na v1, soma da coluna calculada `Lucro`, que precisa dar o mesmo valor) |
| Margem % | margem dividida por receita líquida, razão das somas e nunca média das razões, porque a média das razões distorce o resultado quando o peso das linhas varia |
| Quantidade | soma de `quantidade` |
| Linhas de venda | contagem de linhas do fato; controle técnico, fora das páginas |
| Pedidos | contagem distinta de `numero_pedido` |
| Ticket médio | receita líquida dividida por pedidos |
| Clientes com compra | contagem distinta de cliente com receita líquida no contexto |
| Receita Linha Premium | receita líquida com categoria igual a Linha Premium |
| Receita ano anterior | receita líquida no mesmo período do ano anterior |
| Receita acumulada no ano | receita líquida de 1º de janeiro até a última data do contexto, no mesmo ano |
| Crescimento sobre ano anterior % | receita líquida menos receita ano anterior, dividido pela receita ano anterior, vazio quando não houver ano anterior |
| Participação na receita | receita líquida dividida pela receita líquida de todas as regiões |
| Peso de mercado | soma de `peso_mercado` da região |

Região, em toda a peça, é a região do cliente (`fato_vendas.regiao`). A `dim_vendedor` também tem
coluna `regiao`, e ela não é usada em nenhum corte.

## 5. Protocolo de medição

**Máquina declarada.** A máquina de medição é um Intel Core i5-14400F com 10 núcleos, 15,8 GB de
memória e dois SSD SATA de 480 GB (WD Green e Kingston A400). Um arquivo `desempenho/maquina.md`
registra isso junto com a letra do disco onde ficam a base e o arquivo, processador, núcleos, memória,
tipo de disco, versão do Windows, plano de energia (alto desempenho, na tomada), versão do Power
BI Desktop, do DAX Studio e do Tabular Editor 2, resolução de tela e data da sessão. Durante a
medição, só o Desktop e o DAX Studio abertos.

**Mesma sessão para as duas pontas.** O Desktop muda todo mês, e medir a v1 em outubro e a
v2 em novembro mistura versão com refatoração. A medição feita na construção vale como
diagnóstico, e a tabela final do caso sai de uma sessão única de medição final em que a v1 e a v2 são
medidas na mesma máquina, na mesma versão, no mesmo dia, em ordem alternada.

| Grandeza | Como medir | Repetições | Cache |
|---|---|---|---|
| tamanho do modelo | DAX Studio, View Metrics (VertiPaq Analyzer), tamanho total do modelo; salvar o `.vpax` como evidência. Tamanho do arquivo `.pbix` salvo fica como número secundário, porque é o que quem usa o painel enxerga | uma medição após atualização completa, conferida depois de uma segunda atualização | não se aplica |
| tempo de atualização | atualização completa disparada pelo botão Atualizar do Desktop, com a duração lida do rastreamento de atualização do DAX Studio (Refresh Profile) ou, se a versão instalada não tiver, do SQL Server Profiler conectado à porta local do Desktop, pelo evento de fim do comando. Conta do início do comando ao fim, incluindo Power Query, compressão, colunas calculadas e relações | uma atualização de aquecimento descartada e cinco medidas | quente: o arquivo CSV já no cache do sistema operacional, que é o mais estável |
| renderização da página mais pesada | Analisador de desempenho do Desktop, botão Atualizar visuais, com exportação do resultado em JSON. O tempo da página é o fim do último evento menos o início do primeiro, calculado por `desempenho/tempo_pagina.py` a partir do JSON exportado, que também soma o tempo de consulta DAX e conta as consultas | cinco a frio e cinco a quente, em dois estados de filtro | frio: limpar o cache pelo DAX Studio (Clear Cache) antes de cada execução; quente: repetir sem limpar |

**Página mais pesada.** Na construção, todas as páginas da v1 são medidas uma vez e a mais lenta é
escolhida. A mesma página é medida na v2, mesmo que outra passe a ser a mais lenta.

**Estados de filtro.** Estado A, nenhuma seleção. Estado B, região Sudeste e o último ano da
janela. O relatório é salvo no estado A, e o B é aplicado à mão antes das execuções dele.

**Filtro de detalhamento.** Desde o redesenho visual, o Detalhe de vendas da v2 recebe detalhamento por
cliente, produto e vendedor. Antes de cada sessão de medição, o painel de filtros da página é aberto
e a seção de detalhamento precisa estar vazia, porque um filtro de detalhamento esquecido reduz a
tabela e falsifica o tempo. A página da v2 também leva as três segmentações sincronizadas da
moldura, que são três consultas pequenas a mais do que a v1 nessa página, e isso vai declarado no
guia técnico junto do resultado (decisão de 27-09-2026).

**Janela.** Desktop maximizado, na resolução declarada, zoom em ajustar à página, painel de
filtros recolhido.

**Conferência do cache.** Na construção, a primeira execução depois de limpar o cache precisa ser mais
lenta que as seguintes. Se não for, a limpeza não pegou e o protocolo a frio precisa ser revisto
antes de seguir. O formato exato do JSON do analisador e a presença do Refresh Profile no DAX
Studio precisam ser conferidos na versão instalada.

**Diagnóstico de apoio, fora da tabela principal.** Server Timings do DAX Studio na consulta do
visual mais lento (motor de fórmulas contra motor de armazenamento), contagem de violações do Best
Practice Analyzer do Tabular Editor 2 com o conjunto de regras publicado pela Microsoft, versão
fixada, e contagem de tabelas, colunas e visuais. É aqui que D4, D7 e D8 aparecem com número.

**Registro.** Cada execução vira uma linha em `desempenho/resultados.csv` com as colunas `sessao`,
`ponta`, `grandeza`, `estado`, `cache`, `repeticao`, `valor`, `unidade`. O resumo preenchido está
no [guia técnico](README.md#o-resultado).

**Critério de diferença.** Uma diferença só é afirmada quando as faixas da v1 e da v2 não se
sobrepõem. Se sobrepuserem, o README diz que não houve diferença mensurável naquela grandeza.

## 6. Protocolo de paridade

A paridade tem três pernas. A fonte é o `_manifesto.json` do gerador, com o total de linhas e as
somas das colunas de valor. As outras duas são a v1 e a v2, consultadas pelo DAX Studio
com consultas `SUMMARIZECOLUMNS` versionadas em `paridade/consultas_v1.dax` e
`paridade/consultas_v2.dax`, exportadas em CSV e comparadas por `paridade/comparar.py`.

| Corte | Medidas |
|---|---|
| total | todas, e as aditivas também contra o manifesto |
| ano-mês (36) | todas |
| região (5) | todas, menos as de inteligência de tempo |
| categoria (3) | todas, menos as de inteligência de tempo |
| porte (3) | todas, menos as de inteligência de tempo |
| vendedor, pela chave (150) | as aditivas e as contagens |
| cliente, pela chave (20.000) | as aditivas e as contagens |
| ano-mês por região (180) | todas |
| estado B, total | todas |

O corte por cliente usa `cliente_id` e nunca o nome, porque o nome se repete na base atual. Na
v1, as medidas de inteligência de tempo dependem do remendo com `ALL` nas nove colunas de
calendário (D7); cortar por uma coluna de data que não esteja na lista devolveria ano anterior
vazio, e essa armadilha é parte da história do D7.

| Tipo de medida | Tolerância |
|---|---|
| contagem | igualdade exata |
| valor monetário | diferença absoluta de até R$ 0,01 por célula |
| razão e percentual | diferença absoluta de até 0,000001 |

A tolerância existe só para absorver ordem de soma em ponto flutuante. Divergência acima dela é
investigada e explicada, e nunca resolvida alargando a tolerância. O resultado vai para
`paridade/resultado.csv` com `medida`, `corte`, `chave`, `valor_fonte`, `valor_v1`,
`valor_v2`, `diferenca` e `dentro_tolerancia`, e o README mostra o número de comparações e o
número de divergências, que na medição final precisa ser zero.

**Paridade de conteúdo da página.** Todo número visível na página medida da v1 precisa estar ao
alcance na v2, na página, em dica de ferramenta ou em detalhamento. Sem isso a comparação de
renderização deixa de ser justa, porque uma página com menos informação é mais rápida por
definição.

## 7. Riscos e armadilhas

| Risco | O que fazer |
|---|---|
| a diferença de tempo fica dentro do ruído | a regra de faixas sem sobreposição decide. Se a atualização ficar no ruído, subir uma vez para 10 milhões de linhas **antes** de medir a v2; depois de ver a v2, o volume não muda, e grandeza sem diferença é declarada como tal |
| a v1 parece caricata | cada defeito precisa passar no teste "já vi isso em empresa", a v1 dá número certo e só é lento e difícil, a página pesada fica em torno de 22 visuais e não 50, e o README apresenta a v1 com o mesmo respeito com que se apresentaria o painel de um cliente |
| o Desktop não aguenta a v1 na máquina | a máquina tem 15,8 GB. Se a atualização da v1 estourar a memória ou passar de 15 minutos, descer para 3 milhões de linhas e registrar o motivo |
| separador decimal | o CSV usa ponto. Com cultura pt-BR na mudança de tipo, `0.125` vira 125 e o painel mostra número errado com cara de certo. As duas pontas declaram `en-US` na mudança de tipo, e a paridade contra o manifesto pega qualquer deslize |
| nome repetido | resolvido para cliente e vendedor na ampliação do gerador. Corte de paridade continua sempre pela chave |
| base com e sem `--colunas-origem` têm números diferentes | com a opção, o fato nasce do pedido e muda linha a linha. A v1 e a v2 do caso usam sempre a base gerada com a opção, e nenhum número do caso é comparado com o feed padrão |
| `numero_pedido` com menos cardinalidade que o previsto | cerca de 1,25 milhão de distintos em 5 milhões de linhas. Se o D2 pesar pouco no tamanho, o README atribui a diferença de tamanho a cada coluna pelo VertiPaq Analyzer, sem inflar o defeito |
| regra de valor duplicada no gerador | o fato por pedido repete as regras de quantidade, desconto e valores de `_fato_vendas`, para o caminho padrão não mudar. Quem mudar uma regra precisa mudar as duas; o comentário no código avisa |
| a janela do gerador anda sozinha | `--hoje 2026-08-31` fixo em todo comando do caso |
| versão do Desktop muda entre a v1 e a v2 | sessão única de medição final, seção 5 |
| a tabela plana renderiza mais rápido que a estrela em algum visual | publicar por visual quando acontecer; o ganho de renderização se apoia em D5 e D6, e o texto não atribui ao esquema estrela o que ele não entregou |
| data e hora automáticas é opção por arquivo | conferir em Opções, Arquivo atual, que fica desligada nas duas pontas (decisão de 27-09-2026) |
| arquivo grande no repositório | o `.pbip` não leva dado, o `cache.abf` fica no `.gitignore` e a base é gerada localmente; só os scripts, as consultas, os resultados em texto e o registro das execuções de medição são versionados |

## 8. Estrutura de pastas

Cada defeito da seção 3 vira um passo da refatoração, um por vez sempre que der, e o registro de
mudanças conta esses passos em linguagem de negócio.

```
refatoracao-de-paineis/
  README.md                       a página do serviço: resultado, o que se recebe e como funciona
  registro-de-mudancas.md         registro de mudanças, a prova da manutenção
  catalogo-de-tecnicas.md         o repertório de técnicas do serviço
  painel-antes/                   PBIP do painel de partida (v1)
  painel-depois/                  PBIP do painel reestruturado (v2), com o sistema visual em design/
  evidencias/
    README.md                     guia técnico: medição completa, paridade e como refazer
    metodologia.md                esta especificação
    desempenho/                   máquina, scripts, resultados e registro das execuções
    paridade/                     consultas, comparador e resultados
  imagens/                        prints do README
```

A base do gerador fica fora do repositório, numa pasta local apontada pelo parâmetro `PastaDados`.

## 9. Decisões de escopo

As quatro decisões foram tomadas em 27-09-2026.

| Decisão | Opções | Recomendação | Decidido em 27-09-2026 |
|---|---|---|---|
| volume da demonstração | 1 milhão, mais leve e rápido de iterar; 5 milhões; duas medições (1 e 5 milhões) mostrando como a diferença cresce | 5 milhões, com 1 milhão usado só durante a construção | 5 milhões na medição e 1 milhão na construção. Plano B de 3 milhões se a atualização da v1 estourar a memória da máquina de 15,8 GB |
| defeito de dobra de consulta | trocar pelo D9, mantendo tudo em CSV; acrescentar um banco local (SQL Server Express ou Postgres) para mostrar dobra de verdade | trocar pelo D9. O banco local quebra o "sobe do zero lendo o README", e a dobra de consulta só aparece com fonte relacional | a dobra sai e entra o D9. |
| nome de cliente repetido | corrigir no gerador para toda saída, mudando uma vez 12 nomes no feed público; corrigir só com a opção desta demonstração; manter e usar como defeito plantado | corrigir para toda saída. Nenhum número muda, qualquer painel sobre a mesma base tropeçaria no mesmo problema, e defeito plantado em nome confundiria a paridade | corrigir para toda saída, implementado na ampliação do gerador |
| defeito de regra de negócio (média de percentuais no lugar de razão das somas), que faria um número mudar com aviso | incluir nesta demonstração; deixar de fora | deixar de fora. A definição de pronto da medição final pede paridade sem divergência, e a demonstração fica mais forte com os números batendo | fica de fora |
