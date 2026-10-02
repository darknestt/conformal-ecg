# §10 Threats to Validity — Draft v2

> **Status:** 🟢 DRAF PROSA v2 · **Ditulis ulang:** 2026-10-02 (menggantikan `sec11-draft.md`).
> Dipangkas dari ±2.230 ke ±1.150 kata. Hasil yang sudah ada di §8.5 tidak diulang, hanya dirujuk.

---

## 10. Threats to Validity

### 10.1 Internal validity

**Label provenance.** Only 64–68% of PTB-XL records in folds 1–8 were validated
by a cardiologist, against 100% in folds 9 and 10. An early version of the study
calibrated on fold 8 and evaluated on fold 9 and found an apparent 1.43
percentage-point deficit at $\alpha=0.05$; it was an artefact of label-quality
shift between folds, not of block dependence. All confirmatory analyses therefore
use fold 9, and fold 10 has not been examined.

**Data handling.** Each data-handling decision of §6.2–6.3 guards against a
failure mode that raises no error: the 411 PTB-XL records without a diagnostic
superclass are excluded rather than given a default label; the MIT-BIH lead is
selected by name because record 114 stores its channels in reverse order; beats
too close to a record boundary are dropped rather than zero-padded; and the
subject shared by records 201 and 202 across DS1 and DS2 is retained for
comparability and stated. All preprocessing is fitted on training data only.

### 10.2 Construct validity

**Degenerate class.** MIT-BIH class Q has 15 beats in total, of which 7 lie in
just two evaluation records. Per-class statistics for Q are uninterpretable; we report
$K_1(\mathrm{Q})=2$, i.e. $\alpha_{\min}=1/3$, so that the boundary is visible
rather than averaged away.

**Model quality.** Conformal guarantees are model-agnostic: a weak model widens
prediction sets without reducing coverage. Our primary backbones are below
published PTB-XL benchmarks [F1] and weak on MIT-BIH minority classes (balanced
accuracy 0.37–0.38 for all three backbones). Their discrimination therefore bears
on set size, not on the coverage findings — a reading we tested rather than
assumed, by repeating every audit on two larger residual networks (§8.5).

**Checkpoint selection.** The MIT-BIH validation set holds 4 records, and early
stopping selected epoch 1 for ResNet1D-50. The pre-registered last-epoch
sensitivity analysis (§8.5) preserved the sign of every deficit and every $K_1$,
but not its magnitude, which we therefore do not interpret across backbones.

### 10.3 External validity

**Single institution.** PTB-XL was recorded at one institution between 1989 and
1996. Its device, nurse and site metadata are what make the block analysis
possible, but its estimates of $\rho$ and $H$ need not transfer to contemporary
multi-centre cohorts.

**One gradient, one external point.** Eleven of the twelve points in the
dose–response analysis are synthetic configurations of MIT-BIH obtained by
reassigning beats between records; the twelfth is PTB-XL. The combined
correlation is therefore driven by the internal gradient, which is an
intervention rather than an observation of naturally differing cohorts. PTB-XL
serves as a prediction check — a different modality, task and block type that
lands where the design effect predicts — and we claim no more than that.

**Fixed evaluation subjects.** All MIT-BIH intervals derive from repeated splits
of the same 22 DS2 records. They quantify variability across splits, not across
the population of patients.

**Domain.** All results concern ECG. Other clinical signals with repeated
measurements are plausible candidates for the same analysis but are not
examined.

### 10.4 Statistical conclusion validity

**Per-configuration deficits.** No single split, and no single dose–response
point, establishes a deficit: split-to-split ranges contain $1-\alpha$ in every
MIT-BIH cell (Table 8.3), and every per-point interval in the dose–response
analysis contains zero. The evidence rests on the comparison with a permutation
null and on the monotone trend, which are what the pre-registered tests address.

**Strength across backbones.** After Holm correction the deficit against the
permutation null is significant at every level for two of three backbones and at
none for ResNet1D-34 (Table 8.4). The pre-registered criterion fails for that
backbone, and we claim invariance of direction only.

**Coverage and set size.** Coverage alone overstates HCP: at $\alpha=0.10$ on
MIT-BIH its coverage of 0.9615 is obtained with 2.43 of 5 labels per beat, and
below $\alpha_{\min}$ it covers by abstaining. We report both quantities
throughout.

**Withdrawn and replaced criteria.** Two pre-registered criteria did not survive.
The comparison "HCP covers better than split conformal" was withdrawn because
the permutation control showed it to be largely mechanical (§8.3). A Spearman
test across datasets could not be executed as written, because with two datasets
the rank correlation takes only the values $\pm1$; it was replaced by a test over
design-effect points within MIT-BIH. Both changes are logged as deviations.

### 10.5 Theoretical threats

**Assumption (A).** The variance (6) and design effects (7) assume a one-way
random-effects model with compound symmetry. Proposition 1, Corollary 2.2 and
the label-level condition of §5.3 are distribution-free and do not depend on it.
Expression (6) concerns the correlation of the coverage indicator rather than of
raw scores; recomputing the dose–response analysis with the indicator correlation
leaves every Spearman coefficient significant (Table 8.5). PTB-XL's correlation
falls from 0.35 to 0.19–0.20 under this definition, but its design effect remains
near 1.

**Scope of the impossibility result.** *Corollary 2.2 is proved for the HCP/Dunn
family. Whether it holds for every distribution-free method that relies on
exchangeability between blocks remains an open question.* The collapse of joined
partitions into a giant component is itself known [P2]. On PTB-XL the verdict is
exhaustive only with respect to the declared sources {patient, site, nurse,
device}, which cannot be verified from data. Declaring only {patient, site}
yields $K_1=34$ on the full calibration fold and makes $\alpha=0.05$ feasible,
but 31 of those blocks consist solely of 188 records lacking nurse metadata; on
the 1,960 records with complete metadata the same declaration gives $K_1=3$. We
therefore state the result conditionally: *if patient, site, nurse, and device are
all treated as dependence sources, no admissible calibration grouping exists at
any conventional $\alpha$.*

### 10.6 Researcher degrees of freedom

Our reading of the MIT-BIH evidence changed three times before stabilising
(Table 10.1). Each change followed the addition of a control, not a
reinterpretation of existing data. The second stage was our own error: it
compared analyses with different calibration sizes (about 24,800 against 16,500
beats) and attributed the difference to block balance.

**Table 10.1.** Interim conclusions on MIT-BIH and the control that overturned each.

| Stage | Interim conclusion | Overturned by |
|---|---|---|
| 1 | HCP improves on naive split conformal | Permutation control: 81–107% of the gap is mechanical |
| 2 | The deficit is driven by block-size imbalance | 2×2 factorial: imbalance significant at 0/3 levels, clustering at 3/3 |
| 3 | The deficit increases monotonically with ICC | PTB-XL: ICC 0.35 yet no deficit |
| 4 | The deficit tracks $1+(H-1)\rho$ | — stands |

Three analyses were added or changed after results were seen, and each tightened
rather than relaxed the evidence: the permutation control, which invalidated a
criterion that had favoured our hypothesis; the Holm correction, which the frozen
analysis plan required but which had not been applied, and which removed the one
remaining significant level for ResNet1D-34; and the choice of reporting axis,
adopted after ICC failed to unify the two datasets. For the last, the factor
$1+(H-1)\rho$ was part of our theoretical notes before the data were collected,
and $H$ follows from (6) rather than being chosen; the decision to report on that
axis was nonetheless made with the results in view. A complete deviation log
accompanies the protocol.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Dibuang dari v1 | (1) "published benchmark of approximately 0.93" — **tidak terverifikasi**; diganti "below published PTB-XL benchmarks [F1]". (2) "Subgroup definitions … examined explicitly" — **salah**, E3 tidak dijalankan. (3) "Randomised recording dates … all temporal analysis" — tidak ada analisis temporal di naskah. (4) "Boundary cells" — menyangkut kriteria `B12_memperbaiki` yang sudah dicabut. (5) Pengulangan angka §8.5 — kini dirujuk |
| Ditambah | Holm sebagai perubahan ketiga sesudah hasil dilihat (§10.6) — wajib jujur |
| Angka | 1,43 pp, 64–68%, 411, 40 detak, 15 detak Q, $K_1(Q)=2$, 0,9615 / 2,43, 81–107%, 24.800 vs 16.500, 34 / 31 / 188 / 1.960 / 3 — semuanya sama dengan v1 dan §8 |
| Penomoran | Persamaan (6), (7) di §5.1.2–5.1.3; Corollary 2.2 di §4.2; Tabel 10.1 → TABLE XI di Word |
