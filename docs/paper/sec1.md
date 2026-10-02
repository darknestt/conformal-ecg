# §1 Introduction

> **v3 — 2026-10-02.** Ditulis ulang mengikuti struktur enam paragraf (konteks → conformal → blok → HCP → celah → kontribusi). Versi sebelumnya: `sec1-draft.md` di riwayat git (commit 9098746).

---

## 1. Introduction

Deep networks for electrocardiogram (ECG) interpretation are now routinely
benchmarked on large public datasets [F1], [H1], and reviews of clinical deep
learning [G1] and the FUTURE-AI consensus guideline [G2] treat calibrated
uncertainty as a condition for their deployment.

Conformal prediction turns any trained classifier into a set-valued predictor
whose coverage holds in finite samples [A11]. It has been applied across clinical
domains [E1]–[E3] and, for ECG and related cardiac signals, to calibrate quantized
models [E7], adapt inference on wearables [E9], expose per-class and per-patient
failures [E8], and control false alarms in monitoring [E6]. The guarantee rests on
exchangeability of calibration and test observations; when that fails, the
coverage gap can be bounded only in general terms [A1].

Clinical ECG data are seldom exchangeable at the level at which they are stored:
a patient contributes several recordings, a Holter episode is cut into segments,
a recording yields thousands of beats, and devices, sites and operators are
shared across patients. A calibration set of many records may therefore contain
far fewer independent units.

For grouped or repeated measurements, Lee et al. derived hierarchical
exchangeability and a hierarchical conformal prediction (HCP) procedure that
calibrates over blocks [A0]; Dunn et al. gave related constructions for two-layer
models [A0b]. Because HCP gives every calibration block equal mass and adds an
atom at $+\infty$, its threshold is finite only when the target error rate
$\alpha$ is at least $1/(K_1+1)$, with $K_1$ the number of calibration blocks.
Once every dependence source is respected a large dataset can have few blocks,
and a rare diagnosis fewer still. Conversely, ignoring blocks need not cost
coverage when most patients contribute a single recording. Lee et al. name the
trade-off between many small and few large groups as an open question for study
design [A0], and Sim and Kim have shown for ECG monitoring that the false-alarm
bound of split conformal prediction counts subjects rather than beats [E6].

What remains insufficiently characterized is whether the intended finite-sample
guarantee is feasible under the dependence structures of real clinical
resources, where several sources may be crossed and coverage may be required per
diagnosis. We examine this design-stage question through an empirical audit of
three public ECG resources: PTB-XL [H1], [H2], with 18,869 patients averaging
1.16 records each; the MIT-BIH Arrhythmia Database [H3], with 44 subjects
contributing more than 1,500 beats each; and the PhysioNet/CinC Challenge 2021
collection [H5], in which the block identifier is not documented at all. We
introduce no new conformal procedure. Our contributions are four.

- **A metadata-only feasibility audit** (§5, §8.1). Given the declared dependence
  sources, the HCP bound and the join of those sources yield exact feasibility
  calculations before any patient is enrolled. Declaring all four documented
  sources of PTB-XL collapses every admissible calibration grouping to a single
  block; under patient blocking alone, 24 of 44 SCP diagnostic statements admit
  no finite per-label threshold at $\alpha=0.05$; and dividing the 22 MIT-BIH
  evaluation subjects of the canonical inter-patient partition evenly between
  calibration and test cannot support a subject-level guarantee at the 95% level.
- **Attribution of under-coverage to dependence acting through repetition**
  (§8.2–§8.4). On MIT-BIH, naive split conformal under-covers relative to a
  matched permutation null, and a factorial design attributes the deficit to
  clustering rather than to unequal block sizes. In a controlled dose–response
  experiment within MIT-BIH the deficit rises with the design effect, and PTB-XL
  falls where the design effect predicts — near zero — despite a substantial
  within-patient correlation.
- **A caution for evaluating hierarchical conformal methods** (§8.3, §9.3). The
  apparent improvement of HCP over naive split conformal persists at 75–110% of
  its size once within-block dependence is permuted away, so it is largely
  mechanical. We recommend matched permutation nulls and joint reporting of set
  size.
- **Pre-registered robustness checks reported in full** (§8.5, §10). The direction
  of every finding holds across three backbones spanning more than a hundredfold
  range of parameters and across checkpoints. Statistical strength does not, and
  the backbone that fails the pre-registered criterion is reported.

All resampling is performed on blocks, the held-out PTB-XL fold was never
examined, deviations from the protocol are logged, and code and per-result
artifacts are released with the paper.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Angka | 18.869 pasien; 1,155 → 1,16 rekaman/pasien (§6.2); 44 subjek; >1.500 detak (rentang 1.517–3.361); 24/44 (Tabel 8.2); 75–110% (§8.3, §8.5) |
| Kebaruan | Tanpa "first"/"novel". Celah dirumuskan "insufficiently characterized", sesuai tinjauan eksternal |
| "Code ... released" | Repo masih privat — wajib dibuka/diarsip Zenodo sebelum submit (R5) |
