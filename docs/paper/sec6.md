# §6 Discussion

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0). Semua ancaman validitas, angka dan sitasi tetap; kalimat kondisional PTB-XL tetap kata per kata.

---

## 6. Discussion

### 6.1 Main findings

This audit keeps apart two questions that are usually conflated: can a
block-level coverage guarantee be *enforced* on a clinical dataset, and does
ignoring block structure *cost* coverage when it is not enforced? The first is
combinatorial and is answered from metadata. On public ECG resources the answer
is more restrictive than their size would suggest, because declared sources
collapse under the join and rare labels are spread over few patients (§5.1).
Proposition 1 gives a direct illustration: dividing the 22 evaluation subjects of
the canonical MIT-BIH partition equally between calibration and test leaves
$K_1=11$, which rules out a subject-level guarantee at the 95% level for this
design regardless of the model or of how many beats each record holds.

The second question is statistical, and its answer turns on how many repeats the
blocks contain rather than on how strongly observations within them are
correlated (§5.3–§5.4). PTB-XL makes the point most clearly. Its within-patient
correlation would seem to call for block-level calibration, yet with $H=1.05$ the
factor $1+(H-1)\rho$ stays close to 1 for any $\rho$, and counting repeats shows,
correctly for marginal coverage at these levels, that such calibration is
unnecessary. Both quantities should therefore be reported, and neither belongs to
the dataset alone, since $K_1$ depends on the split design and $\rho$ on the model
that produced the scores (§4.1). The design effect is used here purely as an
ordering axis, a heuristic under a compound-symmetric model (§3.2); a principled
effective sample size for thresholds under clustering is derived in [P1].

### 6.2 A pitfall in evaluating hierarchical conformal methods

The lesson that travels furthest concerns evaluation, not ECG. Applied to the
same data, HCP seems to "restore" the coverage that naive split conformal loses,
but 75–110% of that difference persists after within-block dependence has been
permuted away (§5.3, §5.5). Placing mass $1/(K_1+1)$ at $+\infty$ lifts HCP to a
higher empirical quantile irrespective of dependence, and when $K_1$ is small —
exactly the regime in which block-level calibration matters — this mechanical
inflation is the dominant effect. Below $\alpha_{\min}$ the comparison
degenerates altogether, since HCP achieves coverage by returning every label
(Fig. 5). Any claim that a hierarchical method improves coverage should
accordingly be tested against a null that keeps block sizes and score marginals
but removes dependence, and coverage should always be accompanied by set size,
abstention being the cheapest route to coverage.

### 6.3 Implications and relation to prior work

Before collecting or splitting data, a study that plans to attach
distribution-free guarantees to an ECG classifier can run four checks:

1. **Declare dependence sources** — patient, device, site, operator, monitoring
   episode — and confirm that each is documented. If one is not, as with patient
   identity in the PhysioNet/CinC Challenge 2021 collection (§4.1), the block
   count becomes an assumption instead of a measurement.
2. **Count blocks, not records**, in the calibration set, using the grouping that
   respects all declared sources, and compare that count with
   $\lceil 1/\alpha\rceil-1$.
3. **Repeat the count per label** whenever a label-conditional claim is made,
   with $\lceil m/\alpha\rceil-1$ for simultaneous claims over $m$ labels; rare
   diagnoses usually fail first.
4. **Estimate the repetition** through the harmonic mean block size before
   deciding whether marginal coverage requires block-level calibration.

The same arithmetic applies whenever coverage is conditioned on patient groups.
Group-conditional calibration has been proposed to equalize coverage across
demographic groups [D4]; once it must also respect patient blocks, a group
represented by few patients in calibration faces the same bound as a rare label.
Settings with thousands of blocks, such as patients nested in hospitals [E5],
are far from this boundary, which explains why it is easily missed. The
inter-patient protocol protects against subject-level leakage between training
and evaluation [F2], [F3], [F10], and training regimes that differ in this
respect have been compared directly [F5]; the audit extends the same concern to
the boundary between calibration and test, where a split that is inter-patient
for training may still leave calibration with too few subjects.

Regarding the study-design trade-off left open by Lee et al. [A0], our results
settle its most elementary part: whether a finite threshold exists depends only
on the number of groups (Proposition 1). The bound plays, with blocks in place of
points, the part that the universal coverage distribution of split conformal
prediction plays for exchangeable data, where it fixes a minimum calibration
size [A9]. Similarly, rare classes are known to starve class-conditional
calibration under exchangeability [A12], but under block dependence what must be
counted is the number of blocks carrying the class, and the condition is
necessary but not sufficient (§3.4).

These findings are in line with those of Sim and Kim on false-alarm control in
ECG [E6]: in both settings subjects rather than beats carry the guarantee, and too
few calibration subjects undermine it. The two studies differ in what is counted
and in how the effect is attributed. The audit counts blocks under crossed
dependence sources and for each diagnostic label, and it uses a matched
permutation null and a factorial design to separate dependence from block-size
imbalance and from the mechanical effect of the finite-block correction. That
marginal coverage can mask per-class and per-patient failures in cardiac
monitoring [E8] agrees with the label-level boundary of §5.1. Risk-control
extensions of conformal prediction [C1], [C2] and its time-series variants [C4]
depend on related exchangeability or stationarity assumptions, and whether their
block-level versions meet the same boundary is left open.

### 6.4 Limitations and threats to validity

This audit addresses marginal and label-wise coverage for a single method
family; the threats to its conclusions are grouped below by type.

**Internal validity.** In folds 1–8 of PTB-XL only 64–68% of records were
validated by cardiologists, against 100% in folds 9 and 10. An early version of
the study that calibrated on fold 8 and evaluated on fold 9 reported an apparent
deficit of 1.43 percentage points at $\alpha=0.05$; this proved to reflect the
change in label quality between folds rather than block dependence, which is why
confirmatory analyses use fold 9 and fold 10 remains unexamined. Each
data-handling choice in §4.1 protects against a failure that would raise no
error (unlabelled records, the channel order of record 114, boundary beats, and
the subject shared by records 201 and 202), and every preprocessing step is
fitted on training data alone.

**Construct validity.** MIT-BIH class Q comprises 15 beats in total, 7 of which
fall in two evaluation records, so per-class statistics for Q cannot be
interpreted; reporting $K_1(\mathrm{Q})=2$, i.e. $\alpha_{\min}=1/3$, keeps the
boundary in view instead of averaging it away. Our backbones perform below
published PTB-XL benchmarks [F1] and poorly on MIT-BIH minority classes
(balanced accuracy 0.37–0.38 for all three), which enlarges prediction sets
without lowering coverage (§4.3, §5.5). Since only 4 records were available for
validation, early stopping chose epoch 1 for ResNet1D-50 on MIT-BIH; the
pre-registered last-epoch analysis left the sign of every deficit and every $K_1$
intact but not the magnitude, which is therefore not compared across backbones.

**External validity.** PTB-XL comes from a single institution and was recorded
between 1989 and 1996; its device, nurse and site metadata are what make the
block analysis possible, but its estimates of $\rho$ and $H$ may not carry over to
present-day multi-center cohorts. Of the twelve dose–response points, eleven are
synthetic MIT-BIH configurations and only PTB-XL is observed, so the combined
correlation reflects an intervention inside one dataset rather than naturally
differing cohorts, and PTB-XL — which differs in modality, task and block type —
serves only as a prediction check (§5.4). Every MIT-BIH interval is derived from
repeated splits of the same 22 DS2 records and thus captures variability across
splits, not across the patient population. All results concern ECG, and
temporal dependence within a patient across visits is not addressed; other
clinical signals with repeated measurements are natural candidates for the same
analysis but were not examined.

**Statistical conclusion validity.** Neither a single split nor a single
dose–response point establishes a deficit: the split-to-split range covers
$1-\alpha$ in every MIT-BIH cell (Table 5.3), and each per-point interval of the
dose–response analysis includes zero. The evidence comes instead from the
comparison with a permutation null and from the monotone trend, which are exactly
what the pre-registered tests examine. After Holm correction the deficit against
the permutation null is significant at every level for two of the three
backbones and at none for ResNet1D-34 (Table 5.4); for that backbone the
pre-registered criterion fails, and we claim only that the direction is
invariant. Coverage on its own flatters HCP, which covers by abstaining below
$\alpha_{\min}$ (§5.2), so set size is reported alongside coverage throughout. Two
pre-registered criteria did not survive. "HCP covers better than split
conformal" was withdrawn after the permutation control revealed the gap to be
largely mechanical (§5.3). A Spearman test across datasets could not be carried
out as specified, because with two datasets a rank correlation can only equal
$\pm1$, and it was replaced by a test over design-effect points within MIT-BIH.
Both changes appear in the deviation log.

**Theoretical scope.** The variance of §3.2 and the design effects (6) depend on
Assumption (A), a one-way random-effects model with compound symmetry, whereas
Proposition 1, Corollary 2 and Proposition 3 hold without distributional
assumptions. That variance involves the correlation of the coverage indicator
rather than of the raw score; with the indicator correlation every Spearman
coefficient stays significant (Table 5.5), and PTB-XL's correlation drops from
0.35 to 0.19–0.20 while its design effect remains near 1. The design effect ranks
configurations, but we do not show that it is a sufficient statistic for
coverage loss. Corollary 2 is proved for the HCP/Dunn family only (§3.3), and the
hierarchical constructions are not compared with one another [A0b]. For PTB-XL
the verdict is exhaustive only with respect to the declared sources {patient,
site, nurse, device}, which the data cannot verify, and the merging of joined
partitions into a giant component is already known [P2]. Declaring only
{patient, site} yields $K_1=34$ on the full calibration fold and makes
$\alpha=0.05$ feasible, yet 31 of these blocks consist entirely of 188 records
without nurse metadata, and on the 1,960 fully annotated records the same
declaration yields $K_1=3$. The result is therefore stated conditionally: *if
patient, site, nurse, and device are all treated as dependence sources, no
admissible calibration grouping exists at any conventional $\alpha$.* Lastly,
what ECG networks learn [F6] and how well they discriminate on benchmarks [F1]
are orthogonal to the present question: an accurate model calibrated on too few
blocks still carries no guarantee.

**Researcher degrees of freedom.** Our interpretation of the MIT-BIH evidence
changed three times before settling, each change prompted by an added control
rather than by rereading existing data (Appendix B). Three analyses were
introduced or modified after results had been seen, and every one of them made
the evidence stricter. The permutation control overturned a criterion that had
favored our hypothesis; the Holm correction, which the frozen analysis plan
required but which was not applied at first, removed the last significant level
for ResNet1D-34; and the reporting axis was chosen after ICC had failed to place
the two datasets on one scale. The factor $1+(H-1)\rho$ already appeared in our
theoretical notes before data collection, and $H$ follows from the variance in
§3.2 instead of being selected, but the decision to report on this axis was taken
with the results in view. The protocol is accompanied by a complete deviation
log.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Dipertahankan | Semua butir §6.4 dan angka: 64–68%, 1,43 pp, 15/7 detak Q, $K_1(Q)=2$, 0,37–0,38, 4 rekaman validasi, 1989–1996, 22 rekaman, 0,35 → 0,19–0,20, 34 / 31 / 188 / 1.960 / 3 |
| Kata per kata | Kalimat kondisional PTB-XL (klaim inti, tidak boleh bergeser maknanya) |
