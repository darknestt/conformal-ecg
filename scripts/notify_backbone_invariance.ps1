# Ringkas hasil invariansi backbone dan tampilkan pemberitahuan di layar.
#
# Dipanggil oleh run_backbone_invariance.ps1 saat selesai, atau oleh pengawas
# yang menunggu runner berakhir. Aman dipanggil berulang.
# -Kering: cetak pesan saja, tanpa kotak pesan dan tanpa menghapus tugas terjadwal.
param([switch]$Kering)

$akar = Split-Path -Parent $PSScriptRoot
$dir = Join-Path $akar 'results\raw\backbone_invariance'
$teks = Join-Path $dir 'RINGKASAN.txt'

# Python menulis UTF-8; tanpa ini PowerShell 5.1 membacanya dengan codepage OEM.
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
& python (Join-Path $akar 'scripts\summarize_backbone_invariance.py') 2>&1 |
    ForEach-Object { "$_" } | Set-Content -Path $teks -Encoding UTF8

$ringkas = Get-Content (Join-Path $dir 'summary.json') -Raw | ConvertFrom-Json
$selesai = ($ringkas | Measure-Object -Property selesai -Sum).Sum
$baris = foreach ($r in $ringkas) {
    $k1 = if ($null -eq $r.k1_identik) { 'belum dapat dinilai' } elseif ($r.k1_identik) { 'LOLOS' } else { 'GAGAL - ada bug' }
    $inv = if ($null -eq $r.alpha_konsisten) { 'belum dapat dinilai' } else { "$($r.alpha_konsisten)/$($r.alpha_total) alpha konsisten" }
    "$($r.dataset.ToUpper()): $($r.selesai)/3 backbone | kontrol K1: $k1 | invariansi: $inv"
}

$lengkap = $selesai -ge 6
$judul = if ($lengkap) { 'Sqopus - pelatihan SELESAI' } else { 'Sqopus - pelatihan BERHENTI sebelum selesai' }
$pesan = (@("$selesai/6 konfigurasi selesai.", '') + $baris + @('', "Rincian lengkap:", $teks)) -join "`n"
if (-not $lengkap) {
    $pesan += "`n`nLanjutkan dengan:`npowershell -ExecutionPolicy Bypass -File scripts\run_backbone_invariance.ps1"
}

if ($Kering) {
    "[$judul]`n$pesan"
    return
}

if ($lengkap) {
    Unregister-ScheduledTask -TaskName 'Sqopus-BackboneInvariance' -Confirm:$false -ErrorAction SilentlyContinue
}

Add-Type -AssemblyName System.Windows.Forms
$ikon = if ($lengkap) { 'Information' } else { 'Warning' }
# DefaultDesktopOnly memaksa kotak pesan tampil di depan walau dipanggil dari jendela tersembunyi.
[System.Windows.Forms.MessageBox]::Show($pesan, $judul, 'OK', $ikon, 'Button1', 'DefaultDesktopOnly') | Out-Null
