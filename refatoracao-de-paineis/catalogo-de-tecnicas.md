# Técnicas de refatoração e manutenção de painel Power BI

Este catálogo reúne o que dá para fazer num painel Power BI herdado, aquele que funciona e dá o
número certo, mas ficou pesado, lento para atualizar e difícil de mexer. Cada técnica vem com o
problema que ela resolve, como ela é aplicada, o que melhora e como o ganho é provado, porque
refatoração sem prova vira opinião. Algumas aparecem aplicadas na demonstração, sobre base
sintética, e estão marcadas com o defeito correspondente da
[metodologia](evidencias/metodologia.md#3-defeitos-da-v1) ou com a etapa do registro de mudanças em que
entram. As demais fazem parte do repertório do serviço e entram quando o painel pede.

O catálogo cobre painel que roda no ambiente de quem contrata, sem hospedagem e sem dado sob guarda
de terceiro.

O princípio que vale para todas é o mesmo do [registro de mudanças](registro-de-mudancas.md): nenhuma regra de
negócio muda, e o que muda de comportamento aparece escrito como exceção antes da entrega.

## Como o ganho é provado

São três formas de prova, e cada técnica usa uma ou mais delas.

A **contagem estrutural** sai do próprio projeto. Com o painel salvo em PBIP, modelo em TMDL e
relatório em PBIR, um script conta tabelas, colunas calculadas, relações por tipo e direção, medidas,
páginas, visuais por página e o que não é usado por nenhum visual, relação, ordenação ou fórmula. A
mesma contagem rodada antes e depois mostra o que saiu, sem depender de abrir o Power BI Desktop.

A **medição** cobre três grandezas: tamanho do modelo, lido pelas visões de armazenamento do motor
depois de uma atualização completa; tempo de atualização, com uma rodada de aquecimento descartada e
cinco medidas; e tempo da página mais usada, a frio e a quente. Antes e depois rodam na mesma máquina,
na mesma versão do Desktop e na mesma sessão, e uma melhora só é afirmada quando as faixas de antes e
de depois não se sobrepõem. O [protocolo da demonstração](evidencias/metodologia.md#5-protocolo-de-medição) é
esse mesmo.

A **paridade** garante que a refatoração não mudou número. As medidas acordadas com quem usa o painel
são consultadas nos mesmos cortes nas duas versões, com tolerância só para a ordem de soma em ponto
flutuante, e divergência é investigada até ter explicação. O
[protocolo de paridade](evidencias/metodologia.md#6-protocolo-de-paridade) da demonstração mostra o formato.

## Visão de conjunto

| # | Técnica | Frente | O que melhora | Como se prova | Na demonstração |
|---|---|---|---|---|---|
| 1 | inventário do painel como código | diagnóstico | foco: mexe-se no que pesa | contagem estrutural | diagnóstico de apoio |
| 2 | linha de base e paridade antes da primeira mudança | diagnóstico | comparação justa | medição e paridade | protocolo inteiro |
| 3 | data e hora automáticas desligadas | modelo | tamanho, clareza | contagem e tamanho | |
| 4 | calendário único gerado por parâmetro | modelo | manutenção, tempo correto | paridade nas medidas de tempo | D7 e padronização |
| 5 | relação pela chave, em direção única | modelo | filtro previsível | contagem e paridade | D8 |
| 6 | relação virtual quando o grão não fecha | modelo | sem muitos para muitos por rótulo | paridade | |
| 7 | dimensão de papel duplo sem leitura duplicada | modelo e carga | atualização | contagem de leituras e tempo | |
| 8 | atributo de cadastro fora do fato | modelo | tamanho, manutenção | tamanho e paridade | D1 |
| 9 | coluna calculada que vira medida | modelo | tamanho, atualização | tamanho por coluna e paridade | D3 |
| 10 | corte do que não é usado e tipo certo | modelo | tamanho, atualização | contagem e tamanho | D2 |
| 11 | regra de conjunto empurrada para a origem | carga | atualização | tempo de atualização | |
| 12 | uma leitura por fonte | carga | atualização | tempo de atualização | D9 |
| 13 | consulta com parâmetro, grupo e passo com nome | carga | manutenção, troca de ambiente | contagem estrutural | padronização |
| 14 | tabela de medidas, nome de negócio e internas ocultas | medidas | consistência, manutenção | contagem estrutural | D4 |
| 15 | família de medidas copiadas virando uma só | medidas | manutenção, consulta | contagem e paridade | |
| 16 | DAX caro reescrito com o mesmo resultado | medidas | tempo de página | medição e paridade | D5 |
| 17 | âncora temporal no dado, e não no relógio | medidas | número reproduzível | paridade em datas diferentes | |
| 18 | BLANK e zero resolvidos sem medida duplicada | medidas | manutenção | contagem e paridade | |
| 19 | parâmetro de campo no lugar de bookmark e página-cópia | relatório | manutenção, objetos por página | contagem estrutural | |
| 20 | faixa de KPI num visual só, e dica única | relatório | consultas por página | medição da página | D6 |
| 21 | eixo desconectado de propósito | relatório | comportamento correto | teste de filtro | |
| 22 | cor por faixa em gráfico de várias séries | relatório | leitura imediata | revisão da tela | |
| 23 | HTML só onde o nativo não alcança | relatório | leitura, legenda honesta | revisão da tela | |
| 24 | chassi, tema e segmentação sincronizada | relatório | consistência entre páginas | revisão da tela | redesenho visual |
| 25 | descrição para pessoa e para assistente de IA | governança | uso correto do indicador | contagem de cobertura | padronização |
| 26 | pastas, prefixos e nomes no padrão | governança | navegação no modelo | contagem estrutural | padronização |
| 27 | registro de mudança e exceção declarada | entrega | confiança de quem aceita | histórico do projeto | registro de mudanças |

## Diagnóstico

### 1. Inventário do painel como código

Painel herdado costuma chegar sem documentação, e a primeira tentação é sair corrigindo o que salta
aos olhos. O inventário vem antes: o projeto é salvo em PBIP, e um script lê o modelo e o relatório
como texto para contar o que existe e cruzar uso. Daí saem a lista de colunas que nenhum visual,
relação, ordenação ou fórmula toca, as medidas órfãs, as tabelas carregadas sem nenhuma referência, as
relações bidirecionais e de muitos para muitos, as colunas calculadas que dependem da data do dia e o
número de visuais com consulta em cada página. O resultado ordena o trabalho por impacto sobre esforço
e vira a primeira coluna da tabela de antes e depois.

### 2. Linha de base e paridade antes da primeira mudança

Correção de desempenho que muda um número é defeito novo, e melhora afirmada sem medição de antes não
se sustenta. Antes de mexer em qualquer arquivo, as três grandezas são medidas na versão original e as
consultas de paridade são escritas e rodadas contra ela. Quando o modelo depende da data do dia, as
duas pontas são comparadas no mesmo dia, senão a paridade falha por um motivo que não tem relação com
a refatoração. O ganho é poder dizer, no fim, quanto melhorou e que nada mudou de valor.

## Modelo

### 3. Data e hora automáticas desligadas

Com a opção ligada, o Power BI cria uma tabela de data oculta para cada coluna de data do modelo,
inclusive as que ninguém usa em visual, cada uma cobrindo do menor ao maior valor da coluna. Em modelo
com muitas colunas de data, isso vira um punhado de tabelas escondidas e relações que ninguém pediu. A
opção é desligada no arquivo e o tempo passa a ser filtrado por um calendário único. Melhora tamanho e
deixa o modelo legível, e a prova é a contagem de tabelas e relações e a leitura de tamanho. A
demonstração não usa esta técnica, porque o painel de partida já tinha a opção desligada.

### 4. Calendário único gerado por parâmetro

Calendário montado com coluna calculada e exceção escrita à mão (um mês específico, uma data de
corte fixa) quebra em silêncio quando o dado avança. O calendário passa a ser gerado no Power Query, a
partir de um parâmetro de data inicial e com fim no ano seguinte, com mês e ano em coluna numérica de
ordenação para cada rótulo, e o fato liga a ele pela data. As medidas de tempo deixam de depender de
remendo, e a paridade nas medidas de ano anterior e acumulado confirma o resultado. Na demonstração,
o D7 faz do calendário a tabela de data oficial do modelo, e a padronização o gera por uma função de
calendário cuja janela, da primeira venda à data de corte, é lida do manifesto que acompanha a base,
no lugar do parâmetro de data inicial.

### 5. Relação pela chave, em direção única

Relação por rótulo em texto, como "mês/ano", costuma nascer muitos para muitos e bidirecional para
"a segmentação funcionar", e traz junto relação inativa por caminho ambíguo. Cada fato passa a ligar
às dimensões pela chave, de um para muitos, com o filtro indo da dimensão para o fato. O efeito para
quem usa é lista de segmentação que não encolhe sem motivo e medida que não muda conforme a página. A
prova é a contagem de relações por tipo e direção e a paridade dos indicadores. Na demonstração, D8.

### 6. Relação virtual quando o grão não fecha

Fato mensal ao lado de calendário diário é o caso clássico de relação que não fecha: a chave do fato é
ano e mês, e a do calendário é a data. Em vez de inventar uma coluna de texto e uma relação muitos para
muitos, a medida remove o filtro do calendário e leva ano e mês selecionados ao fato com `TREATAS`,
no grão certo. O modelo fica sem caminho ambíguo e a medida diz explicitamente como o filtro chega. A
prova é a paridade da medida nos cortes por mês, trimestre e ano.

### 7. Dimensão de papel duplo sem leitura duplicada

A mesma dimensão costuma aparecer copiada no modelo para cumprir dois papéis, como data da venda e
data de vencimento, ou cliente comprador e cliente pagador, e cada cópia lê a origem de novo. A dimensão
passa a ser lida uma vez. O segundo papel vira relação inativa ativada por `USERELATIONSHIP` dentro da
medida, ou, quando ele precisa de segmentação própria, uma tabela calculada que espelha a dimensão
lida, sem nova consulta à origem. Cai o número de leituras e o tempo de atualização, e a prova é a
contagem de partições que leem a fonte e a medição de atualização.

### 8. Atributo de cadastro fora do fato

Quando o atributo do cadastro é copiado para cada linha do fato, por mesclagem no Power Query ou por
`LOOKUPVALUE` em coluna calculada, o modelo repete o mesmo nome milhões de vezes e qualquer atributo
novo exige mexer no fato. O fato fica só com chaves, datas e valores, e o atributo passa a vir da
dimensão pela relação. Melhora tamanho e manutenção, e a prova é o tamanho por coluna e a paridade nos
cortes por atributo. Na demonstração, D1.

### 9. Coluna calculada que vira medida

Coluna de razão ou de produto calculada linha a linha, como valor vezes quantidade ou margem dividida
pela receita, é decimal de alta cardinalidade e costuma ser a maior coluna do modelo. A conta vai para a
medida, com `SUMX` quando é soma de produtos e com `DIVIDE` sobre as somas quando é razão, que é também
a forma correta de agregar percentual. Rótulo de mês feito com `FORMAT` sai para o calendário. Melhora
tamanho e atualização, e a prova é o ranking de colunas por tamanho antes e depois e a paridade da
medida. Na demonstração, D3.

### 10. Corte do que não é usado e tipo certo

Extração costuma trazer tudo "para o caso de precisar": identificador de linha, data e hora com
segundos, número de documento em texto, fatos inteiros que nenhum visual consulta. Com o inventário da
técnica 1 em mãos, o que não tem uso sai na leitura, e o que fica ganha o tipo certo já na consulta,
com número inteiro no lugar de texto e data no lugar de data e hora. Melhora tamanho e atualização, e a
prova é a contagem e a leitura de tamanho. Na demonstração, D2.

## Power Query e carga

### 11. Regra de conjunto empurrada para a origem

Painel que lê a tabela inteira e conserta no Power Query (troca de valor, extração de texto,
ordenação antes de carregar, coluna derivada) gasta a atualização fazendo o que o banco faria melhor.
Quando a fonte é relacional, a regra vai para a consulta: conversão de tipo, classificação por `CASE`,
pivô de linhas em colunas, filtro de horizonte. O Power Query fica com fonte, tipos e nomes. A
atualização encurta e a regra fica num lugar só, e a prova é o tempo de atualização e a contagem de
passos de transformação.

### 12. Uma leitura por fonte

Consulta criada por referência a outra que lê fonte grande reavalia a cadeia inteira, e cópia de
consulta lê a mesma fonte duas vezes. Os dois casos dobram trabalho sem trazer tabela nova. Cada
dimensão passa a ler o próprio cadastro, e consulta repetida vira uma só, servindo os papéis pela
técnica 7. A prova é o tempo de atualização e a contagem de partições que leem a origem. Na
demonstração, D9.

### 13. Consulta com parâmetro, grupo e passo com nome

Endereço de servidor escrito dentro de cada consulta impede trocar de ambiente sem editar uma por uma,
e passo com nome automático da interface esconde o que cada etapa faz. Servidor, base e janela de datas
viram parâmetros, as consultas ficam em grupos de parâmetros, dimensões e fatos, os passos ganham nome
que diz o que fazem, e consulta antiga que não carrega sai do projeto. A troca de desenvolvimento para
produção vira mudança de parâmetro, e a prova é a contagem estrutural. Na demonstração, a padronização
do Power Query no registro de mudanças.

## Medidas

### 14. Tabela de medidas, nome de negócio e internas ocultas

Medida espalhada pelas tabelas de fato, visual que soma a coluna por conta própria e medida técnica
aparecendo para quem monta relatório geram o mesmo indicador com formato diferente em cada lugar. As
medidas vão para uma tabela própria, com nome de negócio e unidade, em pastas por assunto; as
intermediárias ganham prefixo e ficam ocultas; e a sumarização automática das colunas numéricas é
desligada, com o modelo configurado para desestimular medida implícita. A prova é a contagem estrutural. Na
demonstração, D4 e a tabela de medidas da padronização.

### 15. Família de medidas copiadas virando uma só

É comum encontrar a mesma medida copiada uma vez por região, loja ou unidade de negócio, cada cópia
com o próprio filtro escrito à mão, e o total montado somando as cópias. Uma unidade nova exige criar
uma família inteira de medidas. A versão refatorada filtra a dimensão dentro de uma única medida,
deixa o corte por unidade para a segmentação, e quando a regra realmente difere por unidade, a
diferença vira atributo da dimensão, e não texto dentro do DAX. O número de medidas cai bastante, e a
prova é a contagem e a paridade por unidade.

### 16. DAX caro reescrito com o mesmo resultado

Fórmula copiada de fórum costuma dar o número certo do jeito mais caro: `FILTER` sobre a tabela
inteira, contagem sobre `FILTER ( VALUES (...), CALCULATE (...) )`, iterador com transição de
contexto, `IFERROR` envolvendo divisão, `GROUPBY` com `ALL` para fixar o total do mês. Cada uma é
trocada pela forma direta com o mesmo resultado: predicado de coluna com `KEEPFILTERS`,
`DISTINCTCOUNT`, `DIVIDE`, `REMOVEFILTERS` e variáveis para não recalcular a mesma subexpressão. O
ganho aparece no tempo de consulta da página, e a prova é a medição a frio e a quente junto com a
paridade. Na demonstração, D5.

### 17. Âncora temporal no dado, e não no relógio

Medida que decide passado e futuro por `TODAY` dá um número hoje e outro amanhã para a mesma seleção,
e coluna calculada com `TODAY` congela a data da última atualização sem avisar. Onde existe uma data de
referência no próprio dado, como a data de vigência de uma meta ou a data da última carga, a medida
passa a se ancorar nela, e a data do dia fica só como reserva quando não há referência no contexto. O
número fica reproduzível, e a prova é rodar a paridade em dois dias diferentes.

### 18. BLANK e zero resolvidos sem medida duplicada

Para o gráfico não ter buraco, muita gente cria uma segunda versão de cada medida que devolve zero no
lugar de BLANK, e o modelo passa a ter dois números para o mesmo indicador. A medida base continua
devolvendo BLANK quando não há dado, e a apresentação resolve o resto com formato e com a opção de
mostrar itens sem dado. A variante duplicada sai, e a prova é a contagem e a paridade.

## Relatório

### 19. Parâmetro de campo no lugar de bookmark e de página-cópia

Trocar o que o gráfico mostra (realizado contra meta, volume contra percentual, por mês ou por
categoria) costuma ser feito com bookmarks que escondem e mostram visuais empilhados, ou com uma cópia
inteira da página para cada variante. Cada estado novo multiplica visuais ocultos, botões e páginas. A
troca passa a ser um parâmetro de campo para a medida e outro para o eixo, com uma segmentação que o
usuário entende. Quando a variante muda o grão, como descer de mês para dia, um fator de
distribuição reparte o valor mensal pelos dias no próprio cálculo. A página fica com um visual por bloco, e a
prova é a contagem de bookmarks, páginas e objetos.

### 20. Faixa de KPI num visual só, e dica única

Página que cresceu por pedido tem um cartão por indicador, e cada cartão dispara a própria consulta.
Os indicadores vão para o cartão novo com vários valores, ou para um cartão de várias linhas, e as
dicas que existiam uma por variante viram uma dica que lê a seleção. A página faz menos consultas,
cada uma levando várias medidas no mesmo filtro, e nenhum número sai do alcance de quem usa. A prova é
a medição da página com a paridade de conteúdo: todo número visível antes continua visível na página,
na dica ou no detalhamento. Na demonstração, D6.

### 21. Eixo desconectado de propósito

Há eixos que não devem obedecer a uma segmentação da página, como um gráfico por categoria que
precisa mostrar todas as categorias mesmo com uma delas escolhida no filtro. Em vez de editar interação
visual por visual, o eixo vem de uma tabela desconectada e a medida busca o valor no fato com
`TREATAS`, escolhendo quais filtros respeita. O comportamento fica escrito na medida e não se perde
quando alguém copia o visual. A prova é o teste de filtro documentado.

### 22. Cor por faixa em gráfico de várias séries

Formatação condicional por regra não renderiza em gráfico com mais de uma série, e o pedido de pintar
a barra por faixa (dentro da meta, atenção, fora da meta) parece impossível. A barra é repartida em uma
série por faixa, cada uma com cor fixa, e só a série da faixa certa devolve valor em cada ponto. Quem
olha lê a situação sem legenda, e a prova é a revisão da tela contra os limites escritos na descrição
da medida.

### 23. HTML só onde o nativo não alcança

Legenda nativa lista todas as séries mesmo quando a seleção desenha só parte delas, e alguns blocos
de texto composto não cabem em cartão nativo. Nesses pontos, uma medida monta HTML, exibido por visual
de conteúdo HTML, com legenda que mostra só o que está desenhado e cartão que junta valor, rótulo e
complemento. O HTML fica restrito a leitura e não tenta ser clicável, e a prova é a revisão da tela
nas combinações de seleção.

### 24. Chassi, tema e segmentação sincronizada

Painel herdado costuma ter cada página com uma moldura, cor solta em série e segmentação repetida sem
sincronia. A tela ganha chassi comum (faixa de topo, título com a pergunta da página, painel de
filtros, conteúdo e rodapé com data da carga e recorte), tema próprio registrado no relatório, grupos
de visual nomeados e segmentações sincronizadas entre páginas, com navegação por botão de página. A
prova é a revisão da tela página a página. Na demonstração, o redesenho visual do registro de
mudanças.

## Governança e entrega

### 25. Descrição para pessoa e para assistente de IA

Medida sem descrição é usada no lugar errado, por gente e por assistente de IA que monta consulta a
partir do modelo. Toda medida visível ganha descrição no contrato "o que é e como se calcula, use
para, não use quando", e o modelo ganha uma instrução de negócio no nível do próprio modelo, com a
unidade padrão, a explicação de quais estágios do processo não se somam entre si e quais medidas
usar para cada pergunta. A prova é a cobertura de descrição por contagem. Na demonstração, a descrição de toda
medida na padronização.

### 26. Pastas, prefixos e nomes no padrão

Modelo herdado mistura gerações de nome: prefixo antigo na partição e novo na tabela, código visível
ao lado de rótulo, medida técnica entre as de negócio. Tabelas recebem prefixo de papel (`Fact_`,
`Dim_`, `Aux_`, `Bridge_`), partições e passos ganham o nome da tabela, chaves e colunas de mecânica
ficam ocultas, rótulo com ordem natural ordena por coluna numérica, e as medidas vão para pastas
numeradas. A renomeação é feita sobre o projeto em texto, com cada referência do relatório reapontada
e nenhuma sobrando sem mapa. A prova é a contagem estrutural e o relatório abrindo do zero sem erro.
Na demonstração, a padronização.

### 27. Registro de mudança e exceção declarada

Quem aceita a entrega precisa saber o que mudou, em que ordem e o que muda de comportamento. Cada
correção vira um passo próprio no histórico do projeto, com o motivo em linguagem de negócio, e o que
altera comportamento, como uma lista de segmentação que deixa de encolher ou uma conta de ano anterior
que passa a existir num corte fino, é descrito como exceção antes do aceite. A prova é o próprio
histórico. Na demonstração, o [registro de mudanças](registro-de-mudancas.md).

## Limites

Refatoração preserva comportamento, e por isso há ganho que ela não entrega sozinha. Página com
tabela no grão de linha lê a base inteira com ou sem refatoração, e mudar isso exige filtro obrigatório
ou paginação, que é decisão de quem usa o painel. Medição feita localmente não cobre capacidade do
serviço, gateway, concorrência nem rede. E o tamanho lido do arquivo salvo é uma aproximação, porque o
arquivo é comprimido: a leitura que vale é a do motor depois de uma atualização completa.
