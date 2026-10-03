# §5 Results

> **v7 — 2026-10-02.** Prosa diparafrasekan penuh dari v6 (commit 3edc1f0). Isi Tabel 5.1–5.6 dan keterangan Fig. 3–7 tidak diubah. Fig. 8 kini dua panel: (a) defisit per backbone (gambar lama), (b) sensitivitas checkpoint 16 sel dari `*_terakhir.json` — sebelumnya hanya teks.

---

## 5. Results

The results are presented in the order of the audit: feasibility from metadata
(§5.1), coverage (§5.2), attribution (§5.3), dose–response (§5.4) and robustness
(§5.5). B1 and B12 are as defined in §4.2, and $\alpha_{\min}=1/(K_1+1)$.

### 5.1 Feasibility is decided by the partition, not by the model

**Granularity.** In the PTB-XL calibration fold (fold 9, 2,183 records), blocking
by patient is feasible at every conventional $\alpha$, while each coarser source
restricts the range of admissible levels. For every grouping, Table 5.1 gives the
number of calibration blocks, the resulting $\alpha_{\min}$ and the conventional
levels that remain attainable.

**Table 5.1.** Feasibility of HCP on PTB-XL fold 9 by grouping.

| Grouping | Blocks (all folds) | $K_1$ | Mean block size | $\alpha_{\min}$ | 0.01 | 0.05 | 0.10 | 0.20 |
|---|---:|---:|---:|---:|:-:|:-:|:-:|:-:|
| `patient_id` | 18,869 | 1,942 | 1.12 | 0.00051 | ✓ | ✓ | ✓ | ✓ |
| `site` | 51 | 40 | 54.55 | 0.02439 | — | ✓ | ✓ | ✓ |
| `nurse` | 12 | 12 | 163.42 | 0.07692 | — | — | ✓ | ✓ |
| `device` | 11 | 11 | 198.46 | 0.08333 | — | — | ✓ | ✓ |
| `strat_fold`† | 10 | 8 | 2,179.90 | 0.11111 | — | — | — | ✓ |

† Applicable only if calibration draws on folds 1–8.

The site row calls for caution. Of the 40 sites present in fold 9, 37 appear only
among the 223 records with an empty `nurse` field, whereas the 1,960 fully
annotated records come from just 3 sites. Site-level blocking is admissible, then,
only thanks to a minority of incompletely annotated records that seem to stem
from a different collection regime. Fig. 3 locates these groupings, the joins
considered next and the MIT-BIH record partition on the feasibility frontier, so
that each can be compared with the dotted line of a given $\alpha$.

![**Fig. 3.** Feasibility frontier $\alpha_{\min}=1/(K_1+1)$. Each marker is a calibration grouping on PTB-XL fold 9 (circles: single dependence source; squares: join of sources) or the MIT-BIH record partition (diamond). Values in parentheses are $K_1$. A grouping supports a guarantee at level $\alpha$ only if its marker lies below the corresponding dotted line.](figures/fig3_feasibility_frontier.png)

**Crossed sources.** On PTB-XL the sources cross one another: 46 patients appear
at more than one site, 247 with more than one nurse and 174 on more than one
device. Respecting several sources at once therefore means calibrating on their
join, which coarsens rapidly. Across all 2,183 records, patient and device
together leave $K_1=5$ ($\alpha_{\min}=0.167$), and all four sources together
leave one block ($\alpha_{\min}=0.5$). Restricting attention to the 1,960 records
with complete metadata, we enumerated all 15 joins of the four declared sources;
8 meet the sufficiency condition, and each of those 8 has $K_1=1$. *If patient,
site, nurse, and device are all treated as dependence sources, no admissible
calibration grouping exists at any conventional $\alpha$.* The statement is
conditional on that declaration, which the data cannot verify (§6.4), and the
tendency of joined partitions to merge into a giant component is already known
[P2].

**Labels.** Under label-conditional coverage, Proposition 3 is applied to each
label separately, and the feasible region contracts as the hierarchy becomes
finer. All superclasses pass, yet 24 of the 44 SCP codes fail at $\alpha=0.05$,
`2AVB` occupies a single calibration block, and requiring a Bonferroni
correction across labels makes 43 of 44 codes infeasible at a family-wise
$\alpha=0.05$. Table 5.2 tallies the failing labels at each level of the
hierarchy.

**Table 5.2.** Labels failing the necessary condition of Proposition 3, PTB-XL fold 9, patient blocks.

| Level | Labels $m$ | $K_1(\ell)$ range | Fail at 0.01 | Fail at 0.05 | Fail at 0.10 | Fail at 0.05 / $m$ |
|---|---:|---:|---:|---:|---:|---:|
| Superclass | 5 | 242–905 | 0 | 0 | 0 | 0 |
| Subclass | 23 | 2–905 | 15 | 6 | 4 | 22 |
| SCP code | 44 | 1–905 | 36 | 24 | 12 | 43 |

The hierarchy behaved monotonically in all 23 parent–child pairs, and MIT-BIH
class Q is confined to $K_1=2$ records ($\alpha_{\min}=0.333$). Fig. 4 breaks the
counts of Table 5.2 down label by label and marks the minimum number of blocks
required at $\alpha=0.05$ and $\alpha=0.10$.

![**Fig. 4.** Calibration blocks carrying each label, by level of the PTB-XL hierarchy (fold 9, patient blocks; log scale). Dashed and dotted lines mark the minimum number of blocks for a finite per-label threshold at $\alpha=0.05$ and $\alpha=0.10$. Dark bars meet the $\alpha=0.05$ requirement, light bars only the $\alpha=0.10$ requirement, and orange bars neither.](figures/fig4_label_feasibility.png)

### 5.2 Coverage under block dependence

Across 200 block-level splits (§4.2), mean B1 coverage on MIT-BIH lies 1.0–2.4
percentage points below $1-\alpha$ at every level, while on PTB-XL it reaches or
exceeds the nominal value. Table 5.3 lists coverage and set size for both
methods with the primary backbones.

**Table 5.3.** Coverage (mean over splits, with 2.5–97.5% range across splits) and mean set size.

| Dataset | $\alpha$ | B1 coverage | B12 coverage | $\lvert C\rvert$ B1 | $\lvert C\rvert$ B12 |
|---|---:|---|---:|---:|---:|
| MIT-BIH | 0.01‡ | 0.9673 [0.9137, 0.9997] | 1.0000 | 2.695 | 5.000 |
| | 0.05‡ | 0.9398 [0.8045, 0.9974] | 1.0000 | 1.690 | 5.000 |
| | 0.10 | 0.8851 [0.6887, 0.9788] | 0.9615 | 1.051 | 2.434 |
| | 0.15 | 0.8279 [0.6151, 0.9602] | 0.9234 | 0.924 | 1.443 |
| | 0.20 | 0.7764 [0.5542, 0.9462] | 0.8642 | 0.834 | 1.001 |
| PTB-XL | 0.01 | 0.9910 [0.9823, 0.9972] | 0.9912 | 3.769 | 3.788 |
| | 0.05 | 0.9511 [0.9318, 0.9673] | 0.9510 | 2.741 | 2.742 |
| | 0.10 | 0.9010 [0.8741, 0.9256] | 0.9002 | 2.248 | 2.240 |

‡ Below $\alpha_{\min}=1/12$: HCP returns the full label set for every test beat.

Even so, on MIT-BIH the range across splits includes $1-\alpha$ at every level:
with only 11 test records, no single split can expose a deficit of this
magnitude, and a comparison of means does not amount to a test. B12 coverage has
to be interpreted together with set size. At $\alpha=0.10$ HCP attains 0.9615
using 2.43 of the 5 labels, against 1.05 for B1, and below $\alpha_{\min}$ its
perfect coverage is simply abstention. Fig. 5 displays both points at once,
plotting the coverage gap of each method relative to nominal and shading the
levels below $\alpha_{\min}$.

![**Fig. 5.** Coverage minus nominal $1-\alpha$ for split conformal (B1, mean with 2.5–97.5% range across 200 block-level splits) and HCP (B12, mean), primary backbone. Shaded MIT-BIH levels lie below $\alpha_{\min}=1/12$, where HCP returns every label. Note the different vertical scales.](figures/fig5_coverage.png)

### 5.3 The deficit is attributable to dependence

**Permutation null.** To check whether dependence is what makes B1 under-cover,
we compared it with a matched null obtained by permuting the assignment of beats
to records within DS2. This permutation keeps $K_1=11$, the multiset of block
sizes and the marginal score distribution exactly as they were, while the score
ICC drops from 0.519 to 0.000. Table 5.4 reports the B1 deficit relative to this
null at two levels of uncertainty. Over 200 paired splits of the 22 DS2 records
the deficit is positive in all nine backbone×$\alpha$ cells, and for the primary
backbone its Monte Carlo interval excludes zero at all three levels; these
intervals, however, describe the split procedure on these records only (§4.4).
Treating records as the sampling unit, the leave-one-record-out jackknife gives
deficits of 0.60–1.83 pp with 95% intervals of half-width 3.7–5.7 pp, which
include zero in every cell (Holm-adjusted one-sided $p\ge0.59$). On these 22
subjects B1 thus covers less than the permutation null in every configuration,
but 22 subjects are too few to establish the sign of the deficit for the
population they represent.

**Table 5.4.** MIT-BIH: B1 deficit against the permutation null, pp. Monte Carlo interval: percentile bootstrap over 200 paired splits of the 22 DS2 records, conditional on those records. Record level: leave-one-record-out jackknife (500 paired splits and a new permutation per replicate), 95% t interval with 21 df and Holm-adjusted one-sided p.

| Backbone | ICC | $\alpha$ | Deficit [Monte Carlo 95%] | Record level [95% CI] | Holm $p$ |
|------------|-----|-----|----------------------|------------------------|--------|
| SmallECGNet | 0.519 | 0.10 | +1.49 [0.34, 2.71] | +1.26 [−2.70, +5.22] | 0.77 |
| | | 0.15 | +2.21 [0.85, 3.60] | +1.36 [−3.21, +5.93] | 0.77 |
| | | 0.20 | +2.37 [0.79, 3.93] | +1.02 [−4.67, +6.71] | 0.77 |
| ResNet1D-34 | 0.436 | 0.10 | +1.15 [0.10, 2.23] | +1.55 [−2.15, +5.26] | 0.59 |
| | | 0.15 | +1.02 [−0.16, 2.23] | +1.14 [−3.36, +5.63] | 0.60 |
| | | 0.20 | +0.81 [−0.59, 2.17] | +0.60 [−4.44, +5.65] | 0.60 |
| ResNet1D-50 | 0.462 | 0.10 | +2.54 [1.25, 3.87] | +1.72 [−3.70, +7.14] | 0.68 |
| | | 0.15 | +3.42 [1.91, 4.98] | +1.83 [−3.16, +6.81] | 0.68 |
| | | 0.20 | +3.18 [1.54, 4.82] | +1.17 [−4.07, +6.42] | 0.68 |

**Weighting.** Averaging coverage within each test record before averaging over
records, the empirical counterpart of (2), does not weaken these findings (full
data of the same jackknife runs). Block-weighted B1 coverage lies below its
observation-weighted value in all nine cells, and the deficit against the
permutation null becomes 1.43–2.61 pp. Block-weighted HCP coverage stays above
$1-\alpha$ at every level and for every backbone (0.9531–0.9548 at $\alpha=0.10$,
0.9146–0.9178 at 0.15 and 0.8557–0.8565 at 0.20), as guarantee (2) requires.

This control also shows why a B12-versus-B1 comparison says little. We define the
mechanical share as the B12−B1 gap in the permuted arm divided by the same gap on
the original data. Its values lie between 81% and 107%: removing dependence
hardly alters the gap, and at $\alpha=0.10$ the gap is even slightly wider
without dependence than with it, because the finite-block correction pushes HCP
to the $(1-\alpha)(K_1+1)/K_1$ quantile whether or not dependence is present. "B12
improves on B1" was consequently withdrawn as a criterion (§6.4), and the
deficit against the permutation null is the evidence used throughout.

**Factorial decomposition.** A 2×2 design crossed clustering (original versus
randomized record membership) with block-size balance (balanced versus
imbalanced) with calibration size matched in expectation (§4.4). Clustering lowered
coverage by 1.22, 1.55 and 1.49 pp at $\alpha=0.10, 0.15, 0.20$, with Monte Carlo
intervals over 400 splits that exclude zero (for example $[-1.84, -0.63]$ pp at
0.10). The imbalance main effect was smaller (−0.44, −0.26, −0.27 pp), and
imbalance acted mainly through clustering: at $\alpha=0.10$ it lowered coverage by
0.83 pp when records were clustered but by 0.04 pp when membership was
randomized (interaction −0.79 pp; −0.54 and −0.52 pp at the other levels), as the
pooled design effect in (6), which grows with $\sum_k N_k^2$ only when $\rho>0$,
anticipates. Block-size imbalance therefore does not produce the deficit on its
own; it amplifies the effect of clustering. Like those of Table 5.4, these
intervals are conditional on the 22 DS2 records. Fig. 6 places the two controls
next to each other: panel (a) shows the clustering effect dominating, and panel
(b) that the B12−B1 gap keeps nearly its full size once dependence is permuted
away.

![**Fig. 6.** Attribution of the MIT-BIH deficit, primary backbone. (a) Effects of clustering, block-size imbalance and their interaction on B1 coverage in the 2×2 factorial design (Monte Carlo 95% interval over 400 splits; open markers include zero). (b) B12−B1 coverage gap on the original data and after permuting beats between records (bars: mean; whiskers: 2.5–97.5% range across splits). Percentages give the mechanical share, the permuted gap as a fraction of the original.](figures/fig6_attribution.png)

### 5.4 The deficit tracks the design effect

To vary dependence inside a single dataset, we moved a fraction $p$ of MIT-BIH
beats to randomly chosen records while subsampling every calibration record to
1,355 beats, so that calibration-block imbalance plays no part (11 values of $p$,
300 splits each; test records are used in full). Over this
range the score ICC declines from 0.519 at $p=0$ to 0.0001 at $p=1$. Because
calibration records are subsampled to a common size, the deficits are smaller than in §5.3
(0.65 pp at $p=0$, $\alpha=0.10$) and every per-point Monte Carlo interval includes
zero; the
evidence therefore lies in the trend across points, summarized by Spearman
correlations. These replace the cross-dataset test of the initial protocol
(§6.4) and are descriptive: all points derive from the same 22 records, so the
accompanying $p$-values, which treat points as independent, are not population
inference. Table 5.5 reports the correlations on three dependence axes, and
within MIT-BIH the deficit grows with ICC at all three levels.

**Table 5.5.** Spearman correlation between dependence and coverage deficit ($p$-values treat points as independent and are shown for completeness).

| Axis | Points | $\alpha=0.10$ | $\alpha=0.15$ | $\alpha=0.20$ |
|---|---:|---|---|---|
| Score ICC, MIT-BIH only | 11 | 0.88 ($p=0.0003$) | 0.78 ($p=0.0045$) | 0.80 ($p=0.0031$) |
| DEff, MIT-BIH + PTB-XL | 12 | 0.84 ($p=0.0006$) | 0.80 ($p=0.0016$) | 0.85 ($p=0.0005$) |
| Indicator DEff, MIT-BIH + PTB-XL | 12 | 0.90 ($p<0.0001$) | 0.80 ($p=0.0016$) | 0.71 ($p=0.010$) |

On the ICC axis alone PTB-XL does not fit: its patient-level ICC of 0.352 equals
that of a MIT-BIH point whose deficit is 0.35 pp, yet PTB-XL has none. The design
effect resolves the mismatch. With $H=1.05$, PTB-XL has a DEff of 1.02, compared
with 704 for intact MIT-BIH, and on this axis the combined correlation remains
positive (0.80–0.85); redoing the computation with the ICC of the coverage
indicator at a fixed threshold, the quantity that enters the variance of §3.2,
does not change the conclusion. DEff is used as a summary axis, not a sufficient
statistic; an exceedance-specific design effect is given in [P1]. Fig. 7 shows
the deficit as a function of DEff: the MIT-BIH gradient carries the combined
correlation, while PTB-XL acts as a prediction check at the low-dependence end
rather than as an independent trend (§6.4), with deficits of −0.05, −0.12 and
−0.16 pp, that is, coverage slightly above nominal.

![**Fig. 7.** B1 coverage deficit against the design effect. MIT-BIH points (blue) are obtained by randomly reassigning a growing fraction of beats to other records, with calibration records subsampled to a common size; PTB-XL (orange) is the observed patient partition with its Monte Carlo 95% interval. The annotation gives the Spearman correlation over the 12 points at $\alpha=0.10, 0.15, 0.20$.](figures/fig7_dose_response.png)

### 5.5 Robustness to backbone and checkpoint

**Backbone.** The two residual networks, with about 70 and 155 times as many
parameters, improved discrimination only unevenly: MIT-BIH balanced accuracy
stayed between 0.370 and 0.376, and PTB-XL macro-AUROC dropped slightly. As the
negative control requires, $K_1(\ell)$ did not change across backbones on either
dataset. Table 5.6 sets out the discrimination of all three backbones.

**Table 5.6.** Discrimination by backbone.

| Backbone | Parameters (MIT-BIH / PTB-XL) | MIT-BIH accuracy | MIT-BIH balanced acc. | PTB-XL macro-AUROC |
|---|---|---:|---:|---:|
| SmallECGNet | 101,925 / 104,389 | 0.869 | 0.375 | 0.902 |
| ResNet1D-34 | 7,220,805 / 7,225,733 | 0.922 | 0.376 | 0.897 |
| ResNet1D-50 | 15,964,485 / 15,969,413 | 0.926 | 0.370 | 0.896 |

On PTB-XL, B1 reached nominal coverage in all 9 backbone×$\alpha$ cells, with mean
coverage 0.05–0.19 pp above nominal. On MIT-BIH the deficit against the
permutation null is positive in all 9 backbone×$\alpha$ cells (Table 5.4). Its
Monte Carlo interval excludes zero in 7 of them, the exceptions being ResNet1D-34
at $\alpha=0.15$ and $0.20$, where the deficit is smallest (0.81–1.02 pp); at the
record level no cell excludes zero. Across the three backbones the mechanical
share of the B12−B1 gap ranged from 75% to 110%.

**Checkpoint.** With only 4 validation records on MIT-BIH, early stopping picked
epoch 1 for ResNet1D-50. A sensitivity analysis therefore reran
the audit with last-epoch weights for both residual networks on both datasets
(MIT-BIH epochs 13 vs. 8 and 6 vs. 1; PTB-XL 14 vs. 9 and 12 vs. 7). In all 16
backbone×dataset×$\alpha$ cells the B1 deficit kept its sign and $K_1(\ell)$ was
unchanged, but on MIT-BIH its magnitude shifted by as much as 1.8 pp, enough to
change the ordering of the backbones, so differences in deficit size between
backbones are not interpreted. Fig. 8 summarizes both robustness checks. Panel
(a) sets the Monte Carlo intervals of Table 5.4 against the record-level
intervals: the direction holds for every backbone, but only the narrower,
conditional intervals exclude zero. Panel (b) plots each cell under the two
checkpoints, and every point stays in the quadrant of its original sign.

![**Fig. 8.** Robustness of the audit. (a) MIT-BIH B1 coverage deficit against the matched permutation null, by backbone and $\alpha$: point estimate with Monte Carlo 95% interval over 200 splits of the 22 DS2 records (open markers include zero), and record-level 95% CI from the leave-one-record-out jackknife (light bars). (b) B1 coverage minus nominal under best-validation (horizontal) and last-epoch (vertical) weights for the two residual networks, 16 backbone×dataset×$\alpha$ cells; shaded quadrants mark agreement in sign and the dotted line marks equality.](figures/fig8_robustness.png)

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Sumber angka | 5.1: `feasibility_alpha.json`, `corollary32_lattice.json`, `label_feasibility.json` · 5.2: `backbone_invariance/{mitdb,ptbxl}_small.json` · 5.3: `control_permutation_mitdb.json`, `factorial_mitdb.json` · 5.4: `dose_response.json`, `monotonicity_icc_mitdb.json`, `robustness_indicator_icc.json` · 5.5: `backbone_invariance/*.json` (+ `*_terakhir.json`), `control_permutation_mitdb_resnet1d*.json` |
| Fig. 8b | 16 sel = 2 backbone residual × (5 α MIT-BIH + 3 α PTB-XL); tanda sama di 16/16; selisih maks MIT-BIH 1,82 pp |
| Konvensi tanda | Defisit positif = kurang-cakup |
