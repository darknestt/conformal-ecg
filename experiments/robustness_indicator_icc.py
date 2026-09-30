"""Ketegaran hasil dosis-respons terhadap pilihan estimator ICC.

Prop. 2 dinyatakan untuk ICC dari INDIKATOR 1{s <= t}, bukan ICC skor mentah.
Kurva dosis-respons pertama memakai skor mentah -- lebih mudah dihitung, tetapi
BUKAN besaran yang diminta teori. Selisih keduanya adalah persis celah yang akan
ditanyakan reviewer statistik, dan celah itu ditutup di sini, bukan dibela.

Skrip ini menghitung ulang seluruh kurva dengan rho = ICC indikator pada ambang
tetap t = kuantil (1-alpha) dari seluruh skor evaluasi. Ambang dibuat tetap agar
tidak bergantung pada split, sehingga rho menjadi sifat data, bukan sifat
satu pembagian tertentu.

Bila putusannya berubah, hasil utama bersandar pada aproksimasi dan harus
dinyatakan demikian. Bila tidak berubah, Asumsi (A) berhenti menjadi ancaman
karena ramalannya bertahan pada besaran yang benar.
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
from src.conformal import icc_at_threshold, split_conformal  # noqa: E402
from src.data.mitdb import DS2, KELAS, load_beats  # noqa: E402
from src.data.ptbxl import SUPERCLASS, load_metadata, load_signals  # noqa: E402
from src.models.small_ecg_net import SmallECGNet  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

ALPHAS = [0.10, 0.15, 0.20]
P_GRID = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
FRAKSI = 0.60
CKPT_MIT = ROOT / "results" / "raw" / "feasibility_mitdb_backbone.pt"
CKPT_PTB = ROOT / "results" / "raw" / "feasibility_backbone.pt"


@torch.no_grad()
def prob_mit(model, x, idx, batch=512) -> np.ndarray:
    out = []
    for m in range(0, len(idx), batch):
        xb = torch.from_numpy(x[idx[m : m + batch]]).unsqueeze(1)
        out.append(torch.softmax(model(xb), dim=1).numpy())
    return np.concatenate(out)


def lemahkan(blok, p, rng):
    if p <= 0:
        return blok.copy()
    out = blok.copy()
    pilih = rng.choice(len(blok), int(round(p * len(blok))), replace=False)
    out[pilih] = out[rng.permutation(pilih)]
    return out


def defisit(s, blok, blok_unik, k1, m_tetap, repeats, seed):
    rng = np.random.default_rng(seed)
    per = {b: np.flatnonzero(blok == b) for b in blok_unik}
    out = {a: [] for a in ALPHAS}
    for _ in range(repeats):
        acak = rng.permutation(blok_unik)
        kal, uji = acak[:k1], acak[k1:]
        ambil = [rng.choice(per[b], min(m_tetap, len(per[b])), replace=False) for b in kal]
        s_kal = s[np.concatenate(ambil)]
        s_uji = s[np.concatenate([per[b] for b in uji])]
        for a in ALPHAS:
            t = split_conformal(s_kal, a).threshold
            out[a].append((1 - a) - float((s_uji <= t).mean()))
    return {a: float(np.mean(v)) for a, v in out.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    for c in (CKPT_MIT, CKPT_PTB):
        if not c.exists():
            print(f"GALAT: checkpoint tidak ada: {c}", file=sys.stderr)
            return 1

    # ---- MIT-BIH ----
    x, y, rec = load_beats()
    ds2 = np.array([int(r) for r in DS2])
    i_ev = np.flatnonzero(np.isin(rec, ds2))
    mm = SmallECGNet(n_leads=1, n_classes=len(KELAS))
    mm.load_state_dict(torch.load(CKPT_MIT, weights_only=True))
    mm.eval()
    pr = prob_mit(mm, x, i_ev)
    y_ev, rec_ev = y[i_ev], rec[i_ev]
    s_mit = (1.0 - pr)[np.arange(len(y_ev)), y_ev]

    k1 = len(ds2) // 2
    ukuran = np.array([int((rec_ev == b).sum()) for b in ds2])
    m_tetap = int(round(FRAKSI * ukuran.mean()))
    H_mit = float(len(ukuran) / np.sum(1.0 / np.minimum(ukuran, m_tetap)))

    # ---- PTB-XL ----
    df = load_metadata()
    yp = df[SUPERCLASS].to_numpy(dtype=np.float32)
    blokp = df["patient_id"].to_numpy()
    fold = df["strat_fold"].to_numpy()
    punya = df["n_superclass"].to_numpy() > 0
    idx_p = np.flatnonzero((fold == FOLD_EVAL) & punya)
    xp = load_signals(df, processed=True)
    mp = SmallECGNet(n_classes=len(SUPERCLASS))
    mp.load_state_dict(torch.load(CKPT_PTB, weights_only=True))
    mp.eval()
    sl = skor(mp, xp, idx_p)
    y_p, blok_p = yp[idx_p], blokp[idx_p]
    s_ptb = np.where(y_p > 0, sl, -np.inf).max(axis=1)
    pas, cacah = np.unique(blok_p, return_counts=True)
    H_ptb = float(len(cacah) / np.sum(1.0 / cacah))
    k1_ptb = len(pas) // 2

    print("Ambang TETAP t = kuantil (1-alpha) dari seluruh skor evaluasi")
    print(f"MIT-BIH: H = {H_mit:,.2f} (dibatasi m={m_tetap:,})   "
          f"PTB-XL: H = {H_ptb:.4f}\n")

    print(f"{'sumber':<20}{'alpha':>7}{'rho_skor':>11}{'rho_indik':>11}"
          f"{'DEff_ind':>11}{'defisit':>11}")
    print("-" * 71)

    titik = {a: [] for a in ALPHAS}
    rinci = []
    for p in P_GRID:
        blok_p_mit = lemahkan(rec_ev, p, np.random.default_rng(args.seed + 100))
        d = defisit(s_mit, blok_p_mit, ds2, k1, m_tetap, args.repeats, args.seed)
        for a in ALPHAS:
            t = float(np.quantile(s_mit, 1 - a))
            rho_i = icc_at_threshold(s_mit, blok_p_mit, t).icc
            deff = 1.0 + (H_mit - 1.0) * rho_i
            titik[a].append((deff, d[a]))
            rinci.append({"sumber": "MIT-BIH", "p": p, "alpha": a, "t": t,
                          "rho_indikator": rho_i, "deff_indikator": deff,
                          "defisit": d[a]})
            print(f"{'MIT-BIH p=' + f'{p:.1f}':<20}{a:>7.2f}"
                  f"{'-':>11}{rho_i:>11.4f}{deff:>11.2f}{d[a]:>+11.4f}")

    d_ptb = defisit(s_ptb, blok_p, pas, k1_ptb, 10**9, args.repeats, args.seed)
    for a in ALPHAS:
        t = float(np.quantile(s_ptb, 1 - a))
        rho_i = icc_at_threshold(s_ptb, blok_p, t).icc
        deff = 1.0 + (H_ptb - 1.0) * rho_i
        titik[a].append((deff, d_ptb[a]))
        rinci.append({"sumber": "PTB-XL", "p": None, "alpha": a, "t": t,
                      "rho_indikator": rho_i, "deff_indikator": deff,
                      "defisit": d_ptb[a]})
        print(f"{'PTB-XL (pasien)':<20}{a:>7.2f}{'-':>11}{rho_i:>11.4f}"
              f"{deff:>11.2f}{d_ptb[a]:>+11.4f}")

    print("\n== Spearman(DEff indikator, defisit) pada himpunan gabungan ==")
    ring = {}
    for a in ALPHAS:
        xs = [t[0] for t in titik[a]]
        ys = [t[1] for t in titik[a]]
        r, pv = spearmanr(xs, ys)
        lulus = bool(r > 0 and pv < 0.05)
        print(f"  alpha={a:.2f}  n={len(xs)}  rho_S = {r:+.4f}  p = {pv:.2e}"
              f"  -> {'LULUS' if lulus else 'GAGAL'}")
        ring[f"{a:.2f}"] = {"spearman": float(r), "p": float(pv), "n": len(xs),
                            "lulus": lulus}

    n = sum(v["lulus"] for v in ring.values())
    print(f"\nPutusan ketegaran: {n}/{len(ALPHAS)} alpha tetap LULUS dengan ICC indikator")
    if n == len(ALPHAS):
        print("  -> Hasil utama TIDAK bersandar pada aproksimasi skor mentah.")
        print("     Asumsi (A) berhenti menjadi ancaman: ramalannya bertahan pada")
        print("     besaran yang memang diminta Prop. 2.")
    else:
        print("  -> Hasil BERUBAH. Kurva utama harus dilaporkan memakai ICC indikator,")
        print("     dan selisihnya dinyatakan terbuka di naskah.")

    keluaran = ROOT / "results" / "raw" / "robustness_indicator_icc.json"
    keluaran.write_text(json.dumps(
        {"H_mitdb": H_mit, "H_ptbxl": H_ptb, "m_tetap": m_tetap,
         "repeats": args.repeats, "spearman": ring, "titik": rinci},
        indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
