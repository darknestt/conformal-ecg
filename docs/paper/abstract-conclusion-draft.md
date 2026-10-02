# Abstract & §11 Conclusion — Draft

> **Status:** 🟢 DRAF PROSA · **Ditulis:** 2026-10-02, terakhir.
> Abstract ≤ 250 kata (batas IEEE JBHI / Trans.). Index Terms dari daftar IEEE Taxonomy yang umum.

---

## Abstract

Conformal prediction offers finite-sample coverage guarantees for clinical
classifiers, but only if calibration and test data are exchangeable — an
assumption that repeated recordings, segments and beats from the same patient
violate. Hierarchical conformal prediction restores a guarantee by calibrating
over blocks, yet its threshold is finite only when the target error rate is at
least $1/(K_1+1)$, where $K_1$ is the number of calibration blocks. We audit when
this guarantee can be enforced, and when ignoring blocks actually costs coverage,
on three public electrocardiogram resources. From metadata alone, before any
model is trained, declaring all four documented dependence sources in PTB-XL
collapses every admissible calibration grouping to a single block, and 24 of 44
diagnostic statements admit no finite per-label threshold at $\alpha=0.05$ under
patient blocking. On MIT-BIH, naive split conformal under-covers relative to a
matched permutation null by 1.5–2.4 percentage points; a factorial design
attributes the deficit to clustering rather than to unequal block sizes, and in
a controlled dose–response experiment it increases with the design effect
(Spearman 0.80–0.85). PTB-XL shows no deficit despite a within-patient
correlation of 0.35, because most patients contribute a single recording. The
apparent advantage of hierarchical over naive calibration persists at 75–110% of
its size when dependence is removed, and is therefore largely mechanical.
Directions hold across three backbones spanning a hundredfold range of capacity
and across checkpoints; one backbone fails the pre-registered significance
criterion, and we report it. Counting blocks, not records, should precede any
claim of distribution-free coverage on clinical data.

**Index Terms** — Conformal prediction, electrocardiography, uncertainty
quantification, hierarchical data, exchangeability, calibration, study design.

---

## 11. Conclusion

A distribution-free coverage guarantee on clinical ECG data is a property of the
study design before it is a property of the model. Whether hierarchical conformal
calibration can deliver one at a given error rate is decided by the number of
calibration blocks that respect every declared dependence source, and that number
can be computed from metadata before a single patient is enrolled. On public
resources it is often smaller than the size of the data suggests, and smallest
for the rare diagnoses where calibrated uncertainty would matter most. Whether
ignoring the block structure costs coverage is a separate question, answered by
how much repetition the blocks contain rather than by how correlated they are.
Evaluations of hierarchical conformal methods should compare against a null that
removes dependence while preserving block geometry, and should report set size
alongside coverage. We recommend that clinical studies claiming conformal
guarantees report the number of calibration blocks, per label where labels are
conditioned on, together with the dependence sources they declared. These
conclusions concern one method family and the dependence sources declared here;
whether other block-level procedures share the same boundary remains open.

---

## Catatan penyusunan

| Hal | Sumber / keputusan |
|---|---|
| Jumlah kata Abstract | dihitung saat build; target ≤ 250 |
| 1.5–2.4 pp | Defisit vs null permutasi, SmallECGNet: 1,49 / 2,21 / 2,37 (Tabel 8.4). **Hanya backbone utama**; ResNet1D-50 lebih besar (2,54–3,42), ResNet1D-34 lebih kecil dan tidak signifikan sesudah Holm — dinyatakan di kalimat "one backbone fails" |
| Spearman 0.80–0.85 | Sumbu DEff, 12 titik (Tabel 8.5 baris 2: 0,84 / 0,80 / 0,85) |
| "hundredfold range" | 101.925 → 15.964.485 = 157×; "more than hundredfold" di §1, "hundredfold" di sini (keduanya benar) |
| Kalimat terakhir Abstract | Pesan bawa-pulang; sengaja preskriptif |
