"""Ekspor rujukan yang dikutip naskah ke RIS (Mendeley/Zotero/EndNote), urut nomor sitasi.

    python scripts/export_ris.py   -> docs/paper/references.ris
"""

from __future__ import annotations

import json
import pathlib
import sys
from urllib.parse import quote

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_docx as b  # noqa: E402

KELUAR = b.PAPER / "references.ris"
# Mendeley drops RIS entries with TY=DATA; ELEC preserves the online dataset record.
JENIS = {"journal-article": "JOUR", "proceedings-article": "CONF", "dataset": "ELEC", "preprint": "JOUR"}


def urutan_sitasi() -> list[str]:
    bagian = [b.ambil_abstrak((b.PAPER / b.ABSTRAK).read_text(encoding="utf-8"))]
    bagian += [b.ambil_prosa((b.PAPER / f).read_text(encoding="utf-8")) for _, _, f in b.URUTAN]
    md = b.nomori_tabel(b.tag_persamaan(b.rapikan_baris("\n\n".join(bagian))))
    return b.ganti_sitasi(b.gambar(md))[1]


def entri(nomor: int, kode: str, r: dict) -> list[str]:
    jenis = r.get("jenis", "journal-article")
    if r.get("dataset"):
        jenis = "dataset"
    baris = [f"TY  - {JENIS.get(jenis, 'GEN')}"]
    baris += [f"AU  - {a['family']}, {a['given']}".rstrip(", ") for a in r["penulis"]]
    judul = b.bersih(r["judul"])
    if jenis == "dataset":
        judul += " [Dataset]"
    baris.append(f"TI  - {judul}")
    venue = b.bersih(r.get("venue", ""))
    if jenis == "proceedings-article":
        baris.append(f"T2  - {venue}")
    elif jenis == "dataset":
        baris.append(f"PB  - {'PhysioNet' if 'physionet' in venue.lower() else venue}")
    elif jenis == "preprint":
        baris.append("JO  - arXiv")
    else:
        baris.append(f"JO  - {venue}")
        if r.get("venue_singkat"):
            baris.append(f"J2  - {b.bersih(r['venue_singkat'])}")
    baris.append(f"PY  - {r['tahun']}")
    if r.get("bulan"):
        baris.append(f"DA  - {r['tahun']}/{int(r['bulan']):02d}")
    if r.get("volume"):
        baris.append(f"VL  - {r['volume']}")
    if r.get("nomor"):
        baris.append(f"IS  - {r['nomor']}")
    hal = (r.get("halaman") or "").strip()
    # sama dengan build_docx: nomor halaman yang hanya mengulang akhiran DOI tidak dicetak
    if hal and r.get("doi") and hal == r["doi"].split("/")[-1].split(".")[-1]:
        hal = ""
    if hal:
        awal, _, akhir = hal.partition("-")
        baris.append(f"SP  - {awal}")
        if akhir:
            baris.append(f"EP  - {akhir}")
    if r.get("versi"):
        baris.append(f"ET  - Version {r['versi']}")
    if r.get("penerbit") and jenis != "dataset":
        baris.append(f"PB  - {r['penerbit']}")
    if r.get("doi"):
        baris.append(f"DO  - {r['doi']}")
        baris.append(f"UR  - https://doi.org/{quote(r['doi'], safe='/:;()-._')}")
    elif r.get("arxiv"):
        baris.append(f"UR  - https://arxiv.org/abs/{r['arxiv']}")
        baris.append(f"M1  - arXiv:{r['arxiv']}")
    baris.append(f"N1  - Cited as [{nomor}] in the manuscript (source code {kode})")
    baris.append("ER  - ")
    return baris


def main() -> int:
    refs = json.loads(b.REFS.read_text(encoding="utf-8"))
    urut = urutan_sitasi()
    teks = []
    for i, k in enumerate(urut, 1):
        teks += entri(i, k, refs[k]) + [""]
    KELUAR.write_text("\n".join(teks), encoding="utf-8")
    print(f"Ditulis: {KELUAR} ({len(urut)} rujukan)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
