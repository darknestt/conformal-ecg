# §1 Introduction

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0). Angka, sitasi dan empat kontribusi tetap.

---

## 1. Introduction

Public benchmarks [F1], [H1] have made deep-network interpretation of the
electrocardiogram (ECG) routine, and both reviews of clinical deep learning [G1]
and the FUTURE-AI guideline [G2] treat calibrated uncertainty as a prerequisite
for deployment. Conformal prediction provides it by turning a trained classifier
into a set predictor with finite-sample coverage [A11]. It has been applied
across clinical domains [E1] and, for cardiac signals, to calibrate
quantized models [E7], adapt inference on wearables [E9], expose class- and
patient-level failures [E8] and bound false alarms in monitoring [E6]. All of
these uses assume that calibration and test observations are exchangeable;
without that assumption only a generic bound on the coverage gap survives [A1].

Stored ECG data rarely meet it. A patient contributes several recordings, Holter
episodes are cut into segments, one recording yields thousands of beats, and
patients share devices, sites and operators, so a calibration set may hold far
fewer independent units than records. Hierarchical conformal prediction (HCP)
handles such data by calibrating over blocks under hierarchical exchangeability
[A0]; Dunn et al. developed related two-layer constructions [A0b]. Because HCP
gives each calibration block equal mass and adds an atom at $+\infty$, its
threshold is finite only when the target error rate $\alpha$ is at least
$1/(K_1+1)$, with $K_1$ the number of calibration blocks. A large dataset can
thus be left with few blocks once every dependence source is respected, and a
rare diagnosis with fewer still. Conversely, ignoring blocks may cost nothing
when almost every patient contributes one recording. Lee et al. leave the choice
between many small and few large groups open as a design question [A0], and Sim
and Kim showed for ECG monitoring that the false-alarm guarantee of split
conformal prediction scales with subjects, not beats [E6].

Whether the guarantee is attainable under the dependence structure of real
clinical resources, where sources can be crossed and coverage may be required per
diagnosis, remains insufficiently characterized. We address this design-stage
question by auditing three public ECG resources: PTB-XL [H1], [H2], in which
18,869 patients contribute 1.16 records on average; the MIT-BIH Arrhythmia
Database [H3], in which each of 44 subjects contributes more than 1,500 beats;
and the PhysioNet/CinC Challenge 2021 collection [H5], which does not document a
block identifier. Two questions guide the audit. Can a block-level guarantee be
enforced at conventional error rates (RQ1)? Does ignoring block structure cost
coverage, and through what mechanism (RQ2)? Fig. 1 shows the two stages that
answer them, RQ1 from metadata alone and RQ2 from the conformity scores of three
backbones, with the section that reports each step.

![**Fig. 1.** Audit workflow. Stage 1 (blue header) uses metadata only and gives verdicts exact given the declared sources $D$ (RQ1); Stage 2 (orange headers) uses conformity scores from three backbones at feasible levels only (RQ2). Section numbers mark where each step is reported.](figures/fig1_audit_workflow.png)

We propose no new conformal procedure. The contributions are three.

- **A metadata-only feasibility audit** (RQ1; §3, §5.1). The HCP bound,
  combined with the join of the declared dependence sources, gives exact verdicts
  before any model is trained: all four documented PTB-XL sources together leave
  one admissible calibration block, 24 of 44 SCP statements have no finite
  per-label threshold at $\alpha=0.05$ under patient blocking, and an even split
  of the 22 MIT-BIH evaluation subjects rules out a subject-level guarantee at
  the 95% level.
- **Attribution of under-coverage to dependence acting through repetition**
  (RQ2; §5.2–§5.4). On the 22 MIT-BIH evaluation subjects, naive split conformal
  covers less than a matched permutation null for every backbone and level; a
  factorial design attributes the shortfall mainly to clustering, amplified by
  block-size imbalance, and a dose–response experiment shows it growing with the
  design effect. PTB-XL stays near zero despite substantial within-patient
  correlation, as the design effect predicts. With 22 subjects the deficit is not
  resolved at the subject level, a limit on the evidence that mirrors the limit
  on the guarantee.
- **Two cautions for evaluating conformal methods on clustered data** (§5.3,
  §6.2). Between 75% and 110% of the apparent gain of HCP over naive split
  conformal survives when dependence is permuted away, so the gain is largely
  mechanical; and repeated splits of a fixed set of subjects give intervals for
  the split procedure, not the population, which on MIT-BIH exclude zero where a
  jackknife over subjects does not.

Every finding is checked across three backbones whose sizes differ more than a
hundredfold and across two checkpoints; resampling is always over blocks, and the
held-out PTB-XL fold remains unexamined. We keep three levels of evidence apart:
what is proved (Propositions 1–3 and Corollaries 1–2, exact given the declared
sources), what is observed on the audited records (§5.2–§5.5), and what is not
claimed, namely the population-level sign of the MIT-BIH deficit and a causal
role for the design effect. Code, per-result artifacts, the analysis
protocol and its deviation log are released with the paper. Section 2 reviews
related work, Section 3 derives the feasibility conditions, Section 4 describes
the design, and Sections 5 and 6 report and discuss the results.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Angka | 18.869 pasien; 1,155 → 1,16 rekaman/pasien (§4.1); 44 subjek; >1.500 detak (rentang 1.517–3.361); 24/44 (Tabel 5.2); 75–110% (§5.3, §5.5) |
| Kebaruan | Tanpa "first"/"novel". Celah dirumuskan "insufficiently characterized" |
| "Code ... released" | Repo masih privat — wajib dibuka/diarsip Zenodo sebelum submit (R5) |
