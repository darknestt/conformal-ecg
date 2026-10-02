# Lampiran A–B

> **v5 — 2026-10-02.** Dari v4 (commit 2bbdbec). Tabel B.1 kini didahului kalimat yang menyebutnya. Isi derivasi kata per kata sama.

---

## Appendix A. Supplementary Derivations

### A.1 The boundary case of Proposition 1

An earlier version of this work stated (3) as a strict inequality, which is wrong
at the boundary: at $\alpha=1/(K_1+1)$ the finite mass $K_1/(K_1+1)$ equals
$1-\alpha$, the infimum is attained at $M$, and the threshold is finite.
Simulation at $K_1=19$, $\alpha=0.05$ gives empirical coverage $0.9512\ge0.95$.
Only the non-strict form agrees with the split-conformal case $N_k=1$.

### A.2 Variance under compound symmetry

Under Assumption (A) of §3.2, the variance of $\hat G(t)$ is

$$
\operatorname{Var}\big(\hat G(t)\big) \;=\; \frac{\sigma^2(t)\,[\,1+(H-1)\rho(t)\,]}{K_1 H},
\qquad \sigma^2(t)=F(t)\{1-F(t)\}.
\tag{A.1}
$$

As $N_k\to\infty$ the variance tends to $\sigma^2\rho/K_1$. This floor belongs to
compound symmetry, not to clustered data in general: if correlation decays with
separation, as plausibly holds for consecutive beats in a long Holter record, the
mean pairwise correlation can shrink with $N_k$ and the floor disappears. We make
no claim outside (A).

### A.3 Departing from equal weights can break the guarantee

With $K_1=2$ singleton blocks and $\alpha=1/3$, HCP puts mass $\tfrac13$ on each
calibration score and on $+\infty$, giving threshold $\max(s_1,s_2)$ and coverage
exactly $\tfrac23$; moving the mass to $(\tfrac23,0)$ while keeping $\tfrac13$ on
$+\infty$ makes the threshold $s_1$, and for continuous exchangeable scores the
coverage falls to $\mathbb{P}(s_0\le s_1)=\tfrac12<\tfrac23$.

## Appendix B. Interim Conclusions on MIT-BIH

Our reading of the MIT-BIH evidence changed three times (§6.4). The second stage
was our own error: it compared analyses with different calibration sizes (about
24,800 against 16,500 beats) and attributed the difference to block balance.
Table B.1 lists each interim conclusion together with the control that
overturned it.

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
