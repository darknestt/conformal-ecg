"""Design effect yang BENAR untuk HCP pada blok tak seragam (Prop. 2').

HCP memakai estimator terboboti-BLOK:
    G(t) = (1/K) sum_k Fbar_k(t)
sedangkan design effect Kish diturunkan untuk estimator terboboti-OBSERVASI:
    Xbar(t) = (1/n) sum_k sum_i X_ki(t)

Keduanya berbeda begitu ukuran blok tidak seragam. Skrip ini menghitung
keduanya agar selisihnya terlihat -- dan agar ukuran efisiensi yang dipakai
di dokumen dapat diperiksa, bukan diasumsikan.

Turunan (Asumsi A, korelasi intra-blok rho):
    Var(G)    = sigma^2 [1 + (H-1) rho] / (K H),      H = rata-rata harmonik N_k
    Var(Xbar) = sigma^2 [(1-rho) + rho * sum N_k^2 / n] / n

Relatif terhadap n titik independen (sigma^2 / n):
    DEff_blok(rho)   = n [1 + (H-1) rho] / (K H)   -> n/K = rata-rata aritmetik, saat rho=1
    DEff_pooled(rho) = (1-rho) + rho sum N_k^2 / n -> Kish,                      saat rho=1
"""

from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pandas as pd

for _aliran in (sys.stdout, sys.stderr):
    if hasattr(_aliran, "reconfigure"):
        _aliran.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "ptbxl" / "ptbxl_database.csv"
GROUPINGS = ["patient_id", "site", "nurse", "device", "strat_fold"]
RHOS = [0.1, 0.5, 1.0]


def ukuran(df: pd.DataFrame, kolom: str) -> np.ndarray:
    return df.groupby(kolom).size().to_numpy(dtype=float)


def deff_blok(sizes: np.ndarray, rho: float) -> float:
    k = sizes.size
    n = sizes.sum()
    h = k / np.sum(1.0 / sizes)  # rata-rata harmonik
    return float(n * (1 + (h - 1) * rho) / (k * h))


def deff_pooled(sizes: np.ndarray, rho: float) -> float:
    n = sizes.sum()
    return float((1 - rho) + rho * np.sum(sizes**2) / n)


def main() -> int:
    df = pd.read_csv(CSV)
    print(f"Rekaman: {len(df):,}\n")

    print(
        f"{'granularitas':<14}{'K':>8}{'n':>8}{'arith':>10}{'harm':>9}"
        f"{'Kish':>11}{'blok r=1':>11}{'rasio':>8}"
    )
    print("-" * 79)

    hasil = {}
    for kol in GROUPINGS:
        sizes = ukuran(df.dropna(subset=[kol]), kol)
        k, n = sizes.size, sizes.sum()
        arith = n / k
        harm = k / np.sum(1.0 / sizes)
        kish = deff_pooled(sizes, 1.0)
        blok1 = deff_blok(sizes, 1.0)

        print(
            f"{kol:<14}{k:>8,}{int(n):>8,}{arith:>10.2f}{harm:>9.2f}"
            f"{kish:>11.1f}{blok1:>11.1f}{kish / blok1:>8.1f}x"
        )
        hasil[kol] = {
            "K": int(k),
            "n": int(n),
            "rata_aritmetik": round(arith, 3),
            "rata_harmonik": round(harm, 3),
            "deff_kish_rho1": round(kish, 2),
            "deff_blok": {f"{r}": round(deff_blok(sizes, r), 3) for r in RHOS},
            "deff_pooled": {f"{r}": round(deff_pooled(sizes, r), 3) for r in RHOS},
        }

    print("\n  arith = n/K  = DEff_blok saat rho=1 (ukuran yang BENAR untuk HCP)")
    print("  Kish             = DEff_pooled saat rho=1 (estimator yang BUKAN dipakai HCP)")

    print("\n\nPeringkat efisiensi \u2014 apakah kedua ukuran sepakat?")
    print(f"{'granularitas':<14}{'Kish':>11}{'blok r=1':>11}{'layak 0,05':>13}")
    print("-" * 49)
    kalib = df[df["strat_fold"] == 9]
    baris = []
    for kol in GROUPINGS:
        sizes = ukuran(df.dropna(subset=[kol]), kol)
        k1 = (
            int(df[df["strat_fold"] <= 8]["strat_fold"].nunique())
            if kol == "strat_fold"
            else int(kalib[kol].nunique())
        )
        baris.append((kol, deff_pooled(sizes, 1.0), deff_blok(sizes, 1.0), 0.05 >= 1 / (k1 + 1)))
    for kol, kish, blok1, layak in sorted(baris, key=lambda x: x[2]):
        print(f"{kol:<14}{kish:>11.1f}{blok1:>11.1f}{('LAYAK' if layak else 'TIDAK'):>13}")

    urut_kish = [b[0] for b in sorted(baris, key=lambda x: x[1])]
    urut_blok = [b[0] for b in sorted(baris, key=lambda x: x[2])]
    print(f"\n  urutan menurut Kish     : {' < '.join(urut_kish)}")
    print(f"  urutan menurut blok r=1 : {' < '.join(urut_blok)}")
    print(f"  SAMA? {urut_kish == urut_blok}")
    hasil["peringkat"] = {"kish": urut_kish, "blok": urut_blok, "sama": urut_kish == urut_blok}

    keluaran = ROOT / "results" / "raw" / "design_effect_nonuniform.json"
    keluaran.parent.mkdir(parents=True, exist_ok=True)
    keluaran.write_text(json.dumps(hasil, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
