# §6 Datasets & §7 Experimental Setup — Draft

> **Status:** 🟢 DRAF PROSA · **Dibuat:** 2026-09-30
> Seluruh angka dihitung ulang dari data pada tanggal ini, bukan disalin dari
> dokumen sebelumnya.
>
> ⚠️ **Empat besaran MIT-BIH yang mudah tertukar** dibahas di bagian akhir.

---

## 6. Datasets

Throughout this section we distinguish statements about *what is documented* for
a dataset from statements about *what is observed* in the data. The distinction
matters most where the two diverge (§6.5).

### 6.1 Selection rationale

The three datasets serve **logically distinct roles**; they are not replications
intended to corroborate one another.

| Dataset | Role | Block identifier |
|---|---|---|
| **PTB-XL** | Primary case: patient-level dependence, multi-label targets, label hierarchy | Documented (`patient_id`) |
| **MIT-BIH** | Strong-dependence end of the design-effect axis | Documented (record = subject) |
| **Challenge 2021** | Case study at the limit of observability | Not documented |

The first two datasets occupy opposite corners of the space of block geometries.
A single dataset, however large, cannot separate a theory that depends on the
number of blocks from one that depends on the number of measurements per block,
because the two quantities are fixed within it.

| | PTB-XL | MIT-BIH |
|---|---:|---:|
| Block unit | patient | record (subject) |
| Calibration blocks $K_1$ | 958 | 11 |
| Harmonic mean block size $H$ | 1.05 | 1,355 |
| Design effect | **1.02** | **703.93** |

Two quantities in this table are not properties of the datasets. $K_1$ depends on
the split design: 958 is half of the 1,917 patients in our fold-9 evaluation
subset, and another design would give another value. The design effect
$\mathrm{DEff}=1+(H-1)\rho$ depends on the model, because $\rho$ is the ICC of
conformity scores produced by a particular backbone. Only $H$ is purely
structural. The design effect should therefore not be quoted as a characteristic
of either dataset.

Challenge 2021 is not used to support any claim of generality. Its role is
narrow: to provide a case in which the diagnostic returns a verdict *other than*
"admissible". A diagnostic that has only ever returned "admissible" has not
demonstrated that it discriminates.

### 6.2 PTB-XL

PTB-XL comprises **21,799 twelve-lead records from 18,869 patients**, released
under a permissive licence with full metadata. We use the 100 Hz variant,
yielding 1,000 samples per 10-second record, band-pass filtered at 0.5–40 Hz.

**Label structure.** Diagnostic statements map to five non-exclusive
superclasses: NORM (9,514), MI (5,469), STTC (5,235), CD (4,898), and HYP
(2,649). The 27,765 superclass labels across 21,799 records confirm genuine
multi-label structure, with **5,144 records carrying more than one superclass**.
**411 records (1.9%) carry no diagnostic superclass** and are excluded from
evaluation rather than assigned a default class.

**Block structure.** The dataset is only mildly clustered at the patient level:
mean 1.155 records per patient, maximum 10, with **88.8% of patients contributing
a single record**. In total **5,041 records (23.1%) belong to multi-record
patients**. This mildness is precisely what makes PTB-XL the low-dose end of the
design-effect axis.

**Additional dependence sources.** Beyond patient identity, the metadata exposes
three further grouping variables: **51 recording sites** (17 records missing),
**12 nurses** (1,473 missing), and **11 devices** (complete). These are
*crossed* rather than nested, which is the empirical basis for the impossibility
result of Section 5.2.

**Official folds.** The published stratified 10-fold split is used unchanged:
17,418 records in folds 1–8, 2,183 in fold 9, and 2,198 in fold 10. No patient
crosses a fold boundary. Crucially, **human validation differs sharply between
folds**: 67.0% on average across folds 1–8 (range 64–68%), against **100% on
folds 9 and 10**. All confirmatory analysis is therefore confined to folds 9–10;
**fold 10 is reserved and has not been examined**.

**Demographics.** Age is complete for all records (median 62); sex is recorded
as 11,354 male and 10,445 female. Note that PTB-XL encodes ages above 89 as the
sentinel value **300**, affecting **293 records** — treating this as a numeric
age would corrupt any age-stratified analysis.

### 6.3 MIT-BIH Arrhythmia Database

MIT-BIH contains 48 half-hour two-channel recordings at 360 Hz with
beat-by-beat cardiologist annotations. Following standard practice we **exclude
the four paced records** (102, 104, 107, 217), leaving 44.

**Beat extraction.** Annotations are mapped to the five AAMI classes, yielding
100,733 beats. Of these, **40 lie within 128 samples of a recording boundary**
and cannot yield a complete 256-sample (711 ms) window; they are dropped rather
than zero-padded, leaving **100,693 beats**.

**Channel selection.** The MLII lead is selected **by name rather than by
index**. Record 114 stores its channels in the order `[V5, MLII]`, so index-based
selection silently substitutes a different lead for that record, with no error
raised.

**Class distribution.** N: 90,087 · S: 2,781 · V: 7,008 · F: 802 · **Q: 15**.
Class Q is degenerate and is reported as such throughout rather than being
merged away.

**Inter-patient split.** We adopt the canonical DS1/DS2 partition (22 records
each; 51,000 and 49,693 beats respectively after boundary removal). Across the 44
retained records, sizes range from 1,517 to 3,361 beats with median 2,257 — three
orders of magnitude above PTB-XL's block sizes, which is the property that places
MIT-BIH at the high-dose end of the axis.

> **Known limitation, retained rather than repaired.** Records 201 and 202 belong
> to the same subject and fall on opposite sides of the canonical split. We keep
> the standard partition for comparability with prior work and state the leak
> explicitly.

### 6.4 Noise Stress Test Database

The NSTDB supplies records 118 and 119 corrupted at six signal-to-noise ratios
(−6, 0, 6, 12, 18, 24 dB) together with the three source noise recordings
(baseline wander, electrode motion, muscle artefact). It is used solely for the
coverage-robustness analysis under input degradation, not for calibration.

### 6.5 Challenge 2021 — an observability-limited case

**Structure.** Seven non-duplicate source folders contain 66,416 records:
`ningbo` 34,905; `georgia` 10,344; `chapman_shaoxing` 10,247; `cpsc_2018` 6,877;
`cpsc_2018_extra` 3,453; `ptb` 516; `st_petersburg_incart` 74. The `ptb-xl`
folder (21,837 records) is excluded as a duplicate of §6.2; the two totals sum to
the official 88,253.

**Header fields.** In a sample of 42 headers drawn from all seven sources, the
fields present were `#Age`, `#Sex`, `#Dx`, `#Rx`, `#Hx`, and, in five of the seven
sources, `#Sx`. No field documented as a patient identifier was found. This is a
sample, not a census, and the header schema is demonstrably not uniform across
sources; we therefore claim only that no documented patient identifier appears in
a sample spanning every source.

**Observability.** The patient partition is not observable from the documented
metadata: no substantive variable is documented to determine patient membership.
This is a statement about documentation, not a theorem; without patient labels it
cannot be checked whether the patient partition factors through the available
variables.

**Repetition is documented while its identifier is not.** The official
documentation describes the INCART source as *"74 annotated ECGs ... extracted
from 32 Holter monitor recordings."* Multiple records may therefore originate
from the same monitoring episode, while the corresponding grouping identifier is
not distributed. What is documented is the monitoring episode, not patient
identity. The same holds for the excluded `ptb-xl` folder, whose 21,837 records
derive from 18,869 patients in the original release. This closes the most
dangerous reading of an unobservable partition — that there is no dependence to
worry about. The documentation itself shows that the number of records exceeds
the number of independent units, while the identifier needed to form blocks is
absent.

**Age censoring.** Censoring conventions for age differ across sources: CPSC
encodes ages above 89 as 92, and PTB-XL uses 300. Sentinel values are never
treated as literal ages. We define $\texttt{age\_censored}=\mathbb{1}\{\texttt{age}>89\}$
and use age only where $\texttt{age}\le 89$, with censored records forming a
separate category. Averaging 92 and 300 as numbers would corrupt any age-based
stratification.

**Feasibility on the source partition.** The source partition has $K=7$. Since
$K_1\le K$ for any calibration split, Proposition 1 gives

$$\alpha_{\min}^{\text{source}} \;=\; \frac{1}{K_1+1} \;\ge\; \frac{1}{8} = 0.125 .$$

If at least one source must be held out for testing, $K_1\le 6$ and the bound
tightens to $\alpha\ge 1/7\approx 0.143$. We report the looser bound because it
holds for every design. The bound concerns the **source partition**, not the
dataset: it does not imply that no finer observable partition is admissible.

**Consequence of unobservability.** If the dependence partition $\mathcal{P}$ is
not observable, a guarantee that holds without knowing $\mathcal{P}$ requires a
calibration partition coarser than the join of every admissible candidate. If the
candidate class were unrestricted it would include the single-block partition,
yielding $\alpha\ge 1/2$; for this dataset that is absurd on domain grounds — it
would posit one patient contributing 66,416 ECGs across seven institutions — and
we do not apply it. The correct consequence is that $K_1$ for the patient
partition ceases to be a computable quantity and becomes an **assumption** about
the candidate class, which an author must state. We therefore report no single
$\alpha_{\min}$ for Challenge 2021.

**A modelling prerequisite.** The sufficiency condition of §5.2 is defined only
under hierarchical exchangeability [A0], i.e. when dependence is generated by a
latent block structure. If dependence within an institution were continuous —
for instance, similarity decaying with proximity of acquisition protocol — no
partition $\mathcal{P}$ would exist, and sufficiency would be not merely
unobservable but ill-posed. The uncertainty is therefore layered: $\mathcal{P}$
is unknown, and so is whether a model positing $\mathcal{P}$ applies.

**What we do not claim.** We do not claim that Challenge 2021 cannot be used for
conformal prediction, nor that its records are independent, nor that its
$\alpha_{\min}$ is 0.125 (that bound applies to the source partition only), nor
that $\alpha\ge 1/2$ applies, nor that none of the 66,416 records carries a
patient identifier (42 headers were inspected).

**Cost of the verdict.** All checks above required roughly 0.5 MB of downloads
(70 index files and 42 headers) against a 12.6 GB dataset, and were completed
before any preprocessing or model training.

---

## 7. Experimental Setup

### 7.1 Backbone

Conformal guarantees are model-agnostic; the backbone affects the **size** of
prediction sets, not their validity. We therefore use a deliberately compact
1-D convolutional network — **104,389 parameters** for the 12-lead configuration
and **101,925** for single-lead — rather than a state-of-the-art architecture.
This keeps the experiments reproducible on commodity hardware (CPU-only, 2
threads) and makes clear that the reported coverage behaviour is a property of
the calibration procedure rather than of a particular model.

Reported discriminative performance is macro-AUROC **0.9016** on PTB-XL and
accuracy **0.8690** (balanced accuracy 0.3748, macro-F1 0.3144) on MIT-BIH. The
MIT-BIH figures are weak on minority classes, and we state plainly that this
affects set size and not coverage.

### 7.2 Splits

**PTB-XL.** Folds 1–6 for training, fold 7 for validation, **fold 9 for
calibration and evaluation**, split at the patient level and repeated 200–400
times. Folds 8 and 10 are untouched: fold 8 because its label quality differs
from fold 9, and fold 10 because it is reserved for a single final confirmatory
evaluation.

**MIT-BIH.** DS1 minus four validation records (124, 205, 215, 230) for
training; those four for validation; **DS2 split 11/11 at the record level** for
calibration and evaluation, repeated 200–400 times.

> All resampling is performed **at the block level**. Resampling individual
> records or beats would reproduce exactly the error this paper analyses.

### 7.3 Conformity scores

For multi-class MIT-BIH we use $s(x,y) = 1-\hat p_y(x)$. For multi-label PTB-XL
the per-label score is $1-\hat\sigma_\ell(x)$, and the record-level score for
superset coverage is the maximum over true labels — the construction that, as
noted in §5.3.1, reduces exactly to scalar HCP.

### 7.4 Baselines

Split conformal (B1) and hierarchical conformal prediction (B12) are the primary
comparison. The four constructions of Dunn et al. are implemented as secondary
baselines: pooling CDFs (B13), subsampling once (B14), double conformal (B15),
and repeated subsampling. Mondrian (B2), APS (B4), RAPS (B5) and jackknife+ (B6)
provide non-hierarchical reference points.

### 7.5 Statistical analysis

| Quantity | Procedure |
|---|---|
| Coverage against nominal | Exact binomial, Clopper–Pearson interval |
| Difference between methods | Paired permutation test, block-level |
| All confidence intervals | Bootstrap, **resampled at block level** |
| Monotonicity across design effects | Spearman correlation |
| Multiplicity | Holm–Bonferroni within each hypothesis family |

**Friedman and Nemenyi tests are not used.** The Demšar procedure is designed for
comparing many classifiers across many datasets — conventionally at least five.
With two datasets it is uninformative, and reporting a critical-difference
diagram would be misleading.

### 7.6 Reproducibility

All experiments run on CPU (2 threads). Every reported figure is written to a
JSON artefact under `results/raw/` recording the configuration that produced it.
Random seeds are fixed and stated. Dataset caches are written atomically — to a
temporary file followed by an atomic rename — so that an interrupted run cannot
leave a partially written cache that a later run would silently treat as valid.

---

## Audit adversarial §6 — upaya membangun kontra-contoh

> Dikerjakan 2026-09-30 setelah §6 ditulis. Tiap proposisi dan korolari yang
> dipakai diserang dengan upaya membangun kontra-contoh. Serangan yang **gagal**
> dicatat karena menunjukkan pernyataannya tahan; serangan yang **berhasil**
> dicatat sebagai kerentanan yang bertahan.

### Serangan yang gagal — pernyataannya tahan

**Prop. 1 pada kasus batas dan kasus seri.** Dicoba: bila banyak skor bernilai
sama, CDF empiris melompat, mungkinkah ambang jatuh ke $+\infty$ meski
$\alpha = 1/(K_1+1)$? Tidak. Pada titik itu massa berhingga tepat
$K_1/(K_1+1) = 1-\alpha$, dan karena $Q_\beta = \inf\{t: F(t)\ge\beta\}$, level
$1-\alpha$ tercapai di skor berhingga maksimum. Seri tidak mengubahnya.

**$K_1 \le K$.** Dicoba mencari kasus $K_1 > K$. Blok kalibrasi adalah
himpunan bagian blok; mustahil.

**Prop. 3 (join).** Dicoba: adakah $\mathcal{Q}$ yang lebih kasar daripada setiap
$\mathcal{P}_i$ tetapi lebih halus daripada join-nya? Tidak — join adalah batas
atas terkecil pada kekisi, jadi $\mathcal{Q} \succeq \mathcal{P}_i\ \forall i$
mengimplikasikan $\mathcal{Q} \succeq \bigvee \mathcal{P}_i$ menurut definisi.

**Kor. 3.2 pada PTB-XL — apakah enumerasinya lengkap?** Dicoba: kekisi partisi
yang dibangkitkan empat sumber memuat lebih dari 15 elemen; mungkinkah ada
$\mathcal{Q}$ pemenuh S2 di luar daftar join-himpunan-bagian? Tidak. Setiap
$\mathcal{Q}$ yang memenuhi S2 bagi keempat sumber wajib $\succeq$ join keempatnya,
dan join itu sudah $K_1=1$; setiap yang lebih kasar juga $K_1=1$. Ketidakmungkinan
karena itu ekshaustif **bagi klaim "mengendalikan keempat sumber"**.

**Kor. 0′.1.** Dicoba: bila $\mathcal{P}_\top \in \mathfrak{P}$, mungkinkah
join-nya bukan $\mathcal{P}_\top$? Tidak — join keluarga yang memuat elemen
teratas adalah elemen teratas itu.

### 🔴 Kerentanan yang bertahan

**V1 — TERSELESAIKAN oleh dokumentasi primer; bukan lagi blocker.** *(Diaudit ulang 2026-09-30.)*

Kerentanan semula: struktur subfolder (`g1/`…`g35/`) juga teramati; bila dipakai
sebagai blok maka $K = 70$ dan vonis S1 berbalik. Argumen penolakan kami semula
hanya **induktif** — ukuran tepat 1.000 menunjukkan pemenggalan, tetapi tidak
membuktikan ketiadaan makna sampling. Keduanya memang hal berbeda.

**Dokumentasi resmi menyelesaikannya.** Halaman dataset PhysioNet menyatakan:

> *"Under each dataset folder the files are grouped into subfolders with up to
> 1000 records per subfolder. These subfolders are named as `g#` where the #
> starts at 1. Once 1000 records are allocated to a folder a new folder is
> started with the # incremented by one."*

Alokasinya **berurutan dan berbasis hitungan**, dinyatakan penulis dataset
sendiri. Tidak ada semantik akuisisi, situs, batch, maupun pasien. Hipotesis
"subfolder adalah kelompok bermakna" karena itu **tertutup oleh sumber primer**,
bukan oleh inferensi kami.

#### Analisis sensitivitas — dilaporkan penuh, bukan dipilih

| Pilihan partisi | $K$ | $\alpha_{\min} \ge$ | $\alpha{=}0{,}05$ | $\alpha{=}0{,}10$ |
|---|---:|---:|:-:|:-:|
| Sumber (7 folder) | 7 | **0,1250** | ❌ | ❌ |
| Subfolder (`g*`) | 70 | **0,0141** | ✅ | ✅ |

Selisihnya menentukan: pada $\alpha = 0{,}05$ kedua pilihan memberi **vonis
berlawanan**.

> ⚠️ **Pengakuan yang wajib ditulis.** Pilihan $K=7$ adalah pilihan yang
> **mendukung narasi kami** (Challenge 2021 sebagai kasus keterbatasan). Justru
> karena itu kami mencari dokumentasi primer alih-alih bersandar pada inferensi
> ukuran folder. Yang memutuskan adalah keterangan penulis dataset, bukan
> kenyamanan kesimpulan. Analisis sensitivitas di atas dilaporkan penuh agar
> pembaca dapat menilai sendiri.

#### Mengapa partisi sumber dipilih sebagai partisi analisis utama

Pilihan ini dibuat atas **kriteria substantif**, bukan atas hasil yang
dihasilkannya:

> Partisi sumber dipakai sebagai partisi analisis utama karena ia berpadanan
> dengan **struktur provenans yang terdokumentasi** — tujuh basis data dari
> institusi dan negara berbeda, masing-masing dengan protokol akuisisi dan
> populasi sendiri. Sebaliknya, subfolder `g#` **secara eksplisit dideskripsikan
> dokumentasi sebagai satuan alokasi berkas** berisi sampai 1.000 rekaman.

Memakai `g#` sebagai blok statistik menuntut **asumsi tambahan** — bahwa batas
alokasi berkas menghormati struktur dependensi — dan asumsi itu **tidak disokong
dokumentasi dataset**. Kami karena itu tidak memperlakukannya sebagai blok
dependensi substantif, sambil tetap melaporkan sensitivitasnya.

#### 🔧 Klaim yang DITARIK

Versi sebelumnya dokumen ini menyatakan bahwa karena penggalan berukuran tetap
1.000 sedangkan kelompok klinis tidak berukuran kelipatan 1.000, penggalan
**pasti memotong** kelompok mana pun.

**Klaim itu salah.** Kontra-contohnya sederhana: bila klaster $A$ menempati
rekaman 1–1.000 dan klaster $B$ menempati 1.001–2.000, maka `g1` $= A$ persis dan
`g2` $= B$ persis. Tidak ada yang terpotong. Tanpa mengetahui **urutan** rekaman,
pemotongan tidak dapat disimpulkan.

Yang benar dinyatakan: **hubungan antara `g#` dan struktur dependensi sejati
tidak dapat ditentukan**, karena urutan alokasi tidak terdokumentasi dan struktur
dependensinya sendiri tak teramati. Ini bentuk ketakteramatan yang sama dengan S0,
satu tingkat lebih dalam.

> Perhatikan bahwa untuk dua sumber terkecil, pembedaannya tidak berlaku: INCART
> (74 rekaman) dan `ptb` (516 rekaman) masing-masing muat dalam **satu** subfolder,
> sehingga partisi `g#` dan partisi sumber berimpit di sana. Selisih $K{=}7$
> versus $K{=}70$ sepenuhnya berasal dari lima sumber besar.

**V2 — Klaim "tidak ada pengenal pasien" bersandar pada sampel 42/66.416.**

Skema header terbukti **tidak seragam** (`ptb` dan `georgia` tanpa `#Sx`),
sehingga keseragaman tidak dapat diandaikan dan ekstrapolasi dari sampel
melemah. Sensus penuh memerlukan 66.416 permintaan; PhysioNet memutus koneksi
pada permintaan beruntun. Klaim karena itu tetap **[Dok] berbasis sampel**.

**V3 — $K_1$ menuntut blok kalibrasi TAK KOSONG.**

Prop. 1 memakai bobot $1/\big((K_1+1)N_k\big)$, yang tak terdefinisi bila
$N_k = 0$. Variabel pengelompokan dengan level kosong akan menggelembungkan
$K_1$ bila dihitung naif. Skrip kami mencacah nilai yang **hadir** sehingga aman,
tetapi pernyataan Prop. 1 di naskah harus menyebut syarat ini secara eksplisit.

**V4 — Prop. 0′ tidak menyatakan $\mathfrak{P} \ne \emptyset$.**

Bila kelas admissible kosong, pernyataannya hampa. Syarat sepele, tetapi harus
tertulis.

**V5 — Kriteria seragam atas $\mathfrak{P}$ adalah pilihan, bukan keharusan.**

Prop. 0′ mengadopsi sikap kasus-terburuk. Sikap alternatif — rata-rata terhadap
prior pada $\mathfrak{P}$ — menghasilkan batas berbeda dan mungkin jauh lebih
longgar. Kami menyatakan pilihan ini, tetapi tidak membuktikan ia yang tepat.

**V6 — Pemeriksaan silang 66.416 tidak sepenuhnya independen.**

$66.416 + 21.837 = 88.253$ memakai angka `ptb-xl` dari dokumentasi dataset, yang
tidak kami hitung ulang. Kecocokannya tetap bermakna — hitungan keliru tidak akan
menutup — tetapi ia bukan verifikasi dua jalur penuh.

### Kerentanan yang TIDAK ditemukan meski dicari

Tidak ditemukan cacat pada: penurunan Prop. 1, sifat kekisi Prop. 3, aritmetika
Kor. 0′.1, maupun kelengkapan enumerasi Kor. 3.2 dalam lingkup klaimnya.

> **Tindak lanjut sebelum §8.** V1 harus dinyatakan di naskah sebagai asumsi
> terbuka, bukan didiamkan. V3 dan V4 adalah perbaikan redaksional pada pernyataan
> proposisi. V2, V5, V6 masuk §11 Threats to Validity.

---

### ⚠️ Empat besaran MIT-BIH yang mudah tertukar

Selama penyusunan, empat angka berbeda sempat saya pakai bergantian seolah setara. Ketiganya benar — pada cakupan yang berbeda. Naskah **wajib** konsisten memakai satu definisi dan menyatakannya.

| Besaran | Nilai | Cakupan |
|---|---:|---|
| Seluruh anotasi | **112.647** | 48 rekaman, semua jenis anotasi (termasuk non-detak) |
| Detak terpeta AAMI | **100.733** | 44 rekaman non-berpacu, sebelum pembuangan tepi |
| **Detak yang dipakai** | **100.693** | sesudah 40 detak tepi dibuang — **inilah yang dipakai naskah** |
| N / S / V / F / Q | **90.087 / 2.781 / 7.008 / 802 / 15** | dihitung pada 100.693, bukan 100.733 |

Selisih 40 terurai sebagai 38 N, 1 V, dan 1 F. Distribusi kelas **sebelum** pembuangan (90.125 / 2.781 / 7.009 / 803 / 15) tidak boleh dicampur dengan angka DS1/DS2, sebab split dihitung sesudah pembuangan: **DS1 51.000** dan **DS2 49.693**.

> ✅ Diperiksa: angka pra-pembuangan **tidak pernah masuk** ke dokumen mana pun yang sudah di-commit. README §5 memuat 112.647, yang benar untuk cakupannya sendiri.

### Kolom PTB-XL: 28 atau 33?

Keduanya benar. Berkas `ptbxl_database.csv` memiliki **28 kolom**; `load_metadata()` menambahkan lima kolom indikator superclass sehingga menjadi **33**. Naskah menyebut 28 bila membahas dataset terbitan, dan tidak perlu menyebut 33 sama sekali.

### Angka yang dikutip dan sumbernya

| Angka | Sumber |
|---|---|
| 21.799 / 18.869 / 28 kolom CSV | `load_metadata()`, dihitung 2026-09-30 |
| Superclass 9.514/5.469/5.235/4.898/2.649 | idem |
| 27.765 label; 5.144 multi-label; 411 tanpa superclass | idem |
| 1,155 rerata; 88,8% tunggal; 5.041 (23,1%) | `results/raw/dataset_verification.json` |
| 51 situs (17 kosong), 12 perawat (1.473 kosong), 11 perangkat | `load_metadata()` |
| Fold 17.418 / 2.183 / 2.198 | idem |
| Validasi 67,0% (64–68%) vs 100% | idem |
| Usia = 300 pada 293 rekaman | idem |
| 100.733 → 100.693 (40 tepi) | `src/data/mitdb.py`, verifikasi silang |
| N/S/V/F/Q = 90.087/2.781/7.008/802/15 | `load_beats()` |
| DS1 51.000 / DS2 49.693 | idem |
| Ukuran rekaman 1.517 / 2.257 / 3.361 | idem |
| 104.389 dan 101.925 parameter | `SmallECGNet.n_params()` |
| NSTDB 6 SNR + 3 derau | `data/raw/nstdb` |
| $H$ = 1,05 dan 1.355; DEff 1,02 dan 703,93 | `results/raw/dose_response.json` |

### Yang sengaja TIDAK ditulis

- Tidak ada klaim performa kompetitif untuk backbone — justru dinyatakan lemah
- Tidak ada angka hasil cakupan; itu materi §8
- Tidak ada pembelaan atas kebocoran 201/202; dinyatakan dan dipertahankan apa adanya

### Yang masih menghalangi

| Penghalang | Dampak |
|---|---|
| Backbone final (F2) belum ditetapkan | §7.1 mungkin perlu angka performa baru |
| Daftar baseline B2/B4/B5/B6 belum dijalankan | §7.4 baru menyebut, belum melaporkan |
