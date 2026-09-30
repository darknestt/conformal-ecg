"""H0b di MIT-BIH -- ujung spektrum dependensi yang berlawanan dari PTB-XL.

Protokol par. 11 butir 1 menuntut uji ini SEBELUM C4 dicabut.

    PTB-XL  : K1 = 1.942 blok, N_k = 1,12   -> rasio bobot 1,12x   -> H0 TERREFUTASI
    MIT-BIH : K1 =    11 blok, N_k = 2.260  -> rasio bobot 1.929x  -> ?

Dua hal diuji sekaligus:

  H0b  Apakah split conformal naif kurang-cakup, dan apakah HCP memperbaikinya?
       Yang membuktikan mekanismenya adalah SELISIH B12 - B1, bukan B1 saja.

  H1   Pada K1 = 11, alpha_min = 1/12 = 0,0833. Maka alpha = 0,01 dan 0,05
       WAJIB menghasilkan ambang +inf. Ini prediksi DETERMINISTIK: bila
       gagal, implementasinya yang salah (protokol par. 11), bukan temuan.

Split: DS1 latih (18 rekaman) + validasi (4 rekaman), DS2 dibagi 11/11
pada level REKAMAN, R kali. Rekaman berpacu dikecualikan.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

import numpy as np
import torch
from torch import nn

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.conformal import hcp, split_conformal  # noqa: E402
from src.data.mitdb import DS1, DS2, KELAS, load_beats  # noqa: E402
from src.models.small_ecg_net import SmallECGNet  # noqa: E402

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")

ALPHAS = [0.01, 0.05, 0.10, 0.15, 0.20]
VAL_REC = ["124", "205", "215", "230"]  # 4 dari DS1, dipisah di level rekaman
CKPT = ROOT / "results" / "raw" / "feasibility_mitdb_backbone.pt"


def latih(x, y, i_latih, i_val, epochs, batch, seed) -> nn.Module:
    torch.manual_seed(seed)
    model = SmallECGNet(n_leads=1, n_classes=len(KELAS))
    print(f"  parameter: {model.n_params():,}")

    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    rugi_fn = nn.CrossEntropyLoss()
    rng = np.random.default_rng(seed)
    xv = torch.from_numpy(x[i_val]).unsqueeze(1)
    yv = torch.from_numpy(y[i_val])

    terbaik, bobot, sabar = float("inf"), None, 0
    for ep in range(1, epochs + 1):
        t0 = time.perf_counter()
        model.train()
        urut = rng.permutation(len(i_latih))
        total = 0.0
        for m in range(0, len(urut), batch):
            amb = i_latih[urut[m : m + batch]]
            opt.zero_grad()
            rugi = rugi_fn(model(torch.from_numpy(x[amb]).unsqueeze(1)), torch.from_numpy(y[amb]))
            rugi.backward()
            opt.step()
            total += rugi.detach().item() * len(amb)

        model.eval()
        with torch.no_grad():
            rv = float(rugi_fn(model(xv), yv))
        print(f"  epoch {ep:>2}  latih={total / len(urut):.4f}  val={rv:.4f}"
              f"  ({time.perf_counter() - t0:.0f} d)", flush=True)

        if rv < terbaik - 1e-4:
            terbaik, sabar, bobot = rv, 0, {k: v.clone() for k, v in model.state_dict().items()}
        else:
            sabar += 1
            if sabar >= 5:
                print(f"  early stopping di epoch {ep}")
                break

    if bobot is not None:
        model.load_state_dict(bobot)
    model.eval()
    return model


@torch.no_grad()
def prob(model, x, idx, batch=512) -> np.ndarray:
    keluar = []
    for m in range(0, len(idx), batch):
        xb = torch.from_numpy(x[idx[m : m + batch]]).unsqueeze(1)
        keluar.append(torch.softmax(model(xb), dim=1).numpy())
    return np.concatenate(keluar)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--batch", type=int, default=256)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--repeats", type=int, default=200)
    args = p.parse_args()

    torch.manual_seed(args.seed)
    print("== Memuat detak (cache dibangun bila belum ada) ==")
    x, y, rec = load_beats()
    print(f"  {len(y):,} detak, {len(np.unique(rec))} rekaman, jendela {x.shape[1]} sampel")

    ds1 = np.array([int(r) for r in DS1])
    ds2 = np.array([int(r) for r in DS2])
    val = np.array([int(r) for r in VAL_REC])
    latih_rec = np.setdiff1d(ds1, val)

    i_latih = np.flatnonzero(np.isin(rec, latih_rec))
    i_val = np.flatnonzero(np.isin(rec, val))
    i_eval = np.flatnonzero(np.isin(rec, ds2))

    print(f"  latih {len(i_latih):,} detak / {len(latih_rec)} rekaman"
          f" | val {len(i_val):,} / {len(val)}"
          f" | evaluasi {len(i_eval):,} / {len(ds2)} rekaman")
    for k, n in zip(KELAS, np.bincount(y[i_latih], minlength=5), strict=True):
        print(f"    latih {k}: {n:>6,}")

    if CKPT.exists():
        print("\n== Memuat backbone tersimpan ==")
        model = SmallECGNet(n_leads=1, n_classes=len(KELAS))
        model.load_state_dict(torch.load(CKPT, weights_only=True))
        model.eval()
    else:
        print("\n== Melatih backbone ==")
        model = latih(x, y, i_latih, i_val, args.epochs, args.batch, args.seed)
        torch.save(model.state_dict(), CKPT)

    print("\n== Skor pada DS2 ==")
    pr = prob(model, x, i_eval)
    y_ev, rec_ev = y[i_eval], rec[i_eval]
    s_label = 1.0 - pr  # skor per kelas
    s_benar = s_label[np.arange(len(y_ev)), y_ev]

    from sklearn.metrics import balanced_accuracy_score, f1_score

    pred = pr.argmax(axis=1)
    print(f"  akurasi        : {(pred == y_ev).mean():.4f}")
    print(f"  balanced acc   : {balanced_accuracy_score(y_ev, pred):.4f}")
    print(f"  macro-F1       : {f1_score(y_ev, pred, average='macro', zero_division=0):.4f}")

    # C8 pada dataset kedua: berapa blok kalibrasi yang memuat tiap kelas?
    print("\n  Kelayakan per-kelas (C8) di DS2 -- K1(l) = rekaman yang memuat kelas l:")
    for j, k in enumerate(KELAS):
        rr = np.unique(rec_ev[y_ev == j])
        amin = 1 / (len(rr) + 1) if len(rr) else float("inf")
        print(f"    {k}: {int((y_ev == j).sum()):>6,} detak di {len(rr):>2} rekaman"
              f"  -> alpha_min = {amin:.4f}")

    k1 = len(ds2) // 2
    amin = 1 / (k1 + 1)
    print(f"\n== {args.repeats} split acak level-REKAMAN pada DS2 ({k1}/{len(ds2) - k1}) ==")
    print(f"  K1 = {k1}  ->  alpha_min = {amin:.4f}."
          f"  alpha < itu WAJIB memberi ambang +inf (H1).")

    rng = np.random.default_rng(args.seed)
    hasil = {f"{a:.2f}": {"B1": [], "B12": [], "d": [], "rasio": [], "inf12": [], "sz1": [], "sz12": []}
             for a in ALPHAS}

    for _ in range(args.repeats):
        acak = rng.permutation(ds2)
        m_kal = np.isin(rec_ev, acak[:k1])
        m_uji = ~m_kal
        for a in ALPHAS:
            kk = f"{a:.2f}"
            b1 = split_conformal(s_benar[m_kal], a)
            b12 = hcp(s_benar[m_kal], rec_ev[m_kal], a)
            hasil[kk]["B1"].append(float((s_benar[m_uji] <= b1.threshold).mean()))
            hasil[kk]["B12"].append(float((s_benar[m_uji] <= b12.threshold).mean()))
            hasil[kk]["d"].append(hasil[kk]["B12"][-1] - hasil[kk]["B1"][-1])
            hasil[kk]["rasio"].append((b1.n_points + 1) / (b12.n_blocks + 1))
            hasil[kk]["inf12"].append(bool(b12.is_trivial))
            hasil[kk]["sz1"].append(float((s_label[m_uji] <= b1.threshold).sum(axis=1).mean()))
            hasil[kk]["sz12"].append(float((s_label[m_uji] <= b12.threshold).sum(axis=1).mean()))

    print(f"\n{'alpha':>6}{'target':>8}{'B1 naif (CI95)':>24}{'B12 HCP (CI95)':>24}"
          f"{'selisih B12-B1 (CI95)':>27}{'|C|B1':>7}{'|C|B12':>8}{'B12 inf':>9}")
    print("-" * 113)
    ringkas = {}
    for a in ALPHAS:
        kk = f"{a:.2f}"
        h = hasil[kk]
        c1, c12, d = (np.array(h[n]) for n in ("B1", "B12", "d"))
        ci1, ci12, cid = (np.percentile(v, [2.5, 97.5]) for v in (c1, c12, d))
        frac_inf = float(np.mean(h["inf12"]))
        print(
            f"{a:>6.2f}{1 - a:>8.2f}"
            f"{f'{c1.mean():.4f} [{ci1[0]:.4f},{ci1[1]:.4f}]':>24}"
            f"{f'{c12.mean():.4f} [{ci12[0]:.4f},{ci12[1]:.4f}]':>24}"
            f"{f'{d.mean():+.4f} [{cid[0]:+.4f},{cid[1]:+.4f}]':>27}"
            f"{np.mean(h['sz1']):>7.2f}{np.mean(h['sz12']):>8.2f}{frac_inf * 100:>8.0f}%"
        )
        ringkas[kk] = {
            "B1_mean": float(c1.mean()), "B1_ci": ci1.tolist(),
            "B12_mean": float(c12.mean()), "B12_ci": ci12.tolist(),
            "selisih_mean": float(d.mean()), "selisih_ci": cid.tolist(),
            "B1_kurang_cakup": bool(ci1[1] < 1 - a),
            "B12_memperbaiki": bool(cid[0] > 0),
            "B12_trivial_frac": frac_inf,
            "layak": bool(a >= amin),
            "ukuran_B1": float(np.mean(h["sz1"])), "ukuran_B12": float(np.mean(h["sz12"])),
            "rasio_bobot": float(np.mean(h["rasio"])),
        }

    print("\n== H1 (deterministik): alpha < alpha_min WAJIB memberi ambang +inf ==")
    h1_ok = True
    for a in ALPHAS:
        r = ringkas[f"{a:.2f}"]
        harus = not r["layak"]
        nyata = r["B12_trivial_frac"] == 1.0
        ok = harus == nyata
        h1_ok &= ok
        print(f"  alpha={a:.2f}  layak={r['layak']}  trivial={r['B12_trivial_frac'] * 100:.0f}%"
              f"  -> {'OK' if ok else '!! GAGAL -- IMPLEMENTASI SALAH !!'}")

    layak = [a for a in ALPHAS if ringkas[f"{a:.2f}"]["layak"]]
    n_a = sum(ringkas[f"{a:.2f}"]["B1_kurang_cakup"] for a in layak)
    n_b = sum(ringkas[f"{a:.2f}"]["B12_memperbaiki"] for a in layak)
    print(f"\n== H0b (hanya pada {len(layak)} alpha yang LAYAK: {layak}) ==")
    print(f"  (a) B1 kurang-cakup          : {n_a}/{len(layak)}")
    print(f"  (b) B12 memperbaiki (CI d>0) : {n_b}/{len(layak)}   <- mekanismenya")

    if not h1_ok:
        putusan = "H1 GAGAL -- DEBUG IMPLEMENTASI SEBELUM MENAFSIRKAN APA PUN"
    elif n_b >= max(1, len(layak) - 1):
        putusan = "H0b TERKONFIRMASI -- kerangka valid; PTB-XL sekadar dependensi lemah"
    elif n_a >= max(1, len(layak) - 1):
        putusan = "H0b (a) saja; mekanisme tidak terdukung"
    else:
        putusan = "H0b TIDAK TERKONFIRMASI"
    print(f"\nPutusan: {putusan}")

    keluaran = ROOT / "results" / "raw" / "feasibility_mitdb.json"
    keluaran.write_text(
        json.dumps(
            {
                "desain": {"latih": latih_rec.tolist(), "validasi": val.tolist(),
                           "evaluasi": ds2.tolist(), "split": f"{k1}/{len(ds2) - k1} level-rekaman",
                           "pengulangan": args.repeats, "alpha_min": amin},
                "akurasi": float((pred == y_ev).mean()),
                "balanced_accuracy": float(balanced_accuracy_score(y_ev, pred)),
                "macro_f1": float(f1_score(y_ev, pred, average="macro", zero_division=0)),
                "hasil": ringkas, "h1_lolos": bool(h1_ok),
                "h0b_a": n_a, "h0b_b": n_b, "alpha_layak": layak, "putusan": putusan,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Tersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
