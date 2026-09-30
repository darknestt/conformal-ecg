"""Verifikasi keseragaman medan header Challenge 2021 lintas sumber.

Klaim "tidak ada pengenal pasien" semula bersandar pada DUA header. Itu tidak
memadai sebagai pernyataan tentang 66.416 rekaman: format WFDB mengizinkan
medan komentar sembarang, dan tidak ada jaminan a priori bahwa seluruh sumber
memakai himpunan medan yang sama.

Skrip ini mengambil sampel acak header dari SETIAP folder sumber dan melaporkan
himpunan medan yang ditemukan. Tujuannya menyempitkan klaim dari "diperiksa dua
berkas" menjadi "diperiksa sampel lintas seluruh sumber" -- yang tetap BUKAN
sensus, dan harus dinyatakan demikian.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://physionet.org/files/challenge-2021/1.0.3/"
UA = {"User-Agent": "riset/1.0 (mailto:bloodszidan@gmail.com)"}
FOLDER = ["cpsc_2018", "cpsc_2018_extra", "st_petersburg_incart", "ptb",
          "georgia", "chapman_shaoxing", "ningbo"]

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")


def ambil(path: str, coba: int = 4) -> str | None:
    for i in range(coba):
        try:
            with urllib.request.urlopen(
                urllib.request.Request(BASE + path, headers=UA), timeout=45
            ) as r:
                isi = r.read().decode(errors="replace")
            time.sleep(0.12)
            return isi
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(1.5 * (i + 1))
        except Exception:  # noqa: BLE001
            time.sleep(1.5 * (i + 1))
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-folder", type=int, default=6)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    import random
    rng = random.Random(args.seed)

    akar = ambil("RECORDS")
    if not akar:
        print("GALAT: RECORDS akar tidak terbaca", file=sys.stderr)
        return 1
    per_folder: dict[str, list[str]] = {}
    for b in akar.splitlines():
        b = b.strip()
        if not b:
            continue
        bagian = b.replace("training/", "", 1).split("/")
        if len(bagian) >= 2:
            per_folder.setdefault(bagian[0], []).append("/".join(bagian[1:]))

    print(f"Sampel {args.per_folder} header per sumber, {len(FOLDER)} sumber\n")
    semua_medan: dict[str, set[str]] = {}
    diperiksa = 0
    contoh_medan = None

    for f in FOLDER:
        subs = per_folder.get(f, [])
        if not subs:
            print(f"  {f}: RECORDS tidak terbaca")
            continue
        # Turun ke subfolder lalu ambil nama rekaman.
        sub = rng.choice(subs)
        isi = ambil(f"training/{f}/{sub}RECORDS")
        if not isi:
            print(f"  {f}: subfolder {sub} tidak terbaca")
            continue
        rec = [b.strip() for b in isi.splitlines() if b.strip()]
        pilih = rng.sample(rec, min(args.per_folder, len(rec)))
        medan_f: set[str] = set()
        for nama in pilih:
            teks = ambil(f"training/{f}/{sub}{nama}.hea")
            if teks is None:
                continue
            m = {x.group(1).lower() for x in
                 re.finditer(r"^#\s*([A-Za-z]+)\s*:", teks, re.M)}
            medan_f |= m
            diperiksa += 1
            if contoh_medan is None:
                contoh_medan = sorted(m)
        semua_medan[f] = medan_f
        print(f"  {f:<22} medan: {sorted(medan_f)}")

    print(f"\nTotal header diperiksa: {diperiksa}")
    gabung = set().union(*semua_medan.values()) if semua_medan else set()
    irisan = set.intersection(*semua_medan.values()) if semua_medan else set()
    print(f"Gabungan medan lintas sumber : {sorted(gabung)}")
    print(f"Irisan medan lintas sumber   : {sorted(irisan)}")
    seragam = gabung == irisan
    print(f"Seragam lintas sumber        : {'YA' if seragam else 'TIDAK'}")

    kandidat_id = gabung & {"patient", "patientid", "subject", "subjectid", "id", "pid"}
    print(f"\nMedan yang dapat berfungsi sebagai pengenal pasien: "
          f"{sorted(kandidat_id) if kandidat_id else 'TIDAK ADA'}")
    print("\nBATAS KLAIM: ini SAMPEL, bukan sensus. Yang dapat dinyatakan adalah")
    print("bahwa pada sampel lintas seluruh sumber tidak ditemukan medan yang")
    print("terdokumentasi sebagai pengenal pasien -- bukan bahwa tidak ada satu")
    print("pun di antara 66.416 rekaman.")

    keluaran = ROOT / "results" / "raw" / "challenge2021_header_fields.json"
    keluaran.write_text(json.dumps({
        "per_folder": args.per_folder, "seed": args.seed,
        "header_diperiksa": diperiksa,
        "medan_per_sumber": {k: sorted(v) for k, v in semua_medan.items()},
        "gabungan": sorted(gabung), "irisan": sorted(irisan),
        "seragam": seragam,
        "kandidat_pengenal": sorted(kandidat_id),
        "sensus": False,
    }, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
