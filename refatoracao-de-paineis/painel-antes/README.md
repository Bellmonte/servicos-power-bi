# Painel comercial antes da refatoração (v1)

Este é o painel comercial na versão de partida, a que chega ao serviço de refatoração, em formato
PBIP com o modelo em TMDL. Ele foi **construído de propósito com defeitos
comuns de mercado**, para ser medido, refatorado e medido de novo, e o resultado da refatoração é o
[painel reestruturado (v2)](../painel-depois/README.md).

Os números dele estão certos nos cortes de uso do dia a dia, com uma exceção que a refatoração
encontrou: o ano anterior quebra quando o filtro deixa dias sem venda no período, como um vendedor
num mês. Fora isso, o problema dele está no jeito como chega aos números: pesa mais, atualiza e
renderiza mais devagar e dá mais trabalho para manter do que precisava. O resultado da medição e da
paridade está no [guia técnico](../evidencias/README.md), e a metodologia completa, com o motivo de
cada defeito e o protocolo de medição, em [`../evidencias/metodologia.md`](../evidencias/metodologia.md).

> **Dado 100% fictício**, gerado pelo `gerador-de-dados`. Nenhum nome, número ou entidade tem
> relação com organização ou pessoa real.

## Os defeitos que ele carrega

| # | Defeito | Onde está |
|---|---|---|
| D1 | tabela plana montada por mesclagem no Power Query | consulta `Vendas`, que mescla o fato com `dim_produto`, `dim_cliente`, `dim_vendedor` e `dim_calendario` |
| D2 | colunas de alta cardinalidade sem uso ou com tipo ruim | `venda_id`, `data_hora_emissao` e `numero_pedido` em texto, todas carregadas |
| D3 | coluna calculada no papel de medida | `Lucro`, `Margem % Linha`, `Mês Ano` com `FORMAT` e `Ordem Mês` |
| D4 | medidas implícitas | receita, custo, quantidade, margem e pedidos entram nos visuais como agregação da coluna, e toda coluna numérica soma por padrão, inclusive os códigos |
| D5 | DAX com iteração cara | `Receita Linha Premium`, `Clientes com Compra` e `Ticket Médio` |
| D6 | página sobrecarregada | a página Visão geral, com 22 visuais: seis segmentações, nove cartões, dois gráficos de tendência, rosca, duas barras, matriz de cliente por trimestre e tabela dos 20 produtos |
| D7 | inteligência de tempo sobre a data do fato, sem tabela de calendário | as medidas de tempo usam `Vendas[data]` com um remendo de `ALL` em nove colunas de calendário |
| D8 | relação bidirecional sem necessidade | `Regioes` e `Clientes` filtram `Vendas` nos dois sentidos, e a relação entre `Regioes` e `Clientes` fica inativa |
| D9 | consulta por referência que relê a fonte | `Clientes` é uma referência à consulta `Vendas`, com remoção de duplicadas |

## Como abrir

O passo a passo completo, com o comando do `gerador-de-dados` para a base de 1 e de 5 milhões de
linhas e o parâmetro `PastaDados`, está no [guia técnico](../evidencias/README.md#como-subir-na-sua-máquina).
Em resumo: gerar a base, abrir `painel-antes.pbip`, apontar `PastaDados` para a pasta
`comercial` da base, terminando com barra invertida, e clicar em **Atualizar**. A atualização relê os
seis CSV e refaz as mesclagens, e esse tempo é parte do que a medição compara.

A data e hora automáticas ficam desligadas. As medidas de tempo não dependem delas, e as
segmentações de ano e mês usam `Vendas[ano]` e `Vendas[mes]`.

Custo: zero. O Power BI Desktop e o gerador são gratuitos, e nada fica hospedado.

---

<sub>**B&B** · Matheus Belmonte</sub>
