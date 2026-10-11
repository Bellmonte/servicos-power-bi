# Sistema visual do painel comercial

Escrito em 11-10-2026, antes de qualquer página existir em PBIR. O painel reaproveita inteiro o
sistema visual B&B já aplicado no caso de refatoração, descrito em
[`../../../refatoracao-de-paineis/painel-depois/design/SISTEMA_VISUAL.md`](../../../refatoracao-de-paineis/painel-depois/design/SISTEMA_VISUAL.md),
e este documento lista só o que muda ou se acrescenta. O layout página a página está em
[`LAYOUT.md`](LAYOUT.md) e o desenho de tela em [`mockup.html`](mockup.html).

O trabalho está na etapa de entregável: um arquivo que roda na máquina de quem recebe, sem
nada hospedado, com dado sintético e custo zero.

## O que vem do sistema B&B sem mudança

Paleta inteira, com os neutros, o azul petróleo `#1D5A8C` como única cor de destaque, a cor de
comparação `#7D8796` sempre tracejada, as semânticas bom `#1E7A4C` e ruim `#B3261E` sempre
acompanhadas de seta, e a sequência de oito cores de categoria. Tipografia em Segoe UI com a mesma
escala, nenhum texto abaixo de 8 pt. Grade de 1280 x 720, margem lateral de 16 px, calha de 12 px
entre blocos lado a lado e 10 px entre faixas. Chassi de cabeçalho com a faixa clara `#E8EEF5` de
100 px, o logotipo "B&B" em Segoe UI Black 20 pt numa caixa de 84 x 48 em x 20, y 24, igual ao
cabeçalho do caso de refatoração para os dois painéis ficarem iguais, a pergunta da página com a linha de apoio, o navegador de abas com os cantos de
cima cortados e as três segmentações suspensas de ano, mês e região, sincronizadas entre as quatro
páginas com "Selecionar tudo" ligado. Linha de produto, porte do cliente e vendedor no painel de
filtros, no nível do relatório, com busca no vendedor. Rodapé por cartão novo, com a janela da base
lida do calendário e o aviso de dado sintético. Blocos brancos com borda de raio 5 e sombra leve,
sem barra de ícones. Regras de título, formato de número, estados de interação e itens de
acessibilidade, todos como lá.

## O que muda ou se acrescenta

| # | Item | No sistema B&B | Neste painel | Por quê |
|---|---|---|---|---|
| 1 | Referência dos blocos do cartão | "Mês anterior:" | "Ano anterior:", na receita líquida e na margem % | o catálogo de indicadores compara com o mesmo período do ano anterior e não tem medida de mês anterior |
| 2 | Quando a comparação aparece | com um único mês no contexto | com um único ano no contexto; sem ano escolhido, a referência mostra hífen e a pílula some | sem ano escolhido, a regra do ano anterior compara a janela inteira com a janela deslocada e escreve um crescimento que ninguém deve ler |
| 3 | Cor da pílula | código `.cor_var_*` por indicador comparado | o mesmo padrão, em duas medidas: `.cor_crescimento_ano_anterior` e `.cor_variacao_margem_pp` | só dois blocos têm comparação; a regra condicional por igualdade a 0, 1 e 2 é a estrutura que o Desktop já gravou |
| 4 | Cartão de indicadores | um, na primeira página, com 150 px | um por página em três páginas: 150 px na Visão executiva (com pílula), 130 px em Margem e desconto e em Clientes (sem pílula) | cada pergunta abre com os seus números; 130 px bastam para rótulo, valor e referência quando não há pílula |
| 5 | Gráfico mensal e a caixa Mês | a caixa Mês filtra o gráfico | a caixa Mês não filtra os quatro gráficos mensais (interação desligada) | com um mês escolhido o gráfico virava uma coluna só; assim o cartão lê o mês e o gráfico mostra o ano em volta dele |
| 6 | Segunda série nos gráficos mensais | só a linha tracejada do ano anterior | linhas contínuas para percentuais no eixo secundário: margem % em `#3E8E8B` (sequência 3), desconto médio e clientes sem compra em `#C27C3A` (sequência 4) | tracejado continua reservado ao ano anterior; as duas cores passam de 3:1 sobre branco e cada série tem legenda escrita |
| 7 | Barras com percentual | rótulo em milhões com uma casa, pelo tema | o visual sobrescreve `labels.labelDisplayUnits` para 1 e deixa as casas com a medida | o tema escreve rótulo de barra em milhões, o que estraga percentual; a sobrescrita fica no visual para o tema não mudar |
| 8 | Nome dos visuais do chassi | prefixo só na primeira página, identificador gerado nas outras | todo visual leva o prefixo da página: `ve`, `md`, `cl` e `vd` | as páginas são escritas em PBIR do zero, e nome legível em todas deixa o diff e a conferência mais fáceis |

A cor de atenção `#9A6700` continua reservada. Nenhum visual usa limite de alerta, porque não existe
regra de negócio escrita que diga a partir de quanto o desconto ou a perda de clientes preocupa.

## Tema

**Decisão: reaproveitar o `BBComercial.json` como está**, copiado sem alteração para
`StaticResources/RegisteredResources/BBComercial.json` do relatório novo e registrado como tema
personalizado por cima do tema base do Desktop.

O tema cobre todos os tipos de visual que as quatro páginas usam: `textbox`, `shape`,
`pageNavigator`, `slicer`, `lineClusteredColumnComboChart`, `clusteredBarChart`, `tableEx` e
`pivotTable`. O `cardVisual` fica de fora dele de propósito, como no caso de refatoração, porque
`padding`, `spacing` e `divider` no tema apagam o cartão novo (lição L45); por isso os cartões de
indicadores e o rodapé são formatados no próprio visual. O tema já passou pela conferência de chave
contra a lista de objetos do Desktop instalado, e mexer nele obrigaria a repetir essa conferência
sem ganho visível.

As duas diferenças deste painel ficam no visual, e não no tema: a cor das linhas contínuas mora no `dataPoint` de cada gráfico mensal, e a unidade dos
rótulos das barras com percentual mora no `labels` de cada barra. As entradas de `clusteredColumnChart`,
`actionButton` e `multiRowCard`, que este painel não usa, ficam no tema para quem herdar o arquivo.

## Formato de número, o que se acrescenta

As regras de formato são as do sistema B&B. O que entra de novo é o texto dos blocos que o caso de
refatoração não tinha:

| Onde | Formato | Exemplo |
|---|---|---|
| Valor do bloco, receita bruta, custo, desconto concedido, receita do ano anterior e acumulado no ano | o texto por faixa dos reais, com os cortes meio passo abaixo da fronteira | R$ 69,6 Mi; R$ 464 Mi; R$ 4,5 Mi |
| Valor do bloco, desconto médio e clientes sem compra % | percentual com uma casa, em texto pt-BR | 6,5%; 32,1% |
| Valor do bloco, clientes ativos, base de 12 meses e clientes sem compra | inteiro com milhar | 6.412; 19.776; 6.346 |
| Pílula do crescimento | seta, sinal e uma casa | ▲ +2,7%; ▼ -1,5% |
| Pílula da margem % | seta, sinal, uma casa e "p.p." | ▲ +0,4 p.p. |
| Crescimento em tabela e dica | o formato da própria medida, com seta | ▲ +5,3% |
| Variação da margem em tabela | o formato da própria medida, sem seta | +0,4; -1,1 |

A lista das medidas de texto que o modelo precisa ter, com nome e máscara, está em
[`LAYOUT.md`](LAYOUT.md#medidas-de-exibição-que-o-desenho-pede-ao-modelo).

## Acessibilidade, o que se acrescenta

| Item | Como conferir |
|---|---|
| informação que não depende só de cor | as pílulas têm seta, o crescimento em tabela tem seta, a variação da margem tem sinal, e cada série dos gráficos mensais tem legenda escrita e forma própria (coluna, linha tracejada ou linha contínua) |
| contraste das duas cores novas de linha | `#3E8E8B` com 3,9:1 e `#C27C3A` com 3,4:1 sobre branco, acima do piso de 3:1 para objeto gráfico; nenhuma delas é usada em texto |
| função que não depende do mouse | o filtro por clique na tabela de vendedores está escrito na linha de apoio e no subtítulo; a lista de reativação depende só da caixa Região, que é visível |
| texto alternativo e ordem de tabulação | por página, no `LAYOUT.md` |
