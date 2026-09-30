# §6 Datasets & §7 Experimental Setup — Draft

> **Status:** 🟢 DRAF PROSA · **Dibuat:** 2026-09-30
> Seluruh angka dihitung ulang dari data pada tanggal ini, bukan disalin dari
> dokumen sebelumnya.
>
> ⚠️ **Empat besaran MIT-BIH yang mudah tertukar** dibahas di bagian akhir.

---

## 6. Datasets

### 6.1 Selection rationale

The two datasets are chosen for a reason that is central to the argument rather
than incidental: **they occupy opposite corners of the block-geometry space that
Section 5.1 identifies as decisive.** A single dataset, however large, cannot
distinguish a theory in which the number of blocks matters from one in which the
number of measurements per block matters, because both quantities are fixed.

| | PTB-XL | MIT-BIH |
|---|---:|---:|
| Block unit | patient | record (subject) |
| Calibration blocks $K_1$ | 958 | 11 |
| Harmonic mean block size $H$ | 1.05 | 1,355 |
| Design effect | **1.02** | **703.93** |

The contrast spans roughly three orders of magnitude in design effect while
holding the modality (ECG) and the conformal machinery fixed. A third dataset
was considered and **deliberately excluded**: once the two extremes are covered,
additional datasets add computational cost without addressing a distinct
question.

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

## Catatan penyusunan

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
