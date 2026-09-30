# §5 Proposed Method — Draft

> **Status:** 🟢 DRAF PROSA · **Dibuat:** 2026-09-30
> Mengikuti [`outline.md`](outline.md) §5. Sumber: [`../theory.md`](../theory.md) §2–5.
>
> **Gerbang yang masih aktif:**
> 🔴 Kalimat pembatas ruang lingkup Kor. 3.2 **tidak boleh dilonggarkan** sebelum
> statistikawan mereview.
> ⚠️ Pemisahan bebas-distribusi vs Asumsi (A) harus eksplisit di setiap klaim.

---

## 5. Proposed Method

We develop three components. Section 5.1 characterises how study design governs
both the validity and the efficiency of hierarchical conformal prediction.
Section 5.2 turns the validity half into a decision procedure that runs before any
model is trained. Section 5.3 extends both to hierarchical multi-label outputs.

Throughout, $K$ denotes the number of calibration blocks, $N_k$ the number of
observations in block $k$, $n=\sum_k N_k$, and $H$ the **harmonic** mean of the
$N_k$. We write $\rho$ for the intraclass correlation of the conformity score
indicator at the calibration threshold.

### 5.1 How study design governs validity and efficiency (C6)

#### 5.1.1 Validity depends on the number of blocks alone

**Proposition 1.** *The HCP threshold satisfies $\hat T < \infty$ if and only if
$\alpha \ge \tfrac{1}{K_1+1}$.*

The proof is immediate from the location of the $+\infty$ atom in Theorem 1 of
[A0] and requires no distributional assumption whatsoever. Two corollaries follow.

**Corollary 1.1.** *The feasibility boundary does not depend on $N_k$.* Adding
measurements to existing blocks cannot make an infeasible error rate feasible.

**Corollary 1.3.** *When $N_k = 1$ for all $k$, the condition reduces to
$n \ge \lceil 1/\alpha\rceil - 1$*, recovering the familiar split-conformal
requirement.

> The inequality is **not strict**. At exactly $\alpha = \tfrac{1}{K_1+1}$ the
> threshold remains finite. An off-by-one here silently misreports feasibility for
> every grouping whose $K_1$ sits on the boundary.

#### 5.1.2 Efficiency has a floor that measurements cannot break

The following requires **Assumption (A)**: a one-way random-effects model for the
score indicator, with block effects of variance $\sigma_b^2$ and residual variance
$\sigma_w^2$, giving $\rho = \sigma_b^2/(\sigma_b^2+\sigma_w^2)$.

**Proposition 2′ (non-uniform blocks).** *Under (A) with arbitrary $N_k$,*

$$
\operatorname{Var}(\hat G) \;=\; \frac{\sigma^2\,[\,1+(H-1)\rho\,]}{K H},
\qquad H = \Big(\tfrac{1}{K}\textstyle\sum_k N_k^{-1}\Big)^{-1}.
$$

As $N_k \to \infty$ the variance tends to $\sigma^2\rho/K$, a floor set entirely by
the number of blocks. **No amount of additional measurement per block can reduce
it.** Validity and efficiency are therefore governed by the same resource, and the
tradeoff suggested in the discussion of [A0] does not exist in the direction one
might expect: both improve with $K$.

#### 5.1.3 The Kish design effect measures the wrong estimator

HCP weights blocks equally, so it estimates $\hat G$, the unweighted mean of
block-level means. The Kish effective sample size instead describes the
observation-weighted pooled estimator. The two coincide **only** for uniform
block sizes:

$$
\mathrm{DEff}_{\text{block}}(\rho)=\frac{n[1+(H-1)\rho]}{KH}
\;\xrightarrow{\rho\to1}\;\frac{n}{K}=\bar N
\quad\text{(arithmetic mean)},
$$
$$
\mathrm{DEff}_{\text{Kish}}=\frac{\sum_k N_k^2}{n}
\quad\text{(size-weighted mean)}.
$$

On PTB-XL the discrepancy reaches **15.7×** at the recording site level. On
`strat_fold`, whose blocks are nearly uniform by construction, the ratio is
**1.000** — an internal check that the derivation is correct.

> **Retraction reported in the paper itself.** An earlier version of this work
> claimed that ordering groupings by design effect is *opposite* to ordering them
> by feasibility, citing `site` (feasible) against `device` (infeasible). That
> claim was an artefact of using $\mathrm{DEff}_{\text{Kish}}$ — a quantity
> belonging to an estimator HCP does not use. With the correct measure the two
> orderings coincide, as they must: at $\rho=1$,
> $\mathrm{DEff}_{\text{block}} = n/K$ decreases monotonically in $K$ while
> feasibility increases in $K$. Both are driven by the same variable. The claim is
> withdrawn.

#### 5.1.4 Which quantity predicts calibration loss

Proposition 2′ makes a falsifiable prediction that distinguishes it from the
intuitive alternative. Because $H$ enters only through the product $(H-1)\rho$,
dependence should be harmless whenever blocks are near-singleton, **however
strong the within-block correlation**. A dataset with high $\rho$ but $H \approx 1$
should behave exactly like independent data.

We test this in §8 by placing two datasets with opposite block geometry on a
single axis. We state here, in advance of the result, the quantity the theory
commits us to: the coverage deficit should track $1+(H-1)\rho$, and **not** $\rho$
alone.

### 5.2 A pre-registration diagnostic for block sufficiency (C7)

A practitioner choosing a calibration grouping faces two distinct requirements,
which the literature does not separate.

| | Condition | Character |
|---|---|---|
| **S1** Feasibility | $K_1(g) \ge \lceil 1/\alpha\rceil - 1$ | combinatorial, **exact** |
| **S2** Sufficiency | every dependence source is nested within $g$ | combinatorial, **exact** |

S1 alone is insufficient: a grouping may admit a finite threshold while still
leaving dependence unaccounted for across its blocks.

**Proposition 3.** *When dependence sources are not nested, the coarsest grouping
that satisfies S2 is the **join** of the corresponding partitions in the partition
lattice.*

**Corollary 3.2 (impossibility).** *There exist crossed designs for which no
grouping satisfies S1 and S2 simultaneously at a given $\alpha$.*

> 🔴 **Scope, stated verbatim and not to be softened:** *Corollary 3.2 is proved
> for the HCP/Dunn family. Whether it holds for every distribution-free method
> that relies on exchangeability between blocks remains an open question.*

**The existence claim is verified constructively on real data.** Enumerating all
$2^4-1$ joins of subsets of $\{\texttt{patient\_id}, \texttt{site},
\texttt{nurse}, \texttt{device}\}$ on PTB-XL fold 9 yields eight groupings that
satisfy S2, **all of which collapse to $K_1 = 1$**. None satisfies S1 and S2
simultaneously at $\alpha \in \{0.01, 0.05, 0.10, 0.20\}$. The finest
S2-satisfying grouping is $\texttt{site} \vee \texttt{nurse}$, already a single
block; every other S2-satisfying grouping is coarser still. The impossibility is
therefore exhaustive on this lattice rather than established by sampling.

On PTB-XL the join of `patient_id` with `nurse` and `site` retains $K_1=34$ and
remains feasible at $\alpha=0.05$; adding `device` collapses it to $K_1=5$, and
the join of all four sources yields a single block. The diagnostic returns a
**deterministic verdict** — there is no sampling error, and it can be computed
from a data dictionary before a single patient is recruited.

### 5.3 Per-label feasibility on a label hierarchy (C8)

#### 5.3.1 Superset coverage reduces exactly to HCP

We state this plainly rather than presenting it as a contribution. If the
conformity score for a record is taken to be the maximum score over its true
labels, then superset coverage is a marginal coverage statement about a scalar
score, and Theorem 1 of [A0] applies verbatim. **No new guarantee is obtained.**
We include the construction because it is the operationally correct way to obtain
a superset-valid prediction set, not because it is novel.

#### 5.3.2 Per-label guarantees do not reduce, and yield a new boundary

Per-label validity is a different statement, and it is here that the feasibility
question reappears in sharper form.

**Proposition 4.** *A per-label guarantee for label $\ell$ at level $\alpha$
requires $\alpha \ge \tfrac{1}{K_1(\ell)+1}$, where $K_1(\ell)$ is the number of
calibration blocks containing at least one instance of $\ell$.*

The binding resource is not the number of calibration points carrying the label,
but the number of **blocks** that contain it — a quantity that can be orders of
magnitude smaller for rare labels.

**Proposition 5 (monotonicity).** *If $\ell'$ is an ancestor of $\ell$ in the
label hierarchy, then $K_1(\ell') \ge K_1(\ell)$.*

Monotonicity implies the existence of a **feasibility frontier**: a level of the
taxonomy above which all labels are feasible and below which some are not. On
PTB-XL, at $\alpha=0.05$, all five superclasses are feasible, six of twenty-three
subclasses are not, and twenty-four of forty-four SCP codes are not. The frontier
lies strictly between the superclass and subclass levels.

**Corollary 5.1 (simultaneous coverage).** *Controlling $m$ labels simultaneously
requires $K_1(\ell) \ge \lceil m/\alpha\rceil - 1$ for every $\ell$*, which at
$m=44$ is unattainable for all but one SCP code.

**Corollary 5.2.** *Upward closure never introduces an infeasible label into a
prediction set*, since every ancestor of a feasible label is itself feasible by
Proposition 5. This is the formal content of the hierarchical closure operation.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Pemisahan asumsi | §5.1.1 bebas-distribusi; §5.1.2 dibuka dengan "requires **Assumption (A)**" |
| Pencabutan | §5.1.3 memuat pencabutan klaim "dua sumbu berlawanan" **di dalam naskah** |
| Kor. 3.2 | Kalimat pembatas ditulis **verbatim** dan ditandai tidak boleh dilonggarkan |
| C8 sepele | §5.3.1 menyatakan sendiri bahwa cakupan-superset tereduksi persis — dijadikan Metode, bukan klaim |
| §5.1.4 | Ramalan dinyatakan **sebelum** hasil, dengan rujukan maju ke §8. Ini yang mencegah tuduhan HARKing |

### Yang sengaja TIDAK dimasukkan

- **Tidak ada angka hasil eksperimen.** Validasi empiris Prop 2′ (kurva DEff,
  Spearman gabungan) adalah materi §8 Results, bukan §5. Memasukkannya ke Metode
  akan mengaburkan batas antara yang diramalkan dan yang diamati.
- Tidak ada klaim atas Teorema 1 — selalu dirujuk sebagai milik [A0].

### Yang masih menghalangi

| Penghalang | Dampak |
|---|---|
| 🔴 Review statistikawan atas Kor. 3.2 | Ruang lingkup klaim ketidakmungkinan |
| 🟡 Review atas Asumsi (A) di §5.1.2 | Apakah model efek acak satu arah memadai untuk indikator biner |
