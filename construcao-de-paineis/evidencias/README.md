# Guia técnico: construção de um painel comercial

Este guia reúne o que é preciso para subir o painel do zero numa máquina limpa, refazer a prova de
paridade e publicar o painel na web. A [página do caso](../README.md) traz o resumo para quem decide,
e aqui está o detalhe para quem audita ou quer reproduzir.

> **Dados 100% fictícios.** Clientes, vendedores, produtos e valores foram gerados pelo
> [`port-gerador-dados`](https://github.com/Bellmonte/port-gerador-dados), sem qualquer vínculo com
> organização ou pessoa real.

O trabalho está na etapa de entregável: o painel roda no Power BI Desktop da máquina de quem recebe,
lendo arquivos locais, sem hospedagem e sem custo recorrente. **Custo: zero.** O Power BI Desktop, o
Python e o gerador são gratuitos, e nada fica hospedado. A publicação na web, descrita no fim, é a
única parte que depende de licença paga, e ela é opcional.

## O que tem no caso

| Pasta ou arquivo | O que é |
|---|---|
| [`../levantamento-de-indicadores.md`](../levantamento-de-indicadores.md) e `.docx` | as decisões que o painel apoia, os 20 indicadores com a regra de cada um e os critérios de aceite |
| [`../dicionario-de-medidas.md`](../dicionario-de-medidas.md) | cada medida do modelo com definição, DAX, unidade e quando usar, gerado a partir do próprio modelo |
| [`../painel/`](../painel/) | o painel em formato PBIP, com o modelo em TMDL e as páginas em PBIR |
| [`../painel/design/`](../painel/design/) | sistema visual, layout das páginas e o mockup aprovado antes da construção |
| [`paridade/`](paridade/) | a conta direta na base, as consultas ao modelo, o comparador e o resultado |
| [`decisoes.md`](decisoes.md) | cada decisão tomada na construção e o motivo |
| `gerar_dicionario.py` | regera o dicionário a partir do `Medidas.tmdl` |

## O modelo

O modelo é um esquema estrela com uma tabela fato e cinco dimensões, ligadas por relação de um para
muitos em direção única, da dimensão para o fato, com as chaves ocultas.

| Tabela | Papel |
|---|---|
| `Fact_Vendas` | uma linha por item de pedido, só com chaves, valores e o número do pedido |
| `Dim_Produto`, `Dim_Cliente`, `Dim_Vendedor`, `Dim_Regiao` | cadastros, cada um lido do próprio arquivo; a região é a do cliente |
| `Dim_Calendario` | calendário diário gerado pela função `fn_Calendario`, com a janela lida do manifesto da base, marcado como tabela de data |
| `Medidas` | tabela sem coluna de dado onde moram as 20 medidas de negócio, em cinco pastas, e as de suporte de tela, ocultas |

Cada medida visível tem nome técnico com a unidade entre parênteses e descrição em três partes: o
que é, quando usar e quando não usar. Essa descrição alimenta o
[dicionário](../dicionario-de-medidas.md), que é gerado do modelo para os dois nunca divergirem. A partir da pasta `construcao-de-paineis`:

```powershell
python evidencias\gerar_dicionario.py
```

## Como subir na sua máquina

Pré-requisitos: Windows com o Power BI Desktop 2.158 ou mais novo, Python 3.12 ou mais novo e Git.
A base ocupa cerca de 110 MB em disco.

**1. Gerar a base.** O painel não leva dado nenhum, só a definição do modelo e das páginas, e por
isso o primeiro passo é gerar a base com o `port-gerador-dados`. No PowerShell:

```powershell
git clone https://github.com/Bellmonte/port-gerador-dados.git
cd port-gerador-dados
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python gerar.py comercial --hoje 2026-08-31 --meses 36 --linhas 1000000 --clientes 20000 --produtos 1500 --vendedores 150 --colunas-origem --saida C:\dados\painel-comercial
```

A base sai em cerca de dez segundos em `C:\dados\painel-comercial\comercial\`, com seis arquivos CSV e
um `_manifesto.json` com a contagem de linhas e as somas de controle. A data `--hoje 2026-08-31`
precisa ficar fixa, porque é ela que faz a base sair igual em qualquer máquina e em qualquer dia, com
os mesmos números deste caso. O manifesto confere: 1.000.000 de linhas de venda e receita líquida de
R$ 2.121.440.181,12.

**2. Abrir e apontar para a base.** Clone este repositório com
`git clone https://github.com/Bellmonte/bb-servicos-power-bi.git` e abra
`construcao-de-paineis\painel\painel-comercial.pbip` no Power BI Desktop. O parâmetro `pPastaDados`
já vem com `C:\dados\painel-comercial\comercial\`, e quem gerou a base nessa pasta pula para o passo
3. Para usar outra pasta, vá em **Página Inicial > Transformar dados > Editar parâmetros** e cole o
caminho da pasta `comercial`, **terminando com barra invertida**. O calendário lê a janela do
`_manifesto.json`, então ele precisa estar na mesma pasta dos CSV.

**3. Atualizar.** Clique em **Página Inicial > Atualizar**. A carga leva cerca de 20 segundos. Para
conferir que a base foi lida inteira, a tabela de regiões da Visão executiva, sem filtro, fecha em
R$ 2.121.440.181,12 de receita líquida, igual ao manifesto.

Se o Desktop avisar que o arquivo foi salvo numa versão mais nova, atualize o Power BI Desktop pela
Microsoft Store ou pelo site da Microsoft.

## Paridade

A paridade prova que a regra escrita no levantamento é a regra que o painel calcula. Os 20
indicadores são calculados de duas formas independentes, pela conta direta nos CSV, em Python e sem
Power BI, e pelo modelo aberto no Desktop, e as duas pontas são cruzadas em nove cortes. O último
resultado está em [`paridade/resultado-2026-10-11.md`](paridade/resultado-2026-10-11.md): **zero
divergência em 167.620 comparações**.

| Arquivo | Papel |
|---|---|
| `medidas.py` | a lista única das medidas, dos cortes e do tipo de cada medida, lida pelos outros três |
| `fonte.py` | calcula os 20 indicadores nos nove cortes direto dos CSV da base |
| `gera_consultas.py` | gera `consultas.dax`, uma consulta por corte contra o modelo |
| `rodar.ps1` | roda as consultas no modelo aberto no Desktop e grava um CSV por corte |
| `comparar.py` | cruza as duas pontas com as tolerâncias e sai com erro se houver divergência |

Tolerâncias: contagem igual, valor em reais até R$ 0,01 e razão até 0,000001. A tolerância existe só
para absorver a ordem de soma em ponto flutuante, e vazio dos dois lados conta como igual.

Com o painel aberto e atualizado no Desktop, a porta local do modelo está no arquivo
`msmdsrv.port.txt` dentro de `%LOCALAPPDATA%\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces\`
(na versão da Microsoft Store, em `%USERPROFILE%\Microsoft\Power BI Desktop Store App\AnalysisServicesWorkspaces\`),
ou no DAX Studio. Os scripts em Python usam o pandas, que já está no ambiente criado no passo 1 para
o gerador. No PowerShell, a partir da pasta `evidencias\paridade`, troque `<gerador>` pela pasta
onde o `port-gerador-dados` foi clonado:

```powershell
<gerador>\.venv\Scripts\python fonte.py C:\dados\painel-comercial\comercial C:\dados\painel-comercial\paridade\base
<gerador>\.venv\Scripts\python gera_consultas.py
powershell -NoProfile -ExecutionPolicy Bypass -File rodar.ps1 -Porta <porta> -Arquivo consultas.dax -Saida C:\dados\painel-comercial\paridade\painel
<gerador>\.venv\Scripts\python comparar.py C:\dados\painel-comercial\paridade\resultado.csv base=C:\dados\painel-comercial\paridade\base painel=C:\dados\painel-comercial\paridade\painel
```

O `-ExecutionPolicy Bypass` vale só para essa execução e evita que a política padrão do Windows
bloqueie o script. O `rodar.ps1` acha sozinho a biblioteca de conexão do Desktop, tanto na instalação
pelo site quanto na da Microsoft Store.

O `fonte.py` leva cerca de 30 segundos e as consultas ao modelo, menos de um minuto. Os resultados
são CSV e ficam fora do git.

## Publicação na web

O painel está pronto para ser publicado, e a publicação ficou para o responsável pelo serviço, porque
ela exige uma conta do Power BI com licença Pro, ou Premium por usuário, num tenant próprio. O
roteiro é este:

1. **Publicar.** Com o painel aberto e atualizado no Desktop, clique em **Página Inicial > Publicar**,
   entre com a conta do tenant próprio e escolha um workspace dedicado aos casos de demonstração. O modelo vai com o
   dado importado, que é o retrato da base na data fixa.
2. **Gerar o link público.** No serviço, abra o relatório e vá em **Arquivo > Inserir relatório >
   Publicar na Web (público)**. A opção precisa estar liberada pelo administrador do tenant em
   **Configurações do locatário > Publicar na Web**. Esse link fica visível para qualquer pessoa na
   internet, e por isso só se publica painel com dado fictício, como este.
3. **Levar o link para o caso.** Copie o link e o código de incorporação, ponha o link na página do
   caso e no perfil profissional, e confira numa janela anônima que o painel abre sem login.

Como a base é lida de arquivos locais, o painel publicado não se atualiza sozinho, e isso é suficiente
para uma demonstração com data fixa. Atualização agendada pediria um gateway ou a troca da fonte pelo
feed diário do gerador, que é trabalho da etapa de solução hospedada. O custo da licença, quando a
publicação for feita, entra declarado na página do caso.

## Limites declarados

- O painel foi validado no Power BI Desktop 2.158. Versões anteriores podem recusar o arquivo.
- A paridade cobre os 20 indicadores de negócio. As medidas de suporte de tela, que só escrevem
  texto para cartão e rodapé, ficam fora dela de propósito, porque não carregam regra de negócio.
- A base é sintética e regular: o desconto, a margem e a frequência de compra seguem as regras do
  gerador, e os padrões que o painel mostra servem para demonstrar o serviço, sem valor de análise.

---

<sub>**B&B** · Matheus Belmonte</sub>
