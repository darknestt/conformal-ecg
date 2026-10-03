"""Bangkitkan seluruh figure naskah langsung dari results/raw/*.json.

Tidak ada angka yang diketik tangan: setiap titik, batang, dan selang dibaca dari
berkas hasil yang sama yang dipakai tabel. Pengecualian: Fig. 1 adalah skema
delapan rekaman hipotetis (diberi label demikian di keterangannya). Keluaran
300 dpi, lebar satu kolom ganda IEEE (7,16 in) atau satu kolom (3,5 in).

    python scripts/make_figures.py   -> docs/paper/figures/fig{1..8}_*.png
"""

from __future__ import annotations

import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Arc, FancyArrowPatch, FancyBboxPatch, Patch  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw"
BI = RAW / "backbone_invariance"
KELUAR = ROOT / "docs" / "paper" / "figures"

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 8, "axes.labelsize": 8,
    "axes.titlesize": 8.5, "legend.fontsize": 7, "xtick.labelsize": 7,
    "ytick.labelsize": 7, "axes.linewidth": 0.6, "lines.linewidth": 1.0,
    "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})
LEBAR_GANDA, LEBAR_TUNGGAL = 7.16, 3.5
WARNA = {"B1": "#1f4e79", "B12": "#c55a11", "mit": "#1f4e79", "ptb": "#c55a11", "abu": "#7f7f7f"}


def muat(nama: str):
    return json.loads((RAW / nama).read_text(encoding="utf-8"))


def simpan(fig, nama: str) -> None:
    fig.savefig(KELUAR / nama)
    plt.close(fig)
    print(f"  {nama}")


def fig_join() -> None:
    """Skema Proposisi 2: dua sumber bersilang, join = komponen terhubung."""
    pasien = [(1, 2), (3,), (4, 5), (6,), (7, 8)]
    perangkat = [(1, 3, 5), (2, 4, 6), (7, 8)]
    komponen = [(1, 6), (7, 8)]
    fig, ax = plt.subplots(figsize=(LEBAR_TUNGGAL, 1.25))
    ax.set_xlim(0.4, 8.6)
    ax.set_ylim(-1.55, 0.95)
    ax.axis("off")
    for a, b in komponen:
        ax.add_patch(FancyBboxPatch((a - 0.38, -0.36), b - a + 0.76, 0.72,
                                    boxstyle="round,pad=0.02,rounding_size=0.3",
                                    fc="#e2e2e2", ec="none", zorder=0))

    def busur(x1, x2, atas, gaya, warna):
        lebar = x2 - x1
        ax.add_patch(Arc(((x1 + x2) / 2, 0.22 if atas else -0.22), lebar, 0.55 * lebar + 0.35,
                         theta1=0 if atas else 180, theta2=180 if atas else 360,
                         ls=gaya, lw=0.9, color=warna))

    for g in pasien:
        for x1, x2 in zip(g, g[1:]):
            busur(x1, x2, True, "-", WARNA["ptb"])
    for g in perangkat:
        for x1, x2 in zip(g, g[1:]):
            busur(x1, x2, False, "--", WARNA["mit"])
    for x in range(1, 9):
        ax.plot(x, 0, "o", ms=7, mfc="white", mec="black", mew=0.6, zorder=3)
        ax.text(x, 0, f"{x}", ha="center", va="center", fontsize=5.8, zorder=4)
    ax.plot([], [], "-", color=WARNA["ptb"], label="same patient (5 blocks)")
    ax.plot([], [], "--", color=WARNA["mit"], label="same device (3 blocks)")
    tangan, label = ax.get_legend_handles_labels()
    tangan.append(Patch(fc="#e2e2e2", ec="none"))
    label.append("join (2 blocks)")
    ax.legend(tangan, label, loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False,
              handlelength=1.6, columnspacing=1.0, fontsize=6.3)
    simpan(fig, "fig2_join_schematic.png")


def fig_atribusi() -> None:
    """(a) Efek faktorial 2x2 pada cakupan B1; (b) selisih B12-B1 asli vs. permutasi."""
    fk = muat("factorial_mitdb.json")["hasil"]
    cp = muat("control_permutation_mitdb.json")["hasil"]
    alfa = ["0.10", "0.15", "0.20"]
    gaya = {"0.10": ("o", -0.2), "0.15": ("s", 0.0), "0.20": ("^", 0.2)}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(LEBAR_GANDA, 2.25), gridspec_kw={"width_ratios": [1.1, 1]})

    efek = [("efek_klaster", "Clustering"), ("efek_ketimpangan", "Block-size\nimbalance"),
            ("interaksi", "Interaction")]
    for i, (kunci, _) in enumerate(efek):
        for a in alfa:
            m, dy = gaya[a]
            v = fk[a][kunci]
            sig = v["ci"][1] < 0 or v["ci"][0] > 0
            ax1.errorbar(v["nilai"] * 100, i + dy,
                         xerr=[[(v["nilai"] - v["ci"][0]) * 100], [(v["ci"][1] - v["nilai"]) * 100]],
                         fmt=m, ms=3.2, mfc=WARNA["mit"] if sig else "white", mec=WARNA["mit"],
                         color=WARNA["mit"], capsize=1.5, elinewidth=0.6)
    ax1.axvline(0, color="black", lw=0.6)
    ax1.set_yticks(range(len(efek)))
    ax1.set_yticklabels([n for _, n in efek])
    ax1.invert_yaxis()
    ax1.set_xlabel("Effect on B1 coverage [pp] (Monte Carlo 95% interval)")
    ax1.set_title("(a) 2$\\times$2 factorial design")
    for a in alfa:
        ax1.plot([], [], gaya[a][0], color=WARNA["mit"], ms=3.2, label=f"$\\alpha$={float(a):g}")
    ax1.plot([], [], "o", mfc="white", mec=WARNA["mit"], ms=3.2, label="interval includes 0")
    ax1.legend(loc="upper right", frameon=False, ncol=2, columnspacing=0.8, handletextpad=0.2)

    x = np.arange(len(alfa))
    for j, (lengan, nama, warna) in enumerate((("asli", "original data", WARNA["mit"]),
                                                ("permutasi", "dependence removed", "#9dc3e6"))):
        d = np.array([cp[a][lengan]["d"] for a in alfa]) * 100
        lo = np.array([cp[a][lengan]["d_ci"][0] for a in alfa]) * 100
        hi = np.array([cp[a][lengan]["d_ci"][1] for a in alfa]) * 100
        ax2.bar(x + (j - 0.5) * 0.36, d, width=0.36, color=warna, label=nama, lw=0)
        ax2.errorbar(x + (j - 0.5) * 0.36, d, yerr=[d - lo, hi - d], fmt="none", ecolor="black",
                     elinewidth=0.5, capsize=1.5)
    for i, a in enumerate(alfa):
        ax2.text(i, 26.0, f"{cp[a]['dd']['porsi_mekanis']:.0%}", ha="center", fontsize=6.3)
    ax2.text(1, 28.4, "mechanical share (permuted gap / original gap)", fontsize=6.3, ha="center")
    ax2.set_ylim(0, 37)
    ax2.set_yticks(range(0, 26, 5))
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{float(a):g}" for a in alfa])
    ax2.set_xlabel("Target miscoverage $\\alpha$")
    ax2.set_ylabel("B12 $-$ B1 coverage [pp]")
    ax2.set_title("(b) HCP advantage with and without dependence")
    ax2.legend(loc="upper center", ncol=2, frameon=False)
    fig.tight_layout(w_pad=1.5)
    simpan(fig, "fig7_attribution.png")


def fig1_alur() -> None:
    """Alur audit dua tahap: tahap 1 metadata saja (RQ1), tahap 2 skor model (RQ2)."""
    fig, ax = plt.subplots(figsize=(LEBAR_GANDA, 5.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.set_aspect("equal")
    ax.axis("off")
    tinta, garis = "#2b2b2b", "#555555"
    # palet lembut: (isi, tepi)
    data, biru, oranye = ("#dcecdc", "#93bf93"), ("#d6e4f0", "#8fb0cf"), ("#fbe1cc", "#e0a982")
    krem, mawar, mint, emas = ("#fff6d6", "#d8c37a"), ("#f7dada", "#d9a0a0"), ("#d8eedd", "#86b991"), ("#fde9b8", "#d1ad57")

    def panel(x, y, w, h):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc="white", ec=garis, lw=1.1))

    def judul(xc, yc, w, teks, warna):
        ax.add_patch(FancyBboxPatch((xc - w / 2, yc - 1.35), w, 2.7, boxstyle="round,pad=0,rounding_size=1.35",
                                    fc=warna[0], ec=warna[1], lw=0.8))
        ax.text(xc, yc, teks, ha="center", va="center", fontsize=6.6, fontweight="bold", color=tinta)

    def kotak(x, y, w, h, teks, warna=krem, fs=5.9, bulat=0.0, tebal=False):
        gaya = f"round,pad=0,rounding_size={bulat}" if bulat else "square,pad=0"
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=gaya, fc=warna[0], ec=warna[1], lw=0.7))
        ax.text(x + w / 2, y + h / 2, teks, ha="center", va="center", fontsize=fs, linespacing=1.2,
                color=tinta, fontweight="bold" if tebal else "normal")

    def panah(titik, ls="-", teks=None, xyteks=None, rot=0):
        xs, ys = zip(*titik)
        if len(titik) > 2:
            ax.plot(xs[:-1], ys[:-1], color=garis, lw=0.9, ls=ls, solid_capstyle="butt")
        ax.add_patch(FancyArrowPatch(titik[-2], titik[-1], arrowstyle="-|>", mutation_scale=8, lw=0.9,
                                     color=garis, linestyle=ls, shrinkA=0, shrinkB=0))
        if teks:
            ax.text(*xyteks, teks, fontsize=5.9, color=tinta, ha="center", va="center", rotation=rot,
                    style="italic")

    def lingkaran(xc, yc, r, teks, warna, fs=6.2):
        ax.add_patch(plt.Circle((xc, yc), r, fc=warna[0], ec=warna[1], lw=0.9))
        ax.text(xc, yc, teks, ha="center", va="center", fontsize=fs, fontweight="bold", color=tinta,
                linespacing=1.15)

    def langkah(nomor, x, y, w, h, kepala, isi):
        ax.add_patch(plt.Circle((x - 2.1, y + h / 2), 1.45, fc=emas[0], ec=emas[1], lw=0.8))
        ax.text(x - 2.1, y + h / 2, str(nomor), ha="center", va="center", fontsize=6.4, fontweight="bold")
        ujung = 1.6
        ax.add_patch(plt.Polygon([(x, y), (x + w - ujung, y), (x + w, y + h / 2), (x + w - ujung, y + h), (x, y + h)],
                                 closed=True, fc=krem[0], ec=krem[1], lw=0.7))
        ax.text(x + 0.9, y + h * 0.69, kepala, ha="left", va="center", fontsize=6.0, fontweight="bold", color=tinta)
        ax.text(x + 0.9, y + h * 0.30, isi, ha="left", va="center", fontsize=5.9, color=tinta)

    # A1: sumber data
    panel(1, 41.5, 30, 27.5)
    judul(16, 66.6, 17, "DATA SOURCES", data)
    for x0, nama, butir in ((2.5, "PTB-XL", ("12-lead, multi-label", "5 superclasses", "18,869 patients",
                                             "4 declared sources")),
                            (16.5, "MIT-BIH", ("MLII lead, beats", "5 AAMI classes", "22 DS2 records",
                                               "source: record"))):
        kotak(x0, 61.6, 13, 2.6, nama, data, fs=6.2, tebal=True)
        for i, b in enumerate(butir):
            kotak(x0, 59.2 - i * 2.45, 13, 2.2, b)
    kotak(2.5, 47.0, 27, 4.1, "Challenge 2021: 7 sources,\npatient identifier undocumented", fs=5.8)
    kotak(2.5, 42.3, 27, 4.1, "Declared dependence sources $D$: patient, site,\nnurse, device (PTB-XL); record (MIT-BIH)",
          mawar, fs=5.8)

    # A2: tahap 1, metadata saja
    panah([(16, 41.5), (16, 37.5)], teks="metadata only", xyteks=(22.0, 39.5))
    panel(1, 1, 30, 36.5)
    judul(16, 34.6, 26, "STAGE 1 \u00b7 FEASIBILITY (RQ1)", biru)
    ax.text(16, 31.3, "exact given $D$, before any model is trained", ha="center", va="center",
            fontsize=5.9, style="italic", color=tinta)
    for i, (kepala, isi) in enumerate((
            ("Observability", "is each source documented?"),
            ("Sufficiency (\u00a73.3)", "join of $D$ = connected components"),
            ("Feasibility (\u00a73.2)", "$\\alpha \\geq 1/(K_1+1)$ for each grouping"),
            ("Label level (\u00a73.4)", "$K_1(\\ell)$ per diagnosis (necessary only)"))):
        langkah(i + 1, 5.6, 24.6 - i * 5.7, 24.2, 4.7, kepala, isi)
    kotak(2.5, 2.2, 27, 4.4, "Verdicts (\u00a75.1): $\\alpha_{\\min}$, admissible\ngroupings, failing labels",
          mawar, fs=6.0, tebal=True)

    # B1: tahap 2, kalibrasi pada alpha yang layak
    panah([(31, 58), (35, 58)])
    ax.text(33, 59.3, "scores", fontsize=5.3, color=tinta, ha="center", va="center", style="italic")
    panah([(31, 19), (33, 19), (33, 47), (35, 47)], ls="--", teks="feasible $\\alpha$ only",
          xyteks=(32.0, 33), rot=90)
    panel(35, 38, 30, 31)
    judul(50, 66.6, 27, "STAGE 2 \u00b7 CALIBRATION (RQ2)", oranye)
    hx, hy, hr = 41.6, 51.5, 5.6
    lingkaran(hx, hy, hr, "CONFORMAL\nCALIBRATION", mint, fs=5.4)
    satelit = ("3 backbones,\n2 checkpoints", "B1: split\nconformal", "B12: HCP,\nblock level",
               "splits by block,\n200\u2013400 repeats", "coverage: obs.-\n& block-weighted")
    for i, t in enumerate(satelit):
        yc = 61.2 - i * 4.85
        sudut = np.arctan2(yc - hy, 9)
        ax.plot([hx + hr * np.cos(sudut), 49.6], [hy + hr * np.sin(sudut), yc], color=garis, lw=0.6)
        ax.add_patch(plt.Circle((49.6, yc), 0.55, fc=emas[0], ec=emas[1], lw=0.6, zorder=3))
        kotak(50.5, yc - 2.0, 10.6, 4.0, t, krem, fs=5.5, bulat=0.8)
    kotak(61.8, 39.6, 2.5, 24.2, "", mawar)
    ax.text(63.05, 51.7, "Output: coverage and set size (\u00a75.2)", rotation=270, ha="center", va="center",
            fontsize=5.9, fontweight="bold", color=tinta)

    # B2: atribusi defisit B1
    panah([(50, 38), (50, 34)], teks="B1 deficit", xyteks=(54.6, 36.0))
    panel(35, 1, 30, 33)
    judul(50, 31.1, 25, "ATTRIBUTION (\u00a75.3\u2013\u00a75.4)", oranye)
    cx, cy, cr = 50, 16.0, 5.0
    lingkaran(cx, cy, cr, "ATTRIBUTE\nDEFICIT", mint, fs=5.6)
    for (x0, y0, t) in ((35.9, 18.6, "Permutation\nnull"), (35.9, 9.4, "Mechanical\nshare of HCP\nadvantage"),
                        (55.2, 18.6, "2$\\times$2 factorial:\nclustering $\\times$\nimbalance"),
                        (55.2, 9.4, "Dose\u2013response\nof deficit vs.\n$1+(H-1)\\rho$")):
        kotak(x0, y0, 8.9, 5.4, t, krem, fs=5.5)
        tx, ty = x0 + (8.9 if x0 < cx else 0), y0 + 2.7
        sudut = np.arctan2(ty - cy, tx - cx)
        panah([(cx + cr * np.cos(sudut), cy + cr * np.sin(sudut)), (tx, ty)])
    kotak(39.5, 25.3, 21, 2.4, "Input: B1 coverage deficit per $\\alpha$", krem, fs=5.6)
    panah([(50, 25.3), (50, cy + cr)])
    kotak(37.5, 2.2, 25, 4.4, "Output: share of the deficit\nattributable to dependence", mawar, fs=6.0, tebal=True)

    # C2: ketidakpastian dan robustness
    panah([(65, 13), (69, 13)])
    panel(69, 1, 30, 25)
    judul(84, 23.1, 27, "UNCERTAINTY & ROBUSTNESS", oranye)
    for i, t in enumerate(("Monte Carlo splits,\nconditional on 22 records",
                           "leave-one-record-out\njackknife, $t$ with 21 df",
                           "3 backbones $\\times$\n2 checkpoints (\u00a75.5)")):
        yc = 17.6 - i * 5.1
        ax.add_patch(plt.Circle((72.0, yc), 1.3, fc=emas[0], ec=emas[1], lw=0.7))
        ax.text(72.0, yc, str(i + 1), ha="center", va="center", fontsize=6.0, fontweight="bold")
        kotak(73.8, yc - 2.0, 15.6, 4.0, t, krem, fs=5.6, bulat=1.2)
    sx, sy, sr = 94.3, 12.5, 4.0
    for a, b in (((sx + sr, sy + 0.4), (sx - sr, sy + 0.4)), ((sx - sr, sy - 0.4), (sx + sr, sy - 0.4))):
        ax.add_patch(FancyArrowPatch(a, b, connectionstyle="arc3,rad=0.95", arrowstyle="-|>", mutation_scale=7,
                                     lw=1.3, color="#9aa7b4", shrinkA=0, shrinkB=0))
    ax.text(sx, sy, "repeat\nper\nbackbone\nand $\\alpha$", ha="center", va="center", fontsize=5.0, color=tinta,
            linespacing=1.05)
    kotak(70.5, 2.2, 27, 2.6, "split-level and subject-level intervals", mawar, fs=5.9, tebal=True)

    # C1: temuan
    panah([(84, 26), (84, 30)])
    panel(69, 30, 30, 39)
    judul(84, 66.6, 27, "FINDINGS (RQ2)", oranye)
    temuan = ("Coverage of B1 vs. B12 (\u00a75.2)", "Deficit vs. permutation null (\u00a75.3)",
              "Clustering vs. imbalance (\u00a75.3)", "Deficit vs. design effect (\u00a75.4)",
              "Backbone and checkpoint (\u00a75.5)")
    for i, t in enumerate(temuan):
        yc = 61.8 - i * 4.6
        kotak(71.5, yc - 1.25, 25, 2.5, t, krem, fs=5.8, bulat=1.25)
        if i:
            panah([(84, yc + 3.35), (84, yc + 1.25)])
    for xc, t in ((75.2, "SmallECGNet"), (84, "ResNet1D-34"), (92.8, "ResNet1D-50")):
        panah([(84, 42.15), (xc, 39.6)])
        kotak(xc - 4.2, 37.3, 8.4, 2.3, t, krem, fs=5.2, bulat=1.15)
    kotak(70.5, 31.4, 27, 4.4, "Reported with split- and subject-level\nuncertainty (\u00a76.2)", mawar, fs=5.9,
          tebal=True)
    simpan(fig, "fig1_audit_workflow.png")


def fig_geometri() -> None:
    """Ukuran blok menurut peringkat: lebar kurva = K (kelayakan), tinggi = ukuran blok (DEff)."""
    g = muat("block_geometry.json")
    fig, ax = plt.subplots(figsize=(LEBAR_TUNGGAL, 2.3))
    seri = [("ptbxl_patient_id", "PTB-XL patient", WARNA["ptb"], "-"),
            ("ptbxl_site", "PTB-XL site", WARNA["ptb"], "--"),
            ("ptbxl_nurse", "PTB-XL nurse", WARNA["ptb"], ":"),
            ("ptbxl_device", "PTB-XL device", WARNA["ptb"], "-."),
            ("mitdb_record", "MIT-BIH record", WARNA["mit"], "-")]
    for kunci, nama, warna, gaya in seri:
        u = np.asarray(g[kunci]["ukuran"])
        h = g[kunci]["H"]
        ax.step(np.arange(1, u.size + 1), u, where="post", color=warna, ls=gaya, lw=1.1,
                label=f"{nama} ($K$={u.size:,}, $H$={h:.2f})" if h < 10 else f"{nama} ($K$={u.size:,}, $H$={h:,.0f})")
    ax.axvline(19, color=WARNA["abu"], lw=0.6, ls=":")
    ax.text(21, 1.25, "$K_{\\min}(0.05)=19$", fontsize=6, color=WARNA["abu"])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.8, 3e4)
    ax.set_ylim(0.7, 3e4)
    ax.set_xlabel("Block rank (largest first); curve length = number of blocks $K$")
    ax.set_ylabel("Block size $N_k$")
    ax.legend(loc="upper right", frameon=False, fontsize=5.6, handlelength=2.2)
    simpan(fig, "fig3_block_geometry.png")


def fig2_kelayakan() -> None:
    """Batas kelayakan alpha_min = 1/(K1+1) dan posisi tiap pengelompokan nyata."""
    fa = {g["grouping"]: g for g in muat("feasibility_alpha.json")}
    gab = muat("block_nesting.json")["gabungan"]
    k = np.logspace(0, 3.5, 300)
    fig, ax = plt.subplots(figsize=(LEBAR_TUNGGAL, 2.6))
    ax.plot(k, 1 / (k + 1), color="black", lw=1.0)
    ax.fill_between(k, 1 / (k + 1), 1, color="#d9d9d9", alpha=0.6, lw=0)
    ax.text(1.6, 0.0016, "feasible region\n$\\alpha \\geq 1/(K_1+1)$", fontsize=6.5)
    for a in (0.01, 0.05, 0.10):
        ax.axhline(a, color=WARNA["abu"], lw=0.5, ls=":")
        ax.text(2400, a * 1.08, f"$\\alpha$={a:g}", fontsize=6, ha="right", color=WARNA["abu"])
    titik = [
        ("patient", fa["patient_id"]["blocks_calibration"], WARNA["ptb"], "o"),
        ("site", fa["site"]["blocks_calibration"], WARNA["ptb"], "o"),
        ("nurse", fa["nurse"]["blocks_calibration"], WARNA["ptb"], "o"),
        ("device", fa["device"]["blocks_calibration"], WARNA["ptb"], "o"),
        ("patient $\\vee$ nurse", gab["patient_id + nurse"]["blok_kalibrasi"], WARNA["ptb"], "s"),
        ("patient $\\vee$ site", gab["patient_id + site"]["blok_kalibrasi"], WARNA["ptb"], "s"),
        ("patient $\\vee$ device", gab["patient_id + device"]["blok_kalibrasi"], WARNA["ptb"], "s"),
        ("all four", gab["patient_id + site + device + nurse"]["blok_kalibrasi"], WARNA["ptb"], "s"),
        ("MIT-BIH records", muat("control_permutation_mitdb.json")["k1"], WARNA["mit"], "D"),
    ]
    geser = {"patient": (-6, 5), "site": (5, 2), "nurse": (5, -3), "device": (-30, -8),
             "patient $\\vee$ nurse": (5, 0), "patient $\\vee$ site": (-12, 6),
             "patient $\\vee$ device": (5, 2), "all four": (5, 0), "MIT-BIH records": (-20, 8)}
    for nama, k1, w, m in titik:
        y = 1 / (k1 + 1)
        ax.plot(k1, y, m, ms=3.6, mfc=w, mec="black", mew=0.4, zorder=3)
        ax.annotate(f"{nama} ({k1:,})", (k1, y), xytext=geser[nama], textcoords="offset points", fontsize=5.8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.8, 3000)
    ax.set_ylim(3e-4, 0.8)
    ax.set_xlabel("Calibration blocks $K_1$")
    ax.set_ylabel("Smallest attainable $\\alpha$")
    ax.plot([], [], "o", mfc=WARNA["ptb"], mec="black", mew=0.4, ms=3.6, label="PTB-XL single source")
    ax.plot([], [], "s", mfc=WARNA["ptb"], mec="black", mew=0.4, ms=3.6, label="PTB-XL join of sources")
    ax.plot([], [], "D", mfc=WARNA["mit"], mec="black", mew=0.4, ms=3.6, label="MIT-BIH (DS2, 11/11)")
    ax.legend(loc="upper right", frameon=False, handletextpad=0.2)
    simpan(fig, "fig4_feasibility_frontier.png")


def fig4_label() -> None:
    """K1 per label pada tiga tingkat hierarki PTB-XL."""
    lf = muat("label_feasibility.json")
    fig, axs = plt.subplots(1, 3, figsize=(LEBAR_GANDA, 2.3), sharey=True,
                            gridspec_kw={"width_ratios": [5, 23, 44]})
    judul = {"superclass": "Superclass (5)", "subclass": "Subclass (23)", "scp_code": "SCP statement (44)"}
    for ax, lvl in zip(axs, ["superclass", "subclass", "scp_code"]):
        lab = sorted(lf[lvl]["label"].items(), key=lambda t: -t[1]["blok_kalibrasi"])
        k1 = np.array([v["blok_kalibrasi"] for _, v in lab])
        warna = np.where(k1 >= 19, WARNA["mit"], np.where(k1 >= 9, "#9dc3e6", WARNA["ptb"]))
        ax.bar(range(len(k1)), k1, color=warna, width=0.8, lw=0)
        ax.set_yscale("log")
        ax.set_xticks(range(len(k1)))
        ax.set_xticklabels([n for n, _ in lab], rotation=90, fontsize=4.6 if lvl == "scp_code" else 5.5)
        ax.set_xlim(-0.7, len(k1) - 0.3)
        ax.set_title(judul[lvl])
        for kmin, a in ((19, 0.05), (9, 0.10)):
            ax.axhline(kmin, color="black", lw=0.5, ls="--" if a == 0.05 else ":")
        gagal = int((k1 < 19).sum())
        ax.text(0.97, 0.95, f"{gagal}/{len(k1)} fail at $\\alpha$=0.05", transform=ax.transAxes,
                ha="right", va="top", fontsize=6)
    axs[0].set_ylabel("Calibration blocks $K_1(\\ell)$")
    axs[2].text(len(lf["scp_code"]["label"]) - 0.5, 21, "$K_{\\min}(0.05)=19$", fontsize=5.8, ha="right", va="bottom")
    axs[2].text(len(lf["scp_code"]["label"]) - 0.5, 7.6, "$K_{\\min}(0.10)=9$", fontsize=5.8, ha="right", va="top")
    fig.tight_layout(w_pad=0.4)
    simpan(fig, "fig5_label_feasibility.png")


def fig5_cakupan() -> None:
    """Cakupan B1 dan B12 terhadap nominal; selang = 2,5-97,5% antar-split."""
    fig, axs = plt.subplots(1, 2, figsize=(LEBAR_GANDA, 2.4))
    for ax, ds, judul in ((axs[0], "mitdb", "MIT-BIH (DEff $\\approx$ 704)"),
                          (axs[1], "ptbxl", "PTB-XL (DEff $\\approx$ 1.02)")):
        r = json.loads((BI / f"{ds}_small.json").read_text(encoding="utf-8"))["konformal"]
        al = [float(a) for a in r]
        nom = [1 - a for a in al]
        x = np.arange(len(al))
        b1 = np.array([r[a]["B1_mean"] for a in r])
        lo = np.array([r[a]["B1_ci"][0] for a in r])
        hi = np.array([r[a]["B1_ci"][1] for a in r])
        b12 = np.array([r[a]["B12_mean"] for a in r])
        ax.errorbar(x - 0.12, b1 - np.array(nom), yerr=[b1 - lo, hi - b1], fmt="o", ms=3.2,
                    color=WARNA["B1"], capsize=1.8, elinewidth=0.6, label="B1 split conformal (2.5\u201397.5% across splits)")
        ax.plot(x + 0.12, b12 - np.array(nom), "s", ms=3.2, color=WARNA["B12"], label="B12 HCP (mean)")
        ax.axhline(0, color="black", lw=0.6)
        if ds == "mitdb":
            for i, a in enumerate(al):
                if a < 1 / 12:
                    ax.axvspan(i - 0.45, i + 0.45, color="#d9d9d9", alpha=0.6, lw=0)
            ax.text(0.5, 0.075, "$\\alpha < 1/(K_1+1)$:\nHCP returns all labels", fontsize=5.8, ha="center")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{a:g}" for a in al])
        ax.set_xlabel("Target miscoverage $\\alpha$")
        ax.set_title(judul)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda v, _: "0" if abs(v) < 1e-12 else f"{v * 100:+.0f}".replace("-", "\u2212")))
    axs[0].set_ylabel("Coverage $-$ $(1-\\alpha)$ [pp]")
    axs[0].legend(loc="lower left", frameon=False)
    fig.tight_layout(w_pad=1.0)
    simpan(fig, "fig6_coverage.png")


def fig6_dosis() -> None:
    """Defisit cakupan B1 terhadap design effect, tiga level alpha."""
    d = muat("dose_response.json")
    H = d["mitdb_H"]
    fig, ax = plt.subplots(figsize=(LEBAR_TUNGGAL, 2.5))
    gaya = {0.1: ("o", "-"), 0.15: ("s", "--"), 0.2: ("^", ":")}
    for a, (m, ls) in gaya.items():
        t = sorted([p for p in d["mitdb_titik"] if abs(p["alpha"] - a) < 1e-9], key=lambda p: p["icc"])
        deff = [1 + (H - 1) * p["icc"] for p in t]
        ax.plot(deff, [p["defisit"] * 100 for p in t], marker=m, ls=ls, ms=3, color=WARNA["mit"], lw=0.7,
                label=f"MIT-BIH, $\\alpha$={a:g}")
        dp = d["ptbxl"]["defisit"][f"{a:.2f}"]
        ax.errorbar(d["ptbxl"]["deff"], dp["defisit"] * 100,
                    yerr=[[(dp["defisit"] - dp["ci"][0]) * 100], [(dp["ci"][1] - dp["defisit"]) * 100]],
                    fmt=m, ms=3.4, color=WARNA["ptb"], capsize=1.5, elinewidth=0.6)
    ax.plot([], [], "o", color=WARNA["ptb"], ms=3.4, label="PTB-XL (Monte Carlo 95%)")
    ax.axhline(0, color="black", lw=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("Design effect $\\mathrm{DEff} = 1 + (H-1)\\rho$")
    ax.set_ylabel("B1 coverage deficit [pp]")
    sp = d["spearman_gabungan_deff"]
    ax.text(0.03, 0.97, "Spearman (12 points): " + ", ".join(f"{v['spearman']:.2f}" for v in sp.values()),
            transform=ax.transAxes, fontsize=6, va="top")
    ax.legend(loc="center left", frameon=False, bbox_to_anchor=(0.0, 0.62))
    simpan(fig, "fig8_dose_response.png")


def fig7_backbone() -> None:
    """(a) Defisit B1 terhadap null permutasi per backbone; (b) bobot terbaik vs. epoch terakhir."""
    sumber = [("SmallECGNet", RAW / "control_permutation_mitdb.json"),
              ("ResNet1D-34", BI / "control_permutation_mitdb_resnet1d34.json"),
              ("ResNet1D-50", BI / "control_permutation_mitdb_resnet1d50.json")]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(LEBAR_GANDA, 2.4), gridspec_kw={"width_ratios": [1.15, 1]})
    gaya = {"0.10": ("o", -0.18), "0.15": ("s", 0.0), "0.20": ("^", 0.18)}
    kunci_jk = {"SmallECGNet": "small", "ResNet1D-34": "resnet1d34", "ResNet1D-50": "resnet1d50"}
    for i, (nama, p) in enumerate(sumber):
        h = json.loads(p.read_text(encoding="utf-8"))["hasil"]
        jk = json.loads((RAW / "jackknife_records" / f"mitdb_{kunci_jk[nama]}.json")
                        .read_text(encoding="utf-8"))["hasil"]
        for a, (m, dy) in gaya.items():
            lo, hi = (c * 100 for c in jk[a]["ci"])
            ax.plot([lo, hi], [i + dy, i + dy], color="#bdd7ee", lw=3.2, solid_capstyle="butt", zorder=1)
            v = h[a]["defisit_B1"]
            sig = v["ci"][0] > 0
            ax.errorbar(v["nilai"] * 100, i + dy, xerr=[[(v["nilai"] - v["ci"][0]) * 100], [(v["ci"][1] - v["nilai"]) * 100]],
                        fmt=m, ms=3.2, mfc=WARNA["mit"] if sig else "white", mec=WARNA["mit"],
                        color=WARNA["mit"], capsize=1.5, elinewidth=0.6, zorder=3)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_yticks(range(len(sumber)))
    ax.set_yticklabels([n for n, _ in sumber])
    ax.invert_yaxis()
    ax.set_xlabel("B1 deficit vs. permutation null [pp]")
    for a, (m, _) in gaya.items():
        ax.plot([], [], m, color=WARNA["mit"], ms=3.2, label=f"$\\alpha$={float(a):g}")
    ax.plot([], [], "o", mfc="white", mec=WARNA["mit"], ms=3.2, label="MC interval includes 0")
    ax.plot([], [], color="#bdd7ee", lw=3.2, label="record-level 95% CI")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), frameon=False, ncol=3, columnspacing=0.8,
              handletextpad=0.3, fontsize=6.2)
    ax.set_title("(a) Deficit against the permutation null, MIT-BIH", pad=22)

    penanda = {"resnet1d34": "o", "resnet1d50": "s"}
    batas = 0.0
    for ds, warna in (("mitdb", WARNA["mit"]), ("ptbxl", WARNA["ptb"])):
        for bb, m in penanda.items():
            terbaik = json.loads((BI / f"{ds}_{bb}.json").read_text(encoding="utf-8"))["konformal"]
            akhir = json.loads((BI / f"{ds}_{bb}_terakhir.json").read_text(encoding="utf-8"))["konformal"]
            x = np.array([(terbaik[a]["B1_mean"] - terbaik[a]["target"]) * 100 for a in terbaik])
            y = np.array([(akhir[a]["B1_mean"] - akhir[a]["target"]) * 100 for a in terbaik])
            batas = max(batas, np.abs(x).max(), np.abs(y).max())
            ax2.plot(x, y, m, ms=3.4, mfc=warna, mec="black", mew=0.4, ls="none")
    batas = np.ceil(batas * 1.1)
    ax2.fill_between([-batas, 0], -batas, 0, color="#eef3f8", lw=0, zorder=0)
    ax2.fill_between([0, batas], 0, batas, color="#fbeee6", lw=0, zorder=0)
    ax2.plot([-batas, batas], [-batas, batas], color=WARNA["abu"], lw=0.6, ls=":")
    ax2.axhline(0, color="black", lw=0.5)
    ax2.axvline(0, color="black", lw=0.5)
    ax2.set_xlim(-batas, batas)
    ax2.set_ylim(-batas, batas)
    ax2.set_aspect("equal")
    ax2.set_xlabel("Best-validation weights: B1 coverage $-$ $(1-\\alpha)$ [pp]", fontsize=7)
    ax2.set_ylabel("Last-epoch weights [pp]")
    ax2.set_title("(b) Checkpoint sensitivity")
    ax2.plot([], [], "o", mfc=WARNA["mit"], mec="black", mew=0.4, ms=3.4, ls="none", label="MIT-BIH")
    ax2.plot([], [], "o", mfc=WARNA["ptb"], mec="black", mew=0.4, ms=3.4, ls="none", label="PTB-XL")
    ax2.plot([], [], "o", mfc="white", mec="black", mew=0.4, ms=3.4, ls="none", label="ResNet1D-34")
    ax2.plot([], [], "s", mfc="white", mec="black", mew=0.4, ms=3.4, ls="none", label="ResNet1D-50")
    ax2.legend(loc="upper left", frameon=False, handletextpad=0.2, fontsize=6.3)
    fig.tight_layout(w_pad=1.5)
    simpan(fig, "fig9_robustness.png")


def main() -> int:
    KELUAR.mkdir(parents=True, exist_ok=True)
    for f in (fig1_alur, fig_join, fig_geometri, fig2_kelayakan, fig4_label, fig5_cakupan, fig_atribusi, fig6_dosis,
              fig7_backbone):
        f()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
