param(
    [Parameter(Mandatory = $true)][int]$Porta,
    [Parameter(Mandatory = $true)][string]$Arquivo,
    [Parameter(Mandatory = $true)][string]$Saida
)
# Roda as consultas de paridade de um arquivo .dax contra o modelo aberto no Power BI Desktop e
# grava um CSV por corte em $Saida, no formato que comparar.py le. Os blocos do arquivo comecam
# com a linha "// corte: <nome>". Usa a biblioteca de cliente que vem com o Desktop.
$ErrorActionPreference = 'Stop'
# A biblioteca fica na pasta do Desktop instalado pelo site ou, na versao da Microsoft Store, na
# pasta do pacote em WindowsApps.
$candidatas = @("C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll")
$pacote = Get-AppxPackage -Name Microsoft.MicrosoftPowerBIDesktop -ErrorAction SilentlyContinue | Select-Object -First 1
if ($pacote) { $candidatas += Join-Path $pacote.InstallLocation "bin\Microsoft.PowerBI.AdomdClient.dll" }
$dll = $candidatas | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $dll) { throw 'Microsoft.PowerBI.AdomdClient.dll nao encontrada: confira a instalacao do Power BI Desktop' }
Add-Type -Path $dll
$inv = [Globalization.CultureInfo]::InvariantCulture
New-Item -ItemType Directory -Force -Path $Saida | Out-Null

$texto = [IO.File]::ReadAllText((Resolve-Path $Arquivo), [Text.Encoding]::UTF8)
$blocos = [regex]::Split($texto, '(?m)^(?=// corte: )') | Where-Object { $_ -match '^// corte: ' }

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$Porta")
$conn.Open()
foreach ($b in $blocos) {
    $corte = ([regex]::Match($b, '^// corte: (\S+)')).Groups[1].Value
    $cmd = $conn.CreateCommand(); $cmd.CommandText = $b; $cmd.CommandTimeout = 1800
    $r = $cmd.ExecuteReader()
    $cols = 0..($r.FieldCount - 1) | ForEach-Object { ($r.GetName($_) -replace '^.*\[(.+)\]$', '$1') }
    $linhas = New-Object System.Collections.Generic.List[string]
    $linhas.Add(($cols -join ','))
    while ($r.Read()) {
        $vals = 0..($r.FieldCount - 1) | ForEach-Object {
            $v = $r.GetValue($_)
            if ($v -eq $null -or $v -is [DBNull]) { '' }
            elseif ($v -is [double] -or $v -is [decimal] -or $v -is [single]) { ([double]$v).ToString('R', $inv) }
            else { '"' + ([string]::Format($inv, '{0}', $v) -replace '"', '""') + '"' }
        }
        $linhas.Add(($vals -join ','))
    }
    $r.Close()
    [IO.File]::WriteAllLines((Join-Path $Saida "$corte.csv"), $linhas, (New-Object Text.UTF8Encoding($false)))
    "{0}: {1} linhas" -f $corte, ($linhas.Count - 1)
}
$conn.Close()
