# §9 Discussion — Draft

> **Status:** 🟢 DRAF PROSA · **Ditulis:** 2026-10-02, **sesudah** seluruh hasil §8 terkunci.
> Setiap angka dirujuk ke §8 atau ke berkas di `results/raw/`. Tidak ada klaim baru yang tidak punya baris di §8.

---

## 9. Discussion

### 9.1 What the audit establishes

The audit separates two questions that are usually merged: *can* a block-level
coverage guarantee be enforced on a given clinical dataset, and *does* ignoring
the block structure cost coverage when it is not enforced. The first question is
combinatorial. It is answered from metadata, before any model is trained, and
its answers on public ECG resources are more restrictive than their size
suggests. The second question is statistical, and its answer depends on how much
repetition the blocks contain rather than on how strongly observations within a
block are correlated.

On the first question, three results stand out. PTB-XL fold 9 holds 2,183
records, yet once its four documented dependence sources are all declared, every
admissible calibration grouping collapses to a single block (§8.1). At the label
level, 24 of 44 SCP statements cannot receive a finite per-label threshold at
$\alpha=0.05$ even under patient-level blocking alone, because fewer than 19
calibration patients carry them (Table 8.2, Fig. 3). And on MIT-BIH, dividing
the 22 evaluation subjects of the canonical inter-patient partition evenly
between calibration and test gives $K_1=11$ and therefore $\alpha_{\min}=1/12$:
no subject-level guarantee at the conventional 95% level is attainable under
that design, regardless of the model or the number of beats per record. None of
these statements involves sampling error.

On the second question, naive split conformal under-covers on MIT-BIH relative
to a permutation null that preserves everything except within-record dependence
(Table 8.4), and the factorial decomposition attributes the deficit to clustering
rather than to block-size imbalance (§8.3). The deficit scales with the design
effect (Fig. 5), and PTB-XL — where most patients contribute a single record —
shows none. The direction of this contrast is stable across a more than
hundredfold range of backbone capacity and across checkpoints; its statistical
strength is not (§8.5).

### 9.2 Why a strongly correlated dataset can be harmless

PTB-XL's patient-level ICC of 0.35 is comparable to that of a MIT-BIH
configuration with a positive mean deficit, yet PTB-XL shows none. The resolution is
that dependence harms calibration only through repetition: with a harmonic mean
block size of $H=1.05$, the design effect $1+(H-1)\rho$ stays near 1 whatever
$\rho$ is. A practitioner who measured the correlation alone would conclude that
PTB-XL requires block-level calibration; one who counted repeats would conclude,
correctly for marginal coverage at these levels, that it does not. The practical
reading is that two numbers must be reported together — how correlated
observations within a block are, and how many observations a typical block
contributes — and that neither is a property of the dataset alone: $K_1$ depends
on the split design, and $\rho$ on the model producing the scores (§6.1).

We use the design effect only as an ordering axis. It is a heuristic under a
compound-symmetric model (§5.1), and a principled effective sample size for
thresholds under clustering has been derived separately [P1]. The ordering is
what the dose–response analysis tests, and it holds on both raw-score and
indicator correlations (Table 8.5).

### 9.3 A pitfall in evaluating hierarchical conformal methods

The most transferable lesson of the audit concerns evaluation rather than
ECG. Comparing HCP with naive split conformal on the same data appears to show
that HCP "restores" coverage. Our permutation control shows that 75–110% of that
gap survives when within-block dependence is destroyed (§8.3, §8.5). The finite
block correction places mass $1/(K_1+1)$ at $+\infty$ and thereby forces HCP to a
higher empirical quantile whether or not the data are dependent. With small
$K_1$ — exactly the regime in which block-level calibration matters — this
mechanical inflation dominates. Below $\alpha_{\min}$ the comparison is
degenerate: HCP attains perfect coverage by returning every label (Fig. 4).

Two practices follow. A claim that a hierarchical method improves coverage should
be tested against a null that preserves block sizes and score marginals while
removing dependence, rather than against the naive baseline alone. And coverage
should always be reported jointly with set size, since abstention is the cheapest
way to cover.

### 9.4 Implications for clinical ECG studies

For studies that intend to attach distribution-free guarantees to ECG
classifiers, the audit suggests a short checklist that can be completed before
data are collected or split:

1. **Declare dependence sources** — patient, device, site, operator, monitoring
   episode — and check whether each is documented in the metadata. Where it is
   not, as for patient identity in the PhysioNet/CinC Challenge 2021 collection
   (§6.4), the number of blocks becomes an assumption rather than a count.
2. **Count blocks, not records**, in the calibration set, for the grouping that
   respects every declared source, and compare with $\lceil 1/\alpha\rceil-1$.
3. **Repeat the count per label** for any label-conditional claim, and for
   simultaneous claims across $m$ labels use $\lceil m/\alpha\rceil-1$. Rare
   diagnoses will typically fail first.
4. **Estimate the repetition** — the harmonic mean block size — before deciding
   whether block-level calibration is needed for marginal coverage.

The same counting applies wherever conditional coverage is sought over groups of
patients. Group-conditional conformal prediction has been proposed to equalize
coverage across demographic groups [D4]; when calibration must also respect
patient blocks, a group that contains few patients in calibration is bounded in
exactly the way rare labels are here. Conversely,
hierarchical healthcare settings with thousands of blocks, such as admissions
nested in hospitals [E5], sit far from the boundary, which is why the boundary is
easy to overlook.

The inter-patient protocol for heartbeat classification exists precisely to
prevent subject-level leakage between training and evaluation [F2], [F3], [F10],
and the consequences of inter-patient, intra-patient and patient-specific
training regimes have been compared directly [F5]. The present audit extends the
same concern one step further, from the training–evaluation boundary to the
calibration–test boundary: a split that is inter-patient for training purposes
can still leave too few subjects in calibration for the guarantee one intends to
report.

### 9.5 Relation to prior work

Lee et al. identify the trade-off between many small groups and few large groups
as an open question for study design in this setting [A0]. Our results address
its most elementary part: whether a finite threshold exists at all, which depends
on the number of groups alone (Proposition 1), and when the number of repeats
starts to matter for coverage, which depends on the design effect (§8.4). In the
exchangeable case, the distribution of empirical coverage of split conformal
prediction is universal and depends only on the miscoverage level and the
calibration size, which yields a criterion for the minimum calibration size [A9].
Our feasibility bound plays the analogous role under hierarchical dependence,
with the number of calibration blocks in place of the number of calibration
points. Class-conditional calibration is known to be starved by rare classes
under exchangeability [A12]; under block dependence the unit that must be counted
becomes the number of blocks carrying the class, and the condition we state is
necessary but not sufficient (§5.3).

Risk-control extensions of conformal prediction [C1], [C2] and its time-series
variants [C4] rest on related exchangeability or stationarity assumptions.
Whether their block-level counterparts are subject to the same feasibility
boundary is a natural question that we do not address.

### 9.6 Limitations of scope

The audit concerns marginal and label-wise coverage of a single method family.
It does not compare hierarchical constructions with one another [A0b], does not
address temporal dependence within a patient across visits, and uses two
datasets whose dependence structures differ along one axis. Post hoc explanation
of what ECG networks learn [F6] and benchmark discrimination [F1] are orthogonal
to the question asked here: a highly accurate model calibrated on too few blocks
remains without a guarantee. The threats to validity of each result are
detailed in §10.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Sumber angka | Semua dirujuk ke §8. Angka baru di bagian ini: $K_1=11 \Rightarrow \alpha_{\min}=1/12$ (aritmetika dari Prop. 1, `control_permutation_mitdb.json` `k1=11`); 2.183 rekaman fold 9 (`feasibility_alpha.json`) |
| Rujukan baru | [A9] (abstrak arXiv:2303.02770 dibaca: distribusi cakupan empiris universal, bergantung hanya pada $\alpha$ dan ukuran kalibrasi); [D4] (abstrak OpenAlex: group-conditional CP untuk keadilan cakupan); [E5] (abstrak arXiv: 61.538 admisi di 3.793 rumah sakit, kalibrasi sadar-grup); [C2] (abstrak: perluasan CP ke kendali loss, di bawah exchangeability); [F6] (abstrak: atribusi penjelas pada PTB-XL); [F5] **hanya judul** — abstrak tidak tersedia di Crossref/OpenAlex, jadi kalimatnya dibatasi pada apa yang dinyatakan judul |
| Yang sengaja TIDAK diklaim | (1) bahwa batas kelayakan berlaku untuk risk control — dinyatakan sebagai pertanyaan terbuka; (2) bahwa PTB-XL "tidak butuh" kalibrasi blok untuk cakupan bersyarat-label; (3) superioritas atas metode lain |
| §9.3 | Kontribusi metodologis yang paling mudah dipindahkan ke bidang lain — layak disebut di Abstract dan §1 |
