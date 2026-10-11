# Registro de mudanças da refatoração

Este é o registro do que foi mudado no painel comercial entre o painel de partida (v1) e o painel
reestruturado (v2), em que ordem e por quê, no formato que acompanha a entrega do serviço. Cada
linha é um passo do trabalho na pasta
[`painel-comercial-v2/`](painel-comercial-v2/), registrado durante o serviço com o motivo da
mudança, e a especificação dos defeitos está na [seção 3 da especificação](ESPECIFICACAO.md).

A regra de todas as mudanças foi a do serviço: nenhuma regra de negócio muda, e as medidas
acordadas precisam dar o mesmo número na v1 e na v2 nos cortes da seção 6. As duas exceções de
comportamento estão descritas no fim, porque quem contrata o serviço precisa conhecê-las antes de
aceitar a entrega.

## O que mudou

| Passo | Defeito | O que mudou | Número muda |
|---|---|---|---|
| 1 | ponto de partida | cópia exata da v1 | não |
| 2 | D9 | a tabela de clientes passa a ler o cadastro, em vez de reler as vendas e refazer as mesclagens | não |
| 3 | D1 | vendas guarda só o fato; produto, vendedor e calendário viram tabelas próprias, ligadas por relação de um para muitos | não |
| 4 | D3 | `Lucro` e `Margem % Linha` deixam de ser colunas calculadas por venda; a margem vira medida sobre a margem que vem da origem, e o rótulo de mês passa ao calendário | não |
| 5 | D7 | o calendário vira a tabela de data oficial, e as medidas de ano anterior e de acumulado deixam o remendo que desligava colunas de data uma a uma | não nos cortes acordados; ver exceção 1 |
| 6 | D8 | toda relação vai do cadastro para as vendas em direção única, a relação inativa sai, e a região fica num lugar só | não nos cortes acordados; ver exceção 2 |
| 7 | D2 | saem o código da linha e a data e hora da emissão, que não apareciam em nenhum visual, e o pedido passa a ser guardado como número, exibido ainda como `PV-000000123` | não |
| 8 | D4 | cada indicador vira uma medida com nome de negócio, usada por todos os visuais; as colunas numéricas param de somar sozinhas e as chaves ficam ocultas | não |
| 9 | D5 | receita da linha premium, clientes com compra e ticket médio deixam de percorrer a tabela de vendas linha a linha | não |
| 10 | D6 | a Visão geral cai de 22 para 10 visuais: os nove cartões viram um cartão de várias linhas, três filtros vão para o painel de filtros e a matriz de clientes por trimestre ganha página própria | não |
| 11 | correção | as colunas brutas de quantidade e margem passam a se chamar `quantidade_linha` e `margem_linha`, porque tinham o mesmo nome das medidas e o Power BI recusava abrir o modelo | não |

## Redesenho visual

Depois da refatoração, o painel ganhou acabamento visual, pelo sistema definido em
[`painel-comercial-v2/design/`](painel-comercial-v2/design/). A v1 continua com o visual padrão, de propósito. Nenhuma
mudança desta seção mexe em regra ou em número.

| Passo | O que mudou | Número muda |
|---|---|---|
| 12 | tema próprio registrado no relatório: fundo cinza claro, blocos brancos, uma cor de destaque e escala de fonte fixa | não |
| 13 | valores em reais, variação com seta e sinal, data em dia, mês e ano, trimestre como T1 a T4, e o nome do mês por extenso no calendário | não |
| 14 | Visão geral com a moldura comum (navegação, pergunta da página, filtros de ano, mês e região sincronizados, rodapé), filtros de linha, porte e vendedor no nível do relatório, gráfico mensal com o acumulado na dica e a rosca trocada por colunas | não |
| 15 | Clientes e vendedores na moldura comum, com títulos de negócio e ordem pela receita | não |
| 16 | Clientes por trimestre na moldura comum, sem os filtros de página que as segmentações sincronizadas substituem | não |
| 17 | Detalhe de vendas na moldura comum, com detalhamento por cliente, produto e vendedor e botão Voltar; a tabela mantém campos e ordem | não |

## Padronização

Em 10-10-2026 o painel reestruturado foi reconstruído no padrão de desenvolvimento da B&B: modelo
em estrela com prefixo de papel nas tabelas, medidas numa tabela própria com nome de negócio,
unidade e descrição, calendário gerado por função e o chassi de tela com cabeçalho, faixa de
indicadores e rodapé. A reconstrução mexe em nome, organização e forma, e a regra de cada número
continua a mesma.

**Número muda: não.** As dezesseis medidas da seção 4 da especificação mantêm o resultado em todos
os cortes, e o que mudou nelas foi o nome, a tabela onde moram e, em duas, a forma da fórmula.

| Mudança | O que mudou | Número muda |
|---|---|---|
| nomes do modelo | as tabelas ganham o prefixo do papel (`Fact_Vendas`, `Dim_Produto`, `Dim_Cliente`, `Dim_Vendedor`, `Dim_Regiao`, `Dim_Calendario`); as colunas recebem nome de negócio no último passo do Power Query, e chave, data da venda e coluna de valor ficam ocultas | não |
| tabela de medidas | todas as medidas saem da tabela de vendas e vão para `Medidas`, uma tabela sem coluna de dado, em seis pastas numeradas por assunto e duas internas; o nome carrega a unidade, como `Receita Liquida (R$)`, e toda medida tem descrição com o que é, o formato, quando usar e quando não usar | não |
| calendário | gerado pela função `fn_Calendario`, com a janela lida do manifesto que acompanha a base; continua marcado como tabela de data e com as mesmas 1.096 datas, de 01-09-2023 a 31-08-2026 | não |
| ano anterior | `DATEADD` de um ano no lugar de `SAMEPERIODLASTYEAR`, que devolve o mesmo conjunto de datas; a correção do ano anterior em corte fino continua valendo | não |
| Power Query | cada tabela lê o próprio arquivo em passos com nome que diz o que fazem (`Fonte`, `ComCabecalho`, `TiposAjustados`, `Renomeadas`); o parâmetro da pasta passa a se chamar `pPastaDados`, e as consultas ficam nos grupos `Parametros`, `Funcoes`, `Tabelas Dimensao` e `Tabelas Fato` | não |
| faixa de indicadores | cartão novo com oito blocos, valor abreviado pela unidade do próprio cartão; com um único mês escolhido, sete blocos mostram o valor do mês anterior e a variação numa pílula verde ou vermelha, e a Linha Premium mostra a participação na receita; o crescimento sobre o ano anterior continua na dica do gráfico mensal, mês a mês | não |
| medidas retiradas | saem as seis medidas de exibição "(cartão)", as sete de variação sobre o ano anterior criadas para o cartão anterior e a medida de teste, porque nenhum visual usa mais | não |
| chassi | cabeçalho de 100 pontos com o logotipo, a pergunta da página, as abas de navegação e as três segmentações sincronizadas; blocos com borda de raio 5 e sombra, sem cabeçalho de visual; rodapé com a janela da base, a unidade e o recorte, escrito por medida | não |
| tema | borda de raio 5 e sombra nos blocos de dado, cabeçalho de visual desligado, abas sobre a faixa clara do cabeçalho e segmentação com caixa de raio 5 | não |

Três mudanças são de forma e aparecem na tela. Percentual passa a ter uma casa decimal, como pede o
padrão, e por isso a margem de 40,81% aparece como 40,8%, com o mesmo valor por trás. O trimestre da
matriz de clientes passa de T1 a Tri. 1, e o mês do eixo e da matriz de vendedores passa de set/2023 a
set'23, que são os rótulos da função de calendário.

Para a medição, duas diferenças entram na conta. O rodapé deixa de ser texto fixo e passa a ser uma
consulta pequena ao calendário em cada página, inclusive no Detalhe de vendas, que é a página de
referência. E o cartão de indicadores da Visão geral passa a pedir também as medidas do mês anterior.
A tabela do Detalhe de vendas continua com os mesmos campos, na mesma ordem.

## Exceções de comportamento

**1. Ano anterior em corte fino.** Na v1, as medidas de ano anterior trabalhavam sobre a data das
próprias vendas. Com um filtro amplo, como mês ou região, todo dia do período tem venda e o número
sai certo. Com um filtro fino, como um vendedor que não vende todo dia, os dias do período deixam de
ser contínuos e o Power BI recusa o cálculo, e o visual mostra erro. Na base de construção, um
vendedor que vendeu em 23 dos 31 dias de agosto de 2026 fazia o ano anterior da v1 dar erro assim que
ele e o mês eram escolhidos na Visão geral. A v2 usa o período completo do calendário, que é a regra
escrita na seção 4, e mostra R$ 269.893,41, a receita desse vendedor em agosto de 2025 inteiro,
conferida direto na base. O número passa a existir nesse tipo de corte, e a mudança corrige a v1.

**2. Listas de filtro.** Na v1, região e cliente filtravam as vendas nos dois sentidos, e por isso
uma lista de filtro encolhia para mostrar só o que tinha venda nos outros filtros. Na v2, as
listas mostram todos os itens do cadastro. Nenhum valor de indicador muda, e o que muda é o conteúdo
da lista de seleção.
