# Jalankan seluruh eksperimen invariansi lintas backbone secara berurutan.
#
# Aman dijalankan ulang: backbone yang sudah selesai dimuat dari checkpoint, dan
# pelatihan yang terputus dilanjutkan dari epoch terakhir (src/train.py).
#
# Urutan disengaja: MIT-BIH dulu, karena di sanalah temuan positif berada dan
# SmallECGNet paling lemah (balanced accuracy 0,375) -- serangan "artefak model
# lemah" paling tajam di sana.
#
#   powershell -ExecutionPolicy Bypass -File scripts\run_backbone_invariance.ps1

# 'Continue', bukan 'Stop': di PowerShell 5.1, stderr python lewat 2>&1 menjadi
# ErrorRecord, dan satu peringatan akan menghentikan pelatihan belasan jam.
$ErrorActionPreference = 'Continue'
$akar = Split-Path -Parent $PSScriptRoot
Set-Location $akar

# Cegah tidur hanya selama proses ini hidup; lepas otomatis saat proses berakhir.
Add-Type -Namespace Win32 -Name Daya -MemberDefinition @'
[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);
'@
[Win32.Daya]::SetThreadExecutionState([uint32]'0x80000001') | Out-Null  # CONTINUOUS | SYSTEM_REQUIRED

$dirLog = Join-Path $akar 'results\raw\backbone_invariance\logs'
New-Item -ItemType Directory -Force -Path $dirLog | Out-Null

$jadwal = @(
    @{ dataset = 'mitdb'; backbone = 'small' },
    @{ dataset = 'mitdb'; backbone = 'resnet1d34' },
    @{ dataset = 'mitdb'; backbone = 'resnet1d50' },
    @{ dataset = 'ptbxl'; backbone = 'small' },
    @{ dataset = 'ptbxl'; backbone = 'resnet1d34' },
    @{ dataset = 'ptbxl'; backbone = 'resnet1d50' }
)

foreach ($j in $jadwal) {
    $nama = "$($j.dataset)_$($j.backbone)"
    $log = Join-Path $dirLog "$nama.log"
    $mulai = Get-Date
    Write-Host "[$($mulai.ToString('yyyy-MM-dd HH:mm:ss'))] mulai $nama"

    # Tulis log per baris agar kemajuan dapat dipantau selama pelatihan berjalan.
    & python -u experiments\backbone_invariance.py --dataset $j.dataset --backbone $j.backbone 2>&1 |
        ForEach-Object { "$_" } | Tee-Object -FilePath $log -Append | Out-Null

    if ($LASTEXITCODE -ne 0) {
        Write-Host "GAGAL: $nama (kode $LASTEXITCODE). Lihat $log"
        exit $LASTEXITCODE
    }
    $menit = [math]::Round(((Get-Date) - $mulai).TotalMinutes, 1)
    Write-Host "[$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))] selesai $nama ($menit menit)"
}

Write-Host 'Seluruh eksperimen invariansi selesai.'
# Tugas login hanya berguna selama pelatihan belum tuntas.
Unregister-ScheduledTask -TaskName 'Sqopus-BackboneInvariance' -Confirm:$false -ErrorAction SilentlyContinue
