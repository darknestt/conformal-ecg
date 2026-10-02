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
statements have no finite per-label threshold at $\alpha=0.05$. On MIT-BIH, naive
split conformal falls 1.5–2.4 percentage points short of a matched permutation
null; a factorial design traces the shortfall to clustering rather than to
unequal block sizes, and a controlled dose–response experiment shows it growing
with the design effect (Spearman 0.80–0.85). PTB-XL shows no deficit despite a
within-patient correlation of 0.35, since most of its patients contribute one
recording. The apparent advantage of HCP over naive calibration is largely
mechanical, retaining 75–110% of its size once dependence is removed. The
direction of every result holds across three backbones, one of which fails the
pre-registered significance criterion. Blocks, not records, should be counted
before any claim of distribution-free coverage is made on clinical data.

**Index Terms** — Conformal prediction, electrocardiography, uncertainty
quantification, hierarchical data, exchangeability, calibration, study design.

---

## 7. Conclusion

For clinical ECG data, whether a distribution-free coverage guarantee exists is
settled by the study design before the model plays any part. HCP can deliver one
at a given error rate only if enough calibration blocks remain once the declared
dependence sources are respected — a count that metadata provide before
enrollment and that tends to be smallest for the rare diagnoses where calibrated
uncertainty matters most. Whether ignoring blocks costs coverage is governed by
the amount of repetition inside blocks, not by the strength of correlation.
Evaluations of hierarchical conformal methods should therefore use a null that
removes dependence but keeps block geometry, and should report set size next to
coverage; clinical studies that claim conformal guarantees should report the
dependence sources they declared and the number of calibration blocks, per label
where relevant. These conclusions are limited to one method family and to the
sources declared here, and whether other block-level procedures face the same
boundary is an open question.

---

## Catatan penyusunan

| Hal | Sumber |
|---|---|
| 1,5–2,4 pp | Tabel 5.4 baris SmallECGNet (1,49 / 2,21 / 2,37) |
| Spearman 0,80–0,85 | Tabel 5.5 baris DEff (0,84 / 0,80 / 0,85) |
| 75–110% | Porsi mekanis lintas tiga backbone (§5.3, §5.5) |
| "one of which fails" | ResNet1D-34, Holm 0/3 (Tabel 5.4) |
