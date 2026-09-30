# Catatan Kemajuan Penelitian

> **Periode:** 2026-09-29 (satu hari kerja)
> **Status proyek:** `PLANNING` → siap masuk fase infrastruktur
> **Dokumen induk:** [`../README.md`](../README.md) · [`protocol.md`](protocol.md) · [`references.md`](references.md)

Seluruh angka di dokumen ini diverifikasi langsung dari berkas dan data, bukan dari ingatan. Verifikasi ulang: `python .\scripts\check_consistency.py`

---

## Ringkasan

| Tahap | Status | Luaran utama |
|---|---|---|
| 1. Akuisisi dataset | ✅ **SELESAI** (P0+P1) | 44.379 berkas · 661,5 MB |
| 2. Verifikasi struktural | ✅ **SELESAI** | 29 pemeriksaan · 0 gagal · 2 peringatan |
| 3. Analisis struktur blok | ✅ **SELESAI** | 5 granularitas terukur + E11a |
| 4. Analisis kelayakan $\alpha$ | ✅ **SELESAI** | Batas $\alpha_{\min}$ per granularitas |
| 5. Survei literatur | ✅ **SELESAI** | 42 sitasi terverifikasi; **C1 ditemukan tertutup** |
| 6. Protokol pre-registration | 🟡 **DRAF** | Hipotesis & rencana analisis terkunci |
| 7. Studi kelayakan (backbone) | ⬜ **BELUM** | Jalur kritis berikutnya |

---

## 1. Akuisisi Dataset ✅

### Yang terkumpul

| Dataset | Berkas | Ukuran | Sumber | Kecepatan |
|---|---:|---:|---|---|
| **PTB-XL** (100 Hz saja) | 43.606 | 526,8 MB | Mirror AWS `physionet-open` | 405–914 KB/s paralel |
| **MIT-BIH Arrhythmia** | 706 | 104,3 MB | Mirror AWS `physionet-open` | idem |
| **MIT-BIH NSTDB** | 67 | 30,4 MB | PhysioNet langsung | 174 KB/s |
| **Total** | **44.379** | **661,5 MB** | | |

### Keputusan akuisisi yang terbukti tepat

| Keputusan | Dasar terukur |
|---|---|
| Pakai **mirror AWS S3**, bukan endpoint `get-zip` | get-zip ~33 KB/s (ETA 15 jam untuk PTB-XL) vs S3 405–914 KB/s |
| **Tidak mengunduh `records500/`** | Memangkas PTB-XL dari ~2,9 GB ke 526,8 MB. Konsekuensi langsung keputusan 100 Hz |
| NSTDB diunduh **per-berkas paralel** dari PhysioNet | Tidak ada di bucket S3 — 4 prefix diperiksa (`nstdb`, `nstdb/`, `noise`, `mit-bih-noise`), semua kosong |
| Folder `old/` NSTDB dilewati | Hanya duplikat warisan |
| **Challenge 2021 ditunda** (12,6 GB) | Menunggu H0 terkonfirmasi agar tidak terbuang bila sudut penelitian bergeser |

### Hambatan teknis yang diatasi

| Masalah | Solusi |
|---|---|
| DNS gagal berulang (`getaddrinfo failed`) | `install_dns_cache()` — paksa IPv4 + cache resolusi + 6× retry backoff |
| 43.606 berkas = 43k TLS handshake | Koneksi `HTTPSConnection` persisten per-thread |
| `TypeError: 'type' object is not iterable` | `field(default=tuple)` → `= ()` |
| `SSL: UNEXPECTED_EOF`, `WinError 10054` | Retry berlapis pada `list_objects()` dan `download_one()` |

### ⚠️ Sisa yang perlu dibersihkan

`data/raw/ptbxl.zip` — **5,41 MB**, sisa unduhan `get-zip` yang dibatalkan. PTB-XL utuh berukuran ~1,7 GB, jadi berkas ini **tidak lengkap dan tidak terpakai**.

```powershell
Remove-Item data\raw\ptbxl.zip
```

> Berkas ini **tidak** termasuk dalam hitungan 44.379 / 661,5 MB — angka itu hanya mencakup tiga folder dataset.

---

## 2. Verifikasi Struktural ✅

`python .\scripts\verify_datasets.py` → **29 pemeriksaan · 0 gagal · 2 peringatan** (keduanya disengaja)

### Yang terkonfirmasi persis sesuai rujukan resmi

- 21.799 rekaman · 18.869 pasien · 28 kolom metadata
- Distribusi superclass **identik**: NORM 9.514 · MI 5.469 · STTC 5.235 · CD 4.898 · HYP 2.649
- Multi-label terkonfirmasi: **27.765 label > 21.799 rekaman**
- Hierarki tersedia: **44 dari 71** pernyataan SCP bersifat diagnostik
- **Tidak ada pasien yang menyeberang fold** — split resmi aman dipakai apa adanya
- `age` dan `sex` lengkap tanpa nilai kosong
- MIT-BIH: **112.647 anotasi detak** (rujukan ~110.000)
- NSTDB: 12 rekaman bernoise + 3 rekaman noise, **6 level SNR lengkap**

### Pembagian fold (diverifikasi langsung dari CSV)

| Bagian | Fold | Rekaman | Pasien |
|---|---|---:|---:|
| Latih | 1–8 | 17.418 | 15.023 |
| Kalibrasi | 9 | 2.183 | **1.942** |
| Uji | 10 | 2.198 | 1.904 |

---

## 3. Analisis Struktur Blok ✅

`python .\scripts\analyze_block_structure.py`

### Lima tingkat granularitas pada satu dataset

| Pengelompokan | Blok | Rata-rata | Maks | $n_{\text{eff}}$ | Design effect |
|---|---:|---:|---:|---:|---:|
| `patient_id` | 18.869 | 1,16 | 10 | 15.659 | **1,39** |
| `strat_fold` | 10 | 2.179,90 | 2.198 | 10 | 2.179,9 |
| `device` | 11 | 1.981,73 | 6.140 | 6 | 3.900,6 |
| `nurse` | 12 | 1.693,83 | 8.295 | 4 | 5.185,4 |
| `site` | 51 | 427,10 | 8.940 | 3 | 6.687,0 |

**Dependensi pasien:** 5.041 rekaman (23,1%) berada di blok multi-rekaman.

### E11a — hipotesis yang ditolak, dan mengapa itu berguna

Hipotesis awal: design effect meluruh terhadap interval antar-rekaman. **Tidak terdukung** — hasilnya datar (2,25 → 2,71 → 2,73 → 2,77).

Sebabnya jelas: $n_{\text{eff}}$ Kish hanya fungsi **ukuran blok**, bukan kekuatan korelasi. Tapi justru karena ukuran blok nyaris seragam di keempat bin (2,14–2,44), keempat bin itu menjadi **perbandingan terkendali** untuk E11b nanti.

---

## 4. Analisis Kelayakan $\alpha$ ✅

`python .\scripts\feasibility_alpha.py` — dibuat setelah membaca Teorema 1 HCP.

| Blok | $K_1$ kalibrasi | $\alpha_{\min}$ | α=0,01 | α=0,05 | α=0,10 |
|---|---:|---:|:---:|:---:|:---:|
| `patient_id` | 1.942 | 0,00051 | ✅ | ✅ | ✅ |
| `site` | 40 | 0,0244 | ❌ | ✅ | ✅ |
| `nurse` | 12 | 0,0769 | ❌ | ❌ | ✅ |
| `device` | 11 | 0,0833 | ❌ | ❌ | ✅ |
| `strat_fold` | 8 | 0,1111 | ❌ | ❌ | ❌ |

**Temuan inti (C6):** urutan menurut design effect **berlawanan** dengan urutan menurut kelayakan $\alpha$. `site` punya efisiensi terburuk tapi $\alpha{=}0{,}05$ layak; `device` efisiensinya lebih baik tapi $\alpha{=}0{,}05$ mustahil.

---

## 5. Survei Literatur ✅ — Mengubah Arah Penelitian

### Proses

| Tahap | Alat | Hasil |
|---|---|---|
| Penarikan awal | Crossref API | 41 kandidat, belum disaring relevansi |
| Verifikasi ulang | **OpenAlex API** | 42 final dengan sitasi, FWCI, peringkat JUFO/Norway/CWTS |
| Pembacaan mendalam | Semantic Scholar + ar5iv | Abstrak lengkap B1, B2, B3, A3 + **teks penuh HCP** |
| Pencarian terarah | arXiv API | Menemukan paper yang menutup C1 |

### 🚨 Temuan yang mengubah segalanya

> **Lee Y., Barber R.F., Willett R.** *Distribution-free inference with hierarchical data*. **ACM Journal of Data Science, 2026.** `10.1145/3786352` · arXiv sejak Juni 2023

Menurunkan exchangeability hierarkis untuk "kelompok observasi atau pengukuran berulang" dan memperluas conformal + jackknife+. **Itu persis C1.**

**Konsekuensi:** C1 dicabut, C2 diturunkan ke lema, kontribusi direposisi ke **C6 + C7 + C8**, target venue bergeser ke jurnal klinis/terapan.

### 🎯 Kompensasinya lebih besar daripada kerugiannya

Bagian **Discussion** paper yang sama menyatakan:

> *"...the analyst can choose between a large number of independent groups $K$ with a small number of measurements $N_k$... **Characterizing the pros and cons of this tradeoff is an important question**"*

**Itu C6, dinyatakan terbuka oleh penulis teoremanya sendiri** — argumen novelty terkuat yang bisa diperoleh.

### Empat "ancaman" yang ternyata tidak mengancam

| Paper | Mengapa tidak menutup |
|---|---|
| B1 Papadopoulos review | Dependensi **antar-label**, bukan antar-sampel |
| B3 Pattern Recognition | Efisiensi komputasi Label Powerset, domain teks |
| B2 "hierarchical efficiency" | Irisan lintas-resolusi — arah **berlawanan** dengan penutupan ke atas |
| A3 group-weighted | Kelompok menentukan pergeseran kovariat; exchangeability intra-kelompok tetap |

### Rujukan fondasi terverifikasi

| Rujukan | Peran |
|---|---|
| Lee, Barber & Willett (2026), ACM J. Data Science | Fondasi teoretis · baseline **B12** |
| Dunn, Wasserman & Ramdas (2022), **JASA** | Baseline **B13–B15** |
| Barber dkk. (2023), Annals of Statistics — 278 sitasi, FWCI 63,4 | Landasan |
| Barber dkk. (2021), Annals of Statistics — 338 sitasi | Baseline **B6** |

---

## 6. Protokol Pre-Registration 🟡 DRAF

[`protocol.md`](protocol.md) — 14 bagian, mengunci:

- Hipotesis **H0, H0b, H1, H2, H3** dengan kriteria konfirmasi **dan refutasi**
- Split, preprocessing, skor nonconformity — **beku**
- Rencana analisis statistik: bootstrap level pasien, keluarga Holm-Bonferroni F-A…F-D
- **Aturan keputusan bila H0 tidak konklusif** — mencegah pencarian analisis pasca-hoc
- Checklist membuka fold 10 (sekali saja, tanggal dicatat)
- Log penyimpangan dengan kolom *"sebelum/sesudah melihat hasil?"*

Belum dapat dibekukan sampai backbone terlatih. Prasyarat "B12–B15 lolos unit test" ✅ **sudah terpenuhi** (2026-09-29).

---

## 6b. Implementasi Kalibrasi Conformal — `src/conformal/`

Jalur kritis yang dapat dikerjakan **tanpa model terlatih**, karena B1 dan B12–B15 hanyalah kuantil berbobot atas skor nonconformity.

| Berkas | Isi |
|---|---|
| `quantile.py` | `weighted_quantile`, `quantile_with_infinity` — atom $+\infty$ ditangani eksplisit |
| `calibration.py` | B1 split, B12 HCP, B13 Pooling CDFs, B14 Subsampling Once, B15 Double Conformal, Repeated Subsampling |
| `diagnostics.py` | **C7** — `block_sufficiency`, `minimum_blocks`, `compare_granularities` |
| `__init__.py` | API publik |
| `../tests/test_conformal.py` | 26 uji, seluruhnya lolos |

### Yang diverifikasi unit test

Uji diikat ke **pernyataan formal makalah**, bukan ke intuisi:

| Pernyataan | Sumber | Hasil |
|---|---|---|
| $N_k{=}1\ \forall k$ ⇒ HCP identik split conformal | Lee dkk. §3 | ✅ sama persis di 4 level $\alpha$ |
| $1-\alpha \le$ cakupan $\le 1-\alpha+\frac{2}{K+1}$ | Lee dkk. Teorema 1 | ✅ **0,8237** ∈ [0,800; 0,895], $K{=}20$, 4.000 ulangan |
| Pooling CDFs $\equiv$ HCP dengan $\alpha'=\alpha+\frac{1-\alpha}{K+1}$ | Lee dkk. Proposisi 1 | ✅ identik numerik |
| Cakupan Pooling $\ge 1-\alpha-\frac{1-\alpha}{K+1}$ | Lee dkk. Proposisi 1 | ✅ 0,7895 ≥ 0,762 — **memang** di bawah $1-\alpha$ |
| $\alpha \le \frac{1}{K+1}$ ⇒ ambang $=+\infty$ | H1 protokol | ✅ deterministik di semua metode |
| Repeated Subsampling $\to$ HCP untuk $B$ besar | Lee dkk. Proposisi 2 | ✅ selisih < 0,25 SD |

### 🔍 Temuan baru: B15 punya **dua** syarat kelayakan

Ditemukan saat menulis uji, tidak disebut eksplisit di Dunn dkk. Karena kuantil $1-\alpha/2$ diambil **dua kali**:

$$K+1 \ge \tfrac{2}{\alpha} \quad \textbf{dan} \quad \min_k N_k + 1 \ge \tfrac{2}{\alpha}$$

Syarat kedua tak punya padanan di HCP. Bukti numerik: pada $K{=}500$, $N_k{=}5$, $\alpha{=}0{,}2$ — HCP berhingga, sedangkan **seluruh 500 blok** B15 jatuh ke $+\infty$.

**Implikasi untuk PTB-XL:** dengan pengelompokan `patient_id`, median $N_k{=}1$, sehingga **B15 trivial untuk semua $\alpha<1$**. Ini akan dilaporkan apa adanya sebagai batas metode — bukan disembunyikan sebagai "baseline berkinerja buruk". Temuan ini memperkuat C6: $K$ dan $N_k$ adalah dua sumbu terpisah.

---

## 7. Artefak yang Dihasilkan

### Skrip (`scripts/`)

| Berkas | Fungsi |
|---|---|
| `download_physionet.py` | Unduh paralel lewat mirror S3 (DNS cache, koneksi persisten) |
| `download_nstdb.py` | Unduh NSTDB langsung dari PhysioNet |
| `download_data.ps1` | Cadangan via get-zip (lambat, tidak dipakai) |
| `verify_datasets.py` | 29 pemeriksaan struktural |
| `analyze_block_structure.py` | $n_{\text{eff}}$ & design effect multi-granularitas + E11a |
| `feasibility_alpha.py` | Batas $\alpha$ layak per granularitas (C6/C7) |
| `check_consistency.py` | Angka dokumen vs data nyata — **jalankan sebelum commit** |

### Modul (`src/conformal/`)

`quantile.py` · `calibration.py` (B1, B12–B15) · `diagnostics.py` (C7) · `__init__.py`

### Uji (`tests/`)

`conftest.py` · `test_conformal.py` — 26 uji, seluruhnya lolos

### Dokumen (`docs/`)

| Berkas | Isi |
|---|---|
| `dataset-verification.md` | Laporan verifikasi D1–D5 lengkap |
| `references.md` | 42 sitasi + 2 praterbit + 5 dataset, dengan analisis ancaman |
| `protocol.md` | Pre-registration |
| `progress.md` | Dokumen ini |

### Hasil mentah (`results/raw/`)

`dataset_verification.json` · `block_structure.json` · `feasibility_alpha.json`

---

## 8. Koreksi yang Dilakukan — Dicatat Terbuka

Lima kesalahan ditemukan dan diperbaiki sendiri. Dicatat karena jejak koreksi melindungi Anda saat menulis Methods.

| # | Kesalahan | Koreksi | Cara ditemukan |
|---|---|---|---|
| 1 | Dependensi pasien ~~13,4%~~ | **23,1%** | Ukuran yang benar adalah rekaman di dalam blok multi-rekaman, bukan selisih rekaman−pasien |
| 2 | Klaim gap disusun **tanpa pencarian literatur** | C1 dicabut, kontribusi direposisi | Pencarian arXiv terarah menemukan Lee-Barber-Willett |
| 3 | Validitas dikira ditentukan $n_{\text{eff}}$ Kish → "situs mustahil untuk $\alpha \leq 0{,}25$" | Ditentukan **$K_1$** (jumlah blok) → situs $\alpha_{\min}=0{,}024$, jadi $\alpha{=}0{,}05$ **layak** | Membaca teks penuh Teorema 1, bukan hanya abstrak |
| 4 | Jumlah rekaman per fold dihitung dengan **pengurangan**, fold 9–10 tertukar | 17.418 / 2.183 / 2.198 dari CSV | Verifikasi langsung sebelum membekukan protokol |
| 5 | Satu unit test **lolos secara hampa** — hanya membandingkan `inf >= berhingga` pada 2 dari 3 level $\alpha$ | Blok diperbesar ke $N{=}60$ agar ambang B15 berhingga; ditambah uji khusus dua syarat kelayakan | Mencetak nilai ambang aktual alih-alih memercayai status "26 passed" |

> **Pelajaran yang paling mahal:** kesalahan #3 punya intuisi yang benar tapi kuantitas yang salah. Membaca abstrak saja tidak cukup — teoremanya harus dibuka.
>
> **Pelajaran kedua (dari #5):** uji yang lolos tidak membuktikan apa pun sampai angkanya diperiksa. Suite hijau dapat menyembunyikan perbandingan yang trivial.

---

## 9. Belum Dikerjakan

### ❗ Jalur kritis

| Tugas | Mengapa penting |
|---|---|
| **Studi kelayakan (Langkah 4)** | Latih backbone → conformal naif → ukur cakupan. **Memvalidasi H0** |
| ~~Implementasi B12–B15~~ | ✅ **Selesai 2026-09-29** — `src/conformal/`, 26 uji lolos |
| **Formalisasi C6 di F1** | Pembeda utama penelitian |

### Menyusul

- Baca B7 (arXiv:2410.06296) — ancaman terhadap C2
- Baca E5 (arXiv:2601.01223) — kelompok Baheri, bergerak ke wilayah yang sama
- Verifikasi indeksasi Scopus tiap jurnal (perlu akun institusi)
- Cari rujukan non-jurnal wajib (Angelopoulos, Vovk, Romano, RAPS, Demšar, de Chazal)
- Unduh Challenge 2021 selektif — **setelah H0 terkonfirmasi**
- Rekrut kolaborator statistika

---

## 10. Risiko Terbuka

| Risiko | Tingkat | Mitigasi |
|---|---|---|
| **Belum ada repositori git** | 🔴 **TINGGI** | Seluruh pekerjaan tidak terlacak. Protokol menuntut `git tag protocol-v1` — mustahil tanpa repo. **Inisialisasi segera** |
| B7 terbit di venue kuat lebih dulu | 🟡 Sedang | Pantau arXiv:2410.06296; C2 sudah diturunkan ke lema |
| Kelompok Baheri bergerak ke wilayah sama | 🟡 Sedang | B2 (Feb 2025) → healthcare hierarkis (Jan 2026). Pantau |
| H0 tidak konklusif di PTB-XL | 🟡 Sedang | Design effect hanya 1,39. `protocol.md` §11 sudah menetapkan urutan tindakan |
| Judul & nama metode belum final | 🟢 Rendah | Sengaja ditunda sampai C6 diformalkan |

### Perbaikan yang disarankan segera

```powershell
Remove-Item data\raw\ptbxl.zip     # sisa unduhan gagal, 5,41 MB
git init
git add .
git commit -m "Fondasi penelitian: dataset terverifikasi, survei literatur, protokol draf"
```

#### ⚠️ Satu penyesuaian `.gitignore` yang perlu dilakukan

`.gitignore` sudah benar mengabaikan `data/raw/`, `data/interim/`, `data/processed/` — sehingga **661,5 MB dataset tidak akan ter-commit**. Itu tepat.

Tetapi `results/raw/` **juga diabaikan**, padahal isinya hanya **11,4 KB**:

| Berkas | Ukuran | Isi |
|---|---:|---|
| `dataset_verification.json` | 6,3 KB | 29 pemeriksaan + statistik |
| `block_structure.json` | 3,1 KB | 5 granularitas + E11a |
| `feasibility_alpha.json` | 2,0 KB | Batas $\alpha$ per granularitas |

Ketiganya adalah **bukti asal-usul setiap angka** di README, `protocol.md`, dan dokumen ini. Tanpa mereka, klaim "29 pemeriksaan, 0 gagal" tidak dapat ditelusuri siapa pun — termasuk Anda sendiri enam bulan lagi.

```gitignore
# ganti baris "results/raw/" menjadi:
results/raw/*
!results/raw/*.json
```

> Keluaran besar (bobot model, array sinyal) tetap terabaikan; hanya JSON ringkas yang masuk.

---

## Lingkungan

```
OS      : Windows · PowerShell 5.1
Python  : 3.14.6
pandas  : 3.0.6
wfdb    : 4.3.1
Disk    : 61,4 GB bebas
```

**Pustaka conformal terverifikasi di PyPI:** MAPIE 1.5.0 · TorchCP 1.2.1 · crepes 0.9.1 · torch 2.14.0 — seluruhnya tersedia untuk Python 3.14.6.
