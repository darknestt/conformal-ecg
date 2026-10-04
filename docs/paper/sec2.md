# §2 Related Work

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0); deskripsi karya terdahulu dirumuskan ulang agar tidak menggemakan abstrak sumbernya. Semua 31 kode sitasi tetap; kutipan langsung Lee et al. tetap dalam tanda kutip/miring.

---

## 2. Related Work

### 2.1 Conformal prediction under dependence and for hierarchical data

When exchangeability fails, Barber et al. bound the coverage loss by the
total-variation distance to an exchangeable counterpart [A1]; the bound is
agnostic to the cause and prescribes no remedy. Specific departures have been
handled one by one, namely covariate shift under known or estimable likelihood
ratios [A4], spatial data [A7], network dependence [A8] and temporal data [C4],
and conformal risk control extends the guarantee to general losses [C1].
Bhattacharyya and
Barber consider groups whose membership drives the shift [A3], so exchangeability
still holds within each group; our setting is the reverse, with stable group
proportions but non-exchangeable observations within a block. Fontana et al.
review the framework and its variants, Mondrian conformal prediction included
[A11].

For repeated measurements, Lee et al. formalized hierarchical exchangeability and
extended conformal prediction to it [A0]; (1) and (2) restate their threshold and
guarantee, which we take as given. Their experiments use simulated data and a
Lorenz-96 system. Working independently, Dunn et al. developed conformal
constructions for two-layer hierarchical models, among them double conformal
prediction, CDF pooling and single and repeated subsampling, with and without
covariates, illustrated on simulations and on a sleep-deprivation study of 18
subjects [A0b]. Lee et al. leave open how study design affects inference, noting
that an analyst may trade many small groups against few large ones and that
*characterizing the pros and cons of this tradeoff is an important question to
determine how study design affects inference in this distribution-free setting*
[A0].

### 2.2 Group counts and clustered thresholds

That the number of independent units, not of observations, limits a
distribution-free guarantee is already established. Dunn et al. state, for each
of their finite-sample constructions, how many groups non-trivial prediction
sets require, between $1/\alpha-1$ and $4/\alpha-1$ depending on the
construction [A0b]. For ECG monitoring, Sim and Kim show that the false-alarm
guarantee of split conformal prediction counts exchangeable subjects rather than
beats, give the minimum of $1/\alpha-1$ calibration subjects (19 at
$\alpha=0.05$), decline a subject-level threshold for MIT-BIH because their split
leaves too few calibration subjects, and show that a beat-calibrated threshold
used for patient-level alarms exceeds its nominal false-alarm rate [E6]. On the
precision side, Noonan derives a large-sample variance for the coverage of a
threshold estimated from clustered data, in which the relevant correlation is
that of the exceedance indicator rather than of the score and can change with the
target level [P1].

These results are stated for one grouping at a time. They do not ask which
grouping a clinical dataset admits when several dependence sources are declared,
how the count behaves per diagnostic label, or how much of an observed coverage
gap reflects dependence rather than the construction of the method.

### 2.3 Multi-label, clinical and ECG applications

Multi-label conformal methods, surveyed by Papadopoulos [B1], model dependence
among labels but assume exchangeable samples, the converse of our need. Baheri
and Shahbazi calibrate at several levels of a label hierarchy and intersect the
sets [B2], exploiting structure among labels; here the hierarchy only serves to
count calibration blocks per label (§3.4).

Strodthoff et al. set the PTB-XL benchmarks [F1] for the dataset of [H1], [H2],
and their residual networks guide our choice of backbones. Beat-level evaluation
follows the inter-patient protocol, under which no subject appears in both
training and evaluation [F2], [F10], since mixing them inflates reported
performance [F3]. Clinical uses of conformal prediction are surveyed in [E1]. On
patient-disjoint PTB-XL
partitions, El Allam and Hamlich apply label-conditional Mondrian calibration
and find that it must be redone for the quantized model actually deployed [E7];
they also bring conformal inference to wearables at the edge [E9]. For PPG-based
arrhythmia classification in intensive care, Kinalioğlu finds that marginal
coverage can hide class- and patient-level failures [E8]. Beyond cardiology,
calibration that respects groups has been used for patients nested in thousands
of hospitals [E5].

**Position of this study.** We take the threshold and guarantee of HCP [A0] and
the principle that independent units must be counted [A0b], [E6] as given. What
we add is their application at the design stage of clinical ECG studies: the join
of crossed dependence sources as the finest admissible calibration grouping
(Proposition 2), the block count per diagnostic label (Proposition 3), both
evaluated from metadata on three ECG resources, and an empirical decomposition of
the coverage gap of naive split conformal prediction with a matched permutation
null, a factorial design and a dose–response experiment, which separates
dependence from the mechanical effect of the finite-block correction.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Klaim salah yang dibuang (v3) | "[D2] … we use as a baseline"; "Our hierarchical closure"; "[C1], [C4] … machinery we build on" — tetap tidak ada |
| Klaim dilunakkan (v3) | [F3] hanya "mixing the two inflates reported performance" |
| Kutipan langsung Lee et al. | Kata per kata, miring, dengan sitasi (ejaan asli "characterizing", "tradeoff") |
