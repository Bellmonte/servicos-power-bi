# Painel comercial, versão reestruturada (v2)

Este é o painel comercial depois da refatoração do episódio E1, em formato PBIP com o modelo em
TMDL. Ele nasceu como cópia idêntica do [painel de partida (v1)](../painel-comercial-v1/README.md),
e cada defeito foi corrigido num passo próprio, com o motivo escrito. Em 10-10-2026 ele foi
reconstruído no padrão de desenvolvimento da B&B, sem mudar nenhum número. O que mudou, em que ordem
e por quê está no [registro de mudanças](../MUDANCAS.md), e o resultado da medição e da paridade está
no [README do episódio](../README.md).

A regra de todo passo é a mesma do serviço oferecido: os números de negócio continuam iguais aos da
v1. A especificação, com as medidas de paridade e o protocolo de medição, está em
[`../ESPECIFICACAO.md`](../ESPECIFICACAO.md).

> **Dado 100% fictício**, gerado pelo `port-gerador-dados`. Nenhum nome, número ou entidade tem
> relação com organização ou pessoa real.

## O modelo reestruturado

Esquema estrela, com uma tabela fato e cinco dimensões ligadas por relação de um para muitos em
direção única, da dimensão para o fato, e as chaves ocultas.

| Tabela | Papel |
|---|---|
| `Fact_Vendas` | fato no grão de item de venda: um produto vendido a um cliente por um vendedor numa data. Guarda só as chaves, os valores e o número do pedido |
| `Dim_Produto`, `Dim_Cliente`, `Dim_Vendedor`, `Dim_Regiao` | cadastros, cada um lido do próprio arquivo. A região é a do cliente |
| `Dim_Calendario` | calendário diário gerado pela função `fn_Calendario`, marcado como tabela de data, na janela da base |
| `Medidas` | tabela sem coluna de dado onde mora toda medida, em pastas numeradas por assunto |

As medidas visíveis têm nome de negócio com a unidade entre parênteses, como `Receita Liquida (R$)`
e `Margem (%)`, e descrição com o que são, o formato, quando usar e quando não usar. As que começam
com ponto são suporte de tela e ficam ocultas, nas pastas `.Internas\UI` e `.Texto`.

| Pasta | O que guarda |
|---|---|
| `01 Receita` | receita bruta, receita líquida, receita da Linha Premium e as duas participações |
| `02 Margem` | custo, margem em reais e margem percentual |
| `03 Volume e Pedidos` | quantidade, pedidos, ticket médio e linhas de venda |
| `04 Clientes e Mercado` | clientes com compra e peso de mercado |
| `05 Ano Anterior e Acumulado` | receita do ano anterior, acumulado no ano e crescimento sobre o ano anterior |
| `06 Mes Anterior` | o valor do mês anterior e a variação de cada indicador da faixa |
| `.Internas\UI` | o texto e o código de cor da pílula do cartão (`.ux_var_*`, `.cor_var_*`) e as medidas de exibição `.kpi_*`, que escrevem em texto pt-BR o valor e a referência de cada bloco do cartão, com a abreviação por faixa |

## As páginas

Todas as páginas têm o mesmo chassi: o cabeçalho de 100 pontos com o logotipo B&B, a pergunta de
negócio que a página responde, as abas de navegação e as caixas de ano, mês e região sincronizadas
(o que se escolhe numa página vale nas outras), e o rodapé com a janela da base, a unidade e o
recorte. Linha de produto, porte do cliente e vendedor ficam no painel de filtros, valendo para o
relatório inteiro. O visual segue o sistema de [`design/`](design/).

| Página | O que responde |
|---|---|
| Visão geral | como estão a receita e a margem, e de onde vem a receita |
| Clientes e vendedores | quem gera a receita, e se cada região vende na proporção do seu mercado |
| Clientes por trimestre | quais clientes compram mais a cada trimestre, e com que margem |
| Detalhe de vendas | quais itens compõem cada pedido; recebe detalhamento por cliente, produto e vendedor, pelo botão direito em qualquer página |

A faixa de indicadores da Visão geral compara com o mês anterior quando há um único mês no filtro.
Escolha um ano e um mês nas caixas do cabeçalho, e cada bloco passa a mostrar o valor do mês
anterior e a variação numa pílula verde, quando o indicador subiu, ou vermelha, quando caiu. Sem mês
escolhido, a pílula some de propósito, porque comparar um período de vários meses com o mês
anterior não tem leitura.

Duas coisas importam para quem for medir. O Detalhe de vendas faz quatro consultas a mais que o da
v1, que são as listas das três caixas sincronizadas e o texto do rodapé. E o painel de filtros dessa
página precisa estar sem detalhamento aplicado antes da medição (seção 5 da especificação).

## Como abrir

Os passos são os mesmos da v1 e estão no [README do episódio](../README.md#como-subir-na-sua-máquina):
gerar a base, abrir `painel-comercial-v2.pbip`, apontar o parâmetro `pPastaDados` para a pasta
`comercial` da base, terminando com barra invertida, e atualizar. O calendário lê a janela do
`_manifesto.json` que o gerador grava na mesma pasta, então os dois arquivos precisam estar juntos.

Custo: zero. O Power BI Desktop e o gerador são gratuitos, e nada fica hospedado.

---

<sub>**B&B** · Matheus Belmonte</sub>
