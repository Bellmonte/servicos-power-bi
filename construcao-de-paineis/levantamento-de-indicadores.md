# Levantamento de indicadores do painel comercial

## Contexto

O cenário é o de uma diretoria comercial que precisa de um painel construído do zero para acompanhar o resultado de vendas e apoiar quatro decisões recorrentes: onde concentrar o esforço comercial, como ajustar a política de desconto, quais clientes reativar e como acompanhar cada vendedor. Este documento é o levantamento que abre o serviço de construção, preenchido para esse cenário: as decisões que o painel apoia, os vinte indicadores com a regra de cada um, as regras gerais de leitura, os critérios de aceite e o que fica fora desta entrega. Ele funciona como contrato entre o levantamento, o dicionário de medidas e o painel, e por isso os nomes de indicador escritos aqui são os mesmos que aparecem no modelo.

A base registra a venda por item de pedido, com o produto classificado em três linhas (Essencial, Performance e Premium), o cliente classificado por porte (Pequeno, Médio e Grande) e por região, e o vendedor responsável. Um pedido reúne vários itens e pertence sempre a um único cliente e a um único vendedor. A janela cobre 36 meses, de 01-09-2023 a 31-08-2026.

**Dado fictício.** Todos os dados do painel são 100% fictícios, gerados pelo `gerador-de-dados` com data de corte fixa. Nenhum cliente, vendedor, produto ou valor corresponde a uma empresa real.

**Ambiente e custo.** O painel roda no Power BI Desktop da máquina de quem recebe, lendo arquivos locais, sem hospedagem e sem custo recorrente. O custo declarado é zero, porque as ferramentas usadas são gratuitas e nada fica publicado em serviço pago. A entrega inclui um README que sobe o painel do zero numa máquina limpa, os critérios de aceite da seção 4, a base sintética de exemplo e o custo declarado. Como o painel lê arquivos locais e não usa credencial, não há arquivo de configuração de credencial.

## 1. Decisões que o painel apoia

Cada página do painel responde a uma pergunta e traz essa pergunta no cabeçalho.

| # | Página | Pergunta | Decisão | Quem decide | Frequência |
|---|---|---|---|---|---|
| 1 | Visão executiva | O resultado está acima do ano anterior, e de onde vem a receita? | onde concentrar o esforço comercial no mês seguinte | diretoria comercial | mensal |
| 2 | Margem e desconto | Onde o desconto está corroendo a margem? | revisar a política de desconto por porte e por linha | diretoria comercial | mensal |
| 3 | Clientes | A base de clientes está ativa ou esfriando, e onde? | montar a lista de reativação por região e porte | gestão comercial das regiões | semanal |
| 4 | Vendedores | Quem vende com margem saudável e quem compra volume com desconto? | acompanhamento individual e meta de margem por vendedor | diretoria comercial com a gestão das equipes | mensal |

A base é atualizada uma vez por dia, quando o arquivo de vendas é gerado de novo, e o painel é atualizado na própria máquina de quem o usa. A leitura principal acontece na reunião mensal de resultado, e a página de clientes é consultada toda semana para montar a lista de reativação.

## 2. Indicadores

São vinte indicadores, organizados em cinco grupos: receita, desconto e margem, volume, clientes e ano anterior. A coluna "Medida" traz o nome técnico exatamente como ele aparece no modelo, sem acento, com a unidade entre parênteses quando ela existe. A coluna "Página" indica onde o indicador apoia a decisão, com os nomes da seção 1.

| # | Medida | Nome de negócio | Regra de negócio | Unidade | Periodicidade | Página |
|---|---|---|---|---|---|---|
| 1 | `Receita Bruta (R$)` | Receita bruta | valor vendido a preço de tabela, antes do desconto | R$ | diária, leitura mensal | Margem e desconto |
| 2 | `Receita Liquida (R$)` | Receita líquida | faturamento já descontado; é o indicador principal do painel | R$ | diária, leitura mensal | Visão executiva; Margem e desconto; Vendedores |
| 3 | `Participacao na Receita (%)` | Participação na receita | fatia de cada item na receita líquida de tudo o que está selecionado na tela | % | diária, leitura mensal | Visão executiva |
| 4 | `Desconto Concedido (R$)` | Desconto concedido | quanto deixou de entrar por desconto: receita bruta menos receita líquida | R$ | diária, leitura mensal | Visão executiva; Margem e desconto |
| 5 | `Desconto Medio (%)` | Desconto médio | desconto concedido dividido pela receita bruta, ou seja, ponderado pelo valor vendido | % | diária, leitura mensal | Visão executiva; Margem e desconto; Vendedores |
| 6 | `Custo (R$)` | Custo | custo dos itens vendidos | R$ | diária, leitura mensal | Visão executiva; Margem e desconto |
| 7 | `Margem (R$)` | Margem | receita líquida menos custo, como vem do sistema de origem | R$ | diária, leitura mensal | Visão executiva; Margem e desconto |
| 8 | `Margem (%)` | Margem percentual | margem dividida pela receita líquida | % | diária, leitura mensal | Visão executiva; Margem e desconto; Vendedores |
| 9 | `Pedidos` | Pedidos | quantidade de pedidos distintos, independentemente de quantos itens cada um tem | pedidos | diária, leitura mensal | Visão executiva; Clientes |
| 10 | `Quantidade (un)` | Quantidade vendida | unidades vendidas | unidades | diária, leitura mensal | Vendedores |
| 11 | `Ticket Medio (R$)` | Ticket médio | receita líquida dividida pelo número de pedidos | R$ | diária, leitura mensal | Visão executiva; Clientes; Vendedores |
| 12 | `Clientes Ativos` | Clientes ativos | clientes distintos com ao menos uma compra no período selecionado | clientes | diária, leitura mensal | Clientes; Vendedores |
| 13 | `Base de Clientes 12 Meses` | Base de clientes de 12 meses | clientes com ao menos uma compra nos 365 dias que terminam na última data do período | clientes | diária, leitura semanal | Clientes |
| 14 | `Clientes sem Compra 90 Dias` | Clientes sem compra há 90 dias | dos clientes da base de 12 meses, os que não compraram nos 90 dias que terminam na última data do período | clientes | diária, leitura semanal | Clientes |
| 15 | `Clientes sem Compra 90 Dias (%)` | Clientes sem compra há 90 dias, em percentual | clientes sem compra há 90 dias divididos pela base de clientes de 12 meses | % | diária, leitura semanal | Clientes |
| 16 | `Receita Ano Anterior (R$)` | Receita do ano anterior | receita líquida no mesmo período do ano anterior; fica vazia quando esse período não está inteiro na base | R$ | diária, leitura mensal | Visão executiva |
| 17 | `Crescimento sobre Ano Anterior (%)` | Crescimento sobre o ano anterior | variação da receita líquida contra a do ano anterior; fica vazio quando não há ano anterior | % | diária, leitura mensal | Visão executiva |
| 18 | `Margem Ano Anterior (%)` | Margem percentual do ano anterior | margem percentual no mesmo período do ano anterior; fica vazia quando esse período não está inteiro na base | % | diária, leitura mensal | Visão executiva; Margem e desconto |
| 19 | `Variacao Margem sobre Ano Anterior (p.p.)` | Variação da margem sobre o ano anterior | diferença entre a margem percentual do período e a do ano anterior; fica vazio se faltar um dos lados | p.p. | diária, leitura mensal | Visão executiva; Vendedores |
| 20 | `Receita Acumulada no Ano (R$)` | Receita acumulada no ano | receita líquida de 1º de janeiro até a última data do período, dentro do mesmo ano | R$ | diária, leitura mensal | Visão executiva |

## 3. Regras gerais

**O que não se soma.** Contagens distintas e razões são recalculadas em cada célula e nunca somadas. Pedidos não se somam entre linhas de produto, porque um pedido pode ter itens de mais de uma linha. Clientes ativos não se somam entre meses, entre linhas de produto nem entre vendedores, porque o mesmo cliente compra em vários meses, compra mais de uma linha e pode ser atendido por mais de um vendedor da sua região. Margem percentual, desconto médio, ticket médio e participação são sempre razão das somas, e nunca média dos percentuais das linhas, porque a média dá o mesmo peso a um item pequeno e a um pedido grande e distorce o resultado. O total de qualquer tabela do painel é calculado pela mesma regra do indicador, e por isso pode diferir da soma visual das linhas nesses casos.

**Ano anterior pelo calendário.** As medidas de ano anterior deslocam as datas do período selecionado em um ano, sobre a tabela de calendário do modelo, que vai da primeira venda até a data de corte da base. Com isso, 2026 compara janeiro a agosto com janeiro a agosto de 2025, e cada mês compara com o mesmo mês do ano anterior. Quando o período deslocado não está inteiro dentro da base, a receita e a margem do ano anterior ficam vazias, e com elas o crescimento e a variação. Isso vale para os doze primeiros meses, de setembro de 2023 a agosto de 2024, para o ano de 2024 inteiro, que só teria quatro meses de 2023 para comparar, e para a janela completa sem filtro de data. A regra evita um crescimento anual inflado por comparação de doze meses contra quatro, e a leitura anual fica valendo para 2025 e 2026.

**Referência das medidas de clientes.** A base de 12 meses e os clientes sem compra há 90 dias olham para trás a partir da última data do período selecionado. Com um mês escolhido, a referência é o último dia do mês. Sem filtro de data, a referência é o fim da base, 31-08-2026. As duas medidas respeitam todo filtro que não é de data, como região, porte, linha e vendedor. Com filtro de vendedor, a leitura passa a ser a dos clientes daquele vendedor. Quando nenhum cliente da base de 12 meses está sem compra há 90 dias, as duas medidas de clientes sem compra ficam vazias, e não zero, e o painel mostra hífen; isso acontece só nos primeiros meses da base, quando todo cliente que comprou no ano também comprou no trimestre. Nos primeiros doze meses da base a janela de 365 dias começa antes da primeira venda, e a base de 12 meses desse trecho fica menor do que seria com histórico completo.

**Região é a do cliente.** Todo corte por região usa a região do cliente que fez a compra. O cadastro de vendedores também tem uma região, que não é usada em nenhum indicador nem em nenhum corte do painel.

**Por que o indicador de clientes novos ficou de fora.** Na base deste painel, quase todo cliente faz a primeira compra no primeiro ano da janela. Um indicador de clientes novos ficaria praticamente zerado a partir de 2025 e levaria à leitura errada de que a empresa parou de conquistar clientes. O tema volta quando houver histórico de cadastro anterior à janela.

**Medidas de apoio de tela.** O modelo tem medidas ocultas que só servem à apresentação, como o texto do rodapé e os valores abreviados dos cartões. Como não são indicadores, ficam fora deste levantamento e da paridade, e o dicionário de medidas as descreve num parágrafo à parte.

## 4. Critérios de aceite

A entrega está pronta quando os sete critérios abaixo passam. Eles medem se o painel foi construído conforme o combinado, e não prometem nenhum resultado de negócio.

**1. Correspondência entre levantamento, dicionário e painel.** Os vinte nomes da coluna "Medida" da seção 2 aparecem de forma idêntica no dicionário de medidas e na tabela de medidas visíveis do modelo, sem indicador a mais nem a menos. Verifica-se comparando as três listas.

**2. Cada página responde à sua decisão.** As quatro páginas existem com os nomes da seção 1 e trazem a pergunta correspondente no cabeçalho.

**3. Paridade com a conta direta na base.** Cada indicador é calculado de duas formas independentes, pela conta direta sobre os arquivos da base e pelo modelo aberto no Power BI Desktop, e os resultados são comparados nos cortes abaixo. A conta direta reproduz a regra da seção 2, inclusive a referência das medidas de clientes e o deslocamento de ano anterior.

| Corte | Chaves | Indicadores comparados |
|---|---|---|
| total | 1 | 1 a 20 |
| ano-mês | 36 | 1 a 20 |
| região | uma por região | 1 a 20 |
| linha de produto | 3 | 1 a 20 |
| porte | 3 | 1 a 20 |
| vendedor, pela chave | 150 | 1 a 20 |
| cliente, pela chave | 20.000 | 1, 2, 4, 6, 7, 9, 10 e 12 |
| ano-mês por região | 36 por região | 1 a 20 |
| linha de produto em 2026 | 3 | 1 a 20 |

Todos os cortes comparam os vinte indicadores, menos o de cliente. Nos cortes sem filtro de data, as medidas de ano anterior ficam vazias pela regra da seção 3, e a paridade confere que elas ficam vazias também na conta direta. O corte por cliente usa só os indicadores que fazem sentido para um cliente isolado. Vendedor e cliente são comparados pela chave, e nunca pelo nome.

| Tipo de indicador | Tolerância |
|---|---|
| contagem (pedidos, quantidade, clientes) | igualdade exata |
| valor em reais | diferença de até R$ 0,01 por célula |
| razão, percentual e pontos percentuais | diferença de até 0,000001 na unidade da medida |

Vazio dos dois lados conta como igual. A tolerância existe só para absorver a ordem de soma em ponto flutuante. O critério passa quando o número de divergências é zero, e qualquer divergência acima da tolerância é investigada e explicada, nunca resolvida alargando a tolerância.

**4. README que sobe do zero.** Uma pessoa que não participou da construção, numa máquina limpa, segue o README do início ao fim e chega ao painel aberto e atualizado, sem ajuda e sem passo que não esteja escrito.

**5. Base gerada por comando com data fixa.** A base é gerada pelo comando documentado no README, com data de corte fixa em 31-08-2026. Duas execuções do comando produzem as mesmas contagens de linhas e as mesmas somas registradas no manifesto da base, e o painel aponta para a pasta gerada por um único parâmetro.

**6. Custo declarado.** O README declara o custo da solução, que é zero, e lista as ferramentas gratuitas necessárias para abrir e atualizar o painel.

**7. Aviso de dado fictício.** O README e o rodapé de todas as páginas do painel informam que os dados são fictícios e trazem a janela da base.

## 5. Fora de escopo nesta entrega

- **Meta.** O painel apoia a definição de meta de margem por vendedor, mas a base não traz meta e o painel não compara realizado contra meta.
- **Previsão.** Nenhum indicador projeta receita, margem ou atividade de clientes para o futuro.
- **Publicação hospedada com atualização agendada.** Publicar o painel num serviço, agendar a atualização e controlar o acesso por perfil, como vendedor vendo só os próprios números, dependem de licença e de configuração do serviço do Power BI, e ficam fora desta entrega.
- **Clientes novos.** Fica de fora pelo motivo explicado na seção 3.
- **Peso de mercado da região.** A base traz esse atributo, mas nenhuma das quatro decisões depende dele.
- **Região do vendedor.** Não é usada em nenhum corte, conforme a seção 3.
