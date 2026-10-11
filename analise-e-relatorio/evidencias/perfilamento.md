# Perfilamento da base

Resumo do perfilamento feito no notebook, seção 2, pelos oito passos do roteiro de perfilamento de
base nova. Cada item aponta para a célula que o verifica, e as verificações que podem falhar estão
escritas como asserção: se a base mudar, o notebook para ali.

## A base

Gerada pelo `port-gerador-dados` com data de corte fixa em 31-08-2026, semente 42 e 36 meses de
janela, de 01-09-2023 a 31-08-2026. O notebook confere os parâmetros e as somas de controle contra
o `_manifesto.json` antes de qualquer conta (C03, C05).

| Tabela | Linhas | Uso na análise |
|---|---|---|
| `fato_vendas` | 1.000.000 | todas as colunas |
| `dim_cliente` | 20.000 | porte do cliente |
| `dim_produto` | 1.500 | linha de produto |

## 1. O que é uma linha (C07)

Uma linha é um produto dentro de um pedido. O pedido carrega cliente, vendedor, data e horário, e
não repete produto. São 249.858 pedidos, e todos os 20.000 clientes do cadastro compraram pelo
menos uma vez. Foram conferidas como únicas a chave da linha (`venda_id`), o par pedido e produto,
o cliente no cadastro e o produto no cadastro.

## 2. Classificação das colunas (C08)

| Coluna no notebook | Natureza | Distintos |
|---|---|---|
| `ID_VENDA`, `COD_PRODUTO`, `COD_CLIENTE`, `COD_VENDEDOR`, `COD_PEDIDO` | identificador, sem conta | 1.000.000, 1.500, 20.000, 150, 249.858 |
| `DT_VENDA`, `DT_EMISSAO` | data, e data com hora | 1.096 dias |
| `CLAS_REGIAO`, `CLAS_PORTE`, `CLAS_LINHA` | categórica nominal | 5, 3, 3 |
| `QTD_ITENS` | numérica discreta | 51 valores |
| `PCT_DESCONTO` | numérica contínua, de 0 a 0,18 | 181 valores (três casas) |
| `VLR_RECEITA_BRUTA`, `VLR_RECEITA_LIQUIDA`, `VLR_CUSTO`, `VLR_MARGEM` | numérica contínua, em reais | |

Nenhuma coluna tem nulo. As chaves foram lidas como inteiro e o número do pedido como texto, com o
tipo declarado na leitura (C04). O horário de emissão tem 249.226 valores distintos para 249.858
pedidos, porque pedidos diferentes podem sair no mesmo segundo, e não entra na análise.

## 3. Distribuição das categóricas (C09)

O porte do cliente no cadastro se divide em 54,7% pequeno, 32,4% médio e 12,8% grande. As três
linhas de produto têm um terço do catálogo cada. Nas vendas, o Sudeste concentra 33,6% das linhas
e o Norte 8,0%. Não há grafia diferente para o mesmo valor nem categoria vazia.

## 4 a 6. Numéricas, centro e extremos (C12, C13)

| Coluna | Média | Mediana | Mínimo | Máximo |
|---|---|---|---|---|
| itens por linha | 7,5 | 5 | 1 | 55 |
| desconto | 5,5% | 5,3% | 0% | 18% |
| receita bruta por linha | R$ 2.269,79 | R$ 1.048,44 | R$ 40,07 | R$ 42.674,59 |
| margem por linha | R$ 865,77 | R$ 347,67 | R$ 7,16 | R$ 18.407,49 |

A quantidade e os valores são assimétricos, com média bem acima da mediana, porque o porte muda a
escala: o cliente pequeno leva em média 3,1 itens por linha, o médio 9,0 e o grande 22,5. Por isso
o efeito do desconto é estimado dentro do porte e em escala proporcional, e não sobre a média
geral.

O domínio foi conferido por asserção: desconto entre 0 e 18%, e até 10% fora do porte grande;
quantidade de pelo menos 1; receita bruta positiva; receita líquida igual à bruta menos o desconto,
e margem igual à líquida menos o custo, com tolerância de um centavo. Nenhuma linha tem margem
negativa.

A cerca do intervalo interquartil, calculada dentro de cada porte, marca 1,4% das linhas como
quantidade alta. São pedidos grandes legítimos, dentro do que o porte compra, e ficam na base. A
régua só levantou candidatos, como pede o roteiro de extremos.

## 7. Média ponderada (C14)

O desconto médio por linha e o desconto sobre a receita (total de desconto dividido pela receita
bruta) coincidem em cada porte, 5% no pequeno e no médio e 9% no grande, porque o desconto não
depende do tamanho da linha. Os indicadores do relatório usam a forma ponderada, que é a que vale
para margem.

## 8. Decisões sobre o que foi encontrado

| Achado | Decisão |
|---|---|
| quantidade assimétrica e dependente do porte | estimar o efeito dentro do porte, em escala proporcional (Poisson) |
| desconto acima de 10% só existe no porte grande | é a confusão que a análise precisa separar; documentada como linha de base |
| linhas acima da cerca de quantidade | mantidas, são pedido grande legítimo |
| horário de emissão repetido entre pedidos | fora da análise, sem efeito |
| nenhum nulo, duplicata ou valor fora do domínio | nenhum tratamento necessário |
