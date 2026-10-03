# Lampiran A–C

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

### A.3 Equal weighting in HCP

Cluster-randomized trials compare equal and size-proportional weighting of
cluster means, and equal weighting loses efficiency when cluster sizes vary
[I1, A13]. In HCP it cannot be replaced, so the practitioner is tied to the
estimator that cluster-sampling theory regards as most sensitive to block
imbalance, without the standard remedy. We state this as an observation and do
not prove that equal weights are the only valid choice. On PTB-XL the two design
effects of (4) differ by a factor of 15.7 at the site level, while on
`strat_fold`, whose blocks are almost uniform by construction, their ratio is
1.000, an internal check of the computation.

Departing from equal weights can break the guarantee, not merely cost
efficiency. Take $K_1=2$ singleton blocks and $\alpha=1/3$. HCP assigns mass $\tfrac13$ to each
calibration score and to $+\infty$, so the threshold is $\max(s_1,s_2)$ and the
coverage is exactly $\tfrac23$. Shifting the calibration mass to $(\tfrac23,0)$
while leaving $\tfrac13$ at $+\infty$ makes the threshold $s_1$, and for continuous
exchangeable scores the coverage drops to $\mathbb{P}(s_0\le s_1)=\tfrac12<\tfrac23$.

## Appendix B. Interim Conclusions on MIT-BIH

The reading of the MIT-BIH evidence was revised three times, and its statistical
strength a fourth time (§6.4). The second revision was our own mistake: it
compared analyses with different calibration sizes (about 24,800 against 16,500
beats) and attributed the difference to block balance. Table B.1 lists each
interim conclusion with the control that overturned it.

**Table B.1.** Interim conclusions on MIT-BIH and the control that overturned each.

| Stage | Interim conclusion | Overturned by |
|---|---|---|
| 1 | HCP improves on naive split conformal | Permutation control: 81–107% of the gap is mechanical |
| 2 | The deficit is driven by block-size imbalance | 2×2 factorial: imbalance significant at 0/3 levels, clustering at 3/3 |
| 3 | The deficit increases monotonically with ICC | PTB-XL: ICC 0.35 yet no deficit |
| 4 | The deficit tracks $1+(H-1)\rho$ | — stands |
| 5 | The B1 deficit against the permutation null is significant for two of three backbones | Record-level jackknife over the 22 DS2 records: every 95% CI includes zero |

## Appendix C. Observability of Blocks in Challenge 2021

The seven non-duplicate source folders of the PhysioNet/CinC Challenge 2021
collection [H5] hold 66,416 records, from `ningbo` (34,905) to
`st_petersburg_incart` (74); its `ptb-xl` folder (21,837 records) repeats PTB-XL,
and the two totals give the official 88,253. In a sample of 42 headers from all
seven sources, none of the fields (`#Age`, `#Sex`, `#Dx`, `#Rx`, `#Hx`, plus
`#Sx` in five sources) is documented as a patient identifier; since this is a
sample and header schemas differ between sources, we claim nothing beyond it.
Repetition, by contrast, is documented: the INCART source is described as
*"74 annotated ECGs ... extracted from 32 Holter monitor recordings,"* and the
`ptb-xl` folder holds 21,837 records from 18,869 patients. The bound
$\alpha_{\min}\ge 1/8$ of §4.1 refers to the source partition, not to the
dataset, and no $\alpha_{\min}$ is reported for the patient partition.
Sufficiency also presumes a latent block structure [A0]; if similarity within an
institution faded gradually, for instance with the closeness of acquisition
protocols, the condition would be ill-posed rather than merely unobservable.
These checks needed about 0.5 MB of downloads (70 index files and 42 headers) out
of a 12.6 GB dataset, before any preprocessing or training.

---

## Catatan penyusunan

| Hal | Keputusan |
|---|---|
| Penomoran | Persamaan (A.1); Tabel B.1 menjadi TABLE IX |
