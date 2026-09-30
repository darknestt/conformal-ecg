# How Study Design Determines Distribution-Free Guarantees in Clinical Multi-Label Prediction

> ⚠️ **JUDUL SEDANG DIREVISI.** Judul lama — *Hierarchy-Aware Conformal Risk Control for Multi-Label Clinical Time Series under Patient-Level Dependence* — menjanjikan kontribusi teoretis (C1) yang **ternyata sudah diterbitkan orang lain**. Lihat §4.0.
>
> **Kandidat judul baru:**
>
> 1. *How Study Design Determines Distribution-Free Guarantees in Clinical Multi-Label Prediction* — menekankan C6, menjawab langsung pertanyaan terbuka Lee-Barber-Willett
> 2. *Group Count or Group Size? Feasibility Limits of Hierarchical Conformal Prediction on Clinical ECG* — lebih spesifik, memuat temuan dua-batas
> 3. *Hierarchical Conformal Prediction for Multi-Label ECG: Feasibility Limits and a Block-Sufficiency Diagnostic* — memuat C7 dan C8 sekaligus
>
> **Pilih setelah C6 berhasil diformalkan di F1.** Jangan mengunci judul sebelum kontribusi final.

> **Judul (ID):** Bagaimana Desain Studi Menentukan Jaminan Bebas-Distribusi pada Prediksi Klinis Multi-Label
>
> **Running title:** Feasibility Limits of Hierarchical Conformal Prediction
>
> **Status:** `PLANNING` — belum ada eksperimen dijalankan
> **Dibuat:** 2026-09-29 · **Direvisi:** 2026-09-29 (survei literatur mengubah arah kontribusi — lihat §4)
> **Target:** Artikel jurnal Scopus Q1 — **jalur klinis/terapan**: IEEE JBHI, Artificial Intelligence in Medicine, Computers in Biology and Medicine, Medical Image Analysis

---

## Daftar Isi

1. [Ringkasan Eksekutif](#1-ringkasan-eksekutif)
2. [Latar Belakang & Motivasi](#2-latar-belakang--motivasi)
3. [Research Problem, Questions, Objectives](#3-research-problem-questions-objectives)
4. [Research Gap & Novelty](#4-research-gap--novelty)
5. [Dataset](#5-dataset)
6. [Metode yang Diusulkan (HiCoRC)](#6-metode-yang-diusulkan-hicorc)
7. [Baseline](#7-baseline)
8. [Desain Eksperimen](#8-desain-eksperimen)
9. [Metrik Evaluasi](#9-metrik-evaluasi)
10. [Uji Statistik](#10-uji-statistik)
11. [Threats to Validity](#11-threats-to-validity)
12. [Struktur Artikel](#12-struktur-artikel)
13. [Rencana Kerja & Milestone](#13-rencana-kerja--milestone)
14. [Struktur Repositori](#14-struktur-repositori)
15. [Lingkungan & Hardware](#15-lingkungan--hardware)
16. [Checklist Pra-Penelitian](#16-checklist-pra-penelitian)
17. [Status Verifikasi Referensi](#17-status-verifikasi-referensi)
18. [Log Keputusan](#18-log-keputusan)

---

## 1. Ringkasan Eksekutif

Model deep learning untuk interpretasi EKG melaporkan AUROC tinggi, tetapi **tidak memberikan jaminan statistik apa pun** atas keluarannya. Conformal prediction menawarkan jaminan cakupan bebas distribusi, namun asumsi dasarnya — **exchangeability** — dilanggar secara sistematis pada data klinis nyata karena:

1. **Dependensi tingkat pasien** — beberapa rekaman berasal dari individu yang sama.
2. **Struktur label hierarkis** — diagnosis tersusun sebagai `superclass -> subclass`.
3. **Sifat multi-label** — satu rekaman dapat memiliki beberapa diagnosis simultan.

Prediksi konformal hierarkis (HCP; Lee, Barber & Willett 2026) sudah menyelesaikan masalah **validitas** di bawah dependensi blok. Yang belum terjawab — dan dinyatakan terbuka oleh penulisnya sendiri — adalah **bagaimana desain studi menentukan apakah jaminan itu dapat ditegakkan sama sekali**, serta bagaimana memperluasnya ke keluaran multi-label berhierarki. Penelitian ini menjawab keduanya pada data EKG klinis nyata.

**Kontribusi utama** — direvisi 2026-09-29 setelah survei literatur:

| # | Jenis | Deskripsi | Status |
|---|---|---|---|
| ~~C1~~ | ~~Teoretis~~ | ~~Teorema cakupan finite-sample untuk kalibrasi blok-pasien~~ | ❌ **DICABUT** — sudah diterbitkan Lee, Barber & Willett (ACM J. Data Science 2026). Lihat §4.0 |
| C2 | Lema | Penutupan hierarkis mempertahankan validitas cakupan | ⚠️ Diturunkan dari "teorema" ke lema pendukung — argumennya terlalu pendek untuk klaim utama |
| C3 | Metodologis | Algoritma `HiCoRC` yang model-agnostic | ✅ |
| C4 | Empiris | Bukti kuantitatif bahwa conformal naif **gagal** pada EKG klinis multi-label hierarkis | ✅ **Menguat** — literatur yang ada murni teoretis |
| C5 | Artefak | Pustaka Python open-source + reproduksi penuh (GitHub + Zenodo DOI) | ✅ |
| **C6** | **Teoretis-empiris** | **Karakterisasi tradeoff $K$ blok vs $N_k$ pengukuran**: validitas dibatasi $\alpha > 1/(K_1+1)$, efisiensi dibatasi design effect, dan keduanya **tidak berkorelasi** | ✅ **Kontribusi utama** — dinyatakan sebagai pertanyaan terbuka oleh Lee-Barber-Willett sendiri |
| **C7** | **Metodologis** | **Uji diagnostik kecukupan blok** — menentukan granularitas mana yang layak dikalibrasi, **sebelum** model dilatih | ✅ **Kontribusi utama** |
| **C8** | **Metodologis** | **Perluasan HCP dari regresi skalar ke himpunan prediksi multi-label berhierarki** | ✅ HCP dirumuskan untuk $\hat\mu(x) \pm T$; jembatan ke multi-label belum ada |

> **Pembeda utama kini adalah C6 + C7**, bukan C1 + C2. Lihat [§4 Research Gap](#4-research-gap--novelty) untuk alasan lengkapnya.

---

## 2. Latar Belakang & Motivasi

### 2.1 Kebutuhan regulatif

- EU AI Act mengategorikan sistem AI medis sebagai *high-risk*, menuntut kuantifikasi ketidakpastian yang dapat dipertanggungjawabkan.
- FDA Software as a Medical Device (SaMD) menuntut karakterisasi performa yang dapat diverifikasi.
- Probabilitas softmax **bukan** jaminan statistik — model dapat 99% yakin dan tetap salah.

### 2.2 Mengapa conformal prediction

Conformal prediction menghasilkan **himpunan prediksi** dengan jaminan:

$$P(Y_{n+1} \in \mathcal{C}(X_{n+1})) \geq 1 - \alpha$$

tanpa asumsi distribusi, **asalkan** data exchangeable.

### 2.3 Mengapa asumsi itu gagal di klinik

| Pelanggaran | Bukti pada PTB-XL |
|---|---|
| Dependensi pasien | 21.799 rekaman dari **18.869 pasien** -> banyak pasien punya >1 rekaman |
| Hierarki label | `scp_statements.csv` menyediakan `diagnostic_class` dan `diagnostic_subclass` |
| Multi-label | Jumlah pernyataan melebihi jumlah rekaman (label ganda per rekaman) |

> **Hipotesis inti H0:** Split conformal standar akan menghasilkan cakupan empiris **di bawah** target nominal pada PTB-XL bila kalibrasi dilakukan per-sampel, dan deviasi ini membesar seiring meningkatnya rata-rata rekaman per pasien.

---

## 3. Research Problem, Questions, Objectives

### 3.1 Research Problem

Prediksi konformal hierarkis (HCP) memulihkan validitas cakupan di bawah dependensi blok, tetapi **hanya untuk regresi bernilai skalar** dan **tanpa panduan tentang granularitas blok mana yang layak dipakai**. Pada data klinis nyata, blok tersedia di banyak tingkat sekaligus (pasien, perangkat, perawat, situs) dengan jumlah blok yang sangat berbeda — dan sebagian di antaranya membuat jaminan non-trivial **mustahil** pada level $\alpha$ yang lazim. Praktisi tidak punya cara menentukan tingkat mana yang layak, dan tidak ada prosedur yang membawa jaminan ini ke keluaran diagnosis multi-label berhierarki.

### 3.2 Research Questions

| ID | Pertanyaan |
|---|---|
| **RQ1** | Seberapa besar deviasi cakupan empiris dari nominal ketika split conformal standar diterapkan pada data klinis dengan dependensi pasien? |
| **RQ2** | Pada tingkat granularitas blok mana jaminan cakupan non-trivial masih **mungkin**, dan bagaimana batas $\alpha > 1/(K_1+1)$ berinteraksi dengan design effect? |
| **RQ3** | Bagaimana HCP diperluas dari regresi skalar ke himpunan prediksi multi-label berhierarki, dan berapa harga efisiensi penutupan hierarkis? |
| **RQ4** | Apakah kendali risiko terkondisi-kelompok menghasilkan cakupan yang adil lintas subkelompok umur/jenis kelamin, dibandingkan kendali marginal? |
| **RQ5** | Seberapa jauh temuan RQ1–RQ4 bertahan pada dataset dengan intensitas dependensi berbeda (MIT-BIH, Challenge 2021)? |

### 3.3 Research Objectives

- **O1** Memperluas HCP (Lee dkk., 2026) dari regresi skalar ke **himpunan prediksi multi-label berhierarki** — C8.
- **O2** Mengarakterisasi tradeoff $K$ blok vs $N_k$ pengukuran: memisahkan batas **validitas** ($\alpha > 1/(K_1+1)$) dari batas **efisiensi** (design effect) — C6.
- **O3** Merumuskan dan memvalidasi **uji diagnostik kecukupan blok** yang berjalan sebelum pelatihan model — C7.
- **O4** Memvalidasi secara empiris pada >= 2 dataset klinis dengan intensitas dependensi berbeda.
- **O5** Merilis artefak reproduksi penuh.

> O1 dan O2 versi pertama ("menurunkan dan membuktikan batas cakupan finite-sample untuk kalibrasi blok-pasien") **dihapus** — sudah dikerjakan Lee-Barber-Willett. Lihat §4.0.

---

## 4. Research Gap & Novelty

> 🚨 **BAGIAN INI DIREVISI TOTAL pada 2026-09-29** setelah survei literatur dikerjakan. Klaim gap versi pertama **tidak bertahan**. Baca seluruhnya sebelum melanjutkan.

### 4.0 ❗ HASIL SURVEI LITERATUR — C1 SUDAH TERTUTUP

**Temuan menentukan:**

> Lee Y., **Barber R.F.**, Willett R. *Distribution-free inference with hierarchical data*. **ACM Journal of Data Science**, 2026. DOI: https://doi.org/10.1145/3786352 · arXiv:2306.06342 (sejak Juni 2023)

Kutipan langsung dari abstraknya:

> *"This paper studies distribution-free inference in settings where the data set has a hierarchical structure — for example, **groups of observations, or repeated measurements**. In such settings, **standard notions of exchangeability may not hold**. To address this challenge, **a hierarchical form of exchangeability is derived**, facilitating extensions of distribution-free methods, **including conformal prediction and jackknife+**."*

**Ini persis C1.** "Kelompok observasi atau pengukuran berulang" adalah blok pasien. Mereka bahkan melampauinya dengan properti *second-moment coverage* untuk kendali miscoverage terkondisi.

**Konsekuensi yang harus diterima:**

| Kontribusi lama | Status | Tindakan |
|---|---|---|
| **C1** Teorema cakupan finite-sample kalibrasi blok-pasien | ❌ **TERTUTUP** | Hapus sebagai klaim. **Pakai** teorema mereka sebagai fondasi. |
| **C2** Penutupan hierarkis mempertahankan validitas | ⚠️ **LEMAH** | Argumennya hanya beberapa baris (monoton + ekspansif). Terlalu tipis untuk klaim teoretis Q1. Ada pula arXiv:2410.06296 (Bastani dkk.) pada DAG label hierarkis. Turunkan menjadi lema pendukung. |
| **C3** Algoritma model-agnostic | ✅ Aman | Tetap |
| **C4** Bukti empiris kegagalan conformal naif | ✅ **Menguat** | Lee-Barber-Willett murni teoretis. Belum ada yang menunjukkan ini pada data EKG klinis multi-label berskala. |
| **C5** Artefak reproduksi | ✅ Aman | Tetap |

### 4.1 Celah yang MASIH terbuka — dan ini yang harus dikejar

#### 🎯 Penulisnya sendiri menyatakan C6 sebagai pertanyaan terbuka

Saya membaca teks lengkap Lee-Barber-Willett. Di bagian **Discussion** mereka menulis:

> *"In many statistical applications, the hierarchical structure of the sampling scheme is (at least partially) controlled by the analyst designing the study. In particular, this means that the analyst can choose between, say, **a large number of independent groups $K$ with a small number of measurements $N_k$ within each group, or conversely a small number of groups with large numbers of repeats. Characterizing the pros and cons of this tradeoff is an important question to determine how study design affects inference in this distribution-free setting.**"*

**Itu adalah C6, dinyatakan sebagai masalah terbuka oleh orang yang membangun teorinya.** Ini validasi terkuat yang bisa Anda dapatkan: bukan Anda yang mengklaim ada celah, melainkan Barber sendiri yang menyatakannya.

Dan Anda sudah memiliki datanya: lima tingkat granularitas terukur pada satu dataset klinis nyata, dari $K_1 = 8$ sampai $K_1 = 1.942$.

#### Tiga celah konkret

| Celah | Mengapa terbuka | Bukti yang sudah Anda punya |
|---|---|---|
| **G1 — Tradeoff $K$ vs $N_k$ pada data nyata** | Dinyatakan terbuka di Discussion Lee-Barber-Willett. Simulasi mereka hanya memakai $K \in \{20, 100, 800, 1000\}$ dengan $N_k$ konstan dan data sintetis | §5.6 Temuan 4: lima granularitas, $K_1$ dari 8 hingga 1.942, $N_k$ sangat tidak seragam (1–10 untuk pasien, 1–8.940 untuk situs) |
| **G2 — Uji diagnostik kecukupan blok** | Tidak ada prosedur untuk memutuskan granularitas mana yang layak. Praktisi harus menebak | §5.6 Temuan 4: batas $\alpha > 1/(K_1+1)$ terhitung eksak per granularitas |
| **G3 — Multi-label hierarkis klinis** | HCP diuji pada **regresi** (residual absolut, Lorenz 96). Tidak ada pengujian pada himpunan prediksi multi-label, apalagi dengan hierarki label | PTB-XL: 27.765 label, 44 pernyataan diagnostik berhierarki, 23,1% rekaman di blok multi-rekaman |

> ❗ **Jarak antara HCP dan kebutuhan Anda lebih lebar dari dugaan awal.** HCP adalah metode **regresi** yang menghasilkan interval $\hat\mu(x) \pm T$. Anda butuh **himpunan label multi-label berhierarki**. Menjembataninya bukan pekerjaan sepele — dan itu justru ruang kontribusi C3.

### 4.2 Klaim yang direkomendasikan

> Kami **mengoperasionalkan** prediksi konformal hierarkis (HCP; Lee dkk., 2026) untuk klasifikasi EKG **multi-label berhierarki** — perluasan non-trivial, karena HCP dirumuskan untuk regresi bernilai skalar. Kami kemudian menjawab pertanyaan terbuka yang diajukan penulisnya sendiri: bagaimana desain studi ($K$ blok versus $N_k$ pengukuran) menentukan inferensi bebas-distribusi. Kami menunjukkan bahwa **validitas** dibatasi jumlah blok ($\alpha > 1/(K_1+1)$) sedangkan **efisiensi** dibatasi design effect, bahwa kedua batas ini tidak berkorelasi, dan bahwa keduanya menghasilkan rekomendasi granularitas yang berbeda pada data klinis nyata. Kami menyediakan uji diagnostik yang menentukan tingkat blok mana yang layak dikalibrasi sebelum model apa pun dilatih.

**Mengapa ini tetap layak Q1:**

- Menjawab **pertanyaan terbuka yang dinyatakan eksplisit** oleh penulis teorema rujukan — argumen novelty terkuat yang tersedia
- Perluasan regresi → multi-label berhierarki adalah kontribusi metodologis nyata, bukan penerapan ulang
- Temuan "dua batas tidak berkorelasi" bersifat kontra-intuitif dan langsung berguna
- Uji diagnostik berjalan **sebelum pelatihan model** — artefak yang langsung dipakai praktisi
- Risiko teoretis rendah: fondasinya sudah terbit dan teruji

**Mengapa targetnya bergeser:**

| | Sebelum | Sesudah |
|---|---|---|
| Venue realistis | Jurnal statistika (AoS, JRSS-B) | **Jurnal klinis/terapan**: IEEE JBHI, Artificial Intelligence in Medicine, Computers in Biology and Medicine, Medical Image Analysis |
| Pembeda utama | Teorema baru | Karakterisasi batas + diagnostik + validasi klinis |
| Kebutuhan kolaborator statistika | Mutlak | Tetap dianjurkan, tidak lagi mutlak |

> Semua venue di atas tetap **Scopus Q1**. Yang berubah adalah jenis kontribusinya, bukan tingkatannya.

### 4.3 Yang sudah diverifikasi TIDAK menutup kontribusi Anda

| Paper | Mengapa tidak menutup |
|---|---|
| B1 `10.1098/rsta.2025.0071` | Review; membahas dependensi **antar-label**, bukan antar-sampel |
| B3 `10.1016/j.patcog.2021.108271` | Sumbunya efisiensi komputasi Label Powerset, domain teks |
| B2 `10.1016/j.rinam.2025.100589` | **Irisan** lintas-resolusi dengan pembagian $\alpha$ — arah berlawanan dengan penutupan ke atas |
| A3 `10.1214/26-ejs2506` | Kelompok menentukan **pergeseran kovariat**; exchangeability di dalam kelompok tetap berlaku |

Rincian lengkap beserta kutipan: [`docs/references.md`](docs/references.md).

---

## 5. Dataset

### 5.1 Dataset Utama — PTB-XL ✅ TERVERIFIKASI

| Atribut | Nilai |
|---|---|
| Sumber | PhysioNet |
| URL | https://physionet.org/content/ptb-xl/1.0.3/ |
| Versi | 1.0.3 (9 Nov 2022) |
| Jumlah rekaman | **21.799** |
| Jumlah pasien | **18.869** |
| Format sinyal | 12-lead, 10 detik, WFDB 16-bit, 1 uV/LSB |
| Sampling rate | 500 Hz (`records500/`) dan 100 Hz (`records100/`) |
| Pernyataan label | **71 pernyataan SCP-ECG** |
| Metadata | `ptbxl_database.csv`, **28 kolom** |
| Hierarki label | `scp_statements.csv` -> `diagnostic_class`, `diagnostic_subclass` |
| Split resmi | 10 fold; **fold 1–8 train, 9 val, 10 test**; pasien tidak menyeberang fold |
| Kualitas label | Fold 9–10 telah melalui evaluasi manusia (kualitas tertinggi) |
| Lisensi | **CC BY 4.0** — Anyone can access |
| Ukuran | ZIP 1,7 GB; uncompressed 3,0 GB |
| DOI | https://doi.org/10.13026/kfzx-aw45 |

**Distribusi superclass diagnostik:**

| Superclass | Jumlah | Keterangan |
|---|---|---|
| NORM | 9.514 | Normal ECG |
| MI | 5.469 | Myocardial Infarction |
| STTC | 5.235 | ST/T Change |
| CD | 4.898 | Conduction Disturbance |
| HYP | 2.649 | Hypertrophy (kelas minoritas) |

> Jumlah melebihi total rekaman karena **multi-label**.

**Metadata penting untuk analisis subgrup & XAI:**
`age`, `sex`, `height`, `weight`, `device`, `recording_date`, `static_noise`, `burst_noise`, `baseline_drift`, `electrodes_problems`, `extra_beats`, `pacemaker`, `validated_by_human`, `second_opinion`

> ⚠️ **`recording_date` adalah tanggal TERGESER.** Dokumentasi resmi menyatakan: *"all ECG recording dates were shifted by a random offset for each patient"*. Data terunduh memang menunjukkan rentang 1984-11-09 → 2001-06-11, padahal periode pengumpulan sesungguhnya Oktober 1989–Juni 1996.
>
> **Konsekuensi:** tanggal absolut **tidak bermakna** — setiap analisis temporal shift berbasis kalender akan mengukur derau pseudonimisasi, bukan pergeseran distribusi. Namun karena offset **konstan per pasien**, **interval antar-rekaman dalam satu pasien tetap valid** dan dapat dieksploitasi (lihat E11).

### 5.2 Dataset Pendukung — MIT-BIH Arrhythmia ✅ TERVERIFIKASI

| Atribut | Nilai |
|---|---|
| URL | https://physionet.org/content/mitdb/1.0.0/ |
| Rekaman | **48 rekaman** setengah jam, 2 kanal |
| Subjek | **47 subjek** |
| Sampling | **360 Hz**, resolusi 11-bit, rentang 10 mV |
| Anotasi | **± 110.000 anotasi detak**, divalidasi >= 2 kardiolog |
| Lisensi | **Open Data Commons Attribution License v1.0** |
| Ukuran | ZIP 73,5 MB; uncompressed 104,3 MB |
| DOI | https://doi.org/10.13026/C2F305 |

### 5.3 Dataset Robustness — MIT-BIH Noise Stress Test ✅ TERVERIFIKASI

| Atribut | Nilai |
|---|---|
| URL | https://physionet.org/content/nstdb/1.0.0/ |
| Rekaman EKG | **12** rekaman setengah jam (basis 118 & 119 dari MIT-BIH) |
| Rekaman noise | **3**: `bw` (baseline wander), `ma` (muscle artifact), `em` (electrode motion) |
| Level SNR | **24, 18, 12, 6, 0, −6 dB** |
| Anotasi | Salinan anotasi rekaman bersih → ground truth tetap valid |
| Lisensi | **Open Data Commons Attribution License v1.0** |
| Ukuran | ZIP 67,7 MB |
| DOI | https://doi.org/10.13026/C2HS3T |

**Nilai strategis:** SNR adalah *covariate shift terkendali*. Memungkinkan pengukuran presisi pada degradasi tingkat berapa jaminan cakupan mulai gagal — jauh lebih kuat daripada noise sintetis buatan sendiri.

### 5.4 Dataset Generalisasi — PhysioNet/CinC Challenge 2021 ✅ TERVERIFIKASI

| Atribut | Nilai |
|---|---|
| URL | https://physionet.org/content/challenge-2021/1.0.3/ |
| Data publik (training) | **88.253 rekaman** 12-lead dari 8 folder |
| Label | **SNOMED-CT, multi-label**, di header WFDB `#Dx:` |
| Format | `.mat` (MATLAB v4) + `.hea` (WFDB header) |
| Lisensi | **CC BY 4.0** |
| Ukuran | 12,6 GB |
| DOI | https://doi.org/10.13026/34va-7q14 |

**Rincian folder:** `cpsc_2018` 6.877 · `cpsc_2018_extra` 3.453 · `st_petersburg_incart` 74 · `ptb` 516 · `ptb-xl` 21.837 · `georgia` 10.344 · `chapman-shaoxing` 10.247 · `ningbo` 34.905

⚠️ **Dua peringatan wajib:**
1. Folder `ptb-xl` **duplikat dengan Bagian 5.1** → **harus dikecualikan** dari klaim generalisasi.
2. **Tidak ada `patient_id`** di header (hanya `#Age`, `#Sex`, `#Dx`, `#Rx`, `#Hx`, `#Sx`). Blok yang tersedia adalah **tingkat situs/sumber**, bukan tingkat pasien.

### 5.5 UEA/UCR Archive ✅ TERVERIFIKASI — prioritas diturunkan

Terverifikasi gratis dan mudah (`pip install aeon`), **tetapi seluruh datasetnya single-label dan tanpa pengelompokan subjek**. Akibatnya K1 dan K2 tidak dapat diuji secara alami di sini. **Status: P3, opsional.** Challenge 2021 adalah pilihan yang jauh lebih tepat untuk klaim generalisasi.

### 5.6 ✅ HASIL VERIFIKASI MANDIRI — Reposisi Desain Penelitian

Dijalankan 2026-09-29 atas data yang benar-benar terunduh. **29 pemeriksaan, 0 kegagalan.**
Rincian: [`docs/dataset-verification.md`](docs/dataset-verification.md) · Data mentah: `results/raw/`

#### Temuan 1 — Dependensi pasien SEDANG, bukan lemah (koreksi estimasi awal)

Estimasi kasar sebelumnya (13,4%) **salah** karena hanya menghitung selisih rekaman−pasien. Ukuran yang benar adalah proporsi rekaman yang berada di dalam blok multi-rekaman:

| Rekaman per pasien | Jumlah pasien | % pasien |
|---:|---:|---:|
| 1 | 16.758 | 88,81% |
| 2 | 1.590 | 8,43% |
| 3 | 350 | 1,85% |
| 4 | 99 | 0,52% |
| 5 | 43 | 0,23% |
| 6 | 16 | 0,08% |
| 7 | 5 | 0,03% |
| 8 | 4 | 0,02% |
| 9 | 3 | 0,02% |
| 10 | 1 | 0,01% |

**Rata-rata 1,155 · maksimum 10 · 5.041 rekaman (23,1%) berada di blok multi-rekaman · design effect 1,39.**

Dependensi tergolong **SEDANG** — cukup untuk diteliti, dan cukup ringan sehingga koreksi blok hanya menimbulkan biaya kecil. Justru kombinasi yang ideal untuk menunjukkan sifat adaptif metode.

#### Temuan 2 — MIT-BIH adalah ujung ekstrem ✅

**112.647 anotasi detak** (rujukan ~110.000) dari 48 rekaman. Per rekaman: minimum 1.519 · median 2.301 · maksimum 3.400 · **rata-rata 2.347 detak**. Dependensi **SANGAT KUAT**.

#### Temuan 3 — ❗ PTB-XL punya LIMA tingkat blok sekaligus

| Pengelompokan | Blok | Rata-rata | Maks | % di blok>1 | n_eff | Design effect | Intensitas |
|---|---:|---:|---:|---:|---:|---:|---|
| `patient_id` | 18.869 | 1,16 | 10 | 23,1% | 15.659 | **1,39** | SEDANG |
| `strat_fold` | 10 | 2.179,90 | 2.198 | 100% | 10 | 2.179,9 | SANGAT KUAT |
| `device` | 11 | 1.981,73 | 6.140 | 100% | 6 | 3.900,6 | SANGAT KUAT |
| `nurse` | 12 | 1.693,83 | 8.295 | 100% | 4 | 5.185,4 | SANGAT KUAT |
| `site` | 51 | 427,10 | 8.940 | 100% | 3 | 6.687,0 | SANGAT KUAT |

#### Temuan 4 — ❗❗ BATAS KELAYAKAN DITENTUKAN JUMLAH BLOK, BUKAN $n_{\text{eff}}$

> 🔧 **DIKOREKSI 2026-09-29** setelah membaca teks lengkap Lee, Barber & Willett (2026). Versi pertama temuan ini memakai **kuantitas yang salah**. Koreksinya justru menghasilkan temuan yang lebih tajam.

**Kesalahan versi pertama:** saya memakai $n_{\text{eff}}$ Kish sebagai penentu validitas, lalu menyimpulkan "pada level situs $n_{\text{eff}}=3$ → mustahil untuk $\alpha \leq 0{,}25$". **Itu keliru.**

**Yang benar.** Teorema 1 (HCP) menetapkan ambang

$$T = Q_{1-\alpha}\Big( \sum_{k}\sum_{i} \tfrac{1}{(K_1+1)N_k}\,\delta_{s(Z_{k,i})} \;+\; \tfrac{1}{K_1+1}\,\delta_{+\infty} \Big)$$

Setiap blok diberi bobot **sama** terlepas dari ukurannya. Massa $\frac{1}{K_1+1}$ diletakkan pada $+\infty$. Akibatnya, bila

$$\alpha \leq \frac{1}{K_1 + 1}$$

kuantilnya jatuh di $+\infty$ dan himpunan prediksi menjadi **tak hingga** — valid secara teknis, tetapi tanpa informasi. Penentunya adalah $K_1$ = **jumlah blok kalibrasi**, bukan jumlah sampel dan bukan $n_{\text{eff}}$.

**Hasil pengukuran** (`python .\scripts\feasibility_alpha.py`, kalibrasi = fold 9):

| Blok | Total blok | $K_1$ kalibrasi | $\alpha_{\min}$ | $\alpha{=}0{,}01$ | $\alpha{=}0{,}05$ | $\alpha{=}0{,}10$ | Design effect |
|---|---:|---:|---:|:---:|:---:|:---:|---:|
| `patient_id` | 18.869 | **1.942** | 0,00051 | ✅ | ✅ | ✅ | 1,39 |
| `site` | 51 | 40 | 0,0244 | ❌ | ✅ | ✅ | 6.687,0 |
| `nurse` | 12 | 12 | 0,0769 | ❌ | ❌ | ✅ | 5.185,4 |
| `device` | 11 | 11 | 0,0833 | ❌ | ❌ | ✅ | 3.900,6 |
| `strat_fold` | 10 | 8 | 0,1111 | ❌ | ❌ | ❌ | 2.179,9 |

**Dua kuantitas, dua mode kegagalan yang berbeda — inilah inti C6:**

| | Penentu | Mengatur | Gagal ketika |
|---|---|---|---|
| **Validitas** | $K_1$ (jumlah blok) | Apakah jaminan non-trivial **mungkin** | $\alpha \leq 1/(K_1+1)$ → himpunan tak hingga |
| **Efisiensi** | Design effect Kish | Seberapa **lebar** himpunannya | Blok besar → varians tinggi, himpunan lebar |

Keduanya **tidak berkorelasi**. Perhatikan `site`: design effect 6.687 (efisiensi terburuk) tetapi $\alpha=0{,}05$ masih layak. Sedangkan `device` punya design effect lebih rendah namun $\alpha=0{,}05$ **mustahil**. Memisahkan kedua sumbu ini adalah kontribusi yang tidak dapat dilihat dari satu angka saja.

**Implikasi praktis:** untuk PTB-XL pada level pasien, $K_1 = 1.942$ blok kalibrasi → seluruh level $\alpha$ yang direncanakan aman. Klaim lintas-perangkat dan lintas-fold **tidak dapat dijamin** pada $\alpha=0{,}05$. Ini batas informasi yang melekat pada desain studi, bukan kegagalan metode.

#### Temuan 5 — ⚠️ Hipotesis "dependensi meluruh terhadap waktu" TIDAK terdukung secara struktural — tetapi hasilnya justru lebih berguna

Offset tanggal konstan per pasien, sehingga **jarak antar-rekaman dalam satu pasien tetap valid**. Hipotesis awal: rekaman dari sesi yang sama lebih berkorelasi daripada rekaman berjarak bertahun-tahun, sehingga *design effect* mestinya meluruh terhadap interval.

**Hasil pengukuran (E11a) atas 2.111 pasien multi-rekaman:**

| Bin interval | Pasien | Rekaman | Rata-rata blok | $n_{\text{eff}}$ | Design effect |
|---|---:|---:|---:|---:|---:|
| Sesi sama (0 hari) | 140 | 299 | 2,14 | 133 | **2,25** |
| 1–30 hari | 995 | 2.387 | 2,40 | 881 | **2,71** |
| 31–365 hari | 679 | 1.629 | 2,40 | 598 | **2,73** |
| >365 hari | 297 | 726 | 2,44 | 262 | **2,77** |

Design effect **praktis datar** (2,25 → 2,77), bahkan sedikit naik. **Hipotesis tidak terdukung.**

**Mengapa — dan mengapa ini justru menguntungkan.** $n_{\text{eff}}$ Kish hanya merupakan fungsi **ukuran blok**, bukan kekuatan korelasi di dalam blok. Ia mengukur struktur, bukan isi, sehingga memang tidak mampu mendeteksi peluruhan korelasi.

Konsekuensinya justru berharga: **ukuran blok nyaris seragam di keempat bin** (2,14–2,44 rekaman/pasien). Keempat bin itu karenanya membentuk **perbandingan terkendali** — struktur blok setara, yang berbeda hanya jarak waktu. Bila nanti ditemukan deviasi cakupan yang berbeda antar bin, perbedaan itu **tidak dapat dikaitkan dengan ukuran blok sebagai perancu**; ia harus berasal dari kekuatan korelasi temporal.

**Akibatnya E11 dipecah dua:**

| | Isi | Butuh model? | Status |
|---|---|---|---|
| **E11a** | Struktur blok per bin interval | ❌ Tidak | ✅ **Selesai** — tabel di atas |
| **E11b** | ICC skor nonconformity + deviasi cakupan per bin | ✅ Ya | Menunggu backbone |

E11a sudah menjalankan fungsinya: membuktikan bin-bin tersebut **sepadan secara struktural**, yang merupakan prasyarat agar E11b bermakna.

> Ini menggantikan gagasan "coverage under temporal shift" yang **tidak valid** pada PTB-XL karena tanggal absolutnya tergeser acak.

#### Klaim penelitian direposisi menjadi:

> Pelanggaran exchangeability pada data klinis muncul pada beberapa tingkat granularitas (detak → rekaman → pasien → perangkat → perawat → situs). Kami menunjukkan bahwa **validitas** dibatasi oleh **jumlah blok kalibrasi** ($\alpha > 1/(K_1+1)$) sedangkan **efisiensi** dibatasi oleh *design effect*, bahwa kedua batas ini **tidak berkorelasi**, dan bahwa keduanya menghasilkan rekomendasi granularitas yang berbeda. Kami menyediakan uji diagnostik untuk menentukan tingkat blok mana yang layak dikalibrasi sebelum model apa pun dilatih.

#### Pemetaan dataset ke titik pengamatan

| Tingkat blok | Sumber | $K_1$ kalibrasi | Design effect | Peran |
|---|---|---:|---:|---|
| Detak → Rekaman | MIT-BIH | ~23 subjek | ~2.347 | Ujung ekstrem; bukti eksistensi masalah |
| Rekaman → Pasien | PTB-XL | **1.942** | **1,39** | **Kasus utama**; seluruh $\alpha$ layak |
| Rekaman → Situs | PTB-XL | 40 | 6.687 | Design effect terburuk, **tetapi $\alpha{=}0{,}05$ layak** |
| Rekaman → Perangkat | PTB-XL | 11 | 3.901 | Design effect lebih baik, **tetapi $\alpha{=}0{,}05$ mustahil** |
| Rekaman → Perawat | PTB-XL | 12 | 5.185 | Hanya $\alpha{=}0{,}10$ yang layak |
| Covariate shift | NSTDB | — | — | 6 level SNR; robustness cakupan |

> Dua baris tengah adalah inti C6: **urutan menurut design effect berlawanan dengan urutan menurut kelayakan $\alpha$.**

#### Konfirmasi lain yang lolos verifikasi

- ✅ 21.799 rekaman, 18.869 pasien, 28 kolom — **persis** sesuai rujukan
- ✅ **Tidak ada pasien yang menyeberang fold** — split resmi aman dipakai apa adanya
- ✅ Distribusi superclass **identik** dengan rujukan: NORM 9.514 · MI 5.469 · STTC 5.235 · CD 4.898 · HYP 2.649
- ✅ Multi-label terkonfirmasi: 27.765 label > 21.799 rekaman
- ✅ Hierarki tersedia: 44 dari 71 pernyataan SCP bersifat diagnostik, dengan `diagnostic_class` dan `diagnostic_subclass`
- ✅ `age` dan `sex` lengkap tanpa nilai kosong — K3 dapat dijalankan
- ✅ Metadata kualitas sinyal lengkap: `static_noise`, `burst_noise`, `baseline_drift`, `electrodes_problems`

> Panduan unduh: [`data/README.md`](data/README.md)

---

## 6. Metode yang Diusulkan (HiCoRC)

> ⚠️ **Nama `HiCoRC` bersifat sementara.** Akronimnya berasal dari judul lama (*Hierarchy-Aware Conformal Risk Control*) yang kini dicabut bersama C1. Tetapkan nama final bersamaan dengan judul di F1. Kandidat: `HiFeCal` (Hierarchical Feasibility-aware Calibration) atau cukup **BSD** (Block-Sufficiency Diagnostic) bila C7 menjadi pembeda utama.

### 6.1 Arsitektur Konseptual

```
[ Sinyal EKG 12-lead ]
          |
          v
[ Model dasar (model-agnostic) ]   <- xresnet1d / inception1d / dll.
          |  skor per-label
          v
+---------------------------------------------+
|              H i C o R C                    |
|                                             |
|  K1  Patient-Level Block Calibration        |
|      -> kuantil terkoreksi untuk blok       |
|                                             |
|  K2  Hierarchy-Constrained Set Construction |
|      -> upward closure pada pohon label     |
|                                             |
|  K3  Group-Conditional Risk Control         |
|      -> kendali risiko per subkelompok      |
+---------------------------------------------+
          |
          v
[ Himpunan prediksi dengan jaminan cakupan ]
```

### 6.2 K1 — Patient-Level Block Conformal Calibration

**Masalah:** kalibrasi per-sampel memperlakukan rekaman dari pasien yang sama sebagai independen -> kuantil kalibrasi bias optimis -> cakupan aktual < nominal.

**Ide:** unit pertukaran (exchangeable unit) adalah **pasien**, bukan rekaman. Ini **persis HCP** (Lee dkk., 2026, Teorema 1), yang memberi bobot $\frac{1}{(K_1+1)N_k}$ pada tiap skor sehingga setiap blok berkontribusi sama.

**Status:** K1 **bukan kontribusi Anda** — ini adalah metode rujukan yang Anda pakai dan perluas. Kontribusinya ada pada:

| | Apa yang baru |
|---|---|
| **C8** | HCP dirumuskan untuk regresi skalar ($\hat\mu(x) \pm T$). Perluasan ke **skor per-label multi-label** dengan hierarki belum ada |
| **C6** | Batas kelayakan $\alpha > \frac{1}{K_1+1}$ terhadap design effect — pertanyaan terbuka mereka |
| **C7** | Uji diagnostik memilih granularitas blok sebelum pelatihan |

**Intuisi kunci:** ukuran efektif set kalibrasi adalah **jumlah pasien**, bukan jumlah rekaman. Pada PTB-XL fold 9: $K_1 = 1.942$ blok, bukan 2.183 rekaman.

### 6.3 K2 — Hierarchy-Constrained Prediction Sets

**Aturan:** himpunan prediksi $\mathcal{C}$ wajib **tertutup ke atas**:

$$\forall\, \ell \in \mathcal{C}: \quad \mathrm{parent}(\ell) \in \mathcal{C}$$

**Target (C2, lema pendukung):** tunjukkan bahwa operator penutupan hierarkis $\mathrm{cl}(\cdot)$ bersifat **monoton dan ekspansif**, sehingga

$$\mathcal{C} \subseteq \mathrm{cl}(\mathcal{C}) \implies \text{cakupan } \mathrm{cl}(\mathcal{C}) \geq \text{cakupan } \mathcal{C}$$

Artinya validitas **tidak pernah rusak** oleh penutupan; harga yang dibayar hanya penambahan ukuran himpunan — yang harus dikuantifikasi secara empiris.

**Metrik pendamping:** Hierarchical Consistency Violation Rate (HCVR) — persentase prediksi yang melanggar hierarki sebelum penutupan.

### 6.4 K3 — Group-Conditional Risk Control

**Masalah:** cakupan marginal 90% dapat berarti 95% pada kelompok mayoritas dan 70% pada kelompok minoritas. Secara klinis dan etis, ini tidak dapat diterima.

**Ide:** kalibrasi kuantil **terpisah per subkelompok** $g \in \mathcal{G}$ (umur terkuartil x jenis kelamin), dengan penanganan kelompok berukuran kecil melalui shrinkage/pooling.

**Risiko yang dikendalikan:** selain cakupan, kendalikan **False Negative Rate pada kelas kritis** (mis. MI), karena melewatkan infark jauh lebih berbahaya daripada false alarm.

### 6.5 Pseudokode Tingkat Tinggi

```
INPUT : model f, data kalibrasi D_cal (berlabel, dengan patient_id dan grup),
        pohon hierarki T, target alpha, daftar grup G
OUTPUT: fungsi prediksi C(x)

1.  Hitung skor nonconformity s(x, y) untuk semua (x,y) di D_cal
2.  Kelompokkan D_cal menjadi blok berdasarkan patient_id
3.  FOR setiap grup g di G:
4.      Ambil blok-blok milik grup g
5.      Hitung skor agregat per blok (mis. max atau mean intra-blok)
6.      q_hat[g] <- kuantil terkoreksi-blok pada level (1 - alpha)
7.  END FOR
8.  DEFINE C(x):
9.      g  <- grup dari x
10.     S  <- { y : s(x,y) <= q_hat[g] }
11.     RETURN upward_closure(S, T)      // K2
```

> Implementasi rinci akan ditulis di `src/hicorc/`. Pseudokode ini adalah kontrak desain, bukan kode final.

---

## 7. Baseline

Minimal **15 baseline** — melampaui standar Q1. Semua dievaluasi pada protokol identik.

| # | Baseline | Kategori | Tujuan perbandingan |
|---|---|---|---|
| B1 | Split Conformal (naif, per-sampel) | Conformal | Menunjukkan kegagalan cakupan (inti RQ1) |
| B2 | Mondrian Conformal | Conformal | Pembanding untuk K3 |
| B3 | Conformal Risk Control (CRC) standar | Conformal | Pembanding langsung metode usulan |
| B4 | APS (Adaptive Prediction Sets) | Conformal | Pembanding efisiensi |
| B5 | RAPS (Regularized APS) | Conformal | Pembanding efisiensi |
| B6 | Jackknife+ / CV+ | Conformal | Alternatif tanpa split kalibrasi |
| B7 | Platt Scaling | Kalibrasi | Pembanding non-konformal |
| B8 | Temperature Scaling | Kalibrasi | Pembanding non-konformal |
| B9 | Isotonic Regression | Kalibrasi | Pembanding non-konformal |
| B10 | MC-Dropout | Bayesian approx. | Pembanding UQ |
| B11 | Deep Ensemble | Bayesian approx. | Pembanding UQ (batas atas kualitas) |
| **B12** | **HCP** (Lee, Barber & Willett 2026) | Conformal hierarkis | ❗ **Baseline terpenting** — fondasi teoretis yang Anda perluas |
| **B13** | **Pooling CDFs** (Dunn dkk. 2022) | Conformal hierarkis | Setara HCP dengan $\alpha$ sedikit lebih tinggi |
| **B14** | **Subsampling Once** (Dunn dkk. 2022) | Conformal hierarkis | Ambil 1 rekaman per pasien — valid tapi boros data |
| **B15** | **Double Conformal** (Dunn dkk. 2022) | Conformal hierarkis | Terlalu konservatif (union bound) |

> **B12–B15 wajib ada.** Tanpa membandingkan terhadap HCP dan ketiga metode Dunn dkk., reviewer akan langsung bertanya mengapa metode hierarkis yang sudah mapan tidak diuji. Dunn dkk. (2022) ✅ terverifikasi: **JASA**, `10.1080/01621459.2022.2060112`.

> ✅ **SELESAI (2026-09-29).** B1 dan B12–B15 terimplementasi di [src/conformal/calibration.py](src/conformal/calibration.py); 26 unit test lolos di [tests/test_conformal.py](tests/test_conformal.py). Ini memenuhi satu prasyarat pembekuan protokol §13.

#### Temuan sampingan — B15 punya **dua** syarat kelayakan, bukan satu

Ditemukan saat menulis unit test, bukan dari literatur. Karena Double Conformal mengambil kuantil $1-\alpha/2$ **dua kali** (di dalam blok lalu lintas blok), ia menuntut dua hal sekaligus:

$$K + 1 \ge \frac{2}{\alpha} \qquad \textbf{dan} \qquad \min_k N_k + 1 \ge \frac{2}{\alpha}$$

Syarat kedua **tidak punya padanan di HCP**, yang hanya menuntut $K+1 > 1/\alpha$. Konsekuensinya konkret: pada $K=500$ blok dengan $N_k=5$ dan $\alpha=0{,}2$, HCP menghasilkan ambang berhingga sementara **seluruh 500 blok** B15 jatuh ke $+\infty$ — jumlah blok berlimpah tidak menolong bila tiap blok terlalu dangkal.

Ini relevan langsung bagi C6: syarat $K$ dan syarat $N_k$ adalah **dua sumbu terpisah**, dan B15 adalah contoh tegas sebuah metode yang dapat gagal di sumbu $N_k$ meski sumbu $K$-nya sangat aman. Pada PTB-XL dengan pengelompokan `patient_id`, median $N_k = 1$, sehingga **B15 trivial untuk semua $\alpha < 1$** — fakta yang harus dilaporkan apa adanya, bukan disembunyikan sebagai "baseline berkinerja buruk".

**Model dasar (backbone) yang diuji** — untuk membuktikan sifat model-agnostic:

- `xresnet1d101` (benchmark resmi PTB-XL)
- `inception1d`
- `resnet1d_wang`
- `LSTM`
- Wavelet + shallow NN (jalur fitur tangan)

---

## 8. Desain Eksperimen

### 8.1 Eksperimen Inti

| ID | Eksperimen | Menjawab | Prioritas |
|---|---|---|---|
| E1 | Validasi cakupan empiris vs nominal, $\alpha \in \{0{,}01; 0{,}05; 0{,}10\}$ | RQ1, RQ2 | **P0** |
| E2 | Simulasi pelanggaran exchangeability terkendali: variasikan rata-rata rekaman/pasien | RQ1 | **P0** |
| E3 | Cakupan per subkelompok (umur kuartil x sex x kondisi noise) | RQ4 | **P0** |
| E4 | Efisiensi: ukuran rata-rata himpunan prediksi | RQ2, RQ3 | **P0** |
| E5 | Ablation 2^3 = 8 konfigurasi (K1/K2/K3 on-off) | Semua | **P0** |
| E6 | Sensitivitas ukuran set kalibrasi: 100 / 500 / 1.000 / 5.000 | RQ2 | P1 |
| E7 | Distribution shift: kalibrasi PTB-XL -> uji dataset EKG kedua | RQ5 | P1 |
| E8 | Replikasi pada dataset non-medis (UEA) | RQ5 | P1 |
| E9 | Perbandingan 100 Hz vs 500 Hz (trade-off akurasi–komputasi) | — | P2 |
| E10 | Robustness cakupan pada 6 level SNR NSTDB (24/18/12/6/0/−6 dB) | — | P2 |
| **E11a** | **Struktur blok per bin interval antar-rekaman** {0, 1–30, 31–365, >365 hari} — memastikan bin sepadan secara struktural | RQ1 | ✅ **SELESAI** |
| **E11b** | **ICC skor nonconformity + deviasi cakupan per bin interval** — mengisolasi efek korelasi temporal dari efek ukuran blok | RQ1, RQ2 | **P0** |

### ⚠️ Eksperimen yang SENGAJA TIDAK dilakukan

| Tidak dilakukan | Alasan |
|---|---|
| Temporal shift berbasis tanggal absolut (mis. latih pra-1995, uji pasca-1995) | `recording_date` PTB-XL **digeser acak per pasien**. Split berbasis kalender akan mengukur derau pseudonimisasi, bukan pergeseran distribusi. Diganti oleh **E11** yang memakai interval intra-pasien — satu-satunya informasi temporal yang tetap valid. |
| "Temporal preprocessing" per pasien sebagai deret waktu panjang | Tiap rekaman PTB-XL adalah potongan **10 detik** independen. Sifat longitudinal ada **antar-rekaman**, bukan di dalam rekaman. Preprocessing temporal di sini hanya band-pass filter. |

### 8.2 Protokol Eksperimen

- **Split:** gunakan **split resmi PTB-XL** — fold 1–8 latih (**17.418** rekaman / 15.023 pasien), fold 9 kalibrasi (**2.183** rekaman / **1.942** pasien), fold 10 uji (**2.198** rekaman / 1.904 pasien). Jangan membuat split sendiri — ini menjaga komparabilitas dengan benchmark yang ada.
- **Analisis konfirmatori:** batasi pada **fold 9–10** (kualitas label tertinggi, telah divalidasi manusia).
- **Seed:** minimal **5 seed**, laporkan mean +/- std. Tidak boleh melaporkan run tunggal.
- **Resampling kalibrasi:** untuk estimasi variabilitas cakupan, ulangi pemisahan kalibrasi/uji **>= 100 kali** (murah secara komputasi).
- **Preprocessing:** 100 Hz sebagai konfigurasi utama; band-pass 0,5–40 Hz; normalisasi per-lead.
- **Reproducibility:** semua seed, versi pustaka, dan konfigurasi tercatat di `configs/`.

### 8.3 Aturan Anti-Bias (WAJIB)

- [ ] Tulis protokol eksperimen **sebelum** melihat hasil apa pun (pre-registration internal di `docs/protocol.md`).
- [ ] Test set (fold 10) **hanya disentuh satu kali** di akhir, untuk hasil final.
- [ ] Tidak ada tuning hyperparameter menggunakan fold 10.
- [ ] Semua keputusan desain yang diubah di tengah jalan **dicatat di [Log Keputusan](#18-log-keputusan)** beserta alasannya.

---

## 9. Metrik Evaluasi

### 9.1 Metrik Utama (Conformal)

| Metrik | Definisi | Target |
|---|---|---|
| **Empirical Coverage** | Proporsi kasus uji dengan $Y \in \mathcal{C}(X)$ | >= $1-\alpha$ |
| **Average Set Size** | Rata-rata $\lvert \mathcal{C}(X) \rvert$ | Sekecil mungkin |
| **SSCV** | Size-Stratified Coverage Violation | Sekecil mungkin |
| **Conditional Coverage Gap** | $\max_g \lvert \text{cov}(g) - (1-\alpha) \rvert$ | Sekecil mungkin |
| **HCVR** | Hierarchical Consistency Violation Rate | 0 setelah K2 |
| **Controlled Risk (FNR@MI)** | FNR pada kelas kritis | <= target |

### 9.2 Metrik Pendukung (Model Dasar)

Macro/micro AUROC, AUPRC, F1-max, ECE, Brier score, per-superclass AUROC (khususnya **HYP** sebagai kelas minoritas, n=2.649).

> **Catatan penting:** metrik conformal adalah **metrik utama**. Metrik model dasar hanya untuk memastikan backbone Anda kompetitif — bukan klaim kontribusi.

---

## 10. Uji Statistik

| Perbandingan | Uji | Catatan |
|---|---|---|
| Cakupan vs nominal | Uji binomial eksak / CI Clopper-Pearson | Untuk menyatakan pelanggaran cakupan |
| AUROC antar model | **DeLong test** | Berpasangan |
| Selisih HCVR | **Uji permutasi** | Non-parametrik |
| Ranking banyak metode x banyak dataset | **Friedman + Nemenyi post-hoc** + **Critical Difference diagram** | Protokol Demsar |
| Interval kepercayaan semua metrik | **Bootstrap 1.000 resample** | Resample pada level **pasien**, bukan rekaman |
| Koreksi perbandingan ganda | **Holm-Bonferroni** | Wajib karena banyak konfigurasi |
| Ukuran efek | **Cliff's delta** | Jangan hanya melaporkan p-value |

> **Peringatan:** bootstrap harus dilakukan pada level **pasien**. Bootstrap per-rekaman akan mengulang kesalahan yang justru sedang kita kritik dalam paper ini.

---

## 11. Threats to Validity

| Jenis | Ancaman | Mitigasi |
|---|---|---|
| **Internal** | Label PTB-XL berasal dari laporan dengan likelihood; sebagian tidak divalidasi manusia | Analisis konfirmatori dibatasi pada fold 9–10 |
| **Internal** | Kebocoran informasi saat preprocessing | Semua transformasi di dalam pipeline, fit hanya pada train |
| **Konstruk** | HCVR adalah metrik usulan sendiri | Berikan definisi formal + justifikasi klinis + bandingkan dengan metrik mapan |
| **Konstruk** | Definisi subkelompok bersifat pilihan peneliti | Uji sensitivitas terhadap beberapa skema pengelompokan |
| **Eksternal** | Satu institusi; data dikumpulkan Oktober 1989–Juni 1996 (perangkat Schiller AG) | Validasi pada >= 2 dataset tambahan; nyatakan batasan secara eksplisit |
| **Konstruk** | `recording_date` **digeser acak per pasien** → tanggal absolut tidak bermakna | Analisis temporal dibatasi pada **interval intra-pasien** (offset konstan per pasien sehingga interval terjaga); temporal split berbasis kalender **tidak dilakukan** — lihat §8.1 |
| **Eksternal** | Domain EKG spesifik | Replikasi pada dataset non-medis (UEA) untuk klaim generalitas kerangka |
| **Kesimpulan** | Satu test fold resmi | Lengkapi dengan cross-fold sensitivity analysis + resampling kalibrasi 100x |
| **Teoretis** | Bukti formal mungkin memiliki celah | **Wajib direview oleh pembimbing berlatar statistika sebelum submission** |

---

## 12. Struktur Artikel

| Bagian | Isi | Target halaman |
|---|---|---|
| 1. Introduction | Motivasi regulatif, masalah, kontribusi berpoin C3–C8, struktur | 2 |
| 2. Related Work | Conformal hierarkis (HCP, Dunn dkk.); conformal multi-label; UQ pada EKG; conformal beyond exchangeability | 2,5 |
| 3. Preliminaries & Notation | Exchangeability hierarkis (Definisi 1 Lee dkk.), HCP, hierarki label | 1,5 |
| 4. Problem Formulation | Perluasan HCP ke multi-label berhierarki; formalisasi batas kelayakan | 1,5 |
| 5. Proposed Method | K1, K2, K3 + **uji diagnostik C7** + lema pendukung | 4 |
| 6. Datasets | PTB-XL, MIT-BIH, dataset generalisasi | 1,5 |
| 7. Experimental Setup | Baseline, backbone, protokol, metrik, uji statistik | 2 |
| 8. Results | RQ1–RQ5, satu subbagian per RQ | 5 |
| 9. Ablation Study | 8 konfigurasi + sensitivitas | 2 |
| 10. Discussion | Implikasi klinis & regulatif; kapan metode gagal | 1,5 |
| 11. Threats to Validity | — | 1 |
| 12. Conclusion & Future Work | — | 0,5 |
| — | Data Availability & Code Availability Statement | 0,25 |
| — | Appendix: bukti lengkap, tabel tambahan | (tidak dihitung) |

**Estimasi total:** ~25 halaman (format jurnal Q1).

---

## 13. Rencana Kerja & Milestone

| Fase | Durasi | Luaran | Gate |
|---|---|---|---|
| **F0 — Validasi Kelayakan** | ✅ **SELESAI** | Survei literatur; C1 ditemukan tertutup; kontribusi direposisi ke C6+C7 | ✅ **GO** dengan sudut yang digeser |
| **F1 — Fondasi Teoretis** | Minggu 1–6 | Kuasai HCP; formalkan **batas kelayakan $\alpha > 1/(K_1+1)$ vs design effect** (C6) dan **uji diagnostik** (C7); rumuskan perluasan multi-label (C8) | ❗ **GO/NO-GO**: jika C6/C7 tidak dapat diformalkan → jadikan paper murni empiris |
| **F2 — Infrastruktur** | Minggu 4–10 | Pipeline data, backbone terlatih, kerangka evaluasi, implementasi baseline | Pipeline lolos uji sanity |
| **F3 — Eksperimen Inti** | Minggu 11–20 | E1–E5 tuntas | Hasil E1 mengonfirmasi H0? |
| **F4 — Eksperimen Perluasan** | Minggu 21–28 | E6–E11b; dataset generalisasi | Generalisasi terbukti |
| **F5 — Penulisan** | Minggu 29–38 | Draf lengkap; internal review 2 putaran | Draf siap submit |
| **F6 — Submission & Revisi** | Minggu 39+ | Submit; tanggapi reviewer | — |

**Total estimasi: 9–12 bulan.** Sedikit lebih pendek dari rencana awal karena beban penurunan teorema dari nol berkurang — Anda kini membangun di atas fondasi yang sudah terbit.

### Rencana Cadangan (Contingency)

| Jika... | Maka... |
|---|---|
| Perluasan HCP ke multi-label (C8) ternyata sepele | Perkuat bobot pada C6+C7; jadikan C8 sekadar bagian Metode |
| C6 tidak dapat diformalkan melampaui pengamatan empiris | Turunkan menjadi **paper empiris terukur**: "How study design determines the feasibility of distribution-free guarantees in clinical ML" — tetap layak Q1 terapan |
| B7 (arXiv:2410.06296) terbit di venue kuat lebih dulu | Cabut C2 sepenuhnya; fokus penuh pada C6+C7 yang tidak tersentuh |
| Waktu tidak cukup | Batasi pada PTB-XL + MIT-BIH, hilangkan klaim generalisasi lintas domain |

---

## 14. Struktur Repositori

```
Sqopus/
├── README.md                     <- dokumen ini (dokumen induk)
├── .gitignore                    ✅ dibuat
├── docs/
│   ├── dataset-verification.md   ✅ dibuat - laporan verifikasi D1-D5
│   ├── references.md             ✅ dibuat - 42 sitasi terverifikasi + 2 praterbit + 5 dataset
│   ├── protocol.md               ✅ dibuat - pre-registration, status DRAF
│   ├── progress.md               ✅ dibuat - catatan kemajuan & koreksi
│   ├── theory.md                 <- turunan teorema, bukti, notasi
│   ├── literature-review.md      <- hasil survei sistematis + tabel gap
│   └── paper/                    <- draf naskah
├── scripts/
│   ├── download_physionet.py     ✅ unduh paralel lewat mirror S3
│   ├── download_nstdb.py         ✅ unduh NSTDB langsung dari PhysioNet
│   ├── download_data.ps1         ✅ unduh via get-zip (cadangan, lambat)
│   ├── verify_datasets.py         ✅ verifikasi struktural + statistik blok
│   ├── analyze_block_structure.py ✅ n_eff & design effect multi-granularitas
│   ├── feasibility_alpha.py       ✅ batas alpha layak per granularitas (C6/C7)
│   └── check_consistency.py       ✅ angka dokumen vs data nyata (jalankan sebelum commit)
├── data/
│   ├── README.md                 ✅ dibuat - panduan akuisisi
│   ├── raw/                      <- dataset asli (tidak di-commit)
│   └── interim/                  <- hasil preprocessing
├── src/
│   ├── data/                     <- loader, preprocessing, split
│   ├── models/                   <- backbone (xresnet1d, inception1d, ...)
│   ├── hicorc/                   <- implementasi K1, K2, K3
│   ├── baselines/                <- B1-B15 (termasuk HCP & Dunn dkk.)
│   ├── metrics/                  <- coverage, SSCV, HCVR, set size
│   └── stats/                    <- uji statistik, bootstrap, CD diagram
├── configs/                      <- YAML konfigurasi eksperimen
├── experiments/                   <- skrip runner per eksperimen (E1-E11)
├── results/
│   ├── raw/                      <- keluaran mentah
│   ├── tables/                   <- tabel siap paper
│   └── figures/                  <- gambar siap paper
├── notebooks/                    <- eksplorasi saja, BUKAN hasil final
├── tests/                        <- unit test (kritis untuk kode conformal!)
├── environment.yml
└── requirements.txt
```

> **Aturan:** hasil final **tidak pernah** berasal dari notebook. Semua angka di paper harus dapat direproduksi dengan satu perintah dari `experiments/`.

---

## 15. Lingkungan & Hardware

### 15.1 Kebutuhan Hardware

| Komponen | Kebutuhan | Catatan |
|---|---|---|
| CPU | 4+ core | **Seluruh lapisan conformal berjalan di CPU** |
| RAM | 16 GB | Cukup untuk PTB-XL 100 Hz |
| GPU | 4–6 GB (opsional) | Hanya untuk melatih backbone, **sekali saja** |
| Disk | 20 GB | Dataset + hasil |

> **Keunggulan strategis penelitian ini:** setelah backbone dilatih sekali, ribuan eksperimen kalibrasi berjalan dalam hitungan menit di CPU. Anda bersaing di level ide, bukan level GPU.

### 15.2 Stack Perangkat Lunak

```
python >= 3.10
numpy, scipy, pandas
scikit-learn
torch                  # backbone
wfdb                   # baca format PhysioNet
statsmodels            # uji statistik
matplotlib             # figur
pyyaml                 # konfigurasi
pytest                 # unit test
```

Pustaka conformal untuk baseline — ✅ **diverifikasi 2026-09-29** (PyPI + `pip index versions` pada Python 3.14.6 lokal):

| Pustaka | Versi tersedia | Peran |
|---|---|---|
| **MAPIE** | 1.5.0 | scikit-learn-contrib. Mendukung **risk control multi-label** dan uji exchangeability. Paling relevan untuk C8 |
| **TorchCP** | 1.2.1 | APS, RAPS, LAC, SAPS, class-conditional & cluster predictor — baseline B2, B4, B5 |
| **crepes** | 0.9.1 | Conformal regressor/classifier, Mondrian |
| `torch` | 2.14.0 | Memenuhi syarat TorchCP (`torch >= 2.1`) |

> ⚠️ **Tidak ada pustaka yang mengimplementasikan HCP (B12) maupun metode Dunn dkk. (B13–B15).** Keempatnya harus Anda tulis sendiri — tetapi rumusnya sederhana (kuantil berbobot), jauh lebih ringan daripada implementasi backbone.

---

## 16. Checklist Pra-Penelitian

Kerjakan **berurutan**. Jangan lompat.

### Langkah 1 — Survei Literatur ✅ SELESAI — HASILNYA MENGUBAH ARAH PENELITIAN

**Daftar terverifikasi:** [`docs/references.md`](docs/references.md) — 42 artikel jurnal + analisis mendalam 8 paper kritis.

- [x] Tarik metadata kandidat dari Crossref (41 artikel, 7 klaster topik)
- [x] **Verifikasi ulang lewat OpenAlex** — 40 entri final dengan sitasi, FWCI, dan peringkat JUFO/Norway/CWTS
- [x] **Baca abstrak lengkap B1, B2, B3, A3** — keempatnya **TIDAK** menutup kontribusi
- [x] **Pencarian arXiv terarah** untuk conformal pada data berklaster/pengukuran berulang
- [x] ❗ **DITEMUKAN: C1 sudah tertutup** oleh Lee, Barber & Willett, *Distribution-free inference with hierarchical data*, ACM J. Data Science 2026 (`10.1145/3786352`)
- [x] ⚠️ **DITEMUKAN: C2 berisiko** — arXiv:2410.06296 (Bastani dkk.), conformal pada DAG label hierarkis
- [x] **Kontribusi direposisi** ke C6 (tradeoff $K$ vs $N_k$) + C7 (uji diagnostik) + C8 (perluasan multi-label) — lihat §4
- [x] **Teks lengkap A0 dibaca** — Teorema 1 HCP, batas $\alpha > 1/(K_1+1)$, dan pertanyaan terbuka di Discussion
- [x] **Batas kelayakan dihitung pada data nyata**: `python .\scripts\feasibility_alpha.py` — lihat §5.6 Temuan 4
- [x] **Dunn, Wasserman & Ramdas (2022) ditemukan & diverifikasi** — JASA, `10.1080/01621459.2022.2060112`, sumber baseline B13–B15
- [x] **Pustaka conformal diverifikasi di PyPI** — MAPIE 1.5.0 (mendukung risk control multi-label), TorchCP 1.2.1 (APS/RAPS/LAC/SAPS)
- [ ] Baca B7 (arXiv:2410.06296) untuk mengukur sisa ruang C2
- [ ] Baca E5 (arXiv:2601.01223) — kalibrasi konformal sadar-kelompok pada data kesehatan hierarkis
- [ ] Verifikasi indeksasi Scopus tiap jurnal di https://www.scopus.com/sources
- [ ] Jalankan konfirmasi di Scopus:
  ```
  TITLE-ABS-KEY(("conformal" AND "hierarchical" AND "multi-label")) AND PUBYEAR > 2022
  TITLE-ABS-KEY(("conformal prediction" AND ("exchangeability" OR "dependent data") AND "clinical")) AND PUBYEAR > 2022
  TITLE-ABS-KEY(("conformal" AND ("effective sample size" OR "design effect"))) AND PUBYEAR > 2020
  TITLE-ABS-KEY(("conformal prediction" AND ("ECG" OR "electrocardiography"))) AND PUBYEAR > 2022
  ```
- [ ] Cari rujukan non-jurnal yang wajib (Angelopoulos, Vovk, Romano, RAPS) — daftar di `docs/references.md` §6
- [ ] Catat seluruh hasil di `docs/literature-review.md`

### Langkah 2 — Rekrut Kolaborator (dianjurkan, tidak lagi mutlak)

Setelah C1 dicabut, Anda tidak lagi menurunkan teorema dari nol — risiko desk reject akibat bukti cacat turun drastis. Kolaborator statistika tetap berharga untuk C6.

- [ ] Identifikasi dosen/peneliti berlatar **statistika atau matematika**
- [ ] Presentasikan rencana **C6 (tradeoff $K$ vs $N_k$)** dan **C7 (uji diagnostik)**
- [ ] Minta review atas perumusan batas $\alpha > 1/(K_1+1)$ dan perluasannya ke multi-label

### Langkah 3 — Verifikasi Dataset ✅ SELESAI

- [x] Verifikasi halaman resmi D1–D5 (jumlah, lisensi, DOI, format)
- [x] Identifikasi tumpang tindih PTB-XL ↔ Challenge 2021
- [x] Identifikasi ketiadaan `patient_id` pada Challenge 2021
- [x] Unduh P0: `python .\scripts\download_physionet.py mitdb ptbxl --workers 24`
- [x] Unduh P1: `python .\scripts\download_nstdb.py --workers 8`
- [x] Verifikasi struktural: **29 pemeriksaan, 0 gagal**
- [x] **Distribusi rekaman per pasien PTB-XL** — 23,1% di blok multi-rekaman, design effect 1,39
- [x] **Distribusi detak per rekaman MIT-BIH** — rata-rata 2.347, maksimum 3.400
- [x] Konfirmasi tidak ada pasien menyeberang fold
- [x] Analisis blok multi-granularitas: `python .\scripts\analyze_block_structure.py`
- [x] Angka hasil disalin ke Bagian 5.6

**Terkumpul:** 44.379 berkas · 661,5 MB · PTB-XL + MIT-BIH + NSTDB.
Sisa: Challenge 2021 (P2, setelah H0 terkonfirmasi) dan UEA (P3, opsional).

### Langkah 4 — Studi Kelayakan Cepat (1 minggu)

- [ ] Latih satu backbone sederhana pada PTB-XL 100 Hz
- [ ] Terapkan split conformal naif
- [ ] **Ukur apakah cakupan empiris < nominal** -> ini memvalidasi H0
- [ ] Jika H0 tidak terkonfirmasi, **seluruh premis penelitian perlu ditinjau ulang**

### Langkah 5 — Tulis Protokol 🟡 DRAF SELESAI

- [x] Tulis [`docs/protocol.md`](docs/protocol.md) — hipotesis H0/H0b/H1/H2/H3, split beku, preprocessing beku, rencana analisis statistik, aturan keputusan, log penyimpangan
- [x] Verifikasi jumlah rekaman/pasien per fold langsung dari CSV (bukan pengurangan)
- [ ] Lengkapi setelah backbone terlatih (§13 checklist pembekuan)
- [ ] **Bekukan dengan `git tag protocol-v1`** sebelum eksperimen konfirmatori pertama
- [ ] Isi tanggal + hash commit di kepala protokol

---

## 17. Status Verifikasi Referensi

### ✅ Terverifikasi (dikutip dari halaman resmi)

| Referensi | Detail |
|---|---|
| Wagner, Strodthoff, Bousseljot, Kreiseler, Lunze, Samek, Schaeffter (2020) | *PTB-XL: A Large Publicly Available ECG Dataset*, **Scientific Data**. DOI: https://doi.org/10.1038/s41597-020-0495-6 |
| Wagner, Strodthoff, Bousseljot, Samek, Schaeffter (2022) | PTB-XL v1.0.3, PhysioNet. DOI: https://doi.org/10.13026/kfzx-aw45 |
| Strodthoff, Wagner, Schaeffter, Samek (2021) | *Deep Learning for ECG Analysis: Benchmarks and Insights from PTB-XL*, **IEEE JBHI 25(5):1519–1528**. DOI: https://doi.org/10.1109/jbhi.2020.3022989 |
| Moody, Mark (2001) | *The impact of the MIT-BIH Arrhythmia Database*, **IEEE Eng in Med and Biol 20(3):45–50** (PMID: 11446209) |
| Mark, Schluter, Moody, Devlin, Chernoff (1982) | *An annotated ECG database for evaluating arrhythmia detectors*, **IEEE TBME 29(8):600** |
| Moody, Mark (2005) | MIT-BIH Arrhythmia Database, PhysioNet. DOI: https://doi.org/10.13026/C2F305 |
| Barber, Candès, Ramdas, Tibshirani (2023) | *Conformal prediction beyond exchangeability*, **Annals of Statistics**. DOI: https://doi.org/10.1214/23-aos2276 — 278 sitasi, FWCI 63,4 |
| Barber, Candès, Ramdas, Tibshirani (2021) | *Predictive inference with the jackknife+*, **Annals of Statistics** (= baseline B6). DOI: https://doi.org/10.1214/20-aos1965 — 338 sitasi |
| **Lee, Barber, Willett (2026)** | *Distribution-free inference with hierarchical data*, **ACM Journal of Data Science** (= baseline B12, fondasi teoretis). DOI: https://doi.org/10.1145/3786352 · arXiv:2306.06342 |
| **Dunn, Wasserman, Ramdas (2022)** | *Distribution-Free Prediction Sets for Two-Layer Hierarchical Models*, **JASA** (= baseline B13–B15). DOI: https://doi.org/10.1080/01621459.2022.2060112 · arXiv:1809.07441 — 11 sitasi, FWCI 1,63, JUFO-3 N2 A\* |

### ⚠️ BELUM TERVERIFIKASI — cari sendiri, jangan kutip sebelum dikonfirmasi

| Topik | Kata kunci pencarian |
|---|---|
| Pengantar conformal | "Angelopoulos Bates gentle introduction conformal prediction uncertainty quantification" |
| Conformal risk control | "Angelopoulos conformal risk control" (ICLR) |
| Buku rujukan | "Vovk Gammerman Shafer algorithmic learning in a random world" |
| Conformal adaptif (baseline B4/APS) | "Romano Sesia Candes classification with valid and adaptive coverage" |
| RAPS (baseline B5) | "Angelopoulos uncertainty sets for image classifiers using conformal prediction" |
| Mondrian | "Mondrian conformal prediction Vovk" |
| Uji statistik | "Demsar statistical comparisons of classifiers over multiple data sets" |
| Inter-patient ECG | "de Chazal automatic classification of heartbeats inter-patient" (IEEE TBME 2004) |

> Daftar lengkap beserta venue-nya ada di [`docs/references.md`](docs/references.md) §6. Semuanya bukan artikel jurnal, sehingga tidak tertangkap pencarian otomatis.

> **ATURAN MUTLAK:** jangan pernah mencantumkan DOI atau detail sitasi yang belum Anda buka sendiri. Sitasi fiktif adalah pelanggaran integritas akademik dan terdeteksi dengan mudah oleh reviewer.

### 📚 Daftar pustaka terverifikasi — [`docs/references.md`](docs/references.md)

**42 artikel jurnal + 2 praterbit kritis + 5 rujukan dataset**, seluruhnya diverifikasi lewat OpenAlex API pada 2026-09-29.

| Yang diverifikasi | Status |
|---|---|
| DOI, judul, jurnal, ISSN, tahun | ✅ |
| Jumlah sitasi + **FWCI** (dampak ternormalisasi bidang) | ✅ |
| Mutu jurnal via **JUFO / Norwegian Register / CWTS Core** | ✅ |
| Indeksasi Scopus langsung | ❌ scimagojr.com memblokir akses (HTTP 403) |

**Mutu venue:** **19 entri JUFO-3** (terkemuka dunia) · 9 JUFO-2 · 12 JUFO-1 · 18 Norway-2 · **seluruhnya CWTS Core**. Hanya 2 entri tanpa peringkat JUFO, keduanya ditandai ⚠️ di dokumen.

| Klaster | Isi | Jml |
|---|---|---:|
| A | Fondasi & teori conformal (termasuk **A0** HCP dan **A0b** Dunn dkk.) | 12 |
| B | Multi-label & hierarki — **penentu kelayakan** | 6 + 1 praterbit |
| C | Kendali risiko & deret waktu | 5 |
| D | Pergeseran distribusi & kalibrasi terkondisi | 4 |
| E | Conformal klinis | 4 + 1 praterbit |
| F | Deep learning EKG, PTB-XL, inter-patient | 9 |
| G | AI tepercaya & regulatif | 2 |
| H | Rujukan dataset | 5 |

> **SINTA tidak berlaku di sini.** SINTA hanya mengindeks jurnal terbitan Indonesia; nol dari 42 rujukan ini terbitan Indonesia. Untuk naskah Q1, daftar pustaka yang didominasi jurnal nasional justru merupakan bendera merah bagi reviewer.

### ❗ Rujukan fondasi — wajib dikuasai, bukan sekadar disitasi

| Rujukan | DOI / arXiv | Peran |
|---|---|---|
| **Lee, Barber & Willett (2026)** *Distribution-free inference with hierarchical data*, ACM J. Data Science | `10.1145/3786352` · arXiv:2306.06342 | **Fondasi teoretis.** HCP = baseline B12. Menutup C1. Discussion-nya menyatakan C6 sebagai pertanyaan terbuka |
| **Dunn, Wasserman & Ramdas (2022)** *Distribution-Free Prediction Sets for Two-Layer Hierarchical Models*, **JASA** | `10.1080/01621459.2022.2060112` · arXiv:1809.07441 | ✅ **Terverifikasi** — 11 sitasi, FWCI 1,63, JUFO-3 N2 A\*. Baseline B13–B15 |
| Zhang, Li & Bastani (2024) *Conformal Structured Prediction* | arXiv:2410.06296 | Ancaman terhadap C2; masih praterbit — **pantau** |
| Shahbazi, Baheri & Azadeh-Fard (2026) *Adaptive CP via Bayesian Uncertainty Weighting for Hierarchical Healthcare Data* | arXiv:2601.01223 | Kalibrasi sadar-kelompok pada data kesehatan; bukti pendukung H0 |

Analisis lengkap tiap entri: [`docs/references.md`](docs/references.md).

---

## 18. Log Keputusan

Catat setiap keputusan desain di sini beserta alasannya. Ini melindungi Anda saat menulis bagian Methods dan saat menjawab reviewer.

| Tanggal | Keputusan | Alasan | Diputuskan oleh |
|---|---|---|---|
| 2026-09-29 | ~~Judul final: *Hierarchy-Aware Conformal Risk Control...*~~ ⚠️ **DIGANTIKAN** | Judul itu menjanjikan C1 yang kemudian terbukti sudah diterbitkan. Judul sekarang berstatus **sedang direvisi** dengan 3 kandidat — lihat bagian atas dokumen. Dikunci setelah C6 diformalkan di F1 | — |
| 2026-09-29 | PTB-XL sebagai dataset utama | Terverifikasi, punya hierarki label + split resmi tingkat pasien + metadata kaya | — |
| 2026-09-29 | 100 Hz sebagai konfigurasi utama | Hemat komputasi; disediakan resmi oleh penyedia dataset; akan diuji vs 500 Hz di E9 | — |
| 2026-09-29 | **Reposisi klaim ke "spektrum intensitas dependensi blok"** | Verifikasi menunjukkan PTB-XL hanya 1,16 rekaman/pasien (dependensi lemah). Klaim tunggal "dependensi pasien merusak conformal" terlalu rapuh. Spektrum multi-granularitas lebih kuat dan lebih jujur. | — |
| 2026-09-29 | MIT-BIH dinaikkan menjadi dataset **ko-utama**, bukan pendukung | ~2.340 detak/subjek = dependensi blok ekstrem; kasus terbaik untuk membuktikan eksistensi masalah | — |
| 2026-09-29 | Challenge 2021 dipakai **selektif**: hanya `chapman-shaoxing`, `georgia`, `ningbo` | Folder `ptb-xl` duplikat dengan dataset utama → akan membatalkan klaim independensi | — |
| 2026-09-29 | UEA/UCR diturunkan ke prioritas P3 (opsional) | Seluruh dataset single-label tanpa pengelompokan subjek → K1 & K2 tidak dapat diuji | — |
| 2026-09-29 | NSTDB menggantikan noise sintetis buatan sendiri untuk E10 | Noise nyata terkalibrasi 6 level SNR dengan ground truth terjaga; standar komunitas 40 tahun | — |
| 2026-09-29 | Akuisisi lewat **mirror AWS `physionet-open`**, bukan endpoint `get-zip` | Terukur: get-zip ~33 KB/s (ETA 15 jam) vs S3 405–914 KB/s paralel | — |
| 2026-09-29 | **`records500/` tidak diunduh** | Konsekuensi langsung keputusan 100 Hz; memangkas PTB-XL dari ~2,9 GB ke 526,8 MB. Jalankan `--with-500hz` bila E9 membutuhkannya | — |
| 2026-09-29 | **Koreksi**: dependensi pasien = 23,1% (bukan 13,4%) | Estimasi awal keliru — hanya menghitung selisih rekaman−pasien, bukan rekaman di dalam blok multi-rekaman. Angka benar dari verifikasi mandiri | — |
| 2026-09-29 | Menambah **C6** dan **C7** sebagai kontribusi | Menghindari single-point-of-failure pada C1; keduanya tidak bergantung pada intensitas dependensi empiris. *(Rumusan C6 direvisi kemudian — lihat entri 2026-09-29 tentang "dua batas")* | — |
| 2026-09-29 | ~~Blok `site`/`nurse`/`device` menunjukkan batas ketidakmungkinan ($n_{\text{eff}}$ 3–6 → mustahil untuk $\alpha \leq 0{,}25$)~~ ⚠️ **SALAH, DIGANTIKAN** | Memakai kuantitas keliru. Angka benar: situs $K_1{=}40 \Rightarrow \alpha_{\min}{=}0{,}024$ (jadi $\alpha{=}0{,}05$ **layak**); perangkat $K_1{=}11 \Rightarrow \alpha_{\min}{=}0{,}083$. Lihat entri koreksi di bawah | — |
| 2026-09-29 | NSTDB diunduh per-berkas paralel, folder `old/` dilewati | Tidak ada di bucket S3 (4 prefix diperiksa, semua kosong). Paralel 174 KB/s vs get-zip ~33 KB/s. `old/` hanya duplikat warisan | — |
| 2026-09-29 | **Akuisisi P0+P1 ditutup** pada 661,5 MB / 44.379 berkas | Cukup untuk seluruh eksperimen P0 (E1–E6). Challenge 2021 ditunda sampai H0 terkonfirmasi agar 12,6 GB tidak terbuang bila sudut penelitian bergeser | — |
| 2026-09-29 | **Temporal split berbasis tanggal absolut DIBATALKAN** | Dokumentasi PTB-XL: tanggal digeser acak per pasien. Terkonfirmasi di data: rentang tampak 1984–2001 padahal pengumpulan 1989–1996. Split kalender akan mengukur derau pseudonimisasi | — |
| 2026-09-29 | **Ditambahkan E11** — dependensi sebagai fungsi interval antar-rekaman | Offset konstan per pasien → interval intra-pasien tetap valid. 2.111 pasien, median 23 hari, maks 1.707 hari. Memberi sumbu dependensi kontinu dari data nyata, lebih kuat daripada subsampling buatan | — |
| 2026-09-29 | E10 diperjelas: memakai **6 level SNR NSTDB**, bukan noise sintetis buatan sendiri | Noise nyata terkalibrasi dengan ground truth terjaga; standar komunitas | — |
| 2026-09-29 | **Hipotesis "dependensi meluruh terhadap interval" DITOLAK secara struktural** | Design effect per bin datar: 2,25 / 2,71 / 2,73 / 2,77. Penyebabnya jelas — $n_{\text{eff}}$ Kish hanya fungsi ukuran blok, bukan kekuatan korelasi. Dicatat apa adanya, tidak dipaksakan | — |
| 2026-09-29 | **E11 dipecah menjadi E11a (struktural, selesai) dan E11b (butuh model)** | Keseragaman ukuran blok antar bin (2,14–2,44) menjadikan bin sebagai **perbandingan terkendali**: perbedaan cakupan yang ditemukan nanti tidak dapat diperancu oleh ukuran blok. Hasil negatif E11a justru memperkuat desain E11b | — |
| 2026-09-29 | **Daftar pustaka ditulis ulang total** setelah verifikasi OpenAlex | Draf Crossref pertama tidak memeriksa relevansi maupun mutu venue. Verifikasi ulang menemukan 3 rujukan kritis yang terlewat: conformal multi-label di Pattern Recognition (66 sitasi), conformal deret waktu di TPAMI (64 sitasi), dan rujukan kanonik "inter-patient paradigm" (FWCI 10,9). Dua DOI Scientific Reports 2026 dikeluarkan karena tidak terkonfirmasi di OpenAlex | — |
| 2026-09-29 | **SINTA dinyatakan tidak berlaku** untuk daftar pustaka ini | SINTA hanya mengindeks jurnal terbitan Indonesia. Untuk target Q1 internasional, dominasi jurnal nasional pada daftar pustaka adalah bendera merah bagi reviewer | — |
| 2026-09-29 | 🚨 **C1 DICABUT sebagai kontribusi** | Survei literatur menemukan Lee, Barber & Willett, *Distribution-free inference with hierarchical data*, **ACM J. Data Science 2026** (`10.1145/3786352`, arXiv sejak Jun 2023). Abstraknya menyatakan langsung: menurunkan "bentuk exchangeability hierarkis" untuk "kelompok observasi atau pengukuran berulang" dan memperluas conformal + jackknife+. Ini persis C1, bahkan melampauinya dengan *second-moment coverage* | — |
| 2026-09-29 | **C2 diturunkan dari teorema ke lema pendukung** | Argumen monoton+ekspansif hanya beberapa baris — terlalu tipis sebagai klaim utama Q1. Ditambah arXiv:2410.06296 (Bastani dkk.) sudah menangani conformal pada DAG label hierarkis | — |
| 2026-09-29 | **C6 dan C7 dinaikkan menjadi kontribusi utama** | Keduanya tidak tersentuh Lee-Barber-Willett yang murni teoretis. Datanya sudah ada: lima granularitas blok terukur pada satu dataset klinis, dari $K_1{=}8$ hingga $K_1{=}1.942$ | — |
| 2026-09-29 | **Target venue digeser** dari jurnal statistika ke jurnal klinis/terapan | Tanpa C1, pembeda utama bukan lagi teorema melainkan karakterisasi batas + diagnostik + validasi klinis. IEEE JBHI / AI in Medicine / CBM / MedIA semuanya tetap Scopus Q1 | — |
| 2026-09-29 | **B1, B2, B3, A3 dikonfirmasi TIDAK menutup kontribusi** | Abstrak lengkap dibaca: B1 review dependensi antar-label (bukan antar-sampel); B3 efisiensi Label Powerset pada teks; B2 irisan lintas-resolusi dengan pembagian $\alpha$ (arah berlawanan dengan penutupan ke atas); A3 kelompok menentukan pergeseran kovariat, exchangeability intra-kelompok tetap berlaku | — |
| 2026-09-29 | 🔧 **KOREKSI: batas validitas ditentukan $K_1$, bukan $n_{\text{eff}}$ Kish** | Teks lengkap Lee-Barber-Willett dibaca. Teorema 1 memberi bobot $\frac{1}{(K_1+1)N_k}$ per skor dan massa $\frac{1}{K_1+1}$ pada $+\infty$ → himpunan menjadi tak hingga bila $\alpha \leq 1/(K_1+1)$. Penentunya **jumlah blok**, bukan $n_{\text{eff}}$. Klaim lama "situs $n_{\text{eff}}=3$ → mustahil untuk $\alpha \leq 0{,}25$" **salah**; angka benar: situs $K_1=40 \Rightarrow \alpha_{\min}=0{,}024$ | — |
| 2026-09-29 | **C6 direformulasi menjadi "dua batas yang tidak berkorelasi"** | Validitas diatur $K_1$; efisiensi diatur design effect. `site` punya design effect terburuk (6.687) tetapi $\alpha=0{,}05$ layak; `device` design effect lebih baik (3.901) tetapi $\alpha=0{,}05$ mustahil. Pemisahan dua sumbu ini lebih tajam daripada klaim ketidakmungkinan tunggal | — |
| 2026-09-29 | 🎯 **C6 divalidasi sebagai pertanyaan terbuka oleh penulis teorema sendiri** | Discussion Lee-Barber-Willett: *"the analyst can choose between a large number of independent groups $K$ with a small number of measurements $N_k$... **Characterizing the pros and cons of this tradeoff is an important question**"*. Ini argumen novelty terkuat yang tersedia | — |
| 2026-09-29 | **Ditambahkan C8** — perluasan HCP dari regresi skalar ke multi-label berhierarki | HCP dirumuskan untuk $\hat\mu(x) \pm T$ dan diuji pada Lorenz 96 (regresi). Jembatan ke himpunan label multi-label berhierarki belum ada dan tidak sepele | — |
| 2026-09-29 | **Ditambahkan baseline B12–B15** | HCP (Lee dkk.) + tiga metode Dunn dkk. (Pooling CDFs, Subsampling Once, Double Conformal). Tanpa ini reviewer akan langsung menolak: metode hierarkis mapan tidak diuji | — |
| 2026-09-29 | ✅ **B1 + B12–B15 selesai diimplementasi** | [`src/conformal/`](src/conformal/); 26 unit test lolos. Memverifikasi Teorema 1 (cakupan 0,824 ∈ [0,800; 0,895]), Proposisi 1, dan reduksi HCP→split saat $N_k{=}1$ | Implementasi salah → uji diikat ke pernyataan formal makalah, bukan ke intuisi |
| 2026-09-29 | 🔍 **Ditemukan: B15 punya DUA syarat kelayakan** | Double Conformal menuntut $\min_k N_k + 1 \ge 2/\alpha$ **selain** $K+1 \ge 2/\alpha$. Pada `patient_id` (median $N_k{=}1$) B15 trivial untuk semua $\alpha$. Memperkuat C6: dua sumbu terpisah | Dilaporkan apa adanya sebagai batas metode, bukan disembunyikan sebagai "baseline lemah" |
| 2026-09-29 | 🔧 **KOREKSI: satu unit test lolos secara hampa** | `test_double_conformal_paling_konservatif` hanya membandingkan `inf >= berhingga` pada 2 dari 3 level $\alpha$. Diperbaiki memakai $N{=}60$ agar ambang B15 berhingga | Lolosnya uji tidak membuktikan apa pun sampai angkanya dicetak dan diperiksa |
| 2026-09-29 | **Langkah 2 (kolaborator statistika) diturunkan dari "kritis" ke "dianjurkan"** | Tanpa penurunan teorema dari nol, risiko desk reject akibat bukti cacat turun drastis | — |
| 2026-09-29 | **Protokol pre-registration ditulis** ([`docs/protocol.md`](docs/protocol.md)) | Mengunci hipotesis, split, preprocessing, dan rencana uji **sebelum** fold 10 disentuh. Memuat aturan keputusan eksplisit bila H0 tidak konklusif — mencegah pencarian analisis pasca-hoc | — |
| 2026-09-29 | 🔧 **KOREKSI: jumlah rekaman per fold** | Angka awal (17.441 / 2.198 / 2.160) didapat dari pengurangan, dan fold 9–10 tertukar. Angka benar dari CSV: **17.418 / 2.183 / 2.198**. $K_1{=}1.942$ tetap benar | — |
| 2026-09-29 | **Nama `HiCoRC` dinyatakan sementara** | Akronimnya berasal dari judul lama yang dicabut bersama C1. Ditetapkan bersamaan dengan judul final di F1 | — |
| 2026-09-30 | **Repositori git diinisialisasi** — commit `5ba06f6` | 24 berkas / 277,8 KB. `.gitignore` diperbaiki agar `results/raw/*.json` (11,4 KB bukti provenance) ikut ter-commit sementara dataset 661,5 MB tetap di luar. `data/raw/ptbxl.zip` dihapus setelah diverifikasi rusak | Verifikasi integritas zip dilakukan **sebelum** penghapusan, bukan diasumsikan |
| 2026-09-30 | ❌ **`git tag protocol-v1` sengaja DITUNDA** | Protokol masih 🟡 draf; backbone belum dilatih dan pipeline belum end-to-end. Menandai sekarang akan mengubah pre-registration menjadi formalitas kosong | Tag dibuat setelah checklist §13 protokol tuntas, sebelum fold 10 disentuh |
| 2026-09-30 | 🔧 **`check_consistency.py` diperbaiki** — `UnicodeEncodeError` saat output di-pipe | Gerbang pra-commit yang hanya berfungsi bila dijalankan manual adalah gerbang palsu. Ditambahkan `reconfigure(encoding="utf-8")` | — |
| | | | |

---

## Catatan Penutup

**Tidak ada jaminan diterima di jurnal mana pun.** Dokumen ini menyusun penelitian agar **secara struktural memenuhi ekspektasi Q1** — kontribusi yang jelas, multi-dataset, statistik ketat, artefak terbuka. Sisanya bergantung pada eksekusi dan faktor di luar kendali Anda.

**Dua hal yang paling menentukan keberhasilan — per 2026-09-30:**

| # | Prioritas | Mengapa menentukan | Gagal bila |
|---|---|---|---|
| **1** | **Formalkan C6 + C7 di F1** | Pembeda utama penelitian. Barber sendiri menyatakan C6 sebagai pertanyaan terbuka — argumen novelty terkuat yang tersedia. Datanya sudah ada; yang kurang hanya perumusannya | Tidak dapat diformalkan melampaui pengamatan empiris → turun ke paper empiris terukur |
| **2** | **Studi kelayakan (Langkah 4)** | Melatih backbone, terapkan conformal naif, ukur cakupan. **Memvalidasi H0** sebelum berinvestasi penuh | H0 tidak konklusif → ikuti `protocol.md` §11, jangan mencari analisis baru |
| ~~3~~ | ~~Implementasi B12–B15~~ | ✅ **Selesai 2026-09-29.** [`src/conformal/`](src/conformal/), 26 unit test lolos, Teorema 1 & Proposisi 1 terverifikasi secara empiris | — |

> **Sudah diamankan:** survei literatur ✅ selesai dan menyelamatkan sepuluh bulan. C1 ternyata sudah diterbitkan sejak 2023 — ditemukan sekarang, bukan di laporan reviewer.
>
> ✅ **Repositori git diinisialisasi 2026-09-30** — commit `5ba06f6`, 24 berkas, dataset 661,5 MB tetap di luar riwayat. `git tag protocol-v1` **sengaja belum dibuat**: protokol masih draf, dan menandainya sebelum checklist §13 tuntas akan mengosongkan makna pre-registration. Lihat [`docs/progress.md`](docs/progress.md) §10.1.

> **Dua pelajaran yang layak dicatat:**
>
> 1. Klaim gap versi pertama disusun tanpa pencarian literatur, dan ternyata keliru. Itulah sebabnya §4 kini memuat kutipan langsung dari teks yang benar-benar dibaca.
> 2. Temuan 4 versi pertama memakai $n_{\text{eff}}$ Kish sebagai penentu validitas — juga keliru. Membaca teorema aslinya, bukan hanya abstraknya, mengoreksinya menjadi $K_1$. **Intuisi yang benar dengan kuantitas yang salah tetap salah.**
