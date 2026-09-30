<#
.SYNOPSIS
    Mengunduh dataset untuk penelitian Hierarchy-Aware Conformal Risk Control.

.DESCRIPTION
    Mengunduh dataset PhysioNet secara bertahap sesuai prioritas.
    Mendukung resume (curl -C -), sehingga aman dihentikan dan dilanjutkan.
    Spesifikasi dan hasil verifikasi setiap dataset: docs/dataset-verification.md

.PARAMETER Priority
    P0 = PTB-XL + MIT-BIH (~1,78 GB)  -- wajib untuk studi kelayakan
    P1 = P0 + NSTDB (~1,85 GB)        -- default
    P2 = P1 + Challenge 2021 selektif (~3-5 GB, butuh AWS CLI atau wget)

.PARAMETER DataDir
    Direktori tujuan. Default: data\raw relatif terhadap root repositori.

.PARAMETER SkipExtract
    Hanya unduh ZIP, jangan diekstraksi.

.EXAMPLE
    .\scripts\download_data.ps1
    .\scripts\download_data.ps1 -Priority P0
    .\scripts\download_data.ps1 -Priority P2 -DataDir D:\datasets
#>

[CmdletBinding()]
param(
    [ValidateSet('P0', 'P1', 'P2')]
    [string]$Priority = 'P1',

    [string]$DataDir,

    [switch]$SkipExtract
)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------- konfigurasi

if (-not $DataDir) {
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $DataDir = Join-Path $repoRoot 'data\raw'
}

# Ukuran dan URL dikutip dari halaman resmi PhysioNet per 2026-09-29.
$Datasets = @(
    [pscustomobject]@{
        Id       = 'D1'; Key = 'ptbxl'; Priority = 'P0'
        Name     = 'PTB-XL v1.0.3'
        Url      = 'https://physionet.org/content/ptb-xl/get-zip/1.0.3/'
        S3       = 's3://physionet-open/ptb-xl/1.0.3/'
        SizeNote = '1,7 GB zip / 3,0 GB extracted'
        Marker   = 'ptbxl_database.csv'
    },
    [pscustomobject]@{
        Id       = 'D2'; Key = 'mitdb'; Priority = 'P0'
        Name     = 'MIT-BIH Arrhythmia v1.0.0'
        Url      = 'https://physionet.org/content/mitdb/get-zip/1.0.0/'
        S3       = 's3://physionet-open/mitdb/1.0.0/'
        SizeNote = '73,5 MB zip / 104,3 MB extracted'
        Marker   = 'RECORDS'
    },
    [pscustomobject]@{
        Id       = 'D3'; Key = 'nstdb'; Priority = 'P1'
        Name     = 'MIT-BIH Noise Stress Test v1.0.0'
        Url      = 'https://physionet.org/content/nstdb/get-zip/1.0.0/'
        S3       = 's3://physionet-open/nstdb/1.0.0/'
        SizeNote = '67,7 MB zip / 67,6 MB extracted'
        Marker   = 'RECORDS'
    }
)

# Folder ptb-xl sengaja DIKECUALIKAN: 21.837 rekamannya duplikat dengan D1.
$Challenge2021Sources = @('chapman-shaoxing', 'georgia', 'ningbo')

$PriorityOrder = @{ 'P0' = 0; 'P1' = 1; 'P2' = 2 }

# ------------------------------------------------------------------- utilitas

function Write-Step { param([string]$Message) Write-Host "`n==> $Message" -ForegroundColor Cyan }
function Write-Ok   { param([string]$Message) Write-Host "    [OK] $Message" -ForegroundColor Green }
function Write-Skip { param([string]$Message) Write-Host "    [SKIP] $Message" -ForegroundColor DarkGray }
function Write-Warn { param([string]$Message) Write-Host "    [!] $Message" -ForegroundColor Yellow }

function Test-Command {
    param([string]$Name)
    $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-RemoteFile {
    param([string]$Url, [string]$OutFile)

    if (Test-Command 'curl.exe') {
        # -C - mengaktifkan resume; -L mengikuti redirect; --retry untuk koneksi tidak stabil
        & curl.exe -L -C - --retry 5 --retry-delay 5 -o $OutFile $Url
        if ($LASTEXITCODE -ne 0) { throw "curl gagal (exit $LASTEXITCODE) untuk $Url" }
    }
    else {
        Write-Warn 'curl.exe tidak tersedia; memakai Invoke-WebRequest (tanpa resume).'
        Invoke-WebRequest -Uri $Url -OutFile $OutFile -UseBasicParsing
    }
}

function Expand-Dataset {
    param([string]$ZipPath, [string]$Destination)

    if (Test-Command '7z') {
        & 7z x $ZipPath "-o$Destination" -y | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "7z gagal mengekstraksi $ZipPath" }
    }
    else {
        Expand-Archive -Path $ZipPath -DestinationPath $Destination -Force
    }
}

function Find-Marker {
    param([string]$Root, [string]$Marker)
    if (-not (Test-Path $Root)) { return $null }
    Get-ChildItem -Path $Root -Filter $Marker -Recurse -File -ErrorAction SilentlyContinue |
        Select-Object -First 1
}

# ----------------------------------------------------------------------- main

Write-Host ''
Write-Host '  Akuisisi Dataset - Hierarchy-Aware Conformal Risk Control' -ForegroundColor White
Write-Host '  ---------------------------------------------------------' -ForegroundColor DarkGray
Write-Host "  Prioritas : $Priority"
Write-Host "  Tujuan    : $DataDir"

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null

$targets = $Datasets | Where-Object { $PriorityOrder[$_.Priority] -le $PriorityOrder[$Priority] }

foreach ($ds in $targets) {
    Write-Step "$($ds.Id) - $($ds.Name)  [$($ds.SizeNote)]"

    $extractDir = Join-Path $DataDir $ds.Key
    $zipPath    = Join-Path $DataDir "$($ds.Key).zip"

    if (Find-Marker -Root $extractDir -Marker $ds.Marker) {
        Write-Skip "Sudah terekstraksi ($($ds.Marker) ditemukan)."
        continue
    }

    if (Test-Path $zipPath) {
        Write-Skip "ZIP sudah ada: $zipPath"
    }
    else {
        Write-Host "    Mengunduh $($ds.Url)"
        Get-RemoteFile -Url $ds.Url -OutFile $zipPath
        Write-Ok "Terunduh: $zipPath"
    }

    if ($SkipExtract) {
        Write-Skip 'Ekstraksi dilewati (-SkipExtract).'
        continue
    }

    Write-Host "    Mengekstraksi ke $extractDir"
    New-Item -ItemType Directory -Force -Path $extractDir | Out-Null
    Expand-Dataset -ZipPath $zipPath -Destination $extractDir
    Write-Ok 'Ekstraksi selesai.'
}

# ---------------------------------------------- D4: Challenge 2021 (selektif)

if ($PriorityOrder[$Priority] -ge 2) {
    Write-Step 'D4 - PhysioNet/CinC Challenge 2021 v1.0.3 (SELEKTIF)'
    Write-Warn 'Folder ptb-xl (21.837 rekaman) DIKECUALIKAN: duplikat dengan D1.'

    $chDir = Join-Path $DataDir 'challenge2021'
    New-Item -ItemType Directory -Force -Path $chDir | Out-Null

    if (Test-Command 'aws') {
        foreach ($src in $Challenge2021Sources) {
            $dest = Join-Path $chDir $src
            Write-Host "    Sinkronisasi $src ..."
            & aws s3 sync --no-sign-request `
                "s3://physionet-open/challenge-2021/1.0.3/training/$src/" $dest
            if ($LASTEXITCODE -ne 0) { Write-Warn "Sinkronisasi $src gagal." } else { Write-Ok $src }
        }
    }
    else {
        Write-Warn 'AWS CLI tidak ditemukan. Unduh manual dengan wget:'
        foreach ($src in $Challenge2021Sources) {
            Write-Host "      wget -r -N -c -np -R 'index.html*' https://physionet.org/files/challenge-2021/1.0.3/training/$src/"
        }
        Write-Host '    Pasang AWS CLI: winget install Amazon.AWSCLI' -ForegroundColor DarkGray
    }

    # Peta label SNOMED-CT dari repo evaluasi resmi Challenge.
    $maps = @{
        'dx_mapping_scored.csv'   = 'https://raw.githubusercontent.com/physionetchallenges/evaluation-2021/main/dx_mapping_scored.csv'
        'dx_mapping_unscored.csv' = 'https://raw.githubusercontent.com/physionetchallenges/evaluation-2021/main/dx_mapping_unscored.csv'
    }
    foreach ($name in $maps.Keys) {
        $out = Join-Path $chDir $name
        if (Test-Path $out) { Write-Skip $name; continue }
        Get-RemoteFile -Url $maps[$name] -OutFile $out
        Write-Ok $name
    }
}

# ---------------------------------------------------------------------- akhir

Write-Host ''
Write-Host '  Selesai.' -ForegroundColor Green
Write-Host '  Langkah berikutnya:' -ForegroundColor White
Write-Host '    python .\scripts\verify_datasets.py' -ForegroundColor White
Write-Host ''
