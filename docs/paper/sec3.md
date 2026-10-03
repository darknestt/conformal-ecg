# §3 Problem Formulation and HCP Feasibility

> **v7 — 2026-10-02.** Prosa penghubung diparafrasekan penuh dari v6 (commit 3edc1f0). Pernyataan formal (Proposisi 1–3 + bukti, Corollary 1–2, Definisi, "Scope of Corollary 2") dan persamaan (1)–(6) kata per kata sama. **2026-10-03:** persamaan dinomori ulang menurut urutan kemunculan — DEff (6)→(4), superset (4)→(5), label-conditional (5)→(6); rujukan silang di §4–§6 dan Lampiran A ikut diubah.

---

## 3. Problem Formulation and HCP Feasibility

The notation in §3.1 follows Lee et al. [A0] and is restated rather than
claimed. Sections 3.2–3.4 build three feasibility diagnostics from established
results and cite each source where it is used, so that borrowed tools stay
distinct from findings.

### 3.1 Hierarchical calibration

Calibration data are organized in $K$ blocks: block $k$ contains $N_k$
observations $Z_{k,1},\dots,Z_{k,N_k}$, the total is $n=\sum_k N_k$, and $H$ is the
harmonic mean of the $N_k$. In this study a block is usually a patient and an
observation a 10-second recording, although nothing in the framework depends on
how blocks are defined. Lee et al. [A0] show that nesting observations within
groups breaks ordinary exchangeability and replace it with **hierarchical
exchangeability**: blocks are exchangeable among themselves and observations are
exchangeable within a block, while the pooled sample is not.

Fix a nonconformity score $s(\cdot)$ independently of the calibration data, set
$s_{k,i}=s(Z_{k,i})$, and denote by $Q_\beta(F)=\inf\{t:F(t)\ge\beta\}$ the lower
$\beta$-quantile of a distribution $F$ on $\mathbb{R}\cup\{+\infty\}$. For $K_1$
calibration blocks, the HCP threshold is

$$\hat T \;=\; Q_{1-\alpha}\!\left(\sum_{k=1}^{K_1}\sum_{i=1}^{N_k}\frac{1}{(K_1+1)N_k}\,\delta_{s_{k,i}}\;+\;\frac{1}{K_1+1}\,\delta_{+\infty}\right).\tag{1}$$

Every block receives the same total mass $1/(K_1+1)$, split evenly over its $N_k$
observations, and a further $1/(K_1+1)$ is placed at $+\infty$; this is the cost
of not knowing in advance which block the test point comes from. When the test
point belongs to a block not seen during calibration, Lee et al. [A0, Thm. 1]
establish
$$1-\alpha\;\le\;\mathbb{P}\{Y_{\text{test}}\in\hat C(X_{\text{test}})\}\;\le\;1-\alpha+\frac{2}{K_1+1}.\tag{2}$$

### 3.2 Finite-threshold feasibility

Once $K_1$, $\{N_k\}$ and $\alpha$ are fixed, (1) determines the threshold, but it
does not reveal whether the resulting guarantee is informative.

**Proposition 1 (feasibility).** $\hat T<\infty$ if and only if
$$\alpha\;\ge\;\frac{1}{K_1+1}.\tag{3}$$

*Proof.* The finite atoms in (1) carry total mass
$\sum_k N_k/\{(K_1+1)N_k\}=K_1/(K_1+1)$, so the weighted CDF $\hat F$ in (1)
satisfies $\hat F(t)\le K_1/(K_1+1)$ for every finite $t$, with equality at
$t=M=\max_{k,i}s_{k,i}$. Since $Q_{1-\alpha}(\hat F)=\inf\{t:\hat F(t)\ge1-\alpha\}$,
the threshold is finite iff $K_1/(K_1+1)\ge1-\alpha$. ∎

If (3) is violated, $\hat C(X)=\mathcal{L}$ for every input and (2) is satisfied
only vacuously. Proposition 1 recasts a consequence of the $+\infty$ atom in
Theorem 1 of [A0] so that it can be checked from metadata; we claim nothing
further. Three of its properties matter for the audit. Since $N_k$ does not appear
in the bound, adding measurements to existing blocks never restores
feasibility. Since the inequality is not strict, a grouping lying exactly on the
boundary is still feasible (Appendix A.1). And when $N_k=1$ throughout, the bound
collapses to the familiar split-conformal condition $n\ge1/\alpha-1$, which we
also confirmed numerically.

**Corollary 1.** The minimum number of calibration blocks is
$K_{\min}(\alpha)=\lceil 1/\alpha\rceil-1$; at $\alpha=0.05$ this is 19, not 20.

**Precision.** Unlike feasibility, precision depends on distributional
assumptions. It requires **Assumption (A)**: blocks are independent and
identically distributed, and any two indicators $\mathbb{1}\{s\le t\}$ within one
block share a correlation $\rho(t)$ that does not vary with $N_k$ (compound
symmetry). The quantity $\rho(t)$ is thus the intraclass correlation of the
indicator at threshold $t$ rather than of the raw score. The HCP threshold is a
functional of $\hat G(t)=\frac{1}{K_1}\sum_k \bar F_k(t)$, the unweighted average
of the block-level empirical CDFs, and under (A) its variance takes the textbook
form for an unweighted mean of cluster means [I2],
$\sigma^2(t)[1+(H-1)\rho(t)]/(K_1H)$ with $\sigma^2(t)=F(t)\{1-F(t)\}$
(Appendix A.2). That variance refers to a block-weighted estimator, whereas the
Kish effective sample size refers to an observation-weighted one, and the two
design effects agree only when all blocks have the same size:

$$
\mathrm{DEff}_{\text{block}}(\rho)=\frac{n[1+(H-1)\rho]}{K_1H},
\qquad
\mathrm{DEff}_{\text{pooled}}(\rho)=1+\Big(\frac{\sum_k N_k^2}{n}-1\Big)\rho .
\tag{4}
$$

The second expression is the usual design effect for clusters of unequal size.
In a cluster-randomized trial, equal weighting of cluster means is an inefficient
option that is usually replaced by minimum-variance weights [I1, A13]; in HCP it
is built into the threshold, and abandoning it can invalidate the guarantee
(Appendix A.3).

**The axis used to organize results.** Datasets with very different block
geometry are compared through the variance-inflation factor
$\mathrm{DEff}=1+(H-1)\rho$. Because $H$ enters only through $(H-1)\rho$, the factor
predicts no harm from dependence whenever blocks are close to singletons, however
strong the within-block correlation. In the primary analysis $\rho$ is estimated
from conformity scores, and the analysis is repeated with the indicator
correlation $\rho(t)$ (§5.4); §6.4 records when the axis was adopted. The axis is
a heuristic under (A) that ranks configurations, not a calibrated effective
sample size; for that quantity we defer to Noonan, who derives a closed-form
effective sample size for thresholds under clustering and shows that the
correction now used in the conformal literature targets the wrong quantity [P1].

### 3.3 Crossed dependence sources

Clinical datasets frequently offer several candidate blocking variables at the
same time — patient, device, operator, site — and nothing guarantees that they
are nested.

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

The result is standard for partition lattices; what concerns us is its
implication for calibration. Fig. 2 illustrates it with eight hypothetical
records, where five patient blocks and three device blocks, each acceptable on
its own, shrink to two blocks once both sources have to be respected.

![**Fig. 2.** Schematic of Proposition 2 on eight hypothetical records (circles). Solid arcs link records of the same patient and dashed arcs records of the same device. A grouping sufficient for both sources must keep every linked pair in one block, so the finest such grouping is the join, the connected components (shaded). On PTB-XL the same mechanism collapses four declared sources to a single block (§5.1).](figures/fig2_join_schematic.png)

**Corollary 2 (impossibility).** If $K_1(\mathcal{P}_1\vee\mathcal{P}_2)<\lceil1/\alpha\rceil-1$, no HCP calibration yields a non-trivial guarantee at level $\alpha$ while accounting for both dependence sources; the same holds for any number of sources and their joint join. This is a property of the study design, not a shortcoming of any estimator.

**Scope of Corollary 2.** We prove Corollary 2 for HCP as defined in (1).
Whether it extends to the constructions of Dunn et al. [A0b], or to every
distribution-free method whose validity rests on between-block exchangeability,
remains open. We conjecture that it does, by analogy with the unavoidable
$n\ge1/\alpha-1$ requirement of split conformal, but we do not claim it.

**Admissible groupings.** We call a calibration grouping $g$ admissible at level
$\alpha$ when it passes two checks: **(S1) feasibility**,
$K_1(g)\ge\lceil 1/\alpha\rceil-1$, which is exact by Proposition 1, and **(S2)
sufficiency**, under which every *declared* dependence source is nested in $g$,
exact relative to that declaration. Passing S1 alone does not suffice, because a
grouping may admit a finite threshold yet leave dependence between its blocks
unaddressed. S2, in turn, can be no more complete than the list it is given: a
source left undeclared passes trivially, so S2 verifies that a stated assumption
is internally consistent rather than testing whether it holds. With crossed
sources the finest grouping that passes S2 is their join (Proposition 2). In
leakage control, joins of individually fine groupings are already known to form
giant components [P2]; the consequence here is of a different kind, since a
collapsed join there merely weakens a split, whereas here, below $1/(K_1+1)$, no
finite threshold exists at all (Corollary 2). Because no dataset can confirm the
declared set, each verdict is reported as a function of that set and never as a
property of the data.

### 3.4 Label-conditional feasibility

The PTB-XL diagnoses form a three-level tree with 5 superclasses, 23 subclasses
and 44 diagnostic SCP statements. Since one recording may carry several labels,
the target is a set $Y\subseteq\mathcal{L}$ and a notion of coverage has to be
selected. **Superset coverage**,
$$\mathbb{P}\big(Y_{\text{test}}\subseteq\hat C(X_{\text{test}})\big)\;\ge\;1-\alpha,\tag{5}$$
involves nothing new: Theorem 1 of [A0] needs only a fixed scalar score, and with
$s(x,Y)=\max_{\ell\in Y}s_\ell(x)$ one has $\{Y\subseteq\hat C\}\iff s(x,Y)\le\hat T$,
so HCP carries over unchanged. The substance lies in the **label-conditional**
target
$$\mathbb{P}\big(\ell\in\hat C(X)\,\big|\,\ell\in Y\big)\;\ge\;1-\alpha,\tag{6}$$
which admits no such reduction. For exchangeable data it is well known that rare
classes starve class-conditional calibration [A12]; under hierarchical
dependence the quantity to count is the number of blocks.

**Proposition 3 (necessary condition).** *A finite per-label HCP threshold for
label $\ell$ at level $\alpha$ requires $\alpha \ge \tfrac{1}{K_1(\ell)+1}$, where
$K_1(\ell)$ is the number of calibration blocks containing at least one instance
of $\ell$.*

The condition is necessary, not sufficient. When a test observation is
conditioned on carrying $\ell$, its block is drawn with probability proportional
to the share of $\ell$-positive observations it contains, whereas a calibration
block qualifies as soon as it contains a single one. Unless that share is the
same in every block, test and calibration blocks cease to be exchangeable and the
rank argument no longer yields $\mathbb{P}(\ell\in\hat C\mid\ell\in Y)\ge1-\alpha$;
thresholds under clustering face the same size-biased selection [P1].
Proposition 3 is accordingly used only to exclude guarantees, never to certify
them. Every block that contains a label also contains its ancestors, so
$K_1(\ell)$ cannot decrease toward the root, and the condition breaks along a
frontier of the taxonomy that metadata suffice to map. A union bound over $m$
jointly controlled labels raises the requirement to
$K_1(\ell)\ge\lceil m/\alpha\rceil-1$ for each $\ell$.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Kata per kata | Prop. 1 + bukti, Corollary 1, Definisi, Prop. 2, Corollary 2, "Scope of Corollary 2", Prop. 3, persamaan (1)–(6), keterangan Fig. 2 (skema join; Fig. 1 sejak 2026-10-03 adalah alur audit di §1) |
| Diparafrasekan | Seluruh prosa penghubung, Asumsi (A) (isi sama), paragraf bobot sama, sumbu DEff, "Admissible groupings", §3.4 |
