"""Verifikasi silang: setiap angka yang diklaim di dokumen harus cocok dengan data nyata.

Dijalankan sebelum membekukan protokol. Gagal = ada angka yang diasumsikan,
bukan diverifikasi.
"""

from __future__ import annotations

import pathlib
import sys

import pandas as pd

# Tanpa ini skrip mati oleh UnicodeEncodeError begitu outputnya di-pipe di Windows,
# karena Python beralih dari konsol ke cp1252.
for _aliran in (sys.stdout, sys.stderr):
    if hasattr(_aliran, "reconfigure"):
        _aliran.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "ptbxl" / "ptbxl_database.csv"
DOCS = {
    "README.md": ROOT / "README.md",
    "protocol.md": ROOT / "docs" / "protocol.md",
    "references.md": ROOT / "docs" / "references.md",
    "progress.md": ROOT / "docs" / "progress.md",
}

# Angka lama yang terbukti keliru. Boleh muncul HANYA di dalam narasi koreksi.
DILARANG = {
    "17.441": "jumlah fold 1-8 hasil pengurangan (benar: 17.418)",
    "2.160": "jumlah fold 10 keliru (benar: 2.198)",
    "13,4%": "estimasi dependensi pasien lama (benar: 23,1%)",
}

# Sebuah baris dianggap mendokumentasikan kesalahan, bukan mengulanginya.
PENANDA_KOREKSI = (
    "koreksi",
    "salah",
    "keliru",
    "digantikan",
    "sebelumnya",
    "awal (",
    "~~",
)


def fakta_dari_data(df: pd.DataFrame) -> dict[str, int]:
    return {
        "21.799": len(df),
        "18.869": df["patient_id"].nunique(),
        "17.418": len(df[df["strat_fold"] <= 8]),
        "2.183": len(df[df["strat_fold"] == 9]),
        "2.198": len(df[df["strat_fold"] == 10]),
        "1.942": df[df["strat_fold"] == 9]["patient_id"].nunique(),
    }


def main() -> int:
    if not CSV.exists():
        print(f"TIDAK DITEMUKAN: {CSV}")
        return 1

    df = pd.read_csv(CSV)
    teks = {nama: p.read_text(encoding="utf-8") if p.exists() else "" for nama, p in DOCS.items()}
    fakta = fakta_dari_data(df)

    print("=" * 66)
    print("  ANGKA YANG DIKLAIM vs DATA NYATA")
    print("=" * 66)
    header = f"  {'Klaim':<10} {'Nyata':>10} {'cocok':>7}   " + "  ".join(f"{n[:9]:>9}" for n in DOCS)
    print(header)
    print("  " + "-" * (len(header) - 2))

    gagal = 0
    for label, nyata in fakta.items():
        diklaim = int(label.replace(".", ""))
        cocok = diklaim == nyata
        if not cocok:
            gagal += 1
        hits = "  ".join(f"{teks[n].count(label):>9}" for n in DOCS)
        print(f"  {label:<10} {nyata:>10,} {'OK' if cocok else 'SALAH':>7}   {hits}")

    print()
    print("=" * 66)
    print("  ANGKA LAMA YANG SUDAH DICABUT")
    print("=" * 66)
    for label, alasan in DILARANG.items():
        telanjang = 0
        terdokumentasi = 0
        for nama, isi in teks.items():
            for baris in isi.splitlines():
                if label not in baris:
                    continue
                if any(k in baris.lower() for k in PENANDA_KOREKSI):
                    terdokumentasi += 1
                else:
                    telanjang += 1
                    print(f"     -> {nama}: {baris.strip()[:80]}")
        if telanjang:
            gagal += 1
            status = f"TELANJANG ({telanjang}x)"
        else:
            status = f"OK (hanya {terdokumentasi}x dlm narasi koreksi)"
        print(f"  {label:<10} {status:<38} {alasan}")

    print()
    if gagal:
        print(f"  ❌ {gagal} masalah ditemukan — perbaiki sebelum membekukan protokol.")
        return 1
    print("  ✅ Seluruh angka cocok dengan data. Protokol siap dibekukan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
