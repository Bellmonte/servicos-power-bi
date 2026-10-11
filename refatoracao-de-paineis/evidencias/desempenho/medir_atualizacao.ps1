param(
    [Parameter(Mandatory = $true)][int]$Porta,
    [int]$Runs = 6,
    [string]$Ponta = '',
    [string]$Sessao = '',
    [string]$Saida = ''
)
# Cronometra a atualizacao completa do modelo aberto no Power BI Desktop, enviando o mesmo comando
# do botao Atualizar pela biblioteca de cliente do Desktop. A execucao 0 e o aquecimento e fica
# fora do registro. Com -Saida, as execucoes 1 em diante viram linhas tempo_atualizacao em
# segundos no CSV da secao 5 da especificacao.
Add-Type -Path "C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll"
$inv = [Globalization.CultureInfo]::InvariantCulture
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$Porta")
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT [CATALOG_NAME] FROM `$SYSTEM.DBSCHEMA_CATALOGS"
$r = $cmd.ExecuteReader(); $null = $r.Read(); $db = $r.GetString(0); $r.Close()
"database=$db"
$tmsl = '{"refresh":{"type":"full","objects":[{"database":"' + $db + '"}]}}'
$out = New-Object System.Collections.Generic.List[string]
if ($Saida -and -not (Test-Path $Saida)) { $out.Add('sessao,ponta,grandeza,estado,cache,repeticao,valor,unidade') }
for ($i = 0; $i -lt $Runs; $i++) {
    $c = $conn.CreateCommand(); $c.CommandText = $tmsl; $c.CommandTimeout = 1800
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $null = $c.ExecuteNonQuery()
    $sw.Stop()
    $s = [math]::Round($sw.Elapsed.TotalSeconds, 2)
    "{0};{1}" -f $i, $s
    if ($i -gt 0) { $out.Add(('{0},{1},tempo_atualizacao,na,quente,{2},{3},s' -f $Sessao, $Ponta, $i, $s.ToString($inv))) }
}
$conn.Close()
if ($Saida) { [IO.File]::AppendAllLines($Saida, $out, (New-Object Text.UTF8Encoding($false))) }
