"""Geometri blok: ukuran setiap blok per sumber dependensi (bahan Fig. geometri di \u00a74.1).

Hanya metadata, tanpa model. PTB-XL: semua 21.799 rekaman, blok = patient_id, site,
nurse, device (rekaman tanpa nilai dikeluarkan dari sumber itu). MIT-BIH: 44 rekaman
non-pacu, blok = rekaman, ukuran = jumlah detak di cache yang sama dengan eksperimen.

    python experiments/block_geometry.py   -> results/raw/block_geometry.json
"""

from __future__ import annotations

import json
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
KELUAR = ROOT / "results" / "raw" / "block_geometry.json"


def ringkas(ukuran: np.ndarray) -> dict:
    ukuran = np.sort(ukuran)[::-1]
    return {"K": int(ukuran.size), "n": int(ukuran.sum()), "H": float(ukuran.size / np.sum(1.0 / ukuran)),
            "maks": int(ukuran[0]), "median": float(np.median(ukuran)), "ukuran": ukuran.tolist()}


def main() -> None:
    meta = pd.read_csv(ROOT / "data" / "raw" / "ptbxl" / "ptbxl_database.csv")
    hasil = {}
    for kolom in ("patient_id", "site", "nurse", "device"):
        hasil[f"ptbxl_{kolom}"] = ringkas(meta[kolom].dropna().value_counts().to_numpy())
    rec = np.load(ROOT / "data" / "interim" / "mitdb_beats_256.npz")["rec"]
    hasil["mitdb_record"] = ringkas(np.unique(rec, return_counts=True)[1])
    KELUAR.write_text(json.dumps(hasil, indent=1), encoding="utf-8")
    for k, v in hasil.items():
        print(f"{k:18s} K={v['K']:>6,} n={v['n']:>7,} H={v['H']:9.2f} maks={v['maks']:>5,} median={v['median']:.0f}")


if __name__ == "__main__":
    main()
