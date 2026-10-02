# §3 Preliminaries · §4 Problem Formulation

> **v3 — 2026-10-02.** Ditulis ulang dan dipadatkan (976 → ±700 kata). Semua definisi, persamaan (1)–(5), Proposisi 1–2, Korolari 1.1–2.2 dan Remark tetap; hanya prosa pengantarnya yang diringkas. Versi sebelumnya: `sec3-4-draft.md` di riwayat git (commit 9098746).

---

## 3. Preliminaries and Notation

### 3.1 Hierarchical data and blocked exchangeability

Sections 3.1–3.2 restate the framework of Lee et al. [A0] to fix notation; none
of it is claimed as ours. The calibration data consist of $K$ blocks, block $k$
holding $N_k$ observations $Z_{k,1},\dots,Z_{k,N_k}$, with $n=\sum_k N_k$. In our
setting a block is typically a patient and an observation a 10-second recording,
but the framework does not depend on what defines a block. Lee et al. [A0] show
that standard exchangeability fails when observations are nested within groups,
and introduce **hierarchical exchangeability**: blocks are exchangeable with one
another and observations are exchangeable within each block, but observations
are not exchangeable across the pooled sample.

Let $s(\cdot)$ be a nonconformity score fixed independently of the calibration
data, write $s_{k,i}=s(Z_{k,i})$, and let
$$Q_\beta(F)=\inf\{t:F(t)\ge\beta\}$$
denote the lower $\beta$-quantile of a distribution $F$ on $\mathbb{R}\cup\{+\infty\}$.

### 3.2 Hierarchical conformal prediction (HCP)

With $K_1$ calibration blocks, HCP sets the threshold

$$\hat T \;=\; Q_{1-\alpha}\!\left(\sum_{k=1}^{K_1}\sum_{i=1}^{N_k}\frac{1}{(K_1+1)N_k}\,\delta_{s_{k,i}}\;+\;\frac{1}{K_1+1}\,\delta_{+\infty}\right).\tag{1}$$

Each block contributes the same total mass $\frac{1}{K_1+1}$, divided evenly among
its $N_k$ observations, and a further mass $\frac{1}{K_1+1}$ sits at $+\infty$ —
the price of not knowing the test block in advance. For a test point from a
previously unseen block, Lee et al. [A0, Thm. 1] prove
$$1-\alpha\;\le\;\mathbb{P}\{Y_{\text{test}}\in\hat C(X_{\text{test}})\}\;\le\;1-\alpha+\frac{2}{K_1+1}.\tag{2}$$

### 3.3 Label hierarchy

PTB-XL arranges diagnoses in a three-level tree of 5 superclasses, 23 subclasses
and 44 diagnostic SCP statements. A recording may carry several labels, so the
target is a set $Y\subseteq\mathcal{L}$. We write $\mathrm{parent}(\ell)$ for the
parent of label $\ell$, and call $\mathcal{C}$ upward closed if
$\ell\in\mathcal{C}\Rightarrow\mathrm{parent}(\ell)\in\mathcal{C}$.

---

## 4. Problem Formulation

Equation (1) fully specifies the threshold once $K_1$, $\{N_k\}$ and $\alpha$ are
given, but it does not say whether the resulting guarantee carries any
information. That is the question we take up.

### 4.1 When is a non-trivial guarantee possible?

**Proposition 1 (feasibility).** $\hat T<\infty$ if and only if
$$\alpha\;\ge\;\frac{1}{K_1+1}.\tag{3}$$

*Proof.* The finite atoms in (1) carry total mass
$$\sum_{k}\sum_{i}\frac{1}{(K_1+1)N_k}=\sum_k\frac{N_k}{(K_1+1)N_k}=\frac{K_1}{K_1+1}.$$
Let $M=\max_{k,i}s_{k,i}$ and let $\hat F$ denote the weighted CDF in (1). Then $\hat F(t)\le\frac{K_1}{K_1+1}$ for every finite $t$, with equality at $t=M$. Since $Q_{1-\alpha}(\hat F)=\inf\{t:\hat F(t)\ge1-\alpha\}$, the threshold is finite iff $\frac{K_1}{K_1+1}\ge1-\alpha$. $\square$

When (3) fails, $\hat C(X)=\mathcal{L}$ for every input, and (2) holds vacuously.

**Corollary 1.1 (independence of $N_k$).** The right-hand side of (3) does not
involve $N_k$: collecting more measurements per block can never restore
feasibility.

**Corollary 1.2.** The minimum number of calibration blocks is
$K_{\min}(\alpha)=\lceil 1/\alpha\rceil-1$; at $\alpha=0.05$ this is 19, not 20.

**Corollary 1.3 (consistency with split conformal).** If $N_k=1$ for all $k$, then
$K_1=n$ and (3) reduces to the familiar split-conformal requirement
$n\ge1/\alpha-1$, which we also verified numerically.

**Remark (strictness).** An earlier version of this work stated (3) as a strict
inequality, which is wrong at the boundary: at $\alpha=\frac{1}{K_1+1}$ the finite
mass $\frac{K_1}{K_1+1}$ equals $1-\alpha$, the infimum is attained at $M$, and the
threshold is finite. Simulation at $K_1=19$, $\alpha=0.05$ gives empirical coverage
$0.9512\ge0.95$. Only the non-strict form agrees with Corollary 1.3.

### 4.2 Multiple dependence sources and crossed designs

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
This is a standard fact about partition lattices; what matters here is its
consequence for calibration.

**Corollary 2.1.** $K(\mathcal{P}_1\vee\mathcal{P}_2)\le\min\{K(\mathcal{P}_1),K(\mathcal{P}_2)\}$, hence
$$\alpha_{\min}(\mathcal{P}_1\vee\mathcal{P}_2)\;\ge\;\max\{\alpha_{\min}(\mathcal{P}_1),\alpha_{\min}(\mathcal{P}_2)\}.$$

**Corollary 2.2 (impossibility).** If $K_1(\mathcal{P}_1\vee\mathcal{P}_2)<\lceil1/\alpha\rceil-1$, no HCP calibration yields a non-trivial guarantee at level $\alpha$ while accounting for both dependence sources; the same holds for any number of sources and their joint join. This is a property of the study design, not a shortcoming of any estimator.

**Scope of Corollary 2.2.** We prove Corollary 2.2 for the HCP/Dunn family.
Whether it extends to every distribution-free method whose validity rests on
between-block exchangeability remains open. We conjecture that it does, by
analogy with the unavoidable $n\ge1/\alpha-1$ requirement of split conformal, but
we do not claim it.

### 4.3 What the guarantee is about: multi-label targets

For multi-label outputs the notion of coverage has to be chosen. We use
**superset coverage**,
$$\mathbb{P}\big(Y_{\text{test}}\subseteq\hat C(X_{\text{test}})\big)\;\ge\;1-\alpha.\tag{4}$$
This is not a new result: Theorem 1 of [A0] only requires a fixed scalar score,
and setting $s(x,Y)=\max_{\ell\in Y}s_\ell(x)$ gives
$\{Y\subseteq\hat C\}\iff s(x,Y)\le\hat T$, so HCP applies unchanged. The
substantive question is the **label-conditional** target
$$\mathbb{P}\big(\ell\in\hat C(X)\,\big|\,\ell\in Y\big)\;\ge\;1-\alpha,\tag{5}$$
which does not reduce in this way and is taken up in §5.3. The 411 PTB-XL records
(1.9%) with no diagnostic superclass would be covered trivially under (4); we
exclude them from calibration and evaluation.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Dipertahankan utuh | Definisi blok, $Q_\beta$, (1)–(5), Prop. 1 + bukti, Kor. 1.1–1.3, Remark (0,9512), Definisi sufficiency, Prop. 2, Kor. 2.1–2.2, kalimat ruang lingkup Kor. 2.2 (kata per kata kecuali tanda baca) |
| Dipadatkan | Prosa pengantar §3.1–3.2, penjelasan dua sifat (1), paragraf "superset coverage is not a new result" digabung ke §4.3 |
| Belum boleh dilunakkan | Kalimat ruang lingkup Kor. 2.2 — sampai statistikawan mereview |
