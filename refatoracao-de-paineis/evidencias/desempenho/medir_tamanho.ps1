param(
    [Parameter(Mandatory = $true)][int]$Porta,
    [Parameter(Mandatory = $true)][string]$Ponta,
    [Parameter(Mandatory = $true)][string]$Sessao,
    [string]$Saida = (Join-Path $PSScriptRoot 'resultados.csv')
)
# Le o tamanho do modelo aberto no Power BI Desktop direto do motor, pelas mesmas visoes que o
# VertiPaq Analyzer usa: dicionario das colunas (INFO.STORAGETABLECOLUMNS) mais dados e estruturas
# de indice, de hierarquia e de relacao (INFO.STORAGETABLECOLUMNSEGMENTS). Faz duas leituras, e a
# segunda so vale depois de uma nova atualizacao completa (secao 5 da especificacao).
# Grava uma linha em $Saida com grandeza tamanho_modelo, em bytes.
$ErrorActionPreference = 'Stop'
Add-Type -Path "C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll"

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$Porta")
$conn.Open()

function Somar([string]$dax, [string]$coluna) {
    $c = $conn.CreateCommand(); $c.CommandText = $dax; $c.CommandTimeout = 600
    $r = $c.ExecuteReader()
    $i = 0..($r.FieldCount - 1) | Where-Object { ($r.GetName($_) -replace '^.*\[(.+)\]$', '$1') -eq $coluna }
    if ($null -eq $i) { throw "coluna $coluna nao encontrada em $dax" }
    [long]$soma = 0
    while ($r.Read()) { if (-not $r.IsDBNull($i)) { $soma += [long]$r.GetValue($i) } }
    $r.Close()
    return $soma
}

$dicionario = Somar 'EVALUATE INFO.STORAGETABLECOLUMNS()' 'DICTIONARY_SIZE'
$segmentos = Somar 'EVALUATE INFO.STORAGETABLECOLUMNSEGMENTS()' 'USED_SIZE'
$conn.Close()
$total = $dicionario + $segmentos

$novo = -not (Test-Path $Saida)
$out = New-Object System.Collections.Generic.List[string]
if ($novo) { $out.Add('sessao,ponta,grandeza,estado,cache,repeticao,valor,unidade') }
$rep = 1
if (-not $novo) {
    $rep = 1 + @(Get-Content $Saida | Where-Object { $_ -like "$Sessao,$Ponta,tamanho_modelo,*" }).Count
}
$out.Add(('{0},{1},tamanho_modelo,na,na,{2},{3},bytes' -f $Sessao, $Ponta, $rep, $total))
[IO.File]::AppendAllLines($Saida, $out, (New-Object Text.UTF8Encoding($false)))

"{0} leitura {1}: dicionario {2:N0} + segmentos {3:N0} = {4:N0} bytes ({5:N1} MB)" -f `
    $Ponta, $rep, $dicionario, $segmentos, $total, ($total / 1MB)
