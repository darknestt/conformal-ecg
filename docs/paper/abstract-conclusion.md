# Abstract & §7 Conclusion

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0). Semua angka dan klaim tetap.

---

## Abstract

Conformal prediction guarantees finite-sample coverage only when calibration and
test data are exchangeable, a condition that repeated recordings, segments and
beats from the same patient violate. Hierarchical conformal prediction (HCP)
recovers the guarantee by calibrating over blocks, yet its threshold exists only
for target error rates of at least $1/(K_1+1)$, with $K_1$ the number of
calibration blocks. We audit three public electrocardiogram resources to ask
whether this guarantee can be enforced and whether ignoring blocks costs
coverage. Using metadata alone, the feasibility analysis finds that declaring the
four documented dependence sources of PTB-XL leaves a single admissible
calibration block, and that under patient blocking 24 of 44 diagnostic
statements have no finite per-label threshold at $\alpha=0.05$. Across repeated
splits of the 22 MIT-BIH evaluation subjects, naive split conformal covers
1.5–2.4 percentage points less than a matched permutation null; a factorial
design attributes the shortfall mainly to clustering, and a controlled
dose–response experiment shows it growing with the design effect (rank
correlation 0.80–0.85 over 12 configurations, 11 of them synthetic). A jackknife
over subjects, however, cannot resolve the sign of this deficit: the scarcity of
blocks that limits the guarantee also limits the evidence. PTB-XL shows no
deficit despite a within-patient correlation of 0.35, consistent with most of its
patients contributing one recording. The apparent advantage of HCP over naive
calibration is largely mechanical, retaining 75–110% of its size once dependence
is removed. Blocks, not records, should be counted, and subjects, not splits,
resampled, before claims about distribution-free coverage are made on clinical
data.

**Index Terms** — Conformal prediction, electrocardiography, uncertainty
quantification, hierarchical data, exchangeability, calibration, study design.

---

## 7. Conclusion

For clinical ECG data, whether a distribution-free coverage guarantee exists is
settled by the study design before the model plays any part. HCP can deliver one
at a given error rate only if enough calibration blocks remain once the declared
dependence sources are respected — a count that metadata provide before
enrollment and that tends to be smallest for the rare diagnoses where calibrated
uncertainty matters most. Whether ignoring blocks costs coverage depended on
repetition as well as on correlation: with near-singleton blocks even substantial
correlation left coverage intact, while with thousands of beats per subject a
deficit appeared on the audited subjects that 22 of them were too few to
establish for the population. Evaluations of conformal methods on clustered data
should therefore use a null that removes dependence but keeps block geometry,
report set size next to coverage, and resample subjects rather than splits when
a population claim is made; clinical studies that claim conformal guarantees
should report the dependence sources they declared and the number of
calibration blocks, per label where relevant. These conclusions are limited to
HCP and to the sources declared here, and whether other block-level procedures
face the same boundary is an open question.

---

## Catatan penyusunan

| Hal | Sumber |
|---|---|
| 1,5–2,4 pp | Tabel 5.4 baris SmallECGNet (1,49 / 2,21 / 2,37) |
| Spearman 0,80–0,85 | Tabel 5.5 baris DEff (0,84 / 0,80 / 0,85) |
| 75–110% | Porsi mekanis lintas tiga backbone (§5.3, §5.5) |
| "one of which fails" | ResNet1D-34, Holm 0/3 (Tabel 5.4) |
