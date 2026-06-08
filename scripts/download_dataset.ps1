$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$rawDir = Join-Path $root "data\raw"
$zipPath = Join-Path $root "coffee-sales.zip"
New-Item -ItemType Directory -Force -Path $rawDir | Out-Null

Write-Host "Downloading Kaggle dataset: ahmedabbas757/coffee-sales"

try {
    kaggle datasets download -d ahmedabbas757/coffee-sales -p $root --force
}
catch {
    Write-Host "Kaggle CLI is unavailable or not authenticated. Falling back to Kaggle public download endpoint..."
    Invoke-WebRequest `
        -Uri "https://www.kaggle.com/api/v1/datasets/download/ahmedabbas757/coffee-sales" `
        -OutFile $zipPath
}

Expand-Archive -Path $zipPath -DestinationPath $rawDir -Force
Write-Host "Dataset extracted to $rawDir"
Write-Host "Next: python scripts\prepare_data.py"
