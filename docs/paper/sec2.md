# §2 Related Work

> **v5 — 2026-10-02.** Diparafrasekan dan dipadatkan dari v4 (commit 2bbdbec). Semua 31 kode sitasi §2 tetap; tidak ada klaim baru.

---

## 2. Related Work

### 2.1 Conformal prediction under dependence and for hierarchical data

Barber et al. bound the coverage gap of conformal prediction by the
total-variation distance between the data distribution and its exchangeable
counterpart [A1]; the bound holds whatever causes the violation but suggests no
remedy. Specific departures have been treated separately: covariate shift with
known or estimable likelihood ratios [A4], spatial data [A7] and network
dependence [A8]. Bhattacharyya and Barber consider groups whose membership
determines the covariate shift [A3]; there the data stay exchangeable within each
group, whereas in our setting group proportions are stable and observations
within a block are not exchangeable. Fontana et al. review the framework and its
variants [A11], including the Mondrian construction, for which calibrated
versions have since been developed [D2].

Lee et al. formalized hierarchical exchangeability for groups of repeated
measurements and extended both conformal prediction and the jackknife+ [A2] to
that setting [A0]; their threshold and guarantee are restated in (1) and (2).
Dunn et al. independently proposed four constructions for two-layer hierarchical
models [A0b]. We take these results as given. Both works are theoretical and
evaluate on regression problems ([A0] on simulated data and a Lorenz-96 system),
and neither asks the question that precedes application: for a given clinical
dataset and target error rate, at which grouping, if any, can the guarantee be
enforced? Lee et al. point toward it, noting that an analyst may
choose between many groups with few measurements or few groups with many
repeats, and that *characterizing the pros and cons of this tradeoff is an
important question to determine how study design affects inference in this
distribution-free setting* [A0]. We address its most elementary part — whether a
finite threshold exists for a given design — and then measure what happens on
clinical data when it does.

### 2.2 Multi-label, clinical and ECG applications

Multi-label conformal methods, reviewed by Papadopoulos [B1], model dependence
between labels while assuming exchangeable samples; our setting requires the
converse. Maltoudoglou et al. prune Label Powerset conformal prediction to reduce
its cost [B3], and hierarchical multi-label classification without conformal
guarantees is well developed [B5], [B6]. Baheri and Shahbazi calibrate at several
resolutions of a label hierarchy and intersect the resulting sets [B2], and Zhang
et al. represent prediction sets as nodes of a label graph [B7, preprint]. Both
concern structure among labels; we use the hierarchy only to count calibration
blocks per label (§3.4).

Strodthoff et al. established the PTB-XL benchmarks [F1] on the dataset of
[H1], [H2]; their residual architectures inform our backbones. Heartbeat-level
evaluation follows the inter-patient protocol, in which no subject contributes to
both training and evaluation [F2], [F10], because violating it inflates reported
performance [F3]. Conformal prediction in clinical medicine is surveyed in [E1],
with applications to anatomical landmark localization [E2] and multi-label
diagnosis coding [E3]; conformal risk control [C1] and conformal prediction for
time series [C4] extend the framework to general losses and to temporal data.

Recent cardiac studies come closer to our question. El Allam and Hamlich
calibrate label-conditional Mondrian conformal prediction on patient-disjoint
PTB-XL partitions and show that calibration must match the quantized model
actually deployed [E7]; they also extend conformal inference to edge-deployed
wearables [E9]. Kinalioğlu shows, for PPG-based ICU arrhythmia classification,
that marginal coverage can hide per-class and per-patient failures [E8]. Closest
to the present study, Sim and Kim show that in ECG monitoring the false-alarm
bound of split conformal prediction counts exchangeable subjects rather than
beats, so that too few calibration subjects inflate the realized false-alarm
rate and the unit carrying the guarantee must be the unit raising alarms [E6].
Outside cardiology, group-aware conformal calibration has been applied to
patients nested in thousands of hospitals [E5].

**Position of this study.** These studies ask whether a procedure meets its
target on a given split. We ask two earlier questions: whether a block-level
guarantee is feasible once every declared dependence source — including crossed
sources and label-level conditioning — is respected, and whether ignoring block
structure costs coverage once the mechanical effect of the finite-block
correction is controlled. The contribution is an audit of design-stage
feasibility and of the attribution of coverage loss, not a new conformal
procedure.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Klaim salah yang dibuang (v3) | "[D2] … we use as a baseline"; "Our hierarchical closure"; "[C1], [C4] … machinery we build on" — tetap tidak ada |
| Klaim dilunakkan (v3) | [F3] hanya "violating it inflates reported performance" |
| Kutipan langsung Lee et al. | Kata per kata (ejaan asli "characterizing", "tradeoff") |
