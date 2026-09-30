"""Langkah 4 -- studi kelayakan: menguji H0 secara BENAR.

H0 (docs/protocol.md) punya DUA bagian, dan versi pertama skrip ini hanya
menguji yang pertama:
    (a) split conformal naif kurang-cakup
    (b) penyebabnya dependensi blok -- sehingga koreksi blok MEMPERBAIKINYA

Menguji (a) saja menyesatkan: kurang-cakup dapat berasal dari mana saja.
Yang membuktikan mekanismenya adalah SELISIH cakupan B12 - B1.

Dua konfound pada versi pertama, diperbaiki di sini:

1. PERGESERAN KUALITAS LABEL. Fold 1-8 hanya 64-68% divalidasi manusia;
   fold 9-10 100%. Kalibrasi di fold 8 lalu menguji di fold 9 mencampurkan
   pergeseran kualitas label ke dalam pengukuran cakupan. Diperbaiki dengan
   membagi FOLD 9 SAJA pada level pasien -- kedua sisi 100% tervalidasi.

2. SATU TITIK PENGUKURAN. Diganti R split acak level-pasien, menghasilkan
   sebaran cakupan dan CI untuk SELISIHNYA.

FOLD 10 TIDAK PERNAH DISENTUH.
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
from src.data.ptbxl import SUPERCLASS, load_metadata, load_signals  # noqa: E402
from src.models.small_ecg_net import SmallECGNet  # noqa: E402

for _aliran in (sys.stdout, sys.stderr):
    if hasattr(_aliran, "reconfigure"):
        _aliran.reconfigure(encoding="utf-8", errors="replace")

FOLD_LATIH = [1, 2, 3, 4, 5, 6]
FOLD_VAL = 7
FOLD_EVAL = 9  # dibagi dua di level pasien; kedua sisi 100% tervalidasi
ALPHAS = [0.01, 0.05, 0.10]
CKPT = ROOT / "results" / "raw" / "feasibility_backbone.pt"


def latih(x, y, idx_latih, idx_val, epochs, batch, seed) -> nn.Module:
    torch.manual_seed(seed)
    model = SmallECGNet(n_classes=len(SUPERCLASS))
    print(f"  parameter: {model.n_params():,}")

    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    rugi_fn = nn.BCEWithLogitsLoss()
    rng = np.random.default_rng(seed)
    xv = torch.from_numpy(np.ascontiguousarray(x[idx_val])).permute(0, 2, 1)
    yv = torch.from_numpy(y[idx_val])

    terbaik, bobot, sabar = float("inf"), None, 0
    for ep in range(1, epochs + 1):
        t0 = time.perf_counter()
        model.train()
        urut = rng.permutation(len(idx_latih))
        total = 0.0
        for mulai in range(0, len(urut), batch):
            ambil = np.sort(idx_latih[urut[mulai : mulai + batch]])
            xb = torch.from_numpy(np.ascontiguousarray(x[ambil])).permute(0, 2, 1)
            opt.zero_grad()
            rugi = rugi_fn(model(xb), torch.from_numpy(y[ambil]))
            rugi.backward()
            opt.step()
            total += rugi.detach().item() * len(ambil)

        model.eval()
        with torch.no_grad():
            rv = float(rugi_fn(model(xv), yv))
        print(
            f"  epoch {ep:>2}  latih={total / len(urut):.4f}  val={rv:.4f}"
            f"  ({time.perf_counter() - t0:.0f} d)",
            flush=True,
        )

        if rv < terbaik - 1e-4:
            terbaik, sabar = rv, 0
            bobot = {k: v.clone() for k, v in model.state_dict().items()}
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
def skor(model, x, idx, batch=256) -> np.ndarray:
    keluar = []
    for mulai in range(0, len(idx), batch):
        xb = torch.from_numpy(np.ascontiguousarray(x[idx[mulai : mulai + batch]]))
        keluar.append(1.0 - torch.sigmoid(model(xb.permute(0, 2, 1))).numpy())
    return np.concatenate(keluar)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=25)
    p.add_argument("--batch", type=int, default=128)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--repeats", type=int, default=200)
    args = p.parse_args()

    torch.manual_seed(args.seed)
    df = load_metadata()
    y = df[SUPERCLASS].to_numpy(dtype=np.float32)
    blok = df["patient_id"].to_numpy()
    fold = df["strat_fold"].to_numpy()
    punya = df["n_superclass"].to_numpy() > 0

    x = load_signals(df, processed=True)
    idx_latih = np.flatnonzero(np.isin(fold, FOLD_LATIH))
    idx_val = np.flatnonzero(fold == FOLD_VAL)
    idx_eval = np.flatnonzero((fold == FOLD_EVAL) & punya)

    print(
        f"  latih {len(idx_latih):,} | val {len(idx_val):,} | "
        f"evaluasi fold {FOLD_EVAL}: {len(idx_eval):,} rekaman, "
        f"{len(np.unique(blok[idx_eval])):,} pasien"
    )
    print(
        f"  tervalidasi manusia di fold {FOLD_EVAL}: "
        f"{df.loc[fold == FOLD_EVAL, 'validated_by_human'].mean() * 100:.1f}%"
        "   (fold 8 hanya 67,8% -- itulah sebabnya tidak dipakai)"
    )
    print(f"  FOLD 10 TIDAK DISENTUH ({int((fold == 10).sum()):,} rekaman)")

    if CKPT.exists():
        print("\n== Memuat backbone tersimpan ==")
        model = SmallECGNet(n_classes=len(SUPERCLASS))
        model.load_state_dict(torch.load(CKPT, weights_only=True))
        model.eval()
    else:
        print("\n== Melatih backbone ==")
        model = latih(x, y, idx_latih, idx_val, args.epochs, args.batch, args.seed)
        torch.save(model.state_dict(), CKPT)

    print("\n== Menghitung skor pada fold 9 ==")
    s_label = skor(model, x, idx_eval)
    y_eval, blok_eval = y[idx_eval], blok[idx_eval]
    s_superset = np.where(y_eval > 0, s_label, -np.inf).max(axis=1)

    from sklearn.metrics import roc_auc_score

    auroc = float(roc_auc_score(y_eval, 1 - s_label, average="macro"))
    print(f"  macro-AUROC: {auroc:.4f}")

    pasien, inv = np.unique(blok_eval, return_inverse=True)
    uk = np.bincount(inv)
    print(
        f"\n  Rata-rata N_k = {len(idx_eval) / len(pasien):.4f}; "
        f"{(uk == 1).mean() * 100:.1f}% pasien hanya punya 1 rekaman."
    )
    print("  Rasio bobot atom +inf (n+1)/(K1+1) dilaporkan di kolom terakhir:")
    print("  makin dekat ke 1, makin mustahil HCP berbeda dari split conformal.")

    print(f"\n== {args.repeats} split acak level-PASIEN di dalam fold 9 ==")
    rng = np.random.default_rng(args.seed)
    hasil = {f"{a:.2f}": {"B1": [], "B12": [], "selisih": [], "rasio": []} for a in ALPHAS}

    for _ in range(args.repeats):
        acak = rng.permutation(pasien)
        set_kal = set(acak[: len(acak) // 2].tolist())
        m_kal = np.isin(blok_eval, list(set_kal))
        m_uji = ~m_kal
        if m_kal.sum() < 50 or m_uji.sum() < 50:
            continue

        for a in ALPHAS:
            b1 = split_conformal(s_superset[m_kal], a)
            b12 = hcp(s_superset[m_kal], blok_eval[m_kal], a)
            k = f"{a:.2f}"
            c1 = float((s_superset[m_uji] <= b1.threshold).mean())
            c12 = float((s_superset[m_uji] <= b12.threshold).mean())
            hasil[k]["B1"].append(c1)
            hasil[k]["B12"].append(c12)
            hasil[k]["selisih"].append(c12 - c1)
            hasil[k]["rasio"].append((b1.n_points + 1) / (b12.n_blocks + 1))

    print(
        f"\n{'alpha':>6}{'target':>8}{'B1 naif (CI95)':>24}{'B12 HCP (CI95)':>24}"
        f"{'selisih B12-B1 (CI95)':>28}{'rasio':>8}"
    )
    print("-" * 98)
    ringkas = {}
    for a in ALPHAS:
        k = f"{a:.2f}"
        c1, c12, d = (np.array(hasil[k][n]) for n in ("B1", "B12", "selisih"))
        ci1, ci12, cid = (np.percentile(v, [2.5, 97.5]) for v in (c1, c12, d))
        print(
            f"{a:>6.2f}{1 - a:>8.2f}"
            f"{f'{c1.mean():.4f} [{ci1[0]:.4f},{ci1[1]:.4f}]':>24}"
            f"{f'{c12.mean():.4f} [{ci12[0]:.4f},{ci12[1]:.4f}]':>24}"
            f"{f'{d.mean():+.5f} [{cid[0]:+.5f},{cid[1]:+.5f}]':>28}"
            f"{np.mean(hasil[k]['rasio']):>8.4f}"
        )
        ringkas[k] = {
            "B1_mean": float(c1.mean()),
            "B1_ci": ci1.tolist(),
            "B12_mean": float(c12.mean()),
            "B12_ci": ci12.tolist(),
            "selisih_mean": float(d.mean()),
            "selisih_ci": cid.tolist(),
            "B1_kurang_cakup": bool(ci1[1] < 1 - a),
            "B12_memperbaiki": bool(cid[0] > 0),
            "rasio_bobot": float(np.mean(hasil[k]["rasio"])),
        }

    n_a = sum(v["B1_kurang_cakup"] for v in ringkas.values())
    n_b = sum(v["B12_memperbaiki"] for v in ringkas.values())
    print(f"\nH0 (a) B1 kurang-cakup             : {n_a}/{len(ALPHAS)}")
    print(f"H0 (b) B12 memperbaiki (CI selisih>0): {n_b}/{len(ALPHAS)}   <- INI mekanismenya")

    if n_b >= 2:
        putusan = "H0 TERKONFIRMASI PENUH"
    elif n_a >= 2:
        putusan = "H0 (a) saja; MEKANISME TIDAK TERDUKUNG pada granularitas ini"
    else:
        putusan = "H0 TIDAK TERKONFIRMASI"
    print(f"\nPutusan: {putusan}")

    keluaran = ROOT / "results" / "raw" / "feasibility_study.json"
    keluaran.write_text(
        json.dumps(
            {
                "desain": {
                    "latih": FOLD_LATIH,
                    "validasi": FOLD_VAL,
                    "evaluasi": f"fold {FOLD_EVAL} dibagi level-pasien, {args.repeats}x",
                    "fold_10": "TIDAK DISENTUH",
                    "alasan_tidak_pakai_fold_8": "67,8% tervalidasi manusia vs 100% di fold 9",
                },
                "macro_auroc": auroc,
                "rata_Nk": float(len(idx_eval) / len(pasien)),
                "persen_pasien_satu_rekaman": float((uk == 1).mean() * 100),
                "hasil": ringkas,
                "h0_a_kurang_cakup": n_a,
                "h0_b_mekanisme": n_b,
                "putusan": putusan,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Tersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
