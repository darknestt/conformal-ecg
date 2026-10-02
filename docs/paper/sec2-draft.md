# §2 Related Work — Draft

> **Status:** 🟢 DRAF PROSA · **Dibuat:** 2026-09-30
> Mengikuti [`outline.md`](outline.md) §2. Seluruh sitasi terverifikasi di
> [`../references.md`](../references.md) (35 artikel, 34 terindeks Scopus).
>
> **Aturan atribusi yang dikunci kerangka:** Lee, Barber & Willett **sudah**
> menyelesaikan exchangeability hierarkis. Kita **memakai**, bukan menemukan ulang.
> Kalimat pembuka §2.2 harus menyatakannya tanpa kabur.

---

## 2. Related Work

### 2.1 Conformal prediction under violations of exchangeability

Split conformal prediction attains finite-sample marginal coverage under a single
assumption: that calibration and test points are exchangeable. Barber et al. [A1]
give the sharpest available account of what happens when that assumption fails,
bounding the coverage gap by the total-variation distance between the observed
data distribution and its exchangeable counterpart. Their analysis is agnostic to
*why* exchangeability fails, which makes it broadly applicable but leaves the
practitioner without a constructive remedy for any particular violation.

A complementary line of work treats specific, structured departures. Weighted
conformal prediction handles covariate shift when likelihood ratios are known or
estimable [A4]; spatially indexed data are addressed in [A7]; network dependence
in [A8]. Bhattacharyya and Barber [A3] consider observations belonging to a finite
number of groups where *group membership determines the covariate shift* between
training and test distributions — for instance under stratified sampling.

In [A3] the data remain exchangeable *within* each group; what shifts is the
mixture over groups. The setting we study is the opposite: the group proportions
are stable, but observations within a block are not exchangeable with one
another. The vocabulary collides; the problems do not.

Fontana et al. [A11] provide the standard unified treatment of the conformal
framework and its variants, including the Mondrian (class-conditional)
construction of which we use a calibrated variant [D2] as a baseline.

### 2.2 Conformal prediction for hierarchical data

**The hierarchical exchangeability problem is solved, and not by us.** Lee, Barber
and Willett [A0] derive a hierarchical form of exchangeability for data organized
into groups of repeated measurements, and extend both conformal prediction and
jackknife+ [A2] to that setting. Their Theorem 1 gives the hierarchical conformal
prediction (HCP) threshold

$$
\hat T \;=\; Q_{1-\alpha}\!\left(\sum_{k}\sum_{i} \tfrac{1}{(K_1+1)N_k}\,
\delta_{s(Z_{k,i})} \;+\; \tfrac{1}{K_1+1}\,\delta_{+\infty}\right),
$$

with coverage at least $1-\alpha$ and, when scores are almost surely distinct, at
most $1-\alpha+\tfrac{2}{K_1+1}$. Dunn et al. [A0b] independently study two-layer
hierarchical models and introduce four constructions — pooling CDFs, double
conformal, subsampling once, and repeated subsampling — that address the same
setting.

Everything in the present paper takes this threshold as given. We do not
rederive it, and we claim no credit for it.

Both [A0] and [A0b] are developed as theory, and their empirical sections are
regression problems; [A0] evaluates on simulated data and a Lorenz-96 system.
Neither asks a question that is prior to applying the method at all: *given a
real clinical dataset and a target error rate, at which grouping — if any — can
the guarantee be enforced?* The $\tfrac{1}{K_1+1}$ atom at $+\infty$ makes this a
non-trivial question, because it renders the threshold infinite whenever
$\alpha < \tfrac{1}{K_1+1}$.

The authors of [A0] state the open question themselves in their discussion,
observing that an analyst may choose between many independent groups with few
measurements each or few groups with many repeats, and that *characterizing the
pros and cons of this tradeoff is an important question to determine how study
design affects inference in this distribution-free setting.* Section 5 addresses
the most elementary part of that question — whether a finite threshold exists at
all for a given design — and the remainder of the paper measures what happens on
real clinical data when it does.

### 2.3 Conformal prediction for multi-label and hierarchical label spaces

Papadopoulos [B1] reviews conformal methods for multi-label learning and organizes
them by output type, guarantee, and where label dependence enters. The review is
explicit that the surveyed literature rests on the exchangeability assumption
throughout — that is, it treats dependence **between labels** while assuming
independence **between samples**. Our setting requires the converse.

Maltoudoglou et al. [B3] address the computational cost of Label Powerset
conformal prediction by pruning label sets whose $p$-values cannot exceed the
significance level. Hierarchical multi-label classification without conformal
guarantees is well developed [B5], as is its application to clinical
recommendation [B6].

Two recent efforts are close enough to require explicit differentiation. Baheri
and Amiri Shahbazi [B2] define a conformity function at each of several
resolutions and **intersect** the resulting sets, distributing the miscoverage
budget across scales; the operation shrinks sets and pays a Bonferroni-type price
in coverage. Our hierarchical closure moves in the opposite direction: it
**enlarges** sets upward along the label taxonomy, and coverage is non-decreasing
as a result. Zhang et al. [B7, preprint] represent prediction sets as nodes in a
directed acyclic graph, using coarse labels to *implicitly represent* their
descendants — a downward compression, again opposite in direction to upward
closure.

### 2.4 Uncertainty quantification for ECG and the inter-patient protocol

Strodthoff et al. [F1] established the benchmark suite for PTB-XL [H1, H2], whose
residual architectures inform the backbones used here. Evaluation on heartbeat-level arrhythmia data
follows the inter-patient protocol, in which no subject contributes to both
training and evaluation [F2, F10]; violating this separation inflates reported
performance and is the single most common methodological error in the area [F3].

Reviews of uncertainty quantification in clinical deep learning [G1] and the
FUTURE-AI consensus guideline [G2] both identify calibrated uncertainty as a
prerequisite for deployment, making the requirement a matter of published
consensus rather than authorial preference. Conformal prediction specifically in
clinical medicine is surveyed in [E1], with recent applications to anatomical
landmark localization [E2] and multi-label diagnosis coding [E3]. Conformal risk
control [C1] and conformal prediction for time series [C4] supply the loss-control
and temporal machinery we build on.

Work on conformal prediction for ECG and related cardiac signals has grown
quickly. El Allam and Hamlich calibrate label-conditional Mondrian conformal
prediction on patient-disjoint PTB-XL partitions and show that calibration must
match the quantized model actually deployed [E7], and extend conformal inference
to adaptive, edge-deployed wearables [E9]. Kinalioğlu audits PPG-based ICU
arrhythmia classification and shows that marginal coverage can conceal per-class
and per-patient failures, using patient-clustered resampling [E8]. Closest to the
present study, Sim and Kim show for ECG monitoring that the finite-sample
false-alarm bound of split conformal prediction counts exchangeable subjects
rather than beats, that too few calibration subjects inflate the realized
false-alarm rate, and that the unit carrying the guarantee must be the unit
raising alarms [E6]. Outside cardiology, group-aware conformal calibration has
been applied to patients nested in thousands of hospitals [E5].

These studies evaluate whether a conformal procedure achieves its target on a
given split. The present paper asks a prior, design-stage question that they
leave implicit: whether a block-level coverage guarantee is feasible at all once
every declared dependence source — including crossed sources and label-level
conditioning — is respected, and whether ignoring block structure costs coverage
once mechanical effects of the finite-block correction are controlled.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Panjang target | ~900 kata — padat, empat blok sesuai kerangka |
| Atribusi A0 | Dinyatakan **dua kali**: kalimat pembuka §2.2 dan penutup paragraf kedua |
| B2 dan B7 | Dibedakan **secara eksplisit** karena judulnya mirip; reviewer pasti menanyakannya |
| Praterbit | Ditandai sebagai praterbit di badan teks, bukan hanya di daftar pustaka |
| Klaim celah | Diletakkan sebagai **pertanyaan yang mendahului penerapan**, bukan sebagai "belum ada yang melakukan X" |

### Yang sengaja TIDAK ditulis

- Tidak ada klaim bahwa exchangeability hierarkis adalah kontribusi kami (bekas C1, dicabut)
- Tidak ada klaim superioritas atas [A0]/[A0b] — keduanya fondasi, bukan pesaing
- Tidak ada angka hasil; §2 harus kebal terhadap hasil eksperimen
