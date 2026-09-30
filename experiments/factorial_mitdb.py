"""Faktorial 2x2: apakah defisit cakupan berasal dari KLASTER atau dari KETIMPANGAN N_k?

Uji monotonisitas memunculkan teka-teki. Pada blok penuh (ukuran 1.517-3.249, timpang)
defisit B1 = 0,0221. Pada m=1500 untuk semua rekaman (seimbang) defisit susut jadi
0,0061 -- padahal klasterisasinya praktis sama. Menetapkan m konstan diam-diam sudah
MENYEIMBANGKAN blok, yang justru merupakan hal yang dilakukan HCP.

Dua faktor karena itu dipisahkan secara eksplisit:

    KLASTER      : rekaman asli          vs  penugasan detak diacak (ICC -> 0)
    KETIMPANGAN  : ambil fraksi f tiap blok (ukuran ikut timpang)
                   vs ambil m konstan tiap blok (ukuran seragam)

f dan m dipilih agar n kalibrasi SETARA antar-lengan: m = round(f * rerata N_k).
Tanpa itu, perbedaan n sendiri mengubah konservatisme koreksi 1/(n+1).

Yang dilaporkan: efek utama tiap faktor, interaksinya, dan CI bootstrap.
Backbone diambil dari checkpoint uji H0b -- tidak ada pelatihan ulang.
"""

from __future__ import annotations

import argparse
import itertools
import json
import pathlib
import sys

import numpy as np
import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.conformal import intraclass_correlation, split_conformal  # noqa: E402
from src.data.mitdb import DS2, KELAS, load_beats  # noqa: E402
from src.models.small_ecg_net import SmallECGNet  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

ALPHAS = [0.10, 0.15, 0.20]
FRAKSI = 0.60  # m = 0,60 * rerata N_k harus <= N_k terkecil agar lengan seimbang mungkin
CKPT = ROOT / "results" / "raw" / "feasibility_mitdb_backbone.pt"


@torch.no_grad()
def prob(model, x, idx, batch=512) -> np.ndarray:
    keluar = []
    for m in range(0, len(idx), batch):
        xb = torch.from_numpy(x[idx[m : m + batch]]).unsqueeze(1)
        keluar.append(torch.softmax(model(xb), dim=1).numpy())
    return np.concatenate(keluar)


def lengan(s, blok, blok_unik, k1, seimbang, m_tetap, repeats, seed):
    """Satu sel faktorial. Kembalikan (cakupan per alpha, rerata n kalibrasi)."""
    rng = np.random.default_rng(seed)
    per_blok = {b: np.flatnonzero(blok == b) for b in blok_unik}
    hasil = {a: [] for a in ALPHAS}
    n_kal = []
    for _ in range(repeats):
        acak = rng.permutation(blok_unik)
        kal, uji = acak[:k1], acak[k1:]
        ambil = []
        for b in kal:
            idx = per_blok[b]
            ukuran = m_tetap if seimbang else int(round(FRAKSI * len(idx)))
            ukuran = min(ukuran, len(idx))
            ambil.append(rng.choice(idx, ukuran, replace=False))
        s_kal = s[np.concatenate(ambil)]
        s_uji = s[np.concatenate([per_blok[b] for b in uji])]
        n_kal.append(len(s_kal))
        for a in ALPHAS:
            t = split_conformal(s_kal, a).threshold
            hasil[a].append(float((s_uji <= t).mean()))
    return {a: np.asarray(v) for a, v in hasil.items()}, float(np.mean(n_kal))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repeats", type=int, default=400)
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
    s = (1.0 - pr)[np.arange(len(y_ev)), y_ev]

    k1 = len(ds2) // 2
    ukuran = np.array([int((rec_ev == b).sum()) for b in ds2])
    m_tetap = int(round(FRAKSI * ukuran.mean()))
    rng0 = np.random.default_rng(args.seed)
    rec_perm = rec_ev[rng0.permutation(len(rec_ev))]

    print(f"DS2: {len(y_ev):,} detak, {len(ds2)} rekaman, split {k1}/{len(ds2) - k1}")
    print(f"ukuran rekaman: min {ukuran.min():,}  rerata {ukuran.mean():.0f}"
          f"  maks {ukuran.max():,}")
    print(f"fraksi f = {FRAKSI}  ->  m tetap = {m_tetap:,}"
          f"  (harus <= {ukuran.min():,}: {'OK' if m_tetap <= ukuran.min() else 'GAGAL'})")
    print(f"ICC asli {intraclass_correlation(s, rec_ev).icc:.4f}"
          f"  | ICC permutasi {intraclass_correlation(s, rec_perm).icc:.4f}\n")

    sel = {}
    for klaster, seimbang in itertools.product([True, False], [True, False]):
        blok = rec_ev if klaster else rec_perm
        cak, n = lengan(s, blok, ds2, k1, seimbang, m_tetap, args.repeats, args.seed)
        sel[(klaster, seimbang)] = {"cak": cak, "n": n}

    nama = {(True, True): "berklaster + seimbang", (True, False): "berklaster + TIMPANG",
            (False, True): "acak + seimbang", (False, False): "acak + TIMPANG"}

    print(f"{'alpha':>6}  {'sel':<24}{'n kal':>8}{'cakupan':>10}{'deviasi':>10}")
    print("-" * 60)
    ring = {}
    for a in ALPHAS:
        d = {}
        for k, v in sel.items():
            cov = v["cak"][a]
            dev = cov.mean() - (1 - a)
            d[k] = cov - (1 - a)  # deviasi per ulangan
            print(f"{a:>6.2f}  {nama[k]:<24}{v['n']:>8,.0f}{cov.mean():>10.4f}{dev:>+10.4f}")

        def kontras(w):
            v = sum(w[k] * d[k] for k in d)
            bs = np.random.default_rng(args.seed + 5)
            boot = np.stack([bs.choice(d[k], (3000, len(d[k]))).mean(axis=1) * w[k]
                             for k in d]).sum(axis=0)
            return float(v.mean()), np.percentile(boot, [2.5, 97.5])

        ef_klaster, ci_k = kontras({(True, True): .5, (True, False): .5,
                                    (False, True): -.5, (False, False): -.5})
        ef_timpang, ci_t = kontras({(True, False): .5, (False, False): .5,
                                    (True, True): -.5, (False, True): -.5})
        inter, ci_i = kontras({(True, False): 1.0, (True, True): -1.0,
                               (False, False): -1.0, (False, True): 1.0})

        print(f"{'':>6}  efek KLASTER    = {ef_klaster:+.4f} [{ci_k[0]:+.4f},{ci_k[1]:+.4f}]")
        print(f"{'':>6}  efek KETIMPANGAN= {ef_timpang:+.4f} [{ci_t[0]:+.4f},{ci_t[1]:+.4f}]")
        print(f"{'':>6}  interaksi       = {inter:+.4f} [{ci_i[0]:+.4f},{ci_i[1]:+.4f}]")
        print()
        ring[f"{a:.2f}"] = {
            "sel": {nama[k]: float(sel[k]["cak"][a].mean()) for k in sel},
            "efek_klaster": {"nilai": ef_klaster, "ci": [float(ci_k[0]), float(ci_k[1])]},
            "efek_ketimpangan": {"nilai": ef_timpang, "ci": [float(ci_t[0]), float(ci_t[1])]},
            "interaksi": {"nilai": inter, "ci": [float(ci_i[0]), float(ci_i[1])]},
        }

    print("== Putusan ==")
    for nm, kunci in (("KLASTER", "efek_klaster"), ("KETIMPANGAN", "efek_ketimpangan"),
                      ("INTERAKSI", "interaksi")):
        sig = sum(1 for a in ALPHAS
                  if not (ring[f"{a:.2f}"][kunci]["ci"][0] <= 0 <= ring[f"{a:.2f}"][kunci]["ci"][1]))
        bsr = [abs(ring[f"{a:.2f}"][kunci]["nilai"]) for a in ALPHAS]
        print(f"  {nm:<12} signifikan {sig}/{len(ALPHAS)} alpha"
              f"  | besar {min(bsr):.4f}-{max(bsr):.4f}")

    keluaran = ROOT / "results" / "raw" / "factorial_mitdb.json"
    keluaran.write_text(json.dumps(
        {"fraksi": FRAKSI, "m_tetap": m_tetap, "k1": k1, "repeats": args.repeats,
         "hasil": ring}, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
