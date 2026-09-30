"""Sapuan kandidat rujukan baru: 2021+, terindeks Scopus, relevan dengan naskah.

Menyaring otomatis:
  - DOI yang SUDAH ada di docs/scopus-verification.json
  - venue yang tidak terindeks Scopus (dicek ke daftar sumber resmi Elsevier)
  - terbitan sebelum 2021

Frasa dicari lewat `title_and_abstract.search` DENGAN KUTIP -- tanpa kutip OpenAlex
meng-OR-kan katanya dan mengembalikan blockbuster tak relevan.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[1]
XLSX = ROOT / "data" / "external" / "scopus_source_list_Aug2026.xlsx"
SUDAH = ROOT / "docs" / "scopus-verification.json"
MAILTO = "bloodszidan@gmail.com"

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

# kelompok -> frasa eksak
TEMA = {
    "Dependensi / hierarki / blok": [
        "hierarchical conformal prediction",
        "conformal prediction clustered data",
        "conformal prediction repeated measurements",
        "group conformal prediction coverage",
        "conformal prediction exchangeability violation",
    ],
    "Multi-label & himpunan prediksi": [
        "multi-label conformal prediction",
        "conformal prediction label hierarchy",
        "conformal prediction set size efficiency",
    ],
    "EKG / aritmia + ketidakpastian": [
        "conformal prediction electrocardiogram",
        "uncertainty quantification electrocardiogram deep learning",
        "conformal prediction arrhythmia classification",
        "uncertainty estimation ECG classification",
    ],
    "Kebocoran data & evaluasi berkelompok": [
        "patient-level data leakage machine learning",
        "grouped cross-validation evaluation bias",
        "subject-wise cross-validation",
    ],
    "Kalibrasi & cakupan terkondisi": [
        "conditional coverage conformal prediction",
        "calibration conditional validity prediction sets",
        "conformal risk control",
    ],
}


def norm_issn(v) -> str:
    s = re.sub(r"[^0-9Xx]", "", str(v or "")).upper()
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
        rec = {"judul": r[ti], "aktif": r[ai], "cov": r[ci]}
        for kol in (ii, ei):
            k = norm_issn(r[kol])
            if k:
                idx.setdefault(k, rec)
    return idx


def cari(frasa: str, n: int = 50, coba: int = 5) -> list[dict]:
    url = ("https://api.openalex.org/works?"
           + urllib.parse.urlencode({
               "filter": (f'title_and_abstract.search:"{frasa}",'
                          "from_publication_date:2021-01-01,type:article,is_retracted:false"),
               "sort": "cited_by_count:desc",
               "per_page": n,
               "mailto": MAILTO,
           }))
    for a in range(coba):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode("utf-8")).get("results", [])
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503) or a == coba - 1:
                return []
            time.sleep(3 * (a + 1))
        except Exception:  # noqa: BLE001
            if a == coba - 1:
                return []
            time.sleep(3 * (a + 1))
    return []


def main() -> int:
    idx = muat_scopus()
    lama = {h["doi"].lower() for h in json.loads(SUDAH.read_text(encoding="utf-8"))}
    print(f"Sumber Scopus: {len(idx):,} ISSN | DOI sudah dipakai: {len(lama)}\n")

    semua: dict[str, dict] = {}
    for tema, frasa_list in TEMA.items():
        for f in frasa_list:
            for w in cari(f):
                doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
                if not doi or doi in lama:
                    continue
                sl = (w.get("primary_location") or {}).get("source") or {}
                iss = [norm_issn(x) for x in (sl.get("issn") or [])]
                if sl.get("issn_l"):
                    iss.append(norm_issn(sl["issn_l"]))
                cocok = next((idx[i] for i in iss if i in idx), None)
                if not cocok:
                    continue
                th = w.get("publication_year")
                if th is None or th < 2021 or th not in _tahun(cocok["cov"]):
                    continue
                r = semua.setdefault(doi, {
                    "doi": doi, "judul": w.get("title"), "tahun": th,
                    "venue": sl.get("display_name"), "cov": cocok["cov"],
                    "sitasi": w.get("cited_by_count"), "fwci": w.get("fwci"),
                    "tema": set(),
                })
                r["tema"].add(tema)
            time.sleep(1.2)

    urut = sorted(semua.values(),
                  key=lambda r: (len(r["tema"]), r["fwci"] or 0, r["sitasi"] or 0),
                  reverse=True)
    print(f"Kandidat lolos semua saringan: {len(urut)}\n")
    for i, r in enumerate(urut[:40], 1):
        print(f"{i:>3}. [{r['tahun']}] {(r['judul'] or '')[:96]}")
        print(f"     {r['venue']}  ({r['cov']})")
        print(f"     DOI {r['doi']} | sitasi {r['sitasi']} | FWCI {r['fwci']}"
              f" | tema: {', '.join(sorted(r['tema']))}")
    keluaran = ROOT / "results" / "raw" / "kandidat_rujukan.json"
    keluaran.parent.mkdir(parents=True, exist_ok=True)
    keluaran.write_text(json.dumps(
        [{**r, "tema": sorted(r["tema"])} for r in urut], indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


def _tahun(cov: str) -> set[int]:
    out: set[int] = set()
    for b in str(cov or "").split(";"):
        b = b.strip()
        m = re.match(r"^(\d{4})\s*-\s*(\d{4}|[Pp]resent)$", b)
        if m:
            out.update(range(int(m.group(1)),
                             (2027 if not m.group(2).isdigit() else int(m.group(2))) + 1))
        elif re.match(r"^\d{4}$", b):
            out.add(int(b))
    return out


if __name__ == "__main__":
    raise SystemExit(main())
