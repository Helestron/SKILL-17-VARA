# avisar.ps1 - aviso sonoro e visual quando a sessao do Claude precisa do usuario
# (gancho "Notification" do Claude Code, configurado por executar_lote.ps1).
# Le do stdin o JSON do gancho (campos message, title, notification_type) e mostra um balao na
# bandeja do Windows, com tres bipes. Nao bloqueia: o balao some sozinho em 10 segundos.
# Casos tipicos: desafio de verificacao (CAPTCHA) aberto no navegador, autorizacao de processo
# sigiloso, pasta do Helestron nao localizada.
$ErrorActionPreference = 'SilentlyContinue'
$entrada = [Console]::In.ReadToEnd()
$msg = 'A sessão de minutas da 17ª Vara precisa de você.'
try {
  $j = $entrada | ConvertFrom-Json
  if ($j.message) { $msg = [string]$j.message }
} catch { }
try { [console]::beep(880, 220); [console]::beep(988, 220); [console]::beep(1175, 380) } catch { }
if ($env:OS -eq 'Windows_NT') {
  try {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    $icones = 'System.Drawing.SystemIcons' -as [type]
    $n = New-Object System.Windows.Forms.NotifyIcon
    if ($icones) { $n.Icon = $icones::Information }
    $n.BalloonTipTitle = 'Minutas - 17ª Vara Cível'
    $n.BalloonTipText = $msg.Substring(0, [Math]::Min(240, $msg.Length))
    $n.Visible = $true
    $n.ShowBalloonTip(10000)
    Start-Sleep -Seconds 10
    $n.Dispose()
  } catch { }
}
exit 0
