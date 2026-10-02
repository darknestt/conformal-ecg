"""Susun draf bagian (docs/paper/sec*-draft.md) menjadi naskah Word bergaya IEEE.

Yang dikerjakan, berurutan:
  1. Ambil prosa naskah dari tiap draf (judul "## N." sampai catatan kerja).
  2. Sitasi kode ([A0], [I1, A13], [A0, Thm. 1]) -> nomor IEEE menurut urutan
     kemunculan pertama; daftar pustaka disusun dari docs/paper/references.json
     (metadata Crossref/arXiv/DataCite, bukan ketikan tangan).
  3. Tabel "**Table 8.1.** ..." -> "TABLE I" (Romawi, berurutan) dan rujukan di
     teks ikut diganti. Figure memakai keterangan "Fig. n." di bawah gambar.
  4. \\tag{n} -> nomor persamaan (n) di kanan.
  5. Blockquote jadi paragraf biasa; huruf tebal hanya untuk judul paragraf.
  6. Gaya dokumen: Times New Roman hitam, judul bernomor, teks rata kiri-kanan.

    python scripts/build_docx.py            -> docs/paper/manuscript-draft.docx
"""

from __future__ import annotations

import datetime
import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile

import pypandoc
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs" / "paper"
KELUAR = PAPER / "manuscript-draft.docx"
REFS = PAPER / "references.json"
JUDUL = "Block-Level Feasibility of Conformal Calibration on Clinical ECG Data: An Empirical Audit"

URUTAN = [
    ("1", "Introduction", None),
    ("2", "Related Work", "sec2-draft.md"),
    ("3–4", "Preliminaries and Problem Formulation", "sec3-4-draft.md"),
    ("5", "Methods", "sec5-draft.md"),
    ("6–7", "Datasets and Experimental Setup", "sec6-7-draft.md"),
    ("8", "Results", "sec8-draft.md"),
    ("9", "Discussion", None),
    ("10", "Threats to Validity", "sec11-draft.md"),
    ("11", "Conclusion", None),
]
CATATAN_KERJA = re.compile(r"^## (Catatan penyusunan|Checklist|Audit adversarial)", re.M)
BAGIAN_NASKAH = re.compile(r"^## \d+\.", re.M)
KODE = re.compile(r"^[A-IP]\d+[a-z]?$")
SITASI = re.compile(r"\[([A-IP]\d+[a-z]?(?:,\s*[^\]\[]+?)?)\]")
BULAN = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]


# --------------------------------------------------------------------------- prosa
def ambil_prosa(teks: str) -> str:
    awal = BAGIAN_NASKAH.search(teks)
    if awal is None:
        raise ValueError("tidak ada judul '## N.' di draf")
    akhir = CATATAN_KERJA.search(teks, awal.start())
    isi = teks[awal.start(): akhir.start() if akhir else len(teks)]
    return re.sub(r"\n---\s*$", "\n", isi.rstrip()) + "\n"


def rapikan_baris(md: str) -> str:
    keluar = []
    for baris in md.splitlines():
        b = re.sub(r"^>\s?", "", baris)
        b = re.sub(r"[\u2600-\u27BF\U0001F300-\U0001FAFF]\ufe0f?\s?", "", b) if not b.startswith("|") else b
        if b.startswith("#") or b.startswith("!["):
            keluar.append(b)
            continue
        if b.startswith("|"):
            keluar.append(b.replace("**", "").replace("`", ""))
            continue
        lead = re.match(r"^(\*\*[^*]+?[.:)]\*\*)(.*)$", b)
        if lead:
            keluar.append(lead.group(1) + lead.group(2).replace("**", ""))
        else:
            keluar.append(b.replace("**", ""))
    return "\n".join(keluar)


def tag_persamaan(md: str) -> str:
    # \tfrac menjadi pecahan linear tanpa kurung di OMML: 1/K_1+1 alih-alih 1/(K_1+1).
    md = re.sub(r"\\[td]frac\b", r"\\frac", md)
    return re.sub(r"\\tag\{([^}]+)\}", r"\\qquad\\text{(\1)}", md)


def nomori_tabel(md: str) -> str:
    peta: dict[str, str] = {}
    romawi = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
    for m in re.finditer(r"^\*\*Table (\d+\.\d+)\.\*\*", md, re.M):
        peta.setdefault(m.group(1), romawi[len(peta)])
    md = re.sub(r"^\*\*Table (\d+\.\d+)\.\*\*\s*(.+)$",
                lambda m: f"::TABEL:: TABLE {peta[m.group(1)]}::{m.group(2).strip()}", md, flags=re.M)
    md = re.sub(r"Table (\d+\.\d+)", lambda m: f"Table {peta.get(m.group(1), m.group(1))}", md)
    return md


def gambar(md: str) -> str:
    def ganti(m: re.Match) -> str:
        cap = m.group(1).replace("**", "")
        lebar = "3.4in" if any(k in m.group(2) for k in ("fig2", "fig5", "fig6")) else "6.6in"
        return f"![{cap}]({m.group(2)}){{width={lebar}}}"
    return re.sub(r"^!\[(.+?)\]\((.+?)\)[ \t]*$", ganti, md, flags=re.M)


# ------------------------------------------------------------------------- sitasi
def ganti_sitasi(md: str) -> tuple[str, list[str]]:
    urutan: list[str] = []

    def nomor(kode: str) -> int:
        if kode not in urutan:
            urutan.append(kode)
        return urutan.index(kode) + 1

    def ganti(m: re.Match) -> str:
        token = [t.strip() for t in m.group(1).split(",")]
        kode = [t for t in token if KODE.match(t)]
        lokasi = [t for t in token if not KODE.match(t) and t.lower() != "preprint"]
        if not kode:
            return m.group(0)
        n = [nomor(k) for k in kode]
        if lokasi and len(n) == 1:
            return f"[{n[0]}, {', '.join(lokasi).replace('Thm.', 'Th.')}]"
        n = sorted(set(n))
        if len(n) >= 3 and n[-1] - n[0] == len(n) - 1:
            return f"[{n[0]}]–[{n[-1]}]"
        return ", ".join(f"[{x}]" for x in n)

    teks_baru = []
    for potong in re.split(r"(\$\$.*?\$\$)", md, flags=re.S):
        teks_baru.append(potong if potong.startswith("$$") else SITASI.sub(ganti, potong))
    return "".join(teks_baru), urutan


def inisial(given: str) -> str:
    bagian = []
    for kata in given.replace(".", ". ").split():
        if "-" in kata:
            bagian.append("-".join(p[0] + "." for p in kata.split("-") if p))
        elif kata:
            bagian.append(kata[0] + ".")
    return " ".join(bagian)


def nama_penulis(penulis: list[dict]) -> str:
    nama = [(f"{inisial(a['given'])} {a['family']}".strip()) for a in penulis]
    if len(nama) > 6:
        return f"{nama[0]} *et al.*"
    if len(nama) <= 2:
        return " and ".join(nama)
    return ", ".join(nama[:-1]) + ", and " + nama[-1]


def bersih(t: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()


def entri_ieee(r: dict) -> str:
    pen = nama_penulis(r["penulis"])
    judul = bersih(r["judul"]).rstrip(".")
    tgl = (f"{BULAN[r['bulan'] - 1]} " if r.get("bulan") else "") + str(r["tahun"])
    if r["jenis"] == "preprint":
        return f'{pen}, "{judul}," arXiv:{r["arxiv"]}, {tgl}.'
    if r.get("dataset") or r["jenis"] == "dataset":
        venue = "PhysioNet" if "physionet" in r["venue"].lower() else r["venue"]
        versi = f", ver. {r['versi']}" if r.get("versi") else ""
        return f'{pen}, "{judul}," {venue}{versi}, {r["tahun"]}, doi: {r["doi"]}.'
    venue = bersih(r.get("venue_singkat") or r["venue"])
    bagian = [f"*{venue}*"]
    if r["jenis"] == "proceedings-article":
        bagian = [f"in *{bersih(r['venue'])}*"]
    if r.get("volume"):
        bagian.append(f"vol. {r['volume']}")
    if r.get("nomor"):
        bagian.append(f"no. {r['nomor']}")
    hal = r.get("halaman") or ""
    if hal and hal != r["doi"].split("/")[-1].split(".")[-1]:
        bagian.append(f"pp. {hal.replace('-', '–')}" if "-" in hal else f"Art. no. {hal}")
    bagian.append(tgl)
    return f'{pen}, "{judul}," ' + ", ".join(bagian) + f", doi: {r['doi']}."


def daftar_pustaka(urutan: list[str]) -> str:
    refs = json.loads(REFS.read_text(encoding="utf-8"))
    hilang = [k for k in urutan if k not in refs]
    if hilang:
        raise SystemExit(f"Rujukan tanpa metadata: {hilang} -> jalankan scripts/fetch_references.py")
    baris = ["## References", ""]
    for i, k in enumerate(urutan, 1):
        baris.append(f"::REF::[{i}]::{entri_ieee(refs[k])}")
        baris.append("")
    return "\n".join(baris)


# ------------------------------------------------------------------------- susun
def susun_markdown() -> tuple[str, int]:
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True).stdout.strip() or "?"
    potong = [f"# {JUDUL}\n",
              f"*Working draft for internal review — generated {datetime.date.today():%Y-%m-%d} "
              f"from commit {commit}. Sections marked NOT YET WRITTEN are intentionally empty.*\n"]
    for nomor, judul, berkas in URUTAN:
        if berkas is None:
            potong.append(f"## {nomor}. {judul}\n\n[NOT YET WRITTEN]\n")
            continue
        isi = ambil_prosa((PAPER / berkas).read_text(encoding="utf-8"))
        if berkas == "sec11-draft.md":
            isi = re.sub(r"^(#+ )11(\.)", rf"\g<1>{nomor}\2", isi, flags=re.M)
            isi = re.sub(r"(#+ )11\.(\d)", rf"\g<1>{nomor}.\2", isi)
            isi = re.sub(r"§11\.(\d)", rf"§{nomor}.\1", isi)
        potong.append(isi)
    md = "\n\n".join(potong)
    md = re.sub(r"§11\.(\d)", r"§10.\1", md)
    md = re.sub(r"§11\b", "§10", md)
    md = rapikan_baris(md)
    md = tag_persamaan(md)
    md = nomori_tabel(md)
    md = gambar(md)
    md, urutan = ganti_sitasi(md)
    md += "\n\n" + daftar_pustaka(urutan)
    return md, len(urutan)


# --------------------------------------------------------------------- gaya Word
def siapkan_reference_docx(path: pathlib.Path) -> None:
    pypandoc.convert_text("", "docx", format="markdown", outputfile=str(path))
    doc = Document(path)
    hitam = RGBColor(0, 0, 0)
    for nama, ukuran, tebal, miring in (("Title", 16, True, False), ("Heading 1", 12, True, False),
                                        ("Heading 2", 11, True, False), ("Heading 3", 11, False, True),
                                        ("Heading 4", 11, False, True)):
        if nama in [s.name for s in doc.styles]:
            g = doc.styles[nama]
            g.font.name, g.font.size, g.font.bold, g.font.italic = "Times New Roman", Pt(ukuran), tebal, miring
            g.font.color.rgb = hitam
            rpr = g.element.get_or_add_rPr()
            rpr.get_or_add_rFonts().set(qn("w:asciiTheme"), "")
            for atr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
                rpr.get_or_add_rFonts().attrib.pop(qn(atr), None)
            rpr.get_or_add_rFonts().set(qn("w:ascii"), "Times New Roman")
            rpr.get_or_add_rFonts().set(qn("w:hAnsi"), "Times New Roman")
            g.paragraph_format.space_before = Pt(12 if nama == "Heading 1" else 8)
            g.paragraph_format.space_after = Pt(4)
    for nama in ("Normal", "Body Text", "First Paragraph", "Compact", "Image Caption", "Table Caption"):
        if nama in [s.name for s in doc.styles]:
            g = doc.styles[nama]
            g.font.name = "Times New Roman"
            g.font.size = Pt(9 if "Caption" in nama else 10.5)
            g.font.color.rgb = hitam
            g.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Times New Roman")
    doc.save(path)


def beri_garis_tabel(tabel) -> None:
    tblPr = tabel._tbl.tblPr
    garis = OxmlElement("w:tblBorders")
    for sisi, ukuran in (("top", "8"), ("bottom", "8"), ("insideH", "2")):
        e = OxmlElement(f"w:{sisi}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), ukuran)
        e.set(qn("w:color"), "000000")
        garis.append(e)
    tblPr.append(garis)
    tabel.alignment = WD_TABLE_ALIGNMENT.CENTER
    for baris in tabel.rows:
        for sel in baris.cells:
            for p in sel.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(8.5)
    for sel in tabel.rows[0].cells:
        for p in sel.paragraphs:
            for r in p.runs:
                r.font.bold = True


def rapikan_docx(path: pathlib.Path) -> None:
    doc = Document(path)
    for p in doc.paragraphs:
        teks = p.text
        if teks.startswith("::TABEL::"):
            _, _, label, cap = teks.split("::", 3)
            for r in p.runs:
                r.text = ""
            r1 = p.add_run(label.strip())
            r1.font.size = Pt(9)
            p.add_run("\n")
            r2 = p.add_run(cap.strip().upper())
            r2.font.size = Pt(8)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(8)
        elif teks.startswith("::REF::"):
            _, _, no, isi = teks.split("::", 3)
            for r in p.runs:
                r.text = ""
            p.add_run(f"{no}\t").font.size = Pt(9)
            # kembalikan huruf miring venue (*...*) yang hilang saat teks digabung
            for i, bag in enumerate(re.split(r"\*(.+?)\*", isi)):
                run = p.add_run(bag)
                run.italic = i % 2 == 1
                run.font.size = Pt(9)
            pf = p.paragraph_format
            pf.left_indent, pf.first_line_indent = Pt(22), Pt(-22)
            pf.space_after = Pt(2)
            pf.tab_stops.add_tab_stop(Pt(22))
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        elif p.style.name in ("Body Text", "First Paragraph", "Normal") and len(teks) > 80:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        elif p.style.name == "Title":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif p.style.name in ("Image Caption", "Captioned Figure"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for t in doc.tables:
        beri_garis_tabel(t)
    doc.save(path)


def main() -> int:
    md, n_ref = susun_markdown()
    with tempfile.TemporaryDirectory() as tmp:
        ref = pathlib.Path(tmp) / "reference.docx"
        siapkan_reference_docx(ref)
        pypandoc.convert_text(
            md, "docx", format="markdown+tex_math_dollars+pipe_tables+implicit_figures",
            outputfile=str(KELUAR),
            extra_args=["--shift-heading-level-by=-1", f"--resource-path={PAPER}",
                        f"--reference-doc={ref}"],
        )
    rapikan_docx(KELUAR)
    print(f"Ditulis: {KELUAR.relative_to(ROOT)}  ({KELUAR.stat().st_size / 1024:.0f} KB, {n_ref} rujukan)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
