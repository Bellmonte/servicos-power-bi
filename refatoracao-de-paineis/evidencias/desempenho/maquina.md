# Máquina de medição

Registro exigido pela seção 5 da [metodologia](../metodologia.md). Vale para a sessão única de
medição final, em que o painel de partida (v1) e o painel reestruturado (v2) são medidos na mesma
máquina, na mesma versão do Power BI Desktop e no mesmo dia.

| Item | Valor |
|---|---|
| processador | Intel Core i5-14400F, 10 núcleos |
| memória | 15,8 GB |
| disco | dois SSD SATA de 480 GB (WD Green e Kingston A400); base e arquivos no disco C: |
| sistema | Windows 11 Pro, compilação 22621 |
| plano de energia | alto desempenho, na tomada, conferido em cada sessão |
| Power BI Desktop | 2.155.756.0, versão de junho de 2026, na sessão de 05 e 06-10-2026; 2.158.1304 na sessão de 10-10-2026, só da v2 |
| resolução de tela | 3440 x 1440, Desktop maximizado, zoom em ajustar à página, painel de filtros recolhido |
| base | 5 milhões de linhas, `base-5m` do `port-gerador-dados`, semente fixa |
| data da sessão | 05-10-2026 e 06-10-2026, as duas pontas; 10-10-2026, a v2 padronizada |

O DAX Studio e o Tabular Editor 2 previstos na seção 5 não entram na tabela principal. O tamanho
do modelo, o tempo de atualização e o tempo de consulta a frio e a quente saem dos scripts desta
pasta, que falam direto com o motor do Desktop pela biblioteca de cliente que vem com ele. O
Tabular Editor 2 só volta para o diagnóstico de apoio, na contagem do Best Practice Analyzer.

## Desvios declarados do protocolo

**Atualização cronometrada por script.** O comando enviado é o mesmo do botão Atualizar, e o
cronômetro vai do envio ao retorno, em `medir_atualizacao.ps1`. Desvio já usado no ensaio de
27-09-2026.

**Tamanho lido do motor.** `medir_tamanho.ps1` soma o dicionário das colunas e os segmentos de
dados, de hierarquia e de relação, que é a mesma fonte do VertiPaq Analyzer, sem o arquivo `.vpax`.

**Frio por script, quente pelo analisador.** Adotado em 05-10-2026. No ensaio, a
limpeza de cache feita à mão não pegou, e a primeira execução não ficou mais lenta que as
seguintes. Por isso o tempo a frio sai de `medir_consultas.ps1`, que limpa o cache imediatamente
antes de cada consulta, e o analisador de desempenho mede só a renderização a quente, que é o
tempo que o usuário vê na tela. As consultas medidas pelo script são extraídas do próprio JSON do
analisador por `extrai_consultas.py`, então frio e quente medem as mesmas consultas.

**Duas páginas.** A página de referência continua sendo o Detalhe de vendas, a mais lenta no
ensaio. A Visão geral entra também, incluída em 05-10-2026, porque o ganho do D6 precisa ser
conferido em 5 milhões antes de virar argumento.

## Sessão de 10-10-2026 e o desvio de versão

Depois da padronização de 10-10-2026, a v2 foi medida de novo nesta máquina, sobre a mesma base de 5
milhões, com o plano de energia em alto desempenho e o Power BI Desktop 2.158.1304, que tinha sido
atualizado desde a sessão de 06-10. A v1 não mudou e não foi medida de novo, e os números dela vêm
da sessão de 06-10 no Desktop 2.155.756. Isso desvia do protocolo, que pede as duas pontas na mesma
versão e na mesma sessão, e o desvio vai declarado no resultado final e no guia técnico. O
tamanho do modelo é lido no motor e quase não depende da versão; os tempos valem como ordem de
grandeza. As consultas de medição da Visão geral e do Detalhe de vendas da v2 foram extraídas de novo
do analisador de desempenho nessa sessão, porque o cartão de indicadores, a tabela dos 20 produtos e
o rodapé mudaram de consulta na padronização.
