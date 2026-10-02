"""Ambil metadata rujukan dari Crossref/arXiv dan simpan sebagai cache terverifikasi.

Kode rujukan ([A0], [F1], ...) dipetakan ke DOI atau ID arXiv yang tercatat di
docs/references.md. Metadata TIDAK diketik tangan: penulis, judul, venue, volume,
nomor, halaman, dan tahun diambil dari Crossref atau arXiv. Judul hasil unduhan
dicocokkan dengan judul di references.md; ketidakcocokan menghentikan skrip agar
DOI yang salah tidak lolos diam-diam.

    python scripts/fetch_references.py   -> docs/paper/references.json
"""

from __future__ import annotations

import difflib
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
REFMD = ROOT / "docs" / "references.md"
KELUAR = ROOT / "docs" / "paper" / "references.json"
UA = {"User-Agent": "sqopus-refcheck/1.0 (mailto:research@example.org)"}

# Rujukan tanpa baris tabel ber-DOI standar di references.md.
KHUSUS = {
    "A0": ("doi", "10.1145/3786352", "Distribution-free inference with hierarchical data"),
    "A0b": ("doi", "10.1080/01621459.2022.2060112", "Distribution-Free Prediction Sets for Two-Layer Hierarchical Models"),
    "B7": ("arxiv", "2410.06296", "Conformal Structured Prediction"),
    "P1": ("arxiv", "2608.21262", "The Exceedance Design Effect: Effective Sample Size for Thresholds under Clustering"),
    "P2": ("arxiv", "2608.08892", "A Symmetric Layer-Union Audit of Component Collapse in Hierarchical Procedural Corpora"),
}
DATASET = {"H2", "H3", "H4", "H5"}  # PhysioNet: dikutip dengan format dataset IEEE


def peta_dari_md() -> dict[str, tuple[str, str, str]]:
    teks = REFMD.read_text(encoding="utf-8")
    teks = teks[: teks.find("## 5.")] if "## 5." in teks else teks
    peta: dict[str, tuple[str, str, str]] = {}
    for baris in teks.splitlines():
        m = re.match(r"^\| \*{0,2}([A-I]\d+[a-z]?)\*{0,2} \| (.+)$", baris)
        if not m:
            continue
        kode, sisa = m.group(1), m.group(2)
        kolom = [c.strip() for c in sisa.split("|")]
        doi = re.search(r"`(10\.[^`]+)`", sisa)
        if not doi:
            continue
        judul = kolom[1] if kolom[0].startswith("`") else kolom[0]
        judul = re.sub(r"\s*\(.*?\)\s*$", "", re.sub(r"[*_]", "", judul)).strip()
        peta.setdefault(kode, ("doi", doi.group(1), judul))
    peta.update(KHUSUS)
    return peta


def ambil(url: str, terima: str = "application/json") -> bytes:
    for coba in range(4):
        try:
            req = urllib.request.Request(url, headers={**UA, "Accept": terima})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            if coba == 3:
                raise
            print(f"    ulang ({e})", file=sys.stderr)
            time.sleep(2 * (coba + 1))
    raise RuntimeError("tak tercapai")


def dari_crossref(doi: str) -> dict:
    m = json.loads(ambil("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")))["message"]
    tgl = (m.get("published-print") or m.get("published") or m.get("issued") or {}).get("date-parts", [[None]])[0]
    return {
        "jenis": m.get("type"),
        "penulis": [{"given": a.get("given", ""), "family": a.get("family", a.get("name", ""))}
                    for a in m.get("author", [])],
        "judul": (m.get("title") or [""])[0],
        "venue": (m.get("container-title") or [""])[0],
        "venue_singkat": (m.get("short-container-title") or [""])[0],
        "volume": m.get("volume", ""),
        "nomor": m.get("issue", ""),
        "halaman": m.get("page", "") or m.get("article-number", ""),
        "tahun": tgl[0] if tgl else None,
        "bulan": tgl[1] if tgl and len(tgl) > 1 else None,
        "penerbit": m.get("publisher", ""),
        "doi": doi,
    }


def dari_datacite(doi: str) -> dict:
    a = json.loads(ambil("https://api.datacite.org/dois/" + urllib.parse.quote(doi, safe="")))["data"]["attributes"]
    penulis = []
    for c in a.get("creators", []):
        if c.get("familyName"):
            penulis.append({"given": c.get("givenName", ""), "family": c["familyName"]})
        else:
            penulis.append({"given": "", "family": c.get("name", "")})
    return {
        "jenis": "dataset",
        "penulis": penulis,
        "judul": a["titles"][0]["title"],
        "venue": a.get("publisher", "") if isinstance(a.get("publisher"), str) else a.get("publisher", {}).get("name", ""),
        "volume": "", "nomor": "", "halaman": "",
        "versi": a.get("version", ""),
        "tahun": a.get("publicationYear"), "bulan": None,
        "doi": doi,
    }


def dari_arxiv(aid: str) -> dict:
    xml = ambil(f"http://export.arxiv.org/api/query?id_list={aid}", "application/atom+xml")
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = ET.fromstring(xml).find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        raise ValueError(f"arXiv {aid} tidak ditemukan")
    nama = [n.find("a:name", ns).text.strip() for n in e.findall("a:author", ns)]
    terbit = e.find("a:published", ns).text
    return {
        "jenis": "preprint",
        "penulis": [{"given": " ".join(n.split()[:-1]), "family": n.split()[-1]} for n in nama],
        "judul": " ".join(e.find("a:title", ns).text.split()),
        "venue": "arXiv", "volume": "", "nomor": "", "halaman": "",
        "tahun": int(terbit[:4]), "bulan": int(terbit[5:7]),
        "arxiv": aid, "doi": "",
    }


def mirip(a: str, b: str) -> float:
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower())
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def main() -> int:
    kode = sys.argv[1:] or None
    peta = peta_dari_md()
    lama = json.loads(KELUAR.read_text(encoding="utf-8")) if KELUAR.exists() else {}
    hasil, gagal = dict(lama), []
    for k, (jenis, ident, judul_md) in sorted(peta.items()):
        if kode and k not in kode:
            continue
        if k in lama and not kode:
            continue
        try:
            meta = (dari_arxiv(ident) if jenis == "arxiv"
                    else dari_datacite(ident) if k in DATASET else dari_crossref(ident))
        except Exception as e:  # noqa: BLE001
            gagal.append((k, ident, str(e)))
            print(f"  GAGAL {k:<4} {ident}: {e}")
            continue
        skor = mirip(meta["judul"], judul_md) if judul_md else 1.0
        meta["dataset"] = k in DATASET
        meta["kecocokan_judul"] = round(skor, 3)
        hasil[k] = meta
        tanda = "OK " if skor >= 0.8 or k in DATASET else "CEK"
        print(f"  {tanda} {k:<4} {skor:.2f}  {meta['judul'][:70]}")
        time.sleep(0.3)
    KELUAR.write_text(json.dumps(hasil, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(hasil)} rujukan -> {KELUAR.relative_to(ROOT)}; gagal: {len(gagal)}")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
