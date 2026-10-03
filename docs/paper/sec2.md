# §2 Related Work

> **v7 — 2026-10-02.** Diparafrasekan penuh dari v6 (commit 3edc1f0); deskripsi karya terdahulu dirumuskan ulang agar tidak menggemakan abstrak sumbernya. Semua 31 kode sitasi tetap; kutipan langsung Lee et al. tetap dalam tanda kutip/miring.

---

## 2. Related Work

### 2.1 Conformal prediction under dependence and for hierarchical data

When exchangeability fails, Barber et al. bound the coverage loss by the
total-variation distance to an exchangeable counterpart [A1]; the bound is
agnostic to the cause and prescribes no remedy. Specific departures have been
handled one by one, namely covariate shift under known or estimable likelihood
ratios [A4], spatial data [A7] and network dependence [A8]. Bhattacharyya and Barber consider
groups whose membership drives the shift [A3], so exchangeability still holds
within each group; our setting is the reverse, with stable group proportions but
non-exchangeable observations within a block. Fontana et al. review the framework
and its variants, Mondrian conformal prediction included [A11], and calibrated
Mondrian versions have followed [D2].

For repeated measurements, Lee et al. formalized hierarchical exchangeability and
extended conformal prediction and the jackknife+ [A2] to it [A0]; (1) and (2)
restate their threshold and guarantee, and four two-layer hierarchical
constructions were developed independently by Dunn et al. [A0b]. We take these results as
given. Both lines of work are theoretical and evaluated on regression, [A0] on
simulated data and a Lorenz-96 system, and neither addresses the question an
applied study meets first: for a given clinical dataset and error rate, which
grouping, if any, lets the guarantee be enforced? Lee et al. approach it when
they note that an analyst may trade many small groups against few large ones,
adding that *characterizing the pros and cons of this tradeoff is an important
question to determine how study design affects inference in this
distribution-free setting* [A0]. We take up its most elementary part, whether a
design admits a finite threshold at all, and then measure what happens on
clinical data when it does.

### 2.2 Multi-label, clinical and ECG applications

Multi-label conformal methods, surveyed by Papadopoulos [B1], model dependence
among labels but assume exchangeable samples, the converse of our need. Pruning
makes Label Powerset conformal prediction cheaper [B3], and hierarchical
multi-label classification without conformal guarantees is well developed [B5],
[B6]. Baheri and Shahbazi calibrate at several
levels of a label hierarchy and intersect the sets [B2], and Zhang et al. encode
prediction sets as nodes of a label graph [B7, preprint]. Both exploit structure
among labels; here the hierarchy only serves to count calibration blocks per
label (§3.4).

Strodthoff et al. set the PTB-XL benchmarks [F1] for the dataset of [H1], [H2],
and their residual networks guide our choice of backbones. Beat-level evaluation
follows the inter-patient protocol, under which no subject appears in both
training and evaluation [F2], [F10], since mixing them inflates reported
performance [F3]. For clinical medicine, a survey of conformal prediction is
available [E1], alongside applications to anatomical landmarks [E2] and
multi-label diagnosis coding [E3]; conformal risk control [C1] and time-series
conformal prediction [C4] extend the framework to arbitrary losses and temporal
data.

Several cardiac studies come closer to our question. On patient-disjoint PTB-XL
partitions, El Allam and Hamlich apply label-conditional Mondrian calibration
and find that it must be redone for the quantized model actually deployed [E7];
they also bring conformal inference to wearables at the edge [E9]. For PPG-based arrhythmia classification in intensive care, Kinalioğlu finds
that marginal coverage can hide class- and patient-level failures [E8]. Closest to
our work, Sim and Kim show that the false-alarm guarantee of split conformal
prediction in ECG monitoring is governed by the number of exchangeable subjects,
not beats, so that too few calibration subjects raise the realized false-alarm
rate [E6]. Beyond cardiology, calibration that respects groups has been used for
patients nested in thousands of hospitals [E5].

**Position of this study.** These studies ask whether a procedure reaches its
target on a given split. We ask two prior questions, whether a block-level
guarantee is feasible once every declared dependence source is respected, and
whether ignoring block structure costs coverage once the mechanical effect of the
finite-block correction is removed.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Klaim salah yang dibuang (v3) | "[D2] … we use as a baseline"; "Our hierarchical closure"; "[C1], [C4] … machinery we build on" — tetap tidak ada |
| Klaim dilunakkan (v3) | [F3] hanya "mixing the two inflates reported performance" |
| Kutipan langsung Lee et al. | Kata per kata, miring, dengan sitasi (ejaan asli "characterizing", "tradeoff") |
