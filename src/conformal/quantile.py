"""Kuantil berbobot untuk distribusi diskret.

Seluruh metode conformal di paket ini bermuara pada satu operasi: mengambil
kuantil (1-alpha) dari distribusi diskret berbobot yang memuat satu atom di
+inf. Atom itulah yang menghasilkan koreksi finite-sample.
"""

from __future__ import annotations

import numpy as np

# Toleransi untuk perbandingan kumulatif; bobot pecahan menumpuk galat float.
_TOL = 1e-12


def weighted_quantile(values: np.ndarray, weights: np.ndarray, level: float) -> float:
    """Kuantil ke-`level` dari distribusi diskret berbobot.

    Mengembalikan nilai terkecil ``t`` sedemikian sehingga massa kumulatif pada
    ``values <= t`` mencapai ``level``. Bila massa kumulatif tidak pernah
    mencapai ``level``, hasilnya ``+inf`` -- inilah mekanisme yang membuat
    himpunan prediksi menjadi trivial saat blok kalibrasi terlalu sedikit.
    """
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)

    if values.shape != weights.shape:
        raise ValueError(f"values {values.shape} dan weights {weights.shape} tidak sepadan")
    if values.size == 0:
        return float("inf")
    if np.any(weights < 0):
        raise ValueError("bobot negatif tidak diperbolehkan")
    if not 0.0 < level < 1.0:
        raise ValueError(f"level harus di (0,1), diterima {level}")

    total = weights.sum()
    if total <= 0:
        return float("inf")

    order = np.argsort(values, kind="stable")
    v = values[order]
    cumulative = np.cumsum(weights[order]) / total

    reached = np.nonzero(cumulative >= level - _TOL)[0]
    if reached.size == 0:
        return float("inf")
    return float(v[reached[0]])


def quantile_with_infinity(
    values: np.ndarray,
    weights: np.ndarray,
    inf_weight: float,
    level: float,
) -> float:
    """Kuantil berbobot setelah menambahkan satu atom bermassa `inf_weight` di +inf."""
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    return weighted_quantile(
        np.concatenate([values, [np.inf]]),
        np.concatenate([weights, [inf_weight]]),
        level,
    )
