# executar_lote.ps1 - executa a skill de ponta a ponta, sem pedidos de permissao, a partir da pasta
# de downloads do Helestron. Abre uma sessao do Claude Code ja instruida a trabalhar o lote.
#
# Uso (PowerShell):
#   & "$env:USERPROFILE\.claude\skills\skill-17a-lote-minutas-helestron\scripts\executar_lote.ps1"
#   ... -Pasta 'C:\Users\fulano\Helestron\Downloads' -Lista '0714346-41.2024 0750345-89.2023'
#   ... -Modo lista            (alternativa conservadora: so o que esta na lista de permissoes)
#   ... -SemInteracao          (sem janela de conversa; registra tudo em _Vara17\logs)
#
# Modos:
#   bypass (padrao) - --permission-mode bypassPermissions, valido so para esta sessao (nao altera
#                     o ~/.claude/settings.json). Na primeira vez, o Claude Code pede que o usuario
#                     aceite o aviso do modo; depois, nao pergunta mais nada.
#   lista           - --permission-mode dontAsk + lista de permissoes da skill: o que nao estiver na
#                     lista e negado sem perguntar (a sessao relata o bloqueio e segue).
# Em ambos, um aviso sonoro e visual (avisar.ps1) dispara quando a sessao precisa do usuario: desafio
# de verificacao no navegador, autorizacao de processo sigiloso ou pasta nao localizada.
param(
  [string]$Pasta = '',
  [string]$Transcricoes = '',
  [string]$Lista = '',
  [string]$ListaArquivo = '',
  [ValidateSet('bypass', 'lista')][string]$Modo = 'bypass',
  [switch]$SemInteracao,
  [string]$Instrucao = ''
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$skill = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path -LiteralPath (Join-Path $skill 'SKILL.md'))) { throw "SKILL.md nao encontrado em $skill" }
$claude = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claude) { throw 'Claude Code nao encontrado no PATH. Instale-o (https://code.claude.com) e abra um novo PowerShell.' }

# pasta de trabalho: a pasta de downloads informada; sem ela, a skill descobre pelo Helestron
$dirs = @()
foreach ($p in @($Pasta, $Transcricoes)) {
  if ($p) {
    if (-not (Test-Path -LiteralPath $p -PathType Container)) { throw "Pasta inexistente: $p" }
    $dirs += (Resolve-Path -LiteralPath $p).Path
  }
}
$base = if ($Pasta) { (Resolve-Path -LiteralPath $Pasta).Path } else { Join-Path $env:USERPROFILE 'Documents' }
$trabalho = Join-Path $base '_Vara17'
New-Item -ItemType Directory -Force -Path (Join-Path $trabalho 'logs') | Out-Null

# configuracao da sessao (gancho de aviso e, no modo lista, as permissoes) - arquivo temporario,
# sem tocar nas configuracoes do usuario
$avisar = (Join-Path $PSScriptRoot 'avisar.ps1') -replace '\\', '/'
$cfg = Get-Content -LiteralPath (Join-Path $skill 'config\claude_execucao.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$cfg.hooks.Notification[0].hooks[0].command = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$avisar`""
if ($Modo -ne 'lista') { $cfg.PSObject.Properties.Remove('permissions') }
$cfgArq = Join-Path $trabalho 'logs\claude_sessao.json'
[IO.File]::WriteAllText($cfgArq, ($cfg | ConvertTo-Json -Depth 10), [Text.UTF8Encoding]::new($false))

# instrucao inicial
$numeros = $Lista
if ($ListaArquivo) { $numeros = ($numeros + ' ' + (Get-Content -LiteralPath $ListaArquivo -Raw)).Trim() }
$prompt = 'Use a skill skill-17a-lote-minutas-helestron e execute o lote inteiro, do inventario a entrega das minutas em Word, sem pedir confirmacao.'
if ($Pasta) { $prompt += " Pasta de downloads do Helestron: '$((Resolve-Path -LiteralPath $Pasta).Path)'." }
if ($Transcricoes) { $prompt += " Pasta de transcricoes de audiencias: '$((Resolve-Path -LiteralPath $Transcricoes).Path)'." }
if ($numeros) { $prompt += " Processos, nesta ordem: $numeros." } else { $prompt += ' Sem lista: trabalhe o proximo lote de ate 10 processos da pasta.' }
if ($Instrucao) { $prompt += " $Instrucao" }

$opcoes = @('--permission-mode', $(if ($Modo -eq 'lista') { 'dontAsk' } else { 'bypassPermissions' }), '--settings', $cfgArq)
foreach ($d in $dirs + @($skill)) { $opcoes += @('--add-dir', $d) }

# Python do Helestron para a sessao (a skill o le em HELESTRON_PYTHON; no modo lista, as regras de
# permissao reconhecem a chamada "$HELESTRON_PYTHON" -I ...)
$py = (Get-ItemProperty -LiteralPath 'HKCU:\Software\Helestron' -ErrorAction SilentlyContinue).Python
if (-not ($py -and (Test-Path -LiteralPath $py))) { $py = Join-Path "$env:LOCALAPPDATA" 'Programs\Helestron\python.exe' }
if (Test-Path -LiteralPath $py) { $env:HELESTRON_PYTHON = $py; $prompt += " Python do Helestron: '$py'." }

Set-Location -LiteralPath $base
$log = Join-Path $trabalho ('logs\execucao_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
"[$(Get-Date -Format s)] modo=$Modo pasta=$base`r`n$prompt" | Out-File -LiteralPath $log -Encoding utf8
# a partir daqui, linha na saida de erro do claude nao interrompe o lancador (PowerShell 5.1)
$ErrorActionPreference = 'Continue'
if ($SemInteracao) {
  & $claude.Source -p $prompt @opcoes --output-format text 2>&1 | ForEach-Object { "$_" } |
    Out-File -LiteralPath $log -Append -Encoding utf8
  $codigo = $LASTEXITCODE
  "[$(Get-Date -Format s)] fim, codigo $codigo" | Out-File -LiteralPath $log -Append -Encoding utf8
  exit $codigo
} else {
  & $claude.Source @opcoes $prompt
}
