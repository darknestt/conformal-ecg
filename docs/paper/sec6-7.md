# §6 Datasets · §7 Experimental Setup

> **v3 — 2026-10-02.** Ditulis ulang dan dipadatkan (1.640 → ±1.150 kata). Semua angka dataset, protokol split, hiperparameter dan Tabel 6.1, 6.2, 7.1 dipertahankan. Paragraf "Cost" yang **tertulis dua kali** di §6.4 kini satu. Versi sebelumnya dan audit adversarial §6: `sec6-7-draft.md` di riwayat git (commit 9098746).

---

## 6. Datasets

We distinguish throughout between what is *documented* for a dataset and what is
*observed* in it; the two diverge most in §6.4.

### 6.1 Selection rationale

The three datasets play logically distinct roles (Table 6.1) and are not meant to
replicate one another.

**Table 6.1.** Roles of the three datasets.

| Dataset | Role | Block identifier |
|---|---|---|
| **PTB-XL** | Primary case: patient-level dependence, multi-label targets, label hierarchy | Documented (`patient_id`) |
| **MIT-BIH** | Strong-dependence end of the design-effect axis | Documented (record = subject) |
| **Challenge 2021** | Case study at the limit of observability | Not documented |

PTB-XL and MIT-BIH sit at opposite corners of the space of block geometries
(Table 6.2). Within any single dataset the number of blocks and the number of
measurements per block are fixed together, so no single dataset, however large,
can separate their effects.

**Table 6.2.** Block geometry of the two primary datasets.

| | PTB-XL | MIT-BIH |
|---|---:|---:|
| Block unit | patient | record (subject) |
| Calibration blocks $K_1$ | 958 | 11 |
| Harmonic mean block size $H$ | 1.05 | 1,355 |
| Design effect | **1.02** | **703.93** |

Only $H$ in this table is a structural property of the data: $K_1$ depends on the
split design (958 is half of the 1,917 patients in our fold-9 evaluation subset),
and the design effect on the model, because $\rho$ is the ICC of conformity scores
from a particular backbone. Challenge 2021 supports no claim of generality; it is
included because a diagnostic that only ever returns "admissible" has not shown
that it can discriminate.

### 6.2 PTB-XL

PTB-XL [H1], [H2] holds 21,799 twelve-lead records from 18,869 patients, released
with full metadata under a permissive licence. We use the 100 Hz version (1,000
samples per 10-second record), band-pass filtered at 0.5–40 Hz.

**Labels.** Diagnostic statements map to five non-exclusive superclasses: NORM
(9,514), MI (5,469), STTC (5,235), CD (4,898) and HYP (2,649). Together they give
27,765 labels on 21,799 records, with 5,144 records carrying more than one
superclass. The 411 records (1.9%) with no diagnostic superclass are excluded
rather than assigned a default class.

**Blocks.** Clustering by patient is mild: 1.155 records per patient on average,
at most 10, and 88.8% of patients contribute a single record. Only 5,041 records
(23.1%) belong to patients with more than one, which places PTB-XL at the
low-dose end of the design-effect axis. The metadata expose three further
grouping variables — 51 recording sites (17 records missing), 12 nurses (1,473
missing) and 11 devices (complete) — and these are crossed rather than nested,
the setting of Corollary 2.2.

**Folds.** We use the published stratified ten-fold split unchanged: 17,418
records in folds 1–8, 2,183 in fold 9 and 2,198 in fold 10, with no patient
crossing a fold boundary. Human validation differs sharply between folds: 67.0%
of records on average in folds 1–8 (range 64–68%), against 100% in folds 9 and 10.
Confirmatory analysis is therefore confined to folds 9–10, and fold 10 is
reserved and has not been examined.

**Demographics.** Age is recorded for every record (median 62; ages above 89 are
encoded as the sentinel 300 in 293 records), and sex as 11,354 male and 10,445
female.

### 6.3 MIT-BIH Arrhythmia Database

The MIT-BIH Arrhythmia Database [H3] contains 48 half-hour two-channel recordings
at 360 Hz with beat-by-beat cardiologist annotations. Following standard practice
we exclude the four paced records (102, 104, 107, 217), leaving 44. Annotations
map to the five AAMI classes and yield 100,733 beats; 40 lie within 128 samples of
a record boundary and cannot give a complete 256-sample (711 ms) window, so they
are dropped rather than zero-padded, leaving 100,693. The class counts are N
90,087, S 2,781, V 7,008, F 802 and Q 15; class Q is degenerate and reported as
such rather than merged away. The MLII lead is selected by name: record 114
stores its channels as `[V5, MLII]`, so selecting by index would silently
substitute another lead without any error.

We adopt the canonical inter-patient partition into DS1 and DS2 (22 records each;
51,000 and 49,693 beats after boundary removal). Records range from 1,517 to
3,361 beats (median 2,257), three orders of magnitude above PTB-XL's block sizes,
which places MIT-BIH at the high-dose end of the axis. Records 201 and 202 come
from the same subject but fall on opposite sides of the partition; we keep the
standard split for comparability and state the leak.

### 6.4 Challenge 2021 — an observability-limited case

**Structure.** The PhysioNet/CinC Challenge 2021 collection [H5] spans seven
non-duplicate source folders containing 66,416 records, from `ningbo` (34,905) to
`st_petersburg_incart` (74); the `ptb-xl` folder (21,837 records) is excluded as a
duplicate of §6.2, and the two totals sum to the official 88,253.

**The patient partition is not documented.** None of the fields in a sample of 42
headers drawn from all seven sources (`#Age`, `#Sex`, `#Dx`, `#Rx`, `#Hx` and, in
five sources, `#Sx`) is documented as a patient identifier; since this is a
sample and the schema varies across sources, we claim no more than that.
Repetition, by contrast, is documented: the INCART source is described as *"74
annotated ECGs ... extracted from 32 Holter monitor recordings,"* and the
excluded `ptb-xl` folder holds 21,837 records from 18,869 patients. There are
thus fewer independent units than records, and an unobservable partition is not
evidence of independence.

**Consequence for feasibility.** The only documented grouping is the source
partition, with $K=7$, so by Proposition 1 any calibration on it has
$\alpha_{\min}\ge 1/8$, or $1/7$ if one source is held out; the bound concerns
the source partition, not the dataset. For the patient partition $K_1$ becomes an
assumption an author must state, and we report no single $\alpha_{\min}$. The
sufficiency condition also presupposes a latent block structure [A0]; if
similarity within an institution decayed continuously, for example with
proximity of acquisition protocol, the condition would be ill-posed rather than
merely unobservable. These checks required about 0.5 MB of downloads (70 index
files and 42 headers) from a 12.6 GB dataset, before any preprocessing or
training.

---

## 7. Experimental Setup

### 7.1 Backbones

Because conformal guarantees are model-agnostic, the backbone affects the size of
prediction sets, not their validity. The primary backbone is a compact 1-D
convolutional network (SmallECGNet) with 104,389 parameters for 12-lead input and
101,925 for single-lead. Every audit is repeated with two 1-D residual networks
from the PTB-XL benchmark family [F1]: ResNet1D-34 (7,225,733 / 7,220,805
parameters) and ResNet1D-50 (15,969,413 / 15,964,485). The residual networks are
trained with Adam (learning rate $10^{-3}$), early stopping on validation loss
with patience 5, and at most 25 (PTB-XL) or 30 (MIT-BIH) epochs; SmallECGNet
weights are reused from the primary study without retraining. The primary
backbone reaches macro-AUROC 0.9016 on PTB-XL and, on MIT-BIH, accuracy 0.8690
with balanced accuracy 0.3748 and macro-F1 0.3144 — weak on minority classes,
which affects set size but not coverage.

### 7.2 Splits

**PTB-XL.** Folds 1–6 train, fold 7 validates, and fold 9 is split at the patient
level into calibration and evaluation, repeated 200–400 times. Fold 8 is unused
because its label quality differs from fold 9's, and fold 10 is reserved for a
single final confirmatory evaluation.

**MIT-BIH.** DS1 without four validation records (124, 205, 215, 230) trains,
those four validate, and DS2 is split 11/11 at the record level into calibration
and evaluation, repeated 200–400 times.

### 7.3 Conformity scores

For multi-class MIT-BIH, $s(x,y)=1-\hat p_y(x)$. For multi-label PTB-XL the
per-label score is $1-\hat\sigma_\ell(x)$, and the record-level score for superset
coverage is the maximum over true labels, which reduces to scalar HCP (§4.3).

### 7.4 Methods compared

We compare split conformal prediction calibrated as if records or beats were
exchangeable (B1) with HCP calibrated at the block level (B12) [A0]. Because the
question is whether a guarantee can be enforced at all, not which hierarchical
construction is most efficient, the constructions of Dunn et al. [A0b] and
non-hierarchical variants such as Mondrian conformal prediction are outside the
comparison.

### 7.5 Statistical analysis

Table 7.1 lists the procedures. Every resampling step operates on blocks —
patients or records — and never on individual records or beats, which would
reproduce the error under study. Friedman–Nemenyi tests are not used: designed
for many classifiers across many datasets, conventionally at least five, they are
uninformative with two.

**Table 7.1.** Statistical procedures.

| Quantity | Procedure |
|---|---|
| Coverage and set size | Mean over 200 random block-level splits; 2.5–97.5% range across splits |
| B1 deficit against the permutation null | Percentile bootstrap (4,000 resamples of split-level coverage), 95% CI; one-sided bootstrap $p$ |
| Multiplicity | Holm–Bonferroni across the three $\alpha$ levels within each backbone |
| Factorial effects | Percentile bootstrap (3,000 resamples of 400 split-level values), 95% CI |
| Monotonicity in dependence | Spearman correlation, $p<0.05$ |
| Sensitivity to checkpoint | Agreement of signs between best-validation and last-epoch weights |

### 7.6 Reproducibility

All experiments run on CPU (2 threads) with fixed seeds; every reported number is
written to a JSON artifact under `results/raw/` with its configuration, and
dataset caches are written atomically so that an interrupted run cannot leave a
partial cache.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Duplikasi dibuang | Paragraf "Cost" dan "Cost of the verdict" (§6.4) identik isinya — kini satu |
| Dipertahankan | Semua angka §6.2–6.3 (21.799 / 18.869 / 27.765 / 5.144 / 411 / 1,155 / 88,8% / 5.041 / 23,1% / 51–17 / 12–1.473 / 11 / 17.418 / 2.183 / 2.198 / 67,0% / 64–68% / 62 / 11.354 / 10.445 / 300 / 293; 48 / 4 / 44 / 100.733 / 40 / 128 / 256 / 711 / 100.693 / kelas / DS1 51.000 / DS2 49.693 / 1.517–3.361 / 2.257) |
| Dipadatkan | §6.1 penjelasan Tabel 6.2; §6.3 subjudul digabung jadi dua paragraf; §7 prosa |
| Audit adversarial lama | Tetap di riwayat git `sec6-7-draft.md`; bukan bagian naskah |
