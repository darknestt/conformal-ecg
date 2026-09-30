"""H0b dengan tuas yang BENAR: monotonisitas defisit cakupan terhadap ICC.

Uji monotonisitas sebelumnya memvariasikan UKURAN BLOK dan gagal (1/3 alpha,
pola kurva-U terbalik). Faktorial 2x2 menjelaskan kenapa: ukuran blok bukan
penggeraknya. Efek ketimpangan tidak signifikan (0/3); efek klaster signifikan
(3/3) dan 4-5x lebih besar.

Karena itu tuasnya diganti menjadi ICC secara langsung. Sebagian p dari detak
ditukar label rekamannya secara acak, sehingga dependensi melemah bertahap:

    p = 0   -> rekaman utuh, ICC maksimal
    p = 1   -> penugasan acak penuh, ICC -> 0

Ukuran blok dijaga SERAGAM (m tetap per blok) agar faktor ketimpangan tersingkir
sepenuhnya dan yang tersisa hanya dependensi.

Yang diuji: Spearman(ICC(p), defisit(p)) > 0 dengan p < 0,05 -- yaitu H0b
sebagaimana dimaksud protokol par. 56-62, bukan versi ukuran-bloknya.
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

from src.conformal import intraclass_correlation, split_conformal  # noqa: E402
from src.data.mitdb import DS2, KELAS, load_beats  # noqa: E402
from src.models.small_ecg_net import SmallECGNet  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

ALPHAS = [0.10, 0.15, 0.20]
P_GRID = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
FRAKSI = 0.60
CKPT = ROOT / "results" / "raw" / "feasibility_mitdb_backbone.pt"


@torch.no_grad()
def prob(model, x, idx, batch=512) -> np.ndarray:
    keluar = []
    for m in range(0, len(idx), batch):
        xb = torch.from_numpy(x[idx[m : m + batch]]).unsqueeze(1)
        keluar.append(torch.softmax(model(xb), dim=1).numpy())
    return np.concatenate(keluar)


def lemahkan(blok: np.ndarray, p: float, rng) -> np.ndarray:
    """Tukar label rekaman pada fraksi p detak; multiset ukuran blok terjaga."""
    if p <= 0:
        return blok.copy()
    out = blok.copy()
    pilih = rng.choice(len(blok), int(round(p * len(blok))), replace=False)
    out[pilih] = out[rng.permutation(pilih)]
    return out


def cakupan(s, blok, blok_unik, k1, m_tetap, repeats, seed):
    rng = np.random.default_rng(seed)
    per_blok = {b: np.flatnonzero(blok == b) for b in blok_unik}
    hasil = {a: [] for a in ALPHAS}
    for _ in range(repeats):
        acak = rng.permutation(blok_unik)
        kal, uji = acak[:k1], acak[k1:]
        ambil = []
        for b in kal:
            idx = per_blok[b]
            ambil.append(rng.choice(idx, min(m_tetap, len(idx)), replace=False))
        s_kal = s[np.concatenate(ambil)]
        s_uji = s[np.concatenate([per_blok[b] for b in uji])]
        for a in ALPHAS:
            t = split_conformal(s_kal, a).threshold
            hasil[a].append(float((s_uji <= t).mean()))
    return {a: np.asarray(v) for a, v in hasil.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    if not CKPT.exists():
        print(f"GALAT: checkpoint tidak ada: {CKPT}", file=sys.stderr)
        return 1

    x, y, rec = load_beats()
    ds2 = np.array([int(r) for r in DS2])
    i_eval = np.flatnonzero(np.isin(rec, ds2))

    model = SmallECGNet(n_leads=1, n_classes=len(KELAS))
    model.load_state_dict(torch.load(CKPT, weights_only=True))
    model.eval()

    pr = prob(model, x, i_eval)
    y_ev, rec_ev = y[i_eval], rec[i_eval]
    s = (1.0 - pr)[np.arange(len(y_ev)), y_ev]

    k1 = len(ds2) // 2
    ukuran = np.array([int((rec_ev == b).sum()) for b in ds2])
    m_tetap = int(round(FRAKSI * ukuran.mean()))
    print(f"DS2: {len(y_ev):,} detak, {len(ds2)} rekaman, split {k1}/{len(ds2) - k1}")
    print(f"ukuran blok DISERAGAMKAN pada m = {m_tetap:,} (faktor ketimpangan disingkirkan)")
    print(f"{args.repeats} split per titik, {len(P_GRID)} titik p\n")

    print(f"{'p tukar':>8}{'ICC':>9}{'alpha':>7}{'cakupan':>10}{'defisit (CI95)':>26}")
    print("-" * 62)

    titik = {a: {"icc": [], "def": []} for a in ALPHAS}
    rinci = []
    for p in P_GRID:
        rng = np.random.default_rng(args.seed + 100)
        blok_p = lemahkan(rec_ev, p, rng)
        icc = intraclass_correlation(s, blok_p).icc
        cak = cakupan(s, blok_p, ds2, k1, m_tetap, args.repeats, args.seed)
        for j, a in enumerate(ALPHAS):
            dev = cak[a] - (1 - a)
            bs = np.random.default_rng(args.seed + 9)
            boot = bs.choice(dev, (3000, len(dev))).mean(axis=1)
            ci = np.percentile(boot, [2.5, 97.5])
            titik[a]["icc"].append(icc)
            titik[a]["def"].append(float(-dev.mean()))  # defisit = -deviasi
            rinci.append({"p": p, "icc": icc, "alpha": a,
                          "cakupan": float(cak[a].mean()),
                          "defisit": float(-dev.mean()),
                          "ci_deviasi": [float(ci[0]), float(ci[1])]})
            kol = f"{p:>8.1f}{icc:>9.4f}" if j == 0 else " " * 17
            print(f"{kol}{a:>7.2f}{cak[a].mean():>10.4f}"
                  f"{f'{-dev.mean():+.4f} [{-ci[1]:+.4f},{-ci[0]:+.4f}]':>26}")

    print("\n== H0b dengan tuas ICC: Spearman(ICC, defisit) ==")
    ring = {}
    for a in ALPHAS:
        r, pv = spearmanr(titik[a]["icc"], titik[a]["def"])
        lulus = bool(r > 0 and pv < 0.05)
        print(f"  alpha={a:.2f}  rho_S = {r:+.4f}  p = {pv:.2e}"
              f"  -> {'LULUS' if lulus else 'GAGAL'}")
        ring[f"{a:.2f}"] = {"spearman": float(r), "p": float(pv), "lulus": lulus}

    n = sum(v["lulus"] for v in ring.values())
    print(f"\nPutusan: {n}/{len(ALPHAS)} alpha memenuhi kriteria pra-registrasi")
    if n == len(ALPHAS):
        print("  -> H0b TERKONFIRMASI: defisit cakupan naik monoton terhadap ICC.")
    elif n == 0:
        print("  -> H0b TERREFUTASI.")
    else:
        print("  -> Sebagian; laporkan per alpha.")

    keluaran = ROOT / "results" / "raw" / "monotonicity_icc_mitdb.json"
    keluaran.write_text(json.dumps(
        {"m_tetap": m_tetap, "k1": k1, "repeats": args.repeats, "p_grid": P_GRID,
         "spearman": ring, "titik": rinci}, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
