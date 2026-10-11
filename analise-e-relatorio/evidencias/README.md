# Guia técnico: análise da política de desconto

Este guia reúne o método, a prova de que o critério veio antes do resultado e o passo a passo para
refazer a análise numa máquina limpa. A [página do caso](../README.md) traz o resumo para quem
decide, o [relatório](../relatorio.md) traz a resposta completa, e aqui está o detalhe para quem
audita ou quer reproduzir.

> **Dados 100% fictícios.** A base é gerada pelo
> [`port-gerador-dados`](https://github.com/Bellmonte/port-gerador-dados), sem vínculo com
> organização ou pessoa real.

O trabalho está na **etapa 1** da régua de entrega, com a análise rodando na máquina de quem
contrata e nada hospedado.

## Como subir na sua máquina

Pré-requisitos: Python 3.14, que é a versão em que as dependências foram fixadas e testadas, e Git.
A base ocupa cerca de 120 MB em disco, e a análise inteira roda em menos de um minuto numa máquina
de mesa comum. Os comandos abaixo são do PowerShell, no Windows. Use uma pasta de trabalho de
caminho curto, como `C:\projetos`, porque o Windows limita o caminho de arquivo a 260 caracteres e
a criação do ambiente falha com erro pouco claro quando a pasta é muito funda.

**1. Clonar os dois repositórios lado a lado.** O gerador produz a base, e este repositório traz a
análise. O gerador recebe um commit novo de dado todo dia, e o `checkout` fixa o código na versão
usada no caso, para a base sair igual mesmo que o gerador mude depois.

```powershell
git clone https://github.com/Bellmonte/port-gerador-dados.git
git -C port-gerador-dados checkout a35d495
git clone https://github.com/Bellmonte/bb-servicos-power-bi.git servicos
```

**2. Criar o ambiente da análise.** Um ambiente só serve para gerar a base e para executar o
notebook, porque o `requirements.txt` já inclui as dependências do gerador nas mesmas versões.

```powershell
cd servicos\analise-e-relatorio
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

**3. Gerar a base com data fixa.** O mesmo comando gera os mesmos arquivos em qualquer máquina e
em qualquer dia.

```powershell
.venv\Scripts\python ..\..\port-gerador-dados\gerar.py comercial --hoje 2026-08-31 --meses 36 --linhas 1000000 --clientes 20000 --produtos 1500 --vendedores 150 --colunas-origem --saida C:\dados\analise-relatorio
```

Os arquivos saem em `C:\dados\analise-relatorio\comercial\`, junto do `_manifesto.json`. Para usar
outra pasta, troque o `--saida` e aponte a variável de ambiente `BASE_ANALISE` para a subpasta
`comercial` antes do passo 4, por exemplo `$env:BASE_ANALISE = "D:\outra\comercial"`.

**4. Executar o notebook de ponta a ponta.**

```powershell
.venv\Scripts\python -m nbconvert --to notebook --execute --inplace analise.ipynb
```

A execução regrava os quatro gráficos em `imagens/`, os números em `evidencias/resultados.json` e
as saídas do próprio notebook, que por isso aparece como alterado no Git mesmo quando os números
são os mesmos.
Logo depois dos parâmetros, a célula C03 confere a base pelo manifesto e para com erro se ela
não for a do comando acima.

**5. Conferir que o relatório bate com o notebook.**

```powershell
.venv\Scripts\python evidencias\conferir_relatorio.py
```

O script lê cada parágrafo do relatório, as células que ele cita entre colchetes e os números que
essas células gravaram, e termina com erro se algum número do texto não tiver origem. A saída
esperada termina em `0 problemas`.

Para abrir o notebook no navegador e ler célula por célula, instale também o JupyterLab no mesmo
ambiente (`.venv\Scripts\pip install jupyterlab`) e rode `.venv\Scripts\jupyter lab`. No Linux e no
Mac, troque `.venv\Scripts\` por `.venv/bin/` e use um caminho de pasta do sistema.

## Execução conferida do zero

Em 11-10-2026 uma execução independente seguiu só este guia, numa pasta nova e sem ambiente, base,
gráficos nem `resultados.json`: Python 3.14.4 no Windows 11, gerador clonado do GitHub, ambiente
criado do zero. A criação do ambiente levou 49 segundos, a geração da base 7, a execução do
notebook 15 e a conferência menos de um. O notebook rodou sem erro, os quatro gráficos e o
`resultados.json` saíram idênticos byte a byte aos publicados, e a conferência terminou com
`0 problemas`. A única falha foi a do caminho longo descrita nos pré-requisitos, resolvida com uma
pasta de caminho curto. Linux e Mac não foram testados.

## O que garante que o critério veio antes

O [enquadramento](enquadramento.md) traz a pergunta, as duas linhas de base, o ponto de
equilíbrio e a tabela de decisão, escritos antes da primeira execução do notebook. O adendo do
mesmo arquivo registra as correções do desenho, também anteriores à execução, e declara a
resposta que o gerador implica. O hash do arquivo nesse momento está em [decisões](decisoes.md),
junto do registro do que já se sabia antes.

## Método

| Etapa | O que foi feito | Célula |
|---|---|---|
| parâmetros e apoio | todo parâmetro numa célula, e as funções de registro e de formato em outra | C01, C02 |
| conferir a base | parâmetros e somas de controle contra o manifesto | C03, C05 |
| perfilar | grão, classificação, distribuição, centro, domínio e média ponderada, pelo roteiro de perfilamento | C07 a C14 |
| linhas de base | política atual nos últimos 12 meses e leitura simples por faixa de desconto | C16, C17 |
| ponto de equilíbrio | efeito que zeraria o ganho do teto, pela mesma função que calcula o ganho | C20 |
| efeito principal | Poisson da quantidade sobre o desconto, só clientes grandes, erro agrupado por cliente e vendedor | C23 |
| robustez | logaritmo da quantidade, efeitos fixos de produto, vendedor e mês | C23 |
| leitura simples corrigida | inclinação sem e com efeito fixo de porte, na carteira inteira | C24 |
| diagnóstico | quantidade prevista contra observada em cada faixa de desconto | C25 |
| confirmação | mesma especificação nos 12 meses seguintes | C26 |
| decisão | tabela do critério, com a regra de concordância | C27 |
| ganho do teto e robustez | ganho sem perda de volume, e a perda de volume ou a saída de clientes que o zeraria | C30 |
| sensibilidade do ganho | o ganho com o pior efeito plausível do desconto e com saída de 1%, 2% e 3% da margem do porte; o ganho é conta sobre todos os clientes, sem faixa amostral | C31 |
| exposição e tetos alternativos | concentração do ganho por conta, e tetos de 12% e 14% | C32, C33 |
| piloto | sorteio dentro de cada vendedor principal, com semente 42, e poder do teste de não inferioridade na saída de clientes e no volume por cliente, em 12 meses | C35 |

Os roteiros de método seguidos estão listados no fim do enquadramento. O [perfilamento](perfilamento.md)
resume o estado da base e as decisões sobre o que foi encontrado. O parecer da revisão do
notebook está em [`parecer-revisor-notebook.md`](parecer-revisor-notebook.md).

## O que tem aqui

| Caminho | O que é |
|---|---|
| [`../analise.ipynb`](../analise.ipynb) | o notebook, que roda do zero |
| [`../relatorio.md`](../relatorio.md) e `../relatorio.pdf` | o relatório de entrega, em markdown e em PDF |
| [`../requirements.txt`](../requirements.txt) | dependências com versão |
| [`enquadramento.md`](enquadramento.md) | pergunta, linhas de base e critério, escritos antes do resultado |
| [`decisoes.md`](decisoes.md) | por que esta pergunta, o hash do enquadramento e as decisões de método |
| [`perfilamento.md`](perfilamento.md) | o estado da base e o que foi decidido sobre ele |
| [`resultados.json`](resultados.json) | cada número do relatório, com a célula que o gerou |
| [`conferir_relatorio.py`](conferir_relatorio.py) | a conferência automática entre relatório e notebook |
| [`parecer-revisor-notebook.md`](parecer-revisor-notebook.md) | a revisão do notebook contra o padrão de código |

## Custo

Zero. O gerador, o Python e as bibliotecas são gratuitos, e nada fica hospedado. A geração da base
leva cerca de 6 segundos e a execução do notebook cerca de 20, medidos numa máquina de mesa com
Windows 11.

## Licença

MIT. O dado é fictício e serve de exemplo.

---

<sub>**B&B** · Matheus Belmonte</sub>
