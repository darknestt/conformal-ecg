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
| C4 | Empiris | Bukti kuantitatif bahwa conformal naif **gagal** pada EKG klinis multi-label hierarkis | ✅ **DIPULIHKAN dengan kualifikasi** (2026-09-30). Berlaku bila $\mathrm{DEff}$ tinggi (MIT-BIH: defisit −1,2 s.d. −1,6 pp, signifikan 3/3); nihil bila $\mathrm{DEff}\approx1$ (PTB-XL). Spearman gabungan +0,80 s.d. +0,85, $p<0{,}002$ — lihat §5.8 |
| C5 | Artefak | Pustaka Python open-source + reproduksi penuh (GitHub + Zenodo DOI) | ✅ |
| **C6** | **Teoretis-empiris** | **Karakterisasi tradeoff $K$ blok vs $N_k$ pengukuran**: validitas dibatasi $\alpha \ge 1/(K_1+1)$ dan **tidak bergantung $N_k$ sama sekali**; efisiensi punya **lantai $\sigma^2\rho/K$** yang tak tertembus berapa pun pengukuran ditambahkan | ✅ **Kontribusi utama** — dinyatakan sebagai pertanyaan terbuka oleh Lee-Barber-Willett sendiri |
| **C7** | **Metodologis** | **Uji diagnostik kecukupan blok** — menentukan granularitas mana yang layak dikalibrasi, **sebelum** model dilatih | ✅ **Kontribusi utama** |
| **C8** | **Metodologis** | **Kelayakan kalibrasi per-label pada hierarki**: cakupan-superset tereduksi sepele ke HCP, tetapi jaminan **terkondisi-label** melahirkan batas $\alpha \ge 1/(K_1(\ell)+1)$ yang monoton naik menuju akar — menghasilkan **frontier kelayakan** pada pohon label | ✅ Diformalkan §5 [`docs/theory.md`](docs/theory.md) |

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
>
> ❌ **H0 TERREFUTASI pada granularitas pasien PTB-XL (2026-09-30).** Cakupan naif terukur 0,9910 / 0,9511 / 0,9010 terhadap target 0,99 / 0,95 / 0,90 — **tepat di nominal**. Koreksi blok tidak berefek (CI selisih melingkupi nol). Penyebabnya struktural: rata-rata $N_k = 1{,}12$ dan 90,5% pasien hanya punya satu rekaman. Rincian: §5.7 dan [`docs/protocol.md`](docs/protocol.md) §12b.

---

## 3. Research Problem, Questions, Objectives

### 3.1 Research Problem

Prediksi konformal hierarkis (HCP) memulihkan validitas cakupan di bawah dependensi blok, tetapi **hanya untuk regresi bernilai skalar** dan **tanpa panduan tentang granularitas blok mana yang layak dipakai**. Pada data klinis nyata, blok tersedia di banyak tingkat sekaligus (pasien, perangkat, perawat, situs) dengan jumlah blok yang sangat berbeda — dan sebagian di antaranya membuat jaminan non-trivial **mustahil** pada level $\alpha$ yang lazim. Praktisi tidak punya cara menentukan tingkat mana yang layak, dan tidak ada prosedur yang membawa jaminan ini ke keluaran diagnosis multi-label berhierarki.

### 3.2 Research Questions

| ID | Pertanyaan |
|---|---|
| **RQ1** | Seberapa besar deviasi cakupan empiris dari nominal ketika split conformal standar diterapkan pada data klinis dengan dependensi pasien? |
| **RQ2** | Pada tingkat granularitas blok mana jaminan cakupan non-trivial masih **mungkin**, dan bagaimana batas $\alpha \ge 1/(K_1+1)$ berinteraksi dengan design effect? |
| **RQ3** | Bagaimana HCP diperluas dari regresi skalar ke himpunan prediksi multi-label berhierarki, dan berapa harga efisiensi penutupan hierarkis? |
| **RQ4** | Apakah kendali risiko terkondisi-kelompok menghasilkan cakupan yang adil lintas subkelompok umur/jenis kelamin, dibandingkan kendali marginal? |
| **RQ5** | Seberapa jauh temuan RQ1–RQ4 bertahan pada dataset dengan intensitas dependensi berbeda (MIT-BIH), dan dapatkah diagnostik C7 mengenali dataset yang struktur pengelompokannya **tidak cukup** untuk target kalibrasi yang diinginkan (Challenge 2021)? |

### 3.3 Research Objectives

- **O1** Memperluas HCP (Lee dkk., 2026) dari regresi skalar ke **himpunan prediksi multi-label berhierarki** — C8.
- **O2** Mengarakterisasi tradeoff $K$ blok vs $N_k$ pengukuran: memisahkan batas **validitas** ($\alpha \ge 1/(K_1+1)$) dari batas **efisiensi** (design effect) — C6.
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
| **G2 — Uji diagnostik kecukupan blok** | Tidak ada prosedur untuk memutuskan granularitas mana yang layak. Praktisi harus menebak | §5.6 Temuan 4: batas $\alpha \ge 1/(K_1+1)$ terhitung eksak per granularitas |
| **G3 — Multi-label hierarkis klinis** | HCP diuji pada **regresi** (residual absolut, Lorenz 96). Tidak ada pengujian pada himpunan prediksi multi-label, apalagi dengan hierarki label | PTB-XL: 27.765 label, 44 pernyataan diagnostik berhierarki, 23,1% rekaman di blok multi-rekaman |

> ❗ **Jarak antara HCP dan kebutuhan Anda lebih lebar dari dugaan awal.** HCP adalah metode **regresi** yang menghasilkan interval $\hat\mu(x) \pm T$. Anda butuh **himpunan label multi-label berhierarki**. Menjembataninya bukan pekerjaan sepele — dan itu justru ruang kontribusi C3.

### 4.2 Klaim yang direkomendasikan

> Kami **mengoperasionalkan** prediksi konformal hierarkis (HCP; Lee dkk., 2026) untuk klasifikasi EKG **multi-label berhierarki**, lalu menjawab pertanyaan terbuka yang diajukan penulisnya sendiri: bagaimana desain studi ($K$ blok versus $N_k$ pengukuran) menentukan inferensi bebas-distribusi. Kami menunjukkan bahwa **validitas** dibatasi jumlah blok ($\alpha \ge 1/(K_1+1)$) dan **sama sekali tidak bergantung pada $N_k$**, sedangkan **efisiensi** memiliki lantai $\sigma^2\rho/K$ yang tak tertembus berapa pun pengukuran berulang ditambahkan. Kami menunjukkan pula bahwa design effect Kish mengukur estimator yang **bukan** dipakai HCP — selisihnya mencapai 15,7× pada data nyata — dan menurunkan ukuran yang tepat untuk blok tak seragam. Pada desain **bersilang**, mengendalikan beberapa sumber dependensi sekaligus menuntut partisi *join*, yang pada PTB-XL meruntuhkan set kalibrasi menjadi satu blok. Kami menyediakan uji diagnostik yang menentukan tingkat blok dan tingkat label mana yang layak dikalibrasi sebelum model apa pun dilatih.

**Mengapa ini tetap layak Q1:**

- Menjawab **pertanyaan terbuka yang dinyatakan eksplisit** oleh penulis teorema rujukan — argumen novelty terkuat yang tersedia
- Perluasan regresi → multi-label berhierarki adalah kontribusi metodologis nyata, bukan penerapan ulang
- Temuan "design effect Kish salah estimator untuk HCP" langsung berguna bagi siapa pun yang memakai HCP pada blok tak seragam
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

### 5.4 Studi Kasus Batas Keteramatan — PhysioNet/CinC Challenge 2021 ✅ DIAGNOSTIK SELESAI

> 🎯 **Reposisi 2026-09-30.** Dataset ini **bukan** dataset generalisasi tingkat pasien — datanya tidak mendukung klaim itu, dan **bukan** bukti empiris utama. Ia masuk naskah sebagai **studi kasus batas keteramatan** yang menjelaskan *mengapa* prasyarat S0 diperlukan. Diagnostik yang hanya pernah bilang "lolos" tidak membuktikan apa pun.

| Atribut | Nilai |
|---|---|
| URL | https://physionet.org/content/challenge-2021/1.0.3/ |
| Data publik (training) | **88.253 rekaman** 12-lead dari 8 folder |
| **Non-duplikat (terverifikasi)** | **66.416** dari 7 folder |
| Label | **SNOMED-CT, multi-label**, di header WFDB `#Dx:` |
| Lisensi | **CC BY 4.0** |
| Ukuran penuh | 12,6 GB |
| **Diunduh** | **~0,5 MB** — 70 berkas indeks + 1 header |
| DOI | https://doi.org/10.13026/34va-7q14 |

**Rincian terverifikasi langsung** ([`scripts/verify_challenge2021.py`](scripts/verify_challenge2021.py)): `ningbo` 34.905 · `georgia` 10.344 · `chapman_shaoxing` 10.247 · `cpsc_2018` 6.877 · `cpsc_2018_extra` 3.453 · `ptb` 516 · `st_petersburg_incart` 74. Folder `ptb-xl` (21.837) **dikecualikan** karena duplikat §5.1.

> Pemeriksaan silang: $66.416 + 21.837 = 88.253$ — persis total resmi.

#### Vonis diagnostik C7

Isi header diperiksa langsung (760 B): `#Age`, `#Sex`, `#Dx`, `#Rx`, `#Hx`, `#Sx`. **Tidak ada pengenal pasien.**

| Syarat | Hasil |
|---|---|
| **S0 Keteramatan** | ⚠️ **TAK TERAMATI** — tidak ada variabel terdokumentasi sebagai pengenal pasien |
| **S2 Kecukupan** | ⚠️ **TIDAK DAPAT DIPUTUSKAN** — bukan gagal, bukan lolos |
| **S1 Kelayakan** (sumber, $K{=}7$) | ❌ $\alpha_{\min} \ge 1/8 = 0{,}125$ |
| **Prop. 0′** | $K_1$ berhenti menjadi besaran terhitung → menjadi **asumsi** yang wajib dinyatakan |

> ⚠️ **S0 tidak pernah "gagal".** Ia terpenuhi atau tak teramati. Tidak menemukan pengenal pasien **bukan** membuktikan rekamannya independen — justru sebaliknya, tidak ada yang dapat dibuktikan. Ini **bukan** klaim bahwa cakupan pasti rusak; yang hilang adalah **jaminannya**.
>
> ❗ **Dokumentasi resmi menyatakan pengulangan ADA.** Sumber INCART berisi *"74 annotated ECGs … extracted from **32 Holter monitor recordings**"*. Beberapa rekaman dapat berasal dari **episode pemantauan yang sama**, sementara pengenal pengelompokannya tidak disediakan — persis celah yang S0 dimaksudkan menangkap. Rumusan sengaja menyebut *episode pemantauan*, bukan identitas pasien.
>
> 🟡 **S0 adalah klaim dokumentasi, bukan teorema.** Tanpa label pasien, ketakteramatan tidak dapat *dibuktikan* dari data — yang dapat dinyatakan hanya bahwa tidak ada variabel yang terdokumentasi sebagai pengenal.
>
> ✅ **Pilihan $K=7$ disokong sumber primer dan kriteria substantif.** Partisi sumber berpadanan dengan **struktur provenans terdokumentasi** (tujuh basis data, institusi dan negara berbeda), sedangkan subfolder `g#` dideskripsikan dokumentasi sebagai **satuan alokasi berkas** sampai 1.000 rekaman. Memakai `g#` sebagai blok menuntut asumsi tambahan yang tidak disokong dokumentasi. Sensitivitas dilaporkan penuh: $K{=}7 \Rightarrow \alpha_{\min}\ge0{,}125$ versus $K{=}70 \Rightarrow \alpha_{\min}\ge0{,}014$ — **vonis berlawanan** pada $\alpha{=}0{,}05$. Lihat audit adversarial §6 di `docs/paper/sec6-7-draft.md` (riwayat git, commit 9098746).

**Rumusan klaim yang boleh masuk naskah:** *dengan partisi teramati yang tersedia pada metadata Challenge 2021, dan di bawah kondisi kelayakan sampel-hingga yang dipakai penelitian ini, target $\alpha < 0{,}125$ tidak memenuhi syarat kelayakan untuk jaminan non-trivial pada tingkat blok tersebut.* Yang **tidak boleh** ditulis: *"Challenge 2021 terbukti tidak dapat dipakai untuk conformal prediction"* — terlalu luas.

**Nilai demonstratifnya:** vonis definitif diperoleh dengan mengunduh **~0,5 MB dari 12,6 GB** — rasio ~25.000× — sebelum preprocessing dan sebelum melatih model apa pun. Itu inti klaim praktis C7.

Turunan lengkap, Prop. 0, dan dua kesalahan yang tertangkap saat menyusunnya: [`docs/theory.md`](docs/theory.md) §4.0–4.6.

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

| Pengelompokan | Blok | Rata-rata | Maks | % di blok>1 | n_eff | DEff **Kish** | DEff **blok** | Intensitas |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `patient_id` | 18.869 | 1,16 | 10 | 23,1% | 15.659 | 1,39 | **1,2** | SEDANG |
| `strat_fold` | 10 | 2.179,90 | 2.198 | 100% | 10 | 2.179,9 | **2.179,9** | SANGAT KUAT |
| `device` | 11 | 1.981,73 | 6.140 | 100% | 6 | 3.900,6 | **1.981,7** | SANGAT KUAT |
| `nurse` | 12 | 1.693,83 | 8.295 | 100% | 4 | 5.185,4 | **1.693,8** | SANGAT KUAT |
| `site` | 51 | 427,10 | 8.940 | 100% | 3 | 6.687,0 | **427,1** | SANGAT KUAT |

> ⚠️ **Kolom "DEff Kish" dipertahankan hanya untuk jejak sejarah.** Kish mengukur estimator terboboti-**observasi**, sedangkan HCP memakai terboboti-**blok**. Yang benar untuk penelitian ini adalah kolom **DEff blok** ($= n/K$ pada $\rho{=}1$). Keduanya berimpit hanya bila ukuran blok seragam — perhatikan `strat_fold` yang memang seragam dan menghasilkan angka identik. Lihat koreksi di Temuan 4 dan [`docs/theory.md`](docs/theory.md) §2.1.

#### Temuan 4 — ❗❗ BATAS KELAYAKAN DITENTUKAN JUMLAH BLOK, BUKAN $n_{\text{eff}}$

> 🔧 **DIKOREKSI 2026-09-29** setelah membaca teks lengkap Lee, Barber & Willett (2026). Versi pertama temuan ini memakai **kuantitas yang salah**. Koreksinya justru menghasilkan temuan yang lebih tajam.

**Kesalahan versi pertama:** saya memakai $n_{\text{eff}}$ Kish sebagai penentu validitas, lalu menyimpulkan "pada level situs $n_{\text{eff}}=3$ → mustahil untuk $\alpha \leq 0{,}25$". **Itu keliru.**

**Yang benar.** Teorema 1 (HCP) menetapkan ambang

$$T = Q_{1-\alpha}\Big( \sum_{k}\sum_{i} \tfrac{1}{(K_1+1)N_k}\,\delta_{s(Z_{k,i})} \;+\; \tfrac{1}{K_1+1}\,\delta_{+\infty} \Big)$$

Setiap blok diberi bobot **sama** terlepas dari ukurannya. Massa $\frac{1}{K_1+1}$ diletakkan pada $+\infty$, sehingga massa yang tersisa pada atom berhingga tepat $\frac{K_1}{K_1+1}$. Akibatnya, bila

$$\alpha < \frac{1}{K_1 + 1}$$

kuantilnya jatuh di $+\infty$ dan himpunan prediksi menjadi **tak hingga** — valid secara teknis, tetapi tanpa informasi. Penentunya adalah $K_1$ = **jumlah blok kalibrasi**, bukan jumlah sampel dan bukan $n_{\text{eff}}$.

> 🔧 **DIKOREKSI 2026-09-30: ketaksamaannya TIDAK ketat.** Versi sebelumnya menulis syarat kelayakan sebagai $\alpha > \frac{1}{K_1+1}$. Itu keliru pada kasus batas. Tepat di $\alpha = \frac{1}{K_1+1}$, massa berhingga $\frac{K_1}{K_1+1}$ **persis menyamai** level $1-\alpha$; karena kuantil didefinisikan dengan $\inf\{t : F(t) \ge 1-\alpha\}$, level itu tercapai di skor maksimum. Ambangnya berhingga, dan cakupan terukur 0,9512 pada $K_1{=}19$, $\alpha{=}0{,}05$ — sah.
>
> Syarat yang benar: $\boxed{\alpha \ge \frac{1}{K_1+1}}$, setara $K_1 \ge \lceil 1/\alpha \rceil - 1$. Bentuk ini **sejajar dengan syarat baku split conformal** $n \ge 1/\alpha - 1$ — yang justru menjadi pemeriksaan silang bahwa koreksi ini benar. Tidak ada satu pun verdict di tabel bawah yang berubah, karena tak ada granularitas yang kebetulan jatuh tepat di batas.

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
| **Validitas** | $K_1$ (jumlah blok) | Apakah jaminan non-trivial **mungkin** | $\alpha < 1/(K_1+1)$ → himpunan tak hingga |
| **Efisiensi** | $K$, rata-rata harmonik $H$, dan $\rho$ | Seberapa **lebar** himpunannya | Lantai $\sigma^2\rho/K$ tak tertembus |

> 🔧 **DIKOREKSI 2026-09-30 — klaim "dua sumbu tidak berkorelasi" DICABUT.** Versi sebelumnya menyatakan *"urutan menurut design effect berlawanan dengan urutan menurut kelayakan"*, memakai `site` (DEff 6.687, layak) versus `device` (DEff 3.901, tidak layak).
>
> **Itu artefak dari memakai design effect Kish** — ukuran milik estimator terboboti-**observasi**, padahal HCP memakai estimator terboboti-**blok** $\hat G = \frac{1}{K}\sum_k \bar F_k$. Keduanya berimpit hanya bila $N_k$ seragam; pada `site` selisihnya **15,7×**.
>
> Dengan ukuran yang benar ($\mathrm{DEff}_{\text{blok}}$ pada $\rho{=}1$ = $n/K$): `patient_id` 1,2 ✅ · `site` **427,1** ✅ · `nurse` 1.693,8 ❌ · `device` 1.981,7 ❌ · `strat_fold` 2.179,9 ❌. **Kedua granularitas yang layak justru dua yang paling efisien** — urutannya sejalan, bukan berlawanan.
>
> **Dan itu memang seharusnya:** pada $\rho{=}1$, $\mathrm{DEff}_{\text{blok}} = n/K$ turun monoton terhadap $K$ sementara kelayakan naik monoton terhadap $K$. Keduanya digerakkan variabel yang sama. Ini justru **konsisten dengan Teorema C6(c)** yang menyatakan tidak ada tradeoff — tabel empiris lamalah yang bertentangan dengan teorinya sendiri. Rincian: [`docs/theory.md`](docs/theory.md) §2.1 dan §3.1.

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

#### Temuan 6 — ❗❗ GRANULARITAS PTB-XL TIDAK BERSARANG — dan itu menghasilkan batas ketidakmungkinan

Ditemukan 2026-09-30 saat memformalkan C7 ([`scripts/check_nesting.py`](scripts/check_nesting.py)). Aturan keputusan C7 yang semula hendak ditulis — *"pilih granularitas terkasar yang masih layak"* — **runtuh**, karena aturan itu diam-diam mengandaikan granularitasnya bersarang. Ternyata tidak.

**Pelanggaran persarangan (pasien yang menyeberang):**

| Pasien muncul di | Jumlah |
|---|---:|
| >1 `site` | **46** |
| >1 `nurse` | **247** |
| >1 `device` | **174** |
| >1 `strat_fold` | **0** ✅ |

Hanya `patient_id` $\subset$ `strat_fold` yang bersarang. Akibatnya **memblok per `site` tidak mengandung dependensi pasien**: 46 pasien terbelah ke site berbeda lalu diperlakukan sebagai independen — persis kesalahan yang penelitian ini kritik.

**Konsekuensi formal.** Untuk mengendalikan dua sumber dependensi sekaligus pada desain bersilang, blok yang sah adalah **komponen terhubung** dari gabungan kedua partisi (join pada kekisi partisi). Jumlah bloknya **tidak pernah lebih besar** daripada masing-masing, dan dapat runtuh drastis:

| Sumber yang dikendalikan | $K_1$ (fold 9) | Blok terbesar | $\alpha_{\min}$ | $\alpha{=}0{,}05$ |
|---|---:|---:|---:|:---:|
| `patient_id` | 1.942 | 8 | 0,00051 | ✅ |
| `patient_id` + `nurse` | 204 | 1.467 | 0,00488 | ✅ |
| `patient_id` + `site` | 34 | 843 | 0,02857 | ✅ |
| `patient_id` + `device` | **5** | 889 | **0,16667** | ❌ |
| keempatnya | **1** | 2.183 | **0,50000** | ❌ |

**Tiga bacaan yang masuk naskah:**

1. **Mengendalikan pasien + perangkat sekaligus mustahil pada $\alpha \le 0{,}167$.** 174 pasien menyeberang perangkat, sehingga union-find merantai 11 perangkat menjadi hanya **5** komponen.
2. **Mengendalikan keempat sumber meruntuhkan set kalibrasi menjadi SATU blok** ($\alpha_{\min}{=}0{,}5$). Tidak ada jaminan bermakna yang mungkin — ini batas **desain studi**, bukan kekurangan metode.
3. `patient_id` + `nurse` layak, tetapi satu blok memuat **1.467 dari 2.183** rekaman kalibrasi (67%). **Layak belum tentu berguna.**

> $K_1{=}1.942$ untuk `patient_id` tunggal **cocok persis** dengan hasil `feasibility_alpha.py` yang dihitung lewat jalur berbeda — pemeriksaan silang bahwa union-find-nya benar.

> ⚠️ **Konteks yang juga terungkap:** `nurse` kosong pada 1.473 rekaman (6,8%), dan site 0/1/2 memuat 20.309 rekaman (93,2%). Ke-47 site sisanya hanya membawa 1.469 rekaman — dan hampir seluruhnya justru yang `nurse`-nya kosong. Jadi kelayakan `site` bertumpu pada 37 site mungil yang tampaknya rezim pengumpulan berbeda. Wajib dilaporkan.

Turunan lengkap: [`docs/theory.md`](docs/theory.md) §4.

#### Temuan 7 — ❗❗ FRONTIER KELAYAKAN PADA HIERARKI LABEL (C8)

Ditemukan 2026-09-30 ([`scripts/label_feasibility.py`](scripts/label_feasibility.py)). Terhitung dari **metadata saja** — tanpa model, tanpa skor.

**Pertama, kejujuran yang harus dinyatakan:** cakupan-**superset** $\mathbb{P}(Y \subseteq \hat C(X)) \ge 1-\alpha$ tereduksi **persis** ke HCP lewat skor skalar $s(x,Y)=\max_{\ell\in Y}s_\ell(x)$. Teorema 1 HCP agnostik terhadap struktur $\mathcal{Y}$, jadi ini **sepele** dan tidak boleh dijual sebagai perluasan non-trivial.

**Isi C8 yang sesungguhnya** ada pada jaminan **terkondisi-label**, yang tidak tereduksi. Kalibrasi label $\ell$ hanya boleh memakai titik yang memuat $\ell$, sehingga blok menyusut dan batas Prop. 1 berlaku **per label**:

$$\alpha \;\ge\; \frac{1}{K_1(\ell)+1}, \qquad K_1(\ell) = \text{blok kalibrasi yang memuat } \ell$$

**Hasil pada PTB-XL** (fold 9 · blok = `patient_id` · 44 pernyataan diagnostik · 3.070 pasangan pada 1.917 blok):

| Tingkat | $m$ | Tak-layak $\alpha{=}0{,}05$ **marginal** | Tak-layak $\alpha{=}0{,}05$ **serentak** | Blok/label untuk serentak |
|---|---:|---:|---:|---:|
| **Superclass** | 5 | **0 / 5** | **0 / 5** | 99 |
| **Subclass** | 23 | 6 / 23 | **22 / 23** | 459 |
| **Kode SCP** | 44 | **24 / 44** | **43 / 44** | 879 |

$K_1$ superclass: NORM 905 · MI 486 · STTC 473 · CD 449 · HYP 242 — seluruhnya aman bahkan serentak. Sebaliknya pada kode SCP, `2AVB` hanya punya **1** blok kalibrasi ($\alpha_{\min}{=}0{,}5$); `INJIN`, `3AVB`, `INJLA`, `INJIL`, `PMI` masing-masing 2 blok.

**Monotonisitas terkonfirmasi: 0 pelanggaran dari 23 pasangan** subclass→superclass. Karena setiap blok yang memuat anak pasti memuat induknya, $K_1$ monoton naik menuju akar. Konsekuensinya ada **antirantai** pada pohon yang memisahkan wilayah layak dari tak-layak — dan letaknya **di antara superclass dan subclass**.

**Tiga konsekuensi langsung:**

1. Klaim terkondisi-label pada tingkat **superclass** sah dan dapat dipertahankan.
2. Klaim pada tingkat **kode SCP** tidak dapat dipertahankan pada $\alpha$ lazim — dan itu **bukan** karena modelnya lemah. Melaporkan cakupan per-kode tanpa menyebut $K_1(\ell)$ akan menyesatkan.
3. Bila jaminan **serentak** diinginkan, hanya tingkat superclass yang tersedia.

> **Bonus untuk C2:** penutupan ke atas hanya menambahkan leluhur, dan menurut monotonisitas leluhur selalu setidaknya selayak keturunannya. Jadi penutupan hierarkis **tidak pernah** memasukkan label tak-layak — biayanya murni efisiensi.

Turunan lengkap: [`docs/theory.md`](docs/theory.md) §5.

### 5.7 ❌ Temuan 8 — H0 TERREFUTASI pada granularitas pasien PTB-XL

Studi kelayakan (Langkah 4) dijalankan 2026-09-30. Rincian: [`docs/protocol.md`](docs/protocol.md) §12b · kode: [`experiments/feasibility.py`](experiments/feasibility.py)

**Desain:** latih fold 1–6 · validasi fold 7 · evaluasi = fold 9 dibagi level-pasien, **200 pengulangan**. Backbone `SmallECGNet` 104.389 parameter, macro-AUROC 0,9016. Fold 10 tidak disentuh.

| $\alpha$ | Target | B1 naif (CI95) | B12 HCP (CI95) | Selisih B12−B1 (CI95) |
|---:|---:|---|---|---|
| 0,01 | 0,99 | **0,9910** [0,9823; 0,9972] | 0,9912 [0,9822; 0,9973] | $+0{,}0003$ [$0{,}0000$; $+0{,}0028$] |
| 0,05 | 0,95 | **0,9511** [0,9318; 0,9673] | 0,9510 [0,9318; 0,9673] | $-0{,}0002$ [$-0{,}0047$; $+0{,}0047$] |
| 0,10 | 0,90 | **0,9010** [0,8741; 0,9256] | 0,9002 [0,8728; 0,9231] | $-0{,}0008$ [$-0{,}0056$; $+0{,}0038$] |

Cakupan naif **tepat di nominal**, bukan di bawahnya. Koreksi blok tidak berefek: CI selisih melingkupi nol di ketiga level, cukup sempit untuk menyingkirkan efek di atas 0,5 poin persen.

**Penyebabnya struktural, bukan kegagalan pengukuran.** Pada fold 9: rata-rata $N_k = 1{,}1195$, **90,5% pasien hanya punya satu rekaman**, rasio bobot atom $+\infty$ HCP vs split hanya **1,12×**. HCP secara konstruksi tidak dapat berbeda di sini — konsisten dengan $\mathrm{DEff}_{\text{blok}} = 1{,}2$.

#### 🔍 Konfound yang nyaris lolos — dan positif palsu yang dihasilkannya

Rancangan **pertama** studi ini mengalibrasi di fold 8 lalu menguji di fold 9, dan melaporkan cakupan 0,9357 pada $\alpha{=}0{,}05$ — defisit **1,43 poin persen**, tampak mendukung H0.

Itu **positif palsu**. Fold 1–8 hanya **64–68%** divalidasi manusia; fold 9–10 **100%**. Rancangan itu mencampurkan pergeseran kualitas label ke dalam pengukuran cakupan. Begitu kalibrasi dan uji diambil dari fold 9 saja (100% vs 100%), defisitnya **hilang sepenuhnya**.

| Rancangan | Kalibrasi tervalidasi | Uji tervalidasi | Cakupan $\alpha{=}0{,}05$ |
|---|---|---|---|
| Pertama (konfound) | 67,8% | 100% | 0,9357 — defisit semu |
| Diperbaiki | 100% | 100% | **0,9511** — tepat nominal |

> Yang menangkapnya bukan pemeriksaan cakupan, melainkan pertanyaan **"mengapa B12 identik dengan B1?"** Ambangnya 0,9136 vs 0,9137. Kalau dependensi blok penyebabnya, HCP pasti memperbaikinya.

#### Tiga hal yang justru menguat

1. **Ini kontrol positif yang lolos.** Split conformal mencapai cakupan nominal **persis** — tepat yang harus terjadi bila exchangeability berlaku. Hasil nol ini memvalidasi implementasi skor, kalibrasi, dan evaluasi sekaligus.
2. **Mutu backbone tidak relevan.** Jaminan conformal model-agnostik: model lemah melebarkan $|C|$, tidak menurunkan cakupan. macro-AUROC 0,9016 vs benchmark ~0,93 memengaruhi efisiensi, bukan validitas.
3. **Protokol bekerja.** §11 butir 2 sudah menuliskan tafsiran "pada design effect rendah, koreksi blok tidak diperlukan" **sebelum** hasil terlihat. Melaporkannya bukan rasionalisasi pasca-hoc.

#### Konsekuensi

| | Status |
|---|---|
| **C4** | ❌ Tidak terdukung di PTB-XL. → **Terselesaikan di §5.8**: bukan salah, melainkan **berkualifikasi** — PTB-XL berada pada $\mathrm{DEff}{\approx}1$ |
| **C6, C7, C8** | ✅ **Tidak tersentuh.** Batas kelayakan kombinatorial, terbukti tanpa model |
| Langkah berikutnya | Uji H0b di **MIT-BIH** (~2.347 detak/rekaman, tiga orde lebih besar) |

> Klaim lama *"Dependensi tergolong SEDANG — cukup untuk diteliti"* (Temuan 1) kini **terbantah secara empiris untuk keperluan cakupan**. Cukup untuk *diukur*, tidak cukup untuk *merusak* conformal.

#### Klaim penelitian direposisi menjadi:

> Pelanggaran exchangeability pada data klinis muncul pada beberapa tingkat granularitas (detak → rekaman → pasien → perangkat → perawat → situs). Kami menunjukkan bahwa **validitas** dibatasi oleh **jumlah blok kalibrasi** ($\alpha \ge 1/(K_1+1)$) dan **sama sekali tidak bergantung pada jumlah pengukuran per blok**, sedangkan **efisiensi** memiliki lantai $\sigma^2\rho/K$ yang tak tertembus berapa pun pengukuran ditambahkan. Kami juga menunjukkan bahwa design effect Kish mengukur estimator yang **tidak** dipakai HCP, dan menyediakan ukuran yang tepat beserta uji diagnostik untuk menentukan tingkat blok mana yang layak dikalibrasi sebelum model apa pun dilatih.

#### Pemetaan dataset ke titik pengamatan

| Tingkat blok | Sumber | $K_1$ kalibrasi | Design effect | Peran |
|---|---|---:|---:|---|
| Detak → Rekaman | MIT-BIH | ~23 subjek | ~2.347 | Ujung ekstrem; bukti eksistensi masalah |
| Rekaman → Pasien | PTB-XL | **1.942** | **1,39** | **Kasus utama**; seluruh $\alpha$ layak |
| Rekaman → Situs | PTB-XL | 40 | 427,1 | Efisiensi terbaik di antara granularitas kasar, **dan $\alpha{=}0{,}05$ layak** |
| Rekaman → Perangkat | PTB-XL | 11 | 1.981,7 | Kurang efisien, **dan $\alpha{=}0{,}05$ mustahil** |
| Rekaman → Perawat | PTB-XL | 12 | 1.693,8 | Hanya $\alpha{=}0{,}10$ yang layak |
| Covariate shift | NSTDB | — | — | 6 level SNR; robustness cakupan |

> Design effect di tabel ini memakai $\mathrm{DEff}_{\text{blok}}$ pada $\rho{=}1$ (ukuran yang benar untuk HCP), **bukan** Kish. Lihat koreksi di Temuan 4.

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

### 5.8 ✅ Temuan 9 — Kontradiksi terselesaikan: **design effect**, bukan ICC

Temuan 8 menyisakan teka-teki: H0 terrefutasi di PTB-XL tetapi MIT-BIH seharusnya berperilaku sebaliknya. Empat eksperimen berturut-turut menyelesaikannya — dan **dua di antaranya membatalkan kesimpulan saya sendiri**.

#### Urutan pembalikan

| Tahap | Kesimpulan sementara | Dibatalkan oleh |
|---|---|---|
| 1 | "B12 memperbaiki B1 di MIT-BIH → H0b terkonfirmasi" | **Kontrol permutasi**: 81–107% selisih bersifat mekanis |
| 2 | "Defisit berasal dari ketimpangan $N_k$" | **Faktorial 2×2**: ketimpangan 0/3, klaster 3/3 |
| 3 | "Defisit naik monoton terhadap ICC" | **PTB-XL**: ICC 0,35 tetapi defisit nol |
| 4 | **"Defisit naik monoton terhadap DEff"** | — bertahan |

Setiap pembalikan datang dari **menambah kontrol**, bukan menafsir ulang data yang sama.

#### Kriteria (b) ternyata tautologis

Pada $K_1{=}11$, atom $+\infty$ berbobot $\tfrac{1}{12}$ memaksa HCP menembus persentil

$$\frac{1-\alpha}{K_1/(K_1+1)}$$

Ramalan ini cocok sampai **empat desimal** pada lengan permutasi:

| $\alpha$ | Diramalkan | Teramati |
|---|---:|---:|
| 0,10 | 0,9818 | **0,9819** |
| 0,15 | 0,9273 | **0,9273** |
| 0,20 | 0,8727 | **0,8729** |

Artinya "B12 mencakup lebih baik daripada B1" nyaris dijamin saat $\alpha$ dekat $\alpha_{\min}$ — **bukan bukti dependensi**. Kriteria ini dicabut sebagai alat uji.

#### Faktorial 2×2 memisahkan dua mekanisme

| Faktor | Besar efek | Signifikan |
|---|---|---|
| **Klasterisasi** | −0,0122 … −0,0155 | **3/3** |
| Ketimpangan $N_k$ | −0,0026 … −0,0044 | 0/3 |
| Interaksi | −0,0052 … −0,0079 | 0/3 |

Lengan teracak mengenai nominal nyaris sempurna (0,9003 / 0,8499 / 0,8000), **termasuk saat blok timpang** — membuktikan ketimpangan ukuran tidak berbahaya tanpa korelasi.

#### ICC saja tidak cukup — dan itu justru menguatkan teori

PTB-XL ber-**ICC 0,3525**, setara titik MIT-BIH yang defisitnya +0,0035. Namun defisit PTB-XL **−0,0005**. Penjelasannya ada di Prop 2′ sendiri:

$$\mathrm{DEff} = 1 + (H-1)\rho, \qquad H = \text{rerata harmonik ukuran blok}$$

PTB-XL: $H{=}1{,}05 \Rightarrow \mathrm{DEff}{=}1{,}02$ meski $\rho{=}0{,}35$. Dependensi baru merusak kalibrasi bila **ada pengulangan di dalam blok untuk dikorelasikan**.

#### Kurva tunggal yang menyatukan keduanya

| Sumber | $H$ | $\rho$ | $\mathrm{DEff}$ | Defisit $\alpha{=}0{,}15$ |
|---|---:|---:|---:|---:|
| PTB-XL (pasien) | 1,05 | 0,3525 | **1,02** | −0,0012 |
| MIT-BIH $p{=}1$ | 1.355 | 0,0001 | 1,10 | +0,0001 |
| MIT-BIH $p{=}0{,}5$ | 1.355 | 0,1334 | 181,60 | −0,0004 |
| MIT-BIH $p{=}0$ | 1.355 | 0,5192 | **703,93** | **+0,0102** |

**Spearman gabungan: +0,84 / +0,80 / +0,85, seluruhnya $p<0{,}002$ — LULUS 3/3.**

#### Kejujuran yang wajib tertulis di naskah

1. **Defisit per titik tidak signifikan sendiri-sendiri** — seluruh CI memuat nol. Buktinya terletak pada **tren monoton**, dan itu memang yang diuji kriteria Spearman pra-registrasi.
2. **PTB-XL menyumbang 1 dari 12 titik.** Korelasi gabungan digerakkan gradien internal MIT-BIH. Peran PTB-XL adalah **uji ramalan**: kurva meramalkan defisit nol pada $\mathrm{DEff}{\approx}1$, dan itulah yang terjadi — pada modalitas berbeda (12-sadapan vs 1), tugas berbeda (multi-label vs multi-kelas), dan jenis blok berbeda (pasien vs rekaman).
3. **Kontrol permutasi bersifat post-hoc**, tercatat di [protocol.md §12](docs/protocol.md).

#### Konsekuensi terhadap C4

| | Status |
|---|---|
| **C4** | ✅ **DIPULIHKAN dengan kualifikasi.** Berlaku bila $\mathrm{DEff}$ tinggi; nihil bila $\mathrm{DEff}\approx1$. Bukan klaim tanpa syarat |
| **C6, C7, C8** | ✅ Tidak tersentuh, dan **C6 kini punya dukungan empiris** — Prop 2′ meramalkan dengan benar di mana ICC gagal |
| Nilai tambah | Praktisi dapat menghitung $\mathrm{DEff}$ **sebelum melatih model** untuk memutuskan apakah koreksi blok diperlukan |

> Kontradiksi PTB-XL vs MIT-BIH bukan kelemahan naskah — ia **bukti bahwa besaran teoretisnya benar**. Dua dataset yang tampak bertentangan ternyata dua dosis pada satu kurva.

Skrip: [`experiments/control_permutation_mitdb.py`](experiments/control_permutation_mitdb.py) · [`factorial_mitdb.py`](experiments/factorial_mitdb.py) · [`monotonicity_icc_mitdb.py`](experiments/monotonicity_icc_mitdb.py) · [`dose_response.py`](experiments/dose_response.py)

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
| **C6** | Batas kelayakan $\alpha \ge \frac{1}{K_1+1}$ terhadap design effect — pertanyaan terbuka mereka |
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

> ✅ **SELESAI (2026-09-29).** B1 dan B12–B15 terimplementasi di [src/conformal/calibration.py](src/conformal/calibration.py); **52 unit test** lolos di [tests/test_conformal.py](tests/test_conformal.py). Ini memenuhi satu prasyarat pembekuan protokol §13.

#### Temuan sampingan — B15 punya **dua** syarat kelayakan, bukan satu

Ditemukan saat menulis unit test, bukan dari literatur. Karena Double Conformal mengambil kuantil $1-\alpha/2$ **dua kali** (di dalam blok lalu lintas blok), ia menuntut dua hal sekaligus:

$$K + 1 \ge \frac{2}{\alpha} \qquad \textbf{dan} \qquad \min_k N_k + 1 \ge \frac{2}{\alpha}$$

Syarat kedua **tidak punya padanan di HCP**, yang hanya menuntut $K+1 \ge 1/\alpha$. Konsekuensinya konkret: pada $K=500$ blok dengan $N_k=5$ dan $\alpha=0{,}2$, HCP menghasilkan ambang berhingga sementara **seluruh 500 blok** B15 jatuh ke $+\infty$ — jumlah blok berlimpah tidak menolong bila tiap blok terlalu dangkal.

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
| **F1 — Fondasi Teoretis** | Minggu 1–6 | Kuasai HCP; formalkan **batas kelayakan $\alpha \ge 1/(K_1+1)$ vs design effect** (C6) dan **uji diagnostik** (C7); rumuskan perluasan multi-label (C8) | 🟡 **SELESAI kecuali review** — [`docs/theory.md`](docs/theory.md): Prop 1, 2, 2′, 3–5 + Teorema C6. Sisa: 🔴 review statistikawan atas Kor. 3.2 dan §5.6 |
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
│   ├── theory.md                 ✅ dibuat - Prop 1-3, Teorema C6, prosedur C7
│   ├── literature-review.md      <- hasil survei sistematis + tabel gap
│   └── paper/                    <- draf naskah
├── scripts/
│   ├── download_physionet.py     ✅ unduh paralel lewat mirror S3
│   ├── download_nstdb.py         ✅ unduh NSTDB langsung dari PhysioNet
│   ├── download_data.ps1         ✅ unduh via get-zip (cadangan, lambat)
│   ├── verify_datasets.py         ✅ verifikasi struktural + statistik blok
│   ├── analyze_block_structure.py ✅ n_eff & design effect multi-granularitas
│   ├── feasibility_alpha.py       ✅ batas alpha layak per granularitas (C6/C7)
│   ├── check_nesting.py           ✅ persarangan & partisi gabungan (C7)
│   ├── label_feasibility.py       ✅ kelayakan per-label pada hierarki (C8)
│   ├── design_effect_nonuniform.py ✅ DEff blok vs Kish pada blok tak seragam
│   └── check_consistency.py       ✅ angka dokumen vs data nyata (jalankan sebelum commit)
├── data/
│   ├── README.md                 ✅ dibuat - panduan akuisisi
│   ├── raw/                      <- dataset asli (tidak di-commit)
│   └── interim/                  <- hasil preprocessing
├── src/
│   ├── data/                     <- loader, preprocessing, split
│   ├── models/                   <- backbone (xresnet1d, inception1d, ...)
│   ├── conformal/                ✅ B1 + B12-B15, diagnostik blok (C7) & per-label (C8), estimator ICC
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
- [x] **Teks lengkap A0 dibaca** — Teorema 1 HCP, batas $\alpha \ge 1/(K_1+1)$, dan pertanyaan terbuka di Discussion
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
- [ ] Minta review atas perumusan batas $\alpha \ge 1/(K_1+1)$ dan perluasannya ke multi-label

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

### Langkah 4 — Studi Kelayakan Cepat ✅ SELESAI — H0 TERREFUTASI

- [x] Latih satu backbone sederhana pada PTB-XL 100 Hz — `SmallECGNet` 104.389 parameter, macro-AUROC **0,9016**
- [x] Terapkan split conformal naif **dan** HCP, 200 split acak level-pasien di dalam fold 9
- [x] **Ukur cakupan empiris** — 0,9910 / 0,9511 / 0,9010 vs target 0,99 / 0,95 / 0,90: **tepat nominal, tidak kurang**
- [x] Uji mekanisme H0 (selisih B12−B1) — CI melingkupi nol di ketiga level $\alpha$
- [x] Catat hasil di [`docs/protocol.md`](docs/protocol.md) §12b beserta log penyimpangan
- [x] **Uji H0b di MIT-BIH** — protokol §11 butir 1, selesai 2026-09-30. H1 lulus 5/5; H0b terkonfirmasi lewat sumbu DEff. Lihat §5.8

> Premis penelitian **tidak** perlu ditinjau ulang: C6/C7/C8 tidak bergantung pada H0. Yang terdampak hanya C4.

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
| 2026-09-29 | ~~**C6 direformulasi menjadi "dua batas yang tidak berkorelasi"**~~ ⚠️ **DICABUT 2026-09-30** | Validitas diatur $K_1$; efisiensi diatur design effect. `site` punya design effect terburuk (6.687) tetapi $\alpha=0{,}05$ layak; `device` design effect lebih baik (3.901) tetapi $\alpha=0{,}05$ mustahil. **Angka-angka itu memakai Kish, ukuran milik estimator yang salah** — lihat entri koreksi 2026-09-30 | — |
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
| 2026-09-30 | 🔧 **KOREKSI: batas kelayakan TIDAK ketat** — $\alpha \ge \frac{1}{K_1+1}$, bukan $\alpha >$ | Tepat di batas, massa berhingga $\frac{K_1}{K_1+1}$ menyamai $1-\alpha$ sehingga ambangnya jatuh di skor maksimum. Cakupan terukur 0,9512 pada $K_1{=}19,\alpha{=}0{,}05$. `minimum_blocks()` salah $+1$ di semua kasus | Ditemukan sebelum menulis teorema. Tidak ada verdict tabel yang berubah; pemeriksaan silang = syarat baku split conformal $n \ge 1/\alpha - 1$ |
| 2026-09-30 | ❗❗ **DITEMUKAN: granularitas PTB-XL tidak bersarang** | 46 pasien menyeberang `site`, 247 menyeberang `nurse`, 174 menyeberang `device`. Hanya `patient_id` ⊂ `strat_fold`. Aturan keputusan C7 "pilih yang terkasar dan layak" **runtuh** — ia mengandaikan persarangan | Aturan diganti: desain bersilang menuntut partisi **join** (komponen terhubung) |
| 2026-09-30 | 🎯 **Hasil ketidakmungkinan pada data nyata** | Mengendalikan `patient_id`+`device` sekaligus → $K_1{=}5$, $\alpha_{\min}{=}0{,}167$. Keempat sumber → $K_1{=}1$, $\alpha_{\min}{=}0{,}5$. Ini batas **desain studi**, bukan kekurangan metode — pernyataan C6 yang jauh lebih kuat daripada rumusan sebelumnya | Klaim universal ditahan: baru terbukti untuk keluarga HCP/Dunn, menunggu review statistikawan |
| 2026-09-30 | **Kish $n_{\text{eff}}$ diidentifikasi sebagai kasus $\rho{=}1$** | $\mathrm{DEff} = 1+(N-1)\rho \le N = \mathrm{DEff}_{\text{Kish}}$. Kish adalah **batas atas**, fungsi ukuran blok semata, dan buta terhadap $\rho$. Menjelaskan secara formal mengapa E11a wajib datar | E11b diarahkan ulang: estimasi $\rho(t)$, bukan $n_{\text{eff}}$ |
| 2026-09-30 | **[`docs/theory.md`](docs/theory.md) ditulis** — luaran F1 | Prop 1 (kelayakan), Prop 2 (design effect), Teorema C6 (a–d), Prop 3 (partisi join), prosedur C7. Setiap pernyataan ditandai 🟢 terbukti / 🟡 butuh asumsi / 🔴 butuh statistikawan | Pemisahan taraf pembuktian dibuat eksplisit agar tidak tercampur di naskah |
| 2026-09-30 | ⚠️ **C8 bagian cakupan-superset diakui SEPELE** | Teorema 1 HCP agnostik terhadap struktur $\mathcal{Y}$; skor $\max_{\ell\in Y}s_\ell(x)$ membuatnya berlaku tanpa modifikasi. Dijadikan bagian Metode, **bukan** klaim kontribusi | Lebih baik mengakuinya sendiri daripada dibongkar reviewer |
| 2026-09-30 | 🎯 **C8 direposisi ke kelayakan per-label** (Prop. 4–5) | Jaminan terkondisi-label menuntut $\alpha \ge 1/(K_1(\ell)+1)$ dengan $K_1(\ell)$ = blok yang memuat $\ell$. Pada PTB-XL: **24/44 kode SCP tak-layak** pada $\alpha{=}0{,}05$ marginal, **43/44** serentak. Superclass seluruhnya aman | Terhitung dari metadata saja — artefak praktisi, bukan sekadar teorema |
| 2026-09-30 | **Frontier kelayakan pada pohon label** | $K_1$ monoton naik menuju akar (0 pelanggaran dari 23 pasangan), sehingga ada antirantai pemisah wilayah layak/tak-layak. Letaknya **di antara superclass dan subclass** | Menentukan tingkat mana yang boleh diklaim di naskah |
| 2026-09-30 | **C2 diperkuat lewat Kor. 5.2** | Penutupan ke atas hanya menambahkan leluhur, yang selalu setidaknya selayak keturunannya → penutupan tak pernah memasukkan label tak-layak. Biayanya murni efisiensi | Memberi C2 isi formal yang sebelumnya hanya "monoton + ekspansif" |
| 2026-09-30 | **Prop. 2′ — blok tak seragam** | $\operatorname{Var}(\hat G) = \sigma^2[1+(H-1)\rho]/(KH)$ dengan $H$ = rata-rata **harmonik** ukuran blok. Rumus seragam bertahan persis dengan $N \mapsto H$ | Melengkapi sisa F1 |
| 2026-09-30 | 🚨 **KOREKSI BESAR: klaim "dua sumbu tidak berkorelasi" DICABUT** | Design effect Kish milik estimator terboboti-**observasi**; HCP memakai terboboti-**blok**. Berimpit hanya bila $N_k$ seragam — pada `site` selisihnya **15,7×**. Dengan ukuran benar, dua granularitas yang layak justru dua yang paling efisien; urutannya **sejalan** | Terdeteksi karena tabel empiris lama bertentangan dengan Teorema C6(c) buatan sendiri. `strat_fold` (nyaris seragam) memberi rasio 1,000 — validasi internal |
| 2026-09-30 | **Estimator $\rho(t)$ ditulis** ([`src/conformal/icc.py`](src/conformal/icc.py)) | ANOVA satu arah untuk desain tak seimbang + CI bootstrap **level blok**. Diuji memulihkan $\rho$ sejati pada $\{0;0{,}2;0{,}5;0{,}8\}$ dalam toleransi 0,05 | Bootstrap level titik akan mengulang persis kesalahan yang dikritik paper ini |
| 2026-09-30 | ❌ **H0 TERREFUTASI pada granularitas pasien PTB-XL** | Cakupan naif 0,9910/0,9511/0,9010 vs target 0,99/0,95/0,90 — tepat nominal. Selisih B12−B1 mencakup nol di ketiga $\alpha$. Sebab: rata-rata $N_k{=}1{,}12$, 90,5% pasien satu rekaman, rasio bobot 1,12× | C4 **belum dicabut** — §11 butir 1 menuntut MIT-BIH diuji dulu. C6/C7/C8 tidak tersentuh |
| 2026-09-30 | ✅ **C4 DIPULIHKAN dengan kualifikasi — sumbunya DEff, bukan ICC** | Empat eksperimen berturut: (1) kontrol permutasi membatalkan kriteria (b) sebagai 81–107% mekanis; (2) faktorial 2×2 menunjukkan klaster signifikan 3/3 sedangkan ketimpangan $N_k$ 0/3; (3) monotonisitas ICC lulus 3/3 di MIT-BIH; (4) PTB-XL ber-ICC 0,3525 namun defisit nol, sehingga ICC saja **gagal** menyatukan. Prop 2' menjelaskannya: $H{=}1{,}05 \Rightarrow \mathrm{DEff}{=}1{,}02$. Pada sumbu DEff, Spearman gabungan +0,84/+0,80/+0,85, $p<0{,}002$ | C4 berlaku **bersyarat DEff**. C6 memperoleh dukungan empiris: besaran teoretisnya meramalkan dengan benar di titik ICC gagal |
| 2026-09-30 | 🚨 **Positif palsu tertangkap: konfound kualitas label** | Rancangan pertama (kalibrasi fold 8 → uji fold 9) melaporkan defisit 1,43 pp. Fold 1–8 hanya 64–68% tervalidasi manusia vs 100% di fold 9–10. Setelah split bersih di dalam fold 9, defisit **hilang total** | Tertangkap bukan dari angka cakupan, melainkan dari pertanyaan "mengapa B12 identik B1?" |
| 2026-09-30 | 🔧 **Uji H0 diperbaiki: tambahkan CI selisih B12−B1** | Versi pertama hanya menguji "B1 kurang-cakup" (bagian a). Mekanisme H0 justru ada di selisihnya (bagian b). Menguji (a) saja menghasilkan putusan yang menyesatkan | Memperketat uji, bukan melonggarkan |
| 2026-09-30 | **Hasil nol diperlakukan sebagai kontrol positif** | Split conformal mencapai nominal *persis* — memvalidasi implementasi skor, kalibrasi, dan evaluasi. Mutu backbone tidak relevan: conformal model-agnostik | — |
| | | | |

---

## Catatan Penutup

**Tidak ada jaminan diterima di jurnal mana pun.** Dokumen ini menyusun penelitian agar **secara struktural memenuhi ekspektasi Q1** — kontribusi yang jelas, multi-dataset, statistik ketat, artefak terbuka. Sisanya bergantung pada eksekusi dan faktor di luar kendali Anda.

**Dua hal yang paling menentukan keberhasilan — per 2026-09-30:**

| # | Prioritas | Mengapa menentukan | Gagal bila |
|---|---|---|---|
| **1** | **Uji H0b di MIT-BIH** | H0 terrefutasi di PTB-XL. Protokol §11 butir 1 menuntut MIT-BIH diuji (~2.347 detak/rekaman) **sebelum** C4 dicabut | Terrefutasi juga → C4 dicabut; naskah murni C6+C7+C8 |
| **2** | **Review statistikawan** atas Kor. 3.2 dan §5.6 theory.md | Dua klaim ditandai 🔴/🟡 dan belum boleh masuk naskah tanpa diperiksa | Tidak lolos review → turunkan ke klaim khusus keluarga HCP/Dunn |
| ~~3~~ | ~~Studi kelayakan (Langkah 4)~~ | ✅ **Selesai 2026-09-30.** H0 terrefutasi; implementasi tervalidasi sebagai kontrol positif | — |
| ~~4~~ | ~~Formalkan C6 + C7 + C8 di F1~~ | ✅ **Selesai 2026-09-30** kecuali review. [`docs/theory.md`](docs/theory.md): Prop 1, 2, 2′, 3–5, Teorema C6, prosedur C7, frontier C8 | — |
| ~~5~~ | ~~Implementasi B12–B15~~ | ✅ **Selesai 2026-09-29.** [`src/conformal/`](src/conformal/), **52 unit test** lolos | — |

> **Sudah diamankan:** survei literatur ✅ selesai dan menyelamatkan sepuluh bulan. C1 ternyata sudah diterbitkan sejak 2023 — ditemukan sekarang, bukan di laporan reviewer.
>
> ✅ **Repositori git diinisialisasi 2026-09-30** — commit `5ba06f6`, 24 berkas, dataset 661,5 MB tetap di luar riwayat. `git tag protocol-v1` **sengaja belum dibuat**: protokol masih draf, dan menandainya sebelum checklist §13 tuntas akan mengosongkan makna pre-registration. Lihat [`docs/progress.md`](docs/progress.md) §10.1.

> **Dua pelajaran yang layak dicatat:**
>
> 1. Klaim gap versi pertama disusun tanpa pencarian literatur, dan ternyata keliru. Itulah sebabnya §4 kini memuat kutipan langsung dari teks yang benar-benar dibaca.
> 2. Temuan 4 versi pertama memakai $n_{\text{eff}}$ Kish sebagai penentu validitas — juga keliru. Membaca teorema aslinya, bukan hanya abstraknya, mengoreksinya menjadi $K_1$. **Intuisi yang benar dengan kuantitas yang salah tetap salah.**
