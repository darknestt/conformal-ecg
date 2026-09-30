"""Kurva dosis-respons tunggal: defisit cakupan terhadap ICC, lintas kedua dataset.

Sampai titik ini PTB-XL dan MIT-BIH berdiri sebagai dua hasil terpisah yang
tampak bertentangan:

    PTB-XL  : H0 TERREFUTASI  (B1 mengenai nominal)
    MIT-BIH : H0b TERKONFIRMASI (defisit naik monoton terhadap ICC)

Keduanya sebenarnya dua titik pada SATU kurva. Skrip ini menempatkan PTB-XL pada
sumbu ICC yang sama dengan 11 titik sintetis MIT-BIH, sehingga "bertentangan"
berubah menjadi "dosis rendah vs dosis tinggi".

PTB-XL: ICC dihitung pada blok pasien di fold 9 memakai backbone studi kelayakan.
Bootstrap pada level PASIEN, bukan rekaman.
MIT-BIH: titik dibaca dari results/raw/monotonicity_icc_mitdb.json.

CATATAN PENTING -- sumbunya BUKAN ICC. Percobaan pertama memakai ICC dan gagal:
PTB-XL ber-ICC 0,35 (setara titik MIT-BIH yang defisitnya +0,0035) namun
defisitnya nol. Penjelasannya ada di Prop 2' sendiri:

    DEff = 1 + (H - 1) * rho,   H = rerata harmonik ukuran blok

PTB-XL: H = 1,12 -> DEff = 1,04 meski rho = 0,35.
MIT-BIH: H = 1.355 -> DEff = 705 pada rho = 0,52.

Dependensi baru merusak kalibrasi bila ADA PENGULANGAN di dalam blok untuk
dikorelasikan. ICC tinggi pada blok nyaris-tunggal tidak berakibat apa-apa.

FOLD 10 TIDAK DISENTUH.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
import torch
from scipy.stats import spearmanr

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.feasibility import FOLD_EVAL, skor  # noqa: E402
from src.conformal import intraclass_correlation, split_conformal  # noqa: E402
from src.data.ptbxl import SUPERCLASS, load_metadata, load_signals  # noqa: E402
from src.models.small_ecg_net import SmallECGNet  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

ALPHAS = [0.10, 0.15, 0.20]
CKPT = ROOT / "results" / "raw" / "feasibility_backbone.pt"
MITDB_JSON = ROOT / "results" / "raw" / "monotonicity_icc_mitdb.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--bootstrap", type=int, default=500)
    args = ap.parse_args()

    if not CKPT.exists():
        print(f"GALAT: checkpoint PTB-XL tidak ada: {CKPT}", file=sys.stderr)
        return 1

    df = load_metadata()
    y = df[SUPERCLASS].to_numpy(dtype=np.float32)
    blok = df["patient_id"].to_numpy()
    fold = df["strat_fold"].to_numpy()
    punya = df["n_superclass"].to_numpy() > 0
    idx_eval = np.flatnonzero((fold == FOLD_EVAL) & punya)

    x = load_signals(df, processed=True)
    model = SmallECGNet(n_classes=len(SUPERCLASS))
    model.load_state_dict(torch.load(CKPT, weights_only=True))
    model.eval()

    s_label = skor(model, x, idx_eval)
    y_ev, blok_ev = y[idx_eval], blok[idx_eval]
    s = np.where(y_ev > 0, s_label, -np.inf).max(axis=1)

    pasien, cacah = np.unique(blok_ev, return_counts=True)
    print("== PTB-XL, fold 9 (blok = pasien) ==")
    print(f"  {len(idx_eval):,} rekaman, {len(pasien):,} pasien")
    print(f"  N_k: rerata {cacah.mean():.4f}  maks {cacah.max()}"
          f"  | tunggal {(cacah == 1).sum() / len(cacah) * 100:.1f}%")

    icc = intraclass_correlation(s, blok_ev, n_bootstrap=args.bootstrap,
                                 rng=np.random.default_rng(args.seed))
    print(f"  ICC skor di dalam pasien = {icc.icc:.4f}"
          f"  [{icc.ci_low:.4f}, {icc.ci_high:.4f}]"
          if hasattr(icc, "ci_low") else f"  ICC = {icc.icc:.4f}")

    # Defisit B1 pada split level-PASIEN 50/50, dibandingkan nominal.
    rng = np.random.default_rng(args.seed)
    per = {b: np.flatnonzero(blok_ev == b) for b in pasien}
    k1 = len(pasien) // 2
    dev = {a: [] for a in ALPHAS}
    for _ in range(args.repeats):
        acak = rng.permutation(pasien)
        s_kal = s[np.concatenate([per[b] for b in acak[:k1]])]
        s_uji = s[np.concatenate([per[b] for b in acak[k1:]])]
        for a in ALPHAS:
            t = split_conformal(s_kal, a).threshold
            dev[a].append(float((s_uji <= t).mean()) - (1 - a))

    print(f"\n  {args.repeats} split level-pasien ({k1}/{len(pasien) - k1}):")
    ptbxl = {}
    for a in ALPHAS:
        d = np.asarray(dev[a])
        bs = np.random.default_rng(args.seed + 3)
        boot = bs.choice(d, (3000, len(d))).mean(axis=1)
        ci = np.percentile(boot, [2.5, 97.5])
        print(f"    alpha={a:.2f}  cakupan {1 - a + d.mean():.4f}"
              f"  defisit {-d.mean():+.4f} [{-ci[1]:+.4f},{-ci[0]:+.4f}]")
        ptbxl[f"{a:.2f}"] = {"defisit": float(-d.mean()),
                             "ci": [float(-ci[1]), float(-ci[0])]}

    if not MITDB_JSON.exists():
        print(f"\nGALAT: {MITDB_JSON} tidak ada; jalankan monotonicity_icc_mitdb.py",
              file=sys.stderr)
        return 1
    mit = json.loads(MITDB_JSON.read_text(encoding="utf-8"))

    print("\n== Kurva dosis-respons gabungan pada sumbu DESIGN EFFECT ==")
    print("   DEff = 1 + (H - 1) * rho  dengan H = rerata harmonik ukuran blok (Prop 2')\n")

    h_ptbxl = float(len(cacah) / np.sum(1.0 / cacah))
    deff_ptbxl = 1.0 + (h_ptbxl - 1.0) * icc.icc
    h_mit = float(mit["m_tetap"])
    print(f"  PTB-XL : H = {h_ptbxl:.4f}  rho = {icc.icc:.4f}  ->  DEff = {deff_ptbxl:.3f}")
    print(f"  MIT-BIH: H = {h_mit:,.0f}  rho maks = {max(t['icc'] for t in mit['titik']):.4f}"
          f"  ->  DEff maks = {1 + (h_mit - 1) * max(t['icc'] for t in mit['titik']):,.0f}\n")

    print(f"{'sumber':<20}{'H':>9}{'rho':>9}{'DEff':>11}{'alpha':>7}{'defisit':>11}")
    print("-" * 67)
    baris = []
    for t in mit["titik"]:
        baris.append(("MIT-BIH sintetis", h_mit, t["icc"],
                      1 + (h_mit - 1) * t["icc"], t["alpha"], t["defisit"]))
    for a in ALPHAS:
        baris.append(("PTB-XL (pasien)", h_ptbxl, icc.icc, deff_ptbxl, a,
                      ptbxl[f"{a:.2f}"]["defisit"]))
    baris.sort(key=lambda r: (r[4], r[3]))
    for nm, h, rho, de, a, d in baris:
        print(f"{nm:<20}{h:>9,.2f}{rho:>9.4f}{de:>11,.2f}{a:>7.2f}{d:>+11.4f}")

    print("\n== Spearman pada himpunan GABUNGAN (MIT-BIH + PTB-XL) ==")
    sp = {}
    for a in ALPHAS:
        pts = [(r[3], r[5]) for r in baris if r[4] == a]
        r_s, pv = spearmanr([p[0] for p in pts], [p[1] for p in pts])
        lulus = bool(r_s > 0 and pv < 0.05)
        print(f"  alpha={a:.2f}  n={len(pts)}  rho_S = {r_s:+.4f}  p = {pv:.2e}"
              f"  -> {'LULUS' if lulus else 'GAGAL'}")
        sp[f"{a:.2f}"] = {"spearman": float(r_s), "p": float(pv), "n": len(pts),
                          "lulus": lulus}

    keluaran = ROOT / "results" / "raw" / "dose_response.json"
    keluaran.write_text(json.dumps({
        "ptbxl": {"icc": icc.icc, "H_harmonik": h_ptbxl, "deff": deff_ptbxl,
                  "n_rekaman": int(len(idx_eval)), "n_pasien": int(len(pasien)),
                  "N_k_rerata": float(cacah.mean()), "defisit": ptbxl},
        "mitdb_H": h_mit,
        "mitdb_titik": mit["titik"],
        "spearman_mitdb_icc": mit["spearman"],
        "spearman_gabungan_deff": sp,
    }, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
