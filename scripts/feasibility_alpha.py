"""Hitung batas alpha yang layak per tingkat granularitas blok.

Teorema 1 (Lee, Barber & Willett 2026) untuk HCP memberi ambang

    T = Q_{1-alpha}( sum_k sum_i 1/((K1+1) N_k) delta_{s(Z_ki)} + 1/(K1+1) delta_{+inf} )

Massa 1/(K1+1) pada +inf berarti: bila alpha < 1/(K1+1), kuantilnya jatuh di
+inf dan himpunan prediksi menjadi tak hingga (trivial). Jadi syarat kelayakan
adalah alpha >= 1/(K1+1), dengan K1 = JUMLAH BLOK kalibrasi -- bukan jumlah
sampel, dan bukan n_eff Kish.

Ketaksamaan ini TIDAK ketat. Pada alpha = 1/(K1+1) tepat, massa berhingga
K1/(K1+1) sudah menyamai level 1-alpha, sehingga ambangnya jatuh di skor
maksimum -- berhingga, dan cakupannya tetap >= 1-alpha. Bentuk ini sejajar
dengan syarat baku split conformal, n >= 1/alpha - 1.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd

GROUPINGS = ["patient_id", "site", "nurse", "device", "strat_fold"]
ALPHAS = [0.01, 0.05, 0.10, 0.20]
CALIB_FOLD = 9
TEST_FOLD = 10


def kish_neff(sizes: pd.Series) -> float:
    total = float(sizes.sum())
    return total * total / float((sizes.astype(float) ** 2).sum())


def min_feasible_alpha(n_blocks: int) -> float:
    return 1.0 / (n_blocks + 1)


def analyse(df: pd.DataFrame, column: str) -> dict:
    calib = df[df["strat_fold"] == CALIB_FOLD]

    if column == "strat_fold":
        # Kalibrasi berisi satu fold saja, jadi fold tidak bisa menjadi unit blok.
        train_blocks = int(df[df["strat_fold"] <= 8]["strat_fold"].nunique())
        k1 = train_blocks
        note = "fold dipakai sebagai blok hanya bila kalibrasi memakai fold 1-8"
    else:
        k1 = int(calib[column].nunique())
        note = ""

    sizes_all = df.groupby(column).size()
    sizes_calib = calib.groupby(column).size() if column != "strat_fold" else sizes_all

    alpha_min = min_feasible_alpha(k1)
    return {
        "grouping": column,
        "blocks_total": int(df[column].nunique()),
        "blocks_calibration": k1,
        "records_calibration": int(len(calib)),
        "mean_block_size_calib": round(float(sizes_calib.mean()), 3),
        "alpha_min_feasible": round(alpha_min, 5),
        "feasible": {f"{a:.2f}": bool(a >= alpha_min) for a in ALPHAS},
        "kish_neff_full": round(kish_neff(sizes_all), 1),
        "design_effect_full": round(float(sizes_all.sum()) / kish_neff(sizes_all), 2),
        "note": note,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="data/raw/ptbxl/ptbxl_database.csv")
    parser.add_argument("--json", default="results/raw/feasibility_alpha.json")
    args = parser.parse_args()

    path = Path(args.csv)
    if not path.exists():
        print(f"TIDAK DITEMUKAN: {path}")
        return 1

    df = pd.read_csv(path)
    rows = [analyse(df, c) for c in GROUPINGS if c in df.columns]

    header = f"{'Blok':<12} {'Total':>7} {'K1 kal':>7} {'alpha min':>10} {'0.01':>6} {'0.05':>6} {'0.10':>6} {'DEff':>8}"
    print(header)
    print("-" * len(header))
    for r in rows:
        f = r["feasible"]
        print(
            f"{r['grouping']:<12} {r['blocks_total']:>7} {r['blocks_calibration']:>7} "
            f"{r['alpha_min_feasible']:>10.5f} "
            f"{'OK' if f['0.01'] else 'GAGAL':>6} "
            f"{'OK' if f['0.05'] else 'GAGAL':>6} "
            f"{'OK' if f['0.10'] else 'GAGAL':>6} "
            f"{r['design_effect_full']:>8.2f}"
        )

    print("\nCatatan: alpha_min = 1/(K1+1). Bila alpha < alpha_min, himpunan prediksi")
    print("menjadi tak hingga -- tidak ada jaminan non-trivial yang mungkin diberikan.")
    print("Design effect Kish mengukur EFISIENSI, bukan VALIDITAS. Keduanya berbeda.")

    out = Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
