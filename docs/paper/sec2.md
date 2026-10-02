# §2 Related Work

> **v4 — 2026-10-02.** Empat subbab digabung jadi dua; paragraf posisi diberi judul paragraf "Position of this study". Isi dan sitasi v3 tetap.
>
> **v3 — 2026-10-02.** Dipadatkan (1.084 → ±690 kata); tiap karya diposisikan sebagai *apa yang diselesaikan → asumsinya → bedanya dengan studi ini*. Versi sebelumnya: `sec2-draft.md` di riwayat git (commit 9098746).

---

## 2. Related Work

### 2.1 Conformal prediction under dependence and for hierarchical data

Barber et al. bound the coverage gap of conformal prediction by the total-variation
distance between the data distribution and its exchangeable counterpart [A1], a
bound that holds whatever causes the violation but offers no constructive remedy.
Specific departures have been handled separately: covariate shift with known or
estimable likelihood ratios [A4], spatial data [A7] and network dependence [A8].
Bhattacharyya and Barber treat groups whose membership determines the covariate
shift [A3]; there the data remain exchangeable within each group, whereas in our
setting group proportions are stable and observations within a block are not
exchangeable. Fontana et al. review the framework and its variants [A11],
including the Mondrian construction, for which calibrated versions have since
been developed [D2].

Hierarchical exchangeability was formalized by Lee et al., who derive it for
groups of repeated measurements and extend both conformal prediction and the
jackknife+ [A2] to that setting [A0]; their threshold and guarantee are restated
in (1) and (2). Dunn et al. independently propose four constructions for two-layer
hierarchical models — pooling CDFs, double conformal, subsampling once and
repeated subsampling [A0b]. We take these results as given. Both works are
theoretical and evaluate on regression problems; [A0] uses simulated data and a
Lorenz-96 system. Neither asks a question that comes before applying the method:
given a clinical dataset and a target error rate, at which grouping, if any, can
the guarantee be enforced? Lee et al. point toward it themselves, noting that an
analyst may choose between many groups with few measurements or few groups with
many repeats, and that *characterizing the pros and cons of this tradeoff is an
important question to determine how study design affects inference in this
distribution-free setting* [A0]. We address its most elementary part — whether a
finite threshold exists for a given design — and then measure what happens on
clinical data when it does.

### 2.2 Multi-label, clinical and ECG applications

Papadopoulos reviews multi-label conformal methods [B1], which model dependence
between labels while assuming exchangeable samples; our setting requires the
converse. Maltoudoglou et al. reduce the cost of Label Powerset conformal
prediction by pruning [B3], and hierarchical multi-label classification without
conformal guarantees is well developed [B5], [B6]. Baheri and Shahbazi calibrate
at several resolutions of a label hierarchy and intersect the resulting sets [B2],
and Zhang et al. represent prediction sets as nodes of a label graph [B7,
preprint]. Both concern structure among labels; we use the label hierarchy only
to count calibration blocks per label (§3.4).

Strodthoff et al. established the PTB-XL benchmarks [F1] on the dataset of
[H1], [H2]; their residual architectures inform our backbones. Heartbeat-level
evaluation follows the inter-patient protocol, in which no subject contributes to
both training and evaluation [F2], [F10], because violating it inflates reported
performance [F3]. Conformal prediction in clinical medicine is surveyed in [E1],
with applications to anatomical landmark localization [E2] and multi-label
diagnosis coding [E3]; conformal risk control [C1] and conformal prediction for
time series [C4] extend the framework to general losses and to temporal data.

Several recent studies apply conformal prediction to ECG and related cardiac
signals. El Allam and Hamlich calibrate label-conditional Mondrian conformal
prediction on patient-disjoint PTB-XL partitions and show that calibration must
match the quantized model actually deployed [E7]; they also extend conformal
inference to edge-deployed wearables [E9]. Kinalioğlu shows, for PPG-based ICU
arrhythmia classification, that marginal coverage can hide per-class and
per-patient failures [E8]. Closest to the present study, Sim and Kim show that the
false-alarm bound of split conformal prediction in ECG monitoring counts
exchangeable subjects rather than beats, that too few calibration subjects
inflate the realized false-alarm rate, and that the unit carrying the guarantee
must be the unit raising alarms [E6]. Outside cardiology, group-aware conformal
calibration has been applied to patients nested in thousands of hospitals [E5].

**Position of this study.** These studies ask whether a procedure meets its
target on a given split. We ask the earlier question of whether a block-level
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
| Klaim salah yang dibuang | (1) "[D2] … *we use as a baseline*" — tidak ada baseline Mondrian; kini "calibrated versions have since been developed [D2]". (2) "*Our hierarchical closure* … enlarges sets" — metode itu tidak ada di naskah; kini "We use the label hierarchy only to count calibration blocks per label". (3) "[C1], [C4] … *machinery we build on*" — tidak dipakai; kini hanya "extend the framework". |
| Klaim dilunakkan | [F3] "*the single most common methodological error in the area*" belum terverifikasi; kini hanya "violating it inflates reported performance [F3]" |
| Duplikasi dibuang | Rumus HCP di §2.2 (sudah ada sebagai (1) di §3.2); [G1], [G2] kini hanya di §1 |
| Sitasi | Ke-31 kode yang ada di §2 lama tetap ada; tak satu pun dipindah ke klaim lain |
