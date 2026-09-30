"""H0b sebagaimana DIPRA-REGISTRASI: monotonisitas deviasi cakupan terhadap design effect.

Protokol par. 56-62 menuntut korelasi Spearman antara design effect dan besar deviasi
cakupan. Dengan dua dataset saja, rho hanya bisa +-1 dan p tak terdefinisi -- cacat
pra-registrasi. Skrip ini memperbaikinya dengan membangkitkan BANYAK titik DEff di
dalam MIT-BIH sendiri.

Tuas: m = jumlah detak yang diambil dari tiap rekaman kalibrasi.

    DEff_blok(m) = 1 + (m - 1) * rho        (rho = ICC skor di dalam rekaman)

    m = 1     -> 11 detak dari 11 pasien berbeda: praktis tak berkorelasi
    m = 1500  -> rekaman nyaris utuh: klaster maksimal

JEBAKAN yang ditangani: n = 11m ikut berubah, dan n kecil membuat koreksi 1/(n+1)
pada split conformal sangat konservatif. Itu sendiri menghasilkan tren monoton PALSU.
Penawarnya: tiap m dibandingkan terhadap null permutasinya SENDIRI, sehingga
konservatisme sampel-hingga muncul identik di kedua lengan dan saling hapus.

    defisit(m) = cakupan_permutasi(m) - cakupan_asli(m)

Yang diuji: Spearman(DEff(m), defisit(m)) > 0 dengan p < 0,05.
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

ALPHAS = [0.10, 0.15, 0.20]  # hanya yang LAYAK pada K1 = 11
M_GRID = [1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1500]
CKPT = ROOT / "results" / "raw" / "feasibility_mitdb_backbone.pt"


@torch.no_grad()
def prob(model, x, idx, batch=512) -> np.ndarray:
    keluar = []
    for m in range(0, len(idx), batch):
        xb = torch.from_numpy(x[idx[m : m + batch]]).unsqueeze(1)
        keluar.append(torch.softmax(model(xb), dim=1).numpy())
    return np.concatenate(keluar)


def cakupan(s_benar, blok, blok_unik, k1, m, repeats, seed):
    """Rerata cakupan B1 saat m detak diambil dari tiap blok kalibrasi."""
    rng = np.random.default_rng(seed)
    per_blok = {b: np.flatnonzero(blok == b) for b in blok_unik}
    hasil = {a: [] for a in ALPHAS}
    for _ in range(repeats):
        acak = rng.permutation(blok_unik)
        kal, uji = acak[:k1], acak[k1:]
        ambil = []
        for b in kal:
            idx = per_blok[b]
            ambil.append(idx if len(idx) <= m else rng.choice(idx, m, replace=False))
        s_kal = s_benar[np.concatenate(ambil)]
        s_uji = s_benar[np.concatenate([per_blok[b] for b in uji])]
        for a in ALPHAS:
            t = split_conformal(s_kal, a).threshold
            hasil[a].append(float((s_uji <= t).mean()))
    return {a: np.asarray(v) for a, v in hasil.items()}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repeats", type=int, default=200)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

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
    s_benar = (1.0 - pr)[np.arange(len(y_ev)), y_ev]

    k1 = len(ds2) // 2
    rho = intraclass_correlation(s_benar, rec_ev).icc
    rng0 = np.random.default_rng(args.seed)
    rec_perm = rec_ev[rng0.permutation(len(rec_ev))]

    ukuran = np.array([int((rec_ev == b).sum()) for b in ds2])
    print(f"DS2: {len(y_ev):,} detak, {len(ds2)} rekaman, split {k1}/{len(ds2) - k1}")
    print(f"ukuran rekaman: min {ukuran.min():,}  median {int(np.median(ukuran)):,}"
          f"  maks {ukuran.max():,}")
    print(f"ICC skor di dalam rekaman: rho = {rho:.4f}")
    print(f"\n{args.repeats} split per titik, {len(M_GRID)} titik m\n")

    print(f"{'m':>6}{'n=11m':>8}{'DEff':>9}"
          f"{'alpha':>7}{'asli':>9}{'permutasi':>11}{'defisit (CI95)':>26}")
    print("-" * 76)

    titik = {a: {"deff": [], "defisit": []} for a in ALPHAS}
    rinci = []
    for m in M_GRID:
        deff = 1.0 + (m - 1) * rho
        c_asli = cakupan(s_benar, rec_ev, ds2, k1, m, args.repeats, args.seed)
        c_perm = cakupan(s_benar, rec_perm, ds2, k1, m, args.repeats, args.seed)
        for j, a in enumerate(ALPHAS):
            d = c_perm[a] - c_asli[a]
            bs = np.random.default_rng(args.seed + 11)
            boot = bs.choice(c_perm[a], (2000, len(d))).mean(axis=1) - \
                bs.choice(c_asli[a], (2000, len(d))).mean(axis=1)
            ci = np.percentile(boot, [2.5, 97.5])
            titik[a]["deff"].append(deff)
            titik[a]["defisit"].append(float(d.mean()))
            rinci.append({"m": m, "alpha": a, "deff": deff,
                          "asli": float(c_asli[a].mean()),
                          "perm": float(c_perm[a].mean()),
                          "defisit": float(d.mean()),
                          "ci": [float(ci[0]), float(ci[1])]})
            kol_m = f"{m:>6}{11 * m:>8}{deff:>9.1f}" if j == 0 else " " * 23
            print(f"{kol_m}{a:>7.2f}{c_asli[a].mean():>9.4f}{c_perm[a].mean():>11.4f}"
                  f"{f'{d.mean():+.4f} [{ci[0]:+.4f},{ci[1]:+.4f}]':>26}")

    print("\n== H0b sebagaimana dipra-registrasi: Spearman(DEff, defisit) ==")
    ring = {}
    for a in ALPHAS:
        r, pv = spearmanr(titik[a]["deff"], titik[a]["defisit"])
        lulus = bool(r > 0 and pv < 0.05)
        print(f"  alpha={a:.2f}  rho_S = {r:+.4f}  p = {pv:.2e}  "
              f"-> {'LULUS' if lulus else 'GAGAL'}")
        ring[f"{a:.2f}"] = {"spearman": float(r), "p": float(pv), "lulus": lulus}

    n_lulus = sum(v["lulus"] for v in ring.values())
    print(f"\nPutusan: {n_lulus}/{len(ALPHAS)} alpha memenuhi kriteria pra-registrasi")
    if n_lulus == len(ALPHAS):
        print("  -> H0b TERKONFIRMASI: deviasi cakupan naik monoton terhadap design effect.")
    elif n_lulus == 0:
        print("  -> H0b TERREFUTASI: tak ada hubungan monoton.")
    else:
        print("  -> Sebagian. Laporkan per alpha, jangan digeneralisasi.")

    keluaran = ROOT / "results" / "raw" / "monotonicity_mitdb.json"
    keluaran.write_text(json.dumps(
        {"rho_icc": rho, "k1": k1, "repeats": args.repeats, "m_grid": M_GRID,
         "spearman": ring, "titik": rinci}, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
