# §1 Introduction — Draft

> **Status:** 🟢 DRAF PROSA · **Ditulis:** 2026-10-02, **terakhir**, sesudah §8 dan §9 terkunci (sesuai `outline.md`: Introduction ditulis setelah tahu apa yang ditemukan).
> Kontribusi di bawah hanya memuat temuan yang punya baris di §8. Tidak ada kata "first" / "novel method".

---

## 1. Introduction

Deep networks for electrocardiogram (ECG) interpretation are now routinely
benchmarked on large public datasets [F1], [H1], yet a calibrated statement of
uncertainty is widely regarded as a prerequisite for their clinical use. Reviews
of uncertainty quantification in clinical deep learning [G1] and the FUTURE-AI
consensus guideline [G2] both make this point. Conformal prediction is attractive
in this setting because it converts any trained classifier into a set-valued
predictor whose coverage holds in finite samples without distributional
assumptions [A11], and it has been applied across clinical domains [E1]–[E3].

That guarantee rests on a single assumption: calibration and test observations
are exchangeable. Clinical ECG data rarely satisfy it. A patient contributes
several recordings; a Holter episode is cut into many segments; a single
recording yields thousands of beats; devices, sites and operators are shared
across patients. Observations within such a block are more alike than
observations across blocks. Exchangeability can fail in many ways, and the size
of the resulting coverage gap is bounded in general terms [A1]. For the specific
case of grouped or repeated measurements, Lee et al. have derived a hierarchical
form of exchangeability and a hierarchical conformal prediction (HCP) procedure
that restores a finite-sample guarantee by calibrating at the level of blocks
rather than observations [A0]; related constructions for two-layer hierarchical
models are given by Dunn et al. [A0b].

The remedy therefore exists. What has not been examined is whether it can be
applied to the clinical data on which it is needed. HCP assigns each calibration
block equal mass and places a further atom at $+\infty$, so its threshold is
finite only when the target error rate $\alpha$ is at least $1/(K_1+1)$, where
$K_1$ is the number of calibration blocks. Large clinical datasets can have few
blocks once every dependence source is respected, and fewer still for rare
diagnoses. At the same time, it is not obvious when ignoring block structure
actually costs coverage: a dataset in which most patients contribute a single
recording may be harmless even if the few repeated recordings are strongly
correlated. The authors of [A0] identify the trade-off between many small and
few large groups as an open question for study design.

This paper reports an empirical audit of block-level conformal calibration on
three public ECG resources: PTB-XL [H1], [H2], the MIT-BIH Arrhythmia Database
[H3], and the PhysioNet/CinC Challenge 2021 collection [H5]. The datasets were
chosen to occupy opposite ends of the space of block geometries — PTB-XL with
18,869 patients averaging 1.16 records each, MIT-BIH with 44 subjects
contributing more than 1,500 beats each — and, in the case of Challenge 2021, to
provide a resource in which the block identifier is not documented at all. We
introduce no new conformal procedure. The contributions are the following.

- **A metadata-only feasibility audit** (§5, §8.1). Combining the HCP
  feasibility bound with the join of declared dependence sources yields exact,
  pre-enrolment verdicts. On PTB-XL, declaring all four documented sources
  collapses every admissible calibration grouping to a single block, and 24 of
  44 SCP diagnostic statements cannot receive a finite per-label threshold at
  $\alpha=0.05$ under patient blocking alone. On MIT-BIH, dividing the 22
  evaluation subjects of the canonical inter-patient partition evenly between
  calibration and test cannot support a subject-level guarantee at the 95% level.
- **Evidence that block dependence, not block imbalance, drives under-coverage,
  and that it does so through repetition** (§8.2–§8.4). Naive split conformal
  under-covers on MIT-BIH relative to a matched permutation null; a factorial
  design attributes the deficit to clustering rather than to unequal block
  sizes; and the deficit increases with the design effect across twelve
  configurations, with PTB-XL falling where the design effect predicts — near
  zero — despite a substantial within-patient correlation.
- **A caution for evaluating hierarchical conformal methods** (§8.3, §9.3). The
  apparent improvement of HCP over naive split conformal is 75–110% mechanical:
  it persists when dependence is removed. We recommend matched permutation nulls
  and joint reporting of set size.
- **Pre-registered robustness checks reported in full** (§8.5, §10). The direction
  of every finding holds across three backbones spanning a more than hundredfold
  range of parameters and across checkpoints. Its statistical strength does not:
  one of three backbones fails the pre-registered significance criterion, and we
  report that failure.

All analyses use block-level resampling, a held-out PTB-XL fold that was never
examined, and a protocol whose deviations are logged. Code and per-result
artifacts are released with the paper.

The paper is organized as follows. Section 2 reviews related work. Sections 3
and 4 fix notation and state the feasibility problem. Section 5 describes the
audit diagnostics, Sections 6 and 7 the data and setup, and Section 8 the
results. Section 9 discusses their implications, Section 10 the threats to their
validity, and Section 11 concludes.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Angka | 18.869 pasien, 1,155 rekaman/pasien (§6.2: "mean 1.155" → ditulis 1.16); 44 subjek MIT-BIH (48 − 4 paced); "more than 1,500 beats each" (§6.3: rentang 1.517–3.361); 24/44 SCP (Tabel 8.2); 75–110% (§8.5) |
| Klaim kinerja model | Kalimat "match or exceed specialist performance" **dibuang sebelum disimpan**: [F1] adalah benchmark PTB-XL dan tidak membandingkan dengan kardiolog. Diganti "routinely benchmarked" |
| "Code ... released" | Repo saat ini **privat** (`darknestt/conformal-ecg`). Wajib dibuka (atau diarsip di Zenodo dengan DOI) sebelum submit, atau kalimat ini dihapus |
| Split MIT-BIH | 11/11 adalah **rancangan kami** atas DS2, bukan bagian dari partisi kanonik DS1/DS2 — rumusan disesuaikan |
| Penomoran bagian | Sama dengan naskah Word: Threats = §10 (`sec10-draft.md`), Conclusion = §11 |
