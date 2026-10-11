# port-analise-dados

Este repositório demonstra serviços de Power BI em episódios. Cada episódio mostra um serviço
completo, do diagnóstico à entrega, com o painel em formato PBIP, o registro do que foi feito e o
resultado medido. Os episódios são independentes, e cada pasta tem o seu README e sobe sozinha numa
máquina com Windows e o Power BI Desktop.

> **Dados 100% fictícios.** Os nomes e os números dos episódios são inventados, e toda base é gerada
> pelo [`port-gerador-dados`](https://github.com/Bellmonte/port-gerador-dados), sem qualquer vínculo
> com organização ou pessoa real.

## Episódios

| # | Episódio | O que mostra | Estado |
|---|---|---|---|
| E1 | [Refatoração de um painel comercial](e1-refatoracao-painel-comercial/README.md) | o serviço de refatoração e manutenção aplicado a um painel com defeitos comuns de mercado, reestruturado sem mudar nenhum número de negócio: modelo 74% menor, atualização 29% mais rápida e as consultas da página principal de 22% a 88% mais rápidas, com a paridade conferida, o registro de cada mudança e o catálogo de técnicas do serviço | publicado |
| E2 | Construção de painel do zero | levantamento de indicadores no formato que o serviço entrega, dicionário de medidas e painel publicado na web, sobre a mesma base | próximo |
| E3 | Relatório e análise | uma pergunta de negócio respondida em notebook, com relatório que traz conclusão e limitação | depois do E2 |

## O que todo episódio traz

Cada episódio sobe do zero seguindo só o README dele. A base é sintética e sai de um comando com
data fixa, para os números serem os mesmos em qualquer máquina, e o custo vem declarado. Até aqui
ele é zero, porque o Power BI Desktop e o gerador são gratuitos e nada fica hospedado.

## Licença

MIT. O dado é fictício e serve de exemplo. Os temas base em `StaticResources/SharedResources/BaseThemes/` são gerados pelo Power BI Desktop e pertencem à Microsoft, por isso ficam fora dessa licença.

---

<sub>**B&B** · Matheus Belmonte</sub>
