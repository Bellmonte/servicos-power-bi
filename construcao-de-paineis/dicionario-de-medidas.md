# Dicionário de medidas do painel comercial

> Arquivo gerado a partir do modelo semântico (`painel/painel-comercial.SemanticModel/definition/tables/Medidas.tmdl`). Não edite à mão: a regra muda no modelo e este arquivo é regerado, a partir da pasta `construcao-de-paineis`, com `python evidencias/gerar_dicionario.py`.

Todas as medidas partem da tabela de fato `Fact_Vendas`. Grão: uma linha por item de pedido, isto é, um produto vendido a um cliente por um vendedor numa data. Um pedido tem vários itens. Guarda só chaves, valores e o número do pedido; os atributos moram nas dimensões. Cada número respeita os filtros e segmentações que estiverem na tela, e as razões são sempre refeitas sobre as somas do recorte. São 20 medidas de negócio em 5 pastas, na ordem em que aparecem no painel de campos do Power BI.

| Pasta | Medidas |
|---|---|
| 01 Receita | Receita bruta (R$), Receita líquida (R$), Participação na receita (%) |
| 02 Desconto e Margem | Desconto concedido (R$), Desconto médio (%), Custo (R$), Margem (R$), Margem (%) |
| 03 Volume | Pedidos, Quantidade (un), Ticket médio (R$) |
| 04 Clientes | Clientes ativos, Base de clientes 12 meses, Clientes sem compra 90 dias, Clientes sem compra 90 dias (%) |
| 05 Ano Anterior | Receita ano anterior (R$), Crescimento sobre ano anterior (%), Margem ano anterior (%), Variação margem sobre ano anterior (p.p.), Receita acumulada no ano (R$) |

## 01 Receita

### Receita bruta (R$)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Receita Bruta (R$)` |
| Unidade | reais (R$) |
| Formato | `\R\$ #,0.00` |

**Definição.** Receita a preço de tabela, antes do desconto: soma do valor bruto de cada item de pedido, em reais com duas casas.

**Quando usar.** Use para medir o tamanho da venda antes da negociação e como base do desconto concedido.

**Quando não usar.** Não use como faturamento do período, que é a Receita Liquida (R$).

```dax
SUM ( Fact_Vendas[Valor Bruto] )
```

### Receita líquida (R$)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Receita Liquida (R$)` |
| Unidade | reais (R$) |
| Formato | `\R\$ #,0.00` |

**Definição.** Faturamento do período já descontado: soma do valor líquido de cada item de pedido, em reais com duas casas. É o indicador principal de receita do painel.

**Quando usar.** Use como medida de resultado em qualquer recorte de região, linha de produto, porte, vendedor ou mês.

**Quando não usar.** Não use para falar de rentabilidade, que pede a Margem (R$) ou a Margem (%).

```dax
SUM ( Fact_Vendas[Valor Liquido] )
```

### Participação na receita (%)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Participacao na Receita (%)` |
| Unidade | percentual |
| Formato | `0.0%;-0.0%;0.0%` |

**Definição.** Fatia do item na receita líquida de tudo o que está selecionado na tela: a receita do item dividida pela receita do conjunto visível, respeitando segmentações e filtros, em percentual com uma casa. As fatias de um mesmo visual fecham em 100%.

**Quando usar.** Use em tabela ou gráfico quebrado por região, linha de produto, porte ou vendedor, para ver quem concentra a receita.

**Quando não usar.** Não use em cartão sem quebra, onde o resultado é sempre 100%, nem para comparar fatias de telas com filtros diferentes.

```dax
DIVIDE (
    [Receita Liquida (R$)],
    CALCULATE ( [Receita Liquida (R$)], ALLSELECTED () )
)
```

## 02 Desconto e Margem

### Desconto concedido (R$)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Desconto Concedido (R$)` |
| Unidade | reais (R$) |
| Formato | `\R\$ #,0.00` |

**Definição.** Quanto deixou de entrar por desconto: receita bruta menos receita líquida, em reais com duas casas.

**Quando usar.** Use para dimensionar em dinheiro o custo da política de desconto num recorte.

**Quando não usar.** Não use para comparar recortes de tamanho diferente, que pedem o Desconto Medio (%).

```dax
[Receita Bruta (R$)] - [Receita Liquida (R$)]
```

### Desconto médio (%)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Desconto Medio (%)` |
| Unidade | percentual |
| Formato | `0.0%;-0.0%;0.0%` |

**Definição.** Desconto médio ponderado pelo valor bruto: desconto concedido dividido pela receita bruta, razão das somas, em percentual com uma casa.

**Quando usar.** Use para comparar a intensidade do desconto entre porte, linha de produto, região e vendedor.

**Quando não usar.** Não use a média simples do percentual de cada item no lugar dela, porque um item pequeno pesaria o mesmo que um item grande.

```dax
DIVIDE ( [Desconto Concedido (R$)], [Receita Bruta (R$)] )
```

### Custo (R$)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Custo (R$)` |
| Unidade | reais (R$) |
| Formato | `\R\$ #,0.00` |

**Definição.** Custo dos itens vendidos: soma do custo total de cada item de pedido, em reais com duas casas.

**Quando usar.** Use junto da receita líquida para explicar a margem.

**Quando não usar.** Não use como despesa da operação, que não está na base.

```dax
SUM ( Fact_Vendas[Valor Custo] )
```

### Margem (R$)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Margem (R$)` |
| Unidade | reais (R$) |
| Formato | `\R\$ #,0.00` |

**Definição.** Margem bruta em valor: soma da margem de cada item, que é a receita líquida menos o custo, como vem da origem, em reais com duas casas.

**Quando usar.** Use para resultado em dinheiro e para ver quem traz mais margem absoluta.

**Quando não usar.** Não use para comparar recortes de tamanho diferente, que pedem a Margem (%).

```dax
SUM ( Fact_Vendas[Valor Margem] )
```

### Margem (%)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Margem (%)` |
| Unidade | percentual |
| Formato | `0.0%;-0.0%;0.0%` |

**Definição.** Margem sobre a receita líquida: Margem (R$) dividida por Receita Liquida (R$), razão das somas, em percentual com uma casa.

**Quando usar.** Use para comparar rentabilidade entre recortes de tamanho diferente e para acompanhar o efeito do desconto.

**Quando não usar.** Não use a média das margens percentuais de meses, regiões ou vendedores, porque a razão precisa ser refeita sobre as somas.

```dax
DIVIDE ( [Margem (R$)], [Receita Liquida (R$)] )
```

## 03 Volume

### Pedidos

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Pedidos` |
| Unidade | contagem |
| Formato | `#,0` |

**Definição.** Número de pedidos distintos no período, contado pelo número do pedido; um pedido tem vários itens.

**Quando usar.** Use para volume de transações e como base do ticket médio.

**Quando não usar.** Não use somando recortes de linha de produto ou de produto, porque um pedido com itens de duas linhas conta uma vez em cada uma.

```dax
DISTINCTCOUNT ( Fact_Vendas[Numero Pedido] )
```

### Quantidade (un)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Quantidade (un)` |
| Unidade | unidades |
| Formato | `#,0` |

**Definição.** Unidades vendidas: soma da quantidade de cada item de pedido.

**Quando usar.** Use para volume físico e para comparar giro entre linhas de produto.

**Quando não usar.** Não use como número de pedidos, nem para tratar como equivalentes produtos de preço muito diferente.

```dax
SUM ( Fact_Vendas[Quantidade Vendida] )
```

### Ticket médio (R$)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Ticket Medio (R$)` |
| Unidade | reais (R$) |
| Formato | `\R\$ #,0.00` |

**Definição.** Receita líquida por pedido: Receita Liquida (R$) dividida por Pedidos, em reais com duas casas.

**Quando usar.** Use para ver se o pedido médio cresce ou encolhe num recorte de região, porte, vendedor ou mês.

**Quando não usar.** Não use a média de tickets de meses ou vendedores, que precisa ser refeita sobre as somas, nem em recorte por linha de produto sem lembrar que o pedido com itens de várias linhas entra em cada uma delas.

```dax
DIVIDE ( [Receita Liquida (R$)], [Pedidos] )
```

## 04 Clientes

### Clientes ativos

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Clientes Ativos` |
| Unidade | contagem |
| Formato | `#,0` |

**Definição.** Clientes distintos com ao menos uma compra no período selecionado.

**Quando usar.** Use para acompanhar quantos clientes estão comprando, mês a mês ou por recorte.

**Quando não usar.** Não use somado entre meses ou vendedores, porque o mesmo cliente compra em vários meses e com mais de um vendedor, nem como tamanho da base de clientes, que olha os últimos 12 meses.

```dax
DISTINCTCOUNT ( Fact_Vendas[ID Cliente] )
```

### Base de clientes 12 meses

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Base de Clientes 12 Meses` |
| Unidade | contagem |
| Formato | `#,0` |

**Definição.** Clientes distintos com ao menos uma compra nos 365 dias que terminam na última data do período selecionado. Respeita todo filtro que não é de data, e sem filtro de data a referência é o fim da base.

**Quando usar.** Use como denominador da leitura de clientes sem compra e para dimensionar a base de clientes viva num recorte.

**Quando não usar.** Não use somado mês a mês, porque cada mês olha os doze anteriores, nem nos doze primeiros meses da base, quando a janela ainda está incompleta.

```dax
VAR v_ref = MAX ( Dim_Calendario[Data] )
RETURN
    CALCULATE (
        DISTINCTCOUNT ( Fact_Vendas[ID Cliente] ),
        DATESBETWEEN ( Dim_Calendario[Data], v_ref - 364, v_ref )
    )
```

### Clientes sem compra 90 dias

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Clientes sem Compra 90 Dias` |
| Unidade | contagem |
| Formato | `#,0` |

**Definição.** Dos clientes da base de 12 meses, os que não compraram nos 90 dias que terminam na última data do período selecionado. Respeita todo filtro que não é de data, e com filtro de vendedor conta os clientes daquele vendedor.

**Quando usar.** Use para montar e dimensionar a lista de reativação por região e porte.

**Quando não usar.** Não use somado entre meses, nem nos doze primeiros meses da base, quando a janela de 12 meses ainda está incompleta.

```dax
VAR v_ref = MAX ( Dim_Calendario[Data] )
VAR v_base =
    CALCULATETABLE ( VALUES ( Fact_Vendas[ID Cliente] ), DATESBETWEEN ( Dim_Calendario[Data], v_ref - 364, v_ref ) )
VAR v_recentes =
    CALCULATETABLE ( VALUES ( Fact_Vendas[ID Cliente] ), DATESBETWEEN ( Dim_Calendario[Data], v_ref - 89, v_ref ) )
RETURN
    COUNTROWS ( EXCEPT ( v_base, v_recentes ) )
```

### Clientes sem compra 90 dias (%)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Clientes sem Compra 90 Dias (%)` |
| Unidade | percentual |
| Formato | `0.0%;-0.0%;0.0%` |

**Definição.** Parcela da base de 12 meses que está sem compra há 90 dias: Clientes sem Compra 90 Dias dividido por Base de Clientes 12 Meses, em percentual com uma casa.

**Quando usar.** Use para comparar regiões, portes e vendedores de tamanhos diferentes.

**Quando não usar.** Não use a média do percentual entre recortes, porque a razão precisa ser refeita sobre as contagens.

```dax
DIVIDE ( [Clientes sem Compra 90 Dias], [Base de Clientes 12 Meses] )
```

## 05 Ano Anterior

### Receita ano anterior (R$)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Receita Ano Anterior (R$)` |
| Unidade | reais (R$) |
| Formato | `\R\$ #,0.00` |

**Definição.** Receita líquida no mesmo período do ano anterior, com as datas do filtro deslocadas em um ano pelo calendário, em reais com duas casas; vazio quando o mesmo período do ano anterior não está inteiro na base, o que vale para os doze primeiros meses, para o ano de 2024 inteiro e para a base sem filtro de data.

**Quando usar.** Use como referência de comparação anual em cartão, tabela ou linha do tempo mensal.

**Quando não usar.** Não use para comparar períodos de tamanho diferente, nem trate o vazio como zero.

```dax
VAR v_inicio = MIN ( Dim_Calendario[Data] )
VAR v_inicio_base = CALCULATE ( MIN ( Dim_Calendario[Data] ), REMOVEFILTERS ( Dim_Calendario ) )
RETURN
    IF ( EDATE ( v_inicio, -12 ) >= v_inicio_base, CALCULATE ( [Receita Liquida (R$)], DATEADD ( Dim_Calendario[Data], -1, YEAR ) ) )
```

### Crescimento sobre ano anterior (%)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Crescimento sobre Ano Anterior (%)` |
| Unidade | percentual |
| Formato | `▲ +0.0%;▼ -0.0%;0.0%` |

**Definição.** Variação da receita líquida contra o mesmo período do ano anterior: a diferença entre as duas dividida pela do ano anterior, em percentual com seta; vazio quando não há ano anterior inteiro na base.

**Quando usar.** Use para dizer se o período está melhor ou pior que o mesmo período do ano anterior.

**Quando não usar.** Não use a média das variações de meses ou recortes, nem trate o vazio dos primeiros períodos como crescimento zero.

```dax
VAR a = [Receita Liquida (R$)]
VAR b = [Receita Ano Anterior (R$)]
RETURN
    IF ( ISBLANK ( b ), BLANK (), DIVIDE ( a - b, b ) )
```

### Margem ano anterior (%)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Margem Ano Anterior (%)` |
| Unidade | percentual |
| Formato | `0.0%;-0.0%;0.0%` |

**Definição.** Margem percentual no mesmo período do ano anterior, refeita como razão das somas sobre as datas deslocadas em um ano, em percentual com uma casa; vazio quando o mesmo período do ano anterior não está inteiro na base.

**Quando usar.** Use como referência da margem atual em cartão e tabela.

**Quando não usar.** Não use a média das margens de anos anteriores de vários recortes, nem trate o vazio como margem zero.

```dax
VAR v_inicio = MIN ( Dim_Calendario[Data] )
VAR v_inicio_base = CALCULATE ( MIN ( Dim_Calendario[Data] ), REMOVEFILTERS ( Dim_Calendario ) )
RETURN
    IF ( EDATE ( v_inicio, -12 ) >= v_inicio_base, CALCULATE ( [Margem (%)], DATEADD ( Dim_Calendario[Data], -1, YEAR ) ) )
```

### Variação margem sobre ano anterior (p.p.)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Variacao Margem sobre Ano Anterior (p.p.)` |
| Unidade | pontos percentuais |
| Formato | `+0.0;-0.0;0.0` |

**Definição.** Diferença entre a margem atual e a do mesmo período do ano anterior, em pontos percentuais: Margem (%) menos Margem Ano Anterior (%), vezes cem; vazio se faltar um dos lados.

**Quando usar.** Use para dizer quantos pontos de margem o período ganhou ou perdeu.

**Quando não usar.** Não use como variação percentual da margem, que seria outra conta, nem trate o vazio como estabilidade.

```dax
VAR a = [Margem (%)]
VAR b = [Margem Ano Anterior (%)]
RETURN
    IF ( ISBLANK ( a ) || ISBLANK ( b ), BLANK (), ( a - b ) * 100 )
```

### Receita acumulada no ano (R$)

| Campo | Conteúdo |
|---|---|
| Nome técnico | `Receita Acumulada no Ano (R$)` |
| Unidade | reais (R$) |
| Formato | `\R\$ #,0.00` |

**Definição.** Receita líquida de 1º de janeiro até a última data do período selecionado, dentro do mesmo ano, em reais com duas casas.

**Quando usar.** Use em linha do tempo mensal para acompanhar o acumulado do ano.

**Quando não usar.** Não use em 2023, que começa em setembro na base e por isso acumula só quatro meses, nem somando anos diferentes.

```dax
CALCULATE ( [Receita Liquida (R$)], DATESYTD ( Dim_Calendario[Data] ) )
```

## Medidas de suporte de tela

As medidas abaixo ficam ocultas, começam com ponto e devolvem texto pronto para um elemento de tela, como o valor abreviado de um cartão ou o rodapé. Elas não entram em cálculo, comparação, exportação nem na conferência de paridade, e por isso aparecem aqui só pelo nome e pela função.

| Nome técnico | Pasta | Para que serve |
|---|---|---|
| `.rodape_pagina` | .Internas\UI | Texto do rodapé de todas as páginas: origem sintética do dado, janela da base lida do calendário, unidade e recorte de região. |
| `.kpi_receita_liquida` | .Internas\UI | Texto de Receita Liquida (R$) para o valor do cartão, escrito com FORMAT na cultura pt-BR e formato curto por faixa: R$ 2,1 Bi a partir de um bilhão, R$ 952 Mi de cem milhões para cima, R$ 24,8 Mi a partir de um milhão e R$ 339.930 abaixo disso; vazio quando a medida base é vazia, e o cartão mostra o hífen. |
| `.kpi_receita_ano_anterior` | .Internas\UI | Texto de Receita Ano Anterior (R$) para a referência do cartão, escrito com FORMAT na cultura pt-BR e o mesmo formato curto por faixa dos reais; vazio quando o ano anterior é vazio. Só devolve valor com um único ano no contexto (Dim_Calendario[Ano]), e fora disso volta vazia. |
| `.kpi_crescimento_ano_anterior` | .Internas\UI | Texto da pílula de crescimento: seta para cima quando positivo, para baixo quando negativo e nenhuma no zero, seguida de Crescimento sobre Ano Anterior (%) com sinal e uma casa na cultura pt-BR, como em ▲ +2,7%. Só devolve valor com um único ano no contexto (Dim_Calendario[Ano]), e fora disso volta vazia. |
| `.kpi_receita_acumulada_ano` | .Internas\UI | Texto de Receita Acumulada no Ano (R$) para o valor do cartão, escrito com FORMAT na cultura pt-BR e o mesmo formato curto por faixa dos reais; vazio quando a medida base é vazia. |
| `.kpi_margem_pct` | .Internas\UI | Texto de Margem (%) para o cartão, escrito com FORMAT na cultura pt-BR, como em 40,8%; vazio quando a medida base é vazia. |
| `.kpi_margem_pct_ano_anterior` | .Internas\UI | Texto de Margem Ano Anterior (%) para a referência do cartão, escrito com FORMAT na cultura pt-BR, como em 39,9%; vazio quando o ano anterior é vazio. Só devolve valor com um único ano no contexto (Dim_Calendario[Ano]), e fora disso volta vazia. |
| `.kpi_variacao_margem_pp` | .Internas\UI | Texto da pílula da margem: seta para cima quando positivo, para baixo quando negativo e nenhuma no zero, seguida de Variacao Margem sobre Ano Anterior (p.p.) com sinal, uma casa e o sufixo p.p., como em ▲ +0,4 p.p. Só devolve valor com um único ano no contexto (Dim_Calendario[Ano]), e fora disso volta vazia. |
| `.kpi_margem` | .Internas\UI | Texto de Margem (R$) para o valor do cartão, escrito com FORMAT na cultura pt-BR e o mesmo formato curto por faixa dos reais; vazio quando a medida base é vazia. |
| `.kpi_custo` | .Internas\UI | Texto de Custo (R$) para o cartão, escrito com FORMAT na cultura pt-BR e o mesmo formato curto por faixa dos reais; vazio quando a medida base é vazia. |
| `.kpi_desconto_medio` | .Internas\UI | Texto de Desconto Medio (%) para o cartão, escrito com FORMAT na cultura pt-BR, como em 6,5%; vazio quando a medida base é vazia. |
| `.kpi_desconto_concedido` | .Internas\UI | Texto de Desconto Concedido (R$) para o cartão, escrito com FORMAT na cultura pt-BR e o mesmo formato curto por faixa dos reais; vazio quando a medida base é vazia. |
| `.kpi_receita_bruta` | .Internas\UI | Texto de Receita Bruta (R$) para o valor do cartão, escrito com FORMAT na cultura pt-BR e o mesmo formato curto por faixa dos reais; vazio quando a medida base é vazia. |
| `.kpi_pedidos` | .Internas\UI | Texto de Pedidos para o cartão, escrito com FORMAT na cultura pt-BR, como em 1.234; vazio quando a medida base é vazia. |
| `.kpi_pedidos_referencia` | .Internas\UI | Texto de Pedidos para a referência do cartão, com FORMAT na cultura pt-BR e a palavra pedidos no fim, como em 1.234 pedidos; vazio quando a medida base é vazia. |
| `.kpi_ticket_medio` | .Internas\UI | Texto de Ticket Medio (R$) para o cartão, escrito com FORMAT na cultura pt-BR em reais cheios, sem centavos, como em R$ 1.234; vazio quando a medida base é vazia. |
| `.kpi_clientes_ativos` | .Internas\UI | Texto de Clientes Ativos para o valor do cartão, escrito com FORMAT na cultura pt-BR, como em 1.234; vazio quando a medida base é vazia. |
| `.kpi_base_clientes_12m` | .Internas\UI | Texto de Base de Clientes 12 Meses para o valor do cartão, escrito com FORMAT na cultura pt-BR, como em 1.234; vazio quando a medida base é vazia. |
| `.kpi_clientes_sem_compra_90d` | .Internas\UI | Texto de Clientes sem Compra 90 Dias para o valor do cartão, escrito com FORMAT na cultura pt-BR, como em 1.234; vazio quando a medida base é vazia. |
| `.kpi_clientes_sem_compra_90d_pct` | .Internas\UI | Texto de Clientes sem Compra 90 Dias (%) para a referência do cartão, escrito com FORMAT na cultura pt-BR, como em 32,1%; vazio quando a medida base é vazia. |
| `.cor_crescimento_ano_anterior` | .Internas\UI | Código de cor da pílula de crescimento sobre o ano anterior: 0 sem comparação, inclusive sem um único ano no contexto, 1 quando [Crescimento sobre Ano Anterior (%)] é maior que zero, que é favorável, e 2 quando é menor. A regra condicional do cartão lê este código para a cor do texto e do fundo da pílula. |
| `.cor_variacao_margem_pp` | .Internas\UI | Código de cor da pílula de variação da margem sobre o ano anterior: 0 sem comparação, inclusive sem um único ano no contexto, 1 quando [Variacao Margem sobre Ano Anterior (p.p.)] é maior que zero, que é favorável, e 2 quando é menor. A regra condicional do cartão lê este código para a cor do texto e do fundo da pílula. |
