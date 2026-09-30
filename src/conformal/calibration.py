"""Metode kalibrasi conformal untuk data berstruktur blok.

Implementasi baseline B1 dan B12-B15 dari README §7. Tidak ada satu pun
pustaka publik yang menyediakan B12-B15, sehingga keempatnya ditulis di sini
langsung dari rumus aslinya.

Rujukan
-------
B1   Split conformal
     Vovk, Gammerman & Shafer (2005); rumus (5) pada Lee dkk. (2026)
B12  HCP -- Hierarchical Conformal Prediction
     Lee, Barber & Willett (2026), ACM J. Data Science, rumus (6) & Teorema 1
     DOI 10.1145/3786352
B13-B15  Pooling CDFs, Subsampling Once, Double Conformal
     Dunn, Wasserman & Ramdas (2022), JASA
     DOI 10.1080/01621459.2022.2060112

Catatan penting mengenai bobot
------------------------------
Split conformal meletakkan massa 1/(n+1) pada +inf, dengan n = jumlah SAMPEL.
HCP meletakkan massa 1/(K+1) pada +inf, dengan K = jumlah BLOK. Karena
K <= n, HCP selalu menghasilkan ambang yang lebih besar (lebih konservatif).
Selisih inilah yang memulihkan validitas di bawah dependensi blok -- dan yang
membuat jaminan menjadi mustahil ketika alpha <= 1/(K+1).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .quantile import quantile_with_infinity, weighted_quantile

__all__ = [
    "CalibrationResult",
    "split_conformal",
    "hcp",
    "pooling_cdfs",
    "subsampling_once",
    "double_conformal",
    "repeated_subsampling",
    "METHODS",
]


@dataclass(frozen=True)
class CalibrationResult:
    """Ambang kalibrasi beserta konteks yang diperlukan untuk menafsirkannya."""

    threshold: float
    method: str
    alpha: float
    n_points: int
    n_blocks: int
    alpha_min: float
    """Batas bawah alpha agar jaminan non-trivial mungkin: 1/(n_blocks+1)."""

    extra: dict = field(default_factory=dict)

    @property
    def is_trivial(self) -> bool:
        """True bila ambangnya +inf -- himpunan prediksi memuat seluruh label."""
        return not np.isfinite(self.threshold)

    @property
    def is_feasible(self) -> bool:
        """True bila alpha melampaui batas kelayakan blok."""
        return self.alpha > self.alpha_min

    def __str__(self) -> str:
        t = "inf" if self.is_trivial else f"{self.threshold:.4f}"
        return (
            f"{self.method:<20} alpha={self.alpha:<6.3f} T={t:<10} "
            f"K={self.n_blocks:<6} n={self.n_points:<6} "
            f"{'TRIVIAL' if self.is_trivial else 'ok'}"
        )


def _prepare(scores: np.ndarray, blocks: np.ndarray | None) -> tuple[np.ndarray, np.ndarray | None]:
    scores = np.asarray(scores, dtype=float).ravel()
    if scores.size == 0:
        raise ValueError("scores kosong")
    if not np.all(np.isfinite(scores)):
        raise ValueError("scores memuat NaN atau inf")
    if blocks is None:
        return scores, None
    blocks = np.asarray(blocks).ravel()
    if blocks.shape != scores.shape:
        raise ValueError(f"blocks {blocks.shape} dan scores {scores.shape} tidak sepadan")
    return scores, blocks


def _block_index(blocks: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Kembalikan (kode blok 0..K-1, ukuran tiap blok)."""
    _, inverse, counts = np.unique(blocks, return_inverse=True, return_counts=True)
    return inverse, counts


def split_conformal(scores: np.ndarray, alpha: float) -> CalibrationResult:
    """B1 -- split conformal naif, memperlakukan setiap skor sebagai independen.

    Setiap titik berbobot 1/(n+1), dengan satu atom 1/(n+1) di +inf.
    Inilah metode yang diklaim gagal pada data berblok (hipotesis H0).
    """
    scores, _ = _prepare(scores, None)
    n = scores.size
    w = np.full(n, 1.0 / (n + 1))
    threshold = quantile_with_infinity(scores, w, 1.0 / (n + 1), 1.0 - alpha)
    return CalibrationResult(
        threshold=threshold,
        method="B1 split",
        alpha=alpha,
        n_points=n,
        n_blocks=n,  # naif menganggap tiap titik adalah blok tersendiri
        alpha_min=1.0 / (n + 1),
    )


def hcp(scores: np.ndarray, blocks: np.ndarray, alpha: float) -> CalibrationResult:
    """B12 -- Hierarchical Conformal Prediction (Lee, Barber & Willett 2026, rumus 6).

    Setiap BLOK menyumbang massa yang sama, 1/(K+1), yang dibagi rata di antara
    N_k anggotanya. Satu atom 1/(K+1) diletakkan di +inf.

    Bila setiap blok berisi tepat satu titik, metode ini identik dengan
    :func:`split_conformal` -- sesuai pernyataan di makalah aslinya.
    """
    scores, blocks = _prepare(scores, blocks)
    codes, sizes = _block_index(blocks)
    k = sizes.size

    w = 1.0 / ((k + 1) * sizes[codes])
    threshold = quantile_with_infinity(scores, w, 1.0 / (k + 1), 1.0 - alpha)
    return CalibrationResult(
        threshold=threshold,
        method="B12 HCP",
        alpha=alpha,
        n_points=scores.size,
        n_blocks=int(k),
        alpha_min=1.0 / (k + 1),
        extra={"mean_block_size": float(sizes.mean()), "max_block_size": int(sizes.max())},
    )


def pooling_cdfs(scores: np.ndarray, blocks: np.ndarray, alpha: float) -> CalibrationResult:
    """B13 -- Pooling CDFs (Dunn dkk. 2022).

    Rata-ratakan CDF empiris tiap blok, lalu ambil kuantil (1-alpha).
    Tidak ada atom di +inf, sehingga sedikit kurang konservatif daripada HCP.

    Lee dkk. (Proposisi 1) menunjukkan metode ini setara HCP dengan
    ``alpha' = alpha + (1-alpha)/(K+1)``, sehingga jaminannya
    ``>= 1 - alpha - (1-alpha)/(K+1)``.
    """
    scores, blocks = _prepare(scores, blocks)
    codes, sizes = _block_index(blocks)
    k = sizes.size

    w = 1.0 / (k * sizes[codes])
    threshold = weighted_quantile(scores, w, 1.0 - alpha)
    return CalibrationResult(
        threshold=threshold,
        method="B13 pooling",
        alpha=alpha,
        n_points=scores.size,
        n_blocks=int(k),
        alpha_min=1.0 / (k + 1),
        extra={"alpha_efektif": alpha + (1 - alpha) / (k + 1)},
    )


def subsampling_once(
    scores: np.ndarray,
    blocks: np.ndarray,
    alpha: float,
    rng: np.random.Generator | None = None,
) -> CalibrationResult:
    """B14 -- Subsampling Once (Dunn dkk. 2022).

    Ambil satu titik acak per blok sehingga exchangeability biasa pulih, lalu
    jalankan split conformal. Valid, tetapi membuang sebagian besar data
    kalibrasi sehingga hasilnya sangat bervariasi antar-pengulangan.
    """
    scores, blocks = _prepare(scores, blocks)
    rng = np.random.default_rng() if rng is None else rng
    codes, sizes = _block_index(blocks)
    k = sizes.size

    order = np.argsort(codes, kind="stable")
    starts = np.concatenate([[0], np.cumsum(sizes)[:-1]])
    picked = order[starts + rng.integers(0, sizes)]
    chosen = scores[picked]

    w = np.full(k, 1.0 / (k + 1))
    threshold = quantile_with_infinity(chosen, w, 1.0 / (k + 1), 1.0 - alpha)
    return CalibrationResult(
        threshold=threshold,
        method="B14 subsample",
        alpha=alpha,
        n_points=scores.size,
        n_blocks=int(k),
        alpha_min=1.0 / (k + 1),
        extra={"n_terpakai": int(k), "n_dibuang": int(scores.size - k)},
    )


def double_conformal(scores: np.ndarray, blocks: np.ndarray, alpha: float) -> CalibrationResult:
    """B15 -- Double Conformal (Dunn dkk. 2022).

    Kuantil (1-alpha/2) di dalam tiap blok, lalu kuantil (1-alpha/2) lintas
    blok. Valid finite-sample lewat union bound, tetapi **secara praktik
    terlalu konservatif** karena membayar alpha/2 dua kali.

    Dirancang untuk ukuran blok seragam; di sini digeneralkan dengan memakai
    N_k masing-masing blok.

    Perhatian: metode ini menuntut DUA syarat kelayakan sekaligus,
    ``K + 1 >= 2/alpha`` DAN ``min_k N_k + 1 >= 2/alpha``. Syarat kedua tidak
    punya padanan di HCP, sehingga B15 dapat trivial total walau blok berlimpah
    -- selama tiap blok terlalu dangkal. Lihat ``extra["blok_trivial"]``.
    """
    scores, blocks = _prepare(scores, blocks)
    codes, sizes = _block_index(blocks)
    k = sizes.size
    half = 1.0 - alpha / 2.0

    per_block = np.empty(k)
    for b in range(k):
        s = scores[codes == b]
        m = s.size
        per_block[b] = quantile_with_infinity(
            s, np.full(m, 1.0 / (m + 1)), 1.0 / (m + 1), half
        )

    w = np.full(k, 1.0 / (k + 1))
    threshold = quantile_with_infinity(per_block, w, 1.0 / (k + 1), half)
    return CalibrationResult(
        threshold=threshold,
        method="B15 double",
        alpha=alpha,
        n_points=scores.size,
        n_blocks=int(k),
        alpha_min=1.0 / (k + 1),
        extra={"blok_trivial": int(np.sum(~np.isfinite(per_block)))},
    )


def repeated_subsampling(
    scores: np.ndarray,
    blocks: np.ndarray,
    alpha: float,
    n_repeats: int = 200,
    rng: np.random.Generator | None = None,
) -> CalibrationResult:
    """Repeated Subsampling (Dunn dkk. 2022), diformulasikan ulang sebagai HCP.

    Lee dkk. (Proposisi 2) membuktikan metode ini setara menjalankan HCP pada
    set kalibrasi hasil bootstrap dalam-blok, sehingga jaminannya menguat dari
    ``1-2*alpha`` menjadi ``1-alpha``. Untuk ``n_repeats`` besar hasilnya
    mendekati HCP biasa.
    """
    scores, blocks = _prepare(scores, blocks)
    rng = np.random.default_rng() if rng is None else rng
    codes, sizes = _block_index(blocks)
    k = sizes.size

    order = np.argsort(codes, kind="stable")
    starts = np.concatenate([[0], np.cumsum(sizes)[:-1]])

    boot_scores = np.empty(k * n_repeats)
    for b in range(k):
        idx = order[starts[b] + rng.integers(0, sizes[b], size=n_repeats)]
        boot_scores[b * n_repeats : (b + 1) * n_repeats] = scores[idx]

    w = np.full(k * n_repeats, 1.0 / ((k + 1) * n_repeats))
    threshold = quantile_with_infinity(boot_scores, w, 1.0 / (k + 1), 1.0 - alpha)
    return CalibrationResult(
        threshold=threshold,
        method="repeated subsample",
        alpha=alpha,
        n_points=scores.size,
        n_blocks=int(k),
        alpha_min=1.0 / (k + 1),
        extra={"n_repeats": n_repeats},
    )


METHODS = {
    "B12_hcp": hcp,
    "B13_pooling": pooling_cdfs,
    "B14_subsampling": subsampling_once,
    "B15_double": double_conformal,
}
