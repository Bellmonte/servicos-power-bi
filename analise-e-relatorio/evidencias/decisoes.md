# Decisões do caso

Registro curto do que foi decidido e por quê, na ordem em que aconteceu. O trabalho está na
**etapa 1** da régua de entrega.

## 1. A pergunta

Três candidatas foram avaliadas contra a base comercial sintética:

| Candidata | Veredito | Motivo |
|---|---|---|
| **O desconto compra volume que pague o que custa? Quanto rende um teto de 10% para o cliente grande?** | **escolhida** | decisão concreta de política comercial com efeito direto na margem; a base tem desconto por linha, quantidade, margem e porte, e a confusão entre porte e desconto existe de fato no dado, o que faz a leitura simples enganar e dá ao método algo para desmontar |
| Quais clientes estão esfriando e quanto da receita está em risco | descartada | o gerador sorteia o cliente de cada pedido sem ciclo de vida nem perda de cliente; qualquer "cliente esfriando" seria ruído, e a análise forçaria conclusão |
| Projeção de receita dos próximos dois trimestres, com faixa | descartada | a base sustenta, mas a projeção só recuperaria a sazonalidade fixa do gerador e serve planejamento, sem decisão de margem; projeção com intervalo também é tema de outra peça do catálogo |

## 2. A resposta já é conhecida, e isso foi declarado antes

O gerador é público e sorteia o desconto sem ligação com a quantidade. O efeito verdadeiro, dentro
do porte, é zero por construção. Em vez de mexer no gerador para criar um efeito e deixar a
história mais interessante, o caso foi assumido como teste de método com resposta conhecida, e
isso foi escrito no adendo do enquadramento antes da primeira execução. O que o caso mostra é a
leitura simples enganando, o método chegando ao zero e esse zero sustentando uma decisão com
número.

## 3. Prova de que o critério veio antes do resultado

O enquadramento, com o adendo, foi fechado em 11-10-2026 às 15:31, antes da primeira execução do
notebook. O SHA-256 do arquivo nesse momento era
`511b482db898602d4bc03efd47f9693e15f2c74c7eeaa7d1b1acb02fd84782ac`. Qualquer mudança posterior
entra no fim dele, com data, e muda o hash.

Houve uma mudança desse tipo, depois da execução: a revisão de segurança pediu a troca de um termo
interno num cabeçalho de tabela, e a emenda de forma no fim do enquadramento descreve o que mudou.
O hash depois da emenda é
`8fbaf555c5a6ed0d3b692491c4d45cf568c9b7e33b5992e98a6847fe59ca5ca3`.

Depois houve uma emenda de método, também posterior à execução e registrada no fim do enquadramento:
efeito fixo de cliente na robustez, logaritmo fora da votação, ganho como ponto em vez de faixa e
piloto sorteado por vendedor. Ela não muda a decisão, porque a versão anterior leva ao mesmo
resultado. O hash depois dela é
`3eb2eb04d4cbb230aaf2c3381bd75cae870fe56b7730286a55a1618931ced54c`.

Para ser exato sobre o que já se sabia: antes do adendo, a triagem de viabilidade olhou a
quantidade média por faixa de desconto e por porte, e um teste da biblioteca de regressão rodou
uma vez sobre a janela de estimação para conferir que ela aguentava o volume. A regra do gerador,
pública, já dizia o que esses números mostraram.

## 4. Método

| Decisão | Motivo |
|---|---|
| base de 1 milhão de linhas, e não a de 5 milhões | o mesmo comando do caso de refatoração com menos linhas; sobra amostra (128 mil linhas de cliente grande) e o notebook roda em menos de um minuto |
| Poisson por pseudo-máxima verossimilhança como estimador principal | mede o efeito sobre a quantidade média, que é a escala da conta de margem |
| só clientes grandes no modelo principal | a decisão é sobre o teto do cliente grande, e só ele recebe desconto acima de 10% |
| erro agrupado por cliente e por vendedor | as linhas de um mesmo cliente e de um mesmo vendedor não são independentes |
| ponto de equilíbrio derivado da conta do teto | critério e ganho saem da mesma função, sem aproximação |
| ganho apresentado como ponto, com cenários de saída de clientes | a conta usa todos os clientes do período, então não há incerteza amostral a declarar; uma faixa por reamostragem chegou a ser usada e foi retirada, porque passava ao gestor uma precisão que não existia justamente onde o risco é maior |
| efeito fixo de cliente na robustez, e o logaritmo fora da votação | o cliente é o primeiro controle que um revisor pediria em dado real; o logaritmo mede a mediana, enquanto o equilíbrio está na escala da média |
| piloto sorteado dentro de cada vendedor principal, lido como não inferioridade | os dois grupos ficam com a mesma mistura de vendedores, e o poder é medido como a chance de demonstrar que a saída fica abaixo da margem, que é como esse tipo de teste se lê |
| conferência da base pelo manifesto, e não por hash do CSV | o separador de linha do CSV muda entre Windows e Linux, e o hash mudaria sem o dado mudar; o manifesto confere parâmetros, contagem e somas |
| `pyfixest` para a regressão | absorve efeitos fixos e agrupa o erro em duas dimensões, com a correção de graus de liberdade feita pela biblioteca |

## 5. Escopo

Ficam fora deste trabalho a execução do piloto, que entra só desenhado, o efeito por produto,
região ou vendedor como resultado, métodos causais além da regressão com efeitos fixos, painel e
atualização recorrente. A leitura de recompra fica como exploratória, sem voto na decisão.
