$env:MONGODB_URI = 'mongodb://127.0.0.1:27018/?replicaSet=rs0'
$env:MONGODB_DATABASE = 'saigon_zoo_tcv_dataset_dev'
& (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..')).Path '.venv\Scripts\python.exe') (Join-Path $PSScriptRoot 'check_admin_state.py')
