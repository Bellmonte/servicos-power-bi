# Enquadramento da análise

Escrito em 11-10-2026, antes da primeira execução do notebook, seguindo a fase 1 (entendimento do
negócio) e a triagem de viabilidade do CRISP-DM. A pergunta, a linha de base e o critério de
decisão abaixo não mudam depois de visto o resultado. Se alguma coisa precisar mudar, a mudança
entra no fim deste arquivo com data e motivo, e o texto original fica como está.

Trabalho na **etapa 1** da régua de entrega: análise que roda na máquina de quem contrata, sem
nada hospedado.

## Situação

A distribuidora fictícia da base vende três linhas de produto para clientes de porte pequeno,
médio e grande, em cinco regiões. A política comercial em vigor deixa o vendedor conceder desconto
por linha de pedido até um teto que depende do porte: até 18% para cliente grande e até 10% para
os demais. Em três anos, o desconto concedido somou R$ 148,4 milhões, o equivalente a 17% da
margem do período, segundo o manifesto da base.

O argumento que sustenta essa política é conhecido em qualquer área comercial: o desconto compra
volume. Se isso for verdade, o desconto se paga. Se não for, ele é margem entregue sem
contrapartida.

## A pergunta

**O desconto concedido está comprando volume que pague o que custa, ou está só reduzindo a margem?
E quanto a empresa recupera por ano limitando o desconto do cliente grande a 10%, o mesmo teto dos
demais portes?**

Objetivo de negócio: decidir se o teto de desconto do cliente grande cai de 18% para 10%, com o
efeito na margem anual expresso em faixa.

Objetivo técnico: estimar o efeito do desconto sobre a quantidade comprada, separando o efeito do
porte do cliente, com intervalo de confiança, e comparar esse efeito com o mínimo que pagaria o
desconto.

## Linha de base

São duas, e as duas ficam calculadas no notebook antes da estimativa principal.

1. **A política atual**, que é a regra que já existe: teto de 18% para cliente grande e de 10%
   para os demais. A margem dos últimos doze meses sob essa política é o ponto de comparação de
   qualquer cenário.
2. **A leitura simples**, que é o que um relatório comum mostraria: a quantidade média por linha
   em cada faixa de desconto, sem separar o porte do cliente. Ela é a resposta que a análise
   precisa confirmar ou desmentir.

## Método

O efeito principal é a variação percentual da quantidade por linha a cada ponto percentual de
desconto, estimada por regressão do logaritmo da quantidade sobre o desconto, com efeito fixo de
porte e erro padrão agrupado por cliente, porque as linhas de um mesmo cliente não são
independentes entre si. Duas especificações de robustez acrescentam o produto e o vendedor como
controles. O porte entra porque é a variável de confusão plausível: cliente grande compra mais e
também recebe desconto maior, e por isso as duas coisas andam juntas mesmo que uma não cause a
outra (`analise-de-correlacao-entre-variaveis`, passo 7).

O ponto de equilíbrio é o efeito mínimo que pagaria o desconto. Um ponto percentual a mais de
desconto custa 1% da receita bruta da linha, e só se paga se a quantidade extra trouxer pelo menos
essa margem. Para a carteira de clientes grandes, o equilíbrio é 0,01 vezes a receita bruta
dividida pela margem, somadas na janela de estimação. Esse número sai da conta, e não do
resultado da regressão.

Validação que respeita o tempo: a estimativa é feita nos primeiros 24 meses da base (setembro de
2023 a agosto de 2025) e confirmada nos 12 meses seguintes (setembro de 2025 a agosto de 2026),
que também são o ano de referência para o efeito do teto na margem.

Uma leitura secundária olha a recompra: entre os clientes grandes, quem recebeu desconto médio
maior nos primeiros 24 meses fez mais pedidos nos 12 meses seguintes?

Semente fixa em tudo que sorteia, e a base sai do gerador com data de corte fixa.

## Critério de decisão

Escrito antes de qualquer estimativa, sobre o intervalo de confiança de 95% do efeito estimado na
janela de estimação, entre clientes grandes:

| Resultado | Decisão |
|---|---|
| limite superior do intervalo **abaixo** do ponto de equilíbrio | o desconto acima de 10% não se paga em volume; recomendar o teto, com o ganho de margem em faixa |
| limite inferior do intervalo **acima** do ponto de equilíbrio | o desconto se paga; manter a política atual |
| intervalo **contendo** o ponto de equilíbrio | inconclusivo; a base não sustenta a decisão, e o passo seguinte é um teste controlado antes de mudar a política |

A confirmação nos 12 meses seguintes precisa levar à mesma decisão. Se levar a outra, o resultado
é inconclusivo, qualquer que seja o da janela de estimação.

## Faixa do efeito na margem

O ganho do teto em 12 meses é apresentado como faixa. O limite de cima supõe que nenhum cliente
compra menos por causa do teto. O limite de baixo supõe a perda de volume do pior caso plausível,
dada pelo limite superior do intervalo do efeito. A conta também diz quanto volume os clientes
afetados precisariam deixar de comprar para o ganho desaparecer, que é a pergunta de robustez da
`calculo-de-roi-de-projeto-de-dados` (passo 6).

## O que encerra a análise

A análise termina com uma das três decisões do critério, e a terceira é uma entrega tão válida
quanto as outras duas. O relatório diz qual delas saiu, com o número, e diz o que a base sintética
não permite afirmar.

## Metodologias seguidas

| Fase | Roteiro de método |
|---|---|
| enquadramento e critério | `enquadramento-de-projeto-de-dados-com-crisp-dm` |
| perfilamento da base | `perfilamento-descritivo-de-base-nova` |
| domínio e extremos | `deteccao-e-tratamento-de-outliers` |
| tipagem, grão e junção | `preparacao-de-base-para-modelagem` |
| associação e confusão | `analise-de-correlacao-entre-variaveis` |
| regressão para explicação, resíduo e faixa | `projecao-de-valores-com-regressao` |
| faixa e robustez do ganho | `calculo-de-roi-de-projeto-de-dados` |
| desenho do piloto recomendado | `planejamento-e-analise-de-teste-ab`, `dimensionamento-e-desenho-de-amostra` |

## Adendo de 11-10-2026, antes da primeira execução

A revisão do desenho, feita antes de qualquer estimativa, trouxe as mudanças abaixo. O texto acima
fica como estava, e onde houver conflito vale este adendo.

1. **Resposta conhecida, declarada antes.** O gerador da base sorteia o desconto de cada linha sem
   nenhuma ligação com a quantidade, e isso está no código público dele. Dentro do mesmo porte, o
   efeito verdadeiro do desconto sobre o volume é zero por construção. A previsão, escrita aqui
   antes de rodar, é um efeito perto de zero com intervalo estreito. O caso passa a ser um teste de
   método com resposta conhecida: a leitura simples precisa enganar, e o método precisa encontrar o
   zero e transformá-lo numa decisão com número.
2. **Estimador principal.** Regressão de Poisson por pseudo-máxima verossimilhança da quantidade
   sobre o desconto em pontos percentuais, só com clientes grandes, com erro padrão agrupado em
   duas dimensões, cliente e vendedor, porque o desempenho do vendedor é um choque comum a todas as
   linhas dele. O Poisson mede o efeito sobre a quantidade média, que é a escala da conta de
   margem. A regressão do logaritmo e os efeitos fixos de produto, vendedor e mês ficam como
   robustez.
3. **Ponto de equilíbrio.** Passa a ser o efeito que zera o ganho do teto de 10% na janela de
   estimação, calculado pela mesma função que calcula a faixa do ganho. O equilíbrio marginal da
   versão anterior (0,01 vezes a receita bruta dividida pela margem) fica só como referência.
4. **Regra de concordância.** A decisão sai da especificação principal na janela de estimação. A
   robustez e a confirmação nos 12 meses seguintes só podem rebaixar o resultado para inconclusivo,
   nunca promover. Com isso não há correção de nível para múltiplas especificações.
5. **Faixa do ganho.** O limite superior do efeito entra truncado em zero, para o teto nunca ser
   creditado com ganho de volume. A incerteza do ano seguinte entra por reamostragem de clientes
   (1.000 reamostragens, semente 42) sobre os 12 meses de confirmação. A perda de volume e a saída
   de clientes que zerariam o ganho passam a ser números principais de robustez.
6. **Escopo acrescentado.** A mesma conta de faixa para três tetos do cliente grande (10%, 12% e
   14%), e a exposição por conta: quantos clientes grandes concentram o desconto acima do teto.
7. **Leitura de recompra.** Fica exploratória, sem voto na decisão, porque o gerador também sorteia
   o cliente de cada pedido sem relação com o desconto.
8. **Leitura simples.** Faixas de desconto de 2 em 2 pontos. A previsão é um artefato de
   composição: acima de 10% só existe cliente grande, que compra mais por ser grande. A inclinação
   ingênua, sem separar o porte, entra como linha de base do estimador.

## Emenda de forma, 11-10-2026

Depois da execução, a revisão de segurança antes da publicação pediu a troca de um termo interno.
O cabeçalho da segunda coluna da tabela de metodologias passou a "Roteiro de método", no lugar de
um nome de acervo interno de estudos. É a única mudança no texto acima, de forma e sem efeito sobre
pergunta, linha de base, critério ou método. Os dois hashes estão em `decisoes.md`.

## Emenda de método, 11-10-2026, posterior à execução

Depois da primeira execução, um confronto do caso com o material de estudo que sustenta o método
levou a quatro mudanças. Elas vêm registradas aqui porque contrariam o adendo, que foi escrito antes
de qualquer resultado.

1. **Efeito fixo de cliente** entrou entre as especificações de robustez que votam na decisão.
2. **A regressão do logaritmo da quantidade saiu da votação** e ficou como leitura à parte, porque o
   efeito no logaritmo não se traduz no efeito sobre a média quando a variância cresce com a
   quantidade, e o ponto de equilíbrio está na escala da média.
3. **A faixa do ganho por reamostragem de clientes saiu.** O ganho é uma conta sobre todos os
   clientes do período, sem incerteza amostral, e passou a ser apresentado como ponto, ao lado do
   ganho com o pior efeito plausível e de cenários de saída de clientes.
4. **O piloto** passou a ser sorteado dentro de cada vendedor principal, e o poder passou a ser lido
   como teste de não inferioridade.

Nenhuma das mudanças altera a decisão. Pela versão escrita antes da execução, com o logaritmo
votando e sem o efeito fixo de cliente, todas as especificações e a confirmação ficam com o
intervalo abaixo do ponto de equilíbrio, e a decisão é a mesma, recomendar o teto. Pergunta, linhas
de base, ponto de equilíbrio e critério de decisão continuam como estão. O hash depois desta emenda
está em `decisoes.md`.
