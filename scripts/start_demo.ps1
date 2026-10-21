param([switch]$NoTunnel)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$runDir = Join-Path $root '.demo-run'
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

function Get-ContainerConfig([string]$name) {
  $raw = docker inspect $name 2>$null
  if ($LASTEXITCODE -ne 0) { throw "Required Docker container '$name' was not found." }
  return ($raw | ConvertFrom-Json)[0]
}
function Get-ContainerEnv([string[]]$items, [string]$name) {
  $entry = $items | Where-Object { $_.StartsWith("$name=") } | Select-Object -First 1
  if (-not $entry) { throw "Required container environment variable '$name' is missing." }
  return $entry.Substring($name.Length + 1)
}
function Start-HiddenProcess([string]$file, [string]$arguments, [string]$directory, [string]$log) {
  $err = "$log.err"
  $proc = Start-Process -FilePath $file -ArgumentList $arguments -WorkingDirectory $directory -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError $err -PassThru
  Set-Content -Path "$log.pid" -Value $proc.Id -NoNewline
  return $proc
}

$mongo = Get-ContainerConfig 'saigon-zoo-t10-replset'
$seaweed = Get-ContainerConfig 'saigon-zoo-t10-seaweedfs'
$redis = Get-ContainerConfig 'saigon-zoo-redis'
if ($mongo.State.Status -ne 'running' -or $seaweed.State.Status -ne 'running' -or $redis.State.Status -ne 'running') { throw 'MongoDB, SeaweedFS and Redis containers must be running.' }
$seaweedEnv = @($seaweed.Config.Env)
$env:MONGODB_URI = 'mongodb://127.0.0.1:27018/?replicaSet=rs0'
$env:MONGODB_DATABASE = 'saigon_zoo_tcv_dataset_dev'
$env:REDIS_URL = 'redis://127.0.0.1:6379/0'
$env:AUDIO_STORAGE_ENDPOINT_URL = 'http://127.0.0.1:8333'
$env:AUDIO_STORAGE_BUCKET = Get-ContainerEnv $seaweedEnv 'S3_BUCKET'
$env:AUDIO_STORAGE_ACCESS_KEY_ID = Get-ContainerEnv $seaweedEnv 'AWS_ACCESS_KEY_ID'
$env:AUDIO_STORAGE_SECRET_ACCESS_KEY = Get-ContainerEnv $seaweedEnv 'AWS_SECRET_ACCESS_KEY'
$env:AUDIO_STORAGE_REGION = 'us-east-1'
$env:ADMIN_COOKIE_SECURE = if ($NoTunnel) { 'false' } else { 'true' }
& (Join-Path $PSScriptRoot 'check_storage_access.ps1')
if ($LASTEXITCODE -ne 0) { throw 'SeaweedFS S3 preflight failed.' }

$backendPidPath = Join-Path $runDir 'backend.out.log.pid'
if (Test-Path $backendPidPath) {
  $existing = Get-Process -Id (Get-Content $backendPidPath) -ErrorAction SilentlyContinue
  if ($existing) {
    $command = (Get-CimInstance Win32_Process -Filter "ProcessId = $($existing.Id)").CommandLine
    if ($command -notlike "*$root*" -or $command -notmatch 'uvicorn backend.main:app') { Remove-Item -LiteralPath $backendPidPath }
  } else { Remove-Item -LiteralPath $backendPidPath }
}
if (-not (Test-Path $backendPidPath)) {
  Start-HiddenProcess (Join-Path $root '.venv\Scripts\python.exe') '-m uvicorn backend.main:app --host 127.0.0.1 --port 8000' $root (Join-Path $runDir 'backend.out.log') | Out-Null
}
$frontendPidPath = Join-Path $runDir 'frontend.out.log.pid'
if (Test-Path $frontendPidPath) {
  $frontendPid = [int](Get-Content $frontendPidPath)
  $existing = Get-Process -Id $frontendPid -ErrorAction SilentlyContinue
  if ($existing) {
    $frontendCommand = (Get-CimInstance Win32_Process -Filter "ProcessId = $frontendPid").CommandLine
    if ($frontendCommand -notlike "*$root*" -or $frontendCommand -notmatch 'vite\.js"?\s+preview') {
      Remove-Item $frontendPidPath
    }
  } else { Remove-Item $frontendPidPath }
}
if (-not (Test-Path $frontendPidPath)) {
  $nodeExe = (Get-Command node -ErrorAction Stop).Source
  Push-Location (Join-Path $root 'frontend')
  try {
    npm run build
    if ($LASTEXITCODE -ne 0) { throw 'Frontend production build failed.' }
  } finally { Pop-Location }
  Start-HiddenProcess $nodeExe ('"' + (Join-Path $root 'frontend\node_modules\vite\bin\vite.js') + '" preview --host 0.0.0.0 --port 3000') (Join-Path $root 'frontend') (Join-Path $runDir 'frontend.out.log') | Out-Null
}

$healthy = $false
for ($i = 0; $i -lt 40; $i++) {
  try { Invoke-RestMethod 'http://127.0.0.1:8000/health' -TimeoutSec 2 | Out-Null; $healthy = $true; break } catch { Start-Sleep -Milliseconds 750 }
}
if (-not $healthy) { throw "Backend did not become healthy; inspect $runDir\backend.out.log and .err." }
try { Invoke-WebRequest 'http://127.0.0.1:3000/' -TimeoutSec 4 | Out-Null } catch { throw "Frontend did not become available; inspect $runDir\frontend.out.log and .err." }

if ($NoTunnel) { Write-Output 'Demo services are running at http://localhost:3000'; exit 0 }
$dockerCli = (Get-Command docker -ErrorAction Stop).Source
$existingTunnel = docker ps -a --filter 'name=^/saigon-zoo-demo-tunnel$' --format '{{.Names}}'
if ($existingTunnel -contains 'saigon-zoo-demo-tunnel') { docker stop saigon-zoo-demo-tunnel | Out-Null }
$tunnelLog = Join-Path $runDir 'tunnel.out.log'
$tunnelArgs = 'run --rm --pull=missing --name saigon-zoo-demo-tunnel cloudflare/cloudflared:latest tunnel --no-autoupdate --url http://host.docker.internal:3000'
$tunnel = Start-HiddenProcess $dockerCli $tunnelArgs $root $tunnelLog
$publicUrl = $null
for ($i = 0; $i -lt 70; $i++) {
  $logs = @()
  foreach ($path in @($tunnelLog, "$tunnelLog.err")) { if (Test-Path $path) { $logs += Get-Content $path -Raw } }
  $match = [regex]::Match(($logs -join "`n"), 'https://[a-z0-9-]+\.trycloudflare\.com')
  if ($match.Success) { $publicUrl = $match.Value; break }
  if ($tunnel.HasExited) { break }
  Start-Sleep -Milliseconds 500
}
if (-not $publicUrl) { throw "HTTPS tunnel did not provide a URL; inspect $tunnelLog and .err." }
$qrPath = Join-Path $runDir 'phone-demo-qr.png'
node (Join-Path $PSScriptRoot 'write_demo_qr.mjs') $publicUrl $qrPath
Set-Content -Path (Join-Path $runDir 'phone-demo-url.txt') -Value $publicUrl -NoNewline
Write-Output "Phone URL: $publicUrl"
Write-Output "Scan code: $qrPath"
Write-Output 'Admin: open /admin. Bootstrap an account with python -m scripts.create_admin if none exists.'
