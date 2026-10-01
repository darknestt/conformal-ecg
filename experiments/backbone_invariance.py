"""Invariansi temuan konformal lintas kapasitas backbone.

Serangan paling wajar terhadap paper audit: "temuan kalibrasi Anda mungkin artefak
model yang lemah". Skrip ini menjawabnya dengan menjalankan protokol yang SAMA
PERSIS dengan experiments/feasibility.py (PTB-XL) dan feasibility_mitdb.py (MIT-BIH)
pada tiga backbone dengan rentang kapasitas >100x, lalu mencatat apakah temuannya
bertahan.

Dua pemeriksaan bawaan:
  1. backbone `small` TIDAK dilatih ulang -- checkpoint lama dimuat, sehingga
     metrik diskriminasinya harus terulang persis (bukti pipeline identik);
  2. K1(l) dihitung dari metadata dan TIDAK boleh bergantung backbone
     (kontrol negatif: bila berubah antar-backbone, ada bug).

FOLD 10 PTB-XL TIDAK PERNAH DISENTUH.

Pemakaian:
    python experiments/backbone_invariance.py --dataset mitdb --backbone resnet1d34
    python experiments/backbone_invariance.py --dataset ptbxl --backbone small --smoke
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
from src.models.resnet1d import resnet1d34, resnet1d50  # noqa: E402
from src.models.small_ecg_net import SmallECGNet  # noqa: E402
from src.train import latih  # noqa: E402

for _aliran in (sys.stdout, sys.stderr):
    if hasattr(_aliran, "reconfigure"):
        _aliran.reconfigure(encoding="utf-8", errors="replace")

RAW = ROOT / "results" / "raw"
BANGUN = {"small": SmallECGNet, "resnet1d34": resnet1d34, "resnet1d50": resnet1d50}
CKPT_LAMA = {
    "ptbxl": RAW / "feasibility_backbone.pt",
    "mitdb": RAW / "feasibility_mitdb_backbone.pt",
}

# Protokol asli, disalin apa adanya agar perbandingan sah.
PROTOKOL = {
    "ptbxl": {"alphas": [0.01, 0.05, 0.10], "epochs": 25, "batch": 128, "mikro": 32},
    "mitdb": {"alphas": [0.01, 0.05, 0.10, 0.15, 0.20], "epochs": 30, "batch": 256, "mikro": 64},
}
PTBXL_FOLD_LATIH, PTBXL_FOLD_VAL, PTBXL_FOLD_EVAL = [1, 2, 3, 4, 5, 6], 7, 9
MITDB_VAL_REC = ["124", "205", "215", "230"]


def siapkan_ptbxl() -> dict:
    from src.data.ptbxl import SUPERCLASS, load_metadata, load_signals

    df = load_metadata()
    fold = df["strat_fold"].to_numpy()
    punya = df["n_superclass"].to_numpy() > 0
    x = load_signals(df, processed=True)
    return {
        "x": x,
        "y": df[SUPERCLASS].to_numpy(dtype=np.float32),
        "blok": df["patient_id"].to_numpy(),
        "idx_latih": np.flatnonzero(np.isin(fold, PTBXL_FOLD_LATIH)),
        "idx_val": np.flatnonzero(fold == PTBXL_FOLD_VAL),
        "idx_eval": np.flatnonzero((fold == PTBXL_FOLD_EVAL) & punya),
        "ambil_x": lambda i: torch.from_numpy(np.ascontiguousarray(x[i])).permute(0, 2, 1),
        "n_leads": 12,
        "kelas": list(SUPERCLASS),
        "rugi_fn": nn.BCEWithLogitsLoss(),
        "n_fold10_tak_disentuh": int((fold == 10).sum()),
    }


def siapkan_mitdb() -> dict:
    from src.data.mitdb import DS1, DS2, KELAS, load_beats

    x, y, rec = load_beats()
    ds1 = np.array([int(r) for r in DS1])
    ds2 = np.array([int(r) for r in DS2])
    val = np.array([int(r) for r in MITDB_VAL_REC])
    return {
        "x": x,
        "y": y,
        "blok": rec,
        "idx_latih": np.flatnonzero(np.isin(rec, np.setdiff1d(ds1, val))),
        "idx_val": np.flatnonzero(np.isin(rec, val)),
        "idx_eval": np.flatnonzero(np.isin(rec, ds2)),
        "ambil_x": lambda i: torch.from_numpy(x[i]).unsqueeze(1),
        "n_leads": 1,
        "kelas": list(KELAS),
        "rugi_fn": nn.CrossEntropyLoss(),
        "ds2": ds2,
    }


@torch.no_grad()
def skor_label(model: nn.Module, d: dict, dataset: str, batch: int = 256) -> np.ndarray:
    """Skor nonconformity per label: 1 - probabilitas."""
    keluar = []
    for m in range(0, len(d["idx_eval"]), batch):
        logit = model(d["ambil_x"](d["idx_eval"][m : m + batch]))
        prob = torch.sigmoid(logit) if dataset == "ptbxl" else torch.softmax(logit, dim=1)
        keluar.append(1.0 - prob.numpy())
    return np.concatenate(keluar)


def diskriminasi(s_label: np.ndarray, y_ev: np.ndarray, dataset: str) -> dict:
    from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score

    if dataset == "ptbxl":
        return {"macro_auroc": float(roc_auc_score(y_ev, 1 - s_label, average="macro"))}
    pred = s_label.argmin(axis=1)
    return {
        "akurasi": float((pred == y_ev).mean()),
        "balanced_acc": float(balanced_accuracy_score(y_ev, pred)),
        "macro_f1": float(f1_score(y_ev, pred, average="macro", zero_division=0)),
    }


def k1_per_label(y_ev: np.ndarray, blok_ev: np.ndarray, kelas: list[str], dataset: str) -> dict:
    """Jumlah blok yang memuat tiap label. Bergantung metadata saja, bukan model."""
    hasil = {}
    for j, k in enumerate(kelas):
        punya = y_ev[:, j] > 0 if dataset == "ptbxl" else y_ev == j
        hasil[k] = int(len(np.unique(blok_ev[punya])))
    return hasil


def audit_konformal(
    s_label: np.ndarray, y_ev: np.ndarray, blok_ev: np.ndarray, d: dict,
    dataset: str, alphas: list[float], repeats: int, seed: int,
) -> dict:
    """R split acak level-blok; cakupan, ukuran himpunan, dan selisih B12-B1."""
    if dataset == "ptbxl":
        s_target = np.where(y_ev > 0, s_label, -np.inf).max(axis=1)
        unit = np.unique(blok_ev)
        k_kal = len(unit) // 2
    else:
        s_target = s_label[np.arange(len(y_ev)), y_ev]
        unit = d["ds2"]
        k_kal = len(unit) // 2

    rng = np.random.default_rng(seed)
    kumpul = {f"{a:.2f}": {n: [] for n in ("B1", "B12", "d", "sz1", "sz12", "inf12")} for a in alphas}
    for _ in range(repeats):
        m_kal = np.isin(blok_ev, rng.permutation(unit)[:k_kal])
        m_uji = ~m_kal
        if m_kal.sum() < 50 or m_uji.sum() < 50:
            continue
        for a in alphas:
            k = kumpul[f"{a:.2f}"]
            b1 = split_conformal(s_target[m_kal], a)
            b12 = hcp(s_target[m_kal], blok_ev[m_kal], a)
            c1 = float((s_target[m_uji] <= b1.threshold).mean())
            c12 = float((s_target[m_uji] <= b12.threshold).mean())
            k["B1"].append(c1)
            k["B12"].append(c12)
            k["d"].append(c12 - c1)
            k["sz1"].append(float((s_label[m_uji] <= b1.threshold).sum(axis=1).mean()))
            k["sz12"].append(float((s_label[m_uji] <= b12.threshold).sum(axis=1).mean()))
            k["inf12"].append(bool(b12.is_trivial))

    ringkas = {}
    for a in alphas:
        k = kumpul[f"{a:.2f}"]
        c1, c12, dd = (np.array(k[n]) for n in ("B1", "B12", "d"))
        ci1, ci12, cid = (np.percentile(v, [2.5, 97.5]).tolist() for v in (c1, c12, dd))
        ringkas[f"{a:.2f}"] = {
            "target": 1 - a,
            "B1_mean": float(c1.mean()), "B1_ci": ci1,
            "B12_mean": float(c12.mean()), "B12_ci": ci12,
            "defisit_B1_pp": float((c1.mean() - (1 - a)) * 100),
            "selisih_mean": float(dd.mean()), "selisih_ci": cid,
            "B1_kurang_cakup": bool(ci1[1] < 1 - a),
            "B12_memperbaiki": bool(cid[0] > 0),
            "ukuran_B1": float(np.mean(k["sz1"])),
            "ukuran_B12": float(np.mean(k["sz12"])),
            "frac_B12_trivial": float(np.mean(k["inf12"])),
            "n_split": len(c1),
        }
    return ringkas


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", choices=["ptbxl", "mitdb"], required=True)
    p.add_argument("--backbone", choices=list(BANGUN), required=True)
    p.add_argument("--repeats", type=int, default=200)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--smoke", action="store_true", help="3 batch, 1 epoch, 5 split; keluaran terpisah")
    args = p.parse_args()

    prot = PROTOKOL[args.dataset]
    sub = "smoke" if args.smoke else "backbone_invariance"
    dir_hasil, dir_ckpt = RAW / sub, RAW / sub / "ckpt"
    dir_ckpt.mkdir(parents=True, exist_ok=True)
    nama = f"{args.dataset}_{args.backbone}"
    repeats = 5 if args.smoke else args.repeats

    t_mulai = time.perf_counter()
    torch.manual_seed(args.seed)
    print(f"== {nama}{'  [SMOKE]' if args.smoke else ''} ==")
    d = siapkan_ptbxl() if args.dataset == "ptbxl" else siapkan_mitdb()
    print(f"  latih {len(d['idx_latih']):,} | val {len(d['idx_val']):,} | evaluasi {len(d['idx_eval']):,}")
    if args.dataset == "ptbxl":
        print(f"  FOLD 10 TIDAK DISENTUH ({d['n_fold10_tak_disentuh']:,} rekaman)")

    model = BANGUN[args.backbone](n_leads=d["n_leads"], n_classes=len(d["kelas"]))
    print(f"  parameter: {model.n_params():,}")
    info_latih: dict = {}

    if args.backbone == "small":
        model.load_state_dict(torch.load(CKPT_LAMA[args.dataset], weights_only=True))
        model.eval()
        info_latih = {"sumber": f"checkpoint lama {CKPT_LAMA[args.dataset].name} (tidak dilatih ulang)"}
        print(f"  {info_latih['sumber']}")
    else:
        final = dir_ckpt / f"{nama}.pt"
        if final.exists():
            model.load_state_dict(torch.load(final, weights_only=True))
            model.eval()
            info_latih = {"sumber": f"checkpoint {final.name}"}
            print(f"  memuat {final.name}")
        else:
            torch.manual_seed(args.seed)
            model, info_latih = latih(
                model, d["ambil_x"], d["y"], d["idx_latih"], d["idx_val"],
                rugi_fn=d["rugi_fn"],
                epochs=1 if args.smoke else prot["epochs"],
                batch=prot["batch"], mikro=prot["mikro"], seed=args.seed,
                titik_simpan=dir_ckpt / f"{nama}.resume.pt",
                maks_batch=3 if args.smoke else None,
                log=lambda s: print(s, flush=True),
            )
            torch.save(model.state_dict(), final)

    print("\n== Skor dan audit konformal ==")
    s_label = skor_label(model, d, args.dataset)
    y_ev, blok_ev = d["y"][d["idx_eval"]], d["blok"][d["idx_eval"]]
    metrik = diskriminasi(s_label, y_ev, args.dataset)
    print("  " + "  ".join(f"{k}={v:.4f}" for k, v in metrik.items()))

    k1 = k1_per_label(y_ev, blok_ev, d["kelas"], args.dataset)
    print("  K1(l): " + "  ".join(f"{k}={v}" for k, v in k1.items()))

    ringkas = audit_konformal(s_label, y_ev, blok_ev, d, args.dataset, prot["alphas"], repeats, args.seed)
    print(f"\n{'alpha':>6}{'B1':>9}{'B12':>9}{'defisit B1':>12}{'B12-B1 CI95':>24}{'|C|B1':>8}{'|C|B12':>8}")
    for a, r in ringkas.items():
        lo, hi = r["selisih_ci"]
        print(f"{a:>6}{r['B1_mean']:>9.4f}{r['B12_mean']:>9.4f}{r['defisit_B1_pp']:>+11.2f}p"
              f"{f'[{lo:+.4f},{hi:+.4f}]':>24}{r['ukuran_B1']:>8.3f}{r['ukuran_B12']:>8.3f}")

    keluar = dir_hasil / f"{nama}.json"
    keluar.write_text(json.dumps({
        "dataset": args.dataset, "backbone": args.backbone, "smoke": args.smoke,
        "parameter": model.n_params(), "protokol": prot, "repeats": repeats, "seed": args.seed,
        "pelatihan": info_latih, "diskriminasi": metrik, "k1_per_label": k1,
        "konformal": ringkas, "detik_total": time.perf_counter() - t_mulai,
    }, indent=2), encoding="utf-8")
    print(f"\nDitulis: {keluar.relative_to(ROOT)}  ({time.perf_counter() - t_mulai:.0f} d)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
