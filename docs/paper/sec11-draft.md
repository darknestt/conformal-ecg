# §11 Threats to Validity — Draft

> **Status:** 🟢 DRAF PROSA · **Dibuat:** 2026-09-30
> Mengikuti [`outline.md`](outline.md) §11 dan README §11.
> Seluruh angka diverifikasi terhadap log eksperimen dan `results/raw/*.json`.
>
> **Prinsip penyusunan:** bagian ini bukan formalitas. Empat pembalikan tafsir
> yang terjadi selama penelitian dilaporkan di sini sebagai **kekuatan
> metodologis**, bukan disembunyikan. Reviewer yang menemukannya sendiri akan
> jauh lebih merusak daripada penulis yang menyatakannya lebih dulu.

---

## 11. Threats to Validity

### 11.1 Internal validity

**Label provenance.** PTB-XL diagnostic statements derive from clinical reports
and carry likelihood annotations. Only 64–68% of records in folds 1–8 were
validated by a human cardiologist, against 100% in folds 9 and 10. An early
version of our feasibility study calibrated on fold 8 and evaluated on fold 9,
and reported an apparent 1.43 percentage-point coverage deficit at $\alpha=0.05$.
That deficit was an artefact of **label-quality shift between folds**, not of
block dependence. All confirmatory analyses are therefore restricted to folds 9
and 10, both fully human-validated; fold 10 is reserved and has not been examined.

**Records without a superclass label.** 411 of 21,799 records (1.9%) carry no
diagnostic superclass. These are excluded from evaluation rather than assigned a
default class, which would fabricate labels.

**Channel ordering in MIT-BIH.** Record 114 stores its leads in the order
`[V5, MLII]` rather than the conventional `[MLII, V5]`. Selecting channel 0 by
index — the natural implementation — silently trains on a different lead for that
record, with no error and no trace in any log. Our loader selects by **channel
name**. We report this because the failure mode is invisible to standard checks.

**Boundary beats.** 40 of 100,733 AAMI-mappable beats lie within 128 samples of a
record boundary and cannot yield a complete 256-sample window. They are dropped
rather than zero-padded, leaving 100,693.

**Subject overlap in the canonical MIT-BIH split.** Records 201 and 202 belong to
the same subject and are assigned to DS1 and DS2 respectively by the standard
inter-patient partition. This is a mild train/evaluation leak inherent to the
canonical split. We retain the split for comparability with prior work and state
the leak explicitly rather than silently repairing it.

**Preprocessing leakage.** All transformations are fitted on training data only
and applied within the pipeline.

### 11.2 Construct validity

**Degenerate class.** MIT-BIH class Q contains 15 beats in total across DS1 and
DS2 — 8 in the training split and 7 in DS2, distributed over only 2 records. Any
per-class statistic for Q is uninterpretable. We report per-class $K_1(\ell)$ so
that the reader can see the feasibility boundary directly: $K_1(Q)=2$ gives
$\alpha_{\min}=0.333$, far above any error rate of practical interest.

**Model quality is not a threat to validity, but is a threat to efficiency.**
Conformal guarantees are model-agnostic: a weak model widens $|\hat C|$ without
reducing coverage. Our PTB-XL backbone reaches macro-AUROC 0.9016 against a
published benchmark of approximately 0.93, and our MIT-BIH backbone reaches
accuracy 0.8690 with balanced accuracy 0.3748 and macro-F1 0.3144 — weak on
minority classes. These figures affect the *size* of reported prediction sets and
must not be read as evidence about coverage.

**Subgroup definitions are researcher choices.** Sensitivity to alternative
grouping schemes is examined explicitly.

**Randomised recording dates.** PTB-XL shifts `recording_date` by a random offset
per patient. Absolute dates are therefore meaningless, while *intra-patient
intervals* are preserved because the offset is constant within a patient. All
temporal analysis is restricted to intra-patient intervals; no calendar-based
temporal split is performed.

### 11.3 External validity

**Single institution, dated acquisition.** PTB-XL was collected at one site
between October 1989 and June 1996 on Schiller AG hardware. Device, nurse, and
site metadata are available, which is precisely why the dataset supports the
block-structure analysis; but the resulting estimates of $\rho$ and $H$ should not
be assumed to transfer to modern multi-centre cohorts.

**Two datasets, twelve points, one of them external.** The dose–response curve in
§8 comprises 11 synthetic points generated within MIT-BIH by progressively
randomising block membership, plus a single point from PTB-XL. The combined
Spearman correlation is therefore **driven by the internal MIT-BIH gradient**.
PTB-XL's role is a **prediction check**, not an independent trend: the theory
predicts negligible deficit at $\mathrm{DEff}\approx 1$, and PTB-XL — a different
modality (12-lead against single-lead), a different task (multi-label against
multi-class), and a different block type (patient against record) — lands where
predicted. We claim no more than that.

**Synthetic weakening of dependence.** The MIT-BIH points are produced by
randomly reassigning record labels to a fraction $p$ of beats, not by observing
cohorts with naturally differing $\rho$. The construction preserves the block-size
multiset and the marginal score distribution, and drives ICC from 0.5192 at $p=0$
to 0.0001 at $p=1$; but it is an intervention, not an observation.

**Resampling reuses the same 22 records.** All MIT-BIH confidence intervals derive
from repeated splits of a fixed set of 22 DS2 records. They quantify variability
**across splits**, not across the population of patients. With 22 subjects,
generalisation beyond MIT-BIH is correspondingly limited.

**Domain specificity.** Results are established on ECG. Replication on a
non-medical benchmark would be required before claiming framework generality.

### 11.4 Conclusion validity

**Per-point deficits are not individually significant.** In the dose–response
analysis every per-point confidence interval contains zero. The evidence rests on
the **monotone trend across points**, which is exactly what the pre-registered
Spearman criterion tests. Presenting individual points as significant would
misstate the result.

**Coverage must be read jointly with set size.** At $\alpha=0.10$ on MIT-BIH, HCP
attains 0.9615 coverage against B1's 0.8851 — but at an average set size of 2.43
labels out of 5, against B1's 1.05. Reporting coverage alone would make HCP appear
uniformly superior when much of the gain is abstention.

**A criterion we pre-registered turned out to be near-vacuous.** Our initial test
of H0b asked whether HCP improves coverage over naive split conformal. A
permutation control showed that at $K_1=11$ the $+\infty$ atom mechanically forces
HCP to the $(1-\alpha)(K_1+1)/K_1$ percentile — predicted 0.9818/0.9273/0.8727
against observed 0.9819/0.9273/0.8729. Between 81% and 107% of the apparent
improvement is mechanical and carries no information about dependence. The
criterion is withdrawn; the evidence we report instead is the deficit of naive
split conformal against a matched permuted null.

**A pre-registered criterion that could not be executed as written.** The protocol
specified a Spearman correlation between design effect and coverage deviation
*across datasets*. With two datasets, $\rho_S$ can only take the values $\pm 1$
and no $p$-value is defined. This is a defect in our own pre-registration. We
replaced it with a within-MIT-BIH test over multiple design-effect points, and
record the substitution as a deviation.

### 11.5 Theoretical threats

**Assumption (A) is a modelling choice.** Propositions 2 and 2′ assume a one-way
random-effects model for the score indicator. Proposition 1 and the feasibility
results of §5.2–5.3 are distribution-free and do not depend on it. We keep the two
classes of claim separated throughout.

A further gap deserves explicit treatment. Proposition 2 is stated for the ICC of
the **indicator** $\mathbb{1}\{s\le t\}$, whereas the dose–response analysis is
more conveniently computed on raw scores. We therefore recomputed the entire
curve using the indicator ICC at a fixed threshold. The conclusion is unchanged:
Spearman $+0.90/+0.80/+0.71$, all $p<0.05$, against $+0.84/+0.80/+0.85$ with raw
scores. The value of $\rho$ does shift — PTB-XL falls from 0.3525 to 0.19–0.20 —
but its design effect remains $\approx 1.01$ and its position on the curve does
not move. The prediction survives on the quantity the theory actually specifies.

**Scope of the impossibility result.** *Corollary 3.2 is proved for the HCP/Dunn
family. Whether it holds for every distribution-free method that relies on
exchangeability between blocks remains an open question.* The existence claim
itself is verified exhaustively on the PTB-XL partition lattice: of the fifteen
joins of dependence sources, eight satisfy sufficiency and all eight collapse to
a single block.

**Formal proofs require statistical review.** All derivations in §5 are to be
reviewed by a statistician before submission.

### 11.6 Researcher degrees of freedom

Our interpretation of the MIT-BIH evidence reversed three times before
stabilising. We report the sequence because the alternative — presenting only the
final position — would conceal how the conclusion was reached.

| Stage | Interim conclusion | Overturned by |
|---|---|---|
| 1 | HCP improves on naive split conformal, confirming H0b | Permutation control: 81–107% of the gap is mechanical |
| 2 | The deficit is driven by block-size imbalance | 2×2 factorial: imbalance significant in 0/3 settings, clustering in 3/3 |
| 3 | The deficit increases monotonically with ICC | PTB-XL: $\rho=0.3525$ yet deficit $-0.0012$ |
| 4 | The deficit tracks $\mathrm{DEff}=1+(H-1)\rho$ | — stands |

Every reversal followed the **addition of a control**, not a reinterpretation of
existing data. Stage 2 was an error of ours: it compared results from two analyses
with different calibration sizes (approximately 24,800 beats against 16,500) and
attributed the difference to block balance.

Two deviations require explicit statement. First, **the permutation control was
added post hoc**, after the pre-registered criterion produced a result we
suspected was tautological. It tightened rather than relaxed the analysis: it
invalidated a criterion that had supported our hypothesis. Second, **the reporting
axis was fixed after seeing the data** — we tried ICC first and it failed to
unify the two datasets. We note that $\mathrm{DEff}=1+(H-1)\rho$ was stated as
Proposition 2′ *before* these data were collected, and that the harmonic mean is
derived from $\operatorname{Var}(\hat G)$ rather than chosen; but the decision to
report on that axis was nonetheless made with the results in view.

A complete deviation log is maintained in the accompanying protocol.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Panjang | ~1.200 kata; target 1 halaman jurnal (padat, boleh dipangkas ke tabel bila perlu) |
| §11.6 | **Bagian terpenting.** Empat pembalikan dilaporkan sebagai urutan, bukan disembunyikan |
| Kor. 3.2 | Kalimat ruang lingkup ditulis **verbatim**, sama persis dengan §5 |
| Angka | Seluruhnya terverifikasi dari log sesi; tidak ada yang dibulatkan tanpa sumber |
| Nada | Menyatakan batas tanpa merendahkan hasil; tiap ancaman disertai apa yang sudah dikerjakan |

### Angka yang dikutip dan sumbernya

| Angka | Sumber |
|---|---|
| 64–68% vs 100% tervalidasi | `scripts/check_consistency.py`, metadata PTB-XL |
| 411 (1,9%) tanpa superclass | `scripts/verify_datasets.py` |
| Rekaman 114 = `[V5, MLII]` | `scripts/verify_mitdb.py` |
| 100.733 → 100.693 (40 tepi) | verifikasi silang `src/data/mitdb.py` |
| Q = 15 detak; DS2: 7 detak di 2 rekaman | `experiments/feasibility_mitdb.py` |
| macro-AUROC 0,9016 | `results/raw/feasibility_study.json` |
| akurasi 0,8690 / bal 0,3748 / F1 0,3144 | `results/raw/feasibility_mitdb.json` |
| 0,9818/0,9273/0,8727 vs 0,9819/0,9273/0,8729 | `results/raw/control_permutation_mitdb.json` |
| ICC 0,5192 → 0,0001 | `results/raw/monotonicity_icc_mitdb.json` |
| PTB-XL $\rho{=}0{,}3525$, defisit $-0{,}0012$ | `results/raw/dose_response.json` |
| $|C|$ 2,4339 vs 1,0507 | `results/raw/feasibility_mitdb.json` (`ukuran_B12`, `ukuran_B1`) |
| ~24.800 vs 16.500 | rerata $n$ kalibrasi: separuh dari 49.693 detak DS2, vs $11\times1500$ |

### Yang sengaja TIDAK ditulis

- Tidak ada pembelaan yang melunakkan ancaman ("meskipun demikian, hasil kami tetap...")
- Tidak ada ancaman yang dicantumkan tanpa mitigasi atau pernyataan batas
- Tidak ada klaim bahwa pembalikan tafsir adalah hal biasa — ia dilaporkan sebagai fakta prosedural
