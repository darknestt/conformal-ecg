"""Cari pengganti mutakhir (2021-2026) yang TERINDEKS SCOPUS untuk rujukan tua.

Tiap kandidat dicari lewat OpenAlex, lalu ISSN-nya dicocokkan ke daftar sumber
Scopus resmi. Hanya kandidat yang lolos KEDUA syarat yang ditampilkan.

Peringatan yang harus dibaca sebelum memakai hasilnya:

    Sitasi pencetus metode TIDAK dapat digantikan tanpa melanggar atribusi.
    Bila Anda memakai APS, Anda wajib menyitasi Romano dkk. Skrip ini mencari
    pendamping/alternatif, bukan pemutih sitasi.

Yang benar-benar bisa diganti hanyalah rujukan yang perannya "menunjukkan praktik
terkini" -- bukan yang perannya "inilah asal metodenya".
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[1]
XLSX = ROOT / "data" / "external" / "scopus_source_list_Aug2026.xlsx"
MAILTO = "bloodszidan@gmail.com"

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

# peran -> (daftar frasa untuk title_and_abstract.search, apakah pencetus metode)
CARI = {
    "APS / adaptive prediction sets (pengganti Romano 2020)": (
        ["adaptive prediction sets", "conformal classification adaptive coverage"], True),
    "Mondrian / class-conditional CP (pengganti Vovk 2012)": (
        ["Mondrian conformal prediction", "class-conditional conformal"], True),
    "Perbandingan statistik pengklasifikasi (pengganti Demsar 2006)": (
        ["statistical comparison of classifiers", "benchmarking machine learning statistical tests"],
        False),
    "Protokol inter-patient EKG (pengganti de Chazal 2004)": (
        ["inter-patient ECG arrhythmia", "inter-patient paradigm heartbeat classification"], False),
}


def norm_issn(v) -> str:
    if v is None:
        return ""
    s = re.sub(r"[^0-9Xx]", "", str(v)).upper()
    return s.zfill(8) if s else ""


def muat_scopus() -> dict[str, dict]:
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["Scopus Sources Aug. 2026"]
    it = ws.iter_rows(values_only=True)
    h = list(next(it))
    ti, ii, ei, ai, ci = (h.index(c) for c in
                          ("Source Title", "ISSN", "EISSN", "Active or Inactive", "Coverage"))
    idx: dict[str, dict] = {}
    for r in it:
        rec = {"judul": r[ti], "aktif": r[ai], "coverage": r[ci]}
        for kol in (ii, ei):
            k = norm_issn(r[kol])
            if k:
                idx.setdefault(k, rec)
    return idx


def cari_openalex(frasa: str, n: int = 40, coba: int = 4) -> list[dict]:
    """Frasa DIKUTIP agar dicocokkan eksak; tanpa kutip OpenAlex meng-OR-kan katanya."""
    url = ("https://api.openalex.org/works?"
           + urllib.parse.urlencode({
               "filter": (f'title_and_abstract.search:"{frasa}",'
                          "from_publication_date:2021-01-01,type:article,is_retracted:false"),
               "sort": "cited_by_count:desc",
               "per_page": n,
               "mailto": MAILTO,
           }))
    for percobaan in range(coba):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode("utf-8")).get("results", [])
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503) or percobaan == coba - 1:
                raise
            time.sleep(3 * (percobaan + 1))
        except (urllib.error.URLError, TimeoutError):
            if percobaan == coba - 1:
                raise
            time.sleep(3 * (percobaan + 1))
    return []


def main() -> int:
    idx = muat_scopus()
    print(f"Daftar sumber Scopus: {len(idx):,} ISSN\n")

    for peran, (frasa_list, pencetus) in CARI.items():
        print("=" * 78)
        print(peran)
        if pencetus:
            print("  !! PERAN INI ADALAH PENCETUS METODE -- atribusi tidak boleh dihapus.")
        print("=" * 78)

        hasil, lihat = [], set()
        for frasa in frasa_list:
            try:
                for w in cari_openalex(frasa):
                    if w["id"] not in lihat:
                        lihat.add(w["id"])
                        hasil.append(w)
            except Exception as e:  # noqa: BLE001
                print(f"  galat pencarian '{frasa}': {e}")
            time.sleep(1.0)
        hasil.sort(key=lambda w: w.get("cited_by_count") or 0, reverse=True)

        tampil = 0
        for w in hasil:
            sl = (w.get("primary_location") or {}).get("source") or {}
            issns = [norm_issn(x) for x in (sl.get("issn") or [])]
            if sl.get("issn_l"):
                issns.append(norm_issn(sl["issn_l"]))
            cocok = next((idx[i] for i in issns if i in idx), None)
            if not cocok:
                continue
            doi = (w.get("doi") or "").replace("https://doi.org/", "")
            print(f"\n  [{w.get('publication_year')}] {(w.get('title') or '')[:92]}")
            print(f"     {sl.get('display_name')}  |  Scopus OK ({cocok['coverage']})")
            print(f"     DOI {doi}  |  sitasi {w.get('cited_by_count')}"
                  f"  |  FWCI {w.get('fwci')}")
            tampil += 1
            if tampil >= 6:
                break
        if tampil == 0:
            print("  (tak ada kandidat terindeks Scopus pada 2021+)")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
