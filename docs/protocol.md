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
| ~~Ranking lintas metode × dataset~~ | ~~Friedman + Nemenyi post-hoc + CD diagram~~ | **DICABUT 2026-09-30** — lihat di bawah |
| Monotonisitas DEff ↔ deviasi (H0b, H2) | Korelasi Spearman | |
| CI seluruh metrik | Bootstrap 1.000 resample | **Resample pada level pasien** |
| Koreksi perbandingan ganda | **Holm-Bonferroni** dalam tiap keluarga hipotesis | |
| Ukuran efek | Cliff's delta | Wajib dilaporkan bersama p-value |

### ❗ Friedman + Nemenyi dicabut

Prosedur Demšar dirancang untuk membandingkan banyak pengklasifikasi **lintas banyak dataset** — lazimnya minimal lima. Rancangan ini memakai **dua** dataset (PTB-XL dan MIT-BIH), sehingga uji Friedman tidak bermakna dan CD diagram tidak dapat dibaca.

Penggantinya sudah dipakai konsisten sejak awal: **CI bootstrap pada level blok, 200 ulangan**, ditambah uji permutasi berpasangan. Keduanya tidak memerlukan asumsi ranking lintas dataset.

Konsekuensi turunan: rujukan Demšar 2006 dicabut dari daftar pustaka — lihat [references.md §6a](references.md).

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
| 2026-09-30 | Studi kelayakan memakai fold 1–6 latih, 7 validasi, **9 dibagi level-pasien** untuk kalibrasi/uji — bukan split konfirmatori 1–8 / 9 / 10 | Menjaga fold 10 tetap perawan. Studi ini **eksploratoris**, bukan konfirmatori | **Sebelum** |
| 2026-09-30 | Rancangan awal studi kelayakan (kalibrasi fold 8 → uji fold 9) **dibatalkan** dan diganti | Fold 1–8 hanya 64–68% divalidasi manusia; fold 9–10 100%. Rancangan itu mencampurkan **pergeseran kualitas label** ke dalam pengukuran cakupan | **Sesudah** melihat hasil pertama — dinyatakan terbuka; hasil pertama **tidak dipakai** |
| 2026-09-30 | Uji H0 diperluas: selain "B1 kurang-cakup", ditambahkan CI untuk **selisih B12−B1** | Versi pertama hanya menguji bagian (a) H0. Mekanisme H0 justru terletak pada selisihnya | **Sesudah** — perbaikan metodologis, memperketat uji bukan melonggarkan |
| 2026-09-30 | **Kontrol permutasi** ditambahkan pada MIT-BIH (lengan blok-teracak sebagai null tersuai) | Kriteria (b) "B12 > B1" dicurigai tautologis: pada $K_1{=}11$, atom $+\infty$ memaksa HCP menembus persentil ke-98,2, bukan ke-90. Dugaan terbukti — **81–107% selisih bersifat mekanis** | **Sesudah** — dinyatakan **post-hoc**. Uji ini memperketat, bukan melonggarkan: ia **membatalkan** kriteria yang semula mendukung hipotesis |
| 2026-09-30 | Kriteria H0b pra-registrasi (Spearman DEff ↔ deviasi) **tidak dapat dijalankan** sebagaimana ditulis | Dengan dua dataset, $\rho$ hanya bisa $\pm 1$ dan $p$ tak terdefinisi. Cacat pra-registrasi. Diganti uji monotonisitas **di dalam** MIT-BIH dengan 11 titik DEff | **Sesudah** — hasilnya **1/3 alpha, pola non-monoton**; dilaporkan sebagai temuan negatif |
| 2026-09-30 | **Friedman + Nemenyi + CD diagram dicabut** dari §9 | Prosedur Demšar menuntut banyak dataset (lazimnya ≥5); rancangan ini memakai dua. Uji tidak bermakna | **Sebelum** — tak satu pun hasil Friedman pernah dihitung |
| 2026-09-30 | Tuas uji monotonisitas diganti dari **ukuran blok** menjadi **ICC**, lalu sumbu pelaporan menjadi **DEff** | Faktorial 2×2 menunjukkan ukuran blok bukan penggerak (0/3 signifikan) sedangkan klaster ya (3/3). Uji monotonisitas pertama karena itu memutar tuas yang salah | **Sesudah** — dinyatakan terbuka. Uji pertama dilaporkan apa adanya sebagai **temuan negatif**, tidak disembunyikan |
| 2026-09-30 | Sumbu dosis-respons ditetapkan **DEff**, bukan ICC | PTB-XL ber-ICC 0,3525 namun defisit nol; ICC saja gagal menyatukan kedua dataset. Prop 2' ($H{=}1{,}05 \Rightarrow \mathrm{DEff}{=}1{,}02$) menjelaskannya | **Sesudah** — tetapi sumbunya adalah besaran yang **sudah ada di teori sebelum data dilihat**, bukan dipilih agar cocok |
| 2026-10-01 | **Analisis sensitivitas checkpoint** ditambahkan pada eksperimen invariansi backbone (rincian di bawah) | `mitdb_resnet1d50` memilih bobot **epoch 1** karena rugi validasi tidak pernah membaik lagi; set validasi MIT-BIH hanya **4 rekaman** sehingga rugi validasinya bising (0,144–0,474). Reviewer dapat menyebut model itu kurang terlatih | **Sesudah** melihat riwayat rugi validasi, **sebelum** melihat hasil konformal dari checkpoint alternatif. **Analisis utama tidak diubah** |

### Pra-registrasi analisis sensitivitas checkpoint — ditulis 2026-10-01 sebelum dijalankan

**Pertanyaan.** Apakah temuan konformal bergantung pada checkpoint mana yang dipilih oleh set validasi 4 rekaman?

**Rancangan.** Untuk setiap backbone yang dilatih (`resnet1d34`, `resnet1d50`) pada setiap dataset, audit konformal diulang memakai **bobot epoch terakhir** (yang tersimpan saat pelatihan berhenti) menggantikan **bobot terbaik-validasi**. Protokol lain identik: split, $\alpha$, 200 split acak level-blok, seed. `SmallECGNet` dikecualikan karena checkpoint lamanya hanya menyimpan bobot terbaik.

**Kriteria — ditetapkan sekarang, tidak diubah sesudah hasil keluar.**

| Kriteria | Lolos bila |
|---|---|
| **S-1** arah perbaikan HCP | `B12_memperbaiki` (CI selisih B12−B1 di atas nol) **sama** untuk kedua checkpoint pada **setiap** $\alpha$ |
| **S-2** arah kurang-cakup B1 | tanda defisit B1 **sama** untuk kedua checkpoint pada setiap $\alpha$ |
| **S-3** kontrol negatif | $K_1(\ell)$ identik — wajib, karena tidak bergantung bobot |

**Pelaporan.** Analisis utama tetap memakai bobot terbaik-validasi sebagaimana ditetapkan. Hasil sensitivitas dilaporkan **apa pun hasilnya**, di naskah §8 dan §11. Bila S-1 gagal pada suatu $\alpha$, naskah wajib menyatakan bahwa temuan pada $\alpha$ itu peka terhadap pemilihan checkpoint.

**Yang tidak dilakukan.** Aturan pemilihan model utama **tidak** diganti, dan tidak satu pun backbone dilatih ulang dengan aturan berbeda sebelum hasil ini keluar. Mengganti aturan sesudah melihat hasil adalah *p-hacking*.

**Hasil MIT-BIH — 2026-10-01** (`*_terakhir.json`; dinilai otomatis oleh `scripts/summarize_backbone_invariance.py`)

| Backbone | Epoch terbaik-val → terakhir | S-1 | S-2 | S-3 | Vonis |
|---|---|:-:|:-:|:-:|:-:|
| `resnet1d34` | 8 → 13 | 5/5 | 5/5 | ya | **LOLOS** |
| `resnet1d50` | 1 → 6 | 5/5 | 5/5 | ya | **LOLOS** |

Defisit B1 (pp), terbaik-val → terakhir:

| $\alpha$ | `resnet1d34` | `resnet1d50` |
|---|---|---|
| 0,01 | −2,09 → −1,69 | −1,73 → −2,57 |
| 0,05 | −1,00 → −1,08 | −1,38 → −2,38 |
| 0,10 | −1,16 → −1,15 | −2,54 → −2,79 |
| 0,15 | −1,01 → −1,42 | −3,41 → −1,70 |
| 0,20 | −0,81 → −1,51 | −3,18 → −1,36 |

**Tafsiran yang wajib dibawa ke naskah.**
1. **Arah** temuan (B1 kurang-cakup; B12 memulihkan) tahan terhadap pemilihan checkpoint di 20/20 sel.
2. **Besaran** defisit **tidak** tahan: berubah hingga 1,8 pp, dan urutan antar-backbone berubah. Klaim "besaran tidak monoton terhadap kapasitas" karena itu **tidak boleh** diangkat sebagai temuan, sebab ia ada dalam rentang derau pemilihan checkpoint. Naskah hanya mengklaim arah.
3. Bobot epoch 6 `resnet1d50` (rugi latih 0,035 vs 0,161 di epoch 1) memberi kesimpulan yang sama, sehingga temuan tidak bergantung pada model yang "kurang terlatih".

PTB-XL — 2026-10-02, kriteria yang sama:

| Backbone | Epoch terbaik-val → terakhir | S-1 | S-2 | S-3 | Vonis |
|---|---|:-:|:-:|:-:|:-:|
| `resnet1d34` | 9 → 14 | 3/3 | 3/3 | ya | **LOLOS** |
| `resnet1d50` | 7 → 12 | 3/3 | 3/3 | ya | **LOLOS** |

Di PTB-XL, defisit B1 tetap positif (+0,05 sampai +0,19 pp) pada kedua checkpoint, artinya tidak ada kurang-cakup. HCP tidak memperbaiki karena memang tidak ada yang perlu diperbaiki.

**Catatan sel batas.** Tiga CI selisih B12−B1 mempunyai ujung **tepat 0,0**: PTB-XL `small` $\alpha{=}0{,}01$ dan `resnet1d50` $\alpha{=}0{,}10$ (utama), serta `resnet1d34` $\alpha{=}0{,}05$ (terakhir). Cakupan adalah proporsi diskret, sehingga ujung CI persentil dapat jatuh tepat di nol. Aturan `B12_memperbaiki = batas_bawah > 0` (ketidaksamaan ketat, ditetapkan sebelum eksperimen) menggolongkannya sebagai **tidak memperbaiki**. Vonis pada sel ini bergantung pada ketatnya ketidaksamaan, dan dilaporkan demikian.

---

## 12b. Hasil Studi Kelayakan (Langkah 4) — 2026-09-30

**Desain:** latih fold 1–6 · validasi fold 7 · evaluasi = fold 9 dibagi level-pasien, **200 pengulangan**. Kedua sisi 100% tervalidasi manusia. Fold 10 tidak disentuh.
Backbone: `SmallECGNet` 104.389 parameter, macro-AUROC **0,9016**.

| $\alpha$ | Target | B1 naif (CI95) | B12 HCP (CI95) | Selisih B12−B1 (CI95) |
|---:|---:|---|---|---|
| 0,01 | 0,99 | **0,9910** [0,9823; 0,9972] | 0,9912 [0,9822; 0,9973] | $+0{,}00027$ [$0{,}00000$; $+0{,}00282$] |
| 0,05 | 0,95 | **0,9511** [0,9318; 0,9673] | 0,9510 [0,9318; 0,9673] | $-0{,}00015$ [$-0{,}00467$; $+0{,}00468$] |
| 0,10 | 0,90 | **0,9010** [0,8741; 0,9256] | 0,9002 [0,8728; 0,9231] | $-0{,}00078$ [$-0{,}00564$; $+0{,}00379$] |

| Bagian H0 | Hasil |
|---|---|
| (a) B1 kurang-cakup | **0 / 3** |
| (b) B12 memperbaikinya | **0 / 3** |

### ❌ Putusan: H0 TERREFUTASI TEGAS pada granularitas pasien PTB-XL

Cakupan split conformal naif **tepat di nominal**, bukan di bawahnya. Koreksi blok tidak memberi efek yang dapat dibedakan dari nol.

**Penyebab struktural — bukan kegagalan pengukuran.** Pada fold 9: rata-rata $N_k = 1{,}1195$, **90,5% pasien hanya punya satu rekaman**, dan rasio bobot atom $+\infty$ antara HCP dan split hanya **1,12×**. Secara konstruksi HCP tidak dapat berbeda di sini. Ini konsisten dengan $\mathrm{DEff}_{\text{blok}} = 1{,}2$ yang sudah terukur sejak awal.

**Mutu backbone tidak menjelaskan hasil ini.** Jaminan conformal bersifat model-agnostik: model lemah menghasilkan himpunan lebih lebar, bukan cakupan lebih rendah. macro-AUROC 0,9016 (vs benchmark ~0,93) memengaruhi $|C|$, bukan validitas.

**Justru sebaliknya, ini kontrol positif yang lolos.** Split conformal mencapai cakupan nominal **secara persis** — persis yang harus terjadi bila exchangeability berlaku. Hasil nol ini memvalidasi implementasi skor, kalibrasi, dan evaluasi sekaligus.

### Tindakan menurut §11

Aturan "H0 tidak konklusif" butir 1 berlaku dan **harus dijalankan sebelum C4 dicabut**:

1. **Uji H0b di MIT-BIH** (~2.347 detak per rekaman — tiga orde lebih besar). Bila terkonfirmasi di sana, kerangka tetap valid; PTB-XL sekadar kasus dependensi lemah.
2. Laporkan hasil PTB-XL apa adanya sebagai **temuan**: *"pada design effect 1,2, koreksi blok tidak diperlukan."*
3. Geser bobot naskah ke **C6+C7+C8**, yang tidak bergantung pada H0 sama sekali.

> 🎯 **Butir 2 sudah tertulis di §11 sebelum hasil terlihat.** Melaporkannya karena itu **bukan rasionalisasi pasca-hoc** — ini tafsiran yang sudah dipra-registrasi. Protokolnya bekerja.

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
