"""Verifikasi konstruktif Korolari 3.2 pada kekisi partisi PTB-XL yang sebenarnya.

Kor. 3.2 adalah KLAIM EKSISTENSI: terdapat desain bersilang yang tidak memiliki
granularitas mana pun yang memenuhi S1 (kelayakan) dan S2 (kecukupan) sekaligus.
Klaim eksistensi dibuktikan dengan satu contoh terverifikasi, bukan dengan
argumen umum -- sehingga tidak memerlukan pelonggaran ruang lingkup.

    S1  kelayakan : K1(g) >= ceil(1/alpha) - 1
    S2  kecukupan : setiap sumber dependensi BERSARANG di dalam g

Arah persarangan penting dan mudah terbalik. Sumber p bersarang di dalam g bila
setiap blok p termuat seluruhnya dalam satu blok g -- yaitu g LEBIH KASAR
daripada p. Karena itu S2 menuntut g lebih kasar daripada SELURUH sumber
sekaligus, dan granularitas TERHALUS yang memenuhi S2 adalah tepat join dari
seluruh sumber.

Konsekuensinya: bila join seluruh sumber pun gagal S1, maka tidak ada g mana pun
yang lolos keduanya, sebab setiap g pemenuh S2 lebih kasar lagi sehingga K1-nya
lebih kecil lagi.

Skrip ini tidak bersandar pada argumen itu. Ia MENGENUMERASI seluruh 2^m join
dari himpunan bagian sumber dan memeriksa S1 dan S2 satu per satu, agar
kesalahan penalaran di atas akan tertangkap oleh tabelnya sendiri.
"""

from __future__ import annotations

import itertools
import json
import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.ptbxl import load_metadata  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

SUMBER = ["patient_id", "site", "nurse", "device"]
ALPHAS = [0.01, 0.05, 0.10, 0.20]
FOLD_KALIBRASI = 9


def join_partisi(df: pd.DataFrame, kolom: list[str]) -> np.ndarray:
    """Partisi JOIN pada kekisi: partisi TERHALUS yang lebih kasar daripada tiap sumber.

    Menggabungkan label (`"a|b"`) menghasilkan IRISAN -- itu meet, bukan join, dan
    arahnya terbalik. Join sejati adalah komponen terhubung: dua rekaman sekelas bila
    berbagi nilai pada SALAH SATU sumber, secara transitif.
    """
    n = len(df)
    induk = np.arange(n)

    def cari(a: int) -> int:
        while induk[a] != a:
            induk[a] = induk[induk[a]]
            a = induk[a]
        return a

    def satukan(a: int, b: int) -> None:
        ra, rb = cari(a), cari(b)
        if ra != rb:
            induk[rb] = ra

    posisi = np.arange(n)
    for k in kolom:
        for _, idx in df.groupby(k, observed=True).indices.items():
            anggota = posisi[idx]
            for j in anggota[1:]:
                satukan(int(anggota[0]), int(j))

    return pd.factorize(np.array([cari(i) for i in range(n)]))[0]


def bersarang(halus: np.ndarray, kasar: np.ndarray) -> tuple[bool, int]:
    """Apakah `halus` bersarang di dalam `kasar`? Kembalikan (ya, jumlah pelanggar).

    Bersarang berarti setiap blok `halus` termuat dalam TEPAT SATU blok `kasar`.
    """
    d = pd.DataFrame({"h": halus, "k": kasar})
    cacah = d.groupby("h")["k"].nunique()
    pelanggar = int((cacah > 1).sum())
    return pelanggar == 0, pelanggar


def main() -> int:
    df = load_metadata()
    kal = df[df["strat_fold"] == FOLD_KALIBRASI].copy()

    # Baris dengan metadata sumber kosong dibuang SEKALI di awal, bukan per pasangan --
    # penyaringan per pasangan pernah menghasilkan K situs yang bertentangan dengan
    # nilai terdokumentasi.
    sebelum = len(kal)
    kal = kal.dropna(subset=SUMBER)
    print(f"Fold kalibrasi {FOLD_KALIBRASI}: {sebelum:,} rekaman, "
          f"{len(kal):,} sesudah membuang metadata sumber kosong "
          f"({sebelum - len(kal)} dibuang)\n")

    part = {s: join_partisi(kal, [s]) for s in SUMBER}
    print("Jumlah blok tiap sumber pada fold kalibrasi:")
    for s in SUMBER:
        print(f"  {s:<12} K = {len(np.unique(part[s])):>6,}")

    print("\n== Enumerasi seluruh join himpunan bagian sumber ==")
    print(f"{'granularitas':<44}{'K1':>8}{'S2?':>6}{'alpha_min':>12}  " +
          "  ".join(f"a={a:g}" for a in ALPHAS))
    print("-" * 104)

    baris = []
    for r in range(1, len(SUMBER) + 1):
        for kombinasi in itertools.combinations(SUMBER, r):
            g = join_partisi(kal, list(kombinasi))
            k1 = len(np.unique(g))
            amin = 1.0 / (k1 + 1)

            # S2: setiap sumber harus bersarang di dalam g.
            pelanggar = {s: bersarang(part[s], g)[1] for s in SUMBER}
            s2 = all(v == 0 for v in pelanggar.values())

            s1 = {a: (a >= amin) for a in ALPHAS}
            nama = " v ".join(kombinasi)
            tanda = "  ".join(("OK " if s1[a] else "-- ").rjust(5) for a in ALPHAS)
            print(f"{nama:<44}{k1:>8,}{'YA' if s2 else 'tidak':>6}{amin:>12.5f}  {tanda}")
            baris.append({"granularitas": list(kombinasi), "K1": k1, "alpha_min": amin,
                          "S2": bool(s2), "pelanggar_persarangan": pelanggar,
                          "S1": {f"{a:g}": bool(s1[a]) for a in ALPHAS}})

    print("\n== Putusan Korolari 3.2 ==")
    hasil = {}
    for a in ALPHAS:
        lolos = [b for b in baris if b["S2"] and b["S1"][f"{a:g}"]]
        hanya_s2 = [b for b in baris if b["S2"]]
        print(f"  alpha={a:g}: granularitas pemenuh S2 = {len(hanya_s2)}, "
              f"pemenuh S1 DAN S2 = {len(lolos)}"
              + ("   <- KETIDAKMUNGKINAN TERVERIFIKASI" if not lolos else
                 f"   -> {[' v '.join(b['granularitas']) for b in lolos]}"))
        hasil[f"{a:g}"] = {"n_S2": len(hanya_s2), "n_S1_dan_S2": len(lolos),
                           "ketidakmungkinan": len(lolos) == 0}

    s2_set = [b for b in baris if b["S2"]]
    if s2_set:
        terhalus = max(s2_set, key=lambda b: b["K1"])
        print(f"\n  Granularitas TERHALUS yang memenuhi S2: "
              f"{' v '.join(terhalus['granularitas'])}  ->  K1 = {terhalus['K1']}, "
              f"alpha_min = {terhalus['alpha_min']:.5f}")
        print("  Setiap granularitas pemenuh S2 lainnya lebih kasar, sehingga K1-nya "
              "lebih kecil dan alpha_min-nya lebih besar.")

    keluaran = ROOT / "results" / "raw" / "corollary32_lattice.json"
    keluaran.write_text(json.dumps(
        {"fold": FOLD_KALIBRASI, "n_rekaman": int(len(kal)), "sumber": SUMBER,
         "kekisi": baris, "putusan": hasil}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
