"""Periksa relasi persarangan antar granularitas blok PTB-XL.

Aturan keputusan C7 ("pilih granularitas terkasar yang masih layak") hanya sah
bila granularitas benar-benar bersarang. Kalau tidak bersarang, memblok pada
level yang lebih kasar TIDAK otomatis melindungi dependensi level yang lebih
halus, dan aturannya harus ditulis ulang.

B bersarang di atas A  <=>  setiap blok A termuat seluruhnya dalam satu blok B.
"""

from __future__ import annotations

import json
import pathlib
import sys

import pandas as pd

for _aliran in (sys.stdout, sys.stderr):
    if hasattr(_aliran, "reconfigure"):
        _aliran.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "ptbxl" / "ptbxl_database.csv"
KOLOM = ["patient_id", "site", "nurse", "device", "strat_fold"]
CALIB_FOLD = 9


def bersarang(df: pd.DataFrame, halus: str, kasar: str) -> tuple[bool, int, int]:
    """Apakah `halus` bersarang di dalam `kasar`? Kembalikan juga jumlah pelanggaran.

    Baris disaring per PASANGAN kolom. Memakai dropna lintas seluruh kolom akan
    menghapus 47 dari 51 site, karena site-site kecil justru yang `nurse`-nya
    kosong -- dan itu menghasilkan jawaban yang salah.
    """
    sub = df[[halus, kasar]].dropna()
    n_nilai_kasar = sub.groupby(halus, observed=True)[kasar].nunique()
    melanggar = int((n_nilai_kasar > 1).sum())
    return melanggar == 0, melanggar, int(len(n_nilai_kasar))


def komponen_terhubung(df: pd.DataFrame, kolom: list[str]) -> pd.Series:
    """Partisi terhalus yang memuat SELURUH sumber dependensi di `kolom`.

    Dua rekaman berada di blok sama bila berbagi nilai pada salah satu kolom,
    secara transitif. Inilah blok yang wajib dipakai bila ingin mengendalikan
    beberapa sumber dependensi sekaligus pada desain yang bersilang.
    """
    induk = list(range(len(df)))

    def cari(x: int) -> int:
        while induk[x] != x:
            induk[x] = induk[induk[x]]
            x = induk[x]
        return x

    def satukan(a: int, b: int) -> None:
        ra, rb = cari(a), cari(b)
        if ra != rb:
            induk[rb] = ra

    posisi = {c: df.columns.get_loc(c) for c in kolom}
    for c in kolom:
        kol = df.iloc[:, posisi[c]]
        wakil: dict = {}
        for i, nilai in enumerate(kol.to_numpy()):
            if pd.isna(nilai):
                continue
            if nilai in wakil:
                satukan(wakil[nilai], i)
            else:
                wakil[nilai] = i

    return pd.Series([cari(i) for i in range(len(df))])


def analisis_gabungan(df: pd.DataFrame) -> dict:
    """Berapa blok tersisa bila beberapa sumber dependensi dikendalikan sekaligus?

    Dihitung pada data penuh DAN pada fold 9 saja. Yang menentukan kelayakan
    adalah K1 pada set KALIBRASI (fold 9), bukan pada data penuh.
    """
    kombinasi = [
        ["patient_id"],
        ["patient_id", "device"],
        ["patient_id", "nurse"],
        ["patient_id", "site"],
        ["patient_id", "site", "device", "nurse"],
    ]
    kalib = df[df["strat_fold"] == CALIB_FOLD].reset_index(drop=True)

    print("\nBlok gabungan \u2014 mengendalikan beberapa sumber dependensi sekaligus")
    print(f"{'':<40}{'--- data penuh ---':>26}{'--- fold 9 (kalibrasi) ---':>32}")
    print(
        f"{'sumber':<40}{'K':>9}{'terbesar':>10}"
        f"{'K1':>9}{'terbesar':>10}{'alpha_min':>11}{'0,05?':>7}"
    )
    print("-" * 98)

    hasil = {}
    for kombi in kombinasi:
        komp_penuh = komponen_terhubung(df, kombi)
        komp_kal = komponen_terhubung(kalib, kombi)

        k_penuh = int(komp_penuh.nunique())
        k1 = int(komp_kal.nunique())
        alpha_min = 1.0 / (k1 + 1)
        layak = "YA" if 0.05 >= alpha_min else "TIDAK"
        nama = " + ".join(kombi)

        print(
            f"{nama:<40}{k_penuh:>9,}{int(komp_penuh.value_counts().iloc[0]):>10,}"
            f"{k1:>9,}{int(komp_kal.value_counts().iloc[0]):>10,}"
            f"{alpha_min:>11.5f}{layak:>7}"
        )
        hasil[nama] = {
            "blok_data_penuh": k_penuh,
            "blok_kalibrasi": k1,
            "blok_terbesar_kalibrasi": int(komp_kal.value_counts().iloc[0]),
            "alpha_min": round(alpha_min, 6),
            "layak_005": bool(0.05 >= alpha_min),
        }
    return hasil


def main() -> int:
    df = pd.read_csv(CSV)[KOLOM]
    print(f"Total rekaman: {len(df):,}")
    print("Nilai kosong per kolom: " + ", ".join(f"{c}={int(df[c].isna().sum())}" for c in KOLOM))
    print()

    print("Jumlah blok per granularitas (data penuh):")
    ukuran = {c: int(df[c].nunique()) for c in KOLOM}
    for c, k in sorted(ukuran.items(), key=lambda x: -x[1]):
        print(f"  {c:<12} K = {k:>6,}")

    print("\nMatriks persarangan  (baris HALUS bersarang di dalam kolom KASAR?)")
    header = "".join(f"{c[:9]:>11}" for c in KOLOM)
    print(f"{'':<13}{header}")

    hasil = {}
    for halus in KOLOM:
        baris = f"{halus:<13}"
        for kasar in KOLOM:
            if halus == kasar:
                baris += f"{'--':>11}"
                continue
            ok, melanggar, total = bersarang(df, halus, kasar)
            hasil[f"{halus}|{kasar}"] = {
                "bersarang": ok,
                "blok_melanggar": melanggar,
                "blok_total": total,
            }
            baris += f"{('YA' if ok else f'x{melanggar}'):>11}"
        print(baris)

    print("\nRantai persarangan yang terkonfirmasi (halus -> kasar):")
    rantai = [k for k, v in hasil.items() if v["bersarang"]]
    if rantai:
        for r in sorted(rantai):
            h, k = r.split("|")
            print(f"  {h} bersarang di dalam {k}   (K: {ukuran[h]:,} -> {ukuran[k]:,})")
    else:
        print("  (tidak ada)")

    gabungan = analisis_gabungan(df)

    keluaran = ROOT / "results" / "raw" / "block_nesting.json"
    keluaran.parent.mkdir(parents=True, exist_ok=True)
    keluaran.write_text(
        json.dumps(
            {"blok": ukuran, "persarangan": hasil, "gabungan": gabungan},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
