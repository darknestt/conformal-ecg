"""Ringkas hasil invariansi lintas backbone menjadi tabel naskah dan vonis.

Membaca results/raw/backbone_invariance/{dataset}_{backbone}.json, lalu memeriksa:
  1. kontrol negatif -- K1(l) harus identik di semua backbone (dari metadata);
  2. invariansi temuan -- apakah arah defisit B1 dan perbaikan B12 sama lintas backbone.

Aman dijalankan kapan saja; konfigurasi yang belum selesai dilaporkan sebagai menunggu.
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIR = ROOT / "results" / "raw" / "backbone_invariance"
BACKBONE = ["small", "resnet1d34", "resnet1d50"]
DATASET = ["mitdb", "ptbxl"]

for _aliran in (sys.stdout, sys.stderr):
    if hasattr(_aliran, "reconfigure"):
        _aliran.reconfigure(encoding="utf-8", errors="replace")


def muat(dataset: str) -> dict[str, dict]:
    hasil = {}
    for b in BACKBONE:
        p = DIR / f"{dataset}_{b}.json"
        if p.exists():
            hasil[b] = json.loads(p.read_text(encoding="utf-8"))
    return hasil


def ringkas_dataset(dataset: str, hasil: dict[str, dict]) -> dict:
    print(f"\n{'=' * 78}\n  {dataset.upper()}  —  {len(hasil)}/{len(BACKBONE)} backbone selesai\n{'=' * 78}")
    if not hasil:
        return {"dataset": dataset, "selesai": 0}

    print(f"\n{'backbone':<12}{'parameter':>12}  diskriminasi")
    for b, r in hasil.items():
        metrik = "  ".join(f"{k}={v:.4f}" for k, v in r["diskriminasi"].items())
        print(f"{b:<12}{r['parameter']:>12,}  {metrik}")

    k1 = {b: r["k1_per_label"] for b, r in hasil.items()}
    k1_identik = len({json.dumps(v, sort_keys=True) for v in k1.values()}) == 1
    status_k1 = "LOLOS" if k1_identik else "GAGAL -- ADA BUG"
    if len(hasil) < 2:
        status_k1 = "BELUM DAPAT DINILAI (1 backbone)"
    print(f"\nKontrol negatif K1(l) identik lintas backbone: {status_k1}")
    print("  " + "  ".join(f"{k}={v}" for k, v in next(iter(k1.values())).items()))

    alphas = list(next(iter(hasil.values()))["konformal"])
    print(f"\n{'alpha':>6} {'backbone':<12}{'B1':>8}{'B12':>8}{'defisit B1':>12}"
          f"{'B12-B1 CI95':>22}{'|C| B1':>8}{'|C| B12':>9}")
    vonis_alpha = {}
    for a in alphas:
        tanda_defisit, perbaiki = set(), set()
        for b, r in hasil.items():
            k = r["konformal"][a]
            lo, hi = k["selisih_ci"]
            print(f"{a:>6} {b:<12}{k['B1_mean']:>8.4f}{k['B12_mean']:>8.4f}"
                  f"{k['defisit_B1_pp']:>+11.2f}p{f'[{lo:+.4f},{hi:+.4f}]':>22}"
                  f"{k['ukuran_B1']:>8.3f}{k['ukuran_B12']:>9.3f}")
            tanda_defisit.add(k["B1_kurang_cakup"])
            perbaiki.add(k["B12_memperbaiki"])
        vonis_alpha[a] = {
            "B1_kurang_cakup_konsisten": len(tanda_defisit) == 1,
            "B12_memperbaiki_konsisten": len(perbaiki) == 1,
            "B1_kurang_cakup": sorted(tanda_defisit),
            "B12_memperbaiki": sorted(perbaiki),
        }
        print()

    konsisten = sum(v["B12_memperbaiki_konsisten"] for v in vonis_alpha.values())
    if len(hasil) < 2:
        print("Invariansi BELUM DAPAT DINILAI: butuh minimal 2 backbone (konsistensi dengan diri sendiri hampa)")
    else:
        print(f"Temuan B12-memperbaiki konsisten lintas {len(hasil)} backbone pada {konsisten}/{len(alphas)} tingkat alpha")
    return {
        "dataset": dataset,
        "selesai": len(hasil),
        "backbone": list(hasil),
        "k1_identik": k1_identik if len(hasil) >= 2 else None,
        "per_alpha": vonis_alpha,
        "alpha_konsisten": konsisten if len(hasil) >= 2 else None,
        "alpha_total": len(alphas),
    }


def sensitivitas(dataset: str, utama: dict[str, dict]) -> list[dict]:
    """Kriteria S-1..S-3 pra-registrasi (protocol.md §12): bobot terakhir vs terbaik-validasi."""
    keluar = []
    for b in ("resnet1d34", "resnet1d50"):
        p = DIR / f"{dataset}_{b}_terakhir.json"
        if b not in utama or not p.exists():
            continue
        alt, ref = json.loads(p.read_text(encoding="utf-8")), utama[b]
        s1 = {a: alt["konformal"][a]["B12_memperbaiki"] == ref["konformal"][a]["B12_memperbaiki"]
              for a in ref["konformal"]}
        s2 = {a: (alt["konformal"][a]["defisit_B1_pp"] < 0) == (ref["konformal"][a]["defisit_B1_pp"] < 0)
              for a in ref["konformal"]}
        s3 = alt["k1_per_label"] == ref["k1_per_label"]
        lolos = all(s1.values()) and all(s2.values()) and s3
        print(f"\n  Sensitivitas {dataset}/{b}: epoch terakhir {alt['pelatihan']['epoch_dipakai']}"
              f" vs terbaik-validasi {alt['pelatihan']['epoch_terbaik_validasi']}"
              f"  ->  {'LOLOS' if lolos else 'GAGAL'}")
        print(f"    S-1 arah perbaikan HCP sama : {sum(s1.values())}/{len(s1)}")
        print(f"    S-2 tanda defisit B1 sama   : {sum(s2.values())}/{len(s2)}")
        print(f"    S-3 K1 identik              : {'ya' if s3 else 'TIDAK -- BUG'}")
        for a in ref["konformal"]:
            r, s = ref["konformal"][a], alt["konformal"][a]
            print(f"    alpha {a}: defisit B1 {r['defisit_B1_pp']:+.2f} -> {s['defisit_B1_pp']:+.2f} pp"
                  f" | |C| B12 {r['ukuran_B12']:.3f} -> {s['ukuran_B12']:.3f}")
        keluar.append({"backbone": b, "S1": s1, "S2": s2, "S3": s3, "lolos": lolos,
                       "epoch_terakhir": alt["pelatihan"]["epoch_dipakai"],
                       "epoch_terbaik": alt["pelatihan"]["epoch_terbaik_validasi"]})
    return keluar


def main() -> int:
    ringkasan = []
    for d in DATASET:
        utama = muat(d)
        r = ringkas_dataset(d, utama)
        r["sensitivitas_checkpoint"] = sensitivitas(d, utama)
        ringkasan.append(r)
    total = sum(r["selesai"] for r in ringkasan)
    print(f"\n{'=' * 78}\n  {total}/{len(DATASET) * len(BACKBONE)} konfigurasi selesai\n{'=' * 78}")
    (DIR / "summary.json").write_text(json.dumps(ringkasan, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
