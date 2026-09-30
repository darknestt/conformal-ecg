"""Verifikasi asumsi MIT-BIH sebelum membangun apa pun.

Yang diperiksa:
- rekaman yang benar-benar ada di disk
- simbol anotasi dan pemetaannya ke 5 kelas AAMI
- nama kanal (klaim: kanal 0 = MLII kecuali pada rekaman berpacu)
- split inter-pasien de Chazal DS1/DS2
- JUMLAH BLOK yang tersedia -> menentukan alpha mana yang layak (Prop. 1)
"""

from __future__ import annotations

import pathlib
import sys
from collections import Counter

import numpy as np
import wfdb

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
MITDB = ROOT / "data" / "raw" / "mitdb"

# Rekaman berpacu -- dikecualikan menurut rekomendasi AAMI.
BERPACU = {"102", "104", "107", "217"}

# Split inter-pasien de Chazal dkk. (2004), standar 20+ tahun.
DS1 = ["101", "106", "108", "109", "112", "114", "115", "116", "118", "119", "122",
       "124", "201", "203", "205", "207", "208", "209", "215", "220", "223", "230"]
DS2 = ["100", "103", "105", "111", "113", "117", "121", "123", "200", "202", "210",
       "212", "213", "214", "219", "221", "222", "228", "231", "232", "233", "234"]

AAMI = {
    "N": set("NLRej"),
    "S": set("AaJS"),
    "V": {"V", "E"},
    "F": {"F"},
    "Q": {"/", "f", "Q"},
}
SIMBOL_DETAK = set().union(*AAMI.values())


def kelas_aami(sym: str) -> str | None:
    for k, s in AAMI.items():
        if sym in s:
            return k
    return None


def main() -> int:
    ada = sorted({p.stem for p in MITDB.glob("*.dat")})
    print(f"Rekaman .dat di disk: {len(ada)}")
    print(f"  {' '.join(ada)}")

    hilang = [r for r in DS1 + DS2 if r not in ada]
    print(f"\nRekaman DS1+DS2 yang HILANG: {hilang if hilang else 'tidak ada'}")
    print(f"Rekaman berpacu (dikecualikan): {sorted(BERPACU)}")
    print(f"  ada di disk? {[r in ada for r in sorted(BERPACU)]}")
    sisa = set(ada) - set(DS1) - set(DS2) - BERPACU
    print(f"Rekaman di disk tapi bukan DS1/DS2/berpacu: {sorted(sisa) if sisa else 'tidak ada'}")

    print("\n=== Nama kanal (klaim: kanal 0 = MLII) ===")
    kanal0 = Counter()
    anomali = []
    for r in DS1 + DS2:
        hdr = wfdb.rdheader(str(MITDB / r))
        kanal0[hdr.sig_name[0]] += 1
        if hdr.sig_name[0] != "MLII":
            anomali.append((r, hdr.sig_name))
        if hdr.fs != 360:
            anomali.append((r, f"fs={hdr.fs}"))
    print(f"  {dict(kanal0)}")
    print(f"  ANOMALI: {anomali if anomali else 'tidak ada'}")

    print("\n=== Simbol anotasi di DS1+DS2 ===")
    semua = Counter()
    per_kelas = Counter()
    bukan_detak = Counter()
    per_rekaman = {}
    for r in DS1 + DS2:
        ann = wfdb.rdann(str(MITDB / r), "atr")
        n_rec = 0
        for s in ann.symbol:
            semua[s] += 1
            k = kelas_aami(s)
            if k:
                per_kelas[k] += 1
                n_rec += 1
            else:
                bukan_detak[s] += 1
        per_rekaman[r] = n_rec

    print(f"  simbol unik: {len(semua)}")
    print(f"  {dict(sorted(semua.items(), key=lambda x: -x[1]))}")
    print(f"\n  Bukan-detak (dibuang): {dict(sorted(bukan_detak.items(), key=lambda x: -x[1]))}")

    total = sum(per_kelas.values())
    print(f"\n=== Kelas AAMI (total {total:,} detak) ===")
    for k in ("N", "S", "V", "F", "Q"):
        print(f"  {k}: {per_kelas[k]:>7,}  ({per_kelas[k] / total * 100:5.2f}%)")

    print("\n=== STRUKTUR BLOK -- ini yang menentukan kelayakan ===")
    uk1 = np.array([per_rekaman[r] for r in DS1])
    uk2 = np.array([per_rekaman[r] for r in DS2])
    for nama, uk, rec in (("DS1 (latih)", uk1, DS1), ("DS2 (kalibrasi/uji)", uk2, DS2)):
        print(
            f"\n  {nama}: K={len(rec)} rekaman, n={uk.sum():,} detak"
            f"\n    N_k: min={uk.min():,} median={int(np.median(uk)):,} maks={uk.max():,}"
            f" rata={uk.mean():,.0f}"
        )

    print("\n  Kelayakan bila DS2 dibagi dua (K1 = 11 blok kalibrasi):")
    k1 = len(DS2) // 2
    amin = 1 / (k1 + 1)
    print(f"    K1 = {k1}  ->  alpha_min = 1/{k1 + 1} = {amin:.4f}")
    for a in (0.01, 0.05, 0.10, 0.15, 0.20):
        print(f"      alpha={a:.2f}  {'LAYAK' if a >= amin else 'TIDAK -> ambang +inf (H1)'}")

    n_kal = int(uk2[:k1].sum())
    print(f"\n  Rasio bobot atom +inf (n+1)/(K1+1) ~ {(n_kal + 1) / (k1 + 1):,.0f}x")
    print("    Bandingkan PTB-XL: 1,12x. Di sinilah HCP harus berbeda dari B1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
