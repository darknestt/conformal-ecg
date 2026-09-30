# Panduan Akuisisi Data

Direktori ini menampung dataset mentah. **Isi `data/raw/` tidak pernah di-commit ke git** (lihat `.gitignore`).

Spesifikasi lengkap dan hasil verifikasi setiap dataset ada di [`docs/dataset-verification.md`](../docs/dataset-verification.md).

---

## Struktur Target

```
data/
├── README.md              <- file ini
├── raw/                   <- hasil unduhan mentah (tidak di-commit)
│   ├── ptbxl/             <- D1  PTB-XL v1.0.3
│   ├── mitdb/             <- D2  MIT-BIH Arrhythmia v1.0.0
│   ├── nstdb/             <- D3  MIT-BIH Noise Stress Test v1.0.0
│   ├── challenge2021/     <- D4  PhysioNet/CinC Challenge 2021 (P2, selektif)
│   └── uea/               <- D5  UEA/UCR Archive (P3, opsional)
└── interim/               <- hasil preprocessing (tidak di-commit)
```

---

## Cara Tercepat

Dari root repositori:

```powershell
python .\scripts\download_physionet.py mitdb ptbxl --workers 24   # 631 MB lewat mirror S3
python .\scripts\download_nstdb.py --workers 8                    # 30 MB langsung dari PhysioNet
python .\scripts\verify_datasets.py
```

Semua skrip dapat dilanjutkan kapan saja — berkas yang sudah lengkap dilewati otomatis.

**Status saat ini:** P0 dan P1 ✅ selesai (661 MB, 44.379 berkas, 29 pemeriksaan lolos).

---

## ⚠️ Temuan Penting tentang Jalur Unduh (terukur 2026-09-29)

### Jangan pakai endpoint `get-zip` PhysioNet

PhysioNet membuat arsip ZIP secara dinamis saat diminta. Hasil pengukuran nyata:

| Jalur | Kecepatan terukur | ETA untuk PTB-XL |
|---|---|---|
| `physionet.org/content/.../get-zip/` | **~33 KB/s** | **~15 jam** ❌ |
| `physionet.org/files/...` (statis) | lambat, sering terpotong | tidak andal ❌ |
| **`s3://physionet-open/...`** (mirror AWS) | **405–716 KB/s per koneksi** | **menit dengan paralel** ✅ |

Uji pembanding pada berkas yang sama (`ptbxl_database.csv`, 6.594.879 byte): S3 menyelesaikan seluruh berkas; `physionet.org/files` baru mencapai 343.691 byte pada durasi yang sama.

### Lewati `records500/` — hemat 2,4 GB

Penelitian ini memakai **100 Hz** sebagai konfigurasi utama, sesuai keputusan di README §15. Karena itu `records500/` tidak diperlukan:

| Cakupan | Objek | Ukuran |
|---|---|---|
| PTB-XL lengkap | 87.204 | ~2,9 GB |
| **Tanpa `records500/`** | **43.606** | **526,8 MB** ✅ |
| Yang dilewati | 43.598 | 2,4 GB |

Jika kelak perlu 500 Hz untuk eksperimen E9, jalankan `--with-500hz`.

### NSTDB tidak tersedia di bucket terbuka

Halaman resmi MIT-BIH dan PTB-XL mencantumkan perintah `aws s3 sync --no-sign-request s3://physionet-open/...`, tetapi halaman NSTDB **tidak** — dan prefix `nstdb/1.0.0/` memang kosong di bucket tersebut. Ambil NSTDB lewat `get-zip` (hanya 67,7 MB, masih wajar) atau `wget`.

### Jaringan tidak stabil

Selama pengujian muncul kegagalan berulang: `getaddrinfo failed`, `SSL: UNEXPECTED_EOF_WHILE_READING`, dan `WinError 10054`. Skrip sudah menanganinya dengan pemaksaan IPv4, retry berjenjang, dan koneksi HTTPS persisten per-thread. **Jika unduhan berhenti, cukup jalankan ulang perintah yang sama.**

---

## Rencana Bertahap

| Prioritas | Dataset | Ukuran | Kapan diunduh |
|---|---|---|---|
| **P0** | PTB-XL (tanpa 500 Hz) + MIT-BIH | ~631 MB | ✅ **Selesai** |
| **P1** | + NSTDB | +30,4 MB | ✅ **Selesai** |
| **P2** | + Challenge 2021 (selektif) | ~3–5 GB | **Hanya setelah H0 terkonfirmasi** |
| **P3** | + UEA | ~1,5 GB | Opsional, kemungkinan tidak dipakai |

> **Jangan langsung unduh 12,6 GB Challenge 2021.** Tidak ada gunanya sebelum studi kelayakan pada PTB-XL dan MIT-BIH memberi hasil.

---

## Perintah Manual (jika skrip gagal)

### D1 — PTB-XL v1.0.3 (526,8 MB tanpa `records500/`)

```powershell
python .\scripts\download_physionet.py ptbxl --workers 24
```

Dengan AWS CLI (jika terpasang, juga cepat):

```powershell
aws s3 sync --no-sign-request --exclude "records500/*" `
  s3://physionet-open/ptb-xl/1.0.3/ data\raw\ptbxl\
```

**File kunci setelah unduhan:**
- `ptbxl_database.csv` — 21.799 baris, 28 kolom (6.594.879 byte)
- `scp_statements.csv` — peta hierarki label
- `records100/` — sinyal 100 Hz (**yang dipakai**)
- `SHA256SUMS.txt` — verifikasi integritas

### D2 — MIT-BIH Arrhythmia v1.0.0 (104,3 MB, 706 objek)

```powershell
python .\scripts\download_physionet.py mitdb --workers 24
```

### D3 — MIT-BIH Noise Stress Test v1.0.0 (30,4 MB inti)

Tidak ada di bucket terbuka — sudah diperiksa untuk prefix `nstdb`, `nstdb/`, `noise`, dan `mit-bih-noise`, semuanya kosong. Gunakan pengunduh langsung dengan koneksi paralel:

```powershell
python .\scripts\download_nstdb.py --workers 8
```

Terukur **174 KB/s** — sekitar 5x lebih cepat daripada `get-zip` aliran tunggal (~33 KB/s).

**Yang diunduh (67 berkas, 30,4 MB):**
- 12 rekaman EKG bernoise: `118e{24,18,12,06,00,_6}` dan `119e{24,18,12,06,00,_6}`
- 3 rekaman noise: `bw`, `ma`, `em`
- Berkas pendukung: `RECORDS`, `ANNOTATORS`, `SHA256SUMS.txt`, `nstdb.txt`, `nstdbgen`

> Folder `old/` **tidak** diunduh — berisi duplikat warisan yang tidak dipakai. Itulah sebabnya totalnya 30,4 MB, bukan 67,6 MB seperti tertera di halaman resmi.

Alternatif lewat ZIP (lambat, hanya jika skrip gagal):

```powershell
curl.exe -L -C - -o data\raw\nstdb.zip "https://physionet.org/content/nstdb/get-zip/1.0.0/"
Expand-Archive -Path data\raw\nstdb.zip -DestinationPath data\raw\nstdb -Force
```

### D4 — Challenge 2021 v1.0.3 (SELEKTIF — jangan unduh semuanya)

⚠️ **Kecualikan folder `ptb-xl`** — 21.837 rekamannya identik dengan D1. Memasukkannya akan membatalkan klaim "validasi pada dataset independen".

Unduh hanya sumber yang benar-benar independen:

```powershell
$base = "https://physionet.org/files/challenge-2021/1.0.3/training"
foreach ($src in @("chapman-shaoxing", "georgia", "ningbo")) {
    aws s3 sync --no-sign-request "s3://physionet-open/challenge-2021/1.0.3/training/$src/" "data\raw\challenge2021\$src\"
}
```

Tanpa AWS CLI, gunakan wget (pasang via `winget install JernejSimoncic.Wget` atau WSL):

```bash
wget -r -N -c -np -R "index.html*" \
  https://physionet.org/files/challenge-2021/1.0.3/training/chapman-shaoxing/
```

**Ukuran per sumber (jumlah rekaman terverifikasi):**

| Folder | Rekaman | Pakai? |
|---|---|---|
| `chapman-shaoxing` | 10.247 | ✅ Ya |
| `georgia` | 10.344 | ✅ Ya |
| `ningbo` | 34.905 | ✅ Ya (atau subsample) |
| `cpsc_2018` | 6.877 | Opsional |
| `cpsc_2018_extra` | 3.453 | Opsional |
| `ptb` | 516 | Opsional (kecil) |
| `st_petersburg_incart` | 74 | Opsional (sangat kecil) |
| `ptb-xl` | 21.837 | ❌ **JANGAN — duplikat D1** |

**Berkas pendukung yang wajib diambil:**

```powershell
curl.exe -L -o data\raw\challenge2021\dx_mapping_scored.csv `
  "https://raw.githubusercontent.com/physionetchallenges/evaluation-2021/main/dx_mapping_scored.csv"
curl.exe -L -o data\raw\challenge2021\dx_mapping_unscored.csv `
  "https://raw.githubusercontent.com/physionetchallenges/evaluation-2021/main/dx_mapping_unscored.csv"
```

### D5 — UEA/UCR Archive (opsional)

```powershell
# Cara termudah: lewat pustaka aeon, tanpa unduh manual
pip install aeon
```

```python
from aeon.datasets import load_classification
X, y, meta = load_classification("FaceDetection", meta_data=True)
```

Atau unduh arsip penuh (gunakan format `.ts`, bukan ARFF):

```powershell
curl.exe -L -C - -o data\raw\uea\Multivariate2018_ts.zip `
  "http://www.timeseriesclassification.com/aeon-toolkit/Archives/Multivariate2018_ts.zip"
```

---

## Verifikasi Integritas

PhysioNet menyertakan `SHA256SUMS.txt` di setiap dataset. Verifikasi setelah ekstraksi:

```powershell
# Contoh untuk satu berkas
Get-FileHash data\raw\ptbxl\ptbxl_database.csv -Algorithm SHA256
```

Lalu cocokkan dengan entri di `data\raw\ptbxl\SHA256SUMS.txt`.

`scripts\verify_datasets.py` melakukan pengecekan struktural (jumlah baris, kolom, distribusi label) secara otomatis.

---

## Lisensi & Kewajiban Sitasi

Semua dataset **gratis dan publik**, tetapi **setiap penggunaan wajib disertai sitasi**. Lisensi per dataset:

| Dataset | Lisensi |
|---|---|
| PTB-XL | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| MIT-BIH Arrhythmia | Open Data Commons Attribution License v1.0 |
| MIT-BIH Noise Stress Test | Open Data Commons Attribution License v1.0 |
| Challenge 2021 | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| UEA/UCR | Lihat https://www.timeseriesclassification.com/citationpolicy.php |

Daftar sitasi lengkap (termasuk DOI terverifikasi) ada di [`docs/dataset-verification.md`](../docs/dataset-verification.md).

**Khusus Challenge 2021:** wajib menyitasi **parent projects**-nya juga — PTB Diagnostic ECG Database dan PTB-XL — selain paper Challenge itu sendiri.

**Semua dataset PhysioNet** juga meminta sitasi standar PhysioNet.

---

## Kebutuhan Disk

| Tahap | Kebutuhan |
|---|---|
| P0 + P1 (zip + ekstraksi) | ~5 GB |
| + interim/preprocessed | ~8 GB |
| + P2 selektif | ~18 GB |
| Rekomendasi cadangan | **25 GB** |

---

## Troubleshooting

**`curl.exe` tidak dikenali** — tersedia sejak Windows 10 build 17063. Jika tidak ada, gunakan `Invoke-WebRequest -Uri <url> -OutFile <file>` (tidak mendukung resume).

**Unduhan PhysioNet lambat atau putus** — gunakan AWS S3 mirror (`s3://physionet-open/...`) dengan `--no-sign-request`; tidak perlu akun AWS.

**`Expand-Archive` gagal pada ZIP besar** — gunakan 7-Zip: `7z x data\raw\ptbxl.zip -odata\raw\ptbxl`.

**Kehabisan disk saat ekstraksi** — PTB-XL uncompressed 3,0 GB. Jika ruang terbatas, ekstrak hanya `records100/` dan berkas CSV; abaikan `records500/`.
