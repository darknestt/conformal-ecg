"""C7 -- uji diagnostik kecukupan blok.

Menjawab satu pertanyaan yang harus dijawab **sebelum** model apa pun dilatih:
pada tingkat granularitas blok mana jaminan cakupan non-trivial masih mungkin?

Dua batas yang terpisah dan tidak berkorelasi
---------------------------------------------
VALIDITAS  diatur jumlah blok K. Bila ``alpha < 1/(K+1)`` ambang kalibrasi
           jatuh di +inf dan himpunan prediksi memuat seluruh label. Tidak ada
           metode yang dapat memperbaikinya -- ini batas informasi.

EFISIENSI  diatur design effect Kish. Blok besar menaikkan varians estimasi
           kuantil, sehingga himpunan prediksi melebar. Tidak memengaruhi
           apakah jaminan *mungkin*, hanya seberapa *berguna*.

Pada PTB-XL kedua urutan itu berlawanan: `site` punya design effect terburuk
(6.687) namun alpha=0,05 tetap layak, sedangkan `device` design effect-nya
lebih baik (3.901) tetapi alpha=0,05 mustahil.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "BlockDiagnostic",
    "block_sufficiency",
    "compare_granularities",
    "label_sufficiency",
    "minimum_blocks",
]


def minimum_blocks(alpha: float) -> int:
    """Jumlah blok kalibrasi minimum agar ``alpha >= 1/(K+1)`` terpenuhi.

    ``K_min = ceil(1/alpha) - 1``. Ketaksamaannya tidak ketat, jadi alpha=0,05
    hanya menuntut 19 blok, bukan 20.
    """
    if not 0.0 < alpha < 1.0:
        raise ValueError(f"alpha harus di (0,1), diterima {alpha}")
    return int(np.ceil(1.0 / alpha)) - 1


def _kish_neff(sizes: np.ndarray) -> float:
    total = float(sizes.sum())
    return total * total / float((sizes.astype(float) ** 2).sum())


@dataclass(frozen=True)
class BlockDiagnostic:
    """Hasil uji kecukupan blok untuk satu granularitas pada satu level alpha."""

    grouping: str
    alpha: float
    n_points: int
    n_blocks: int
    alpha_min: float
    blocks_required: int
    feasible: bool
    mean_block_size: float
    max_block_size: int
    n_eff: float
    design_effect: float

    @property
    def verdict(self) -> str:
        if not self.feasible:
            kurang = self.blocks_required - self.n_blocks
            return f"MUSTAHIL — kurang {kurang} blok (butuh >= {self.blocks_required})"
        if self.design_effect > 100:
            return "LAYAK tetapi sangat tidak efisien"
        if self.design_effect > 2:
            return "LAYAK dengan biaya efisiensi sedang"
        return "LAYAK dan efisien"

    def __str__(self) -> str:
        mark = "OK" if self.feasible else "GAGAL"
        return (
            f"{self.grouping:<14} alpha={self.alpha:<6.3f} K={self.n_blocks:<6} "
            f"alpha_min={self.alpha_min:<8.5f} DEff={self.design_effect:<10.2f} "
            f"{mark:<6} {self.verdict}"
        )


def block_sufficiency(
    blocks: np.ndarray,
    alpha: float,
    grouping: str = "blocks",
) -> BlockDiagnostic:
    """Jalankan uji kecukupan blok pada satu pengelompokan.

    Tidak memerlukan skor maupun model — hanya label blok. Itulah gunanya:
    keputusan granularitas dapat diambil sebelum pelatihan dimulai.
    """
    blocks = np.asarray(blocks).ravel()
    if blocks.size == 0:
        raise ValueError("blocks kosong")

    _, counts = np.unique(blocks, return_counts=True)
    k = int(counts.size)
    alpha_min = 1.0 / (k + 1)
    n_eff = _kish_neff(counts)

    return BlockDiagnostic(
        grouping=grouping,
        alpha=alpha,
        n_points=int(blocks.size),
        n_blocks=k,
        alpha_min=alpha_min,
        blocks_required=minimum_blocks(alpha),
        feasible=alpha >= alpha_min,
        mean_block_size=float(counts.mean()),
        max_block_size=int(counts.max()),
        n_eff=n_eff,
        design_effect=float(blocks.size) / n_eff,
    )


def compare_granularities(
    groupings: dict[str, np.ndarray],
    alphas: list[float],
) -> list[BlockDiagnostic]:
    """Jalankan uji kecukupan blok pada banyak granularitas x banyak alpha."""
    return [
        block_sufficiency(labels, alpha, grouping=name)
        for name, labels in groupings.items()
        for alpha in alphas
    ]


def label_sufficiency(
    blocks: np.ndarray,
    labels: np.ndarray,
    alpha: float,
    label_names: list[str] | None = None,
    simultaneous: bool = False,
) -> list[BlockDiagnostic]:
    """C8 -- kelayakan kalibrasi per label (Prop. 4).

    Jaminan terkondisi-label untuk label ``l`` hanya boleh memakai titik
    kalibrasi yang memuat ``l``, sehingga blok yang tersedia menyusut menjadi
    blok yang MEMUAT ``l``. Batas kelayakannya karenanya per label:

        alpha >= 1 / (K1(l) + 1)

    Dengan ``simultaneous=True``, union bound menuntut alpha/m per label
    (m = jumlah label), yang menaikkan ambangnya secara linear terhadap m.

    Berjalan tanpa model: hanya butuh label blok dan matriks label biner.

    Parameters
    ----------
    blocks : (n,) label blok per pengamatan
    labels : (n, m) matriks biner; ``labels[i, j]`` benar bila pengamatan i
             memuat label j
    """
    blocks = np.asarray(blocks).ravel()
    labels = np.asarray(labels, dtype=bool)
    if labels.ndim != 2:
        raise ValueError(f"labels harus 2-D (n, m), diterima {labels.shape}")
    if labels.shape[0] != blocks.size:
        raise ValueError(f"labels {labels.shape} dan blocks {blocks.shape} tidak sepadan")

    m = labels.shape[1]
    if label_names is None:
        label_names = [f"label_{j}" for j in range(m)]
    elif len(label_names) != m:
        raise ValueError(f"label_names {len(label_names)} != jumlah label {m}")

    alpha_efektif = alpha / m if simultaneous else alpha

    hasil = []
    for j, nama in enumerate(label_names):
        ada = labels[:, j]
        if not ada.any():
            raise ValueError(f"label '{nama}' tidak muncul sama sekali")
        hasil.append(block_sufficiency(blocks[ada], alpha_efektif, grouping=nama))
    return hasil
