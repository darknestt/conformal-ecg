# §1 Introduction

> **v5 — 2026-10-02.** Diparafrasekan dan dipadatkan dari v4 (commit 2bbdbec). Semua angka, sitasi dan empat kontribusi tetap.

---

## 1. Introduction

Deep networks for electrocardiogram (ECG) interpretation are now routinely
benchmarked on large public datasets [F1], [H1], and both reviews of clinical
deep learning [G1] and the FUTURE-AI consensus guideline [G2] list calibrated
uncertainty among the conditions for deployment.

Conformal prediction turns any trained classifier into a set-valued predictor
with finite-sample coverage [A11]. It has been applied across clinical domains
[E1]–[E3] and, for ECG and related cardiac signals, to calibrate quantized
models [E7], adapt inference on wearables [E9], expose per-class and per-patient
failures [E8], and control false alarms in monitoring [E6]. The guarantee assumes
that calibration and test observations are exchangeable; without that
assumption the coverage gap can be bounded only in general terms [A1].

Clinical ECG data rarely meet this assumption at the level at which they are
stored: a patient contributes several recordings, a Holter episode is cut into
segments, a recording yields thousands of beats, and devices, sites and
operators are shared across patients. A calibration set of many records may thus
contain far fewer independent units.

For such grouped data, Lee et al. formalized hierarchical exchangeability and a
hierarchical conformal prediction (HCP) procedure that calibrates over blocks
[A0]; Dunn et al. gave related constructions for two-layer models [A0b]. HCP
gives every calibration block equal mass and adds an atom at $+\infty$, so its
threshold is finite only when the target error rate $\alpha$ is at least
$1/(K_1+1)$, with $K_1$ the number of calibration blocks. Respecting every
dependence source can leave a large dataset with few blocks, and a rare
diagnosis with fewer still; conversely, ignoring blocks need not cost coverage
when most patients contribute a single recording. Lee et al. leave the trade-off
between many small and few large groups open as a question of study design [A0],
and Sim and Kim have shown for ECG monitoring that the false-alarm bound of
split conformal prediction counts subjects rather than beats [E6].

What remains insufficiently characterized is whether the intended guarantee is
feasible under the dependence structures of real clinical resources, where
several sources may be crossed and coverage may be required per diagnosis. We
examine this design-stage question through an empirical audit of three public
ECG resources: PTB-XL [H1], [H2], with 18,869 patients averaging 1.16 records
each; the MIT-BIH Arrhythmia Database [H3], whose 44 subjects each contribute
more than 1,500 beats; and the PhysioNet/CinC Challenge 2021 collection [H5],
which does not document a block identifier at all. We introduce no new conformal
procedure. The audit makes four contributions.

- **A metadata-only feasibility audit** (§3, §5.1). Given the declared dependence
  sources, the HCP bound and the join of those sources yield exact verdicts
  before any patient is enrolled. Declaring all four documented sources of PTB-XL
  collapses every admissible calibration grouping to a single block; under
  patient blocking alone, 24 of 44 SCP diagnostic statements admit no finite
  per-label threshold at $\alpha=0.05$; and an even calibration–test split of the
  22 MIT-BIH evaluation subjects cannot support a subject-level guarantee at the
  95% level.
- **Attribution of under-coverage to dependence acting through repetition**
  (§5.2–§5.4). On MIT-BIH, naive split conformal under-covers a matched
  permutation null; a factorial design attributes the deficit to clustering
  rather than unequal block sizes, and in a controlled dose–response experiment
  it rises with the design effect. PTB-XL falls where the design effect predicts
  — near zero — despite substantial within-patient correlation.
- **A caution for evaluating hierarchical conformal methods** (§5.3, §6.2). The
  apparent gain of HCP over naive split conformal persists at 75–110% of its size
  once within-block dependence is permuted away, so it is largely mechanical. We
  recommend matched permutation nulls and joint reporting of set size.
- **Pre-registered robustness checks reported in full** (§5.5, §6.4). Every
  finding keeps its direction across three backbones spanning more than a
  hundredfold range of parameters and across checkpoints; statistical strength
  does not, and the backbone that fails the pre-registered criterion is reported.

All resampling is performed on blocks, the held-out PTB-XL fold was never
examined, protocol deviations are logged, and code and per-result artifacts are
released with the paper. Section 2 positions the audit, Section 3 states the
feasibility conditions, Section 4 describes the design, and Sections 5 and 6
report and interpret the results.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Angka | 18.869 pasien; 1,155 → 1,16 rekaman/pasien (§4.1); 44 subjek; >1.500 detak (rentang 1.517–3.361); 24/44 (Tabel 5.2); 75–110% (§5.3, §5.5) |
| Kebaruan | Tanpa "first"/"novel". Celah dirumuskan "insufficiently characterized" |
| "Code ... released" | Repo masih privat — wajib dibuka/diarsip Zenodo sebelum submit (R5) |
