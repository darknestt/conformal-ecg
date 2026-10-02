# Lampiran A–B

> **v7 — 2026-10-02.** Diparafrasekan dari v6 (commit 3edc1f0). Persamaan (A.1), angka 0,9512 dan contoh kontra tetap.

---

## Appendix A. Supplementary Derivations

### A.1 The boundary case of Proposition 1

An earlier version of this work wrote (3) as a strict inequality, which fails at
the boundary. At $\alpha=1/(K_1+1)$ the finite mass $K_1/(K_1+1)$ is exactly
$1-\alpha$, the infimum is reached at $M$, and the threshold is finite. A
simulation with $K_1=19$ and $\alpha=0.05$ yields an empirical coverage of
$0.9512\ge0.95$. Only the non-strict form is consistent with the split-conformal
case $N_k=1$.

### A.2 Variance under compound symmetry

Under Assumption (A) of §3.2, $\hat G(t)$ has variance

$$
\operatorname{Var}\big(\hat G(t)\big) \;=\; \frac{\sigma^2(t)\,[\,1+(H-1)\rho(t)\,]}{K_1 H},
\qquad \sigma^2(t)=F(t)\{1-F(t)\}.
\tag{A.1}
$$

As $N_k\to\infty$ this tends to $\sigma^2\rho/K_1$. The floor is a feature of
compound symmetry rather than of clustered data in general: when correlation
decays with distance, as is plausible for consecutive beats in a long Holter
record, the average pairwise correlation may shrink as $N_k$ grows and the floor
vanishes. We make no claim outside (A).

### A.3 Departing from equal weights can break the guarantee

Take $K_1=2$ singleton blocks and $\alpha=1/3$. HCP assigns mass $\tfrac13$ to each
calibration score and to $+\infty$, so the threshold is $\max(s_1,s_2)$ and the
coverage is exactly $\tfrac23$. Shifting the calibration mass to $(\tfrac23,0)$
while leaving $\tfrac13$ at $+\infty$ makes the threshold $s_1$, and for continuous
exchangeable scores the coverage drops to $\mathbb{P}(s_0\le s_1)=\tfrac12<\tfrac23$.

## Appendix B. Interim Conclusions on MIT-BIH

The reading of the MIT-BIH evidence went through three revisions (§6.4). The
second revision was our own mistake: it set analyses with different calibration
sizes (about 24,800 against 16,500 beats) side by side and ascribed the
difference to block balance. Table B.1 records each interim conclusion alongside
the control that overturned it.

**Table B.1.** Interim conclusions on MIT-BIH and the control that overturned each.

| Stage | Interim conclusion | Overturned by |
|---|---|---|
| 1 | HCP improves on naive split conformal | Permutation control: 81–107% of the gap is mechanical |
| 2 | The deficit is driven by block-size imbalance | 2×2 factorial: imbalance significant at 0/3 levels, clustering at 3/3 |
| 3 | The deficit increases monotonically with ICC | PTB-XL: ICC 0.35 yet no deficit |
| 4 | The deficit tracks $1+(H-1)\rho$ | — stands |

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Penomoran | Persamaan (A.1); Tabel B.1 menjadi TABLE IX |
