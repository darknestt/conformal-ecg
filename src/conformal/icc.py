"""Estimasi korelasi intra-blok (ICC) -- masukan untuk Prop. 2 dan E11b.

Kish n_eff hanya fungsi UKURAN blok dan secara struktural buta terhadap rho
(lihat docs/theory.md Kor. 2.1). Untuk mengukur kekuatan dependensi yang
sebenarnya, rho harus diestimasi langsung.

Dipakai estimator ANOVA satu arah untuk desain tak seimbang:

    MSB = sum_k N_k (Ybar_k - Ybar)^2 / (K - 1)
    MSW = sum_k sum_i (Y_ki - Ybar_k)^2 / (n - K)
    N0  = (n - sum_k N_k^2 / n) / (K - 1)
    ICC = (MSB - MSW) / (MSB + (N0 - 1) MSW)

Untuk skor conformal, kuantitas yang relevan bagi Prop. 2 adalah rho(t) --
ICC dari INDIKATOR 1{s <= t}, bukan dari skor mentah. Keduanya disediakan.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = ["ICCResult", "intraclass_correlation", "icc_at_threshold", "icc_curve"]


@dataclass(frozen=True)
class ICCResult:
    icc: float
    n_blocks: int
    n_points: int
    n0: float
    """Ukuran blok efektif ANOVA; sama dengan N bila blok seragam."""

    ms_between: float
    ms_within: float
    ci: tuple[float, float] | None = None

    def __str__(self) -> str:
        ci = f"  CI95 [{self.ci[0]:.4f}, {self.ci[1]:.4f}]" if self.ci else ""
        return f"ICC={self.icc:.4f}  K={self.n_blocks}  n={self.n_points}  N0={self.n0:.2f}{ci}"


def _anova_icc(values: np.ndarray, codes: np.ndarray, k: int) -> tuple[float, float, float, float]:
    n = values.size
    if k < 2:
        raise ValueError(f"butuh >= 2 blok, diterima {k}")
    if n == k:
        raise ValueError("setiap blok hanya berisi 1 titik; ragam intra-blok tak terdefinisi")

    sizes = np.bincount(codes, minlength=k).astype(float)
    jumlah = np.bincount(codes, weights=values, minlength=k)
    mean_k = jumlah / sizes
    mean_all = values.mean()

    ss_between = float(np.sum(sizes * (mean_k - mean_all) ** 2))
    ss_within = float(np.sum((values - mean_k[codes]) ** 2))

    ms_between = ss_between / (k - 1)
    ms_within = ss_within / (n - k)
    n0 = (n - np.sum(sizes**2) / n) / (k - 1)

    penyebut = ms_between + (n0 - 1) * ms_within
    icc = 0.0 if penyebut == 0 else (ms_between - ms_within) / penyebut
    return float(icc), float(ms_between), float(ms_within), float(n0)


def intraclass_correlation(
    values: np.ndarray,
    blocks: np.ndarray,
    n_bootstrap: int = 0,
    rng: np.random.Generator | None = None,
    clip: bool = True,
) -> ICCResult:
    """ICC ANOVA satu arah, dengan CI bootstrap pada level BLOK.

    Bootstrap harus meresample blok, bukan titik. Meresample titik akan
    mengulang persis kesalahan yang penelitian ini kritik.

    ``clip=True`` memangkas ke [0, 1]; estimator ANOVA dapat bernilai negatif
    ketika rho sejati mendekati nol.
    """
    values = np.asarray(values, dtype=float).ravel()
    blocks = np.asarray(blocks).ravel()
    if values.shape != blocks.shape:
        raise ValueError(f"values {values.shape} dan blocks {blocks.shape} tidak sepadan")

    _, codes = np.unique(blocks, return_inverse=True)
    k = int(codes.max()) + 1
    icc, msb, msw, n0 = _anova_icc(values, codes, k)

    ci = None
    if n_bootstrap > 0:
        rng = np.random.default_rng() if rng is None else rng
        indeks_blok = [np.flatnonzero(codes == b) for b in range(k)]
        sampel = []
        for _ in range(n_bootstrap):
            terpilih = rng.integers(0, k, size=k)
            idx = np.concatenate([indeks_blok[b] for b in terpilih])
            kode_baru = np.repeat(np.arange(k), [indeks_blok[b].size for b in terpilih])
            try:
                nilai, *_ = _anova_icc(values[idx], kode_baru, k)
            except ValueError:
                continue
            sampel.append(np.clip(nilai, 0.0, 1.0) if clip else nilai)
        if sampel:
            ci = (float(np.percentile(sampel, 2.5)), float(np.percentile(sampel, 97.5)))

    return ICCResult(
        icc=float(np.clip(icc, 0.0, 1.0)) if clip else icc,
        n_blocks=k,
        n_points=values.size,
        n0=n0,
        ms_between=msb,
        ms_within=msw,
        ci=ci,
    )


def icc_at_threshold(scores: np.ndarray, blocks: np.ndarray, t: float, **kwargs) -> ICCResult:
    """rho(t) -- ICC dari indikator 1{s <= t}, kuantitas yang dipakai Prop. 2."""
    return intraclass_correlation(
        (np.asarray(scores, dtype=float) <= t).astype(float), blocks, **kwargs
    )


def icc_curve(
    scores: np.ndarray,
    blocks: np.ndarray,
    quantiles: np.ndarray | None = None,
) -> list[tuple[float, float, float]]:
    """Kurva rho(t) pada beberapa kuantil skor. Kembalikan (kuantil, t, rho)."""
    scores = np.asarray(scores, dtype=float).ravel()
    if quantiles is None:
        quantiles = np.array([0.5, 0.75, 0.9, 0.95, 0.99])

    keluaran = []
    for q in quantiles:
        t = float(np.quantile(scores, q))
        indikator = (scores <= t).astype(float)
        # Ambang ekstrem dapat membuat indikator konstan; ICC tak terdefinisi.
        if indikator.min() == indikator.max():
            continue
        keluaran.append((float(q), t, icc_at_threshold(scores, blocks, t).icc))
    return keluaran
