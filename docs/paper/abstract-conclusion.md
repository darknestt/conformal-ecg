# Abstract & §7 Conclusion

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0). Semua angka dan klaim tetap.
> **2026-10-03 — draf netral jurnal (arahan dosen pembimbing).** Jurnal tujuan dan template belum ditentukan. Bagian khusus jurnal/administratif (Highlights, Ethics Statement, CRediT, Competing Interest, Funding, deklarasi AI generatif, DOI arsip kode) TIDAK dimasukkan ke draf; diisi dosen saat submisi. Keywords dipertahankan (lazim di semua jurnal).

---

## Abstract

Conformal prediction guarantees finite-sample coverage only when calibration and
test data are exchangeable, which repeated recordings, segments and beats from
one patient violate. Hierarchical conformal prediction (HCP)
recovers the guarantee by calibrating over blocks, yet its threshold exists only
for target error rates of at least $1/(K_1+1)$, with $K_1$ the number of
calibration blocks. We audit three public electrocardiogram resources: can this
guarantee be enforced when several dependence sources are declared and coverage
is required per diagnosis, and does ignoring blocks cost coverage? From metadata alone, declaring the four documented dependence
sources of PTB-XL leaves a single admissible calibration block, and under patient
blocking 24 of 44 diagnostic SCP statements have no finite per-label threshold at
$\alpha=0.05$. Across repeated
splits of the 22 MIT-BIH evaluation subjects, naive split conformal covers
1.5–2.4 percentage points less than a matched permutation null (primary
backbone); a factorial
design attributes the shortfall mainly to clustering, and a controlled
dose–response experiment shows it growing with the design effect (rank
correlation 0.80–0.85 over 12 configurations, 11 of them synthetic). A jackknife
over subjects cannot resolve the sign of this deficit: the scarcity of
blocks that limits the guarantee also limits the evidence. PTB-XL, where most
patients contribute one recording, shows no deficit despite a within-patient
correlation of 0.35. Most of the coverage gap between HCP and
naive calibration is mechanical: 75–110% of it persists when dependence is
permuted away and block sizes are kept. Clinical coverage claims should count
blocks, not records, and resample subjects, not splits.

**Keywords** — Conformal prediction, electrocardiography, uncertainty
quantification, hierarchical data, exchangeability, calibration, study design.

---

## 7. Conclusion

For clinical ECG data, whether HCP can deliver a block-level coverage guarantee
is settled by the study design before any model is trained. It can do so at a
given error rate only if enough calibration blocks remain once the declared
dependence sources are respected, a count that metadata provide before
enrollment and that tends to be smallest for the rare diagnoses where calibrated
uncertainty matters most; this extends to crossed sources and diagnostic labels a
requirement already known for single groupings. Whether ignoring blocks costs
coverage depended on repetition as well as correlation: near-singleton blocks
left coverage intact despite substantial correlation, while thousands of beats
per subject produced a deficit on the 22 audited subjects that they were too few
to establish for the population. The feasibility verdicts are exact given the
declared sources; the coverage findings are observations on these records.
Evaluations of conformal methods on clustered data should use a null
that removes dependence but keeps block geometry, report set size with coverage,
and resample subjects rather than splits for population claims; clinical studies
claiming conformal guarantees should report the dependence sources they declared
and the number of calibration blocks, per label where relevant. These
conclusions are limited to HCP and the sources declared here; other hierarchical
constructions carry their own group-count conditions [A0b], and whether every
block-level procedure faces such a boundary is not addressed.

## Data and Code Availability

PTB-XL (version 1.0.3) [H2], the MIT-BIH Arrhythmia Database [H3] and the
PhysioNet/CinC Challenge 2021 collection (version 1.0.3) [H5] are publicly
available from PhysioNet under their respective licences; all recordings are
de-identified, and no new data were collected for this study. The code, the
analysis protocol with its deviation log, and the JSON artifact behind every
reported number are available at https://github.com/darknestt/conformal-ecg.

---

## Catatan penyusunan

| Hal | Sumber |
|---|---|
| 1,5–2,4 pp | Tabel 5.4 baris SmallECGNet (1,49 / 2,21 / 2,37) |
| Spearman 0,80–0,85 | Tabel 5.5 baris DEff (0,84 / 0,80 / 0,85) |
| 75–110% | Porsi mekanis lintas tiga backbone (§5.3, §5.5) |
| "one of which fails" | ResNet1D-34, Holm 0/3 (Tabel 5.4) |

**Untuk diisi dosen saat submisi (tidak ada di draf):** DOI/identitas arsip kode; pernyataan etika institusi (draf hanya menyebut data publik ter-de-identifikasi, tanpa data baru); CRediT; competing interest; funding; deklarasi penggunaan AI generatif bila jurnal mewajibkan; Highlights/graphical abstract bila jurnal memintanya.
