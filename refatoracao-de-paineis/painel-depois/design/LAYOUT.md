# Layout do painel reestruturado (v2)

Escrito em 27-09-2026, antes do redesenho visual da v2, e refeito em 10-10-2026, quando o painel
foi reconstruído no padrão de desenvolvimento do serviço. Este documento diz o que cada página faz, que visual fica onde, com quais campos do modelo,
e para onde foi cada número que o painel de partida (v1) mostrava. O visual (cor, fonte, grade,
tema) está em [`SISTEMA_VISUAL.md`](SISTEMA_VISUAL.md). O [`mockup.html`](mockup.html) é o desenho de
27-09-2026 e continua valendo para o conteúdo de cada página; o chassi mudou em 10-10-2026 e está
descrito aqui.

O padrão aplicado é o de desenvolvimento de painel do serviço, e a mecânica de cada visual foi conferida
contra visuais de referência gravados pelo Desktop. Os nomes de visual reaproveitam os que já existiam sempre que o visual
continua, para o diff contar a história de uma edição e não de uma troca.

## Quem usa e o que faz

A diretoria comercial abre o painel para saber, em dois minutos, como estão a receita e a margem e
de onde a receita vem. O gerente regional abre para ver a própria região: escolhe a região e o ano,
olha os vendedores mês a mês e os maiores clientes, e desce até os itens de um pedido quando precisa
conferir alguma coisa ou levar para o Excel.

O caminho que dá certo, em passos:

1. Abre na Visão geral e lê a faixa de indicadores. Escolhendo um ano e um mês no cabeçalho, cada
   bloco passa a mostrar o valor do mês anterior e a variação numa pílula verde ou vermelha.
2. Escolhe ano, mês ou região nas caixas do canto direito do cabeçalho. Linha de produto, porte e
   vendedor, se precisar, estão no painel de filtros, e a linha de apoio da página diz isso.
3. Lê a tendência mensal contra o ano anterior e a composição por região, linha e porte.
4. Passa para Clientes e vendedores pelas abas do cabeçalho; os filtros vão junto, porque as caixas
   são sincronizadas.
5. Clica com o botão direito num cliente ou vendedor e escolhe Detalhar, Detalhe de vendas.
6. No detalhe, exporta pela opção Mais opções da tabela, Exportar dados, e volta pelo botão Voltar.

O que dá errado, e o que a tela faz:

| Situação | O que o usuário vê | Como sai |
|---|---|---|
| combinação de filtro sem venda (vendedor de uma região com outra região escolhida) | blocos com hífen, gráficos vazios com título, tabelas só com cabeçalho | "Selecionar tudo" na caixa, visível sem passar o mouse |
| mais de um mês no filtro, ou nenhum | a referência "Mês anterior" mostra hífen e a pílula some | é o comportamento correto: a comparação só tem leitura com um único mês |
| setembro de 2023 escolhido | sem mês anterior na base, a referência mostra hífen e a pílula some | é o comportamento correto, porque a base começa nesse mês |
| ano de 2023 escolhido | a variação sobre o ano anterior, na dica do cartão e do gráfico mensal, fica vazia | é o comportamento correto da regra da seção 4 da especificação |
| esqueceu um filtro no painel de filtros | cartão de filtro aplicado muda de cor e ganha contorno azul | limpar no próprio cartão |
| detalhamento aplicado ao voltar para o Detalhe pela aba | o filtro aparece na seção de detalhamento do painel de filtros | limpar no cartão; ver o risco de medição na decisão 4 |
| atualização falhou (pasta da base errada) | o Power BI mostra o erro nativo de atualização | o README da v2 ensina a apontar o parâmetro `pPastaDados` |

## Os quatro estados

**Carregando.** O Power BI desenha o indicador nativo em cada visual. Como todo bloco tem borda,
sombra e título próprios, o esqueleto da página aparece inteiro antes dos números.

**Vazio.** Não existe estado vazio de instalação, porque o painel só abre depois da atualização com a
base. O vazio real é o de filtro sem venda, tratado na tabela acima: hífen no bloco, título mantido
em todo visual e o caminho de volta visível na caixa de seleção.

**Com erro.** Os dois erros possíveis são nativos: falha de atualização e visual que não carrega. O
erro que a v1 tinha com vendedor e mês escolhidos juntos (`SAMEPERIODLASTYEAR` recusando datas
não contíguas) foi eliminado pela refatoração e não volta, porque o ano anterior desloca as datas do
calendário e não as da venda.

**Com conteúdo.** É o que o mockup mostra, no estado A do protocolo (nenhuma seleção).

## Chassi comum às quatro páginas

Toda página tem o mesmo chassi, para o usuário aprender o painel uma vez. Na Visão geral os visuais
do chassi têm o prefixo `vg`, como na tabela abaixo. Nas outras três páginas o chassi foi copiado no
Desktop, que deu a cada visual copiado um identificador gerado por ele, e o prefixo da página (`cv`,
`ct` e `dv`) ficou nos visuais de conteúdo. O cabeçalho é um grupo chamado "Cabeçalho", e a posição
dos visuais de dentro dele é relativa ao grupo, que fica em 0, 0.

| Nome | Tipo | Campos | x | y | L | A | Conteúdo |
|---|---|---|---|---|---|---|---|
| `xxGrupoCabecalho` | grupo | | 0 | 0 | 1280 | 100 | agrupa a faixa do topo, em modo de escala |
| `xxFaixa` | forma | | 0 | 0 | 1280 | 100 | retângulo `#E8EEF5`, sem contorno |
| `xxCabecalho` | caixa de texto | | 20 | 24 | 84 | 48 | logotipo "B&B" em Segoe UI Black 20 pt, `#16263D` |
| `xxPergunta` | caixa de texto | | 116 | 6 | 620 | 60 | pergunta da página em Semibold 13 pt e linha de apoio em 9 pt |
| `xxNavegador` | navegador de páginas | | 116 | 70 | 620 | 30 | quatro abas com os cantos de cima cortados; a aba da página atual tem a cor da página e parece recortada na faixa |
| `xxSegAno` | segmentação suspensa | `Dim_Calendario[Ano]` | 820 | 15 | 110 | 70 | cabeçalho "Ano" |
| `xxSegMes` | segmentação suspensa | `Dim_Calendario[Nome do Mes]` | 940 | 15 | 150 | 70 | cabeçalho "Mês" |
| `xxSegRegiao` | segmentação suspensa | `Dim_Regiao[Regiao]` | 1100 | 15 | 160 | 70 | cabeçalho "Região" |
| `xxRodape` | cartão novo | `[.rodape_pagina]` | 16 | 680 | 1248 | 40 | texto centralizado em Semibold 8 pt: "Dado 100% sintético, gerado para demonstração", a janela da base, "valores em R$", "região é a do cliente" e a assinatura B&B |

O conteúdo de cada página ocupa a faixa de y 108 a 680. As três segmentações ficam nos grupos de
sincronização `segAno`, `segMes` e `segRegiao`, com filtro e campo sincronizados nas quatro páginas,
e com "Selecionar tudo" ligado. O rodapé lê a primeira e a última data do calendário, então a janela
escrita nele acompanha a base sozinha quando ela for gerada de novo.

**Filtros de relatório**, no painel de filtros, valendo para as quatro páginas:
`Dim_Produto[Linha de Produto]` com o nome "Linha de produto", `Dim_Cliente[Porte]` com o nome "Porte
do cliente" e `Dim_Vendedor[Vendedor]` com o nome "Vendedor", este com busca.

## Página 1, Visão geral

**Objetivo:** mostrar em uma tela como estão a receita e a margem, como elas evoluem mês a mês contra
o ano anterior, e de onde a receita vem por região, linha de produto e porte de cliente.

Pergunta: "Como estão a receita e a margem, e de onde vem a receita?". Linha de apoio: "Ano, mês e
região ao lado. Linha de produto, porte e vendedor ficam no painel de filtros, à direita."

| Nome | Tipo | Campos | x | y | L | A | Título e subtítulo |
|---|---|---|---|---|---|---|---|
| `vgCartaoIndicadores` | cartão novo (`cardVisual`), oito blocos numa linha | ver a tabela do cartão | 16 | 110 | 1248 | 150 | sem título |
| `vgLinhaReceitaMes` | colunas e linha (`lineClusteredColumnComboChart`) | eixo `Dim_Calendario[Mes.Ano]`; colunas `[Receita Liquida (R$)]`; linha tracejada `[Receita Ano Anterior (R$)]`; dica `[Receita Acumulada no Ano (R$)]` e `[Crescimento sobre Ano Anterior (%)]` | 16 | 266 | 828 | 203 | "Receita líquida por mês" / "Colunas: mês · linha tracejada: mesmo mês do ano anterior · acumulado no ano e variação na dica" |
| `vgBarraRegiao` | barras agrupadas | eixo `Dim_Regiao[Regiao]`; valor `[Receita Liquida (R$)]`, ordem decrescente; dica `[Participacao na Receita (%)]` e `[Margem (%)]` | 856 | 266 | 408 | 203 | "Receita líquida por região" / "Região do cliente · participação e margem na dica" |
| `vgBarraCategoria` | colunas agrupadas | eixo `Dim_Produto[Linha de Produto]`; valor `[Receita Liquida (R$)]`, ordem decrescente; dica `[Margem (%)]` | 16 | 479 | 303 | 201 | "Receita líquida por linha de produto" |
| `vgBarraPorte` | colunas agrupadas | eixo `Dim_Cliente[Porte]`, ordem crescente do rótulo (Grande, Médio, Pequeno); valor `[Receita Liquida (R$)]`; dica `[Margem (%)]` | 331 | 479 | 303 | 201 | "Receita líquida por porte de cliente" |
| `vgTabelaTop20Produtos` | tabela | `Dim_Produto[Produto]` como "Produto", `Dim_Produto[Linha de Produto]` como "Linha", `[Receita Liquida (R$)]` com barra de dados, `[Quantidade (un)]` como "Unidades", `[Margem (%)]`; ordem por receita decrescente; filtro Top 20 travado e oculto; total desligado | 646 | 479 | 618 | 201 | "20 produtos de maior receita" / "No filtro atual, do maior para o menor" |

Em todo visual que mostra o nome de uma medida, a projeção leva o rótulo que o usuário já via
("Receita Líquida", "Margem %", "Ticket Médio"), e o nome técnico com a unidade fica só no modelo.

**A tabela dos 20 produtos** continua com a coluna Linha entre Produto e Receita Líquida, a barra de
dados em `#C9D8E8` gravada pelo Desktop, com o valor escrito por cima, e as larguras de 140, 112, 196,
66 e 66 px.

**O cartão de indicadores** segue a faixa de KPIs do padrão: um único cartão novo na largura da
página, com um bloco por indicador. A estrutura veio inteira de um cartão de referência gravado pelo
Desktop: uma projeção por bloco no papel `Data`, e para cada
bloco as entradas `referenceLabel`, `referenceLabelTitle`, `referenceLabelValue` e
`referenceLabelDetail` com o seletor do bloco e um identificador próprio. Cada bloco tem fundo branco,
contorno fino, cantos arredondados de raio 15, sombra e brilho leves, e a barra de destaque à esquerda
em `#1D5A8C`.

| Bloco | Rótulo | Valor | Rótulo de referência | Detalhe |
|---|---|---|---|---|
| 1 | Receita líquida | `[.kpi_receita]` | "Mês anterior:" `[.kpi_receita_mes_anterior]` | pílula com `[.ux_var_receita]`, cor por `[.cor_var_receita]` |
| 2 | Margem | `[.kpi_margem]` | "Mês anterior:" `[.kpi_margem_mes_anterior]` | pílula com `[.ux_var_margem]`, cor por `[.cor_var_margem]` |
| 3 | Margem % | `[.kpi_margem_pct]` | "Mês anterior:" `[.kpi_margem_pct_mes_anterior]` | pílula com `[.ux_var_margem_pct]` em pontos percentuais, cor por `[.cor_var_margem_pct]` |
| 4 | Quantidade | `[.kpi_quantidade]` | "Mês anterior:" `[.kpi_quantidade_mes_anterior]` | pílula com `[.ux_var_quantidade]`, cor por `[.cor_var_quantidade]` |
| 5 | Pedidos | `[.kpi_pedidos]` | "Mês anterior:" `[.kpi_pedidos_mes_anterior]` | pílula com `[.ux_var_pedidos]`, cor por `[.cor_var_pedidos]` |
| 6 | Ticket médio | `[.kpi_ticket]` | "Mês anterior:" `[.kpi_ticket_mes_anterior]` | pílula com `[.ux_var_ticket]`, cor por `[.cor_var_ticket]` |
| 7 | Clientes com compra | `[.kpi_clientes]` | "Mês anterior:" `[.kpi_clientes_mes_anterior]` | pílula com `[.ux_var_clientes]`, cor por `[.cor_var_clientes]` |
| 8 | Linha Premium | `[.kpi_linha_premium]` | "Participação:" `[.kpi_participacao_linha_premium]` | sem pílula |

O valor e a referência de todos os blocos chegam ao cartão como texto pronto. Desde 11-10-2026 as
dezesseis medidas de exibição `.kpi_*`, ocultas em `.Internas\UI`, leem a medida de negócio e
escrevem o número com `FORMAT` na cultura pt-BR, como as `.ux_var_*` da pílula, que sempre saíram
certas. O motivo foi visto na tela: o cartão novo formata a referência fora da localização do modelo,
com ponto decimal ("Participação: 66.7%", "Mês anterior: 39.9%"), mesmo com medida de formato fixo, e
o formato dinâmico que fazia a abreviação não abreviou a faixa de cem milhões a um bilhão, saindo
"R$ 952.94..." no lugar de "R$ 953 Mi".

As faixas são as mesmas de antes: R$ 10,6 Bi a partir de um bilhão, R$ 953 Mi de cem milhões para
cima, R$ 24,8 Mi a partir de um milhão e o valor cheio sem centavos abaixo disso (R$ 339.930);
quantidade em 37,6 Mi a partir de um milhão e cheia abaixo (1.237); ticket médio cheio (R$ 8.517);
pedidos e clientes com milhar (274.142 e 20.000); margem % e participação com uma casa (40,8% e
66,7%). Cada corte fica meio passo abaixo da fronteira, para o arredondamento não escrever "1.000 Mi"
nem "R$ 1.000.000". A referência do mês anterior usa o mesmo formato do valor do bloco, para os dois
números se compararem na mesma grafia. Medida vazia continua vazia, e o cartão desenha o hífen. As
regras de cor da pílula leem as `.cor_var_*`, que seguem numéricas, e a ordenação do cartão não muda
nada na tela, porque os blocos seguem a ordem das projeções. As medidas de negócio continuam com
formato fixo, e por isso nenhuma tabela, gráfico ou consulta de paridade muda.

A pílula segue o padrão de cor por código. A medida `.ux_var_*` escreve a seta (`UNICHAR`) e a
variação com uma casa, e a medida `.cor_var_*` devolve um código: 0 sem comparação, 1 favorável e 2
desfavorável. O cartão traduz o código por regra condicional na cor do texto e na cor de fundo do
detalhe, `#1E7A4C` para 1 e `#B3261E` para 2, e o fundo com 90% de transparência desenha a pílula
clara atrás do texto. A seta acompanha a cor, para quem não distingue verde de vermelho. Nos sete
indicadores comparados, subir é favorável.

A comparação só aparece com um único mês no contexto, pela guarda `HASONEVALUE` em
`Dim_Calendario[Mes.Ano]` nas medidas do mês anterior. A Linha Premium mostra a participação na
receita no lugar do mês anterior, porque ela é uma fatia da receita do bloco 1, e a pergunta que ela
responde é quanto da receita vem dela.

O crescimento sobre o ano anterior, que a v1 mostrava em cartão próprio, está na dica de cada mês do
gráfico mensal. O cartão não repete esse número na própria dica nesta
versão.

**Eixo do gráfico mensal.** A unidade do eixo de valor é automática, assim como as casas. Com a
unidade fixa em milhões e sem casas, um mês e um vendedor escolhidos punham "R$ 0 Mi" nas três
marcas do eixo, e agora a escala acompanha o filtro (R$ 400 Mi no ano inteiro, R$ 300 Mil num mês
de um vendedor).

**Ordem de tabulação:** abas, pergunta, Ano, Mês, Região, cartão, gráfico mensal, região, linha de
produto, porte, tabela.

**Texto alternativo:** cartão, "Indicadores do filtro atual, um por bloco: receita líquida, margem,
margem percentual, quantidade, pedidos, ticket médio, clientes com compra e receita da Linha
Premium. Com um único mês escolhido, cada bloco mostra o valor do mês anterior e a variação com seta e
cor; a Linha Premium mostra a participação na receita"; gráfico mensal, "Receita líquida por mês
comparada ao mesmo mês do ano anterior"; barras e colunas, "Receita líquida por região", "por linha de
produto" e "por porte de cliente"; tabela, "Os 20 produtos de maior receita líquida no filtro atual".

## Página 2, Clientes e vendedores

**Objetivo:** mostrar quem gera a receita, com cada vendedor mês a mês, os maiores clientes e a
participação de cada região comparada ao peso dela no mercado.

Pergunta: "Quem gera a receita, e cada região vende na proporção do seu mercado?". Linha de apoio:
"Clique com o botão direito num cliente ou vendedor e escolha Detalhar para ver os itens de venda."

| Nome | Tipo | Campos | x | y | L | A | Título e subtítulo |
|---|---|---|---|---|---|---|---|
| `cvMatrizVendedorMes` | matriz | linhas `Dim_Vendedor[Vendedor]`; colunas `Dim_Calendario[Mes.Ano]`; valores `[Receita Liquida (R$)]`; linhas ordenadas por receita decrescente | 16 | 108 | 828 | 348 | "Receita líquida por vendedor e mês" / "Do vendedor de maior receita para o de menor" |
| `cvTabelaRegiaoPeso` | tabela | `Dim_Regiao[Regiao]` como "Região", `[Receita Liquida (R$)]`, `[Participacao na Receita (%)]`, `[Peso de Mercado (%)]`; ordem por receita decrescente; total ligado | 16 | 468 | 828 | 212 | "Participação na receita e peso de mercado, por região" / "Participação acima do peso quer dizer região vendendo mais que o tamanho do seu mercado" |
| `cvRankingClientes` | tabela | `Dim_Cliente[Cliente]` como "Cliente", `[Receita Liquida (R$)]`, `[Pedidos]`, `[Ticket Medio (R$)]`; ordem por receita decrescente; total ligado | 856 | 108 | 408 | 572 | "Clientes por receita líquida" / "Todos os clientes com compra no filtro, do maior para o menor" |

No estado A, a matriz tem 36 meses e rola para a direita, com o nome do vendedor fixo. No uso típico
do gerente, com um ano escolhido, os meses do ano e o total cabem na largura sem rolagem.

**Ordem de tabulação:** abas, pergunta, Ano, Mês, Região, matriz, tabela de região, ranking.
**Texto alternativo:** "Receita líquida de cada vendedor por mês", "Participação de cada região na
receita comparada ao peso de mercado", "Clientes ordenados pela receita líquida, com pedidos e ticket
médio".

## Página 3, Clientes por trimestre

**Objetivo:** mostrar, cliente a cliente, a receita e a margem de cada trimestre, para quem precisa
acompanhar a carteira ao longo do tempo.

Pergunta: "Quais clientes compram mais a cada trimestre, e com que margem?". Linha de apoio: "Com um
ano escolhido, os quatro trimestres cabem lado a lado. Ordenado pela receita total do cliente."

| Nome | Tipo | Campos | x | y | L | A | Título e subtítulo |
|---|---|---|---|---|---|---|---|
| `ctMatrizClienteTrimestre` | matriz | linhas `Dim_Cliente[Cliente]`; colunas `Dim_Calendario[Ano]` e `Dim_Calendario[Trimestre]`, expandida até o trimestre; valores `[Receita Liquida (R$)]` e `[Margem (%)]`; linhas ordenadas por receita decrescente | 16 | 108 | 1248 | 572 | "Receita líquida e margem por cliente e trimestre" / "Role para a direita para os trimestres seguintes; o nome do cliente fica fixo" |

O trimestre aparece como Tri. 1 a Tri. 4, o rótulo que a função de calendário grava.

**Texto alternativo:** "Receita líquida e margem de cada cliente por trimestre".

## Página 4, Detalhe de vendas

**Objetivo:** mostrar os itens de cada pedido, linha a linha, para conferência e exportação.

Pergunta: "Quais itens compõem cada pedido?". Linha de apoio: "Uma linha por produto vendido. Para
levar ao Excel, use Mais opções no canto da tabela e Exportar dados."

| Nome | Tipo | Campos | x | y | L | A | Título e subtítulo |
|---|---|---|---|---|---|---|---|
| `dvVoltar` | botão, ação Voltar | | 746 | 34 | 64 | 32 | texto "‹ Voltar", na faixa do cabeçalho, entre a pergunta e as segmentações |
| `dvTabelaLinhas` | tabela | `Fact_Vendas[Numero Pedido]` como "Pedido", `Dim_Calendario[Data]` como "Data", `Dim_Cliente[Cliente]` como "Cliente", `Dim_Produto[Produto]` como "Produto", `[Quantidade (un)]`, `[Receita Bruta (R$)]`, `[Receita Liquida (R$)]`, `[Custo (R$)]`, `[Margem (R$)]`; ordem por pedido crescente, igual à v1; total ligado | 16 | 108 | 1248 | 572 | "Itens de venda por pedido" / "Pedidos em ordem de emissão" |

Larguras de coluna da tabela: 118, 84, 210, 170, 80, 140, 140, 140 e 140 px.

**Detalhamento:** a página recebe detalhamento por `Dim_Cliente[Cliente]`, `Dim_Produto[Produto]` e
`Dim_Vendedor[Vendedor]`, mantendo os filtros. Ela continua visível nas abas. A ordem e os campos da
tabela não mudam, para a consulta da página de referência da medição continuar a mesma da v1.

**Texto alternativo:** "Itens de venda por pedido, com cliente, produto, quantidade e valores".

## Visuais e consultas na v1 e na v2

Elementos contam tudo que está na página, inclusive grupo, forma e caixa de texto. Consultas contam o
que pede dado ao modelo.

| Página | v1 | v2 só refatorada | v2 padronizada, 10-10-2026 |
|---|---|---|---|
| Visão geral | 22 visuais, 19 consultas (ensaio de 27-09-2026) | 10 visuais, 10 consultas | 15 elementos, 10 consultas (11 se o cartão separar as referências) |
| Clientes e vendedores | 4 visuais, 4 consultas | 4 visuais, 4 consultas | 12 elementos, 7 consultas |
| Clientes por trimestre | na Visão geral da v1 | 1 visual, 1 consulta | 10 elementos, 5 consultas |
| Detalhe de vendas | 1 visual, 1 consulta | 1 visual, 1 consulta | 11 elementos, 5 consultas |

Nas páginas além da Visão geral, a v2 consulta mais que a v1 por dois motivos: as três segmentações
sincronizadas pedem a lista de valores ao abrir, e o rodapé pede a janela da base ao calendário. São
consultas pequenas (quatro anos, doze meses, cinco regiões e duas datas) que rodam em paralelo com o
visual principal. Na medição de 06-10-2026 as listas das segmentações não geraram consulta a quente,
porque ficavam no cache. No Detalhe de vendas, que é a página de referência da medição, essa
diferença vai declarada no README (decisão 4).

## Paridade de conteúdo

Todo número que a v1 mostrava continua ao alcance. A coluna "Destino" diz onde.

### Visão geral da v1

| # | Indicador na v1 | Visual da v1 | Destino na v2 |
|---|---|---|---|
| 1 | Receita líquida | cartão | Visão geral, bloco 1 do cartão |
| 2 | Margem (soma de `Lucro`) | cartão | Visão geral, bloco 2 |
| 3 | Margem % | cartão | Visão geral, bloco 3 |
| 4 | Quantidade | cartão | Visão geral, bloco 4 |
| 5 | Pedidos | cartão | Visão geral, bloco 5 |
| 6 | Ticket médio | cartão | Visão geral, bloco 6 |
| 7 | Clientes com compra | cartão | Visão geral, bloco 7 |
| 8 | Crescimento sobre ano anterior % | cartão | Visão geral, dica de cada mês do gráfico mensal |
| 9 | Receita Linha Premium | cartão | Visão geral, bloco 8; o mesmo valor aparece na coluna Linha Premium |
| 10 | Receita líquida por mês | linha | Visão geral, colunas do gráfico mensal |
| 11 | Receita ano anterior por mês | linha | Visão geral, linha tracejada do gráfico mensal |
| 12 | Receita acumulada no ano por mês | colunas | Visão geral, dica de cada mês do gráfico mensal e Mostrar como tabela |
| 13 | Receita líquida por região | barras | Visão geral, barras por região |
| 14 | Receita líquida por categoria | barras | Visão geral, colunas por linha de produto |
| 15 | Receita líquida por porte | rosca | Visão geral, colunas por porte |
| 16 | Receita e margem % por cliente e trimestre | matriz | página Clientes por trimestre |
| 17 | Receita, quantidade e margem % dos 20 maiores produtos | tabela | Visão geral, tabela dos 20 produtos |
| 18 a 20 | Segmentações de ano, mês e região | segmentação | segmentações sincronizadas do cabeçalho, em todas as páginas |
| 21 a 23 | Segmentações de categoria, porte e vendedor | segmentação | painel de filtros, nível de relatório |

### Clientes e vendedores da v1

| Indicador na v1 | Destino na v2 |
|---|---|
| Receita por vendedor e mês | mesma página, matriz |
| Ranking de clientes com receita, pedidos e ticket | mesma página, mesma tabela |
| Receita, participação e peso de mercado por região | mesma página, mesma tabela |
| Segmentação de região | segmentação sincronizada do cabeçalho |

### Detalhe de vendas da v1

| Indicador na v1 | Destino na v2 |
|---|---|
| Tabela no grão de linha, com pedido, data, cliente, produto, quantidade e valores | mesma página, mesma tabela, mesmos campos e mesma ordem, mais o detalhamento de entrada |

Das dezesseis medidas de paridade, `Receita Bruta (R$)` e `Custo (R$)` aparecem no Detalhe de vendas,
`Participacao na Receita (%)` e `Peso de Mercado (%)` em Clientes e vendedores, e `Linhas de Venda`
segue como controle técnico fora das páginas, como na v1.

## O que o desenho pede ao modelo

Desde 10-10-2026 o modelo segue o padrão: tabelas `Fact_` e `Dim_`, todas as medidas em `Medidas`,
e o calendário da função `fn_Calendario`. Do lado do desenho, o que importa:

| Item | Onde | Por quê |
|---|---|---|
| cadeia do mês anterior por indicador da faixa: o valor do mês anterior, a variação, o texto `.ux_var_*` e o código de cor `.cor_var_*` | pastas `06 Mes Anterior` e `.Internas\UI` | alimenta o rótulo de referência e a pílula de cada bloco |
| `Participacao Linha Premium na Receita (%)` | pasta `01 Receita` | complemento do bloco da Linha Premium |
| medidas de exibição `.kpi_*`, uma por valor e uma por referência de cada bloco do cartão | pasta `.Internas\UI` | texto em pt-BR no cartão, com a abreviação por faixa, sem mudar o formato da medida de negócio |
| `.rodape_pagina` | pasta `.Texto` | texto do rodapé, com a janela lida do calendário |
| `Dim_Calendario[Nome do Mes]` ordenado por `Mes`, `Dim_Calendario[Mes.Ano]` ordenado por `Ordem` | `Dim_Calendario` | segmentação de mês em ordem de calendário e eixo mensal em ordem cronológica |
| máscara `\P\V\-000000000` em `Fact_Vendas[Numero Pedido]` | `Fact_Vendas` | o pedido guardado como número aparece como PV-000000123 |
| moeda `\R\$ #,0.00`, percentual com uma casa e seta no crescimento | `Medidas` | formato na medida, igual em todo visual |

As seis medidas de exibição "(cartão)" do cartão anterior saíram do modelo na reconstrução, junto
com as sete medidas de variação sobre o ano anterior. A aposta era a unidade de exibição do cartão
novo fazer a abreviação, e ela escreveu ponto decimal em inglês. O formato curto voltou para a medida
em 10-10-2026, em nove medidas `.kpi_*` com formato dinâmico, e em 11-10-2026 elas passaram a devolver
texto, porque o cartão continuou escrevendo a referência com ponto decimal e não abreviou uma das
faixas. São dezesseis: oito para o valor de cada bloco e oito para a referência, sete do mês anterior
e a participação da Linha Premium.

## O que o desenho pede ao relatório, fora dos visuais

Grupos de sincronização das três segmentações, os três filtros de relatório com nome de negócio, o
filtro dos 20 produtos travado e oculto, o detalhamento no Detalhe de vendas, e o tema do
`SISTEMA_VISUAL.md` aplicado como tema personalizado do relatório. O painel de filtros continua
recolhido ao salvar.

## Decisões tomadas sobre o desenho

As quatro decisões foram tomadas em 27-09-2026, todas conforme a recomendação do desenho.

| # | Decisão | Escolha |
|---|---|---|
| 1 | tom do painel | azul petróleo sobre barra marinho, que é o desenho do mockup |
| 2 | estado do print de capa | arquivo salvo sem seleção e print com o ano de 2026 escolhido nas duas pontas. Sem seleção, o crescimento sobre o ano anterior compara três anos com dois, e esse número na capa confunde quem lê |
| 3 | acentos da base ("Medio", "Marco", "Sabado") | corrigidos no gerador para toda saída, sem mudar nenhum número |
| 4 | moldura e detalhamento na página de referência da medição | mesma moldura em todas as páginas, com as consultas a mais do Detalhe de vendas declaradas no README, e a conferência de que nenhum filtro de detalhamento ficou salvo entrando no protocolo de medição |
