# Paridade entre o painel de partida (v1) e o reestruturado (v2)

Aqui estão as ferramentas do protocolo de paridade da seção 6 da
[metodologia](../metodologia.md). Elas conferem as 16 medidas da seção 4 em nove cortes (total,
ano-mês, região, categoria, porte, vendedor, cliente, ano-mês por região e estado B) e cruzam três
pontas: a fonte, que é a conta feita direto nos CSV do gerador, a v1 e a v2.

| Arquivo | Papel |
|---|---|
| `gera_consultas.py` | gera `consultas_v1.dax` e `consultas_v2.dax`, com as mesmas colunas de saída nas duas pontas |
| `consultas_v1.dax`, `consultas_v2.dax` | uma consulta por corte, cada uma começando com `// corte: <nome>` |
| `rodar.ps1` | roda um desses arquivos contra o modelo aberto no Desktop e grava um CSV por corte |
| `fonte.py` | calcula os mesmos cortes direto da base, sem Power BI |
| `comparar.py` | cruza as pontas com as tolerâncias da seção 6 e sai com erro se houver divergência |

Na v1, o que o visual mostrava como soma automática vira uma medida local da consulta, com a
mesma conta. A margem da v1 é a soma da coluna `Lucro`, como no painel.

## Como rodar

A porta do modelo aberto no Desktop aparece no DAX Studio ou no `medir_atualizacao.ps1`. Os
resultados são CSV e ficam fora do git, numa pasta local.

```powershell
python fonte.py <pasta-comercial-da-base> <local>\fonte
.\rodar.ps1 -Porta <porta-da-v1> -Arquivo consultas_v1.dax -Saida <local>\v1
.\rodar.ps1 -Porta <porta-da-v2> -Arquivo consultas_v2.dax -Saida <local>\v2
python comparar.py <local>\resultado.csv fonte=<local>\fonte v1=<local>\v1 v2=<local>\v2
```

Quem preferir rodar as consultas por outra ferramenta pode salvar cada resultado como
`<corte>.csv` ou `<corte>.json` numa pasta por ponta. O `comparar.py` aceita os dois formatos e
normaliza nomes de coluna com colchete.

Tolerâncias: contagem igual, valor em reais até R$ 0,01 e razão até 0,000001. A diferença de
tolerância absorve só a ordem de soma em ponto flutuante; divergência acima disso é investigada.
