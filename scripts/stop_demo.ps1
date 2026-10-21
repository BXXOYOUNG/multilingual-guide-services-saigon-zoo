$ErrorActionPreference = 'Continue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$runDir = Join-Path $root '.demo-run'
foreach ($name in @('tunnel.out.log', 'frontend.out.log', 'backend.out.log')) {
  $pidFile = Join-Path $runDir "$name.pid"
  if (Test-Path $pidFile) {
    $processId = [int](Get-Content $pidFile)
    $command = (Get-CimInstance Win32_Process -Filter "ProcessId = $processId" -ErrorAction SilentlyContinue).CommandLine
    if ($command -like "*$root*" -and $command -match 'uvicorn backend.main:app|vite[\\/]bin[\\/]vite.js|vite\.js preview') {
      taskkill /PID $processId /T /F 2>$null | Out-Null
    }
    Remove-Item -LiteralPath $pidFile -Force
  }
}
docker stop saigon-zoo-demo-tunnel 2>$null | Out-Null
Write-Output 'Demo processes stopped. Docker database/storage containers were left running.'
