"""Verifikasi indeksasi Scopus untuk seluruh rujukan di docs/references.md.

Sumber kebenaran: daftar sumber RESMI Elsevier (ext_list_Aug_2026.xlsx), bukan proksi
seperti SCImago/JUFO. Berkas itu memuat 49.010 sumber lengkap dengan ISSN, EISSN,
status aktif/nonaktif, rentang tahun cakupan, dan lembar judul yang DIHENTIKAN.

Yang diperiksa per rujukan:

  1. DOI resolve di OpenAlex                       -> judul, tahun, venue, ISSN
  2. ISSN/EISSN cocok di daftar sumber Scopus      -> terindeks atau tidak
  3. Tahun terbit berada di dalam rentang cakupan  -> artikelnya sendiri terindeks
  4. Status aktif / dihentikan
  5. Tahun >= AMBANG_TAHUN kecuali rujukan dataset -> aturan "5 tahun terakhir"

Unduh daftar sumber bila belum ada:
  https://www.elsevier.com/products/scopus/content -> "Download the Source title list"
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
REFS = ROOT / "docs" / "references.md"
KELUARAN = ROOT / "docs" / "scopus-verification.json"

AMBANG_TAHUN = 2021  # "5 tahun terakhir" relatif 2026
MAILTO = "bloodszidan@gmail.com"  # polite pool OpenAlex

# DOI dataset/PhysioNet dikecualikan dari aturan 5 tahun (dan dari Scopus).
PREFIKS_DATASET = ("10.13026/",)
DOI_DATASET_LAIN = {"10.1038/s41597-020-0495-6"}  # paper dataset PTB-XL

# OpenAlex memakai tanggal online-first; Crossref 'published-print' yang dipakai menyitasi.
TAHUN_CETAK = {"10.1109/jbhi.2020.3022989": 2021}  # Crossref: 2021-05, JBHI 25(5):1519-1528

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")


def norm_issn(v) -> str:
    if v is None:
        return ""
    s = re.sub(r"[^0-9Xx]", "", str(v)).upper()
    return s.zfill(8) if s else ""


def parse_coverage(teks: str) -> set[int]:
    """'2026; 2023-2024' -> {2026, 2023, 2024}. 'to Present' diperlakukan sampai 2026."""
    tahun: set[int] = set()
    if not teks:
        return tahun
    for bagian in str(teks).split(";"):
        bagian = bagian.strip()
        m = re.match(r"^(\d{4})\s*-\s*(\d{4}|Present|present)$", bagian)
        if m:
            a = int(m.group(1))
            b = 2026 if not m.group(2).isdigit() else int(m.group(2))
            tahun.update(range(a, b + 1))
            continue
        m = re.match(r"^(\d{4})\s*-?\s*$", bagian)
        if m:
            tahun.add(int(m.group(1)))
    return tahun


def muat_scopus() -> tuple[dict, dict]:
    if not XLSX.exists():
        print(f"GALAT: {XLSX} tidak ada.", file=sys.stderr)
        sys.exit(1)
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)

    ws = wb["Scopus Sources Aug. 2026"]
    baris = ws.iter_rows(values_only=True)
    hdr = list(next(baris))
    i_t, i_i, i_e = hdr.index("Source Title"), hdr.index("ISSN"), hdr.index("EISSN")
    i_a = hdr.index("Active or Inactive")
    i_c = hdr.index("Coverage")
    i_d = hdr.index("Titles Discontinued by Scopus")
    i_ty = hdr.index("Source Type")

    indeks: dict[str, dict] = {}
    for r in baris:
        rec = {"judul": r[i_t], "aktif": r[i_a], "coverage": r[i_c],
               "dihentikan": r[i_d], "tipe": r[i_ty],
               "tahun": parse_coverage(r[i_c])}
        for kol in (i_i, i_e):
            k = norm_issn(r[kol])
            if k:
                indeks.setdefault(k, rec)

    ws2 = wb["Discontinued Titles Aug. 2026"]
    b2 = ws2.iter_rows(min_row=2, values_only=True)
    h2 = list(next(b2))
    try:
        j_i, j_e = h2.index("ISSN"), h2.index("EISSN")
        j_c = h2.index("Indexation Change")
    except ValueError:
        return indeks, {}
    henti: dict[str, str] = {}
    for r in b2:
        for kol in (j_i, j_e):
            k = norm_issn(r[kol])
            if k:
                henti[k] = str(r[j_c])
    return indeks, henti


def openalex(doi: str) -> dict | None:
    url = ("https://api.openalex.org/works/doi:"
           + urllib.parse.quote(doi, safe="") + f"?mailto={MAILTO}")
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"    ! OpenAlex gagal untuk {doi}: {e}", file=sys.stderr)
        return None


def buang_blok_dikeluarkan(teks: str) -> str:
    """Blok '### ❌ Dikeluarkan' memuat DOI yang sudah DIBUANG dari daftar.

    Tanpa ini, DOI mati ikut terhitung dan angka ringkasan menggelembung.
    """
    awal = teks.find("### ❌ Dikeluarkan")
    if awal == -1:
        return teks
    akhir = teks.find("\n### ", awal + 1)
    return teks[:awal] + (teks[akhir:] if akhir != -1 else "")


def main() -> int:
    teks = buang_blok_dikeluarkan(REFS.read_text(encoding="utf-8"))
    # Rujukan aktif hanya ada di tabel sebelum §4; sesudahnya log pemangkasan
    # dan penukaran yang memuat DOI yang SUDAH DIBUANG.
    batas = teks.find("## 4. Ringkasan Mutu Jurnal")
    if batas != -1:
        teks = teks[:batas]
    doi_list, lihat = [], set()
    # DOI dalam backtick diambil utuh: DOI SICI lama memuat <, >, ( dan ) yang
    # memotong regex umum dan diam-diam memverifikasi DOI yang salah.
    dalam_backtick = [m.group(1) for m in re.finditer(r"`(10\.\d{4,9}/[^`\s]+)`", teks)]
    umum = [m.group(0).rstrip(".,;`*") for m in re.finditer(r"\b10\.\d{4,9}/[^\s`|)>\]]+", teks)]
    for d in dalam_backtick + umum:
        if any(b.lower() != d.lower() and b.lower().startswith(d.lower()) for b in dalam_backtick):
            continue
        if d.lower() not in lihat:
            lihat.add(d.lower())
            doi_list.append(d)
    print(f"DOI unik ditemukan di references.md: {len(doi_list)}")

    indeks, henti = muat_scopus()
    print(f"Daftar sumber Scopus dimuat: {len(indeks):,} ISSN unik\n")

    hasil = []
    for n, doi in enumerate(doi_list, 1):
        w = openalex(doi)
        time.sleep(0.12)
        if w is None:
            hasil.append({"doi": doi, "status": "DOI_TIDAK_RESOLVE"})
            print(f"{n:>3}. {doi}\n     -> DOI TIDAK RESOLVE")
            continue

        tahun = w.get("publication_year")
        tahun_sitasi = TAHUN_CETAK.get(doi.lower(), tahun)
        sl = (w.get("primary_location") or {}).get("source") or {}
        venue = sl.get("display_name") or "(tanpa venue)"
        issns = [norm_issn(x) for x in (sl.get("issn") or [])]
        if sl.get("issn_l"):
            issns.append(norm_issn(sl["issn_l"]))
        judul = (w.get("title") or "")[:70]

        dataset = doi.startswith(PREFIKS_DATASET) or doi in DOI_DATASET_LAIN
        cocok = next((indeks[i] for i in issns if i in indeks), None)
        issn_cocok = next((i for i in issns if i in indeks), None)

        if cocok:
            in_cov = tahun in cocok["tahun"] if cocok["tahun"] else None
            scopus = "TERINDEKS" if in_cov is not False else "TERINDEKS_TAPI_TAHUN_DI_LUAR_CAKUPAN"
            aktif = str(cocok["aktif"] or "").strip()
            dihentikan = bool(cocok["dihentikan"]) or issn_cocok in henti
        else:
            scopus = "TIDAK_DITEMUKAN"
            aktif, dihentikan, in_cov = "", False, None

        lolos_tahun = dataset or (tahun_sitasi is not None and tahun_sitasi >= AMBANG_TAHUN)
        hasil.append({
            "doi": doi, "judul": w.get("title"), "tahun": tahun,
            "tahun_sitasi": tahun_sitasi, "venue": venue,
            "issn": issns, "issn_cocok": issn_cocok, "scopus": scopus,
            "aktif": aktif, "dihentikan": dihentikan,
            "coverage": cocok["coverage"] if cocok else None,
            "tahun_dalam_cakupan": in_cov,
            "dataset": dataset, "lolos_aturan_5_tahun": lolos_tahun,
        })

        tanda = {"TERINDEKS": "OK", "TIDAK_DITEMUKAN": "TIDAK ADA"}.get(scopus, "PERIKSA")
        th = f"{tahun_sitasi}" + (f" (OpenAlex: {tahun})" if tahun_sitasi != tahun else "") \
            + ("" if lolos_tahun else "  <<< PRA-2021")
        print(f"{n:>3}. {doi}\n     {judul}\n     {venue}  |  {th}\n"
              f"     Scopus: {tanda} ({scopus})"
              + (f" | {aktif}" if aktif else "")
              + (" | DIHENTIKAN" if dihentikan else "")
              + (f" | cakupan: {cocok['coverage']}" if cocok else ""))

    KELUARAN.write_text(json.dumps(hasil, indent=2, ensure_ascii=False), encoding="utf-8")

    ok = [h for h in hasil if h.get("scopus") == "TERINDEKS"]
    tidak = [h for h in hasil if h.get("scopus") == "TIDAK_DITEMUKAN"]
    periksa = [h for h in hasil if h.get("scopus") not in ("TERINDEKS", "TIDAK_DITEMUKAN")]
    tua = [h for h in hasil if h.get("lolos_aturan_5_tahun") is False]
    mati = [h for h in hasil if h.get("dihentikan")]

    print("\n" + "=" * 70)
    print(f"  Terindeks Scopus            : {len(ok)}/{len(hasil)}")
    print(f"  TIDAK ditemukan di Scopus   : {len(tidak)}")
    print(f"  Perlu diperiksa manual      : {len(periksa)}")
    print(f"  Dihentikan Scopus           : {len(mati)}")
    print(f"  Melanggar aturan 5 tahun    : {len(tua)}")
    for h in tidak:
        print(f"    TIDAK ADA  {h['doi']}  {h.get('venue')}")
    for h in periksa:
        print(f"    PERIKSA    {h['doi']}  {h.get('venue')}  ({h.get('scopus', 'DOI_TIDAK_RESOLVE')})")
    for h in mati:
        print(f"    DIHENTIKAN {h['doi']}  {h.get('venue')}")
    for h in tua:
        print(f"    PRA-2021   {h['doi']}  {h.get('tahun')}  {h.get('venue')}")
    print(f"\nTersimpan: {KELUARAN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
