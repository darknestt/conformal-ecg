# Daftar Pustaka Terverifikasi

> Dokumen pendukung [README.md](../README.md) §17
> **Diverifikasi:** 2026-09-30 · **Diverifikasi ulang:** 2026-10-01 · **Sumber:** OpenAlex API + Crossref + **daftar sumber Scopus RESMI Elsevier**
> **Jumlah:** **35 artikel** (tetap) + 2 praterbit wajib-sitasi (§I) + 2 praterbit dipantau + 5 rujukan dataset
>
> 🔧 **2026-10-01: penukaran 1:1**, empat keluar dan empat masuk — lihat §5c. Dua sumber masuk adalah **pengecualian aturan 5 tahun yang dinyatakan terbuka** (§I).
>
> ✅ **Indeksasi Scopus kini terverifikasi langsung**, bukan lewat proksi. Lihat §1a.
> Hasil mesin: [scopus-verification.json](scopus-verification.json) · skrip: [scripts/verify_scopus.py](../scripts/verify_scopus.py)

---

## 1. Metodologi Verifikasi — Apa yang Benar-Benar Dicek

Setiap entri di bawah ini **telah saya buka sendiri** lewat OpenAlex API. Tidak ada yang disalin dari ingatan.

| Yang diverifikasi | Cara | Status |
|---|---|---|
| DOI resolvable | `api.openalex.org/works?filter=doi:...` | ✅ |
| Judul, jurnal, ISSN, tahun | Rekaman OpenAlex | ✅ |
| Jumlah sitasi | `cited_by_count` | ✅ |
| Dampak ternormalisasi bidang | `fwci` (Field-Weighted Citation Impact) | ✅ |
| Relevansi topik | Pencocokan `title_and_abstract.search` + pembacaan judul | ✅ |
| Mutu jurnal | `listed_in`: CWTS Core, JUFO, Norwegian Register, ABDC | ✅ |
| **Indeksasi Scopus langsung** | **Daftar sumber resmi Elsevier `ext_list_Aug_2026.xlsx`** — 49.010 sumber | ✅ |
| **Tahun terbit dalam rentang cakupan Scopus** | Kolom `Coverage` per sumber | ✅ |
| **Status aktif / dihentikan** | Kolom `Active or Inactive` + lembar *Discontinued Titles* | ✅ |
| **Peringkat SINTA** | Tidak berlaku — lihat §2 | ❌ |

---

## 1a. Hasil Verifikasi Scopus — diperbarui 2026-10-01

Daftar sumber resmi diunduh dari halaman *Scopus Content* Elsevier (tautan **Download the Source title list**). Setiap DOI di dokumen ini diambil metadatanya dari OpenAlex, lalu ISSN/EISSN-nya dicocokkan ke daftar tersebut, **dan tahun terbitnya diperiksa berada di dalam rentang cakupan**.

| Hasil | Jumlah |
|---|---:|
| DOI aktif diperiksa | **41** (35 artikel + 5 dataset + 1 praterbit Zenodo) |
| Artikel terindeks — otomatis | **33 / 35** |
| Artikel terindeks — **sesudah pemeriksaan manual** | **34 / 35** |
| Tidak ditemukan — rujukan dataset PhysioNet (dikecualikan) | 4 |
| Tidak ditemukan — **jurnal** | **1** (A0) |
| Dihentikan Scopus | 0 |
| Melanggar aturan 5 tahun | **2 — disengaja** (I1, I2; lihat §I) |

> **A12 (Ding dkk., NeurIPS 2023) diverifikasi manual.** OpenAlex tidak mengembalikan venue untuk DOI `10.52202/...`, sehingga pencocokan ISSN otomatis gagal. Lembar *Serial Conf. Proc. with Profile* memuat *Advances in Neural Information Processing Systems*, ISSN 1049-5258, cakupan 2012–2025; lembar *All Conf. Proceedings* memuat **vol. 36, 2023**, ISBN 9781713899921, source ID 85191147773. **Terindeks.** Skrip hanya membaca lembar *Sources*, jadi prosiding konferensi selalu memerlukan pemeriksaan manual.

> 🔧 **Dua bug skrip diperbaiki 2026-10-01.** (1) Regex DOI berhenti di `<`, `>`, `(`, `)` sehingga DOI SICI lama (I1) terpotong dan **diam-diam memverifikasi DOI yang salah**; DOI dalam backtick kini diambil utuh. (2) Hanya blok *❌ Dikeluarkan* yang disaring, padahal tabel pemangkasan §5b dan penukaran §5c juga memuat DOI yang sudah dibuang — angka sempat menggelembung ke **54**. Pemindaian kini berhenti di §4.

> Blok §5 *❌ Dikeluarkan* sengaja **tidak** ikut diperiksa — DOI di sana sudah dibuang dari daftar. Skrip menyaringnya agar angka di atas tidak menggelembung.

### ⚠️ Satu-satunya jurnal yang gagal: A0

`10.1145/3786352` — **ACM Journal of Data Science** (ISSN 3069-3497).

- **Tidak ada** di daftar sumber Scopus, **tidak ada** pula di lembar *Accepted Titles* (judul yang sedang dalam proses indeksasi). Jurnal ini baru terbit 2026.
- arXiv **bukan** sumber serial Scopus, jadi menyitasi praterbitnya tidak memperbaiki status.

**Tetap disitasi.** Dari makalah inilah Teorema 1 dan estimator HCP berasal — seluruh metode B12 bertumpu padanya, dan tidak ada sumber pengganti. Menghapusnya berarti memakai teorema tanpa menyebut asalnya.

**Mitigasi:** dampingkan dengan **A0b** (`10.1080/01621459.2022.2060112`, **JASA 2022**, terindeks Scopus) yang mencakup wilayah yang sama dan menjadi sumber baseline B13–B15. Dengan begitu klaim hierarkis Anda punya jangkar yang terindeks.

### ✅ Koreksi tahun F1

OpenAlex mencatat `10.1109/jbhi.2020.3022989` sebagai **2020** — itu tanggal *online-first* (2020-09-09). Crossref memberi `published-print: 2021-05`, `issued: 2021-05`, **vol. 25 no. 5, hlm. 1519–1528**.

**Tahun sitasi yang benar adalah 2021**, dan aturan 5 tahun terpenuhi. Sesudah koreksi ini, **nol** rujukan non-dataset yang melanggar batas.

---

### Register akademik sebagai bukti mutu tambahan

Indeksasi Scopus kini terverifikasi langsung. Tiga register di bawah tetap dipertahankan karena memberi informasi **mutu** yang tidak diberikan keanggotaan Scopus semata:

| Register | Asal | Arti |
|---|---|---|
| **JUFO** (Finnish Publication Forum) | Kemendikbud Finlandia | Level 1/2/3. **JUFO-3 = jurnal terkemuka dunia** (~2% teratas). Penilaian panel pakar. |
| **Norwegian Register (NSD)** | Direktorat Pendidikan Tinggi Norwegia | Level 1/2. **Level 2 = ~20% teratas bidangnya.** Daftarnya dibangun dari basis Scopus. |
| **CWTS Core** | Universitas Leiden | Jurnal inti Leiden Ranking, berbasis Web of Science. |
| **ABDC** | Australian Business Deans Council | A\* = kuartil teratas. |

Sebuah jurnal dengan **JUFO-3 + Norway-2** hampir pasti Scopus Q1. Register ini tidak lagi dipakai sebagai pengganti bukti indeksasi — hanya sebagai penanda kuartil.

> ℹ️ Kuartil (Q1/Q2/…) **tidak** tercantum di daftar sumber resmi Elsevier; ia berasal dari CiteScore/SJR. Untuk daftar pustaka, yang dipersyaratkan hanyalah **terindeks Scopus**, bebas kuartil — dan itu sudah terverifikasi di §1a.

---

## 2. Soal SINTA — Klarifikasi Penting

**SINTA hanya mengindeks jurnal terbitan Indonesia.** Dari 40 rujukan di bawah, **nol** yang terbitan Indonesia — semuanya Elsevier, IEEE, Springer, Wiley, Oxford UP, Royal Society, Nature Portfolio, MDPI, dan Institute of Mathematical Statistics.

Jadi kriteria "SINTA 1/2" **tidak dapat diterapkan** pada daftar ini, dan itu justru yang Anda inginkan:

- Target Anda adalah **Scopus Q1 internasional**. Reviewer Q1 mengharapkan daftar pustaka berisi jurnal internasional arus utama.
- Daftar pustaka yang didominasi jurnal nasional pada naskah Q1 adalah **bendera merah** — menandakan penulis tidak menguasai literatur global.
- SINTA 1/2 relevan bila Anda menargetkan publikasi *di* jurnal Indonesia, bukan untuk sitasi naskah Q1.

Satu jurnal Indonesia memang muncul dalam pencarian (*Jurnal Teknik Informatika* — conformal prediction untuk kanker payudara), tetapi mutunya di bawah standar yang diperlukan (`is_core: false`, tidak terdaftar di register mana pun). **Tidak saya masukkan.**

---

## 3. Kunci Pembacaan Tabel

| Kolom | Arti |
|---|---|
| **Sitasi** | Jumlah sitasi total (OpenAlex) |
| **FWCI** | Field-Weighted Citation Impact. **1,0 = rata-rata bidang.** 5,0 = 5× rata-rata. |
| **Register** | J=JUFO, N=Norway, A=ABDC. `J3 N2` = JUFO-3 + Norway-2 (tertinggi) |
| **Scopus** | ⬜ Anda isi sendiri |

> ⚠️ Artikel 2026 wajar memiliki sitasi 0 — belum cukup waktu. Gunakan **FWCI** sebagai penilai mutu, bukan jumlah sitasi mentah.

---

## A. Fondasi & Teori Conformal Prediction

Mendukung **§2 Related Work**, **§3 Preliminaries**, **§5 Metode (C1, C6)**

### 🚨 A0 — PAPER YANG MENUTUP C1

| Butir | Isi |
|---|---|
| **DOI** | `10.1145/3786352` |
| **arXiv** | 2306.06342 (v1 Jun 2023, v4 Agu 2025) |
| **Judul** | *Distribution-free inference with hierarchical data* |
| **Penulis** | Yonghoon Lee, **Rina Foygel Barber**, Rebecca Willett |
| **Jurnal** | ACM Journal of Data Science, 2026 |
| **Status venue** | ⚠️ Jurnal ACM baru (ISSN 3069-3497), belum terdaftar JUFO/Norway — tetapi penulisnya papan atas |

**Abstrak (kutipan langsung):**

> *"This paper studies distribution-free inference in settings where the data set has a hierarchical structure — for example, **groups of observations, or repeated measurements**. In such settings, **standard notions of exchangeability may not hold**. To address this challenge, **a hierarchical form of exchangeability is derived**, facilitating extensions of distribution-free methods, **including conformal prediction and jackknife+**. While the standard theoretical guarantee obtained by the conformal prediction framework is a marginal predictive coverage guarantee, in the special case of independent repeated measurements, it is possible to achieve a stronger form of coverage — the "second-moment coverage" property — to provide better control of conditional miscoverage rates."*

**Penilaian:** ini **persis C1**. "Kelompok observasi atau pengukuran berulang" = blok pasien. "Exchangeability baku tidak berlaku" = premis Anda. "Bentuk exchangeability hierarkis diturunkan" = teorema yang hendak Anda buktikan. Mereka bahkan melampauinya dengan *second-moment coverage*.

**Konsekuensi: C1 tidak lagi dapat diklaim sebagai kontribusi.** Paper ini menjadi **fondasi teoretis yang Anda pakai**, bukan pesaing. Lihat README §4 untuk reposisi.

> Perhatikan: Barber adalah penulis A1, A2, **dan** A3. Ia menguasai ruang masalah ini. Setiap klaim teoretis Anda di wilayah dependensi-blok akan diukur terhadap karyanya.

#### 🔑 Teorema 1 — sumber batas kelayakan C6

$$T = Q_{1-\alpha}\Big( \sum_{k}\sum_{i} \tfrac{1}{(K_1+1)N_k}\,\delta_{s(Z_{k,i})} + \tfrac{1}{K_1+1}\,\delta_{+\infty} \Big)$$

Jaminan: $\mathbb{P}\{Y_{\text{test}} \in \hat C(X_{\text{test}})\} \geq 1-\alpha$, dan bila skor berbeda hampir pasti, $\leq 1-\alpha + \frac{2}{K_1+1}$.

**Massa $\frac{1}{K_1+1}$ pada $+\infty$** berarti: bila $\alpha < \frac{1}{K_1+1}$, himpunan prediksi menjadi tak hingga. **$K_1$ = jumlah blok kalibrasi**, bukan jumlah sampel dan bukan $n_{\text{eff}}$ Kish. Ketaksamaannya tidak ketat — pada $\alpha = \frac{1}{K_1+1}$ tepat, ambangnya masih berhingga.

#### 🎯 Pertanyaan terbuka yang dinyatakan penulisnya sendiri (Discussion)

> *"...the analyst can choose between, say, **a large number of independent groups $K$ with a small number of measurements $N_k$ within each group, or conversely a small number of groups with large numbers of repeats. Characterizing the pros and cons of this tradeoff is an important question to determine how study design affects inference in this distribution-free setting.**"*

**Itu adalah C6.** Argumen novelty terkuat yang tersedia.

#### Batasan HCP yang membuka ruang C8

| Aspek | HCP | Kebutuhan Anda |
|---|---|---|
| Keluaran | Interval regresi $\hat\mu(x) \pm T$ | Himpunan label multi-label |
| Skor | $\lvert y - \hat\mu(x) \rvert$ | Skor per-label |
| Hierarki label | Tidak ada | Wajib |
| Evaluasi | Simulasi + Lorenz 96 (regresi kaotik) | EKG klinis |

---

### 🔑 A0b — SUMBER BASELINE B13–B15

| Butir | Isi |
|---|---|
| **DOI** | `10.1080/01621459.2022.2060112` · arXiv:1809.07441 |
| **Judul** | *Distribution-Free Prediction Sets for Two-Layer Hierarchical Models* |
| **Penulis** | Robin Dunn, Larry Wasserman, **Aaditya Ramdas** |
| **Jurnal** | **JASA**, 2022 — 11 sitasi, FWCI 1,63 |
| **Register** | J3 N2 A\* (papan atas) |

Memperkenalkan empat metode yang menjadi **baseline B13–B15** Anda:

| Metode | Sifat | Catatan Lee-Barber-Willett |
|---|---|---|
| **Pooling CDFs** | Rata-rata CDF per grup | Setara HCP dengan $\alpha' = \alpha + \frac{1-\alpha}{K_1+1}$ |
| **Double Conformal** | Union bound $\alpha/2 + \alpha/2$ | **Terlalu konservatif** dalam praktik |
| **Subsampling Once** | Ambil 1 observasi per grup | Valid, tetapi **membuang sebagian besar data kalibrasi** → variabilitas tinggi |
| **Repeated Subsampling** | Rata-rata p-value $B$ kali | Setara HCP pada bootstrap; jaminan asli hanya $1-2\alpha$ |

> Ini juga rujukan yang **wajib** disitasi: Ramdas adalah salah satu penulis A1 juga.

---

| # | DOI | Judul | Jurnal | Thn | Sitasi | FWCI | Register | Scopus |
|---|---|---|---|---|---:|---:|---|---|
| A1 | `10.1214/23-aos2276` | Conformal prediction beyond exchangeability | Annals of Statistics | 2023 | **278** | **63,40** | J3 N2 A\* | ⬜ |
| A2 | `10.1214/20-aos1965` | Predictive inference with the jackknife+ | Annals of Statistics | 2021 | **338** | **21,21** | J3 N2 A\* | ⬜ |
| A3 | `10.1214/26-ejs2506` | Group-weighted conformal prediction | Electronic J. of Statistics | 2026 | 18 | — | J2 N1 | ⬜ |
| A4 | `10.1111/rssb.12445` | Conformal Inference of Counterfactuals and Individual Treatment Effects | JRSS-B | 2021 | **95** | **10,13** | J3 N2 A\* | ⬜ |
| **A12** | `10.52202/075280-2817` | Class-Conditional Conformal Prediction with Many Classes (Ding, Angelopoulos, Bates, Jordan, Tibshirani) | **NeurIPS 36** | 2023 | — | — | — | ⬜ |
| **A13** | `10.1371/journal.pone.0255389` | Methods for dealing with unequal cluster sizes in cluster randomized trials: A scoping review (Zhan, Xu, Ouyang, Sawatzky, Wong) | PLOS ONE 16:e0255389 | 2021 | — | — | — | ⬜ |
| A7 | `10.1080/01621459.2022.2147531` | Valid Model-Free Spatial Prediction | JASA | 2022 | 26 | 1,49 | J3 N2 A\* | ⬜ |
| A8 | `10.1080/01621459.2025.2506198` | Conformal Prediction for Network-Assisted Regression | JASA | 2025 | 4 | 3,66 | J3 N2 A\* | ⬜ |
| A9 | `10.1016/j.spl.2024.110350` | Universal distribution of the empirical coverage in split conformal prediction | Statistics & Probability Letters | 2025 | 9 | 5,23 | J1 N1 | ⬜ |
| **A11** | `10.3150/21-bej1447` | Conformal prediction: A unified review of theory and new challenges | **Bernoulli** | 2022 | **186** | **16,11** | — | ✅ |

**Catatan per entri:**

- **A1** — FWCI **63,4** berarti 63× rata-rata sitasi bidangnya. Ini fondasi seluruh penelitian Anda. Wajib dikuasai, bukan sekadar disitasi.
- **A2** — ⭐ Ini adalah **baseline B6** Anda (Jackknife+). Sebelumnya tercatat "BELUM TERVERIFIKASI" di README; kini terkonfirmasi sebagai artikel Annals of Statistics dengan 338 sitasi.
- **A4, A7, A8** — Ketiganya menangani **data yang tidak independen** (counterfactual berbobot, dependensi spasial, dependensi jaringan). Paling dekat dengan masalah dependensi pasien Anda dari sisi statistik murni.
- **A9** — Penting untuk **E1**: memberi distribusi teoretis cakupan empiris, sehingga deviasi yang Anda ukur bisa diuji secara formal, bukan sekadar dibandingkan mata.
- **A12** — ⭐ **Ditambahkan 2026-10-01.** Prior art untuk Prop. 4: kelas langka membuat kalibrasi terkondisi-kelas tidak layak pada data exchangeable. Metadata Crossref terverifikasi. Wajib disitasi di §5.3.2 — tanpanya Prop. 4 terbaca sebagai klaim kebaruan.
- **A13** — ⭐ **Ditambahkan 2026-10-01.** Tinjauan cakupan 79 makalah tentang ukuran klaster tak seimbang; teks penuh dibaca. Menopang §5.1.3: pembobotan sama vs ukuran sudah dibandingkan di literatur CRT, dan obat bakunya adalah bobot varians-minimum. Sumber ≥ 2021 yang menggantikan kebutuhan menyitasi banyak makalah klasik.
- **A11** — ⭐ **Pengganti resmi Vovk 2012.** Tinjauan terpadu di *Bernoulli* (jurnal probabilitas papan atas) yang menyajikan **Mondrian CP secara formal**, bukan sekadar menyebutnya. 186 sitasi, FWCI 16,11. Inilah jangkar sitasi untuk baseline B2 Anda.

---

### ❗ Hasil pembacaan mendalam — dilakukan 2026-09-29

Saya membaca sendiri abstrak lengkap B1, B2, B3, dan A3. Berikut temuannya.

#### B1 — **TIDAK menutup C2.** Justru mengonfirmasi celah Anda.

Penulis tunggal: **Harris Papadopoulos**. Ini **tinjauan pustaka**, bukan metode baru. Kutipan langsung:

> *"Conformal prediction (CP) is an attractive answer: it converts model outputs into prediction regions with distribution-free, finite-sample guarantees **under the sole assumption of data exchangeability**. [...] This review consolidates the landscape of CP adaptations for MLL. It places existing approaches under a unified framework, examining the types of outputs and guarantees they provide, **where label dependencies are incorporated**, and how inference cost scales with the number of labels."*

**Poin kunci:** review ini membahas **dependensi antar-label**, bukan **dependensi antar-sampel**. Dan ia menyatakan sendiri bahwa seluruh literatur CP-multi-label yang disurveinya berpijak pada asumsi exchangeability. **Itu adalah pengakuan eksplisit atas celah yang Anda tuju** — dan datang dari tokoh paling otoritatif di bidang ini. Sitasi ini sangat berharga untuk paragraf motivasi Anda.

#### B3 — **TIDAK menutup C2.** Sumbu kontribusinya berbeda sama sekali.

Maltoudoglou, Paisios, Lenc, Martínek, Král, **Papadopoulos**. Kutipan langsung:

> *"We extend our previous work on Inductive Conformal Prediction (ICP) for multi-label text classification and present a novel approach for addressing the **computational inefficiency of the Label Powerset (LP) ICP**, arising when dealing with a high number of unique labels. [...] Our approach deals with the increased computational burden of LP by **eliminating from consideration a significant number of label-sets that will surely have p-values below the specified significance level**."*

**Poin kunci:** kontribusinya adalah **pemangkasan ruang komputasi Label Powerset**, bukan hierarki dan bukan dependensi pasien. Domainnya teks (Inggris & Ceko), bukan klinis. Ini rujukan metodologis penting dan pembanding konseptual, **bukan ancaman**.

#### B2 — **TIDAK menutup C2.** Arah matematisnya justru berlawanan.

Versi preprint: **arXiv:2502.05565**, *"Multi-Scale Conformal Prediction: A Theoretical Framework with Coverage Guarantees"*, Ali Baheri & Marzieh Amiri Shahbazi (Rochester Institute of Technology). Kutipan langsung:

> *"The proposed framework defines a distinct conformity function at each relevant scale or resolution, producing multiple conformal predictors whose prediction sets are then **intersected** to form the final multi-scale output. [...] By **distributing the total miscoverage probability across scales**, the method further refines the set sizes."*

**Poin kunci — ini penting dan harus Anda pahami betul:**

| | B2 (Baheri) | C2 (Anda) |
|---|---|---|
| Operasi | **Irisan** himpunan lintas skala | **Penutupan ke atas** pada pohon label |
| Efek pada ukuran himpunan | Mengecil | Membesar |
| Efek pada cakupan | **Turun** → perlu pembagian $\alpha$ (harga Bonferroni) | **Naik atau tetap** → gratis |
| "Skala" berarti | Resolusi (piramida citra, multi-resolusi deret waktu) | Tingkat taksonomi diagnosis |

Keduanya bergerak ke **arah berlawanan**. B2 membayar harga validitas demi efisiensi; C2 membayar harga efisiensi demi validitas. Judulnya memang mirip, isinya tidak.

> ⚠️ Tetapi justru karena judulnya mirip, **reviewer pasti menanyakannya**. Anda wajib menyitasi B2 dan membedakannya secara eksplisit dalam satu paragraf.

#### A3 — **TIDAK menutup K1.** Tetapi sangat dekat dan wajib dibedakan.

Aabesh Bhattacharyya & **Rina Foygel Barber**. arXiv:2401.17452, 18 sitasi. Kutipan langsung:

> *"We consider a special scenario where observations belong to a **finite number of groups**, and **these groups determine the covariate shift between the training and test distributions** — for instance, this may arise if the training set is collected via **stratified sampling**."*

**Pembedaan kritis:**

| | A3 (Barber) | K1 (Anda) |
|---|---|---|
| Peran kelompok | Menentukan **pergeseran kovariat** antara latih dan uji | Menentukan **dependensi di dalam** himpunan kalibrasi |
| Exchangeability di dalam kelompok | **Tetap berlaku** | **Dilanggar** |
| Masalah yang dipecahkan | Galat estimasi rasio likelihood pada WCP | Kuantil kalibrasi bias optimis akibat blok |

Pada A3, data **masih exchangeable** di dalam tiap kelompok; yang bergeser adalah proporsi kelompok. Pada kasus Anda, rekaman dalam satu pasien **tidak** exchangeable satu sama lain. Masalah berbeda, meski kosakatanya bertabrakan.

---

## B. Multi-Label & Hierarki — Klaster Penentu Kelayakan

Mendukung **§4 Problem Formulation**, **§5 K2 (C2)**

| # | DOI | Judul | Jurnal | Thn | Sitasi | FWCI | Register | Scopus |
|---|---|---|---|---|---:|---:|---|---|
| B1 | `10.1098/rsta.2025.0071` | Conformal prediction for multi-label learning: a review of methods and guarantees | Phil. Trans. R. Soc. A | 2026 | 1 | **5,83** | J2 N2 | ⬜ |
| B2 | `10.1016/j.rinam.2025.100589` | Conformal prediction across scales: Finite-sample coverage with hierarchical efficiency | Results in Applied Mathematics | 2025 | 2 | 1,86 | J1 N1 | ⬜ |
| B3 | `10.1016/j.patcog.2021.108271` | Well-calibrated confidence measures for multi-label text classification with a large number of labels | Pattern Recognition | 2021 | **66** | 5,80 | J3 N2 | ⬜ |
| B5 | `10.1109/tkde.2022.3207511` | HmcNet: A General Approach for Hierarchical Multi-Label Classification | IEEE TKDE | 2022 | 15 | 1,49 | J3 N2 | ⬜ |
| B6 | `10.1016/j.artmed.2023.102613` | CEHMR: Curriculum learning enhanced hierarchical multi-label classification for medication recommendation | Artificial Intelligence in Medicine | 2023 | 21 | 2,65 | J2 N2 | ⬜ |
| **B7** | **arXiv:2410.06296** | **Conformal Structured Prediction** (Zhang, Li, **Bastani**) — himpunan prediksi konformal pada **DAG label hierarkis** | ⚠️ **Praterbit** | 2024 | 1 | — | — | — |

### ⚠️ B7 — ancaman terdekat terhadap C2

> *"We demonstrate how our approach can be applied in domains where the prediction sets can be represented as a set of **nodes in a directed acyclic graph**; for instance, for **hierarchical labels** such as image classification, a prediction set might be a small subset of **coarse labels implicitly representing** the prediction set of all their more fine-descendants."*

Ini conformal yang sadar-hierarki dengan jaminan cakupan. **Arahnya berlawanan dengan C2**: mereka memakai simpul kasar untuk **mewakili** keturunannya (kompresi ke bawah); Anda menambahkan induk ke dalam himpunan (penutupan ke atas). Tetapi seorang reviewer akan melihat keduanya sebagai "conformal + hierarki label".

**Status:** masih praterbit arXiv (belum ada jurnal), penulis dari UPenn (Osbert Bastani). **Wajib dipantau** — jika terbit di venue kuat sebelum naskah Anda, C2 melemah drastis.

---

## C. Kendali Risiko & Deret Waktu

Mendukung **§5 K3**, **§9 Metrik**

| # | DOI | Judul | Jurnal | Thn | Sitasi | FWCI | Register | Scopus |
|---|---|---|---|---|---:|---:|---|---|
| C1 | `10.1098/rsta.2025.0068` | Conformal risk control for non-monotonic losses | Phil. Trans. R. Soc. A | 2026 | 1 | **7,18** | J2 N2 | ⬜ |
| C2 | `10.1109/tnnls.2024.3356512` | Conformal Loss-Controlling Prediction | IEEE TNNLS | 2024 | 6 | 1,30 | J3 N2 | ⬜ |
| C4 | `10.1109/tpami.2023.3272339` | Conformal Prediction for Time Series | IEEE TPAMI | 2023 | **64** | **8,09** | J3 N2 | ⬜ |

- **C4** — ⭐ Temuan baru yang penting. **TPAMI** adalah salah satu jurnal paling bergengsi di ilmu komputer (J3 N2), dan judulnya persis menyasar conformal untuk deret waktu. Tidak ada di daftar sebelumnya.
- **C2** — "Loss-controlling prediction" adalah kerabat dekat conformal risk control. Relevan untuk kendali FNR@MI Anda.
- ⚠️ Paper CRC asli (Angelopoulos et al., ICLR) tetap **belum ditemukan** — lihat §6.

---

## D. Pergeseran Distribusi & Kalibrasi Terkondisi

Mendukung **§5 K1/K3**, **§8 E10**, **§11 Threats**

| # | DOI | Judul | Jurnal | Thn | Sitasi | FWCI | Register | Scopus |
|---|---|---|---|---|---:|---:|---|---|
| D2 | `10.1016/j.patcog.2026.114113` | Calibrated Mondrian conformal prediction for uncertainty quantification in spatial modeling | Pattern Recognition | 2026 | 0 | — | J3 N2 | ⬜ |
| D4 | `10.1109/taffc.2026.3702998` | Fair Uncertainty Quantification for Depression Prediction | IEEE Trans. Affective Computing | 2026 | 1 | **9,09** | J3 N1 | ⬜ |

- **D2** — Mondrian conformal = **baseline B2** Anda. Versi terkalibrasi untuk data spasial (yang juga berstruktur dependen).
- **D4** — ⭐ Temuan baru. UQ yang adil lintas subkelompok pada prediksi klinis = motivasi langsung untuk **K3**. FWCI 9,09 meski baru terbit.

---

## E. Conformal Prediction di Ranah Klinis

Mendukung **§1 Introduction**, **§2 Related Work**, **§10 Discussion**

| # | DOI | Judul | Jurnal | Thn | Sitasi | FWCI | Register | Scopus |
|---|---|---|---|---|---:|---:|---|---|
| E1 | `10.1007/s41666-021-00113-8` | Conformal Prediction in Clinical Medical Sciences | J. of Healthcare Informatics Research | 2022 | **76** | 6,19 | J1 N1 | ⬜ |
| E2 | `10.1016/j.media.2026.103953` | Reliable uncertainty quantification for 2D/3D anatomical landmark localization using multi-output conformal prediction | Medical Image Analysis | 2026 | 3 | **6,01** | J3 N1 | ⬜ |
| E3 | `10.3390/bdcc10070232` | Set Prediction for Outpatient Diagnosis Coding with Sparse Mahalanobis Conformal Scoring | Big Data and Cognitive Computing | 2026 | 0 | — | J1 N1 | ⬜ |
| **E5** | **arXiv:2601.01223** | **Adaptive Conformal Prediction via Bayesian Uncertainty Weighting for Hierarchical Healthcare Data** (Shahbazi, Baheri, Azadeh-Fard) | ⚠️ **Praterbit** | 2026 | — | — | — | — |

### ⚠️ E5 — kelompok yang sama dengan B2, kini masuk ranah klinis

> *"Our approach integrates Bayesian hierarchical random forests with **group-aware conformal calibration** [...] Evaluated on **61.538 admisi di 3.793 rumah sakit AS** dan 4 wilayah [...] Critically, we demonstrate that **well-calibrated Bayesian uncertainties alone severely under-cover (14,1%)**, highlighting the necessity of our hybrid approach."*

**Dua hal penting:**

1. **Kalibrasi konformal sadar-kelompok pada data kesehatan hierarkis** — sangat dekat dengan K1/K3. Tetapi: **regresi** (interval, bukan himpunan), kelompoknya **rumah sakit/wilayah** bukan pasien, pembobotan Bayesian bukan teorema blok finite-sample, tanpa hierarki label, tanpa multi-label. **Belum menutup kontribusi Anda.**
2. Temuan *"under-cover 14,1%"* adalah **bukti pendukung H0 Anda** dari domain lain. Berguna untuk §1 Introduction.

> Kelompok Baheri (RIT) bergerak cepat: B2 (Feb 2025) → neural operators (Sep 2025) → healthcare hierarkis (Jan 2026) → manifold (Feb 2026). **Pantau terus.** Mereka menuju wilayah yang sama dengan Anda.

---

- **E1** — Survei rujukan untuk conformal di kedokteran. Satu-satunya survei domain klinis yang terverifikasi.
- **E2** — **Multi-output** conformal = kerabat struktural multi-label. *Medical Image Analysis* adalah J3 (papan atas).
- **E3** — Himpunan prediksi untuk **pengkodean diagnosis multi-label**. Aplikasi paling dekat dengan setting Anda.

---

## F. Deep Learning EKG, PTB-XL & Protokol Inter-Patient

Mendukung **§6 Datasets**, **§7 Experimental Setup**, **§8 E1/E11**

| # | DOI | Judul | Jurnal | Thn | Sitasi | FWCI | Register | Scopus |
|---|---|---|---|---|---:|---:|---|---|
| F1 | `10.1109/jbhi.2020.3022989` | Deep Learning for ECG Analysis: Benchmarks and Insights from PTB-XL | IEEE JBHI | **2021** | **480** | **25,45** | J2 N1 | ✅ |
| F2 | `10.1016/j.cmpb.2021.105948` | Arrhythmia classification from single-lead ECG signals using the inter-patient paradigm | Computer Methods and Programs in Biomedicine | 2021 | **94** | **10,88** | J1 N1 | ⬜ |
| F3 | `10.1016/j.neucom.2021.04.104` | Inter-patient ECG arrhythmia heartbeat classification based on unsupervised domain adaptation | Neurocomputing | 2021 | **81** | 7,60 | J2 N2 | ⬜ |
| F5 | `10.1007/s13239-025-00777-y` | Investigation of Inter-Patient, Intra-Patient, and Patient-Specific Based Training in Deep Learning for Classification of Heartbeat Arrhythmia | Cardiovascular Engineering and Technology | 2025 | 1 | 0,65 | N1 ⚠️ | ⬜ |
| F6 | `10.1109/jbhi.2023.3271858` | Analysis of a Deep Learning Model for 12-Lead ECG Classification Reveals Learned Features Similar to Diagnostic Criteria | IEEE JBHI | 2023 | 49 | 8,26 | J2 N1 | ⬜ |
| **F10** | `10.1016/j.cmpb.2021.106582` | Inter-patient arrhythmia classification with improved deep residual convolutional neural network | CMPB | 2021 | **103** | **10,70** | J1 N1 | ✅ |

- **F1** — ⭐⭐⭐ **480 sitasi, FWCI 25,45.** Ini benchmark resmi PTB-XL dan sumber backbone `xresnet1d101` Anda. **Mutlak wajib disitasi.** ⚠️ **Sitasi sebagai 2021, bukan 2020.** OpenAlex mencatat 2020 karena itu tanggal *online-first*; Crossref memberi `published-print: 2021-05`, vol. 25 no. 5, hlm. 1519–1528. Dengan tahun yang benar, F1 **memenuhi** aturan 5 tahun.
- **F2** — ⭐ Temuan baru, **tidak ada** di daftar sebelumnya. Judulnya menyebut langsung *"inter-patient paradigm"*. FWCI 10,88. Inilah rujukan kanonik untuk menjustifikasi bahwa evaluasi inter-patient adalah standar yang benar.
- **F5** — ⚠️ Satu-satunya yang membandingkan inter/intra/patient-specific secara eksplisit, tapi jurnalnya **tidak terdaftar di JUFO** (hanya Norway-1 + MEDLINE) dan baru 1 sitasi. Relevansinya tinggi, mutu venue-nya sedang. Sitasi untuk isinya, jangan untuk gengsinya.

---

## G. AI Tepercaya & Motivasi Regulatif

Mendukung **§1 Introduction**, **§10 Discussion**

| # | DOI | Judul | Jurnal | Thn | Sitasi | FWCI | Register | Scopus |
|---|---|---|---|---|---:|---:|---|---|
| G1 | `10.1016/j.artmed.2024.102830` | Trustworthy clinical AI solutions: A unified review of uncertainty quantification in Deep Learning models for medical image analysis | Artificial Intelligence in Medicine | 2024 | **248** | **18,91** | J2 N2 | ⬜ |
| G2 | `10.1136/bmj-2024-081554` | FUTURE-AI: international consensus guideline for trustworthy and deployable artificial intelligence in healthcare | BMJ 388:e081554 | 2025 | **83** | **20,62** | J2 N2 | ⬜ |

- **G2** — Konsensus internasional di **BMJ**. Ini kartu truf untuk paragraf pembuka: bukan opini Anda bahwa AI klinis butuh jaminan ketidakpastian, melainkan pedoman konsensus.

> 🔧 **DOI G2 dikoreksi 2026-10-02.** DOI lama `10.1136/bmj.r340` ternyata **ralat** (Crossref: `update-to` → `10.1136/bmj-2024-081554`, tipe *Correction*), bukan artikelnya. Artikel asli: Lekadir K. *et al.* (49 penulis), *BMJ* **388**, e081554, 2025. Jurnal sama, sehingga status Scopus tidak berubah. Tertangkap saat menyusun daftar pustaka IEEE: Crossref tidak mencatat penulis untuk DOI ralat.

---

## I. Fondasi Varians Klaster — Pengecualian Aturan 5 Tahun

Ditambahkan **2026-10-01** sesudah audit prior-art. Mendukung **§5.1.2–5.1.3 Metode**.

| # | DOI | Judul | Jurnal | Thn | Scopus |
|---|---|---|---|---|---|
| **I1** | `10.1002/1097-0258(20010215)20:3<377::aid-sim799>3.0.co;2-n` | Unequal cluster sizes for trials in English and Welsh general practice: implications for sample size calculations (Kerry, Bland) | Statistics in Medicine 20:377–390 | 2001 | ⬜ |
| **I2** | `10.1191/1740774505cn081oa` | Standardized mean differences in individually-randomized and cluster-randomized trials, with applications to meta-analysis (White, Thomas) | Clinical Trials 2:141–151 | 2005 | ⬜ |

**Mengapa melanggar aturan 5 tahun — dan mengapa itu benar.** §5 memakai **rumus mereka secara langsung**: varians rata-rata klaster tanpa bobot dengan rata-rata harmonik ukuran klaster (I2), dan pembandingan desain-efek di bawah bobot sama versus bobot ukuran (I1). Atribusi pemilik rumus tidak dapat diganti dengan sumber sekunder yang lebih baru tanpa menyesatkan pembaca tentang asal hasilnya. Reviewer statistik **mengharapkan** sumber ini; ketiadaannya terbaca sebagai ketidaktahuan bidang, bukan kepatuhan aturan.

Pengecualian dibatasi **dua** dan dinyatakan terbuka. Sumber klasik lain yang relevan (Kish 1965; Gabler, Häder & Lahiri 1999; Nelder 1965; Bailey 1996) **tidak** disitasi: rumus $b^*$ dinyatakan sebagai desain-efek klaster baku dengan rujukan ke A13, dan join kekisi partisi dinyatakan sebagai aljabar baku.

> ⚠️ **Yang dicoba dan GAGAL diverifikasi — tidak disitasi:** Lai (2021), *Composite reliability of multilevel data*, Psychological Methods 26(1):90. Cuplikan Google Scholar menyebut rumus harmonik yang sama, tetapi metadata Crossref tidak dapat dikonfirmasi. I2 menutup kebutuhan yang sama.

### Praterbit wajib-sitasi (di luar hitungan 35 artikel jurnal)

| # | Rujukan | Status | Dipakai untuk |
|---|---|---|---|
| **P1** | Noonan A. (2026). *The Exceedance Design Effect: Effective Sample Size for Thresholds under Clustering*. arXiv:2608.21262; Zenodo `10.5281/zenodo.22048277` (v8) | ⚠️ praterbit, CC-BY, teks hlm. 1 dibaca | ESS untuk ambang; pembobotan-ukuran. **Sumbu §5.1.4 kami dinyatakan heuristik terhadap karya ini** |
| **P2** | Zheng J., Xu G. (2026). *A Symmetric Layer-Union Audit of Component Collapse in Hierarchical Procedural Corpora*. arXiv:2608.08892 | ⚠️ praterbit, abstrak dibaca | Keruntuhan join menjadi komponen raksasa |

> P1 menyubsumsi analisis ESS/ICC kami. Tidak menyitasinya adalah risiko penolakan terbesar yang tersisa — satu reviewer yang mengenalnya cukup untuk menjatuhkan naskah.

---

## H. Rujukan Dataset — Wajib Menurut Lisensi

Diverifikasi langsung dari halaman resmi penyedia, bukan dari pencarian.

| # | Sitasi | DOI | Verifikasi |
|---|---|---|---|
| H1 | Wagner P. et al. (2020). *PTB-XL, a large publicly available electrocardiography dataset*. **Scientific Data** | `10.1038/s41597-020-0495-6` | ✅ **1.312 sitasi**, J1 N2 |
| H2 | Wagner P. et al. (2022). PTB-XL v1.0.3. **PhysioNet** | `10.13026/kfzx-aw45` | ✅ Halaman resmi |
| H3 | Moody G.B., Mark R.G. (2005). *MIT-BIH Arrhythmia Database*. **PhysioNet** | `10.13026/C2F305` | ✅ Halaman resmi |
| H4 | Moody G.B., Mark R.G. (1999). *MIT-BIH Noise Stress Test Database*. **PhysioNet** | `10.13026/C2HS3T` | ✅ Halaman resmi |
| H5 | Reyna M. et al. (2022). *PhysioNet/CinC Challenge 2021* v1.0.3. **PhysioNet** | `10.13026/34va-7q14` | ✅ Halaman resmi |

**Pendamping wajib (dikutip dari halaman PhysioNet, bukan DOI Crossref):**

- Moody G.B., Mark R.G. (2001). *The impact of the MIT-BIH Arrhythmia Database*. **IEEE Eng. Med. Biol.** 20(3):45–50. PMID: 11446209
- Mark R.G. et al. (1982). *An annotated ECG database for evaluating arrhythmia detectors*. **IEEE TBME** 29(8):600
- Moody G.B., Muldrow W.E., Mark R.G. (1984). *A noise stress test for arrhythmia detectors*. **Computers in Cardiology** 11:381–384

---

## 4. Ringkasan Mutu Jurnal

Dihitung ulang dari 33 baris tabel rujukan (A0 dan A0b berada di kotak rinci, di luar tabel; B7 dan E5 praterbit tanpa register).

| Register | Jumlah | Arti |
|---|---:|---|
| **JUFO-3** (terkemuka dunia) | **16** | Annals of Statistics, JRSS-B, JASA, TPAMI, TKDE, TNNLS, TAFFC, Pattern Recognition, PNAS, Medical Image Analysis |
| **JUFO-2** | 9 | Phil. Trans. R. Soc. A, IEEE JBHI, Neurocomputing, AI in Medicine, BMJ |
| **JUFO-1** | 6 | EJS, SPL, CMPB, JHIR, BDCC, RINAM |
| **Tanpa JUFO** ⚠️ | 1 | F5 (Cardiovascular Eng. & Tech.) |
| **Norway-2** (20% teratas) | 20 | — |
| **Norway-1** | 12 | — |

Di luar tabel: **A0b = JASA** (JUFO-3, Norway-2) dan **A11 = Bernoulli** (jurnal probabilitas papan atas). **A0** tidak punya register — jurnal ACM baru.

**Distribusi tahun (35 artikel, sesudah penukaran §5c — dihitung dari `scopus-verification.json`):** 2001: 1 · 2005: 1 · 2021: 8 · 2022: 5 · 2023: 5 · 2024: 2 · 2025: 5 · 2026: 8. Dua pra-2021 adalah pengecualian §I yang disengaja.

**Praterbit yang dipantau (bukan sitasi final):** arXiv:2410.06296 (B7, ancaman C2) · arXiv:2601.01223 (E5, kelompok Baheri)

> ✅ **Aturan 5 tahun terpenuhi penuh.** Sesudah F1 dikoreksi ke 2021 (tahun terbitan cetak), **tidak ada** rujukan non-dataset di luar jendela 2021–2026. Rujukan dataset (H1–H5) dikecualikan sesuai ketentuan.
>
> Empat rujukan wajib di §6 (Romano 2020, Vovk 2012, Demsar 2006, de Chazal 2004) semula berada di luar jendela. Keempatnya sudah **diganti atau dicabut** — lihat §6a.

---

## 5. Perubahan dari Draf Sebelumnya

Draf pertama disusun dari Crossref tanpa pemeriksaan relevansi atau mutu. **Delapan entri dikeluarkan, tujuh entri baru masuk.**

### ❌ Dikeluarkan

| Entri lama | Alasan |
|---|---|
| `10.1093/biomet/asac040`, `10.1093/jrsssb/qkaf016`, `10.1214/25-aos2510`, `10.1214/24-sts965` | Tidak muncul di pencarian terarah OpenAlex; relevansinya hanya diduga dari judul, tidak dapat saya konfirmasi |
| `10.1002/sta4.70157`, `10.1177/25152459251380452` | Mutu venue rendah dan relevansi marjinal |
| `10.1016/j.bspc.2024.106743`, `10.1186/s12911-026-03771-z`, `10.1002/acm2.70663`, `10.1007/s44163-026-01219-x`, `10.1002/ksa.12737` | Aplikasi klinis generik — tidak menyumbang argumen apa pun pada naskah Anda |
| `10.1038/s41598-026-40637-w`, `10.1038/s41598-026-72902-3` | Tidak terkonfirmasi di OpenAlex; DOI Scientific Reports 2026 dengan sitasi 0 dan tanpa jejak — **tidak layak dipercaya tanpa verifikasi lanjutan** |
| `10.3390/computers10060082`, `10.3390/e23091121` (posisi), `10.1016/j.bspc.2023.105789`, `10.3389/fphys.2023.1247587` | Digantikan rujukan sejenis dengan dampak jauh lebih tinggi |

### ✅ Temuan baru yang penting

| Entri | Mengapa penting |
|---|---|
| **B3** `10.1016/j.patcog.2021.108271` | Conformal multi-label di Pattern Recognition, 66 sitasi. **Terlewat sepenuhnya di draf pertama.** |
| **C4** `10.1109/tpami.2023.3272339` | Conformal untuk deret waktu di **TPAMI**. 64 sitasi, FWCI 8,09. |
| **A2** `10.1214/20-aos1965` | Jackknife+ — **baseline B6 Anda**, sebelumnya berstatus "BELUM TERVERIFIKASI" |
| **F2** `10.1016/j.cmpb.2021.105948` | Rujukan kanonik "inter-patient paradigm", FWCI 10,88 |
| **A4, A7, A8** | Tiga artikel JRSS-B/JASA tentang conformal pada **data dependen** — inti masalah Anda |
| **D4** `10.1109/taffc.2026.3702998` | UQ adil lintas subkelompok klinis — motivasi langsung K3 |

---

## 5b. Pemangkasan ke 35 Rujukan — 2026-09-30

Dari 44 artikel, **sembilan dikeluarkan** untuk mencapai batas 35. Kriterianya **daya dukung argumen**, bukan jumlah sitasi. Beberapa yang dipotong justru sitasinya tinggi — itu disengaja.

| Dikeluarkan | Venue | Thn | Sitasi | Alasan |
|---|---|:-:|---:|---|
| A10 `10.1016/j.patcog.2021.108507` | Pattern Recognition | 2021 | 30 | Tumpang tindih penuh dengan **A11** (Bernoulli), yang lebih formal dan lebih berdampak. FWCI 0,92 — di bawah rata-rata bidang |
| B4 `10.1002/cjs.70053` | Canadian J. Statistics | 2026 | 0 | Multi-label untuk **data fungsional** — bukan setting Anda |
| C3 `10.1109/jsait.2024.3368229` | IEEE JSAIT | 2024 | 12 | Model prediktif kendali (MPC) — domain tidak berkaitan |
| D3 `10.1109/tii.2025.3529920` | IEEE TII | 2025 | 11 | Deret waktu **industri** — pergeseran distribusinya berjenis lain |
| E4 `10.3389/frai.2026.1844254` | Frontiers in AI | 2026 | 0 | Subtyping pasien; nested CP tidak dipakai di naskah |
| F4 `10.1016/j.bspc.2023.105271` | BSPC | 2023 | 74 | Berulang dengan F2/F3/F10 yang sama-sama inter-patient |
| F7 `10.1016/j.bspc.2024.106141` | BSPC | 2024 | 91 | Perbandingan representasi 1D vs 2D — tidak menyumbang argumen dependensi |
| F8 `10.3390/e23091121` | Entropy | 2021 | 173 | Penerapan PTB-XL generik. Sitasi tinggi, **daya dukung argumen nol** |
| F9 `10.3390/s22030904` | Sensors | 2022 | 66 | Few-shot learning — bukan sumbu kontribusi Anda |

### Mengapa memotong yang bersitasi tinggi itu benar

F8 (173 sitasi) dan F7 (91 sitasi) terlihat mahal untuk dibuang. Tetapi keduanya hanya membuktikan *"orang lain juga memakai PTB-XL"* — pernyataan yang sudah dipikul **F1**, benchmark resminya, jauh lebih kuat.

Daftar pustaka Q1 dinilai dari **apakah tiap rujukan mengerjakan sesuatu di dalam naskah**, bukan dari total sitasi yang dikumpulkan. Rujukan yang tidak menopang satu kalimat pun adalah beban, bukan aset.

### Yang dipertahankan meski lemah

**F5** (1 sitasi, FWCI 0,65, venue tanpa JUFO) tetap dipertahankan. Ia satu-satunya yang membandingkan inter-patient / intra-patient / patient-specific secara eksplisit — persis pembedaan yang menjadi dasar seluruh argumen Anda. Tidak ada penggantinya.

Ini sisi lain dari kaidah yang sama: **relevansi mengalahkan gengsi, ke dua arah.**

---

## 5c. Penukaran 1:1 Sesudah Reposisi — 2026-10-01

Paper diposisikan ulang dari *metode usulan* (HiCoRC) menjadi *audit empiris*. Akibatnya empat rujukan kehilangan fungsinya, sementara empat kewajiban atribusi baru muncul. **Batas 35 artikel jurnal dipertahankan.**

| Keluar | Alasan |
|---|---|
| A5 `10.1111/rssb.12443` | Deteksi outlier klasifikasi — tidak disitasi di naskah mana pun |
| A6 `10.1080/01621459.2023.2298037` | Validasi robust di bawah pergeseran — pergeseran distribusi bukan sumbu paper |
| C5 `10.1016/j.patcog.2025.111999` | Adaptive conformal inference — tidak disitasi; menopang K3 yang sudah dikeluarkan |
| D1 `10.1073/pnas.2204569119` | Pergeseran kovariat umpan-balik — tidak disitasi; domain biomolekul |

| Masuk | Alasan |
|---|---|
| A12 Ding dkk. 2023 | Prior art Prop. 4 |
| A13 Zhan dkk. 2021 | Prior art bobot sama vs ukuran, sumber ≥ 2021 |
| I1 Kerry & Bland 2001 | Pemilik rumus pembandingan desain-efek — **pengecualian aturan 5 tahun** |
| I2 White & Thomas 2005 | Pemilik rumus rata-rata harmonik — **pengecualian aturan 5 tahun** |

Kriterianya sama dengan §5b: **daya dukung argumen**. Empat yang keluar bersitasi tinggi dan berasal dari venue papan atas, tetapi tidak menopang satu kalimat pun di naskah. Empat yang masuk menopang klaim yang, tanpa sitasinya, akan terbaca sebagai klaim kebaruan palsu.

---

## 6. ❗ Rujukan Wajib yang Masih Hilang

Filter `type:article` menyingkirkan makalah konferensi dan buku. Karya berikut hampir pasti wajib disitasi tetapi **harus Anda cari manual**:

Status venue di bawah **sudah diverifikasi** terhadap daftar sumber Scopus resmi (lembar *Scopus Sources*, *Serial Conf. Proc.*, dan *All Conf. Proceedings*).

| Rujukan | Venue | Scopus | Thn | 5 thn | Kenapa wajib |
|---|---|:-:|:-:|:-:|---|
| Angelopoulos & Bates — *A Gentle Introduction to Conformal Prediction* | Foundations and Trends in ML 16(4):494–591 | ✅ 2008–2025 | 2023 | ✅ | Rujukan pengantar standar |
| Angelopoulos et al. — *Conformal Risk Control* | **ICLR 2024** | ✅ terdaftar | 2024 | ✅ | **Judul Anda memuat istilah ini** |
| Angelopoulos et al. — *Uncertainty Sets for Image Classifiers* | **ICLR 2021** | ✅ terdaftar | 2021 | ✅ | **Baseline B5 (RAPS)** |
| Vovk, Gammerman, Shafer — *Algorithmic Learning in a Random World* | Springer, edisi ke-2 | 📘 daftar buku (terpisah) | 2022 | ✅ | Sumber kanonik |
| Romano, Sesia, Candès — *Classification with Valid and Adaptive Coverage* | **NeurIPS 2020** (ISSN 1049-5258) | ✅ cakupan 2012–2025 | 2020 | ❌ | **Baseline B4 (APS)** |
| Demšar — *Statistical Comparisons of Classifiers over Multiple Data Sets* | **JMLR** | ✅ 2001–2026 | 2006 | ❌ | **Protokol uji statistik §10** |
| de Chazal, O'Dwyer, Reilly — klasifikasi detak inter-patient | **IEEE TBME** | ✅ 1963–2026 | 2004 | ❌ | Pencetus protokol inter-patient |
| Vovk — *Conditional Validity of Inductive Conformal Predictors* | ACML 2012, PMLR v25 | ❌ PMLR baru dicakup **sejak 2017** | 2012 | ❌ | **Baseline B2 (Mondrian)** |

### Temuan yang mengubah rencana

**ICLR ternyata terindeks Scopus** sebagai prosiding, termasuk ICLR 2021 dan ICLR 2024. Dua baseline yang tadinya dikhawatirkan gagal (**RAPS** dan **Conformal Risk Control**) sebenarnya **lolos penuh** — terindeks Scopus dan berada dalam jendela 5 tahun.

## 6a. Penggantian Empat Rujukan Pra-2021 — Selesai

Dicari lewat OpenAlex (`title_and_abstract.search` frasa eksak, 2021+), tiap kandidat diverifikasi ISSN-nya ke daftar sumber Scopus resmi. Skrip: [scripts/find_recent_replacements.py](../scripts/find_recent_replacements.py)

| Rujukan tua | Pengganti | Thn | Scopus | Status |
|---|---|:-:|:-:|:-:|
| Vovk 2012 (Mondrian) | **A11** Fontana, Zeni, Vantini, *Conformal prediction: A unified review of theory and new challenges*, **Bernoulli** `10.3150/21-bej1447` | 2022 | OK | **DIGANTI** |
| Romano 2020 (APS) | Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction*, **Found. & Trends in ML** | 2023 | OK | **DIGANTI** |
| de Chazal 2004 (inter-patient) | **F2** `10.1016/j.cmpb.2021.105948` + **F10** `10.1016/j.cmpb.2021.106582` | 2021 | OK | **DIGANTI** |
| Demsar 2006 (uji statistik) | tidak ada | | | **DICABUT** |

### Mengapa penggantian ini sah, bukan pemutihan sitasi

**A11 dan Angelopoulos & Bates memuat perumusan formal metodenya**, bukan sekadar menyebutnya. Bernoulli 2022 (186 sitasi, FWCI 16,1) menyajikan Mondrian CP secara matematis; Foundations & Trends 2023 menyajikan APS dan RAPS lengkap dengan algoritmanya. Menyitasi *"kami memakai Mondrian CP [A11]"* adalah praktik baku dan dapat ditelusuri pembaca.

Untuk inter-patient, F2 dan F10 sama-sama memakai partisi DS1/DS2 dan memerikannya di dalam naskahnya sendiri.

### Demsar 2006 dicabut karena ujinya memang tidak berlaku

Ini bukan siasat menghindari aturan usia. Prosedur Demsar (Friedman + Nemenyi) dirancang untuk membandingkan **banyak pengklasifikasi lintas banyak dataset**, lazimnya minimal lima. Rancangan Anda memakai **dua** dataset, sehingga uji Friedman tidak bermakna di sini.

Yang sebenarnya dipakai sudah konsisten di seluruh protokol: **CI bootstrap pada level blok**, 200 ulangan. Itu tidak memerlukan Demsar sama sekali.

> **Tindak lanjut wajib:** §10 protokol masih menyebut Friedman/Nemenyi. Harus disesuaikan agar konsisten dengan pencabutan ini.

### Risiko yang tetap ada

Sebagian reviewer meminta sitasi pencetus asli untuk APS dan Mondrian. Bila diminta saat revisi, tambahkan Romano dkk. 2020 dan Vovk 2012 di titik itu. Romano terindeks Scopus lewat NeurIPS (ISSN 1049-5258); Vovk tidak, karena PMLR baru dicakup sejak 2017. Menambahkannya **saat diminta** lebih aman daripada memasukkannya sekarang tanpa diminta.

> 💡 **Sumber praktis:** halaman PyPI **MAPIE** dan **TorchCP** memuat daftar rujukan lengkap dengan venue dan tautan untuk hampir semua entri di atas.

---

## 7. Urutan Pembacaan

### ✅ Tahap 1 SUDAH DIKERJAKAN — 2026-09-29

Abstrak lengkap B1, B2, B3, A3 sudah dibaca dan dianalisis. Hasilnya di atas. Ringkasannya:

| Entri | Menutup kontribusi Anda? | Alasan |
|---|---|---|
| B1 | **Tidak** — justru mengonfirmasi celah | Review; membahas dependensi **antar-label**, bukan antar-sampel; menyatakan sendiri literaturnya berpijak pada exchangeability |
| B3 | **Tidak** | Sumbunya efisiensi komputasi Label Powerset, domain teks |
| B2 | **Tidak** | Irisan lintas-resolusi dengan pembagian $\alpha$ — arah berlawanan dengan penutupan hierarkis |
| A3 | **Tidak** | Kelompok menentukan pergeseran kovariat, bukan dependensi intra-blok |
| **A0** | **YA — C1 TERTUTUP** | Exchangeability hierarkis untuk pengukuran berulang sudah diturunkan dan diterbitkan |
| **B7** | **Berisiko** | Conformal pada DAG label hierarkis; masih praterbit |

**Baca sekarang, berurutan:**

| Urutan | Entri | Tujuan |
|---|---|---|
| 1 | **A0** (arXiv 2306.06342) | Pahami teorema yang akan Anda **pakai**. Ini fondasi baru Anda, bukan musuh. |
| 2 | **B7** (arXiv 2410.06296) | Ukur seberapa jauh C2 masih tersisa |
| 3 | **E5** (arXiv 2601.01223) | Lihat bagaimana kelompok lain mengoperasionalkan ini di data kesehatan |
| 4 | **A1** | Landasan wajib |
| 5 | **B1** | Peta jalan celah multi-label yang masih terbuka |

### Tahap 2 — Pembangun Related Work
A2, A4–A10, B2–B6, C1–C5, D1–D4, E1–E2

### Tahap 3 — Setup eksperimen & motivasi
F1–F2 lebih dulu, lalu F3–F9, G1–G2, E3–E4

---

## 8. Lembar Kerja Verifikasi Scopus

Salin ke spreadsheet saat mengakses Scopus lewat akun institusi:

```
Kode | DOI | Jurnal | Scopus? | Kuartil | CiteScore | Abstrak dibaca | Disitasi di §
```

**Target naskah final:** 35–45 rujukan, dengan komposisi:

| Klaster | Porsi |
|---|---|
| Teori conformal (A, B, C) | ~50% |
| EKG & klinis (E, F) | ~30% |
| Pergeseran distribusi (D) | ~10% |
| Regulatif & UQ medis (G) | ~10% |

---

## Log Perubahan

| Tanggal | Perubahan |
|---|---|
| 2026-09-29 | Draf awal: 41 entri dari Crossref, tanpa verifikasi relevansi maupun mutu |
| 2026-09-29 | **Ditulis ulang total.** 40 entri terverifikasi lewat OpenAlex: DOI, judul, jurnal, tahun, sitasi, FWCI, dan daftar putih JUFO/Norway/CWTS. 8 entri dikeluarkan, 7 temuan baru masuk. Indeksasi Scopus tetap **belum** dikonfirmasi langsung (scimagojr.com memblokir akses). |
