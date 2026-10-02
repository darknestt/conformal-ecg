"""Jackknife level rekaman untuk defisit B1 terhadap null permutasi (MIT-BIH DS2).

Analisis sensitivitas post hoc, dispesifikasikan di protocol.md §12 sebelum dijalankan.
CI pada Tabel 5.4 hanya mengukur galat Monte Carlo atas pembagian 22 rekaman yang
tetap; di sini unit inferensinya adalah rekaman: setiap replikasi menghapus satu
rekaman, menarik permutasi baru, dan mengulang R split berpasangan.

Keluaran sekunder (P1-B): cakupan berbobot blok di samping berbobot observasi.

    python experiments/jackknife_records_mitdb.py --backbone small
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

import numpy as np
import torch
from scipy import stats

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.control_permutation_mitdb import ALPHAS, BACKBONE, prob  # noqa: E402
from src.conformal import hcp, split_conformal  # noqa: E402
from src.data.mitdb import DS2, load_beats  # noqa: E402

R = 500
KELUAR = ROOT / "results" / "raw" / "jackknife_records"


def berbobot_blok(tercakup: np.ndarray, blok: np.ndarray) -> float:
    _, inv = np.unique(blok, return_inverse=True)
    return float((np.bincount(inv, weights=tercakup) / np.bincount(inv)).mean())


def jalankan(s, blok_asli, blok_perm, rekaman, rng, sekunder=False):
    """R split berpasangan; cakupan B1 kedua lengan (dan B12 bila sekunder)."""
    k1 = len(rekaman) // 2
    out = {a: {k: [] for k in ("asli", "perm", "asli_blk", "perm_blk", "b12", "b12_blk")} for a in ALPHAS}
    for _ in range(R):
        kal = rng.permutation(rekaman)[:k1]
        for lengan, blok in (("asli", blok_asli), ("perm", blok_perm)):
            m_kal = np.isin(blok, kal)
            m_uji = ~m_kal
            for a in ALPHAS:
                c = s[m_uji] <= split_conformal(s[m_kal], a).threshold
                out[a][lengan].append(float(c.mean()))
                if sekunder:
                    out[a][f"{lengan}_blk"].append(berbobot_blok(c, blok[m_uji]))
                    if lengan == "asli":
                        c12 = s[m_uji] <= hcp(s[m_kal], blok[m_kal], a).threshold
                        out[a]["b12"].append(float(c12.mean()))
                        out[a]["b12_blk"].append(berbobot_blok(c12, blok[m_uji]))
    return {a: {k: np.array(v) for k, v in d.items()} for a, d in out.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backbone", choices=list(BACKBONE), default="small")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    bangun, ckpt, _ = BACKBONE[args.backbone]
    mulai = time.perf_counter()

    x, y, rec = load_beats()
    rekaman = np.array([int(r) for r in DS2])
    i_eval = np.flatnonzero(np.isin(rec, rekaman))
    model = bangun()
    model.load_state_dict(torch.load(ckpt, weights_only=True))
    model.eval()
    y_ev, rec_ev = y[i_eval], rec[i_eval]
    s = (1.0 - prob(model, x, i_eval))[np.arange(len(y_ev)), y_ev]
    print(f"{args.backbone}: {len(s):,} detak, {len(rekaman)} rekaman, R={R}")

    rng = np.random.default_rng([args.seed, 0])
    penuh = jalankan(s, rec_ev, rec_ev[rng.permutation(len(rec_ev))], rekaman, rng, sekunder=True)

    replikasi = {a: [] for a in ALPHAS}
    for j, r in enumerate(rekaman, start=1):
        simpan = rec_ev != r
        s_r, b_r = s[simpan], rec_ev[simpan]
        rng = np.random.default_rng([args.seed, j])
        h = jalankan(s_r, b_r, b_r[rng.permutation(len(b_r))], rekaman[rekaman != r], rng)
        for a in ALPHAS:
            replikasi[a].append(float(np.mean(h[a]["perm"] - h[a]["asli"])))
        print(f"  replikasi {j:>2}/{len(rekaman)} (tanpa {r})", flush=True)

    n = len(rekaman)
    t_kritis = float(stats.t.ppf(0.975, n - 1))
    hasil = {}
    for a in ALPHAS:
        selisih = penuh[a]["perm"] - penuh[a]["asli"]
        theta = float(selisih.mean())
        mc_se = float(selisih.std(ddof=1) / np.sqrt(R))
        th = np.array(replikasi[a])
        se_jack = float(np.sqrt((n - 1) / n * np.sum((th - th.mean()) ** 2)))
        t = theta / se_jack
        hasil[f"{a:.2f}"] = {
            "theta": theta, "mc_se": mc_se, "se_jack": se_jack,
            "ci": [theta - t_kritis * se_jack, theta + t_kritis * se_jack],
            "t": float(t), "p_satu_arah": float(stats.t.sf(t, n - 1)),
            "mc_cukup": bool(mc_se < 0.1 * se_jack),
            "theta_replikasi": replikasi[a],
            "sekunder": {
                "B1_obs_asli": float(penuh[a]["asli"].mean()), "B1_blk_asli": float(penuh[a]["asli_blk"].mean()),
                "B1_obs_perm": float(penuh[a]["perm"].mean()), "B1_blk_perm": float(penuh[a]["perm_blk"].mean()),
                "B12_obs_asli": float(penuh[a]["b12"].mean()), "B12_blk_asli": float(penuh[a]["b12_blk"].mean()),
                "theta_blk": float((penuh[a]["perm_blk"] - penuh[a]["asli_blk"]).mean()),
            },
        }

    # Holm atas 3 level alpha per backbone, sesuai spesifikasi.
    urut = sorted(hasil, key=lambda k: hasil[k]["p_satu_arah"])
    maks = 0.0
    for i, k in enumerate(urut):
        maks = max(maks, min(1.0, (len(urut) - i) * hasil[k]["p_satu_arah"]))
        hasil[k]["p_holm"] = maks
        hasil[k]["signifikan_holm"] = bool(maks < 0.05)

    for k, v in hasil.items():
        sk = v["sekunder"]
        print(f"alpha={k}  theta={v['theta'] * 100:+.2f} pp  jackknife 95% CI "
              f"[{v['ci'][0] * 100:+.2f}, {v['ci'][1] * 100:+.2f}]  p_Holm={v['p_holm']:.4f}  "
              f"MC cukup={v['mc_cukup']}  | blok: theta={sk['theta_blk'] * 100:+.2f} pp, "
              f"B12 obs/blk={sk['B12_obs_asli']:.4f}/{sk['B12_blk_asli']:.4f}")

    KELUAR.mkdir(parents=True, exist_ok=True)
    berkas = KELUAR / f"mitdb_{args.backbone}.json"
    berkas.write_text(json.dumps({
        "backbone": args.backbone, "checkpoint": ckpt.name, "R": R, "seed": args.seed,
        "n_rekaman": n, "k1_penuh": n // 2, "k1_replikasi": (n - 1) // 2,
        "status": "post hoc sensitivity analysis (protocol.md §12)",
        "detik": round(time.perf_counter() - mulai, 1), "hasil": hasil}, indent=2), encoding="utf-8")
    print(f"Tersimpan: {berkas.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
