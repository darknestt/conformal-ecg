# §2 Related Work

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0); deskripsi karya terdahulu dirumuskan ulang agar tidak menggemakan abstrak sumbernya. Semua 31 kode sitasi tetap; kutipan langsung Lee et al. tetap dalam tanda kutip/miring.

---

## 2. Related Work

### 2.1 Conformal prediction under dependence and for hierarchical data

When exchangeability fails, Barber et al. bound the loss of coverage by the
total-variation distance between the data distribution and an exchangeable
counterpart [A1]; the bound is agnostic to the source of the violation and does
not prescribe a fix. Other work handles particular departures one at a time:
covariate shift with known or estimable likelihood ratios [A4], spatial data [A7]
and network dependence [A8]. Bhattacharyya and Barber study groups whose
membership drives the covariate shift [A3], so that exchangeability still holds
inside each group; our setting is the reverse, with stable group proportions but
non-exchangeable observations within a block. The framework and its variants,
the Mondrian construction among them, are reviewed by Fontana et al. [A11], and
calibrated Mondrian versions have appeared since [D2].

For groups of repeated measurements, Lee et al. formalized hierarchical
exchangeability and carried both conformal prediction and the jackknife+ [A2]
over to it [A0]; (1) and (2) restate their threshold and guarantee. Working
independently, Dunn et al. proposed four constructions for two-layer
hierarchical models [A0b]. These results are taken as given here. Both lines of
work are theoretical and are evaluated on regression tasks, [A0] on simulated
data and a Lorenz-96 system, and neither addresses the question an applied study
faces first: given a clinical dataset and a target error rate, which grouping, if
any, lets the guarantee be enforced? Lee et al. come close to it when they note
that an analyst may trade many groups with few measurements against few groups
with many repeats, adding that *characterizing the pros and cons of this tradeoff
is an important question to determine how study design affects inference in this
distribution-free setting* [A0]. We take up the most elementary part of that
question — whether a design admits a finite threshold at all — and then measure
what happens on clinical data when it does.

### 2.2 Multi-label, clinical and ECG applications

Multi-label conformal methods, surveyed by Papadopoulos [B1], capture dependence
among labels but assume exchangeable samples, the converse of what our setting
needs. Maltoudoglou et al. lower the cost of Label Powerset conformal prediction
through pruning [B3], and hierarchical multi-label classification without
conformal guarantees is a mature field [B5], [B6]. Baheri and Shahbazi calibrate
at several levels of a label hierarchy and intersect the resulting sets [B2],
while Zhang et al. encode prediction sets as nodes of a label graph [B7,
preprint]. Both exploit structure among labels; here the hierarchy serves only to
count calibration blocks per label (§3.4).

On the ECG side, Strodthoff et al. set the PTB-XL benchmarks [F1] for the dataset
described in [H1], [H2], and their residual networks guide our choice of
backbones. Beat-level evaluation follows the inter-patient protocol, under which
no subject appears in both training and evaluation [F2], [F10], because mixing
the two inflates reported performance [F3]. A survey of conformal prediction in
clinical medicine is given in [E1], with applications to anatomical landmark
localization [E2] and multi-label diagnosis coding [E3]; conformal risk control
[C1] and time-series conformal prediction [C4] generalize the framework to
arbitrary losses and to temporal data.

Several recent cardiac studies approach our question more closely. El Allam and
Hamlich calibrate label-conditional Mondrian conformal prediction on
patient-disjoint PTB-XL partitions, showing that calibration has to match the
quantized model that is actually deployed [E7], and they extend conformal
inference to wearables at the edge [E9]. In PPG-based arrhythmia classification
in intensive care, Kinalioğlu finds that marginal coverage can conceal failures
for particular classes and patients [E8]. Nearest to the present work, Sim and
Kim show that in ECG monitoring the false-alarm guarantee of split conformal
prediction is governed by the number of exchangeable subjects rather than of
beats, so that too few calibration subjects push the realized false-alarm rate
up and the guarantee must attach to the same unit that raises alarms [E6].
Beyond cardiology, group-aware conformal calibration has been used for patients
nested in thousands of hospitals [E5].

**Position of this study.** The studies above check whether a procedure reaches
its target on a given split. We pose two prior questions: is a block-level
guarantee feasible once every declared dependence source — crossed sources and
label-level conditioning included — is respected, and does ignoring block
structure cost coverage once the mechanical effect of the finite-block
correction is accounted for? What we contribute is an audit of design-stage
feasibility and of the attribution of coverage loss, rather than a new conformal
procedure.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Klaim salah yang dibuang (v3) | "[D2] … we use as a baseline"; "Our hierarchical closure"; "[C1], [C4] … machinery we build on" — tetap tidak ada |
| Klaim dilunakkan (v3) | [F3] hanya "mixing the two inflates reported performance" |
| Kutipan langsung Lee et al. | Kata per kata, miring, dengan sitasi (ejaan asli "characterizing", "tradeoff") |
