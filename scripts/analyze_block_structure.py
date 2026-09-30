"""Analisis struktur blok PTB-XL lintas beberapa tingkat granularitas.

Teori conformal dalam penelitian ini berlaku untuk struktur blok sembarang, bukan
khusus blok pasien. PTB-XL memuat beberapa pengelompokan alami sekaligus
(`patient_id`, `site`, `nurse`, `device`) sehingga satu dataset dapat memberi
beberapa titik pada sumbu intensitas dependensi.

Skrip juga menghitung dependensi sebagai fungsi interval antar-rekaman (E11).
Tanggal PTB-XL digeser acak per pasien, sehingga tanggal absolut tidak bermakna,
tetapi interval di dalam satu pasien tetap valid karena offsetnya konstan.

Keluaran skrip ini menjadi dasar kurva dosis-respons pada eksperimen E2 dan E11.

Pemakaian:
    python scripts/analyze_block_structure.py
    python scripts/analyze_block_structure.py --json results/raw/block_structure.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

# Kolom pengelompokan yang diperiksa, diurutkan dari blok terkecil ke terbesar.
BLOCK_COLUMNS = ["patient_id", "nurse", "site", "device", "strat_fold"]


def effective_sample_size(sizes: pd.Series) -> float:
    """n_eff = (sum m_i)^2 / sum m_i^2 (Kish). Sama dengan n bila semua blok tunggal."""
    total = sizes.sum()
    return float(total**2 / (sizes**2).sum())


def analyze(df: pd.DataFrame, column: str) -> dict[str, float | int] | None:
    if column not in df.columns:
        return None

    valid = df[df[column].notna()]
    if valid.empty:
        return None

    sizes = valid.groupby(column).size()
    n_units = int(sizes.sum())
    n_blocks = int(len(sizes))
    multi = sizes[sizes > 1]
    units_in_multi = int(multi.sum())
    n_eff = effective_sample_size(sizes)

    return {
        "n_blocks": n_blocks,
        "n_units": n_units,
        "n_missing": int(len(df) - len(valid)),
        "mean_block_size": n_units / n_blocks,
        "median_block_size": float(sizes.median()),
        "max_block_size": int(sizes.max()),
        "singleton_blocks": int((sizes == 1).sum()),
        "units_in_multi_blocks": units_in_multi,
        "pct_units_in_multi_blocks": 100 * units_in_multi / n_units,
        "n_eff": n_eff,
        "n_eff_ratio": n_eff / n_units,
        "design_effect": n_units / n_eff,
    }


def classify(pct_multi: float, design_effect: float) -> str:
    if design_effect >= 10:
        return "SANGAT KUAT"
    if design_effect >= 3:
        return "KUAT"
    if pct_multi >= 20:
        return "SEDANG"
    if pct_multi >= 5:
        return "LEMAH-SEDANG"
    return "LEMAH"


# Bin interval untuk E11. Batas dipilih dari distribusi nyata: median 23 hari,
# maksimum 1.707 hari, dengan kelompok "sesi sama" yang terpisah jelas.
INTERVAL_BINS = [
    ("sesi sama (0 hari)", 0, 0),
    ("1-30 hari", 1, 30),
    ("31-365 hari", 31, 365),
    (">365 hari", 366, 10**9),
]


def analyze_intervals(df: pd.DataFrame) -> dict[str, dict] | None:
    """Dependensi sebagai fungsi jarak waktu antar-rekaman dalam satu pasien (E11)."""
    if not {"patient_id", "recording_date"}.issubset(df.columns):
        return None

    work = df[["patient_id", "recording_date"]].copy()
    work["rd"] = pd.to_datetime(work["recording_date"], errors="coerce")
    work = work.dropna(subset=["rd"])

    sizes = work.groupby("patient_id").size()
    multi_ids = sizes[sizes > 1].index
    if len(multi_ids) == 0:
        return None

    multi = work[work["patient_id"].isin(multi_ids)]
    span = multi.groupby("patient_id")["rd"].agg(lambda s: (s.max() - s.min()).days)

    print(f"\n  Dependensi vs interval antar-rekaman (E11)  — {len(span):,} pasien multi-rekaman")
    print("  " + "=" * 88)
    print(
        f"  {'Bin interval':<22}{'Pasien':>9}{'Rekaman':>10}{'Rata2 blok':>13}"
        f"{'n_eff':>10}{'Design eff.':>13}  Intensitas"
    )
    print("  " + "-" * 88)

    results: dict[str, dict] = {}
    for label, low, high in INTERVAL_BINS:
        ids = span[(span >= low) & (span <= high)].index
        if len(ids) == 0:
            print(f"  {label:<22}{'0':>9}  (tidak ada pasien di bin ini)")
            continue
        bin_sizes = sizes.loc[ids]
        n_units = int(bin_sizes.sum())
        n_eff = effective_sample_size(bin_sizes)
        deff = n_units / n_eff
        intensity = classify(100.0, deff)
        results[label] = {
            "n_patients": int(len(ids)),
            "n_records": n_units,
            "mean_block_size": n_units / len(ids),
            "n_eff": n_eff,
            "design_effect": deff,
            "intensity": intensity,
        }
        print(
            f"  {label:<22}{len(ids):>9,}{n_units:>10,}{n_units / len(ids):>13.2f}"
            f"{n_eff:>10,.0f}{deff:>13.2f}  {intensity}"
        )

    print("  " + "-" * 88)
    print("\n  Catatan: tanggal PTB-XL digeser acak per pasien, sehingga tanggal absolut")
    print("  tidak bermakna. Interval di dalam satu pasien tetap valid karena offsetnya")
    print("  konstan. Bin ini adalah satu-satunya sumbu temporal yang sah pada dataset ini.")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "data"
        / "raw"
        / "ptbxl"
        / "ptbxl_database.csv",
    )
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"Tidak ditemukan: {args.csv}")
        print("Jalankan dulu: python scripts/download_physionet.py ptbxl")
        return 1

    df = pd.read_csv(args.csv, index_col="ecg_id")
    print(f"\n  Struktur Blok PTB-XL  ({len(df):,} rekaman)")
    print("  " + "=" * 88)

    header = (
        f"  {'Pengelompokan':<14}{'Blok':>8}{'Rata2':>9}{'Maks':>7}"
        f"{'% di blok>1':>13}{'n_eff':>10}{'Design eff.':>13}  Intensitas"
    )
    print(header)
    print("  " + "-" * 88)

    results: dict[str, dict] = {}
    for col in BLOCK_COLUMNS:
        stats = analyze(df, col)
        if stats is None:
            print(f"  {col:<14}  (kolom tidak tersedia)")
            continue
        label = classify(stats["pct_units_in_multi_blocks"], stats["design_effect"])
        stats["intensity"] = label
        results[col] = stats
        print(
            f"  {col:<14}{stats['n_blocks']:>8,}{stats['mean_block_size']:>9.2f}"
            f"{stats['max_block_size']:>7,}{stats['pct_units_in_multi_blocks']:>12.1f}%"
            f"{stats['n_eff']:>10,.0f}{stats['design_effect']:>13.2f}  {label}"
        )

    print("  " + "-" * 88)
    print("\n  Keterangan:")
    print("    n_eff        = ukuran sampel efektif Kish; jumlah sampel independen setara")
    print("    Design eff.  = n / n_eff; seberapa besar n dilebih-lebihkan oleh dependensi blok")
    print("    Design eff. mendekati 1 berarti koreksi blok nyaris tidak diperlukan")

    # Kombinasi pasien x situs memberi blok terbesar yang masih bermakna klinis.
    if {"patient_id", "site"}.issubset(df.columns):
        combo = df.dropna(subset=["site"]).groupby(["site", "patient_id"]).size()
        if not combo.empty:
            n_eff = effective_sample_size(combo)
            print(
                f"\n  Kombinasi site x patient_id: {len(combo):,} blok, "
                f"n_eff={n_eff:,.0f}, design effect={combo.sum() / n_eff:.2f}"
            )

    interval_results = analyze_intervals(df)
    if interval_results:
        results["_intervals"] = interval_results  # type: ignore[assignment]

    print("\n  Implikasi untuk desain eksperimen E2:")
    if results:
        ordered = sorted(
            ((k, v) for k, v in results.items() if k != "_intervals"),
            key=lambda kv: kv[1]["design_effect"],
        )
        span = [f"{k} ({v['design_effect']:.1f}x)" for k, v in ordered]
        print("    Sumbu intensitas dependensi dalam satu dataset: " + "  ->  ".join(span))
        print("    Gunakan urutan ini sebagai titik pengamatan kurva dosis-respons,")
        print("    dilengkapi MIT-BIH tingkat detak sebagai ujung ekstrem.")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\n  Hasil disimpan: {args.json}")

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
