# §1 Introduction

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0). Angka, sitasi dan empat kontribusi tetap.

---

## 1. Introduction

Public benchmarks [F1], [H1] have made deep-network interpretation of the
electrocardiogram (ECG) a routine exercise, and both reviews of clinical deep
learning [G1] and the FUTURE-AI consensus guideline [G2] name calibrated
uncertainty as a prerequisite for deployment.

Conformal prediction supplies such uncertainty by wrapping a trained classifier
so that it outputs prediction sets with finite-sample coverage [A11]. Its
clinical uses span several domains [E1]–[E3]; for ECG and related cardiac signals
it has served to calibrate quantized models [E7], to adapt inference on wearable
devices [E9], to reveal failures hidden at the level of classes and patients
[E8], and to bound false alarms during monitoring [E6]. All of these rest on
exchangeability between calibration and test observations, and once that
assumption is dropped only a generic bound on the coverage gap remains [A1].

Stored ECG data seldom honor the assumption. One patient supplies several
recordings, Holter episodes are cut into segments, a single recording yields
thousands of beats, and patients share devices, sites and operators. The number
of independent units in a calibration set can therefore be much smaller than its
number of records.

Lee et al. addressed grouped data of this kind by formalizing hierarchical
exchangeability and proposing hierarchical conformal prediction (HCP), which
calibrates over blocks [A0]; Dunn et al. developed related constructions for
two-layer models [A0b]. Because HCP assigns every calibration block the same mass
and places an extra atom at $+\infty$, its threshold is finite only if the target
error rate $\alpha$ is no smaller than $1/(K_1+1)$, where $K_1$ counts the
calibration blocks. A large dataset may thus retain few blocks once every
dependence source is honored, and a rare diagnosis fewer still. In the opposite
direction, ignoring blocks may cost nothing when nearly every patient contributes
one recording. Lee et al. identify the choice between many small and few large
groups as an open question of study design [A0], and Sim and Kim have shown, for
ECG monitoring, that the false-alarm guarantee of split conformal prediction
scales with the number of subjects rather than of beats [E6].

It remains insufficiently characterized whether the intended guarantee is
attainable under the dependence structures of real clinical resources, in which
sources may be crossed and coverage may be demanded for each diagnosis. We take
up this design-stage question with an empirical audit of three public ECG
resources: PTB-XL [H1], [H2], where 18,869 patients contribute 1.16 records on
average; the MIT-BIH Arrhythmia Database [H3], where each of 44 subjects
contributes more than 1,500 beats; and the PhysioNet/CinC Challenge 2021
collection [H5], which leaves the block identifier undocumented. We introduce no
new conformal procedure. The audit contributes the following.

- **A metadata-only feasibility audit** (§3, §5.1). The HCP bound, combined with
  the join of the declared dependence sources, returns exact verdicts before a
  single patient is enrolled. With all four documented PTB-XL sources declared,
  every admissible calibration grouping reduces to one block; with patient
  blocking alone, 24 of 44 SCP diagnostic statements lack a finite per-label
  threshold at $\alpha=0.05$; and dividing the 22 MIT-BIH evaluation subjects
  evenly between calibration and test rules out a subject-level guarantee at the
  95% level.
- **Attribution of under-coverage to dependence acting through repetition**
  (§5.2–§5.4). Naive split conformal on MIT-BIH covers less than a matched
  permutation null, a factorial design assigns the shortfall to clustering
  rather than to unequal block sizes, and a controlled dose–response experiment
  shows it increasing with the design effect. PTB-XL, despite substantial
  within-patient correlation, sits near zero, as the design effect predicts.
- **A caution for evaluating hierarchical conformal methods** (§5.3, §6.2).
  Between 75% and 110% of the apparent gain of HCP over naive split conformal
  survives when within-block dependence is permuted away, so the gain is largely
  mechanical; matched permutation nulls and joint reporting of set size are
  therefore recommended.
- **Pre-registered robustness checks reported in full** (§5.5, §6.4). Across
  three backbones whose parameter counts differ by more than a hundredfold, and
  across checkpoints, every finding keeps its direction; statistical strength
  varies, and the backbone that misses the pre-registered criterion is reported.

Resampling is always performed over blocks, the held-out PTB-XL fold has never
been inspected, deviations from the protocol are logged, and the code and
per-result artifacts are released with the paper. Section 2 situates the audit in
prior work, Section 3 derives the feasibility conditions, Section 4 sets out the
design, and Sections 5 and 6 present and discuss the findings.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Angka | 18.869 pasien; 1,155 → 1,16 rekaman/pasien (§4.1); 44 subjek; >1.500 detak (rentang 1.517–3.361); 24/44 (Tabel 5.2); 75–110% (§5.3, §5.5) |
| Kebaruan | Tanpa "first"/"novel". Celah dirumuskan "insufficiently characterized" |
| "Code ... released" | Repo masih privat — wajib dibuka/diarsip Zenodo sebelum submit (R5) |
