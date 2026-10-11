# Sistema visual do painel reestruturado (v2)

Escrito em 27-09-2026, depois da refatoração e antes do redesenho visual da v2, e refeito em
10-10-2026, quando o painel foi reconstruído no padrão de desenvolvimento da B&B. É o acabamento
visual de um entregável que roda na máquina de quem abre, sem nada hospedado. O layout página a
página está em [`LAYOUT.md`](LAYOUT.md).

A régua deste documento é o padrão de desenvolvimento de painel da B&B. Onde o padrão fixa papel e
proporção, este documento fixa o valor de cor e de fonte deste painel.

## Conceito

O painel é lido como um relatório de diretoria: fundo cinza muito claro, uma faixa de cabeçalho clara
de 100 pontos com o logotipo, a pergunta da página, as abas e os filtros, e o conteúdo em blocos
brancos com borda de raio 5 e sombra leve, sem a barra de ícones do visual. Uma única cor de destaque,
o azul petróleo, fica reservada para o dado que importa. A leitura desce numa ordem fixa, com a
pergunta no topo, os indicadores numa faixa só, a tendência mensal, a composição e por fim o detalhe,
e essa ordem se repete em todas as páginas. Cor só carrega significado (destaque, comparação, bom e
ruim), e nenhuma informação depende só dela, porque todo valor também aparece escrito e toda variação
leva seta.

## Paleta

### Neutros

| Papel | Hex | Onde aparece | Contraste |
|---|---|---|---|
| Tinta principal | `#1B2430` | texto principal, valor de bloco, célula de tabela | 15,7:1 sobre branco |
| Tinta da marca | `#16263D` | logotipo, pergunta da página, aba atual | 13,0:1 sobre a faixa |
| Tinta secundária | `#3D4756` | rótulo de dado, cabeçalho de tabela, linha de apoio, aba não selecionada | 9,4:1 sobre branco |
| Tinta suave | `#5F6B7A` | subtítulo, eixo, legenda, rodapé | 5,1:1 sobre branco e 4,6:1 sobre o fundo da página |
| Borda de visual | `#DDE2E8` | contorno dos blocos | decorativo |
| Sombra de bloco | `#C9D0D9` | sombra dos blocos de dado, abaixo e à direita | decorativo |
| Grade | `#EDF0F3` | linha de grade de gráfico, linha entre linhas de tabela | decorativo |
| Fundo da página | `#F3F5F8` | tela, aba da página atual, cartão de filtro disponível, linha de total | |
| Superfície | `#FFFFFF` | fundo de todo visual | |
| Faixa do cabeçalho | `#E8EEF5` | faixa de 100 pontos no alto da página | |
| Aba não selecionada | `#C9D8E6` | abas das outras páginas | o texto `#3D4756` fica com 6,5:1 |
| Fundo externo | `#E9ECF0` | área fora da tela no Desktop | |

### Destaque e comparação

| Papel | Hex | Onde aparece | Contraste |
|---|---|---|---|
| Destaque | `#1D5A8C` | série principal, barras, barra de destaque dos blocos de indicador, contorno de filtro aplicado | 7,3:1 sobre branco, vale também como texto |
| Destaque claro | `#C9D8E8` | barra de dados dentro de tabela, brilho dos blocos de indicador | o texto por cima fica com 10,9:1 |
| Comparação | `#7D8796` | linha do ano anterior, sempre tracejada | 3,6:1 sobre branco |
| Escala sequencial | `#FFFFFF` até `#9DBAD8` | reservada para mapa de calor | o texto na célula mais escura fica com 7,8:1 |

### Semânticas

| Papel | Hex | Uso | Contraste |
|---|---|---|---|
| Bom | `#1E7A4C` | variação favorável na pílula do cartão, sempre com seta | 5,3:1 |
| Ruim | `#B3261E` | variação desfavorável na pílula do cartão, sempre com seta | 6,5:1 |
| Atenção | `#9A6700` | reservada; nenhum visual deste painel usa limite de alerta, porque não existe regra de negócio escrita para isso | 4,9:1 |

A seta faz o trabalho da cor: `▲ 5,6%` e `▼ -2,1%` continuam legíveis para quem não distingue verde
de vermelho. Na pílula, o fundo leva a mesma cor do texto com 90% de transparência, o que dá o tom
claro atrás da variação.

### Sequência de categorias

Usada só quando um visual precisar de mais de uma série. Hoje só o gráfico mensal usa duas, e ele
pega as duas primeiras. Barras de uma série ficam todas na cor de destaque, sem arco-íris.

| Ordem | Hex | Contraste sobre branco |
|---|---|---|
| 1 | `#1D5A8C` | 7,3:1 |
| 2 | `#7D8796` | 3,6:1 |
| 3 | `#3E8E8B` | 3,9:1 |
| 4 | `#C27C3A` | 3,4:1 |
| 5 | `#6D5E99` | 5,7:1 |
| 6 | `#5B8DB8` | 3,5:1 |
| 7 | `#7A8835` | 3,9:1 |
| 8 | `#A86D8C` | 4,0:1 |

Todas passam de 3:1 contra o branco, que é o piso para objeto gráfico.

## Tipografia

Uma família só, Segoe UI, que o Power BI Desktop oferece nativo e que existe em toda máquina
Windows. A hierarquia vem de peso e tamanho: Black só no logotipo, Semibold em título, pergunta,
aba, cabeçalho e no rótulo e no valor dos indicadores, e Regular no corpo. O Power BI mede fonte em pontos.

| Papel | Fonte | Tamanho | Cor |
|---|---|---|---|
| Logotipo na faixa ("B&B") | Segoe UI Black | 20 pt | `#16263D` |
| Pergunta da página | Segoe UI Semibold | 13 pt | `#16263D` |
| Linha de apoio da página | Segoe UI | 9 pt | `#3D4756` |
| Aba de navegação | Segoe UI Semibold | 9 pt | `#3D4756`, atual em `#16263D` |
| Cabeçalho da segmentação | Segoe UI Semibold | 10 pt | `#1B2430` |
| Item da segmentação | Segoe UI | 8 pt | `#1B2430` |
| Título de visual | Segoe UI Semibold | 12 pt | `#1B2430` |
| Subtítulo de visual | Segoe UI | 8 pt | `#5F6B7A` |
| Rótulo do bloco de indicador | Segoe UI Semibold | 8 pt | cor de texto do tema |
| Valor do bloco de indicador | Segoe UI Semibold | 14 pt | `#1B2430` |
| Referência e pílula do bloco | Segoe UI | 9 pt | título e valor na cor do tema; pílula na cor semântica |
| Eixo e legenda | Segoe UI | 8 pt | `#5F6B7A` |
| Rótulo de dado | Segoe UI | 8 pt | `#3D4756` |
| Cabeçalho de tabela | Segoe UI Semibold | 8 pt | `#3D4756` |
| Célula de tabela | Segoe UI | 9 pt | `#1B2430` |
| Total de tabela | Segoe UI Semibold | 9 pt | `#1B2430` |
| Rodapé | Segoe UI Semibold | 8 pt | `#5F6B7A` |

Nenhum texto do painel fica abaixo de 8 pt.

## Grade e espaçamento

A página tem 1280 x 720, com margem lateral de 16 px no conteúdo e calha de 12 px entre blocos
lado a lado.

| Faixa | y | Altura | O que ocupa |
|---|---|---|---|
| Cabeçalho | 0 | 100 | logotipo, pergunta e linha de apoio, abas, segmentações de ano, mês e região |
| Faixa de indicadores (só na Visão geral) | 110 | 150 | cartão de indicadores, largura total |
| Conteúdo | 108, ou 266 na Visão geral | até y 680 | visuais |
| Rodapé | 680 | 40 | janela da base, unidade, recorte e assinatura, centralizados |

Dentro do cabeçalho, o logotipo ocupa x 20 a 104, a pergunta e as abas ocupam x 116 a 736, e as
segmentações ocupam x 820 a 1260, com 70 px de altura cada. As abas ficam encostadas na base da
faixa, de y 70 a 100, para a aba da página atual, na cor da página, parecer recortada na faixa.

Na Visão geral, o cartão de indicadores vai de y 110 a 260, logo abaixo das abas, e as duas linhas
de gráfico ficam em y 266 a 469 e 479 a 680. A linha de baixo perdeu 16 px de altura em 10-10-2026,
e em 11-10-2026 o cartão ganhou mais 20 px para a pílula da variação caber inteira, tirados 12 px da
linha do meio e 8 da de baixo, sem empurrar o rodapé para fora da página. Larguras que se
repetem: 1248 px na largura toda, 828 e 408 px na linha de cima e 303, 303 e 618 px na de baixo.

## Regras de título

Título diz o que o número é, na língua de quem decide, e nunca a agregação técnica. O subtítulo
diz o recorte ou como ler, quando isso não for óbvio. Nome técnico do modelo não aparece em lugar
nenhum: a medida `Receita Liquida (R$)` aparece como "Receita Líquida", e a coluna `Dim_Regiao[Regiao]`
como "Região", pelo nome de exibição de cada projeção.

| Na v1 | Na v2 |
|---|---|
| Soma de receita_liquida e Receita Ano Anterior por Mês Ano | Receita líquida por mês |
| Soma de receita_liquida por regiao | Receita líquida por região |
| Soma de receita_liquida por porte | Receita líquida por porte de cliente |
| Contagem distinta de numero_pedido | Pedidos |
| Soma de quantidade | Quantidade |
| Soma de Lucro | Margem |

As regras, em resumo: sem "Soma de", "Contagem de" nem nome de coluna; sem ponto final; primeira
letra maiúscula e o resto em minúscula, com exceção de nome próprio como Linha Premium; unidade e
recorte no subtítulo e nunca entre parênteses no título; e toda página abre com uma pergunta de
negócio escrita por extenso.

## Formato de número

O formato mora na medida, igual em todo visual. A exceção é o cartão de indicadores, que recebe
texto pronto: o valor e a referência de cada bloco vêm de medidas de exibição `.kpi_*` que escrevem o
número com `FORMAT` na cultura pt-BR, como as medidas da pílula. O cartão novo formata a referência
fora da localização do modelo, com ponto decimal ("Participação: 66.7%", "Mês anterior: 39.9%"), mesmo
quando a medida tem formato fixo, e o formato dinâmico com escala de milhão seguida de texto,
`#,0,, \M\i`, não abreviou no valor e saiu cheio, cortado em "R$ 952.94...". Com texto, o cartão
só desenha o que recebe. A unidade de exibição continua "Nenhum" (`labelDisplayUnits` e
`valueDisplayUnits` em 1), e o vazio continua vazio, desenhado como hífen.

| Onde | Formato | Exemplo de tela, nas bases de 1 e de 5 milhões |
|---|---|---|
| Valor do bloco, receita, margem e Linha Premium | texto por faixa: uma casa em bilhão, nenhuma de cem milhões para cima, uma casa em milhão, cheio e sem centavos abaixo disso; cada corte fica meio passo abaixo da fronteira, para o arredondamento não escrever "1.000 Mi" | R$ 10,6 Bi; R$ 953 Mi; R$ 24,8 Mi; R$ 339.930 |
| Valor do bloco, quantidade | uma casa em milhão, cheio abaixo disso | 37,6 Mi; 1.237 |
| Valor do bloco, ticket médio | reais cheios, sem centavos | R$ 8.513 |
| Valor do bloco, pedidos e clientes com compra | inteiro cheio, com milhar | 274.142; 20.000 |
| Valor do bloco, margem % | percentual com uma casa | 40,8% |
| Referência "Mês anterior" | o mesmo formato do valor do bloco, também em texto pt-BR | R$ 376.101; 1.307; R$ 11.753; 39,9% |
| Variação na pílula | seta, sinal no negativo e uma casa; a da margem % em pontos percentuais | ▲ 5,2%; ▼ -1,3 p.p. |
| Participação no bloco da Linha Premium | percentual, uma casa, em texto pt-BR | 66,7% |
| Variação sobre o ano anterior, na dica | seta, sinal e uma casa | ▲ +55,1% |
| Rótulo de barra e coluna | R$ em milhões, uma casa | R$ 718,7 Mi |
| Eixo de valor do gráfico mensal | unidade e casas automáticas do Power BI, que acompanham a escala do filtro | R$ 400 Mi; R$ 300 Mil |
| Tabela, valor | R$ completo com centavos | R$ 813.161,91 |
| Percentual em tabela | uma casa, como a medida | 33,9% |
| Data | dd/mm/aaaa | 01/09/2023 |
| Pedido | máscara do modelo | PV-000000001 |
| Valor vazio | hífen | - |

O sufixo da unidade nos eixos e rótulos vem da localização pt-BR do Power BI, que escreve Mil, Mi e
Bi, e o do cartão vem do texto das medidas `.kpi_*`, escrito com os mesmos Mi e Bi. Tabela e dica
de ferramenta mostram o valor completo, e é por elas que o número exato continua ao alcance quando o
cartão arredonda. Os exemplos do mês anterior são ilustrativos e saem da
base conforme o mês escolhido.

## O cartão de indicadores

O cartão segue a faixa de KPIs do padrão e foi montado a partir de um cartão de referência gravado
pelo Desktop. Cada bloco tem:

- fundo branco, contorno fino, retângulo arredondado de raio 15, sombra e brilho leves e a barra de
  destaque à esquerda em `#1D5A8C`, com 4 px;
- o rótulo em cima, em Segoe UI Semibold 8;
- o valor em 14 pt, o texto pronto da medida de exibição `.kpi_*`;
- o rótulo de referência no estilo frase, com o título "Mês anterior:" e o valor do mês anterior em
  9 pt, os dois em texto pronto, e no bloco da Linha Premium o título "Participação:" com a fatia
  da receita;
- o detalhe, que é a pílula da variação, com cor por regra condicional sobre o código da medida
  `.cor_var_*` e fundo com 90% de transparência.

Os oito blocos ficam numa linha (`orientation` 2, `columnCount` 8 e `rowCount` 1, a forma que o
Desktop gravou), porque o tema base limita a três blocos por linha quando nada é dito. A comparação só
aparece com um único mês no contexto; sem isso a referência mostra hífen e a pílula some.

**Altura útil do bloco.** O tema base do Desktop dá ao cartão novo 12 px de margem externa e 12 px de
preenchimento por bloco, e isso, somado ao rótulo, ao valor e à referência em duas linhas, cortava o
rótulo no topo e a última linha embaixo. Desde 10-10-2026 o cartão declara os respiros: margem
externa de 4 px (`layout.paddingUniform`), preenchimento do bloco personalizado com 4 px em cima e
embaixo, 8 à esquerda por causa da barra de destaque e 4 à direita (`padding` com `paddingSelection`
`Custom` e `paddingIndividual` ligado, porque o tema traz `paddingIndividual` desligado e, sem ele, a
escolha personalizada é ignorada), espaçamento vertical zero e margem da referência de 2 px.

Na tela, a referência ocupa três linhas por bloco, e não duas: "Mês anterior:", o valor do mês
anterior e a pílula. Com 130 px de cartão, o bloco desenhado tinha cerca de 88 px, porque a sombra e
o brilho de cada bloco reservam por volta de 20 px em volta dele, e com um mês escolhido a pílula
saía cortada na borda de baixo. Desde 11-10-2026 o cartão tem 150 px, o que dá ao bloco cerca de
108 px para o rótulo, o valor, as duas linhas da referência e a pílula, com folga embaixo. Os
respiros internos ficaram como estavam, porque já estavam no mínimo legível. O divisor do bloco
continua desligado, e a cor dele passou a ser `#C9D8E6`, da paleta do tema.

A estrutura do `visual.json` foi conferida objeto a objeto contra o cartão de referência. O que não
está nele são propriedades simples, todas com respaldo em cartão gravado pelo Desktop ou na definição do
visual instalada: `label.position`, `layout.orientation`, `layout.maxTiles`, `layout.paddingUniform`,
`padding.paddingIndividual` com as quatro margens, `value.showBlankAs`, e na referência
`valueDisplayUnits` e `showBlankAs`. As casas decimais forçadas (`labelPrecision` e `valuePrecision`)
saíram, porque o número de casas agora vem do texto da medida. Se algum bloco não se comportar como
previsto ao abrir, é por elas que a conferência começa.

## Segmentação e painel de filtros

Os filtros ficam em dois lugares com papéis diferentes. No cabeçalho ficam só os três que a
diretoria e o gerente regional usam o tempo todo, **ano, mês e região**, como caixas suspensas com
borda de raio 5, sincronizadas entre as quatro páginas: quem escolhe Sudeste e 2026 na Visão geral
continua em Sudeste e 2026 ao abrir o detalhe. Cada caixa tem a opção "Selecionar tudo" ligada, para
que voltar ao total não dependa do ícone de borracha que só aparece ao passar o mouse.

**Linha de produto, porte do cliente e vendedor** ficam no painel de filtros, no nível do relatório,
com nome de negócio no cartão de filtro e busca ligada no de vendedor, que tem 150 nomes. A linha de
apoio da Visão geral avisa onde eles estão. O painel abre recolhido, que é também como o protocolo
de medição pede.

Filtro que o usuário não deve mexer, como o dos 20 produtos de maior receita, fica travado e
oculto. O painel de filtros segue a paleta: fundo branco, cartão disponível em `#F3F5F8` e cartão
com filtro aplicado em `#E8F0F8` com contorno na cor de destaque, que é a pista visual de que há
filtro ativo fora da página.

## Estados de interação

| Componente | Padrão | Ao passar o mouse | Selecionado ou ativo | Foco de teclado |
|---|---|---|---|---|
| Aba de navegação | texto `#3D4756` sobre `#C9D8E6` | fundo `#B7CBDF`, texto `#16263D` | fundo `#F3F5F8`, texto `#16263D` | contorno nativo do Power BI |
| Caixa de segmentação | sem fundo, borda de raio 5 | nativo | valor escolhido escrito na caixa | contorno nativo |
| Botão Voltar | texto `#1D5A8C`, contorno `#7D8796`, fundo branco | fundo `#F3F5F8` | nativo | contorno nativo |
| Barra, coluna e ponto | cor de destaque | dica de ferramenta | realce nativo esmaece os outros | navegação por seta, nativa |
| Linha de tabela | branco | nativo | realce nativo | nativo |
| Cartão de filtro | `#F3F5F8` | nativo | `#E8F0F8` com contorno `#1D5A8C` | nativo |

## Acessibilidade, itens verificáveis

| Item | Como conferir |
|---|---|
| texto com 4,5:1 ou mais | a tabela de paleta: o texto mais fraco é `#5F6B7A`, com 4,6:1 sobre o fundo da página |
| objeto gráfico com 3:1 ou mais | a sequência de categorias e a cor de comparação, todas acima de 3:1 |
| informação que não depende só de cor | variação com seta, ano anterior tracejado, valor escrito em todo bloco |
| texto alternativo em todo visual com dado | lista no `LAYOUT.md`, preenchida em Geral, Texto alternativo |
| ordem de tabulação na ordem de leitura | lista no `LAYOUT.md` |
| nenhuma função só no passar do mouse | exportar e detalhar estão escritos na linha de apoio; o acumulado na dica também sai por Mostrar como tabela |
| tamanho mínimo de fonte | 8 pt |

## Especificação do tema JSON

O tema `BBComercial.json` fica registrado no relatório, por cima do tema base do Desktop. Os nomes de
chave seguem o esquema de tema do Power BI, e cada chave foi conferida na lista de objetos extraída do
Desktop instalado, porque o esquema aceita chave inventada sem avisar. `padding`, `spacing` e `divider` nunca vão no curinga `*`: o cartão novo tem
objetos próprios com esses nomes, e o tema genérico por cima deles apaga o cartão. Por
isso eles se repetem em cada tipo de visual e o `cardVisual` fica de fora.

### Chaves de primeiro nível

| Chave | Valor |
|---|---|
| `name` | `B&B Comercial` |
| `dataColors` | `#1D5A8C`, `#7D8796`, `#3E8E8B`, `#C27C3A`, `#6D5E99`, `#5B8DB8`, `#7A8835`, `#A86D8C` |
| `foreground` | `#1B2430` |
| `foregroundNeutralSecondary` | `#5F6B7A` |
| `foregroundNeutralTertiary` | `#8A94A3` |
| `background` | `#FFFFFF` |
| `backgroundLight` | `#F3F5F8` |
| `backgroundNeutral` | `#DDE2E8` |
| `tableAccent` | `#1D5A8C` |
| `hyperlink` e `visitedHyperlink` | `#1D5A8C` |
| `good`, `neutral`, `bad` | `#1E7A4C`, `#9A6700`, `#B3261E` |
| `minimum`, `center`, `maximum` | `#FFFFFF`, `#CBDAE9`, `#9DBAD8` |
| `null` | `#FFFFFF` |

### `visualStyles`, página

| Seletor e propriedade | Valor |
|---|---|
| `page` › `background` | cor `#F3F5F8`, transparência 0 |
| `page` › `outspace` | cor `#E9ECF0` |
| `page` › `outspacePane` | fundo `#FFFFFF`, texto `#1B2430`, borda `#DDE2E8`, fonte Segoe UI, título 11, cabeçalho 10, caixa de entrada `#FFFFFF`, caixa de seleção e botão aplicar `#1D5A8C` |
| `page` › `filterCard`, `$id` Available | fundo `#F3F5F8`, texto `#1B2430`, borda `#DDE2E8`, caixa de entrada `#FFFFFF`, Segoe UI 9 |
| `page` › `filterCard`, `$id` Applied | fundo `#E8F0F8`, texto `#1B2430`, borda `#1D5A8C`, caixa de entrada `#FFFFFF`, Segoe UI 9 |

### `visualStyles`, todos os visuais (`*`)

| Propriedade | Valor |
|---|---|
| `title` | ligado, Segoe UI Semibold 12, `#1B2430`, alinhado à esquerda, sem quebra |
| `subTitle` | ligado, Segoe UI 8, `#5F6B7A` |
| `background` | ligado, `#FFFFFF`, transparência 0 |
| `border` | ligado, `#DDE2E8`, espessura 1, raio 5 |
| `dropShadow` | ligado, `#C9D0D9`, externa, abaixo e à direita |
| `visualHeader` | desligado |
| `visualTooltip` | fundo `#FFFFFF`, título `#5F6B7A`, valor `#1B2430`, tamanho 9 |
| `categoryAxis` | Segoe UI 8, `#5F6B7A`, título do eixo desligado, grade desligada |
| `valueAxis` | Segoe UI 8, `#5F6B7A`, título do eixo desligado, grade `#EDF0F3` sólida de 1 px |
| `legend` | ligada, no alto à esquerda, Segoe UI 8, `#3D4756`, sem título |
| `labels` | Segoe UI 8, `#3D4756` |

### `visualStyles`, por tipo

| Tipo | Propriedades |
|---|---|
| `textbox` e `shape` | fundo, borda, sombra, título e cabeçalho do visual desligados; espaçamento repetido do curinga |
| `pageNavigator` | sem fundo, borda, sombra e título; abas com os cantos de cima cortados; texto Segoe UI Semibold 9, `#3D4756` sobre `#C9D8E6`; passar o mouse `#16263D` sobre `#B7CBDF`; selecionada `#16263D` sobre `#F3F5F8`; contorno desligado |
| `actionButton` | texto `#1D5A8C` Segoe UI 9, contorno `#7D8796`, fundo `#FFFFFF`, sem sombra; passar o mouse fundo `#F3F5F8` |
| `slicer` | sem fundo, sem sombra e sem título; borda de raio 5; cabeçalho Segoe UI Semibold 10 `#1B2430`; itens Segoe UI 8 `#1B2430` com contorno `#7D8796`; modo suspenso; "Selecionar tudo" ligado |
| `cardVisual` | sem entrada no tema; os dois cartões do relatório, o de indicadores e o do rodapé, são formatados no próprio visual, como no cartão de referência |
| `multiRowCard` | não é mais usado em nenhuma página; a entrada fica no tema para quem herdar o arquivo |
| `lineClusteredColumnComboChart` | espaçamento interno das colunas 38%; linha de 2 px; rótulos de dado desligados; eixo de valor com unidade automática (`labelDisplayUnits` 0) e casas automáticas, porque a unidade fixa em milhões sem casas escrevia "R$ 0 Mi" em todas as marcas com um mês e um vendedor escolhidos; rótulos de categoria sem concatenar |
| `clusteredBarChart` | eixo de valor oculto e sem grade; eixo de categoria Segoe UI 9 `#3D4756`; rótulos de dado ligados, fora da ponta, em milhões com uma casa; espaçamento interno 40% |
| `clusteredColumnChart` | igual à barra |
| `tableEx` | grade horizontal `#EDF0F3`, vertical desligada, respiro de linha 3; cabeçalho Segoe UI Semibold 8 `#3D4756` sobre branco com contorno só embaixo em `#C9D0D9`; valores Segoe UI 9 `#1B2430`; total Segoe UI Semibold 9 sobre `#F3F5F8`. A barra de dados não vem do tema, vai no visual: cor `#C9D8E8`, na estrutura que o Desktop gravou |
| `pivotTable` | igual à tabela; cabeçalho de linha Segoe UI 9 `#1B2430`; cabeçalho de grupo de coluna alinhado à esquerda |

## O que fica de fora de propósito

Nada de gradiente, ícone decorativo ou emoji, e nada de imagem de fundo: a faixa do cabeçalho é uma
forma e o logotipo é uma caixa de texto, que um leitor de tela consegue ler. Nada de dica de
ferramenta em página nesta versão, porque as dicas nativas já levam o que a paridade pede sem
acrescentar página ao relatório. O ícone por bloco do cartão, que o padrão admite, ficou desligado,
porque pediria registrar imagem no relatório sem acrescentar leitura.
