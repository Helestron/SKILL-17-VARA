# instalar.ps1 - instala (ou atualiza) a skill no Claude Code do Windows e cria o atalho de execucao.
#
# Uso: extraia o .zip da skill, abra o PowerShell e rode
#   & '<pasta extraida>\skill-17a-lote-minutas-helestron\scripts\instalar.ps1' [-Pasta '<downloads do Helestron>'] [-SemAtalho]
#
# O que faz:
#   1. copia a skill para %USERPROFILE%\.claude\skills\skill-17a-lote-minutas-helestron; a versao
#      anterior, se houver, e renomeada para ...-anterior-<data> (nada e apagado);
#   2. confere o Python do Helestron e roda o diagnostico da pasta de downloads e de transcricoes;
#   3. cria na Area de Trabalho o atalho "Minutas 17a Vara" (executar_lote.ps1, modo sem permissoes).
# Nao altera o ~/.claude/settings.json: o modo sem permissoes vale so nas sessoes abertas pelo atalho.
param([string]$Pasta = '', [switch]$SemAtalho)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$nome = 'skill-17a-lote-minutas-helestron'
$origem = Split-Path -Parent $PSScriptRoot
$destRaiz = Join-Path $env:USERPROFILE '.claude\skills'
$destino = Join-Path $destRaiz $nome
New-Item -ItemType Directory -Force -Path $destRaiz | Out-Null

if ((Resolve-Path -LiteralPath $origem).Path -ne $destino) {
  if (Test-Path -LiteralPath $destino) {
    $anterior = "$destino-anterior-" + (Get-Date -Format 'yyyyMMdd-HHmmss')
    Rename-Item -LiteralPath $destino -NewName (Split-Path -Leaf $anterior)
    Write-Host "Versao anterior preservada em: $anterior"
  }
  Copy-Item -LiteralPath $origem -Destination $destino -Recurse
  Write-Host "Skill instalada em: $destino"
} else {
  Write-Host "Skill ja esta na pasta de skills: $destino"
}

# Python: o do Helestron (preferido) ou o do sistema
$py = (Get-ItemProperty -LiteralPath 'HKCU:\Software\Helestron' -ErrorAction SilentlyContinue).Python
if (-not ($py -and (Test-Path -LiteralPath $py))) { $py = Join-Path $env:LOCALAPPDATA 'Programs\Helestron\python.exe' }
if (-not (Test-Path -LiteralPath $py)) {
  $sys = Get-Command python -ErrorAction SilentlyContinue
  $py = if ($sys) { $sys.Source } else { $null }
}
if ($py) {
  Write-Host "Python: $py"
  $diag = @('-I', (Join-Path $destino 'scripts\ponte_helestron.py'), 'diagnostico')
  if ($Pasta) { $diag += @('--downloads', $Pasta) }
  & $py @diag
} else {
  Write-Warning 'Python nao encontrado (nem o do Helestron). Instale o Helestron 1.0.2 ou superior.'
}

if (-not $SemAtalho) {
  $desk = [Environment]::GetFolderPath('Desktop')
  $lnk = Join-Path $desk 'Minutas 17a Vara.lnk'
  $ws = New-Object -ComObject WScript.Shell
  $s = $ws.CreateShortcut($lnk)
  $s.TargetPath = (Get-Command powershell).Source
  $argsAtalho = "-NoExit -NoProfile -ExecutionPolicy Bypass -File `"$(Join-Path $destino 'scripts\executar_lote.ps1')`""
  if ($Pasta) { $argsAtalho += " -Pasta `"$Pasta`"" }
  $s.Arguments = $argsAtalho
  $s.WorkingDirectory = $destino
  $s.Description = 'Minutas da 17a Vara Civel da Capital a partir da pasta do Helestron'
  $s.Save()
  Write-Host "Atalho criado: $lnk"
}
Write-Host ''
Write-Host 'Primeiro uso: abra o atalho e aceite, uma unica vez, o aviso do modo sem permissoes do Claude Code.'
