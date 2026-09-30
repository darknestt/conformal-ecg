"""Verifikasi struktural dataset setelah pengunduhan.

Mengecek bahwa angka yang tercatat di docs/dataset-verification.md benar-benar
cocok dengan berkas yang terunduh, lalu menghitung statistik yang menentukan
kelayakan premis penelitian.

Angka paling penting yang dihasilkan skrip ini adalah **distribusi rekaman per
pasien** pada PTB-XL dan **distribusi detak per rekaman** pada MIT-BIH. Kedua
angka itu menentukan seberapa kuat pelanggaran exchangeability yang sedang kita
teliti, dan karenanya menentukan apakah hipotesis H0 layak diuji.

Pemakaian:
    python scripts/verify_datasets.py
    python scripts/verify_datasets.py --data-dir D:/datasets
    python scripts/verify_datasets.py --json results/raw/dataset_verification.json
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    sys.exit("pandas belum terpasang. Jalankan: pip install pandas")


# Nilai rujukan dikutip dari halaman resmi PhysioNet per 2026-09-29.
EXPECTED_PTBXL = {
    "n_records": 21_799,
    "n_patients": 18_869,
    "n_metadata_columns": 28,
    "n_folds": 10,
    "superclass_counts": {
        "NORM": 9_514,
        "MI": 5_469,
        "STTC": 5_235,
        "CD": 4_898,
        "HYP": 2_649,
    },
}
EXPECTED_MITDB = {
    "n_records": 48,
    "n_subjects": 47,
    "n_annotations_approx": 110_000,
    "sampling_rate_hz": 360,
}
EXPECTED_NSTDB = {
    "n_ecg_records": 12,
    "n_noise_records": 3,
    "snr_levels_db": [24, 18, 12, 6, 0, -6],
}

PASS, FAIL, WARN, INFO = "PASS", "FAIL", "WARN", "INFO"

_SYMBOL = {PASS: "[PASS]", FAIL: "[FAIL]", WARN: "[WARN]", INFO: "[INFO]"}


class Report:
    """Kumpulan hasil pemeriksaan, dapat dicetak dan diserialisasi."""

    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []
        self.stats: dict[str, Any] = {}

    def add(self, status: str, name: str, detail: str = "") -> None:
        self.checks.append({"status": status, "name": name, "detail": detail})
        line = f"  {_SYMBOL[status]:<7} {name}"
        if detail:
            line += f"\n          {detail}"
        print(line)

    def section(self, title: str) -> None:
        print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")

    @property
    def failed(self) -> int:
        return sum(c["status"] == FAIL for c in self.checks)

    @property
    def warned(self) -> int:
        return sum(c["status"] == WARN for c in self.checks)


def find_file(root: Path, name: str) -> Path | None:
    """Cari berkas di mana pun di bawah root (struktur ZIP PhysioNet bervariasi)."""
    if not root.exists():
        return None
    direct = root / name
    if direct.is_file():
        return direct
    return next(iter(root.rglob(name)), None)


def describe_block_sizes(sizes: Counter[int], unit: str, block: str) -> dict[str, Any]:
    """Ringkas distribusi ukuran blok dan derajat konsentrasinya."""
    n_blocks = sum(sizes.values())
    n_units = sum(size * count for size, count in sizes.items())
    singletons = sizes.get(1, 0)
    max_size = max(sizes) if sizes else 0

    # Proporsi unit yang berada di blok berukuran > 1. Inilah bagian data yang
    # benar-benar melanggar exchangeability tingkat sampel.
    units_in_multi = sum(s * c for s, c in sizes.items() if s > 1)

    print(f"\n  Distribusi {unit} per {block}:")
    for size in sorted(sizes):
        count = sizes[size]
        pct = 100 * count / n_blocks
        bar = "#" * min(40, max(1, round(pct / 2)))
        label = f"{size:>6}" if size < 100 else f"{size:>6}"
        print(f"    {label} {unit:<8} : {count:>7} {block} ({pct:5.2f}%) {bar}")

    summary = {
        "n_blocks": n_blocks,
        "n_units": n_units,
        "mean_units_per_block": n_units / n_blocks if n_blocks else 0.0,
        "max_units_per_block": max_size,
        "singleton_blocks": singletons,
        "singleton_block_pct": 100 * singletons / n_blocks if n_blocks else 0.0,
        "units_in_multi_unit_blocks": units_in_multi,
        "units_in_multi_unit_blocks_pct": 100 * units_in_multi / n_units if n_units else 0.0,
    }

    print(f"\n    Rata-rata {unit}/{block}      : {summary['mean_units_per_block']:.3f}")
    print(f"    Maksimum {unit}/{block}       : {summary['max_units_per_block']}")
    print(f"    {block} dengan 1 {unit} saja  : {singletons} ({summary['singleton_block_pct']:.2f}%)")
    print(
        f"    {unit} di blok >1 {unit}      : {units_in_multi} "
        f"({summary['units_in_multi_unit_blocks_pct']:.2f}%)  <-- intensitas dependensi"
    )
    return summary


def verify_ptbxl(root: Path, rep: Report) -> None:
    rep.section("D1 - PTB-XL v1.0.3")

    db = find_file(root, "ptbxl_database.csv")
    if db is None:
        rep.add(FAIL, "ptbxl_database.csv ditemukan", f"tidak ada di {root}")
        return
    rep.add(PASS, "ptbxl_database.csv ditemukan", str(db))

    df = pd.read_csv(db, index_col="ecg_id")

    n_records = len(df)
    exp = EXPECTED_PTBXL["n_records"]
    rep.add(
        PASS if n_records == exp else FAIL,
        f"Jumlah rekaman = {exp}",
        f"ditemukan {n_records}",
    )

    n_cols = len(df.columns) + 1  # +1 untuk ecg_id yang dijadikan index
    exp_cols = EXPECTED_PTBXL["n_metadata_columns"]
    rep.add(
        PASS if n_cols == exp_cols else WARN,
        f"Jumlah kolom metadata = {exp_cols}",
        f"ditemukan {n_cols}",
    )

    if "patient_id" not in df.columns:
        rep.add(FAIL, "Kolom patient_id tersedia", "tidak ditemukan - K1 tidak dapat diuji")
        return
    rep.add(PASS, "Kolom patient_id tersedia")

    n_patients = df["patient_id"].nunique()
    exp_pat = EXPECTED_PTBXL["n_patients"]
    rep.add(
        PASS if n_patients == exp_pat else FAIL,
        f"Jumlah pasien unik = {exp_pat}",
        f"ditemukan {n_patients}",
    )

    # ---- angka penentu premis penelitian -------------------------------
    per_patient = df.groupby("patient_id").size()
    sizes = Counter(per_patient.values.tolist())
    stats = describe_block_sizes(sizes, unit="rekaman", block="pasien")
    rep.stats["ptbxl_block_structure"] = stats

    pct_multi = stats["units_in_multi_unit_blocks_pct"]
    if pct_multi < 10:
        rep.add(
            WARN,
            "Intensitas dependensi pasien",
            f"hanya {pct_multi:.1f}% rekaman berada di blok multi-rekaman. "
            "Dependensi LEMAH -> efek pada cakupan conformal kemungkinan kecil. "
            "Jadikan PTB-XL kasus 'mild', gunakan MIT-BIH sebagai kasus 'severe'.",
        )
    elif pct_multi < 30:
        rep.add(
            WARN,
            "Intensitas dependensi pasien",
            f"{pct_multi:.1f}% rekaman di blok multi-rekaman. Dependensi SEDANG.",
        )
    else:
        rep.add(
            PASS,
            "Intensitas dependensi pasien",
            f"{pct_multi:.1f}% rekaman di blok multi-rekaman. Dependensi KUAT.",
        )

    # ---- integritas fold -----------------------------------------------
    if "strat_fold" in df.columns:
        folds = sorted(df["strat_fold"].unique().tolist())
        rep.add(
            PASS if len(folds) == EXPECTED_PTBXL["n_folds"] else FAIL,
            f"Jumlah fold = {EXPECTED_PTBXL['n_folds']}",
            f"ditemukan {folds}",
        )
        # Klaim penyedia dataset: semua rekaman satu pasien berada di fold yang sama.
        leaky = df.groupby("patient_id")["strat_fold"].nunique()
        n_leaky = int((leaky > 1).sum())
        rep.add(
            PASS if n_leaky == 0 else FAIL,
            "Tidak ada pasien yang menyeberang fold",
            f"{n_leaky} pasien muncul di >1 fold"
            if n_leaky
            else "terkonfirmasi - split resmi aman dipakai",
        )
    else:
        rep.add(FAIL, "Kolom strat_fold tersedia", "tidak ditemukan")

    # ---- hierarki label -------------------------------------------------
    scp = find_file(root, "scp_statements.csv")
    if scp is None:
        rep.add(FAIL, "scp_statements.csv ditemukan", f"tidak ada di {root}")
        return
    rep.add(PASS, "scp_statements.csv ditemukan", str(scp))

    agg = pd.read_csv(scp, index_col=0)
    for col in ("diagnostic", "diagnostic_class", "diagnostic_subclass"):
        rep.add(
            PASS if col in agg.columns else FAIL,
            f"Kolom '{col}' tersedia",
        )

    if {"diagnostic", "diagnostic_class"}.issubset(agg.columns):
        diag = agg[agg["diagnostic"] == 1]
        rep.add(INFO, "Pernyataan diagnostik", f"{len(diag)} dari {len(agg)} pernyataan SCP")

        mapping = diag["diagnostic_class"].to_dict()
        counts: Counter[str] = Counter()
        for codes in df["scp_codes"]:
            parsed = ast.literal_eval(codes)
            present = {mapping[k] for k in parsed if k in mapping}
            counts.update(present)

        print("\n  Distribusi superclass diagnostik:")
        all_match = True
        for cls, expected in EXPECTED_PTBXL["superclass_counts"].items():
            found = counts.get(cls, 0)
            ok = found == expected
            all_match &= ok
            mark = "ok " if ok else "BEDA"
            print(f"    {cls:<6} : {found:>6}  (rujukan {expected:>6})  {mark}")

        rep.stats["ptbxl_superclass_counts"] = dict(counts)
        rep.add(
            PASS if all_match else WARN,
            "Distribusi superclass cocok dengan rujukan",
            "" if all_match else "periksa versi dataset atau logika agregasi",
        )

        total = sum(counts.values())
        rep.add(
            PASS if total > n_records else FAIL,
            "Dataset benar-benar multi-label",
            f"total label {total} > {n_records} rekaman"
            if total > n_records
            else "total label <= jumlah rekaman - periksa parsing",
        )

    # ---- metadata untuk K3 ----------------------------------------------
    for col in ("age", "sex"):
        if col in df.columns:
            missing = int(df[col].isna().sum())
            rep.add(
                PASS if missing == 0 else WARN,
                f"Metadata '{col}' untuk analisis subgrup",
                f"{missing} nilai kosong" if missing else "lengkap",
            )

    quality_cols = [
        c
        for c in ("static_noise", "burst_noise", "baseline_drift", "electrodes_problems")
        if c in df.columns
    ]
    rep.add(
        PASS if len(quality_cols) == 4 else WARN,
        "Metadata kualitas sinyal tersedia",
        ", ".join(quality_cols) if quality_cols else "tidak ada",
    )

    for sr, folder in ((100, "records100"), (500, "records500")):
        found = (root / folder).exists() or any(root.rglob(folder))
        rep.add(
            PASS if found else WARN,
            f"Sinyal {sr} Hz ({folder}/)",
            "tersedia" if found else "tidak ada - ekstraksi mungkin belum lengkap",
        )

    rep.stats["ptbxl"] = {
        "n_records": n_records,
        "n_patients": n_patients,
        "n_columns": n_cols,
    }


def verify_mitdb(root: Path, rep: Report) -> None:
    rep.section("D2 - MIT-BIH Arrhythmia v1.0.0")

    records_file = find_file(root, "RECORDS")
    if records_file is None:
        rep.add(FAIL, "Berkas RECORDS ditemukan", f"tidak ada di {root}")
        return
    rep.add(PASS, "Berkas RECORDS ditemukan", str(records_file))

    records = [ln.strip() for ln in records_file.read_text().splitlines() if ln.strip()]
    exp = EXPECTED_MITDB["n_records"]
    rep.add(
        PASS if len(records) == exp else FAIL,
        f"Jumlah rekaman = {exp}",
        f"ditemukan {len(records)}",
    )

    base = records_file.parent
    missing = [r for r in records if not (base / f"{r}.dat").exists()]
    rep.add(
        PASS if not missing else FAIL,
        "Semua berkas sinyal (.dat) tersedia",
        f"hilang: {missing[:10]}" if missing else "lengkap",
    )

    try:
        import wfdb  # noqa: PLC0415
    except ImportError:
        rep.add(
            WARN,
            "Penghitungan anotasi detak",
            "wfdb belum terpasang - jalankan: pip install wfdb",
        )
        return

    print("\n  Membaca anotasi (butuh beberapa detik)...")
    per_record: dict[str, int] = {}
    for rec in records:
        try:
            ann = wfdb.rdann(str(base / rec), "atr")
            per_record[rec] = len(ann.sample)
        except Exception as exc:  # noqa: BLE001
            rep.add(WARN, f"Gagal membaca anotasi {rec}", str(exc))

    if not per_record:
        return

    total = sum(per_record.values())
    exp_ann = EXPECTED_MITDB["n_annotations_approx"]
    within = abs(total - exp_ann) / exp_ann < 0.15
    rep.add(
        PASS if within else WARN,
        f"Total anotasi detak ~ {exp_ann:,}",
        f"ditemukan {total:,}",
    )

    values = sorted(per_record.values())
    mean = total / len(per_record)
    print("\n  Distribusi detak per rekaman:")
    print(f"    Minimum          : {values[0]:,}")
    print(f"    Median           : {values[len(values) // 2]:,}")
    print(f"    Maksimum         : {values[-1]:,}")
    print(f"    Rata-rata        : {mean:,.0f}   <-- intensitas dependensi blok")

    rep.stats["mitdb_block_structure"] = {
        "n_blocks": len(per_record),
        "n_units": total,
        "mean_units_per_block": mean,
        "min_units_per_block": values[0],
        "max_units_per_block": values[-1],
        "beats_per_record": per_record,
    }

    rep.add(
        PASS if mean > 100 else WARN,
        "Intensitas dependensi tingkat rekaman",
        f"rata-rata {mean:,.0f} detak/rekaman - dependensi SANGAT KUAT. "
        "Ini adalah kasus terbaik untuk menunjukkan kegagalan conformal naif."
        if mean > 100
        else f"rata-rata {mean:,.0f} detak/rekaman",
    )


def verify_nstdb(root: Path, rep: Report) -> None:
    rep.section("D3 - MIT-BIH Noise Stress Test v1.0.0")

    records_file = find_file(root, "RECORDS")
    if records_file is None:
        rep.add(WARN, "Berkas RECORDS ditemukan", f"tidak ada di {root} (dataset opsional)")
        return
    rep.add(PASS, "Berkas RECORDS ditemukan", str(records_file))

    records = [ln.strip() for ln in records_file.read_text().splitlines() if ln.strip()]
    ecg = [r for r in records if r.startswith(("118", "119"))]
    noise = [r for r in records if r in ("bw", "ma", "em")]

    rep.add(
        PASS if len(ecg) == EXPECTED_NSTDB["n_ecg_records"] else WARN,
        f"Rekaman EKG bernoise = {EXPECTED_NSTDB['n_ecg_records']}",
        f"ditemukan {len(ecg)}: {sorted(ecg)}",
    )
    rep.add(
        PASS if len(noise) == EXPECTED_NSTDB["n_noise_records"] else WARN,
        "Rekaman noise = 3 (bw, ma, em)",
        f"ditemukan {sorted(noise)}",
    )

    base = records_file.parent
    expected = [f"{b}e{s}" for b in ("118", "119") for s in ("24", "18", "12", "06", "00", "_6")]
    missing = [r for r in expected if not (base / f"{r}.dat").exists()]
    rep.add(
        PASS if not missing else WARN,
        "Semua 6 level SNR tersedia untuk 118 dan 119",
        f"hilang: {missing}" if missing else "24/18/12/6/0/-6 dB lengkap",
    )

    rep.stats["nstdb"] = {"ecg_records": sorted(ecg), "noise_records": sorted(noise)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "raw",
        help="Direktori berisi hasil unduhan (default: data/raw)",
    )
    parser.add_argument("--json", type=Path, help="Simpan hasil sebagai JSON")
    args = parser.parse_args()

    root: Path = args.data_dir
    print("\n  Verifikasi Dataset - Hierarchy-Aware Conformal Risk Control")
    print("  ----------------------------------------------------------")
    print(f"  Direktori: {root}")

    if not root.exists():
        print(f"\n  Direktori tidak ditemukan: {root}")
        print("  Jalankan dulu: .\\scripts\\download_data.ps1")
        return 1

    rep = Report()
    verify_ptbxl(root / "ptbxl", rep)
    verify_mitdb(root / "mitdb", rep)
    verify_nstdb(root / "nstdb", rep)

    rep.section("RINGKASAN")
    total = len(rep.checks)
    print(f"  Total pemeriksaan : {total}")
    print(f"  Gagal             : {rep.failed}")
    print(f"  Peringatan        : {rep.warned}")

    if rep.failed:
        print("\n  Ada pemeriksaan yang GAGAL. Periksa kembali unduhan sebelum melanjutkan.")
    elif rep.warned:
        print("\n  Tidak ada kegagalan, tetapi ada peringatan yang perlu dibaca.")
        print("  Perhatikan khususnya peringatan tentang intensitas dependensi blok:")
        print("  angka itu menentukan apakah hipotesis H0 layak diuji pada dataset ini.")
    else:
        print("\n  Semua pemeriksaan lolos.")

    print("\n  Langkah berikutnya:")
    print("    1. Salin angka distribusi blok ke docs/dataset-verification.md")
    print("    2. Perbarui Bagian 5 README.md dengan hasil verifikasi mandiri")
    print("    3. Lanjut ke studi kelayakan (Checklist Langkah 4)\n")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps({"checks": rep.checks, "stats": rep.stats}, indent=2),
            encoding="utf-8",
        )
        print(f"  Hasil disimpan: {args.json}\n")

    return 1 if rep.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
