"""Kontrol permutasi: apakah selisih B12-B1 berasal dari DEPENDENSI atau dari MEKANIKA?

Kriteria (b) uji H0b ("B12 mencakup lebih baik daripada B1") dicurigai tautologis.
Pada K1 blok, atom +inf berbobot 1/(K1+1). Massa berhingga = K1/(K1+1). Maka untuk
mencapai kuantil (1-alpha), HCP harus menembus persentil

    (1 - alpha) / (K1 / (K1+1))

dari distribusi skor berbobot-blok. Pada K1=11, alpha=0,10 itu berarti persentil
ke-98,2 -- bukan ke-90. Inflasi tersebut MEKANIS: ia muncul dari koreksi blok-hingga
dan sama sekali tidak memerlukan adanya dependensi.

Kontrolnya: permutasikan penugasan detak -> rekaman. Ini mempertahankan K1 dan
seluruh multiset {N_k} secara persis, dan mempertahankan distribusi skor marginal,
tetapi MENGHANCURKAN dependensi intra-rekaman.

    Selisih BERTAHAN di lengan permutasi  -> mekanis; kriteria (b) tak bernilai
    Selisih HILANG di lengan permutasi    -> berasal dari dependensi; (b) sah

Backbone diambil dari checkpoint uji H0b -- tidak ada pelatihan ulang di sini.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.conformal import hcp, intraclass_correlation, split_conformal  # noqa: E402
from src.data.mitdb import DS2, KELAS, load_beats  # noqa: E402
from src.models.small_ecg_net import SmallECGNet  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

ALPHAS = [0.10, 0.15, 0.20]  # hanya yang LAYAK pada K1 = 11
CKPT = ROOT / "results" / "raw" / "feasibility_mitdb_backbone.pt"


@torch.no_grad()
def prob(model, x, idx, batch=512) -> np.ndarray:
    keluar = []
    for m in range(0, len(idx), batch):
        xb = torch.from_numpy(x[idx[m : m + batch]]).unsqueeze(1)
        keluar.append(torch.softmax(model(xb), dim=1).numpy())
    return np.concatenate(keluar)


def jalankan_lengan(s_benar, s_label, blok, ds2, k1, repeats, rng):
    """R split level-blok. Kembalikan dict alpha -> array cakupan/selisih."""
    out = {f"{a:.2f}": {"B1": [], "B12": [], "d": [], "sz12": []} for a in ALPHAS}
    for _ in range(repeats):
        acak = rng.permutation(ds2)
        m_kal = np.isin(blok, acak[:k1])
        m_uji = ~m_kal
        for a in ALPHAS:
            kk = f"{a:.2f}"
            b1 = split_conformal(s_benar[m_kal], a)
            b12 = hcp(s_benar[m_kal], blok[m_kal], a)
            c1 = float((s_benar[m_uji] <= b1.threshold).mean())
            c12 = float((s_benar[m_uji] <= b12.threshold).mean())
            out[kk]["B1"].append(c1)
            out[kk]["B12"].append(c12)
            out[kk]["d"].append(c12 - c1)
            out[kk]["sz12"].append(float((s_label[m_uji] <= b12.threshold).sum(axis=1).mean()))
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repeats", type=int, default=200)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    if not CKPT.exists():
        print(f"GALAT: checkpoint tidak ada: {CKPT}", file=sys.stderr)
        print("Jalankan experiments/feasibility_mitdb.py lebih dulu.", file=sys.stderr)
        return 1

    x, y, rec = load_beats()
    ds2 = np.array([int(r) for r in DS2])
    i_eval = np.flatnonzero(np.isin(rec, ds2))

    model = SmallECGNet(n_leads=1, n_classes=len(KELAS))
    model.load_state_dict(torch.load(CKPT, weights_only=True))
    model.eval()

    pr = prob(model, x, i_eval)
    y_ev, rec_ev = y[i_eval], rec[i_eval]
    s_label = 1.0 - pr
    s_benar = s_label[np.arange(len(y_ev)), y_ev]

    k1 = len(ds2) // 2
    amin = 1.0 / (k1 + 1)
    print(f"DS2: {len(y_ev):,} detak, {len(ds2)} rekaman, split {k1}/{len(ds2) - k1}")
    print(f"K1 = {k1}  ->  alpha_min = {amin:.4f}")
    print("\nPersentil efektif yang WAJIB ditembus HCP (murni mekanis, tanpa dependensi):")
    for a in ALPHAS:
        eff = (1 - a) / (k1 / (k1 + 1))
        print(f"  alpha={a:.2f}  nominal 1-alpha={1 - a:.3f}  ->  persentil {min(eff, 1.0):.4f}")

    rng = np.random.default_rng(args.seed)
    rec_perm = rec_ev[rng.permutation(len(rec_ev))]  # K1 dan {N_k} persis sama

    icc_asli = intraclass_correlation(s_benar, rec_ev)
    icc_perm = intraclass_correlation(s_benar, rec_perm)
    print("\nICC skor di dalam blok:")
    print(f"  rekaman asli : {icc_asli.icc:.4f}")
    print(f"  permutasi    : {icc_perm.icc:.4f}   (harus ~0 bila kontrolnya bekerja)")

    print(f"\n== {args.repeats} split, dua lengan ==")
    a_asli = jalankan_lengan(s_benar, s_label, rec_ev, ds2, k1, args.repeats,
                             np.random.default_rng(args.seed))
    a_perm = jalankan_lengan(s_benar, s_label, rec_perm, ds2, k1, args.repeats,
                             np.random.default_rng(args.seed))

    print(f"\n{'alpha':>6}{'lengan':>12}{'B1':>9}{'B12':>9}"
          f"{'selisih d (CI95)':>26}{'|C|B12':>8}")
    print("-" * 70)
    ringkas = {}
    for a in ALPHAS:
        kk = f"{a:.2f}"
        baris = {}
        for nama, arm in (("asli", a_asli), ("permutasi", a_perm)):
            d = np.array(arm[kk]["d"])
            ci = np.percentile(d, [2.5, 97.5])
            b1m = float(np.mean(arm[kk]["B1"]))
            b12m = float(np.mean(arm[kk]["B12"]))
            print(f"{a:>6.2f}{nama:>12}{b1m:>9.4f}{b12m:>9.4f}"
                  f"{f'{d.mean():+.4f} [{ci[0]:+.4f},{ci[1]:+.4f}]':>26}"
                  f"{float(np.mean(arm[kk]['sz12'])):>8.2f}")
            baris[nama] = {"B1": b1m, "B12": b12m, "d": float(d.mean()),
                           "d_ci": [float(ci[0]), float(ci[1])]}

        # Uji H0 yang sebenarnya: defisit B1 terhadap null tersuai (lengan permutasi).
        b1_a = np.array(a_asli[kk]["B1"])
        b1_p = np.array(a_perm[kk]["B1"])
        bs = np.random.default_rng(args.seed + 7)
        boot_b1 = (bs.choice(b1_p, (4000, len(b1_p))).mean(axis=1)
                   - bs.choice(b1_a, (4000, len(b1_a))).mean(axis=1))
        ci_b1 = np.percentile(boot_b1, [2.5, 97.5])
        defisit = b1_p.mean() - b1_a.mean()
        tanda = "SIGNIFIKAN" if ci_b1[0] > 0 else "tidak signifikan"
        print(f"{'':>6}{'-> defisit B1 (perm - asli)':>12}  = {defisit:+.4f} "
              f"[{ci_b1[0]:+.4f},{ci_b1[1]:+.4f}]   {tanda}")
        baris["defisit_B1"] = {"nilai": float(defisit),
                               "ci": [float(ci_b1[0]), float(ci_b1[1])],
                               "signifikan": bool(ci_b1[0] > 0)}

        # selisih-dari-selisih: berapa banyak d yang TERSISA setelah dependensi dibuang?
        d_a = np.array(a_asli[kk]["d"])
        d_p = np.array(a_perm[kk]["d"])
        dd = d_a.mean() - d_p.mean()
        frac = d_p.mean() / d_a.mean() if abs(d_a.mean()) > 1e-12 else float("nan")
        boot = np.random.default_rng(args.seed).choice(d_a, (2000, len(d_a))).mean(axis=1) - \
            np.random.default_rng(args.seed + 1).choice(d_p, (2000, len(d_p))).mean(axis=1)
        ci_dd = np.percentile(boot, [2.5, 97.5])
        print(f"{'':>6}{'-> d_asli - d_perm':>12}  = {dd:+.4f} "
              f"[{ci_dd[0]:+.4f},{ci_dd[1]:+.4f}]   "
              f"porsi MEKANIS = {frac:.1%}")
        baris["dd"] = {"nilai": float(dd), "ci": [float(ci_dd[0]), float(ci_dd[1])],
                       "porsi_mekanis": float(frac)}
        ringkas[kk] = baris

    print("\n== Putusan ==")
    sig = [ringkas[f"{a:.2f}"]["defisit_B1"]["signifikan"] for a in ALPHAS]
    print(f"  H0(a) vs null tersuai: defisit B1 signifikan pada {sum(sig)}/{len(ALPHAS)} alpha")
    mekanis = [ringkas[f"{a:.2f}"]["dd"]["ci"][0] <= 0 <= ringkas[f"{a:.2f}"]["dd"]["ci"][1]
               for a in ALPHAS]
    porsi = [ringkas[f"{a:.2f}"]["dd"]["porsi_mekanis"] for a in ALPHAS]
    print(f"  CI(d_asli - d_perm) memuat nol pada {sum(mekanis)}/{len(ALPHAS)} alpha")
    print(f"  porsi selisih B12-B1 yang bertahan tanpa dependensi: "
          f"{min(porsi):.1%} - {max(porsi):.1%}")
    print("  -> Kriteria (b) sebagian besar MEKANIS; bukti H0 terletak pada defisit B1.")

    keluaran = ROOT / "results" / "raw" / "control_permutation_mitdb.json"
    keluaran.write_text(json.dumps(
        {"k1": k1, "alpha_min": amin, "icc_asli": icc_asli.icc, "icc_perm": icc_perm.icc,
         "repeats": args.repeats, "hasil": ringkas}, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
