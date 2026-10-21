$ErrorActionPreference = 'Stop'
$cfg = (docker inspect saigon-zoo-t10-seaweedfs | ConvertFrom-Json)[0]
$values = @{}
foreach ($entry in $cfg.Config.Env) {
  if ($entry -match '^(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|S3_BUCKET)=(.*)$') { $values[$Matches[1]] = $Matches[2] }
}
$env:AUDIO_STORAGE_ENDPOINT_URL = 'http://127.0.0.1:8333'
$env:AUDIO_STORAGE_BUCKET = $values['S3_BUCKET']
$env:AUDIO_STORAGE_ACCESS_KEY_ID = $values['AWS_ACCESS_KEY_ID']
$env:AUDIO_STORAGE_SECRET_ACCESS_KEY = $values['AWS_SECRET_ACCESS_KEY']
$env:AUDIO_STORAGE_REGION = 'us-east-1'
& (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..')).Path '.venv\Scripts\python.exe') (Join-Path $PSScriptRoot 'check_storage_access.py')
