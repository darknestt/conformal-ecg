# Protokol Eksperimen (Pre-Registration Internal)

> **Status:** 🟡 `DRAF` — belum dibekukan
> **Dibuat:** 2026-09-29
> **Dibekukan:** *(belum — isi tanggal dan hash commit saat dibekukan)*
> **Dokumen induk:** [`../README.md`](../README.md)

---

## 0. Mengapa dokumen ini ada

Setiap keputusan analisis yang diambil **setelah** melihat hasil adalah peluang untuk menipu diri sendiri. Dokumen ini mengunci keputusan tersebut lebih dulu.

Ketika reviewer bertanya *"mengapa Anda memakai α=0,05 dan bukan 0,10?"* atau *"mengapa uji ini dan bukan itu?"*, jawabannya harus: **"sudah ditetapkan sebelum data uji disentuh, tercatat di commit `abc1234`."**

### Aturan pembekuan

1. Protokol dibekukan dengan `git tag protocol-v1` **sebelum** eksperimen konfirmatori pertama.
2. Setelah beku, perubahan apa pun **wajib** dicatat di §12 dengan tanggal, alasan, dan apakah terjadi sebelum/sesudah melihat hasil.
3. Analisis yang tidak tercantum di sini otomatis berstatus **eksploratif** dan wajib dilabeli demikian di naskah.

---

## 1. Pemisahan Eksploratif vs Konfirmatori

| Sudah dikerjakan | Status | Catatan |
|---|---|---|
| Verifikasi struktural dataset (29 pemeriksaan) | **Deskriptif** | Tidak ada model, tidak ada hipotesis diuji |
| Analisis struktur blok multi-granularitas | **Deskriptif** | Statistik struktur data murni |
| E11a (struktur blok per bin interval) | **Deskriptif** | Tidak ada model |
| Perhitungan batas kelayakan $\alpha \ge 1/(K_1+1)$ | **Deterministik** | Konsekuensi aljabar dari Teorema 1, bukan temuan statistik |

**Tidak ada satu pun analisis di atas yang menyentuh keluaran model.** Karena itu semuanya boleh dilaporkan sebagai karakterisasi dataset, bukan hasil eksperimen.

Semua yang melibatkan skor model bersifat **konfirmatori** dan tunduk pada protokol ini.

---

## 2. Hipotesis yang Ditetapkan Sebelumnya

### H0 — Hipotesis inti (menentukan kelangsungan penelitian)

> Split conformal per-sampel menghasilkan cakupan empiris **di bawah** $1-\alpha$ pada PTB-XL ketika kalibrasi mengabaikan struktur blok pasien.

| Butir | Spesifikasi |
|---|---|
| Arah | Satu arah (under-coverage) |
| Level uji | $\alpha_{\text{uji}} = 0,05$ |
| Uji | Binomial eksak, CI Clopper-Pearson |
| **Kriteria konfirmasi** | Batas atas CI 95% cakupan empiris **< $1-\alpha$ nominal** pada minimal 2 dari 3 level $\alpha$ |
| **Kriteria refutasi** | Batas bawah CI 95% **≥ $1-\alpha$** pada seluruh level $\alpha$ |
| **Zona tidak konklusif** | CI memuat $1-\alpha$ → lihat §11 |

> ⚠️ **Peringatan kalibrasi daya.** Design effect PTB-XL pada level pasien hanya **1,39**, jauh lebih lemah daripada MIT-BIH. Deviasi cakupan yang diharapkan **kecil**. Bila H0 tidak terkonfirmasi di PTB-XL, itu **belum** membatalkan penelitian — lihat H0b.

### H0b — Hipotesis pendukung (dependensi ekstrem)

> Deviasi cakupan membesar secara monoton terhadap design effect blok.

Diuji lintas: MIT-BIH (detak→rekaman, DEff ≈ 2.347) vs PTB-XL pasien (DEff = 1,39).

**Kriteria:** korelasi Spearman antara design effect dan besar deviasi cakupan, $\rho > 0$ dengan $p < 0,05$.

### H1 — Kelayakan (C6)

> Untuk granularitas dengan $\alpha < 1/(K_1+1)$, metode hierarkis menghasilkan himpunan prediksi **tak hingga atau memuat seluruh label** pada ≥ 95% kasus uji.

Ini prediksi **deterministik** dari Teorema 1, bukan hipotesis statistik. Jika gagal, implementasi Anda salah — bukan teorinya.

**Granularitas yang diprediksi gagal** (dari `scripts/feasibility_alpha.py`):

| Granularitas | $K_1$ | $\alpha_{\min}$ | Gagal pada |
|---|---:|---:|---|
| `patient_id` | 1.942 | 0,00051 | — (semua layak) |
| `site` | 40 | 0,0244 | $\alpha = 0,01$ |
| `nurse` | 12 | 0,0769 | $\alpha = 0,01$; $0,05$ |
| `device` | 11 | 0,0833 | $\alpha = 0,01$; $0,05$ |
| `strat_fold` | 8 | 0,1111 | seluruhnya |

### H2 — Ortogonalitas dua batas (C6, klaim utama)

> Urutan granularitas menurut **design effect** tidak sama dengan urutan menurut **kelayakan $\alpha$**.

Sudah terlihat secara struktural. Yang diuji: apakah **ukuran himpunan empiris** mengikuti $\mathrm{DEff}_{\text{blok}} = n[1+(H-1)\rho]/(KH)$ sementara **kelayakan** mengikuti $K_1$.

> 🔧 **Dikoreksi 2026-09-30.** Versi sebelumnya memakai design effect Kish (`site` 6.687 vs `device` 3.901) dan menyimpulkan kedua urutan berlawanan. Kish milik estimator terboboti-observasi, bukan estimator terboboti-blok yang dipakai HCP. Dengan ukuran yang benar urutannya **sejalan**, bukan berlawanan — lihat [`theory.md`](theory.md) §3.1. H2 karenanya diuji terhadap $\mathrm{DEff}_{\text{blok}}$.

**Kriteria:** korelasi Spearman antara design effect dan ukuran himpunan rata-rata signifikan positif, **sementara** korelasi antara design effect dan kelayakan tidak signifikan.

### H3 — Penutupan hierarkis (C2, lema)

> Penutupan ke atas tidak pernah menurunkan cakupan empiris.

Deterministik. Cakupan setelah penutupan ≥ cakupan sebelum penutupan pada **setiap** konfigurasi. Satu pelanggaran = bug.

---

## 3. Data dan Pemisahan — DIBEKUKAN

### Split resmi PTB-XL

| Bagian | Fold | Rekaman | Pasien | Penggunaan |
|---|---|---:|---:|---|
| Latih | 1–8 | **17.418** | 15.023 | Melatih backbone **saja** |
| Kalibrasi | 9 | **2.183** | **1.942** | Menentukan ambang konformal |
| Uji | 10 | **2.198** | 1.904 | **Disentuh satu kali, di akhir** |

> ✅ Diverifikasi langsung dari `ptbxl_database.csv` pada 2026-09-29, bukan hasil pengurangan. Jumlah 17.418 + 2.183 + 2.198 = 21.799 ✓
>
> ⚠️ **$K_1 = 1.942$**, bukan 2.183. Unit kalibrasi adalah **pasien**, bukan rekaman — inilah inti seluruh penelitian ini.

### Aturan mutlak

- [ ] **Fold 10 tidak dibuka sampai seluruh keputusan metode final.** Tidak ada pengecualian.
- [ ] Tuning hiperparameter **hanya** pada fold 1–8 dengan validasi internal.
- [ ] Pemilihan skor nonconformity **hanya** pada fold 9.
- [ ] Bila fold 10 terlanjur dilihat, **catat di §12** dan nyatakan di naskah bagian Threats to Validity.

### Dataset pendamping

| Dataset | Peran | Unit blok |
|---|---|---|
| MIT-BIH (48 rekaman, 47 subjek) | Ujung dependensi ekstrem | Detak → rekaman |
| NSTDB (6 level SNR) | Covariate shift terkendali | — |
| Challenge 2021 (selektif) | Generalisasi | Situs/sumber |

> Challenge 2021 **tidak diunduh** sampai H0 terkonfirmasi. Folder `ptb-xl` **wajib dikecualikan**.

---

## 4. Preprocessing — DIBEKUKAN

```
Sampling      : 100 Hz (records100/)
Filter        : band-pass 0,5–40 Hz, Butterworth orde 3, zero-phase (filtfilt)
Normalisasi   : per-lead, z-score, statistik dihitung HANYA dari fold 1–8
Panjang       : 1000 sampel (10 detik) — tanpa cropping/padding
Lead          : seluruh 12 lead
Penanganan NaN: rekaman dengan NaN dikeluarkan; jumlahnya dicatat
```

**Larangan:** tidak ada augmentasi pada fold 9 dan 10. Tidak ada resampling kelas. Tidak ada pembuangan outlier berdasarkan label.

---

## 5. Model Dasar (Backbone)

| Butir | Spesifikasi |
|---|---|
| Utama | `xresnet1d101` (benchmark resmi PTB-XL) |
| Pendamping | `inception1d`, `resnet1d_wang`, `LSTM` |
| Tugas | Multi-label, 5 superclass diagnostik (NORM/MI/STTC/CD/HYP) |
| Loss | Binary cross-entropy |
| Seed | **5 seed tetap: 0, 1, 2, 3, 4** |
| Kriteria berhenti | Early stopping pada macro-AUROC fold 9, patience 10 |

> Backbone **bukan kontribusi**. Ia hanya perlu kompetitif dengan benchmark. Target: macro-AUROC dalam ±0,02 dari nilai yang dilaporkan Strodthoff dkk. (2021). Bila jauh di bawah, perbaiki backbone sebelum melanjutkan — jangan salahkan lapisan konformal.

---

## 6. Skor Nonconformity — DIBEKUKAN

| Kode | Definisi | Untuk |
|---|---|---|
| `S1` | $1 - \hat p_\ell(x)$ per label | Baseline dasar |
| `S2` | APS (kumulatif terurut) | B4 |
| `S3` | RAPS (APS + regularisasi) | B5 |
| `S4` | Agregat blok: $\max_i s(Z_{k,i})$ | Varian K1 |
| `S5` | Agregat blok: $\text{mean}_i\, s(Z_{k,i})$ | Varian K1 |

**Pemilihan antar S4/S5 dilakukan pada fold 9 saja**, kriteria: ukuran himpunan rata-rata terkecil pada cakupan nominal terpenuhi.

---

## 7. Metode yang Diuji

| Kelompok | Metode |
|---|---|
| Usulan | HiCoRC (K1+K2+K3), plus 7 varian ablasi $2^3$ |
| Conformal hierarkis | **B12 HCP**, B13 Pooling CDFs, B14 Subsampling Once, B15 Double Conformal |
| Conformal standar | B1 Split naif, B2 Mondrian, B3 CRC, B4 APS, B5 RAPS, B6 Jackknife+ |
| Kalibrasi | B7 Platt, B8 Temperature, B9 Isotonic |
| Bayesian aproksimasi | B10 MC-Dropout, B11 Deep Ensemble |

> B12–B15 **tidak tersedia di pustaka mana pun** dan harus diimplementasikan sendiri. Setiap implementasi wajib punya unit test yang memverifikasi cakupan pada data sintetis dengan struktur blok yang diketahui.

> ✅ **Selesai 2026-09-29** — [`src/conformal/calibration.py`](../src/conformal/calibration.py), diuji oleh [`tests/test_conformal.py`](../tests/test_conformal.py) (26 uji lolos).
>
> ⚠️ **Konsekuensi yang ditemukan saat implementasi — dicatat SEBELUM fold 10 dibuka.** B15 (Double Conformal) menuntut **dua** syarat kelayakan sekaligus, karena mengambil kuantil $1-\alpha/2$ dua kali:
>
> $$K+1 \ge \tfrac{2}{\alpha} \quad \textbf{dan} \quad \min_k N_k + 1 \ge \tfrac{2}{\alpha}$$
>
> Pada PTB-XL dengan pengelompokan `patient_id`, median $N_k = 1$, sehingga **B15 dipastikan menghasilkan himpunan trivial untuk seluruh $\alpha \in \{0{,}01; 0{,}05; 0{,}10\}$**. Prediksi ini bersifat **deterministik dan dibuat di muka** — bila hasil eksperimen nanti menunjukkan B15 berhingga pada `patient_id`, itu menandakan **bug implementasi**, bukan temuan.
>
> B15 tetap dilaporkan di tabel hasil dengan nilai trivialnya, disertai penjelasan sebab. Melaporkannya sebagai "baseline berkinerja buruk" tanpa menyebut sebab strukturalnya akan menyesatkan.

---

## 8. Luaran (Outcomes)

### Luaran primer

| Kode | Metrik | Arah |
|---|---|---|
| **P1** | Deviasi cakupan empiris dari $1-\alpha$ | Mendekati 0 dari atas |
| **P2** | Ukuran himpunan prediksi rata-rata | Sekecil mungkin |

> Hanya dua. Menambah luaran primer setelah melihat hasil adalah bentuk p-hacking.

### Luaran sekunder

SSCV · Conditional Coverage Gap lintas subkelompok · HCVR · FNR@MI · proporsi himpunan tak hingga

### Luaran penunjang (bukan klaim)

Macro/micro AUROC, AUPRC, F1-max, ECE, Brier

---

## 9. Rencana Analisis Statistik — DIBEKUKAN

| Perbandingan | Uji | Catatan |
|---|---|---|
| Cakupan vs nominal | Binomial eksak + CI Clopper-Pearson | Satu arah untuk H0 |
| Selisih cakupan antar metode | Uji permutasi berpasangan, 10.000 permutasi | **Permutasi pada level pasien** |
| Ranking lintas metode × dataset | Friedman + Nemenyi post-hoc + CD diagram | Protokol Demšar |
| Monotonisitas DEff ↔ deviasi (H0b, H2) | Korelasi Spearman | |
| CI seluruh metrik | Bootstrap 1.000 resample | **Resample pada level pasien** |
| Koreksi perbandingan ganda | **Holm-Bonferroni** dalam tiap keluarga hipotesis | |
| Ukuran efek | Cliff's delta | Wajib dilaporkan bersama p-value |

### ❗ Aturan bootstrap

Resampling **wajib** pada level pasien: ambil pasien dengan pengembalian, lalu sertakan **seluruh** rekaman pasien terpilih. Bootstrap per-rekaman akan mengulang persis kesalahan yang dikritik paper ini.

### Keluarga hipotesis untuk koreksi Holm-Bonferroni

| Keluarga | Anggota |
|---|---|
| F-A | H0 pada 3 level $\alpha$ |
| F-B | Perbandingan HiCoRC vs B12–B15 (4 uji) |
| F-C | Perbandingan HiCoRC vs B1–B6 (6 uji) |
| F-D | Cakupan per subkelompok (8 subkelompok: 4 kuartil umur × 2 jenis kelamin) |

Koreksi diterapkan **di dalam** keluarga, tidak lintas keluarga.

---

## 10. Konfigurasi yang Dijalankan

```
α          ∈ {0,01 · 0,05 · 0,10}
Granularitas ∈ {patient_id · site · nurse · device}
Metode     ∈ {HiCoRC + 7 ablasi} ∪ {B1…B15}
Seed       ∈ {0, 1, 2, 3, 4}
Resampling kalibrasi: 100 pengulangan pemisahan kalibrasi/uji
```

**Semua kombinasi dijalankan.** Tidak ada penyaringan pasca-hoc. Konfigurasi yang gagal (himpunan tak hingga) dilaporkan sebagai gagal, bukan dihapus.

> `strat_fold` dikecualikan sebagai unit kalibrasi karena kalibrasi memakai satu fold saja.

---

## 11. Aturan Keputusan

### Bila H0 terkonfirmasi

Lanjutkan sesuai rencana. Deviasi cakupan menjadi bukti C4.

### Bila H0 tidak konklusif di PTB-XL

**Jangan langsung menyerah, dan jangan mencari-cari analisis baru sampai signifikan.** Urutan yang dibolehkan:

1. Periksa H0b di MIT-BIH (design effect ~1.690× lebih besar). Jika terkonfirmasi di sana, kerangka tetap valid — PTB-XL sekadar kasus dependensi lemah.
2. Laporkan hasil PTB-XL apa adanya sebagai **temuan**: "pada design effect 1,39, koreksi blok hampir tidak diperlukan." Itu informasi berguna bagi praktisi.
3. Geser bobot naskah ke **C6+C7**, yang tidak bergantung pada H0 sama sekali.

### Bila H0 terrefutasi tegas

C4 dicabut. Naskah menjadi murni C6+C7+C8. Catat di §12 dan di log keputusan README.

### Bila H1 gagal (himpunan tidak menjadi tak hingga pada granularitas yang diprediksi)

**Implementasi Anda salah.** Teorema 1 bersifat deterministik di titik ini. Debug sebelum melanjutkan.

### Bila H3 dilanggar

Bug pada operator penutupan. Perbaiki; jangan laporkan.

---

## 12. Log Penyimpangan Protokol

Setiap penyimpangan dari protokol beku dicatat di sini. **Kolom terakhir adalah yang paling penting** — penyimpangan setelah melihat hasil harus dinyatakan di naskah.

| Tanggal | Penyimpangan | Alasan | Sebelum/sesudah melihat hasil? |
|---|---|---|---|
| | | | |

---

## 13. Checklist Sebelum Membekukan

- [ ] Seluruh angka di §3 diverifikasi terhadap data terunduh
- [ ] Backbone berhasil dilatih dan macro-AUROC dalam ±0,02 dari benchmark
- [x] **B12–B15 terimplementasi dan lolos unit test pada data sintetis** — selesai 2026-09-29, `src/conformal/`, 26 uji lolos, Teorema 1 & Proposisi 1 terverifikasi numerik
- [ ] Pipeline berjalan end-to-end pada fold 1–9 tanpa menyentuh fold 10
- [ ] Seluruh seed dan versi pustaka tercatat di `configs/`
- [ ] `git tag protocol-v1` dibuat
- [ ] Tanggal dan hash commit diisi di kepala dokumen ini

---

## 14. Checklist Sebelum Membuka Fold 10

> Fold 10 hanya boleh dibuka **satu kali**. Setelah dibuka, tidak ada perubahan metode yang diizinkan.

- [ ] Protokol sudah dibekukan dengan tag
- [ ] Seluruh pemilihan metode selesai berdasarkan fold 9
- [ ] Skor nonconformity final sudah dipilih
- [ ] Hiperparameter final sudah dikunci
- [ ] Skrip evaluasi fold 10 sudah ditulis dan diuji pada fold 9
- [ ] Tabel dan gambar naskah sudah disiapkan dengan placeholder
- [ ] Tanggal pembukaan fold 10: `__________`

---

## Lampiran A — Angka Referensi Terverifikasi

Dipakai untuk uji sanity pipeline. Bila pipeline Anda menghasilkan angka berbeda, ada yang salah.

| Besaran | Nilai |
|---|---:|
| Rekaman PTB-XL | 21.799 |
| Pasien PTB-XL | 18.869 |
| Kolom metadata | 28 |
| Rekaman di blok multi-rekaman | 5.041 (23,1%) |
| Design effect (patient_id) | 1,39 |
| $n_{\text{eff}}$ (patient_id) | 15.659 |
| $K_1$ kalibrasi (fold 9, patient_id) | 1.942 |
| Rekaman fold 9 / fold 10 | 2.183 / 2.198 |
| Rekaman fold 1–8 | 17.418 |
| Total label diagnostik | 27.765 |
| NORM · MI · STTC · CD · HYP | 9.514 · 5.469 · 5.235 · 4.898 · 2.649 |
| Anotasi detak MIT-BIH | 112.647 |
| Rata-rata detak per rekaman | 2.347 |

Sumber: `results/raw/dataset_verification.json`, `block_structure.json`, `feasibility_alpha.json`
