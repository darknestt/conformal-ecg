# §5 Methods — Feasibility Diagnostics and Audit Protocol — Draft

> **Status:** 🟢 DRAF PROSA v2 · **Ditulis ulang:** 2026-10-01
> Sumber: [`../theory.md`](../theory.md) §1–5, sesudah audit prior-art 2026-10-01.
>
> **Perubahan identitas.** Versi 1 berjudul *"Proposed Method"* dan membuka dengan
> *"We develop three components"*. Audit prior-art menunjukkan tidak satu pun dari
> ketiga komponen itu baru (lihat tabel di akhir berkas). Bagian ini karena itu
> ditulis ulang sebagai **Metode sebuah studi audit**: setiap alat disitasi ke
> pemiliknya, dan yang dijual hanyalah temuan empiris di §8.
>
> **Kesalahan matematis yang diperbaiki.** Versi 1 menyatakan Prop. 3 sebagai
> *"the **coarsest** grouping that satisfies S2 is the join"*. Itu salah: partisi
> terkasar yang memenuhi S2 selalu satu blok tunggal. Yang benar *finest*.

---

## 5. Methods

This study introduces no new conformal procedure. It audits an existing one —
hierarchical conformal prediction (HCP) [A0] — on clinical ECG data, using three
diagnostics assembled from established results. We state the provenance of each
diagnostic where it is introduced, so that the reader can separate the tools we
borrow from the findings we report in §8.

Throughout, $K_1$ denotes the number of **calibration** blocks, $N_k$ the number of
observations in block $k$, $n=\sum_k N_k$, and $H$ the harmonic mean of the $N_k$.
We write $\rho(t)$ for the intraclass correlation of the indicator
$\mathbb{1}\{s\le t\}$ at threshold $t$ — not of the raw score.

### 5.1 Whether a finite threshold exists, and how precise it is

#### 5.1.1 Existence depends on the number of calibration blocks alone

**Proposition 1.** *The HCP threshold satisfies $\hat T < \infty$ if and only if
$\alpha \ge \tfrac{1}{K_1+1}$.*

This is an immediate consequence of the location of the $+\infty$ atom in
Theorem 1 of [A0], and we claim nothing beyond restating it in a form that can be
checked from metadata. Two consequences matter for the audit. First, the boundary
does not involve $N_k$: adding observations to existing blocks cannot make an
infeasible level feasible. Second, with $N_k=1$ for all $k$ it reduces to the
familiar split-conformal requirement $n \ge \lceil 1/\alpha\rceil - 1$.

> The inequality is **not strict**. At exactly $\alpha = \tfrac{1}{K_1+1}$ the
> threshold remains finite. An off-by-one here silently misreports feasibility for
> every grouping whose $K_1$ sits on the boundary.

#### 5.1.2 Precision under a compound-symmetric model

What follows is **not** distribution-free. It requires **Assumption (A)**: blocks
are independent and identically distributed, and within a block every pair of
indicators has the same correlation $\rho(t)$, **not depending on $N_k$**
(compound symmetry).

Rewriting the HCP threshold shows that it is determined by
$\hat G(t)=\frac{1}{K_1}\sum_k \bar F_k(t)$, the **unweighted** mean of block-level
empirical CDFs. Under (A), the standard variance of an unweighted mean of cluster
means applies [White & Thomas 2005; Lai 2021]:

$$
\operatorname{Var}\big(\hat G(t)\big) \;=\; \frac{\sigma^2(t)\,[\,1+(H-1)\rho(t)\,]}{K_1 H},
\qquad \sigma^2(t)=F(t)\{1-F(t)\}.
$$

Under (A) the variance tends to $\sigma^2\rho/K_1$ as $N_k\to\infty$. **This floor
is a property of compound symmetry, not of clustered data in general.** If
within-block correlation decays with separation — as plausibly holds for
consecutive beats within a long Holter record — the mean pairwise correlation can
shrink with $N_k$ and the floor disappears. We make no claim outside (A).

#### 5.1.3 The equal weighting is imposed, not chosen

The variance above belongs to the block-weighted estimator. The Kish effective
sample size describes a different, observation-weighted estimator, and the two
coincide only for uniform block sizes:

$$
\mathrm{DEff}_{\text{block}}(\rho)=\frac{n[1+(H-1)\rho]}{K_1H},
\qquad
\mathrm{DEff}_{\text{pooled}}(\rho)=1+\Big(\tfrac{\sum_k N_k^2}{n}-1\Big)\rho .
$$

The second expression is the familiar clustering design effect with
$b^*=\sum_k N_k^2/n$ [Gabler, Häder & Lahiri 1999], and comparing design effects
under equal versus size weighting of cluster means is established practice in
cluster-randomised trials [Kerry & Bland 2001]. We use both formulas as given.

What differs in the conformal setting is not the formula but the freedom to choose.
In a cluster-randomised trial, equal weighting is an analyst's choice and is known
to be inefficient under unequal cluster sizes; the standard remedy is
minimum-variance weighting [Kerry & Bland 2001; Zhan et al. 2021]. In HCP the
equal weighting follows from the structure of the threshold itself, and departing
from it can break the finite-sample guarantee rather than merely cost efficiency:
with $K_1=2$ singleton blocks and $\alpha=1/3$, HCP places mass $\tfrac13$ on each
calibration score and on $+\infty$, giving threshold $\max(s_1,s_2)$ and coverage
exactly $\tfrac23$. Moving the mass to $(\tfrac23, 0)$ while keeping $\tfrac13$ on
$+\infty$ makes the threshold $s_1$, and for continuous exchangeable scores the
coverage becomes $\mathbb{P}(s_0\le s_1)=\tfrac12<\tfrac23$. The practitioner is therefore held to the estimator that
cluster-sampling theory identifies as most affected by block imbalance, without
access to its usual remedy. We report this as an observation about the setting;
we do not prove that equal weights are the **only** valid choice.

On PTB-XL the two design effects differ by a factor of **15.7** at the recording
site level. On `strat_fold`, whose blocks are nearly uniform by construction, the
ratio is **1.000** — an internal check of the computation.

#### 5.1.4 The axis used to organise results

The audit in §8 needs an axis on which datasets with very different block geometry
can be compared. We use $\mathrm{DEff}_{\text{block}}$ evaluated with the
threshold-indicator ICC $\rho(t)$. Because $H$ enters only through $(H-1)\rho$, the
quantity predicts that dependence is harmless whenever blocks are near-singleton,
**however strong the within-block correlation**; raw $\rho$ alone predicts the
opposite. We state this prediction here, before the results.

We use this quantity only as an **ordering axis**, not as a calibrated effective
sample size. Noonan (2026) derives a closed-form effective sample size for
thresholds under clustering and shows that the correction currently used in the
conformal literature is the wrong quantity. Our axis shares its central ingredient
— the correlation of threshold indicators rather than of scores — but is a
heuristic under Assumption (A), and we defer to that work for the principled
quantity.

### 5.2 Which calibration groupings are admissible

A practitioner choosing a calibration grouping $g$ faces two requirements.

| | Condition | Character |
|---|---|---|
| **S1** Feasibility | $K_1(g) \ge \lceil 1/\alpha\rceil - 1$ | exact, from Proposition 1 |
| **S2** Sufficiency | every **declared** dependence source is nested within $g$ | exact, given the declaration |

S1 alone is insufficient: a grouping can admit a finite threshold while leaving
dependence unaccounted for across its blocks. S2 is only as complete as the list
of dependence sources supplied to it. It verifies nesting for **declared** sources;
an undeclared source passes vacuously. S2 is therefore a check on the consistency
of a stated assumption, not a test of it.

When declared sources are crossed rather than nested, the finest grouping
satisfying S2 for all of them is their **join** in the partition lattice — the
connected components of the graph that links two observations whenever they share
a block under any declared source. This is classical [Nelder 1965; Bailey 1977,
1996], as is the observation that joining several individually fine groupings can
collapse into a giant component [Zheng & Xu 2026]. Combined with Proposition 1 it
yields a design-level bound that we use as a diagnostic:

**Corollary (feasibility under crossed sources).** *If
$K_1(\mathcal{P}_1\vee\cdots\vee\mathcal{P}_m) < \lceil 1/\alpha\rceil - 1$, no HCP
calibration provides a finite threshold at level $\alpha$ while respecting all $m$
declared sources.*

> **Scope.** This is stated for the HCP family only. The difference from the
> leakage-control setting is one of kind rather than degree: there, a collapsed
> join degrades a split (fewer folds, higher variance); here, below
> $1/(K_1+1)$ no finite threshold exists at all.

The bound depends on which sources are declared, and that choice cannot be
verified from data. We therefore report it as a function of the declared set and
never as a property of a dataset. On PTB-XL, declaring `patient_id` and `site`
retains $K_1=34$ and remains feasible at $\alpha=0.05$; adding `device` collapses
the join to $K_1=5$; declaring all four available sources yields a single block.
Enumerating all $2^4-1$ joins on fold 9 shows that every grouping satisfying S2
for all four sources has $K_1=1$, so under that declaration no grouping satisfies
S1 and S2 together at any $\alpha\in\{0.01,0.05,0.10,0.20\}$.

### 5.3 Per-label feasibility on a label hierarchy

#### 5.3.1 Superset coverage reduces exactly to HCP

If the conformity score of a record is taken to be the maximum score over its true
labels, superset coverage is a marginal coverage statement about a scalar score,
and Theorem 1 of [A0] applies verbatim. **No new guarantee is obtained**; we use
the construction because it is the operationally correct way to obtain a
superset-valid prediction set.

#### 5.3.2 Per-label guarantees are bounded by the number of blocks carrying the label

That rare classes starve class-conditional calibration is well established for
exchangeable data [Ding et al. 2023]. Under hierarchical dependence the unit that
must be counted changes from observations to blocks.

**Proposition 4 (necessary condition).** *A finite per-label HCP threshold for
label $\ell$ at level $\alpha$ requires $\alpha \ge \tfrac{1}{K_1(\ell)+1}$, where
$K_1(\ell)$ is the number of calibration blocks containing at least one instance
of $\ell$.*

The condition is **necessary, not sufficient**. Conditioning a test observation on
carrying $\ell$ selects its block with probability proportional to the fraction of
$\ell$-positive observations in that block, whereas a block enters the calibration
stratum merely by containing one. Unless that fraction is constant across blocks,
test and calibration blocks are not exchangeable, and the rank argument does not
deliver $\mathbb{P}(\ell\in\hat C\mid\ell\in Y)\ge1-\alpha$. The same size-biased
selection appears in the analysis of thresholds under clustering [Noonan 2026]. We
therefore use Proposition 4 only to **rule out** guarantees, never to certify them.

Because every block containing a label contains its ancestors, $K_1$ is monotone
toward the root of the hierarchy, so the necessary condition fails along a frontier
in the taxonomy that can be mapped from metadata before any model is trained.
Controlling $m$ labels jointly by a union bound raises the requirement to
$K_1(\ell) \ge \lceil m/\alpha\rceil - 1$ for every $\ell$.

### 5.4 Audit protocol

All three diagnostics are computed from metadata alone, before training. The
empirical audit in §8 then measures coverage and prediction-set size of naive split
conformal (B1) and HCP (B12) on held-out blocks, over 200 random block-level
splits per configuration. To rule out the objection that calibration behaviour is
an artefact of a weak model, every audit is repeated on three backbones spanning a
more than hundredfold range of capacity (0.10 M, 7.2 M and 16.0 M parameters).
Diagnostics computed from metadata — $K_1$, $K_1(\ell)$ and the join structure —
must be identical across backbones, and we report them per backbone as a negative
control on the pipeline. PTB-XL fold 10 is never used.

---

## Catatan penyusunan

### Status setiap alat — yang dipinjam vs yang dilaporkan

| Alat di §5 | Pemilik | Kami klaim |
|---|---|---|
| Prop. 1 | [A0] Teorema 1 | hanya penyajian dapat-diperiksa |
| Varians $\hat G$, rata-rata harmonik | White & Thomas 2005; Lai 2021 | — |
| $\mathrm{DEff}$ pooled, $b^*$ | Kish 1965; Gabler, Häder & Lahiri 1999 | — |
| Bobot sama vs ukuran | Kerry & Bland 2001 | **pengamatan**: pada HCP bobot sama dipaksakan |
| ESS untuk ambang | **Noonan 2026** | sumbu kami hanya heuristik pengurut |
| Join, komponen terhubung | Nelder 1965; Bailey 1977, 1996 | — |
| Keruntuhan join | Zheng & Xu 2026 (← Guvenilir & Dogan, ⚠️ belum diverifikasi) | **pengamatan**: akibatnya kategoris pada HCP |
| Prop. 4 | Ding dkk. 2023 (versi exchangeable) | satuan hitung = blok; **perlu saja** |
| Pembobotan-ukuran | Noonan 2026 | — |

### Konflik dengan aturan pustaka (35 rujukan, 5 tahun) — BELUM DIPUTUSKAN

Atribusi prior art tidak dapat ditawar: memakai hasil tanpa menyitasi pemiliknya
adalah alasan tolak langsung. Rencana di bawah meminimalkan pelanggaran dengan
memakai **sumber baru yang benar-benar menyatakan hasilnya**, dan menyisakan sumber
klasik hanya bila tidak ada penggantinya.

| Kebutuhan sitasi | Klasik (< 2021) | Pengganti ≥ 2021 yang menyatakan hasil yang sama | Usul |
|---|---|---|---|
| Bobot sama vs ukuran, obat varians-minimum | Kerry & Bland 2001 | **Zhan dkk. 2021**, PLoS ONE ✅ teks penuh dibaca | pakai Zhan; Kerry & Bland lewat Zhan |
| Rata-rata harmonik, rata-rata klaster tanpa bobot | White & Thomas 2005 | **Lai 2021**, Psychological Methods ⚠️ cuplikan | pakai Lai sesudah teks penuh dicek |
| $b^*$, DEff klaster tak seimbang | Gabler dkk. 1999 | **Noonan 2026** ⚠️ praterbit | **pertahankan Gabler** — Noonan belum peer-reviewed |
| Join, kekisi partisi | Nelder 1965; Bailey 1977/1996 | — | nyatakan sebagai aljabar baku **tanpa sitasi**, atau 1 sitasi Bailey 1996 |
| Keruntuhan join | — | Zheng & Xu 2026 ⚠️ praterbit | pakai, ditandai praterbit |
| Kelas langka, conformal terkondisi-kelas | — | **Ding dkk. 2023**, NeurIPS (Scopus ✅) | pakai |
| ESS ambang, pembobotan-ukuran | — | Noonan 2026 ⚠️ praterbit | pakai, ditandai praterbit |

**Tambahan bersih minimal: 5 rujukan** (Zhan 2021, Lai 2021, Ding 2023, Noonan 2026,
Zheng & Xu 2026) + **1–2 klasik** (Gabler 1999; opsional Bailey 1996). Agar tetap 35,
5–7 rujukan lama harus keluar — kandidat terkuat adalah rujukan yang dulu menopang
klaim kebaruan yang kini sudah dicabut.

### Yang wajib diverifikasi sebelum submit

| Hal | Alasan |
|---|---|
| Teks penuh Kerry & Bland 2001 | Sitasi dari cuplikan indeks + tinjauan Zhan dkk. |
| Teks penuh Noonan 2026 §2 | Klaim "berbagi bahan pokok" belum dicocokkan dengan rumusnya |
| Guvenilir & Dogan | Atribusi sekunder; jangan sitasi sebelum ditemukan |
| White & Thomas 2005; Lai 2021 | Rumus harmonik dari cuplikan Google Scholar |

### Yang sengaja tidak dimasukkan

- **Tidak ada angka hasil eksperimen** selain angka struktural dari metadata
  (15,7×; $K_1$; join). Hasil cakupan adalah materi §8.
- Klaim lama *"No amount of additional measurement per block can reduce it"*
  **dicabut** — salah di luar simetri majemuk.
- Klaim lama *"the tradeoff suggested in the discussion of [A0] does not exist"*
  **dicabut** — bergantung pada lantai varians yang tidak berlaku umum.
