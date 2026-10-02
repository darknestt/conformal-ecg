# §10 Threats to Validity

> **v3 — 2026-10-02.** Ditulis ulang dan dipadatkan (1.114 → ±880 kata). Semua ancaman v2 tetap ada (institusi tunggal, split berulang 22 rekaman, titik sintetis, domain EKG, sumber yang dideklarasikan, ruang lingkup Kor. 2.2, kualitas model, statistik, derajat kebebasan peneliti/log deviasi). Versi sebelumnya: `sec10-draft.md` di riwayat git (commit 9098746).

---

## 10. Threats to Validity

### 10.1 Internal validity

**Label provenance.** Cardiologists validated only 64–68% of PTB-XL records in
folds 1–8, against 100% in folds 9 and 10. An early version of the study that
calibrated on fold 8 and evaluated on fold 9 found an apparent 1.43
percentage-point deficit at $\alpha=0.05$, which turned out to reflect the shift
in label quality between folds rather than block dependence. Confirmatory
analyses therefore use fold 9, and fold 10 has not been examined.

**Data handling.** Each decision in §6.2–6.3 guards against a failure that raises
no error (unlabelled records, channel order in record 114, boundary beats, the
subject shared by records 201 and 202), and all preprocessing is fitted on
training data only.

### 10.2 Construct validity

**Degenerate class.** MIT-BIH class Q has 15 beats in total, 7 of them in two
evaluation records. Per-class statistics for Q cannot be interpreted; we report
$K_1(\mathrm{Q})=2$, i.e. $\alpha_{\min}=1/3$, so that the boundary is visible
rather than averaged away.

**Model quality.** Because conformal guarantees are model-agnostic, a weak model
widens prediction sets without reducing coverage. Our primary backbones fall
below published PTB-XL benchmarks [F1] and are weak on MIT-BIH minority classes
(balanced accuracy 0.37–0.38 for all three backbones), so their discrimination
bears on set size rather than on coverage, a reading tested on two larger
networks (§8.5).

**Checkpoint selection.** With 4 validation records, early stopping chose epoch 1
for ResNet1D-50 on MIT-BIH. The pre-registered last-epoch analysis (§8.5)
preserved the sign of every deficit and every $K_1$ but not the magnitude, which
we therefore do not compare across backbones.

### 10.3 External validity

**Single institution.** PTB-XL was recorded at one institution between 1989 and
1996. Its device, nurse and site metadata make the block analysis possible, but
its estimates of $\rho$ and $H$ need not transfer to contemporary multi-center
cohorts.

**One gradient, one external point.** Eleven of the twelve dose–response points
are synthetic MIT-BIH configurations obtained by reassigning beats between
records; only the twelfth, PTB-XL, is observed. The combined correlation is thus
driven by an intervention within one dataset rather than by naturally differing
cohorts, and PTB-XL — different in modality, task and block type — serves only as
a prediction check that lands where the design effect predicts.

**Fixed evaluation subjects.** All MIT-BIH intervals come from repeated splits of
the same 22 DS2 records, so they quantify variability across splits, not across
the patient population.

**Domain.** All results concern ECG. Other clinical signals with repeated
measurements are plausible candidates for the same analysis but were not
examined.

### 10.4 Statistical conclusion validity

**Per-configuration deficits.** No single split and no single dose–response point
establishes a deficit: split-to-split ranges contain $1-\alpha$ in every MIT-BIH
cell (Table 8.3), and every per-point interval in the dose–response analysis
contains zero. The evidence lies in the comparison with a permutation null and in
the monotone trend, which are what the pre-registered tests address.

**Strength across backbones.** After Holm correction the deficit against the
permutation null is significant at every level for two of three backbones and at
none for ResNet1D-34 (Table 8.4). The pre-registered criterion fails for that
backbone, and we claim invariance of direction only.

**Coverage and set size.** Coverage alone overstates HCP, which at
$\alpha=0.10$ on MIT-BIH reaches 0.9615 with 2.43 of 5 labels per beat and below
$\alpha_{\min}$ covers by abstaining; both quantities are reported throughout.

**Withdrawn and replaced criteria.** Two pre-registered criteria did not survive.
"HCP covers better than split conformal" was withdrawn once the permutation
control showed the gap to be largely mechanical (§8.3). A Spearman test across
datasets could not be run as written, because with two datasets the rank
correlation can only be $\pm1$; it was replaced by a test over design-effect
points within MIT-BIH. Both changes are logged as deviations.

### 10.5 Theoretical threats

**Assumption (A).** The variance (6) and design effects (7) assume a one-way
random-effects model with compound symmetry, whereas Proposition 1, Corollary 2.2
and the label-level condition of §5.3 are distribution-free. Expression (6)
concerns the correlation of the coverage indicator rather than of raw scores;
with the indicator correlation every Spearman coefficient remains significant
(Table 8.5), and PTB-XL's correlation falls from 0.35 to 0.19–0.20 while its
design effect stays near 1.

**Scope of the impossibility result.** *Corollary 2.2 is proved for the HCP/Dunn
family. Whether it holds for every distribution-free method that relies on
exchangeability between blocks remains an open question.* The collapse of joined
partitions into a giant component is itself known [P2]. On PTB-XL the verdict is
exhaustive only for the declared sources {patient, site, nurse, device}, which
cannot be verified from data. Declaring only {patient, site} gives $K_1=34$ on the
full calibration fold and makes $\alpha=0.05$ feasible, but 31 of those blocks
consist solely of 188 records lacking nurse metadata, and on the 1,960 records
with complete metadata the same declaration gives $K_1=3$. We therefore state the
result conditionally: *if patient, site, nurse, and device are all treated as
dependence sources, no admissible calibration grouping exists at any
conventional $\alpha$.*

### 10.6 Researcher degrees of freedom

Our reading of the MIT-BIH evidence changed three times before it stabilized
(Table 10.1), each time after a control was added rather than after existing data
were reinterpreted. The second stage was our own error: it compared analyses with
different calibration sizes (about 24,800 against 16,500 beats) and attributed
the difference to block balance.

**Table 10.1.** Interim conclusions on MIT-BIH and the control that overturned each.

| Stage | Interim conclusion | Overturned by |
|---|---|---|
| 1 | HCP improves on naive split conformal | Permutation control: 81–107% of the gap is mechanical |
| 2 | The deficit is driven by block-size imbalance | 2×2 factorial: imbalance significant at 0/3 levels, clustering at 3/3 |
| 3 | The deficit increases monotonically with ICC | PTB-XL: ICC 0.35 yet no deficit |
| 4 | The deficit tracks $1+(H-1)\rho$ | — stands |

Three analyses were added or changed after results were seen, and each tightened
the evidence. The permutation control invalidated a criterion that had favored
our hypothesis. The Holm correction, required by the frozen analysis plan but not
initially applied, removed the one remaining significant level for ResNet1D-34.
The reporting axis was adopted after ICC failed to unify the two datasets; the
factor $1+(H-1)\rho$ was already in our theoretical notes before the data were
collected, and $H$ follows from (6) rather than being chosen, but the decision to
report on that axis was made with the results in view. A complete deviation log
accompanies the protocol.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Dipertahankan | Semua angka: 64–68%, 1,43 pp, 15/7 detak Q, $K_1(Q)=2$, 0,37–0,38, 4 rekaman validasi, 1989–1996, 22 rekaman, 0,9615 / 2,43, 0,35 → 0,19–0,20, 34 / 31 / 188 / 1.960 / 3, 24.800 / 16.500, 81–107% |
| Kalimat ruang lingkup Kor. 2.2 | Tetap kata per kata |
| Dipadatkan | "Data handling": jumlah 411 dan 40 kini dirujuk ke §6 (tetap di sana); kalimat pengantar tiap ancaman |
