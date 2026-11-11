# Decisões da construção

Cada decisão tomada na construção do painel, com o motivo, na ordem em que apareceu. Serve para quem
for manter o painel saber por que ele é como é, e para quem for auditar a demonstração saber o que
foi escolhido e o que ficou de fora.

| # | Decisão | Motivo |
|---|---|---|
| 1 | O painel é desenhado para a leitura de uma diretoria comercial, sem nome de empresa | a peça apresenta o serviço de construção, e um nome inventado só acrescentaria história sem acrescentar prova |
| 2 | A base é a mesma da refatoração na versão de 1 milhão de linhas, gerada pelo mesmo comando, com a data fixa de 31-08-2026, na pasta `C:\dados\painel-comercial` | uma base só atende as duas demonstrações, e 1 milhão de linhas basta para um painel de leitura gerencial; o volume de 5 milhões existe para medir desempenho, que não é o objeto desta demonstração |
| 3 | Quatro perguntas de negócio, uma por página: resultado do período, margem e desconto, clientes, vendedores | cada página responde a uma decisão que alguém toma com periodicidade conhecida, e nada entra no painel sem uma decisão por trás |
| 4 | "Clientes novos" ficou fora do levantamento | o gerador faz quase todo cliente comprar pela primeira vez no primeiro ano da base, e o indicador ficaria em zero a partir de 2025, sugerindo uma queda de captação que não existe |
| 5 | A saúde da base de clientes é medida por "clientes sem compra há 90 dias" dentro da base de quem comprou nos últimos 12 meses, com referência no fim do período escolhido | é uma lista que a área comercial transforma em ação de reativação, e a referência no fim do período deixa o número estável quando se escolhe um mês |
| 6 | A participação na receita é calculada sobre tudo o que está selecionado na tela | o mesmo indicador serve para região, linha, porte e vendedor, e a soma das fatias fecha em 100% em qualquer visual |
| 7 | O peso de mercado da região e o fator de performance do vendedor não entram no modelo | o primeiro não apoia nenhuma das quatro decisões, e o segundo é parâmetro interno do gerador, sem leitura de negócio |
| 8 | Desconto medido como razão das somas sobre a receita bruta, e nunca como média do percentual de cada linha | a média simples daria o mesmo peso a um item de R$ 50 e a um de R$ 50 mil, e o desconto que pesa na margem é o desconto em reais |
| 9 | Padrão de entrega: tabelas `Fact_` e `Dim_`, todas as medidas na tabela `Medidas`, nome técnico em ASCII com a unidade entre parênteses, descrição em três partes, calendário gerado por função a partir da janela do manifesto, relações de um para muitos em direção única | é o mesmo padrão do painel da refatoração, e quem mantém um painel mantém todos |
| 10 | Sistema visual B&B reaproveitado, com o tema `BBComercial.json` | a identidade visual é do serviço, e o que muda de um painel para outro é o layout, desenhado do zero para estas quatro perguntas |
| 11 | Paridade em duas pontas, a conta direta na base em Python e o modelo no Power BI, em nove cortes, com a tolerância da refatoração | a conta direta não passa pelo modelo, e por isso é a prova de que a regra escrita no levantamento é a regra que o painel calcula |
| 12 | Receita e margem do ano anterior ficam vazias quando o período deslocado um ano não está inteiro na base, e com elas o crescimento e a variação | sem essa regra, o ano de 2024 seria comparado com só quatro meses de 2023 e o crescimento anual sairia inflado; a leitura anual vale para 2025 e 2026 |
| 13 | A lista de reativação traz nome, porte e cidade do cliente, sem coluna de prioridade | nenhum dos 20 indicadores dá valor para um cliente parado, e acrescentar um indicador só para ordenar a lista abriria o catálogo fechado no levantamento; fica como evolução natural do painel |
| 14 | A caixa de mês não filtra os gráficos mensais | o cartão lê o mês escolhido e o gráfico mostra o ano em volta dele, que é a comparação que a reunião mensal faz |
| 15 | A comparação com o ano anterior aparece nos cartões só com um ano escolhido | com vários anos no filtro, a comparação não tem leitura, e o cartão mostra hífen em vez de um número enganoso |
| 16 | `Percentual Desconto`, preço de tabela e custo unitário ficam fora do modelo | nenhuma medida usa essas colunas, e a coluna de percentual por item convida a tirar média de razões no lugar do `Desconto Medio (%)` |
| 17 | Paridade em 1 milhão de linhas, sem medição de desempenho | o serviço de construção se prova pela regra escrita e pela paridade, e a medição de desempenho fica para a refatoração, que é onde ela serve de prova |
| 18 | A demonstração não é publicada no serviço do Power BI | publicar exige conta com licença, e a demonstração roda inteira no Desktop, sem custo; o guia técnico descreve como publicar |
