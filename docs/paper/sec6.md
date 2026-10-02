# §6 Discussion

> **v4 — 2026-10-02.** Menggabungkan §9 Discussion dan §10 Threats to Validity (v3). Enam subbab Diskusi → empat; enam subbab Threats → satu subbab §6.4 dengan judul paragraf per jenis ancaman. Semua ancaman v3 tetap; §9.6 ("what this study does not establish") dilebur ke §6.4 tanpa duplikasi; Tabel 10.1 → Lampiran B. Versi sebelumnya: `sec9.md`, `sec10.md` di commit fa8c5f3.

---

## 6. Discussion

### 6.1 Main findings

The audit separates two questions that are usually asked together: whether a
block-level coverage guarantee *can* be enforced on a clinical dataset, and
whether ignoring the block structure *costs* coverage when it is not. The first
is combinatorial and is settled from metadata; on public ECG resources its answer
is more restrictive than their size suggests, because declared sources collapse
under the join and rare labels are carried by few patients (§5.1). A further
example follows directly from Proposition 1: dividing the 22 evaluation subjects
of the canonical MIT-BIH partition evenly between calibration and test gives
$K_1=11$, so no subject-level guarantee at the 95% level is attainable under that
design, whatever the model or the number of beats per record.

The second question is statistical, and its answer depends on how much
repetition the blocks contain rather than on how strongly observations within
them are correlated (§5.3–§5.4). PTB-XL's patient-level ICC of 0.35 is comparable
to that of a MIT-BIH configuration with a positive mean deficit, yet PTB-XL shows
none. Dependence harms calibration only through repetition: with $H=1.05$, the
factor $1+(H-1)\rho$ stays near 1 whatever $\rho$ is. Measuring correlation alone
would suggest that PTB-XL needs block-level calibration; counting repeats shows,
correctly for marginal coverage at these levels, that it does not. Both numbers
should therefore be reported, and neither is a property of the dataset alone,
since $K_1$ depends on the split design and $\rho$ on the model producing the
scores (§4.1). The design effect is used here only as an ordering axis, a
heuristic under a compound-symmetric model (§3.2); a principled effective sample
size for thresholds under clustering is derived in [P1].

### 6.2 A pitfall in evaluating hierarchical conformal methods

The most transferable lesson concerns evaluation rather than ECG. Run on the same
data, HCP appears to "restore" coverage that naive split conformal loses, yet
75–110% of that gap survives when within-block dependence is permuted away
(§5.3, §5.5). By placing mass $1/(K_1+1)$ at $+\infty$, the finite-block
correction pushes HCP to a higher empirical quantile whether or not the data are
dependent, and with small $K_1$ — precisely where block-level calibration matters
— this mechanical inflation dominates. Below $\alpha_{\min}$ the comparison is
degenerate, because HCP covers by returning every label (Fig. 4). A claim that a
hierarchical method improves coverage should therefore be tested against a null
that preserves block sizes and score marginals while removing dependence, and
coverage should be reported with set size, since abstention is the cheapest way
to cover.

### 6.3 Implications and relation to prior work

Studies that intend to attach distribution-free guarantees to ECG classifiers can
complete four checks before data are collected or split:

1. **Declare dependence sources** — patient, device, site, operator, monitoring
   episode — and check that each is documented. Where it is not, as for patient
   identity in the PhysioNet/CinC Challenge 2021 collection (§4.1), the number of
   blocks becomes an assumption rather than a count.
2. **Count blocks, not records**, in the calibration set, for the grouping that
   respects every declared source, and compare the count with
   $\lceil 1/\alpha\rceil-1$.
3. **Repeat the count per label** for any label-conditional claim, using
   $\lceil m/\alpha\rceil-1$ for simultaneous claims across $m$ labels. Rare
   diagnoses typically fail first.
4. **Estimate the repetition**, through the harmonic mean block size, before
   deciding whether block-level calibration is needed for marginal coverage.

The same counting applies whenever coverage is conditioned on groups of patients:
when group-conditional calibration, proposed to equalize coverage across
demographic groups [D4], must also respect patient blocks, a group with few
patients in calibration is bounded exactly as rare labels are here. Settings with
thousands of blocks, such as patients nested in hospitals [E5], sit far from the
boundary, which is why it is easy to overlook. The inter-patient protocol exists
to prevent subject-level leakage between training and evaluation [F2], [F3],
[F10], and inter-patient, intra-patient and patient-specific training regimes
have been compared directly [F5]; the audit carries the same concern to the
calibration–test boundary, where a split that is inter-patient for training can
still leave too few subjects in calibration.

For the study-design trade-off that Lee et al. leave open [A0], our results
settle the most elementary part: whether a finite threshold exists depends on the
number of groups alone (Proposition 1). For exchangeable data, the empirical
coverage of split conformal prediction has a universal distribution that yields
a minimum calibration size [A9]; the feasibility bound plays the analogous role
under hierarchical dependence, with blocks in place of points. Rare classes are
known to starve class-conditional calibration under exchangeability [A12]; under
block dependence the count that matters is the number of blocks carrying the
class, and the condition is necessary but not sufficient (§3.4).

Our findings converge with those of Sim and Kim on ECG false-alarm control [E6]:
in both settings the guarantee is carried by subjects rather than beats, and too
few calibration subjects break it. The audit differs in what it counts and in how
it attributes the effect. It counts blocks under crossed dependence sources and
per diagnostic label, and it separates dependence from block-size imbalance and
from the mechanical effect of the finite-block correction, using a matched
permutation null and a factorial design. Evidence that marginal coverage can hide
per-class and per-patient failures in cardiac monitoring [E8] is consistent with
the label-level boundary of §5.1. Risk-control extensions of conformal prediction
[C1], [C2] and its time-series variants [C4] rest on related exchangeability or
stationarity assumptions; whether their block-level counterparts face the same
boundary is a natural question that we leave open.

### 6.4 Limitations and threats to validity

The audit concerns marginal and label-wise coverage within one method family.
We group the threats to its conclusions by type.

**Internal validity.** Cardiologists validated only 64–68% of PTB-XL records in
folds 1–8, against 100% in folds 9 and 10. An early version of the study that
calibrated on fold 8 and evaluated on fold 9 found an apparent 1.43
percentage-point deficit at $\alpha=0.05$, which turned out to reflect the shift
in label quality between folds rather than block dependence; confirmatory
analyses therefore use fold 9, and fold 10 has not been examined. Each
data-handling decision in §4.1 guards against a failure that raises no error
(unlabelled records, channel order in record 114, boundary beats, the subject
shared by records 201 and 202), and all preprocessing is fitted on training data
only.

**Construct validity.** MIT-BIH class Q has 15 beats in total, 7 of them in two
evaluation records, so per-class statistics for Q cannot be interpreted; we
report $K_1(\mathrm{Q})=2$, i.e. $\alpha_{\min}=1/3$, so that the boundary is
visible rather than averaged away. Because conformal guarantees are
model-agnostic, a weak model widens prediction sets without reducing coverage.
Our primary backbones fall below published PTB-XL benchmarks [F1] and are weak on
MIT-BIH minority classes (balanced accuracy 0.37–0.38 for all three backbones),
so their discrimination bears on set size rather than on coverage, a reading
tested on two larger networks (§5.5). With 4 validation records, early stopping
chose epoch 1 for ResNet1D-50 on MIT-BIH; the pre-registered last-epoch analysis
preserved the sign of every deficit and every $K_1$ but not the magnitude, which
we therefore do not compare across backbones.

**External validity.** PTB-XL was recorded at one institution between 1989 and
1996; its device, nurse and site metadata make the block analysis possible, but
its estimates of $\rho$ and $H$ need not transfer to contemporary multi-center
cohorts. Eleven of the twelve dose–response points are synthetic MIT-BIH
configurations obtained by reassigning beats between records; only the twelfth,
PTB-XL, is observed. The combined correlation is thus driven by an intervention
within one dataset rather than by naturally differing cohorts, and PTB-XL —
different in modality, task and block type — serves only as a prediction check
that lands where the design effect predicts. All MIT-BIH intervals come from
repeated splits of the same 22 DS2 records, so they quantify variability across
splits, not across the patient population. All results concern ECG, and temporal
dependence within a patient across visits is not addressed; other clinical
signals with repeated measurements are plausible candidates for the same
analysis but were not examined.

**Statistical conclusion validity.** No single split and no single dose–response
point establishes a deficit: split-to-split ranges contain $1-\alpha$ in every
MIT-BIH cell (Table 5.3), and every per-point interval in the dose–response
analysis contains zero. The evidence lies in the comparison with a permutation
null and in the monotone trend, which are what the pre-registered tests address.
After Holm correction the deficit against the permutation null is significant at
every level for two of three backbones and at none for ResNet1D-34 (Table 5.4);
the pre-registered criterion fails for that backbone, and we claim invariance of
direction only. Coverage alone overstates HCP, which at $\alpha=0.10$ on MIT-BIH
reaches 0.9615 with 2.43 of 5 labels per beat and below $\alpha_{\min}$ covers by
abstaining; both quantities are reported throughout. Two pre-registered criteria
did not survive. "HCP covers better than split conformal" was withdrawn once the
permutation control showed the gap to be largely mechanical (§5.3). A Spearman
test across datasets could not be run as written, because with two datasets the
rank correlation can only be $\pm1$; it was replaced by a test over design-effect
points within MIT-BIH. Both changes are logged as deviations.

**Theoretical scope.** The variance in §3.2 and the design effects (6) rest on
Assumption (A), a one-way random-effects model with compound symmetry, whereas
Proposition 1, Corollary 2 and Proposition 3 are distribution-free. The variance
concerns the correlation of the coverage indicator rather than of raw scores;
with the indicator correlation every Spearman coefficient remains significant
(Table 5.5), and PTB-XL's correlation falls from 0.35 to 0.19–0.20 while its
design effect stays near 1. The design effect orders configurations; we do not
show that it is a sufficient statistic for coverage loss. Corollary 2 is proved
for the HCP/Dunn family only (§3.3), and hierarchical constructions are not
compared with one another [A0b]. On PTB-XL the verdict is exhaustive only for the
declared sources {patient, site, nurse, device}, which cannot be verified from
data; the collapse of joined partitions into a giant component is itself known
[P2]. Declaring only {patient, site} gives $K_1=34$ on the full calibration fold
and makes $\alpha=0.05$ feasible, but 31 of those blocks consist solely of 188
records lacking nurse metadata, and on the 1,960 records with complete metadata
the same declaration gives $K_1=3$. We therefore state the result conditionally:
*if patient, site, nurse, and device are all treated as dependence sources, no
admissible calibration grouping exists at any conventional $\alpha$.* Finally,
explanations of what ECG networks learn [F6] and benchmark discrimination [F1]
are orthogonal to the question asked here: a highly accurate model calibrated on
too few blocks still has no guarantee.

**Researcher degrees of freedom.** Our reading of the MIT-BIH evidence changed
three times before it stabilized, each time after a control was added rather than
after existing data were reinterpreted (Appendix B). Three analyses were added or
changed after results were seen, and each tightened the evidence. The
permutation control invalidated a criterion that had favored our hypothesis. The
Holm correction, required by the frozen analysis plan but not initially applied,
removed the one remaining significant level for ResNet1D-34. The reporting axis
was adopted after ICC failed to unify the two datasets; the factor
$1+(H-1)\rho$ was already in our theoretical notes before the data were
collected, and $H$ follows from the variance in §3.2 rather than being chosen,
but the decision to report on that axis was made with the results in view. A
complete deviation log accompanies the protocol.

---

## Catatan penyusunan

| Asal (v3) | Tujuan (v4) |
|---|---|
| §9.1 + §9.2 | §6.1 (dua paragraf) |
| §9.3 | §6.2 utuh (jebakan evaluasi tetap subbab sendiri — kontribusi yang paling dapat dipindahkan) |
| §9.4 + §9.5 | §6.3; kalimat Lee et al. dipadatkan karena §2.1 sudah mengutip pertanyaannya kata per kata |
| §9.6 | Dilebur ke §6.4: Kor. 2 HCP/Dunn saja, sumber dideklarasikan, DEff bukan statistik cukup, gradien satu dataset, [A0b], dependensi temporal, ResNet1D-34, [F6]/[F1] — semuanya ada, tanpa ganda |
| §10.1–10.5 | §6.4 Internal / Construct / External / Statistical / Theoretical scope — semua butir dan angka utuh |
| §10.6 paragraf | §6.4 "Researcher degrees of freedom" |
| §10.6 Tabel 10.1 + kalimat "second stage was our own error" (24.800 vs 16.500) | Lampiran B |
| Kalimat miring ruang lingkup Kor. 2.2 di §10.5 | Tidak diulang; bentuk lengkapnya di §3.3 "Scope of Corollary 2" |
