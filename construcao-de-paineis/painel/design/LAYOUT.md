# Layout do painel comercial

Escrito em 11-10-2026, antes de as páginas serem escritas em PBIR. Este documento diz o que cada
página responde, que visual fica onde, com quais campos do modelo, de que visual existente cada um parte e
o que o desenho pede ao modelo. O visual (cor, fonte, grade, tema) está em
[`SISTEMA_VISUAL.md`](SISTEMA_VISUAL.md) e o desenho de tela, com números plausíveis, em
[`mockup.html`](mockup.html).

Todas as páginas têm 1280 x 720. Posição e tamanho estão em pontos do Power BI, na ordem x, y,
largura (L) e altura (A). Campo de medida vem como `Medidas[Nome]` e campo de coluna como
`Tabela[Coluna]`, com o nome técnico exato do modelo. Os papéis são os nomes que o PBIR usa em
`queryState`: `Data` no cartão, `Category`, `Y`, `Y2` e `Tooltips` nos gráficos, `Values` na tabela e
na segmentação, `Rows`, `Columns` e `Values` na matriz.

## Quem usa e o que faz

A diretoria comercial abre o painel na reunião mensal de resultado e precisa saber, em dois minutos,
se o mês foi melhor ou pior que o mesmo mês do ano anterior e de onde a receita veio, para decidir
onde pôr esforço no mês seguinte. Depois passa por margem e desconto para rever a política por porte
e linha, e por vendedores para o acompanhamento individual. O gerente comercial volta toda semana à
página de clientes para tirar a lista de reativação da sua região.

O caminho que dá certo, em passos:

1. Abre na Visão executiva, escolhe o ano e o mês no cabeçalho e lê o cartão: receita líquida e
   margem % com o valor do ano anterior e a variação numa pílula com seta.
2. Lê o gráfico mensal, que mostra o ano inteiro em volta do mês escolhido, e a tabela de regiões,
   que diz quem cresceu e quem caiu.
3. Passa para Margem e desconto pela aba e lê a matriz de porte por linha: onde o desconto é maior e
   a margem é menor.
4. Passa para Vendedores, clica num vendedor da tabela e a página inteira passa a mostrar só ele.
5. Na semana, abre Clientes, escolhe a região na caixa Região e exporta a lista de reativação pela
   opção Mais opções da tabela, Exportar dados.

O que dá errado, e o que a tela faz:

| Situação | O que o usuário vê | Como sai |
|---|---|---|
| nenhum ano escolhido, ou mais de um | a referência "Ano anterior" mostra hífen e a pílula some; a linha de apoio pede um ano | escolher um ano na caixa Ano |
| ano de 2023 escolhido | sem ano anterior na base, referência com hífen, pílula some, linha tracejada vazia | é o comportamento correto, porque a base começa em setembro de 2023 |
| mês escolhido sem ano | o cartão soma aquele mês em todos os anos e a comparação some | escolher também o ano |
| crescimento na tabela de regiões sem ano escolhido | as colunas Ano anterior e Crescimento ficam vazias, porque o mesmo período do ano anterior não está inteiro na base | escolher um ano; o subtítulo da tabela avisa |
| combinação de filtro sem venda | blocos com hífen, gráficos vazios com título, tabelas só com cabeçalho | "Selecionar tudo" na caixa, visível sem passar o mouse |
| lista de reativação vazia | a tabela aparece só com o cabeçalho | é a leitura certa: ninguém da região está sem compra há 90 dias; o subtítulo diz isso |
| filtro esquecido no painel de filtros | o cartão do filtro aplicado muda de cor e ganha contorno azul | limpar no próprio cartão |
| vendedor clicado na tabela de vendedores | a página inteira mostra só aquele vendedor | clicar de novo na mesma linha, ou num espaço vazio da tabela |
| atualização falhou (pasta da base errada) | o Power BI mostra o erro nativo de atualização | o README ensina a apontar o parâmetro `pPastaDados` |

## Os quatro estados

**Carregando.** O Power BI desenha o indicador nativo em cada visual. Como todo bloco tem borda,
sombra e título próprios, o esqueleto da página aparece inteiro antes dos números.

**Vazio.** Não existe estado vazio de instalação, porque o painel só abre depois da atualização com a
base. O vazio real é o de filtro sem venda e o da lista de reativação sem cliente parado, tratados
na tabela acima: hífen no bloco, título mantido em todo visual, subtítulo que explica a lista vazia e
o caminho de volta visível na caixa de seleção.

**Com erro.** Os erros possíveis são nativos: falha de atualização e visual que não carrega. A leitura
errada do crescimento sem ano escolhido não acontece, porque o ano anterior volta vazio quando o
período deslocado não está inteiro na base, e o subtítulo da tabela de regiões diz isso.

**Com conteúdo.** É o que o mockup mostra, com o ano de 2026 e o mês de agosto escolhidos.

O arquivo é salvo sem seleção nas caixas, porque um ano salvo fica velho na virada do ano e a
atualização é diária. A linha de apoio da Visão executiva pede o ano logo na abertura.

## Chassi comum às quatro páginas

Toda página tem o mesmo chassi, para o usuário aprender o painel uma vez. Nos nomes abaixo, `xx` é
o prefixo da página: `ve` na Visão executiva, `md` em Margem e desconto, `cl` em Clientes e `vd` em
Vendedores. O cabeçalho é um grupo, e a posição dos visuais de dentro dele é relativa ao grupo, que
fica em 0, 0. Os pontos de partida marcados como "caso de refatoração" são os visuais de
`../../../refatoracao-de-paineis/painel-depois/painel-depois.Report/definition/pages/VisaoGeral/visuals/`;
os outros partem de visuais nativos gravados pelo Power BI Desktop.

| Nome | Tipo | x | y | L | A | Campos por papel | Conteúdo | Ponto de partida |
|---|---|---|---|---|---|---|---|---|
| `xxGrupoCabecalho` | grupo (`visualGroup`, sem `visualType`) | 0 | 0 | 1280 | 109,94 | | agrupa a faixa do topo, em modo de escala | `visualgroup` |
| `xxFaixa` | `shape` | 0 | 0 | 1280 | 100 | | retângulo `#E8EEF5`, sem contorno | caso de refatoração, `vgFaixa` |
| `xxLogotipo` | `textbox` | 20 | 24 | 84 | 48 | | "B&B" em Segoe UI Black 20 pt, `#16263D`, igual ao cabeçalho do caso de refatoração | caso de refatoração, `vgCabecalho` |
| `xxPergunta` | `textbox` | 116 | 6 | 620 | 60 | | pergunta em Semibold 13 pt `#16263D` e linha de apoio em 9 pt `#3D4756` | caso de refatoração, `vgPergunta` |
| `xxNavegador` | `pageNavigator` | 116,22 | 56,94 | 620,11 | 53 | | quatro abas de 155 px com os cantos de cima cortados; a aba atual tem a cor da página | caso de refatoração, `vgNavegador` |
| `xxSegAno` | `slicer` | 820 | 15 | 110 | 70 | `Values`: `Dim_Calendario[Ano]` | cabeçalho "Ano", grupo de sincronização `segAno` | caso de refatoração, `vgSegAno` |
| `xxSegMes` | `slicer` | 940 | 15 | 150 | 70 | `Values`: `Dim_Calendario[Nome do Mes]` | cabeçalho "Mês", grupo `segMes` | caso de refatoração, `vgSegMes` |
| `xxSegRegiao` | `slicer` | 1100 | 15 | 160 | 70 | `Values`: `Dim_Regiao[Regiao]` | cabeçalho "Região", grupo `segRegiao` | caso de refatoração, `vgSegRegiao` |
| `xxRodape` | `cardVisual` | 16 | 680 | 1248 | 40 | `Data`: `Medidas[.rodape_pagina]` | texto centralizado em Semibold 8 pt `#5F6B7A` | caso de refatoração, `vgRodape` |

O texto do rodapé, devolvido por `.rodape_pagina`: "Dado 100% sintético, gerado para demonstração ·
base de set/2023 até 31/08/2026 · valores em R$ · região é a do cliente · B&B". A janela é lida da
primeira e da última data do calendário.

As abas, na ordem: "Visão executiva", "Margem e desconto", "Clientes" e "Vendedores". As pastas de
página no PBIR: `VisaoExecutiva`, `MargemDesconto`, `Clientes` e `Vendedores`.

**Filtros de relatório**, no painel de filtros, valendo para as quatro páginas:
`Dim_Produto[Linha de Produto]` com o nome "Linha de produto", `Dim_Cliente[Porte]` com o nome
"Porte do cliente" e `Dim_Vendedor[Vendedor]` com o nome "Vendedor", este com busca. O painel abre
recolhido.

**Interação desligada.** Em cada página, a caixa `xxSegMes` não filtra o gráfico mensal da página
(`veComboReceitaMes`, `mdComboDescontoMes`, `clComboClientesMes` e `vdComboVendedorMes`), por uma
entrada `NoFilter` em `visualInteractions` do `page.json`. A estrutura segue a que o
Desktop grava para interações entre visuais. A caixa Ano e a caixa Região continuam filtrando
tudo.

## Página 1, Visão executiva

**Pergunta de negócio:** o resultado do período está melhor ou pior que o do ano anterior, e de onde
vem a receita? **Decisão que apoia:** onde concentrar esforço comercial no mês seguinte.

Na tela: "O resultado está acima do ano anterior, e de onde vem a receita?". Linha de apoio:
"Escolha um ano para ver a comparação. Linha, porte e vendedor ficam no painel de filtros."

| Nome | Tipo | x | y | L | A | Campos por papel | Ordenação | Título e subtítulo | Ponto de partida |
|---|---|---|---|---|---|---|---|---|---|
| `veCartaoIndicadores` | `cardVisual`, seis blocos numa linha | 16 | 110 | 1248 | 150 | ver a tabela do cartão | ordem das projeções | sem título | caso de refatoração, `vgCartaoIndicadores`; estrutura em visual nativo do Desktop |
| `veComboReceitaMes` | `lineClusteredColumnComboChart` | 16 | 270 | 616 | 410 | `Category`: `Dim_Calendario[Mes.Ano]`; `Y`: `Medidas[Receita Liquida (R$)]`; `Y2`: `Medidas[Receita Ano Anterior (R$)]`, linha tracejada `#7D8796` (`lineStyles` com `dashed`, como no ponto de partida); `Tooltips`: `Medidas[Crescimento sobre Ano Anterior (%)]`, `Medidas[Receita Acumulada no Ano (R$)]`, `Medidas[Pedidos]` | `Mes.Ano` crescente, pela coluna `Ordem` | "Receita líquida por mês" / "Linha tracejada: mesmo mês do ano anterior · crescimento e acumulado na dica · a caixa Mês não filtra" | caso de refatoração, `vgLinhaReceitaMes` |
| `veTabelaRegiao` | `tableEx` | 644 | 270 | 620 | 232 | `Values`: `Dim_Regiao[Regiao]` como "Região", `Medidas[Receita Liquida (R$)]` com barra de dados `#C9D8E8`, `Medidas[Participacao na Receita (%)]` como "Participação", `Medidas[Receita Ano Anterior (R$)]` como "Ano anterior", `Medidas[Crescimento sobre Ano Anterior (%)]` como "Crescimento"; total ligado | receita líquida decrescente | "Receita líquida por região, contra o ano anterior" / "Ano anterior e crescimento com um ano escolhido; sem ano, as duas colunas ficam vazias" | caso de refatoração, `vgTabelaTop20Produtos` (barra de dados), sem o filtro Top 20 |
| `veBarraLinha` | `clusteredBarChart` | 644 | 512 | 304 | 168 | `Category`: `Dim_Produto[Linha de Produto]`; `Y`: `Medidas[Receita Liquida (R$)]`; `Tooltips`: `Medidas[Participacao na Receita (%)]`, `Medidas[Crescimento sobre Ano Anterior (%)]` | receita líquida decrescente | "Receita líquida por linha de produto" / "Participação e crescimento na dica" | caso de refatoração, `vgBarraRegiao` |
| `veBarraPorte` | `clusteredBarChart` | 960 | 512 | 304 | 168 | `Category`: `Dim_Cliente[Porte]`; `Y`: `Medidas[Receita Liquida (R$)]`; `Tooltips`: `Medidas[Participacao na Receita (%)]`, `Medidas[Crescimento sobre Ano Anterior (%)]` | receita líquida decrescente | "Receita líquida por porte de cliente" / "Participação e crescimento na dica" | caso de refatoração, `vgBarraRegiao` |

Larguras de coluna da tabela de regiões: 110, 170, 84, 140 e 84 px.

**O cartão de indicadores** segue o do caso de refatoração, com fundo branco por bloco, raio 15,
sombra e brilho leves, barra de destaque de 4 px em `#1D5A8C` à esquerda, e os mesmos respiros
(margem externa de 4 px, preenchimento personalizado de 4, 4, 8 e 4 px, espaçamento vertical zero,
margem da referência de 2 px). Seis blocos numa linha: `orientation` 2, `columnCount` 6, `rowCount` 1.
Cada valor e cada referência é texto pronto de uma medida `.kpi_*`.

| Bloco | Rótulo | Valor (`Data`) | Título da referência | Valor da referência | Detalhe (pílula) | Cor da pílula |
|---|---|---|---|---|---|---|
| 1 | Receita líquida | `Medidas[.kpi_receita_liquida]` | "Ano anterior:" | `Medidas[.kpi_receita_ano_anterior]` | `Medidas[.kpi_crescimento_ano_anterior]` | regra sobre `Medidas[.cor_crescimento_ano_anterior]` |
| 2 | Acumulado no ano | `Medidas[.kpi_receita_acumulada_ano]` | sem referência | | sem pílula | |
| 3 | Margem % | `Medidas[.kpi_margem_pct]` | "Ano anterior:" | `Medidas[.kpi_margem_pct_ano_anterior]` | `Medidas[.kpi_variacao_margem_pp]` | regra sobre `Medidas[.cor_variacao_margem_pp]` |
| 4 | Margem | `Medidas[.kpi_margem]` | "Custo:" | `Medidas[.kpi_custo]` | sem pílula | |
| 5 | Desconto médio | `Medidas[.kpi_desconto_medio]` | "Concedido:" | `Medidas[.kpi_desconto_concedido]` | sem pílula | |
| 6 | Pedidos | `Medidas[.kpi_pedidos]` | "Ticket médio:" | `Medidas[.kpi_ticket_medio]` | sem pílula | |

A regra de cor da pílula é a do caso de refatoração: código 0 sem comparação, 1 favorável em
`#1E7A4C`, 2 desfavorável em `#B3261E`, aplicado à cor do texto e à cor de fundo do detalhe, com o
fundo a 90% de transparência. Nos dois blocos comparados, subir é favorável.

**Ordem de tabulação:** abas, pergunta, Ano, Mês, Região, cartão, gráfico mensal, tabela de regiões,
linha de produto, porte.

**Texto alternativo:** cartão, "Indicadores do período: receita líquida e margem percentual com o
valor do ano anterior e a variação, acumulado no ano, margem com o custo, desconto médio com o
desconto concedido e pedidos com o ticket médio"; gráfico, "Receita líquida por mês do ano escolhido
comparada ao mesmo mês do ano anterior"; tabela, "Receita líquida por região, com participação, ano
anterior e crescimento"; barras, "Receita líquida por linha de produto" e "Receita líquida por porte
de cliente".

## Página 2, Margem e desconto

**Pergunta de negócio:** onde o desconto está corroendo a margem, por porte de cliente, linha de
produto e região? **Decisão que apoia:** revisar a política de desconto por porte e linha.

Na tela: "Onde o desconto está corroendo a margem?". Linha de apoio: "O porte Grande recebe desconto
maior. Compare cada linha de produto dentro do mesmo porte."

| Nome | Tipo | x | y | L | A | Campos por papel | Ordenação | Título e subtítulo | Ponto de partida |
|---|---|---|---|---|---|---|---|---|---|
| `mdCartaoIndicadores` | `cardVisual`, cinco blocos numa linha | 16 | 110 | 1248 | 130 | ver a tabela do cartão | ordem das projeções | sem título | caso de refatoração, `vgCartaoIndicadores`, sem a pílula |
| `mdMatrizPorteLinha` | `pivotTable` | 16 | 250 | 828 | 270 | `Rows`: `Dim_Cliente[Porte]`; `Columns`: `Dim_Produto[Linha de Produto]`; `Values`: `Medidas[Desconto Medio (%)]` como "Desconto médio", `Medidas[Margem (%)]` como "Margem %"; totais de linha e de coluna ligados | porte crescente (Grande, Médio, Pequeno) | "Desconto médio e margem por porte e linha de produto" / "Desconto maior com margem menor aponta onde rever a política" | visual nativo do Desktop; formatação de `ctMatrizClienteTrimestre` do caso de refatoração |
| `mdBarraRegiao` | `clusteredBarChart` | 856 | 250 | 408 | 210 | `Category`: `Dim_Regiao[Regiao]`; `Y`: `Medidas[Desconto Medio (%)]`; `Tooltips`: `Medidas[Receita Bruta (R$)]`, `Medidas[Desconto Concedido (R$)]`, `Medidas[Margem (%)]` | desconto médio decrescente | "Desconto médio por região" / "Receita bruta, desconto concedido e margem na dica" | caso de refatoração, `vgBarraRegiao`, com `labels.labelDisplayUnits` 1 |
| `mdComboDescontoMes` | `lineClusteredColumnComboChart` | 16 | 530 | 828 | 150 | `Category`: `Dim_Calendario[Mes.Ano]`; `Y`: `Medidas[Desconto Medio (%)]`; `Y2`: `Medidas[Margem (%)]`, linha contínua `#3E8E8B`; `Tooltips`: `Medidas[Desconto Concedido (R$)]`, `Medidas[Custo (R$)]`, `Medidas[Margem (R$)]`, `Medidas[Margem Ano Anterior (%)]` | `Mes.Ano` crescente | "Desconto médio e margem por mês" / "Colunas: desconto médio · linha: margem % no eixo da direita · a caixa Mês não filtra" | caso de refatoração, `vgLinhaReceitaMes`; visual nativo do Desktop para o eixo secundário |
| `mdTabelaProdutos` | `tableEx` | 856 | 470 | 408 | 210 | `Values`: `Dim_Produto[Produto]` como "Produto", `Medidas[Desconto Concedido (R$)]` como "Desconto concedido" com barra de dados `#C9D8E8`, `Medidas[Desconto Medio (%)]` como "Desconto médio", `Medidas[Margem (%)]` como "Margem %"; filtro Top 20 por `Medidas[Desconto Concedido (R$)]`, travado e oculto; total desligado | desconto concedido decrescente | "20 produtos com mais desconto concedido" / "No filtro atual, do maior para o menor" | caso de refatoração, `vgTabelaTop20Produtos`; visual nativo do Desktop |

Larguras de coluna: matriz com cabeçalho de linha de 80 px e 86 px por coluna de valor, para os três portes e o total caberem sem rolagem; tabela de
produtos com 120, 120, 70 e 70 px.

| Bloco | Rótulo | Valor (`Data`) | Título da referência | Valor da referência |
|---|---|---|---|---|
| 1 | Receita bruta | `Medidas[.kpi_receita_bruta]` | sem referência | |
| 2 | Desconto concedido | `Medidas[.kpi_desconto_concedido]` | "Desconto médio:" | `Medidas[.kpi_desconto_medio]` |
| 3 | Receita líquida | `Medidas[.kpi_receita_liquida]` | sem referência | |
| 4 | Custo | `Medidas[.kpi_custo]` | sem referência | |
| 5 | Margem | `Medidas[.kpi_margem]` | "Margem %:" | `Medidas[.kpi_margem_pct]` |

Os cinco blocos seguem a ordem da conta, da receita bruta à margem, para quem lê ver de onde o
desconto sai antes de olhar a matriz. `columnCount` 5.

**Ordem de tabulação:** abas, pergunta, Ano, Mês, Região, cartão, matriz, região, gráfico mensal,
produtos.

**Texto alternativo:** cartão, "Da receita bruta à margem no período: receita bruta, desconto
concedido com o desconto médio, receita líquida, custo e margem com a margem percentual"; matriz,
"Desconto médio e margem percentual por porte de cliente e linha de produto"; barras, "Desconto médio
por região"; gráfico, "Desconto médio e margem percentual por mês"; tabela, "Os 20 produtos com mais
desconto concedido no filtro atual".

## Página 3, Clientes

**Pergunta de negócio:** a base de clientes está ativa ou esfriando, e onde? **Decisão que apoia:**
montar a lista de reativação por região e porte. Consultada toda semana.

Na tela: "A base de clientes está ativa ou esfriando, e onde?". Linha de apoio: "Sem compra há 90
dias: comprou nos últimos 12 meses e parou. A lista segue a caixa Região."

| Nome | Tipo | x | y | L | A | Campos por papel | Ordenação | Título e subtítulo | Ponto de partida |
|---|---|---|---|---|---|---|---|---|---|
| `clCartaoIndicadores` | `cardVisual`, quatro blocos numa linha | 16 | 110 | 828 | 130 | ver a tabela do cartão | ordem das projeções | sem título | caso de refatoração, `vgCartaoIndicadores`, sem a pílula |
| `clComboClientesMes` | `lineClusteredColumnComboChart` | 16 | 250 | 828 | 160 | `Category`: `Dim_Calendario[Mes.Ano]`; `Y`: `Medidas[Clientes Ativos]`; `Y2`: `Medidas[Clientes sem Compra 90 Dias (%)]`, linha contínua `#C27C3A`; `Tooltips`: `Medidas[Base de Clientes 12 Meses]`, `Medidas[Clientes sem Compra 90 Dias]` | `Mes.Ano` crescente | "Clientes ativos e clientes sem compra há 90 dias, por mês" / "Colunas: clientes com compra no mês · linha: % da base de 12 meses sem compra · a caixa Mês não filtra" | caso de refatoração, `vgLinhaReceitaMes`; visual nativo do Desktop |
| `clMatrizRegiaoPorte` | `pivotTable` | 16 | 420 | 828 | 260 | `Rows`: `Dim_Regiao[Regiao]`; `Columns`: `Dim_Cliente[Porte]`; `Values`: `Medidas[Clientes sem Compra 90 Dias]` como "Sem compra", `Medidas[Clientes sem Compra 90 Dias (%)]` como "% da base"; totais ligados | clientes sem compra decrescente | "Clientes sem compra há 90 dias, por região e porte" / "Quantidade e fatia da base de 12 meses" | visual nativo do Desktop; formatação de `ctMatrizClienteTrimestre` do caso de refatoração |
| `clTabelaReativacao` | `tableEx` | 856 | 110 | 408 | 570 | `Values`: `Dim_Cliente[Cliente]` como "Cliente", `Dim_Cliente[Porte]` como "Porte", `Dim_Cliente[Cidade]` como "Cidade"; filtro de visual `Medidas[Clientes sem Compra 90 Dias]` é 1, travado e oculto; total desligado | porte crescente, depois cliente crescente | "Lista de reativação" / "Compraram nos últimos 12 meses e não nos últimos 90 · vazia quando ninguém parou" | caso de refatoração, `vgTabelaTop20Produtos` (tabela); filtro de visual sobre medida de visual nativo do Desktop |

Larguras de coluna: matriz com cabeçalho de linha de 104 px e 87 px por coluna de valor; lista com
190, 70 e 120 px.

| Bloco | Rótulo | Valor (`Data`) | Título da referência | Valor da referência |
|---|---|---|---|---|
| 1 | Clientes ativos | `Medidas[.kpi_clientes_ativos]` | sem referência | |
| 2 | Base de 12 meses | `Medidas[.kpi_base_clientes_12m]` | sem referência | |
| 3 | Sem compra há 90 dias | `Medidas[.kpi_clientes_sem_compra_90d]` | "Da base de 12 meses:" | `Medidas[.kpi_clientes_sem_compra_90d_pct]` |
| 4 | Ticket médio | `Medidas[.kpi_ticket_medio]` | "Pedidos:" | `Medidas[.kpi_pedidos]` |

`columnCount` 4.

**A lista de reativação** só projeta colunas de `Dim_Cliente`, sem medida, e é o filtro de visual
sobre `Clientes sem Compra 90 Dias` que escolhe as linhas. Com uma medida projetada, o cliente parado
teria valor vazio no período escolhido e sumiria da lista, e com um mês escolhido a lista ficaria
vazia. A região vem da caixa Região do cabeçalho, que a medida respeita: o gerente escolhe a região
e exporta. A referência da medida é o fim do período escolhido, então a lista da semana sai com o
ano corrente escolhido e o mês em branco, ou com o mês corrente.

**Ordem de tabulação:** abas, pergunta, Ano, Mês, Região, cartão, gráfico mensal, matriz, lista.

**Texto alternativo:** cartão, "Clientes ativos no período, base de 12 meses, clientes sem compra há
90 dias com a fatia da base, e ticket médio com pedidos"; gráfico, "Clientes ativos por mês e
percentual da base de 12 meses sem compra há 90 dias"; matriz, "Clientes sem compra há 90 dias por
região e porte, em quantidade e percentual da base"; lista, "Clientes sem compra há 90 dias, com
porte e cidade, para reativação".

## Página 4, Vendedores

**Pergunta de negócio:** quais vendedores vendem com margem saudável e quais compram volume com
desconto? **Decisão que apoia:** acompanhamento individual e meta de margem.

Na tela: "Quem vende com margem saudável e quem compra volume com desconto?". Linha de apoio:
"Clique num vendedor na tabela para filtrar a página inteira."

| Nome | Tipo | x | y | L | A | Campos por papel | Ordenação | Título e subtítulo | Ponto de partida |
|---|---|---|---|---|---|---|---|---|---|
| `vdTabelaVendedores` | `tableEx` | 16 | 110 | 828 | 360 | `Values`: `Dim_Vendedor[Vendedor]` como "Vendedor", `Medidas[Receita Liquida (R$)]` com barra de dados `#C9D8E8`, `Medidas[Quantidade (un)]` como "Unidades", `Medidas[Desconto Medio (%)]` como "Desconto médio", `Medidas[Margem (%)]` como "Margem %", `Medidas[Variacao Margem sobre Ano Anterior (p.p.)]` como "Margem vs ano ant.", `Medidas[Clientes Ativos]` como "Clientes", `Medidas[Ticket Medio (R$)]` como "Ticket médio"; total ligado | receita líquida decrescente | "Vendedores por receita líquida" / "Clique numa linha para ver só o vendedor · variação da margem em pontos percentuais" | caso de refatoração, `vgTabelaTop20Produtos`, sem o filtro Top 20; visual nativo do Desktop |
| `vdMatrizDescontoPorte` | `pivotTable` | 856 | 110 | 408 | 360 | `Rows`: `Dim_Vendedor[Vendedor]`; `Columns`: `Dim_Cliente[Porte]`; `Values`: `Medidas[Desconto Medio (%)]`; total de linha e de coluna ligados | total de desconto médio decrescente | "Desconto médio por porte de cliente" / "Compare dentro da mesma coluna: o Grande tem desconto maior por política" | visual nativo do Desktop; formatação de `cvMatrizVendedorMes` do caso de refatoração |
| `vdComboVendedorMes` | `lineClusteredColumnComboChart` | 16 | 480 | 828 | 200 | `Category`: `Dim_Calendario[Mes.Ano]`; `Y`: `Medidas[Receita Liquida (R$)]`; `Y2`: `Medidas[Margem (%)]`, linha contínua `#3E8E8B`, e `Medidas[Desconto Medio (%)]`, linha contínua `#C27C3A`; `Tooltips`: `Medidas[Variacao Margem sobre Ano Anterior (p.p.)]` | `Mes.Ano` crescente | "Receita, margem e desconto por mês" / "Todos os vendedores, ou o vendedor clicado na tabela · a caixa Mês não filtra" | caso de refatoração, `vgLinhaReceitaMes`; visual nativo do Desktop |
| `vdBarraMenorMargem` | `clusteredBarChart` | 856 | 480 | 408 | 200 | `Category`: `Dim_Vendedor[Vendedor]`; `Y`: `Medidas[Margem (%)]`; `Tooltips`: `Medidas[Desconto Medio (%)]`, `Medidas[Receita Liquida (R$)]` | margem % crescente | "Vendedores da menor para a maior margem" / "Role para ver os demais · desconto e receita na dica" | caso de refatoração, `vgBarraRegiao`, com `labels.labelDisplayUnits` 1 |

Larguras de coluna: tabela de vendedores com 146, 150, 76, 80, 70, 92, 70 e 104 px; matriz com
cabeçalho de linha de 120 px e 60 px por coluna, para a coluna Total caber. A participação na receita
saiu da tabela de vendedores para o ticket médio caber inteiro, e continua coberta na tabela de
regiões da Visão executiva.

A barra da menor margem mostra todos os vendedores em ordem crescente e rola, em vez de um filtro dos
10 menores, porque o filtro de ordem crescente não tem estrutura conferida no Desktop, e a rolagem tem
barra visível. O clique na tabela usa a interação padrão de filtro do Power BI, sem configuração.

**Ordem de tabulação:** abas, pergunta, Ano, Mês, Região, tabela, matriz, gráfico mensal, barras.

**Texto alternativo:** tabela, "Vendedores por receita líquida, com unidades, desconto
médio, margem percentual, variação da margem sobre o ano anterior, clientes e ticket médio"; matriz,
"Desconto médio de cada vendedor por porte de cliente"; gráfico, "Receita líquida, margem percentual e
desconto médio por mês"; barras, "Margem percentual por vendedor, da menor para a maior".

## Medidas de exibição que o desenho pede ao modelo

Ocultas, na pasta `.Internas\UI`, fora da paridade e do levantamento. Cada uma lê a medida de
negócio e devolve texto com `FORMAT ( valor, "<máscara>", "pt-BR" )` (lições L47 e L48), guarda o
vazio com `IF ( NOT ISBLANK ( v ), ... )` para o cartão desenhar o hífen, e não muda o formato da
medida de negócio, que continua fixo para tabela, gráfico e exportação.

**Faixa dos reais**, usada onde a máscara diz "faixa": prefixo "R$ " com o sinal à frente quando
negativo, e sobre o valor absoluto `v`, `v >= 999500000` escreve `FORMAT ( v / 1000000000, "#,0.0" )
& " Bi"`, `v >= 99950000` escreve `FORMAT ( v / 1000000, "#,0" ) & " Mi"`, `v >= 999950` escreve
`FORMAT ( v / 1000000, "#,0.0" ) & " Mi"`, e abaixo disso `FORMAT ( v, "#,0" )`. É a mesma regra
das `.kpi_*` do caso de refatoração.

**Guarda de um ano**, usada nas medidas marcadas: a medida só devolve valor com
`HASONEVALUE ( Dim_Calendario[Ano] )`, e fora disso devolve `BLANK ()`.

| # | Medida | Lê | Máscara | Guarda de um ano | Exemplo | Onde |
|---|---|---|---|---|---|---|
| 1 | `.kpi_receita_liquida` | `[Receita Liquida (R$)]` | faixa | não | R$ 65,1 Mi | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 2 | `.kpi_receita_ano_anterior` | `[Receita Ano Anterior (R$)]` | faixa | sim | R$ 63,4 Mi | `veCartaoIndicadores` |
| 3 | `.kpi_crescimento_ano_anterior` | `[Crescimento sobre Ano Anterior (%)]` | `UNICHAR ( 9650 )` ou `UNICHAR ( 9660 )` & " " & `FORMAT ( v, "+0.0%;-0.0%;0.0%" )` | sim | ▲ +2,7% | `veCartaoIndicadores`, pílula |
| 4 | `.kpi_receita_acumulada_ano` | `[Receita Acumulada no Ano (R$)]` | faixa | não | R$ 464 Mi | `veCartaoIndicadores` |
| 5 | `.kpi_margem_pct` | `[Margem (%)]` | `"0.0%"` | não | 40,8% | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 6 | `.kpi_margem_pct_ano_anterior` | `[Margem Ano Anterior (%)]` | `"0.0%"` | sim | 40,8% | `veCartaoIndicadores` |
| 7 | `.kpi_variacao_margem_pp` | `[Variacao Margem sobre Ano Anterior (p.p.)]` | seta como no item 3 & " " & `FORMAT ( v, "+0.0;-0.0;0.0" ) & " p.p."` | sim | ▲ +0,4 p.p. | `veCartaoIndicadores`, pílula |
| 8 | `.kpi_margem` | `[Margem (R$)]` | faixa | não | R$ 26,6 Mi | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 9 | `.kpi_custo` | `[Custo (R$)]` | faixa | não | R$ 38,6 Mi | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 10 | `.kpi_desconto_medio` | `[Desconto Medio (%)]` | `"0.0%"` | não | 6,5% | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 11 | `.kpi_desconto_concedido` | `[Desconto Concedido (R$)]` | faixa | não | R$ 4,5 Mi | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 12 | `.kpi_receita_bruta` | `[Receita Bruta (R$)]` | faixa | não | R$ 69,6 Mi | `mdCartaoIndicadores` |
| 13 | `.kpi_pedidos` | `[Pedidos]` | `"#,0"` | não | 7.668 | `veCartaoIndicadores`, `clCartaoIndicadores` |
| 14 | `.kpi_ticket_medio` | `[Ticket Medio (R$)]` | `"R$ " & FORMAT ( v, "#,0" )`, com o sinal à frente quando negativo | não | R$ 8.491 | `veCartaoIndicadores`, `clCartaoIndicadores` |
| 15 | `.kpi_clientes_ativos` | `[Clientes Ativos]` | `"#,0"` | não | 6.412 | `clCartaoIndicadores` |
| 16 | `.kpi_base_clientes_12m` | `[Base de Clientes 12 Meses]` | `"#,0"` | não | 19.776 | `clCartaoIndicadores` |
| 17 | `.kpi_clientes_sem_compra_90d` | `[Clientes sem Compra 90 Dias]` | `"#,0"` | não | 6.346 | `clCartaoIndicadores` |
| 18 | `.kpi_clientes_sem_compra_90d_pct` | `[Clientes sem Compra 90 Dias (%)]` | `"0.0%"` | não | 32,1% | `clCartaoIndicadores` |

No item 3 e no item 7, a seta é `UNICHAR ( 9650 )` quando `v > 0`, `UNICHAR ( 9660 )` quando `v < 0`
e nenhuma quando `v = 0`.

Além das dezoito de texto, o desenho pede duas medidas numéricas de código de cor, na mesma pasta,
no padrão `.cor_var_*` do caso de refatoração: `.cor_crescimento_ano_anterior` e
`.cor_variacao_margem_pp`, que devolvem 0 sem comparação (inclusive fora da guarda de um ano), 1
quando a medida de negócio é maior que zero e 2 quando é menor. E pede `.rodape_pagina`, com o texto
do rodapé.

## O que mais o desenho pede ao modelo

| Item | Onde | Por quê |
|---|---|---|
| calendário terminando na última data da base (31-08-2026 hoje) | `fn_Calendario`, janela do `_manifesto.json` | com o calendário até 31-12, o ano de 2026 compararia oito meses com doze, e as medidas de clientes tomariam 31-12 como referência e marcariam todo cliente como parado |
| `Dim_Calendario[Nome do Mes]` ordenado por `Mes`, `Dim_Calendario[Mes.Ano]` ordenado por `Ordem` | `Dim_Calendario` | caixa de mês em ordem de calendário e eixo mensal em ordem cronológica |
| `Dim_Cliente[Cidade]` visível | `Dim_Cliente` | coluna da lista de reativação |
| porte gravado com acento ("Médio") | base e `Dim_Cliente[Porte]` | rótulo de matriz, barra e lista |
| formato fixo nas medidas de negócio, como no catálogo | `Medidas` | tabela, dica e exportação mostram o valor completo; só o cartão recebe texto |

## O que o desenho pede ao relatório, fora dos visuais

O tema `BBComercial.json` registrado como tema personalizado, os três grupos de sincronização das
caixas, os três filtros de relatório com nome de negócio, o filtro Top 20 da tabela de produtos e o
filtro de medida da lista de reativação travados e ocultos, as quatro entradas `NoFilter` da caixa
Mês nos gráficos mensais, e o painel de filtros recolhido ao salvar.

## Contagem por página

| Página | Visuais de conteúdo | Chassi | Elementos na página |
|---|---|---|---|
| Visão executiva | 5 | 9 (grupo, faixa, logotipo, pergunta, navegador, três caixas, rodapé) | 14 |
| Margem e desconto | 5 | 9 | 14 |
| Clientes | 4 | 9 | 13 |
| Vendedores | 4 | 9 | 13 |

## Cobertura dos 20 indicadores

Cada indicador do catálogo aparece pelo nome da medida de negócio em pelo menos um visual, e alguns
aparecem também como texto de cartão, por uma medida `.kpi_*`.

| # | Indicador | Medida | Visual onde aparece a medida | Também no cartão |
|---|---|---|---|---|
| 1 | Receita bruta | `Receita Bruta (R$)` | `mdBarraRegiao` (dica) | `mdCartaoIndicadores` |
| 2 | Receita líquida | `Receita Liquida (R$)` | `veComboReceitaMes`, `veTabelaRegiao`, `veBarraLinha`, `veBarraPorte`, `vdTabelaVendedores`, `vdComboVendedorMes`, `vdBarraMenorMargem` (dica) | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 3 | Participação na receita | `Participacao na Receita (%)` | `veTabelaRegiao`, `veBarraLinha` (dica), `veBarraPorte` (dica) | |
| 4 | Desconto concedido | `Desconto Concedido (R$)` | `mdTabelaProdutos`, `mdBarraRegiao` (dica), `mdComboDescontoMes` (dica) | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 5 | Desconto médio | `Desconto Medio (%)` | `mdMatrizPorteLinha`, `mdBarraRegiao`, `mdComboDescontoMes`, `mdTabelaProdutos`, `vdTabelaVendedores`, `vdMatrizDescontoPorte`, `vdComboVendedorMes` | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 6 | Custo | `Custo (R$)` | `mdComboDescontoMes` (dica) | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 7 | Margem | `Margem (R$)` | `mdComboDescontoMes` (dica) | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 8 | Margem % | `Margem (%)` | `mdMatrizPorteLinha`, `mdComboDescontoMes`, `mdBarraRegiao` (dica), `mdTabelaProdutos`, `vdTabelaVendedores`, `vdComboVendedorMes`, `vdBarraMenorMargem` | `veCartaoIndicadores`, `mdCartaoIndicadores` |
| 9 | Pedidos | `Pedidos` | `veComboReceitaMes` (dica) | `veCartaoIndicadores`, `clCartaoIndicadores` |
| 10 | Quantidade | `Quantidade (un)` | `vdTabelaVendedores` | |
| 11 | Ticket médio | `Ticket Medio (R$)` | `vdTabelaVendedores` | `veCartaoIndicadores`, `clCartaoIndicadores` |
| 12 | Clientes ativos | `Clientes Ativos` | `clComboClientesMes`, `vdTabelaVendedores` | `clCartaoIndicadores` |
| 13 | Base de clientes 12 meses | `Base de Clientes 12 Meses` | `clComboClientesMes` (dica) | `clCartaoIndicadores` |
| 14 | Clientes sem compra 90 dias | `Clientes sem Compra 90 Dias` | `clMatrizRegiaoPorte`, `clComboClientesMes` (dica), `clTabelaReativacao` (filtro de visual) | `clCartaoIndicadores` |
| 15 | Clientes sem compra 90 dias % | `Clientes sem Compra 90 Dias (%)` | `clComboClientesMes`, `clMatrizRegiaoPorte` | `clCartaoIndicadores` |
| 16 | Receita do ano anterior | `Receita Ano Anterior (R$)` | `veComboReceitaMes`, `veTabelaRegiao` | `veCartaoIndicadores` |
| 17 | Crescimento sobre o ano anterior | `Crescimento sobre Ano Anterior (%)` | `veTabelaRegiao`, `veComboReceitaMes` (dica), `veBarraLinha` (dica), `veBarraPorte` (dica) | `veCartaoIndicadores` |
| 18 | Margem % do ano anterior | `Margem Ano Anterior (%)` | `mdComboDescontoMes` (dica) | `veCartaoIndicadores` |
| 19 | Variação da margem sobre o ano anterior | `Variacao Margem sobre Ano Anterior (p.p.)` | `vdTabelaVendedores`, `vdComboVendedorMes` (dica) | `veCartaoIndicadores` |
| 20 | Receita acumulada no ano | `Receita Acumulada no Ano (R$)` | `veComboReceitaMes` (dica) | `veCartaoIndicadores` |
