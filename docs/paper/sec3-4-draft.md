# §3 Preliminaries · §4 Problem Formulation — working draft

> **Status:** 🟡 DRAF · **Dibuat:** 2026-09-30 · Bahasa Inggris (bentuk akhir naskah)
>
> Sumber: [`../theory.md`](../theory.md) §0–1, §4.2. Setiap pernyataan di sini **sudah tertentu** dan kebal terhadap hasil H0.
>
> ⚠️ Tanda 🔴/🟡 dari `theory.md` **dibawa serta**. Jangan dihapus saat menyalin ke naskah final.

---

## 3. Preliminaries and Notation

### 3.1 Hierarchical data and blocked exchangeability

Sections 3.1–3.2 restate the framework of Lee et al. [A0] for completeness of notation; none of it is claimed as ours.

Let the calibration data consist of $K$ blocks (groups), where block $k$ contains $N_k$ observations $Z_{k,1},\dots,Z_{k,N_k}$. Write $n=\sum_{k} N_k$ for the total number of observations. In our clinical setting a block is a patient and an observation is a single 10-second ECG recording, but the framework is agnostic to what defines a block.

Standard conformal prediction assumes the calibration and test points are exchangeable. Lee et al. [A0] show that this fails whenever observations are nested within groups, and introduce **hierarchical exchangeability**: blocks are exchangeable with one another, and observations are exchangeable *within* each block, but observations are not exchangeable *across* the full pooled sample.

Let $s(\cdot)$ denote a nonconformity score, fixed independently of the calibration data, and write $s_{k,i}=s(Z_{k,i})$. Let
$$Q_\beta(F)=\inf\{t:F(t)\ge\beta\}$$
denote the lower $\beta$-quantile of a distribution $F$ on $\mathbb{R}\cup\{+\infty\}$.

### 3.2 Hierarchical conformal prediction (HCP)

Writing $K_1$ for the number of calibration blocks, HCP calibrates the threshold as

$$\hat T \;=\; Q_{1-\alpha}\!\left(\sum_{k=1}^{K_1}\sum_{i=1}^{N_k}\frac{1}{(K_1+1)N_k}\,\delta_{s_{k,i}}\;+\;\frac{1}{K_1+1}\,\delta_{+\infty}\right).\tag{1}$$

Two features of (1) drive everything that follows. First, **each block contributes the same total mass** $\frac{1}{K_1+1}$ regardless of how many observations it contains; within a block that mass is divided evenly across its $N_k$ members. Second, a mass of $\frac{1}{K_1+1}$ is placed at $+\infty$, which is the price of not knowing the test block in advance.

Lee et al. [A0, Thm. 1] prove the two-sided guarantee
$$1-\alpha\;\le\;\mathbb{P}\{Y_{\text{test}}\in\hat C(X_{\text{test}})\}\;\le\;1-\alpha+\frac{2}{K_1+1}\tag{2}$$
for a test point drawn from a previously unseen block.

### 3.3 Label hierarchy

PTB-XL organises diagnoses as a three-level tree: 5 diagnostic **superclasses**, 23 **subclasses**, and 44 diagnostic **SCP statements**. A recording may carry several labels simultaneously, so the target is a *set* $Y\subseteq\mathcal{L}$ rather than a single class. We write $\mathrm{parent}(\ell)$ for the parent of label $\ell$ and call a set $\mathcal{C}$ **upward closed** if $\ell\in\mathcal{C}\Rightarrow\mathrm{parent}(\ell)\in\mathcal{C}$.

---

## 4. Problem Formulation

Equation (1) is a complete recipe once $K_1$, $\{N_k\}$ and $\alpha$ are given. It does not, however, say anything about *whether the resulting guarantee carries any information*. That is the question we take up.

### 4.1 When is a non-trivial guarantee possible?

**Proposition 1 (feasibility).** $\hat T<\infty$ if and only if
$$\alpha\;\ge\;\frac{1}{K_1+1}.\tag{3}$$

*Proof.* The finite atoms in (1) carry total mass
$$\sum_{k}\sum_{i}\frac{1}{(K_1+1)N_k}=\sum_k\frac{N_k}{(K_1+1)N_k}=\frac{K_1}{K_1+1}.$$
Let $M=\max_{k,i}s_{k,i}$ and let $\hat F$ denote the weighted CDF in (1). Then $\hat F(t)\le\frac{K_1}{K_1+1}$ for every finite $t$, with equality at $t=M$. Since $Q_{1-\alpha}(\hat F)=\inf\{t:\hat F(t)\ge1-\alpha\}$, the threshold is finite iff $\frac{K_1}{K_1+1}\ge1-\alpha$. $\square$

When (3) fails, $\hat C(X)=\mathcal{L}$ for every input: the guarantee (2) holds vacuously and conveys nothing.

**Corollary 1.1 (independence of $N_k$).** The right-hand side of (3) does not involve $N_k$. **Collecting more measurements per block can never restore feasibility**, no matter how many are collected.

**Corollary 1.2.** The minimum number of calibration blocks is $K_{\min}(\alpha)=\lceil 1/\alpha\rceil-1$. At $\alpha=0.05$ this is 19 blocks, not 20.

**Corollary 1.3 (consistency with split conformal).** If $N_k=1$ for all $k$ then $K_1=n$ and (3) reduces to $n\ge1/\alpha-1$, the textbook requirement for split conformal. We verified this numerically as a check on both the derivation and the implementation.

**Remark (strictness).** An earlier version of this work stated (3) as a strict inequality. That is wrong at the boundary: at $\alpha=\frac{1}{K_1+1}$ exactly, the finite mass $\frac{K_1}{K_1+1}$ *equals* the level $1-\alpha$, so the infimum is attained at $M$ and the threshold is finite. Simulation at $K_1=19,\alpha=0.05$ gives empirical coverage $0.9512\ge0.95$. We report the correction because the non-strict form is what makes Corollary 1.3 line up with the standard split-conformal condition — a useful cross-check for readers.

### 4.2 Multiple dependence sources and crossed designs

Real clinical datasets carry several candidate blocking variables at once: patient, device, operator, site. These need not be nested.

**Definition (sufficiency).** A partition $\mathcal{Q}$ is *sufficient* for a dependence source with partition $\mathcal{P}$ if $\mathcal{P}$ refines $\mathcal{Q}$, i.e. every $\mathcal{P}$-block lies entirely inside a single $\mathcal{Q}$-block.

If $\mathcal{Q}$ is not sufficient for $\mathcal{P}$, then dependent observations are split across different $\mathcal{Q}$-blocks and are treated as independent — exactly the error the hierarchical machinery exists to prevent.

**Proposition 2 (crossed designs force the join).** For $\mathcal{Q}$ to be sufficient for both $\mathcal{P}_1$ and $\mathcal{P}_2$, it must be coarser than each. The finest such $\mathcal{Q}$ is the join $\mathcal{P}_1\vee\mathcal{P}_2$ in the partition lattice: the connected components of the graph linking two observations whenever they share a $\mathcal{P}_1$-block or a $\mathcal{P}_2$-block. This is a standard fact about the partition lattice; we state it because its consequence for conformal calibration is what matters here.

**Corollary 2.1.** $K(\mathcal{P}_1\vee\mathcal{P}_2)\le\min\{K(\mathcal{P}_1),K(\mathcal{P}_2)\}$, hence
$$\alpha_{\min}(\mathcal{P}_1\vee\mathcal{P}_2)\;\ge\;\max\{\alpha_{\min}(\mathcal{P}_1),\alpha_{\min}(\mathcal{P}_2)\}.$$

**Corollary 2.2 (impossibility).** If $K_1(\mathcal{P}_1\vee\mathcal{P}_2)<\lceil1/\alpha\rceil-1$ then no HCP calibration yields a non-trivial guarantee at level $\alpha$ while accounting for both dependence sources. The same holds for any number of sources with their joint join. This is a property of the study design, not a shortcoming of any estimator.

**Scope of Corollary 2.2.** We prove Corollary 2.2 for the HCP/Dunn family. Whether it extends to every distribution-free method whose validity rests on between-block exchangeability remains open. We conjecture that it does, by analogy with the unavoidability of the $n\ge1/\alpha-1$ requirement for split conformal, but we do not claim it.

### 4.3 What the guarantee is *about*: multi-label targets

For multi-label outputs the notion of coverage must be chosen, not inherited. We use **superset coverage**
$$\mathbb{P}\big(Y_{\text{test}}\subseteq\hat C(X_{\text{test}})\big)\;\ge\;1-\alpha.\tag{4}$$

Superset coverage (4) is not a new result. Theorem 1 never touches the structure of the label space; it only requires a fixed scalar score. Setting $s(x,Y)=\max_{\ell\in Y}s_\ell(x)$ makes $\{Y\subseteq\hat C\}\iff s(x,Y)\le\hat T$, so HCP applies unchanged. We present this as method, not contribution.

The substantive question is the **label-conditional** target
$$\mathbb{P}\big(\ell\in\hat C(X)\,\big|\,\ell\in Y\big)\;\ge\;1-\alpha,\tag{5}$$
which does not reduce, and which we take up in §5.3.

**Records with $Y=\emptyset$.** In PTB-XL, 411 recordings (1.9%) carry no diagnostic superclass. Under (4) these are covered trivially, so including them would inflate measured coverage without evidence. We exclude them from calibration and evaluation and report the exclusion.

---

## Checklist sebelum bagian ini masuk naskah final

- [ ] Atribusi Lee-Barber-Willett tegas di kalimat pertama §3.1 dan §3.2
- [ ] Persamaan (1) dan (2) dikutip dengan nomor persamaan aslinya
- [ ] Kalimat pembatas Kor. 3.2 **utuh**, belum dilonggarkan — jangan dilunakkan sebelum statistikawan mereview
- [ ] Pengakuan bahwa (4) sepele **tidak dihapus**
- [ ] Catatan koreksi ketaksamaan tetap ada — menunjukkan pemeriksaan silang, bukan kelemahan
- [ ] Pengecualian 411 rekaman disebut di Metode **dan** di Hasil
