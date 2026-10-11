param(
    [Parameter(Mandatory = $true)][int]$Porta,
    [Parameter(Mandatory = $true)][string]$Arquivo,
    [Parameter(Mandatory = $true)][string]$Saida,
    [int]$N = 5,
    [string]$Ponta = '',
    [string]$Pagina = ''
)
# Mede o tempo das consultas DAX de uma pagina contra o modelo aberto no Power BI Desktop.
# Cada bloco do arquivo comeca com a linha "// consulta: <nome>" (ver extrai_consultas.py).
# Para cada consulta: N execucoes a frio, com ClearCache por XMLA imediatamente antes de cada uma,
# e depois uma de aquecimento descartada e N a quente. O tempo vai do envio ate a ultima linha lida.
# Cada execucao vira uma linha em $Saida (CSV, acrescenta se o arquivo ja existir).
$ErrorActionPreference = 'Stop'
Add-Type -Path "C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll"
$inv = [Globalization.CultureInfo]::InvariantCulture

$texto = [IO.File]::ReadAllText((Resolve-Path $Arquivo), [Text.Encoding]::UTF8)
$blocos = [regex]::Split($texto, '(?m)^(?=// consulta: )') | Where-Object { $_ -match '^// consulta: ' }
if (-not $Pagina) { $Pagina = [IO.Path]::GetFileNameWithoutExtension($Arquivo) }

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$Porta")
$conn.Open()
$c0 = $conn.CreateCommand(); $c0.CommandText = "SELECT [CATALOG_NAME] FROM `$SYSTEM.DBSCHEMA_CATALOGS"
$r0 = $c0.ExecuteReader(); $null = $r0.Read(); $db = $r0.GetString(0); $r0.Close()
# No Power BI Desktop o ID do banco e o proprio nome do catalogo.
$xmla = '<ClearCache xmlns="http://schemas.microsoft.com/analysisservices/2003/engine"><Object><DatabaseID>' + $db + '</DatabaseID></Object></ClearCache>'

function Limpar-Cache { $c = $conn.CreateCommand(); $c.CommandText = $xmla; $null = $c.ExecuteNonQuery() }
function Executar([string]$dax) {
    $c = $conn.CreateCommand(); $c.CommandText = $dax; $c.CommandTimeout = 1800
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $r = $c.ExecuteReader(); $linhas = 0
    while ($r.Read()) { $linhas++ }
    $r.Close(); $sw.Stop()
    return @($sw.Elapsed.TotalMilliseconds, $linhas)
}

$sessao = (Get-Date).ToString('yyyy-MM-ddTHH:mm:ss')
$novo = -not (Test-Path $Saida)
$out = New-Object System.Collections.Generic.List[string]
if ($novo) { $out.Add('sessao,ponta,pagina,consulta,cache,repeticao,ms,linhas') }
$resumo = @{}
foreach ($b in $blocos) {
    $nome = ([regex]::Match($b, '^// consulta: (\S+)')).Groups[1].Value
    foreach ($cache in 'frio', 'quente') {
        if ($cache -eq 'quente') { $null = Executar $b }
        $tempos = @()
        for ($i = 1; $i -le $N; $i++) {
            if ($cache -eq 'frio') { Limpar-Cache }
            $t = Executar $b
            $tempos += $t[0]
            $out.Add(('{0},{1},{2},{3},{4},{5},{6},{7}' -f $sessao, $Ponta, $Pagina, $nome, $cache, $i, $t[0].ToString('0.0', $inv), $t[1]))
        }
        $ord = $tempos | Sort-Object
        $resumo["$nome|$cache"] = $ord[[int][math]::Floor(($ord.Count - 1) / 2)]
    }
}
$conn.Close()
[IO.File]::AppendAllLines($Saida, $out, (New-Object Text.UTF8Encoding($false)))

"pagina $Pagina, $($blocos.Count) consultas, N=$N, banco $db"
foreach ($cache in 'frio', 'quente') {
    $soma = 0
    foreach ($b in $blocos) { $nome = ([regex]::Match($b, '^// consulta: (\S+)')).Groups[1].Value; $soma += $resumo["$nome|$cache"] }
    "  {0}: soma das medianas {1} ms" -f $cache, $soma.ToString('0.0', $inv)
}
