# §9 Discussion

> **v3 — 2026-10-02.** Ditulis ulang dan dipadatkan (1.475 → ±1.000 kata). §9.1 lama, yang mengulang hasil §8, diganti satu paragraf tafsir. Struktur: apa yang dipelajari → mengapa penting → jebakan evaluasi → implikasi praktis → kaitan literatur → yang tidak dibuktikan. Versi sebelumnya: `sec9-draft.md` di riwayat git (commit 9098746).

---

## 9. Discussion

### 9.1 What the audit shows

The audit separates two questions that are usually asked together: whether a
block-level coverage guarantee *can* be enforced on a clinical dataset, and
whether ignoring the block structure *costs* coverage when it is not. The first
is combinatorial and is settled from metadata; on public ECG resources its answer
is more restrictive than their size suggests, because declared sources collapse
under the join and rare labels are carried by few patients (§8.1). A further
example follows directly from Proposition 1: dividing the 22 evaluation subjects
of the canonical MIT-BIH partition evenly between calibration and test gives
$K_1=11$, so no subject-level guarantee at the 95% level is attainable under that
design, whatever the model or the number of beats per record. The second
question is statistical, and its answer depends on how much repetition the
blocks contain rather than on how strongly observations within them are
correlated (§8.3–§8.4).

### 9.2 Why a strongly correlated dataset can be harmless

PTB-XL's patient-level ICC of 0.35 is comparable to that of a MIT-BIH
configuration with a positive mean deficit, yet PTB-XL shows none. Dependence
harms calibration only through repetition: with $H=1.05$, the factor
$1+(H-1)\rho$ stays near 1 whatever $\rho$ is. Measuring correlation alone would
suggest that PTB-XL needs block-level calibration; counting repeats shows,
correctly for marginal coverage at these levels, that it does not. Both numbers
should therefore be reported, and neither is a property of the dataset alone,
since $K_1$ depends on the split design and $\rho$ on the model producing the
scores (§6.1). The design effect is used here only as an ordering axis, a
heuristic under a compound-symmetric model (§5.1); a principled effective sample
size for thresholds under clustering is derived in [P1].

### 9.3 A pitfall in evaluating hierarchical conformal methods

The most transferable lesson concerns evaluation rather than ECG. Run on the same
data, HCP appears to "restore" coverage that naive split conformal loses, yet
75–110% of that gap survives when within-block dependence is permuted away
(§8.3, §8.5). By placing mass $1/(K_1+1)$ at $+\infty$, the finite-block
correction pushes HCP to a higher empirical quantile whether or not the data are
dependent, and with small $K_1$ — precisely where block-level calibration matters
— this mechanical inflation dominates. Below $\alpha_{\min}$ the comparison is
degenerate, because HCP covers by returning every label (Fig. 4). A claim that a
hierarchical method improves coverage should therefore be tested against a null
that preserves block sizes and score marginals while removing dependence, and
coverage should be reported with set size, since abstention is the cheapest way
to cover.

### 9.4 Implications for clinical ECG studies

Studies that intend to attach distribution-free guarantees to ECG classifiers can
complete four checks before data are collected or split:

1. **Declare dependence sources** — patient, device, site, operator, monitoring
   episode — and check that each is documented. Where it is not, as for patient
   identity in the PhysioNet/CinC Challenge 2021 collection (§6.4), the number of
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
calibration–test boundary, where
a split that is inter-patient for training can still leave too few subjects in
calibration.

### 9.5 Relation to prior work

Lee et al. pose the trade-off between many small and few large groups as an open
question for study design [A0]; our results address its most elementary part,
since whether a finite threshold exists depends on the number of groups alone
(Proposition 1). For exchangeable data, the empirical coverage of split conformal
prediction has a universal distribution that yields a minimum calibration size
[A9]; the feasibility bound plays the analogous role under hierarchical
dependence, with blocks in place of points. Rare classes are known to starve
class-conditional calibration under exchangeability [A12]; under block dependence
the count that matters is the number of blocks carrying the class, and the
condition is necessary but not sufficient (§5.3).

Our findings converge with those of Sim and Kim on ECG false-alarm control [E6]:
in both settings the guarantee is carried by subjects rather than beats, and too
few calibration subjects break it. The audit differs in what it counts and in how
it attributes the effect. It counts blocks under crossed dependence sources and
per diagnostic label, and it separates dependence from block-size imbalance and
from the mechanical effect of the finite-block correction, using a matched
permutation null and a factorial design. Evidence that marginal coverage can hide
per-class and per-patient failures in cardiac monitoring [E8] is consistent with
the label-level boundary of §8.1. Risk-control extensions of conformal prediction
[C1], [C2] and its time-series variants [C4] rest on related exchangeability or
stationarity assumptions; whether their block-level counterparts face the same
boundary is a natural question that we leave open.

### 9.6 What this study does not establish

The audit concerns marginal and label-wise coverage within one method family,
and several conclusions should not be drawn from it. It does not show that every
block-level conformal procedure shares the feasibility boundary of HCP, since
Corollary 2.2 is proved for the HCP/Dunn family only. It does not show that the
dependence sources declared for PTB-XL are the true ones; the collapse of the
join is conditional on that declaration. It does not show that the design effect
is a sufficient statistic for coverage loss; it orders configurations, and the
dose–response gradient is controlled within one dataset. It does not compare
hierarchical constructions with one another [A0b], does not address temporal
dependence within a patient across visits, and does not establish a significant
MIT-BIH deficit for every backbone. Finally, explanations of what ECG networks
learn [F6] and benchmark discrimination [F1] are orthogonal to the question asked
here: a highly accurate model calibrated on too few blocks still has no
guarantee. Threats to the validity of each result are assessed in §10.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Dibuang | §9.1 lama: ringkasan ulang 2.183 rekaman, 24/44, Tabel 8.4, faktorial, Fig. 5, §8.5 — semuanya sudah di §8. Diganti tafsir satu paragraf. Angka $K_1=11 \Rightarrow 1/12$ dipertahankan karena tidak ada di §8 dalam bentuk ini |
| Sitasi | Semua kode §9 lama tetap ada: A0, A0b, A9, A12, C1, C2, C4, D4, E5, E6, E8, F1, F2, F3, F5, F6, F10, P1 |
| Rujukan [F5] | Masih tingkat judul saja — teks penuh wajib dibaca sebelum submit (R6) |
