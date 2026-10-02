# §3 Problem Formulation and HCP Feasibility

> **v5 — 2026-10-02.** Diparafrasekan dan dipadatkan dari v4 (commit 2bbdbec). Pernyataan formal (Proposisi 1–3, Corollary 1–2, Definisi, Asumsi (A), kalimat ruang lingkup Corollary 2) dan persamaan (1)–(6) kata per kata sama; hanya prosa penghubung yang diringkas.

---

## 3. Problem Formulation and HCP Feasibility

Section 3.1 restates the framework of Lee et al. [A0] to fix notation; none of it
is claimed as ours. Sections 3.2–3.4 derive three feasibility diagnostics from
established results and cite the source of each where it enters, so that
borrowed tools are not mistaken for findings.

### 3.1 Hierarchical calibration

The calibration data consist of $K$ blocks, block $k$ holding $N_k$ observations
$Z_{k,1},\dots,Z_{k,N_k}$, with $n=\sum_k N_k$ and $H$ the harmonic mean of the
$N_k$. Here a block is typically a patient and an observation a 10-second
recording, but the framework does not depend on what defines a block. Lee et al.
[A0] show that standard exchangeability fails when observations are nested
within groups and introduce **hierarchical exchangeability**: blocks are
exchangeable with one another and observations are exchangeable within each
block, but not across the pooled sample.

Let $s(\cdot)$ be a nonconformity score fixed independently of the calibration
data, write $s_{k,i}=s(Z_{k,i})$, and let $Q_\beta(F)=\inf\{t:F(t)\ge\beta\}$ be
the lower $\beta$-quantile of a distribution $F$ on $\mathbb{R}\cup\{+\infty\}$.
With $K_1$ calibration blocks, HCP sets the threshold

$$\hat T \;=\; Q_{1-\alpha}\!\left(\sum_{k=1}^{K_1}\sum_{i=1}^{N_k}\frac{1}{(K_1+1)N_k}\,\delta_{s_{k,i}}\;+\;\frac{1}{K_1+1}\,\delta_{+\infty}\right).\tag{1}$$

Each block carries total mass $1/(K_1+1)$, shared evenly among its $N_k$
observations, and a further $1/(K_1+1)$ sits at $+\infty$ — the price of not
knowing the test block in advance. For a test point from a previously unseen
block, Lee et al. [A0, Thm. 1] prove
$$1-\alpha\;\le\;\mathbb{P}\{Y_{\text{test}}\in\hat C(X_{\text{test}})\}\;\le\;1-\alpha+\frac{2}{K_1+1}.\tag{2}$$

### 3.2 Finite-threshold feasibility

Equation (1) fixes the threshold once $K_1$, $\{N_k\}$ and $\alpha$ are given, but
does not say whether the resulting guarantee is informative.

**Proposition 1 (feasibility).** $\hat T<\infty$ if and only if
$$\alpha\;\ge\;\frac{1}{K_1+1}.\tag{3}$$

*Proof.* The finite atoms in (1) carry total mass
$\sum_k N_k/\{(K_1+1)N_k\}=K_1/(K_1+1)$, so the weighted CDF $\hat F$ in (1)
satisfies $\hat F(t)\le K_1/(K_1+1)$ for every finite $t$, with equality at
$t=M=\max_{k,i}s_{k,i}$. Since $Q_{1-\alpha}(\hat F)=\inf\{t:\hat F(t)\ge1-\alpha\}$,
the threshold is finite iff $K_1/(K_1+1)\ge1-\alpha$. ∎

When (3) fails, $\hat C(X)=\mathcal{L}$ for every input and (2) holds vacuously.
Proposition 1 restates a consequence of the $+\infty$ atom in Theorem 1 of [A0]
in a form checkable from metadata, and we claim nothing beyond that. Three of its
features matter here: the bound does not involve $N_k$, so more measurements per
block can never restore feasibility; it is not strict, so a grouping lying on it
is feasible (Appendix A.1); and with $N_k=1$ for all $k$ it reduces to the
familiar split-conformal requirement $n\ge1/\alpha-1$, which we also verified
numerically.

**Corollary 1.** The minimum number of calibration blocks is
$K_{\min}(\alpha)=\lceil 1/\alpha\rceil-1$; at $\alpha=0.05$ this is 19, not 20.

**Precision.** Feasibility is distribution-free; precision is not. It requires
**Assumption (A)**: blocks are independent and identically distributed, and every
pair of indicators $\mathbb{1}\{s\le t\}$ within a block has the same correlation
$\rho(t)$, which does not depend on $N_k$ (compound symmetry). Here $\rho(t)$ is
the intraclass correlation of the indicator at threshold $t$, not of the raw
score. The HCP threshold is determined by $\hat G(t)=\frac{1}{K_1}\sum_k \bar F_k(t)$,
the unweighted mean of block-level empirical CDFs, whose variance under (A) is
the standard one for an unweighted mean of cluster means [I2],
$\sigma^2(t)[1+(H-1)\rho(t)]/(K_1H)$ with $\sigma^2(t)=F(t)\{1-F(t)\}$
(Appendix A.2). This variance belongs to a block-weighted estimator, whereas the
Kish effective sample size describes an observation-weighted one, and the two
design effects coincide only for uniform block sizes:

$$
\mathrm{DEff}_{\text{block}}(\rho)=\frac{n[1+(H-1)\rho]}{K_1H},
\qquad
\mathrm{DEff}_{\text{pooled}}(\rho)=1+\Big(\frac{\sum_k N_k^2}{n}-1\Big)\rho .
\tag{6}
$$

The second is the standard design effect for unequal cluster sizes, and equal
versus size weighting of cluster means is a familiar choice in cluster-randomized
trials, where equal weighting is known to be inefficient under unequal cluster
sizes and is usually replaced by minimum-variance weights [I1, A13]. In HCP it is
not a choice: it is fixed by the structure of the threshold, and departing from
it can break the guarantee rather than merely cost efficiency (Appendix A.3).
The practitioner is thus bound to the estimator that cluster-sampling theory
finds most affected by block imbalance, without its usual remedy; we report this
as an observation and do not prove that equal weights are the only valid choice.
On PTB-XL the two design effects differ by a factor of 15.7 at the site level,
and on `strat_fold`, whose blocks are nearly uniform by construction, their ratio
is 1.000, an internal check of the computation.

**The axis used to organize results.** To compare datasets with very different
block geometry we order configurations by the variance-inflation factor
$\mathrm{DEff}=1+(H-1)\rho$. Because $H$ enters only through $(H-1)\rho$, the factor
predicts that dependence is harmless whenever blocks are near-singleton, however
strong the within-block correlation — the opposite of what raw $\rho$ suggests.
The primary analysis takes $\rho$ from conformity scores and is repeated with the
indicator correlation $\rho(t)$ (§5.4); when the axis was adopted is recorded in
§6.4. The axis only orders configurations and is not a calibrated effective
sample size: Noonan derives a closed-form effective sample size for thresholds
under clustering and shows that the correction currently used in the conformal
literature is the wrong quantity [P1]. Our axis shares its central ingredient,
the correlation of threshold indicators, but is a heuristic under (A), and we
defer to that work for the principled quantity.

### 3.3 Crossed dependence sources

Clinical datasets often carry several candidate blocking variables at once —
patient, device, operator, site — and these need not be nested.

**Definition (sufficiency).** A partition $\mathcal{Q}$ is *sufficient* for a
dependence source with partition $\mathcal{P}$ if $\mathcal{P}$ refines
$\mathcal{Q}$, i.e. every $\mathcal{P}$-block lies inside a single
$\mathcal{Q}$-block. Otherwise dependent observations fall into different
$\mathcal{Q}$-blocks and are treated as independent.

**Proposition 2 (crossed designs force the join).** For $\mathcal{Q}$ to be
sufficient for both $\mathcal{P}_1$ and $\mathcal{P}_2$, it must be coarser than
each. The finest such $\mathcal{Q}$ is the join $\mathcal{P}_1\vee\mathcal{P}_2$ in
the partition lattice: the connected components of the graph linking two
observations whenever they share a $\mathcal{P}_1$-block or a $\mathcal{P}_2$-block.
Consequently $K(\mathcal{P}_1\vee\mathcal{P}_2)\le\min\{K(\mathcal{P}_1),K(\mathcal{P}_2)\}$
and $\alpha_{\min}(\mathcal{P}_1\vee\mathcal{P}_2)\ge\max\{\alpha_{\min}(\mathcal{P}_1),\alpha_{\min}(\mathcal{P}_2)\}$.

This is a standard fact about partition lattices; its consequence for
calibration is what matters here. Fig. 1 illustrates it on eight hypothetical
records: five patient blocks and three device blocks, each fine on its own,
leave only two blocks once both sources must be respected.

![**Fig. 1.** Schematic of Proposition 2 on eight hypothetical records (circles). Solid arcs link records of the same patient and dashed arcs records of the same device. A grouping sufficient for both sources must keep every linked pair in one block, so the finest such grouping is the join, the connected components (shaded). On PTB-XL the same mechanism collapses four declared sources to a single block (§5.1).](figures/fig1_join_schematic.png)

**Corollary 2 (impossibility).** If $K_1(\mathcal{P}_1\vee\mathcal{P}_2)<\lceil1/\alpha\rceil-1$, no HCP calibration yields a non-trivial guarantee at level $\alpha$ while accounting for both dependence sources; the same holds for any number of sources and their joint join. This is a property of the study design, not a shortcoming of any estimator.

**Scope of Corollary 2.** We prove Corollary 2 for the HCP/Dunn family. Whether
it extends to every distribution-free method whose validity rests on
between-block exchangeability remains open. We conjecture that it does, by
analogy with the unavoidable $n\ge1/\alpha-1$ requirement of split conformal, but
we do not claim it.

**Admissible groupings.** A calibration grouping $g$ is admissible at level
$\alpha$ if it satisfies **(S1) feasibility**, $K_1(g)\ge\lceil 1/\alpha\rceil-1$
(exact, by Proposition 1), and **(S2) sufficiency**: every *declared* dependence
source is nested within $g$ (exact, given the declaration). S1 alone is not
enough, because a grouping can admit a finite threshold while leaving dependence
across its blocks unaccounted for. S2 is only as complete as the declared list:
an undeclared source passes vacuously, so S2 checks the consistency of a stated
assumption rather than testing it. For crossed sources the finest grouping
satisfying S2 is their join (Proposition 2). Joins of individually fine groupings
are known to form giant components in leakage control [P2], but the consequence
here differs in kind: there a collapsed join degrades a split, whereas here,
below $1/(K_1+1)$, no finite threshold exists (Corollary 2). Because the declared
set cannot be verified from data, every verdict is reported as a function of that
set, never as a property of a dataset.

### 3.4 Label-conditional feasibility

PTB-XL arranges diagnoses in a three-level tree of 5 superclasses, 23 subclasses
and 44 diagnostic SCP statements. A recording may carry several labels, so the
target is a set $Y\subseteq\mathcal{L}$ and a notion of coverage must be chosen.
**Superset coverage**,
$$\mathbb{P}\big(Y_{\text{test}}\subseteq\hat C(X_{\text{test}})\big)\;\ge\;1-\alpha,\tag{4}$$
is not a new result: Theorem 1 of [A0] only requires a fixed scalar score, and
setting $s(x,Y)=\max_{\ell\in Y}s_\ell(x)$ gives
$\{Y\subseteq\hat C\}\iff s(x,Y)\le\hat T$, so HCP applies unchanged. The
substantive question is the **label-conditional** target
$$\mathbb{P}\big(\ell\in\hat C(X)\,\big|\,\ell\in Y\big)\;\ge\;1-\alpha,\tag{5}$$
which does not reduce in this way. Rare classes are known to starve
class-conditional calibration for exchangeable data [A12]; under hierarchical
dependence the unit to be counted becomes the block.

**Proposition 3 (necessary condition).** *A finite per-label HCP threshold for
label $\ell$ at level $\alpha$ requires $\alpha \ge \tfrac{1}{K_1(\ell)+1}$, where
$K_1(\ell)$ is the number of calibration blocks containing at least one instance
of $\ell$.*

The condition is necessary, not sufficient. Conditioning a test observation on
carrying $\ell$ selects its block with probability proportional to the fraction
of $\ell$-positive observations in that block, whereas a block enters the
calibration stratum merely by containing one. Unless that fraction is constant
across blocks, test and calibration blocks are not exchangeable, and the rank
argument does not deliver $\mathbb{P}(\ell\in\hat C\mid\ell\in Y)\ge1-\alpha$; the
same size-biased selection arises for thresholds under clustering [P1].
Proposition 3 is therefore used only to rule out guarantees, never to certify
them. Since every block containing a label also contains its ancestors,
$K_1(\ell)$ is monotone toward the root, and the condition fails along a frontier
in the taxonomy that can be mapped from metadata. Controlling $m$ labels jointly
by a union bound raises the requirement to $K_1(\ell)\ge\lceil m/\alpha\rceil-1$
for every $\ell$.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Kata per kata | Prop. 1 + bukti, Corollary 1, Definisi, Prop. 2, Corollary 2, "Scope of Corollary 2", Prop. 3, Asumsi (A), persamaan (1)–(6) |
| Diparafrasekan | Prosa penghubung §3.1–3.4, paragraf bobot sama, sumbu DEff, "Admissible groupings" |
| Struktur v4 → v3 | Lihat catatan di commit 2bbdbec |
