# §6 Discussion

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0). Semua ancaman validitas, angka dan sitasi tetap; kalimat kondisional PTB-XL tetap kata per kata.

---

## 6. Discussion

### 6.1 Main findings

The audit separates two questions that are usually merged: can a block-level
coverage guarantee be *enforced* on a clinical dataset, and does ignoring block
structure *cost* coverage when it is not? The first is combinatorial and is
settled by metadata. On the resources audited here the answer is stricter than
their size suggests, because declared sources collapse under the join and rare
labels are spread over few patients (§5.1). Proposition 1 makes the point
directly: splitting the 22 evaluation subjects of the canonical MIT-BIH partition
evenly between calibration and test leaves $K_1=11$, which rules out a
subject-level guarantee at the 95% level for this design, whatever the model and
however many beats each record holds.

The second question is statistical, and its answer depends on how many repeats
blocks contain more than on how strongly their observations correlate
(§5.3–§5.4). PTB-XL shows this most clearly. Its within-patient correlation seems
to call for block-level calibration, yet with $H=1.05$ the factor $1+(H-1)\rho$
stays near 1 for any $\rho$, and counting repeats correctly predicts that such
calibration is unnecessary for marginal coverage at these levels. Both quantities
should be reported, and neither belongs to the dataset alone: $K_1$ depends on
the split design and $\rho$ on the model (§4.1). The two questions also meet. On
MIT-BIH the deficit has the same sign across backbones, levels and splits of the
22 evaluation subjects, yet a jackknife over those subjects cannot resolve it
(§5.3): the scarcity of blocks that bounds the guarantee also bounds what an
audit of the same subjects can establish.

### 6.2 Two pitfalls in evaluating conformal methods on clustered data

The lesson that travels furthest concerns evaluation rather than ECG. On the same
data HCP seems to "restore" the coverage that naive split conformal loses, but
75–110% of the difference persists once within-block dependence is permuted away
(§5.3, §5.5). The mass $1/(K_1+1)$ at $+\infty$ lifts HCP to a higher empirical
quantile regardless of dependence, and when $K_1$ is small, exactly where
block-level calibration matters, this mechanical inflation dominates. Below
$\alpha_{\min}$ the comparison degenerates, since HCP covers by returning every
label (Fig. 6). A claim that a hierarchical method improves coverage should
therefore be tested against a null that keeps block sizes and score marginals but
removes dependence, and coverage should always be reported with set size,
abstention being the cheapest route to coverage.

The second pitfall concerns uncertainty. Conformal methods are often evaluated
over many random calibration–test splits of one dataset. With clustered data
those splits reuse the same subjects, so the spread or bootstrap interval of the
coverages describes the split procedure on those subjects and shrinks as splits
are added; it is not a confidence interval for the population. On MIT-BIH this
decides the reading: repeated-split intervals exclude zero in most cells of
Table 5.4, while the jackknife over the same 22 subjects includes zero in all of
them. Population claims should resample subjects, and with few subjects the
honest conclusion may be that the sign of a coverage gap is not yet known.

### 6.3 Implications and relation to prior work

A study that plans to attach distribution-free guarantees to an ECG classifier
can run four checks before collecting or splitting data:

1. **Declare dependence sources** (patient, device, site, operator, monitoring
   episode) and check that each is documented; if one is not, as with patient
   identity in Challenge 2021, the block count is an assumption.
2. **Count blocks, not records**, under the grouping that respects all declared
   sources, and compare the count with $\lceil 1/\alpha\rceil-1$.
3. **Repeat the count per label** for label-conditional claims, using
   $\lceil m/\alpha\rceil-1$ for simultaneous claims over $m$ labels; rare
   diagnoses usually fail first.
4. **Estimate repetition** through the harmonic mean block size before deciding
   whether marginal coverage needs block-level calibration.

The same arithmetic applies whenever coverage is conditioned on patient groups:
once group-conditional calibration for demographic fairness [D4] must also
respect patient blocks, a group with few calibration patients faces the same
bound as a rare label. Settings with thousands of blocks, such as patients nested
in hospitals [E5], lie far from this boundary, which is why it is easy to miss.
The inter-patient protocol prevents subject-level leakage [F2], [F3], [F10], and
training regimes that differ in this respect have been compared [F5], but a split
that is inter-patient for training can still leave too few subjects in
calibration.

For the design trade-off left open by Lee et al. [A0], our results settle the
most elementary part: whether a finite threshold exists depends only on the
number of groups (Proposition 1). With blocks in place of points, the bound plays
the role of the minimum calibration size that the universal coverage
distribution of split conformal prediction implies for exchangeable data [A9];
and, as for rare classes under exchangeability [A12], the count that matters per
label is that of blocks carrying it, under a necessary but not sufficient
condition (§3.4). The findings agree with Sim and Kim [E6]: subjects, not beats,
carry the guarantee, and too few calibration subjects undermine it. The audit
differs in counting blocks under crossed sources and per label, and in separating
dependence from block-size imbalance and from the mechanical effect of the
finite-block correction. Evidence that marginal coverage can mask per-class and
per-patient failures in cardiac monitoring [E8] matches the label-level boundary
of §5.1. Risk-control extensions [C1], [C2] and time-series variants [C4] rest on
related exchangeability or stationarity assumptions; whether their block-level
versions meet the same boundary is open.

### 6.4 Limitations and threats to validity

The audit concerns marginal and label-wise coverage for one method family.

**Internal validity.** Only 64–68% of PTB-XL records in folds 1–8 were validated
by cardiologists, against 100% in folds 9 and 10. An early version that
calibrated on fold 8 and evaluated on fold 9 showed an apparent deficit of 1.43
percentage points at $\alpha=0.05$, which proved to reflect label quality rather
than block dependence; confirmatory analyses therefore use fold 9, and fold 10
remains unexamined. Each data-handling choice in §4.1 guards against a silent
failure, and no preprocessing step uses quantities estimated from evaluation
data: the filter is fixed and normalization is per record or per beat.

**Construct validity.** MIT-BIH class Q has 15 beats, 7 of them in two evaluation
records, so its per-class statistics cannot be interpreted; reporting
$K_1(\mathrm{Q})=2$, i.e. $\alpha_{\min}=1/3$, keeps the boundary in view. Our
backbones fall below published PTB-XL benchmarks [F1] and perform poorly on
MIT-BIH minority classes (balanced accuracy 0.37–0.38 for all three), which
enlarges prediction sets without lowering coverage (§4.3, §5.5). With only 4
validation records, early stopping chose epoch 1 for ResNet1D-50 on MIT-BIH; the
last-epoch analysis preserved the sign of every deficit and every $K_1$ but not
the magnitude, which is therefore not compared across backbones.

**External validity.** PTB-XL comes from one institution and was recorded in
1989–1996; its device, nurse and site metadata make the block analysis possible,
but its $\rho$ and $H$ may not carry over to present-day multi-center cohorts.
Eleven of the twelve dose–response points are synthetic MIT-BIH configurations,
so the combined correlation reflects an intervention within one dataset, and
PTB-XL, which differs in modality, task and block type, serves only as a
prediction check (§5.4). All results concern ECG; temporal dependence within a
patient across visits is not addressed, and other clinical signals with repeated
measurements were not examined.

**Statistical conclusion validity.** The repeated-split intervals of Table 5.4
and Fig. 7 and the Spearman $p$-values of Table 5.5 are conditional on the 22 DS2
records and one permutation (§4.4, §6.2). Only the post hoc leave-one-record-out
jackknife treats records as the sampling unit, and its intervals include zero in
every cell; since each replicate rests on 500 splits, Monte Carlo error inflates
its variance somewhat, so those intervals are conservative. No single split or
dose–response point shows a deficit: the split-to-split range covers $1-\alpha$
in every MIT-BIH cell (Table 5.3). Two criteria of the initial protocol were
dropped, "HCP covers better than split conformal" once the permutation control
showed the gap to be largely mechanical (§5.3), and a Spearman test across two
datasets, whose rank correlation can only be $\pm1$; these and the unused parts of
the initial statistical plan (patient-level bootstrap, a paired permutation test
with 10,000 permutations, exact binomial intervals, Cliff's delta) are listed in
the protocol's deviation log.

**Theoretical scope.** The variance of §3.2 and the design effects (4) rest on
Assumption (A), a one-way random-effects model with compound symmetry, whereas
Proposition 1, Corollary 2 and Proposition 3 need no distributional assumption.
The variance involves the correlation of the coverage indicator, not of the raw
score; with the indicator correlation every Spearman coefficient stays positive
(Table 5.5), and PTB-XL's correlation drops from 0.35 to 0.19–0.20 while its
design effect stays near 1. The design effect ranks configurations, but we do not
show that it is sufficient for coverage loss. Corollary 2 is proved for HCP only
(§3.3), and the hierarchical constructions are not compared with one another
[A0b]. For PTB-XL the verdict is exhaustive only for the declared sources
{patient, site, nurse, device}, which the data cannot verify, and the merging of
joins into a giant component is known [P2]. Declaring only {patient, site} gives
$K_1=34$ on the full calibration fold and makes $\alpha=0.05$ feasible, yet 31 of
these blocks consist entirely of 188 records without nurse metadata, and on the
1,960 fully annotated records the same declaration gives $K_1=3$. The result is
therefore conditional: *if patient, site, nurse, and device are all treated as
dependence sources, no admissible calibration grouping exists at any conventional
$\alpha$.* Finally, what ECG networks learn [F6] and how well they discriminate
[F1] are orthogonal to this question: an accurate model calibrated on too few
blocks still carries no guarantee.

**Researcher degrees of freedom.** Our reading of the MIT-BIH evidence changed
three times, each time prompted by an added control rather than by rereading
data, and its statistical strength was revised once more (Appendix B). Every
analysis introduced or modified after results were seen made the evidence
stricter: the permutation control overturned a criterion that favored our
hypothesis; the Holm correction, specified in the initial protocol but applied
late, removed the last significant level for ResNet1D-34; the reporting axis was
chosen after ICC failed to place the two datasets on one scale; and the
record-level jackknife, specified and committed before it was run, showed that
repeated-split significance did not extend to subjects. The factor $1+(H-1)\rho$
appeared in our theoretical notes before data collection, but the decision to
report on this axis was taken with the results in view. The analysis protocol was
kept under version control but not publicly registered or formally frozen; it is
released with its deviation log.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Dipertahankan | Semua butir §6.4 dan angka: 64–68%, 1,43 pp, 15/7 detak Q, $K_1(Q)=2$, 0,37–0,38, 4 rekaman validasi, 1989–1996, 22 rekaman, 0,35 → 0,19–0,20, 34 / 31 / 188 / 1.960 / 3 |
| Kata per kata | Kalimat kondisional PTB-XL (klaim inti, tidak boleh bergeser maknanya) |
