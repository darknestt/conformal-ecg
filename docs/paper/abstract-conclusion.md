# Abstract & §7 Conclusion

> **v3 — 2026-10-02.** Ditulis ulang dan dipadatkan (Abstract 247 → ±220 kata). Versi sebelumnya: `abstract-conclusion-draft.md` di riwayat git (commit 9098746).

---

## Abstract

Conformal prediction gives finite-sample coverage guarantees only when
calibration and test data are exchangeable, an assumption that repeated
recordings, segments and beats from the same patient break. Hierarchical
conformal prediction (HCP) restores the guarantee by calibrating over blocks, but
its threshold is finite only if the target error rate is at least $1/(K_1+1)$,
where $K_1$ is the number of calibration blocks. We audit whether this guarantee
can be enforced on three public electrocardiogram resources, and whether ignoring
blocks costs coverage. Computed from metadata alone, the feasibility analysis
shows that declaring all four documented dependence sources of PTB-XL collapses
every admissible calibration grouping to a single block, and that 24 of 44
diagnostic statements admit no finite per-label threshold at $\alpha=0.05$ under
patient blocking. On MIT-BIH, naive split conformal under-covers a matched
permutation null by 1.5–2.4 percentage points; a factorial design attributes the
deficit to clustering rather than to unequal block sizes, and in a controlled
dose–response experiment the deficit rises with the design effect (Spearman
0.80–0.85). PTB-XL shows no deficit despite a within-patient correlation of 0.35,
because most patients contribute a single recording. The apparent advantage of
HCP over naive calibration is largely mechanical: it persists at 75–110% of its
size when dependence is removed. Directions hold across three backbones, one of
which fails the pre-registered significance criterion. Counting blocks, not
records, should precede any claim of distribution-free coverage on clinical data.

**Index Terms** — Conformal prediction, electrocardiography, uncertainty
quantification, hierarchical data, exchangeability, calibration, study design.

---

## 7. Conclusion

On clinical ECG data, a distribution-free coverage guarantee is a property of the
study design before it is a property of the model. Whether HCP can deliver one at
a given error rate depends on how many calibration blocks respect the declared
dependence sources, a number computable from metadata before enrollment and often
smallest for the rare diagnoses where calibrated uncertainty matters most.
Whether ignoring blocks costs coverage depends on how much repetition the blocks
contain rather than on how correlated they are. Evaluations of hierarchical
conformal methods should compare against a null that removes dependence while
preserving block geometry and report set size with coverage, and clinical studies
claiming conformal guarantees should report the number of calibration blocks,
per label where relevant, with the dependence sources they declared. These
conclusions concern one method family and the sources declared here; whether
other block-level procedures share the same boundary remains open.

---

## Catatan penyusunan

| Hal | Sumber |
|---|---|
| 1,5–2,4 pp | Tabel 5.4 baris SmallECGNet (1,49 / 2,21 / 2,37) |
| Spearman 0,80–0,85 | Tabel 5.5 baris DEff (0,84 / 0,80 / 0,85) |
| 75–110% | Rasio mekanis lintas tiga backbone (§5.3, §5.5) |
| "one of which fails" | ResNet1D-34, Holm 0/3 (Tabel 5.4) |
