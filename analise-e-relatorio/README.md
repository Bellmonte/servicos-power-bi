# Análise e relatório

**O desconto ao cliente grande não comprava volume, e um teto de 10% teria recuperado R$ 5,5
milhões de margem no último ano.**

Uma distribuidora concede até 18% de desconto ao cliente grande e até 10% aos demais, com o
argumento de que o desconto traz volume. A análise responde se esse volume existe e quanto vale
mudar a regra, com o critério de decisão escrito antes de olhar o resultado e a resposta entregue
em faixa, junto com o risco que o dado não consegue medir.

| A leitura simples | A análise |
|---|---|
| ![Quantidade média por faixa de desconto, sem separar o porte: acima de 10% de desconto cada linha leva 3,4 vezes mais itens](imagens/01-leitura-simples.png) | ![Quantidade por faixa de desconto dentro de cada porte, em índice: as três linhas ficam planas em torno de 100](imagens/02-dentro-do-porte.png) |

## Resultado

Caso de exemplo com 1 milhão de linhas de pedido, 20 mil clientes e 36 meses de vendas.

| O que a leitura simples dizia | O que o dado sustenta | Decisão | Ganho do teto em 12 meses |
|---|---|---|---|
| **3,4 vezes mais itens**<br>nas linhas com mais de 10% de desconto | **nenhum efeito mensurável**<br>dentro do mesmo porte, contra +3,2% por ponto que pagariam o desconto | **teto de 10%**<br>pelo critério definido antes | **R$ 5,4 a 5,7 milhões**<br>de margem, se o volume se mantiver |

A diferença que a leitura simples mostrava vinha toda do porte, porque só o cliente grande recebe
mais de 10% de desconto, e ele compra mais por ser grande. O ganho desaparece se clientes
grandes que somam 4,8% da margem do porte deixarem de comprar, ou se todos eles passarem a comprar
4,8% menos. Como a base não registra a venda perdida, o relatório recomenda um piloto de 12
meses em metade dos clientes grandes, dimensionado para detectar a saída de clientes antes que ela
anule o ganho, e um grupo de controle mantido na política atual depois da adoção, porque a queda
pequena e uniforme de compra só aparece com o tempo.

## O que você recebe

- **Relatório em Word**, com situação, método, resultado, conclusão e limitações, escrito para
  quem decide.
- **Notebook que roda do zero**, com cada número do relatório apontando para a célula que o gera.
- **Critério de decisão registrado antes da análise**, para o resultado não ser escolhido depois.
- **Resposta em faixa**, com o ponto que faria a decisão mudar.
- **Desenho do próximo passo**, quando o dado sozinho não fecha a pergunta.

## Como funciona

1. **Enquadramento.** Transforma a dúvida da área numa pergunta com decisão, linha de base e
   critério, escritos antes de abrir o dado.
2. **Análise.** Perfila a base, separa o que confunde a leitura e mede o efeito com intervalo.
3. **Relatório.** Entrega a resposta, a faixa, a limitação e o passo seguinte, em linguagem de
   negócio.

## Contato

Para responder uma pergunta assim com os dados da sua empresa, fale comigo pelo
[LinkedIn](https://www.linkedin.com/in/mbelmontee).

## Para aprofundar

| Documento | O que traz |
|---|---|
| [Relatório](relatorio.md) | a resposta completa, com limitações e anexos (também em `relatorio.docx`) |
| [Guia técnico](evidencias/README.md) | método, rastreabilidade e como refazer tudo numa máquina limpa |
| [Notebook](analise.ipynb) | a análise de ponta a ponta |
| [Enquadramento](evidencias/enquadramento.md) | pergunta, linhas de base e critério, escritos antes do resultado |
| [Perfilamento](evidencias/perfilamento.md) | o estado da base antes da análise |

Custo do caso: zero, porque o gerador, o Python e as bibliotecas são gratuitos e nada fica
hospedado. A base é 100% fictícia, gerada pelo
[`port-gerador-dados`](https://github.com/Bellmonte/port-gerador-dados), sem vínculo com
organização ou pessoa real. Ela foi gerada sem ligação entre desconto e volume, e o caso mostra o
método encontrando essa resposta conhecida.

---

<sub>**B&B** · Matheus Belmonte</sub>
