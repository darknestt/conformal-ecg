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
    simpan(fig, "fig1_join_schematic.png")


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
    ax1.set_xlabel("Effect on B1 coverage [pp] (95% bootstrap CI)")
    ax1.set_title("(a) 2$\\times$2 factorial design")
    for a in alfa:
        ax1.plot([], [], gaya[a][0], color=WARNA["mit"], ms=3.2, label=f"$\\alpha$={float(a):g}")
    ax1.plot([], [], "o", mfc="white", mec=WARNA["mit"], ms=3.2, label="CI includes 0")
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
    simpan(fig, "fig6_attribution.png")


def fig1_alur() -> None:
    """Alur audit: keputusan kombinatorial lebih dulu, model belakangan."""
    fig, ax = plt.subplots(figsize=(LEBAR_GANDA, 1.85))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 30)
    ax.axis("off")
    kotak = [
        (1, "Declare dependence\nsources $D$", "metadata"),
        (17.5, "Observability\nis the partition\ndocumented?", "S0"),
        (34, "Sufficiency\njoin of $D$\n(connected components)", "S2"),
        (50.5, "Feasibility\n$\\alpha \\geq 1/(K_1+1)$\nper grouping and label", "S1"),
        (67, "Coverage audit\nB1 vs. permutation null", "model"),
        (83.5, "Dose\u2013response\ndeficit vs. DEff", "model"),
    ]
    for x, teks, jenis in kotak:
        tanpa_model = jenis != "model"
        ax.add_patch(FancyBboxPatch((x, 7), 15, 17, boxstyle="round,pad=0.3,rounding_size=1.2",
                                    fc="#eef3f8" if tanpa_model else "#fbeee6",
                                    ec=WARNA["mit"] if tanpa_model else WARNA["ptb"], lw=0.8))
        ax.text(x + 7.5, 15.5, teks, ha="center", va="center", fontsize=7)
    for x in (16.2, 32.7, 49.2, 65.7, 82.2):
        ax.add_patch(FancyArrowPatch((x, 15.5), (x + 1.2, 15.5), arrowstyle="-|>", mutation_scale=7, lw=0.8))
    ax.annotate("", xy=(1, 3.2), xytext=(66, 3.2), arrowprops=dict(arrowstyle="<->", lw=0.6, color=WARNA["mit"]))
    ax.text(33.5, 0.6, "No trained model required \u2014 exact given the declared sources", ha="center", fontsize=6.8, color=WARNA["mit"])
    ax.annotate("", xy=(67, 3.2), xytext=(98.5, 3.2), arrowprops=dict(arrowstyle="<->", lw=0.6, color=WARNA["ptb"]))
    ax.text(82.7, 0.6, "Requires scores from a trained model", ha="center", fontsize=6.8, color=WARNA["ptb"])
    ax.text(4.0, 26.6, "S0", fontsize=6.5, color=WARNA["abu"])
    simpan(fig, "fig2_audit_workflow.png")


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
    simpan(fig, "fig3_feasibility_frontier.png")


def fig3_label() -> None:
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
    simpan(fig, "fig4_label_feasibility.png")


def fig4_cakupan() -> None:
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
    simpan(fig, "fig5_coverage.png")


def fig5_dosis() -> None:
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
    ax.plot([], [], "o", color=WARNA["ptb"], ms=3.4, label="PTB-XL (95% CI)")
    ax.axhline(0, color="black", lw=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("Design effect $\\mathrm{DEff} = 1 + (H-1)\\rho$")
    ax.set_ylabel("B1 coverage deficit [pp]")
    sp = d["spearman_gabungan_deff"]
    ax.text(0.03, 0.97, "Spearman (12 points): " + ", ".join(f"{v['spearman']:.2f}" for v in sp.values()),
            transform=ax.transAxes, fontsize=6, va="top")
    ax.legend(loc="center left", frameon=False, bbox_to_anchor=(0.0, 0.62))
    simpan(fig, "fig7_dose_response.png")


def fig6_backbone() -> None:
    """Defisit B1 terhadap null permutasi per backbone (forest plot)."""
    sumber = [("SmallECGNet", RAW / "control_permutation_mitdb.json"),
              ("ResNet1D-34", BI / "control_permutation_mitdb_resnet1d34.json"),
              ("ResNet1D-50", BI / "control_permutation_mitdb_resnet1d50.json")]
    fig, ax = plt.subplots(figsize=(LEBAR_TUNGGAL, 2.3))
    gaya = {"0.10": ("o", -0.18), "0.15": ("s", 0.0), "0.20": ("^", 0.18)}
    for i, (nama, p) in enumerate(sumber):
        h = json.loads(p.read_text(encoding="utf-8"))["hasil"]
        for a, (m, dy) in gaya.items():
            v = h[a]["defisit_B1"]
            sig = v["ci"][0] > 0
            ax.errorbar(v["nilai"] * 100, i + dy, xerr=[[(v["nilai"] - v["ci"][0]) * 100], [(v["ci"][1] - v["nilai"]) * 100]],
                        fmt=m, ms=3.2, mfc=WARNA["mit"] if sig else "white", mec=WARNA["mit"],
                        color=WARNA["mit"], capsize=1.5, elinewidth=0.6)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_yticks(range(len(sumber)))
    ax.set_yticklabels([n for n, _ in sumber])
    ax.invert_yaxis()
    ax.set_xlabel("B1 deficit vs. permutation null [pp] (95% CI)")
    for a, (m, _) in gaya.items():
        ax.plot([], [], m, color=WARNA["mit"], ms=3.2, label=f"$\\alpha$={float(a):g}")
    ax.plot([], [], "o", mfc="white", mec=WARNA["mit"], ms=3.2, label="CI includes 0")
    ax.legend(loc="lower right", frameon=False, ncol=2, columnspacing=0.8, handletextpad=0.2)
    simpan(fig, "fig8_backbone_permutation.png")


def main() -> int:
    KELUAR.mkdir(parents=True, exist_ok=True)
    for f in (fig_join, fig1_alur, fig2_kelayakan, fig3_label, fig4_cakupan, fig_atribusi, fig5_dosis,
              fig6_backbone):
        f()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
