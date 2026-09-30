"""Kelayakan kalibrasi per-label (C8) pada tiga tingkat hierarki PTB-XL.

Teorema 1 HCP bersifat agnostik terhadap skor, sehingga cakupan-superset
    P(Y subset C(X)) >= 1 - alpha
tereduksi persis ke HCP dengan skor skalar s(x,Y) = max_{l in Y} s_l(x).
Yang TIDAK tereduksi adalah jaminan per-label (label-conditional).

Untuk menjamin cakupan label l, blok kalibrasi yang relevan hanyalah blok yang
MEMUAT label l. Jadi batas kelayakan Prop. 1 berlaku per label:

    alpha >= 1 / (K1(l) + 1),    K1(l) = jumlah blok kalibrasi yang memuat l

Skrip ini menghitung K1(l) langsung dari metadata -- tanpa model, tanpa skor.
"""

from __future__ import annotations

import ast
import json
import math
import pathlib
import sys

import pandas as pd

for _aliran in (sys.stdout, sys.stderr):
    if hasattr(_aliran, "reconfigure"):
        _aliran.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "raw" / "ptbxl" / "ptbxl_database.csv"
SCP = ROOT / "data" / "raw" / "ptbxl" / "scp_statements.csv"
BLOK = "patient_id"
CALIB_FOLD = 9
ALPHAS = [0.01, 0.05, 0.10]


def muat() -> tuple[pd.DataFrame, pd.DataFrame]:
    db = pd.read_csv(DB)
    scp = pd.read_csv(SCP, index_col=0)
    return db, scp[scp["diagnostic"] == 1]


def peta_label(db: pd.DataFrame, diag: pd.DataFrame) -> pd.DataFrame:
    """Satu baris per (rekaman, label) untuk ketiga tingkat hierarki."""
    kelas = diag["diagnostic_class"].to_dict()
    subkelas = diag["diagnostic_subclass"].to_dict()

    baris = []
    for rec, pasien, fold, kode_mentah in zip(
        db["ecg_id"], db[BLOK], db["strat_fold"], db["scp_codes"], strict=True
    ):
        for kode in ast.literal_eval(kode_mentah):
            if kode not in kelas:
                continue  # bukan pernyataan diagnostik
            baris.append(
                {
                    "ecg_id": rec,
                    "blok": pasien,
                    "fold": fold,
                    "superclass": kelas[kode],
                    "subclass": subkelas[kode],
                    "scp_code": kode,
                }
            )
    return pd.DataFrame(baris)


def kelayakan(panjang: pd.DataFrame, tingkat: str, m_simultan: int) -> pd.DataFrame:
    kal = panjang[panjang["fold"] == CALIB_FOLD]
    ringkas = (
        kal.groupby(tingkat)
        .agg(blok=("blok", "nunique"), rekaman=("ecg_id", "nunique"))
        .sort_values("blok", ascending=False)
    )
    ringkas["alpha_min"] = 1.0 / (ringkas["blok"] + 1)
    for a in ALPHAS:
        ringkas[f"a={a:.2f}"] = ringkas["alpha_min"] <= a
    # Koreksi Bonferroni: menjamin m label sekaligus menuntut alpha/m per label.
    ringkas["a=0,05 serentak"] = ringkas["alpha_min"] <= 0.05 / m_simultan
    return ringkas


def cetak(judul: str, tabel: pd.DataFrame, m: int) -> None:
    print(f"\n{'=' * 84}\n  {judul}  ({len(tabel)} label, koreksi serentak m={m})\n{'=' * 84}")
    print(
        f"{'label':<12}{'blok K1':>9}{'rekaman':>9}{'alpha_min':>11}"
        + "".join(f"{f'a={a:.2f}':>8}" for a in ALPHAS)
        + f"{'serentak':>10}"
    )
    print("-" * 84)
    for nama, r in tabel.iterrows():
        tanda = "".join(f"{('OK' if r[f'a={a:.2f}'] else 'GAGAL'):>8}" for a in ALPHAS)
        srt = "OK" if r["a=0,05 serentak"] else "GAGAL"
        print(
            f"{str(nama)[:12]:<12}{int(r['blok']):>9,}{int(r['rekaman']):>9,}"
            f"{r['alpha_min']:>11.5f}{tanda}{srt:>10}"
        )


def periksa_monotonisitas(panjang: pd.DataFrame) -> dict:
    """K1 harus naik menuju akar hierarki: K1(subclass) <= K1(superclass)."""
    kal = panjang[panjang["fold"] == CALIB_FOLD]
    k_super = kal.groupby("superclass")["blok"].nunique()
    k_sub = kal.groupby("subclass")["blok"].nunique()
    pasangan = kal[["superclass", "subclass"]].drop_duplicates()

    melanggar = []
    for _, p in pasangan.iterrows():
        if k_sub[p["subclass"]] > k_super[p["superclass"]]:
            melanggar.append(f"{p['subclass']} > {p['superclass']}")

    print(f"\nMonotonisitas hierarki: {len(pasangan)} pasangan subclass->superclass diperiksa")
    if melanggar:
        print(f"  !! {len(melanggar)} PELANGGARAN: {melanggar[:5]}")
    else:
        print("  OK -- K1(subclass) <= K1(superclass) di seluruh pasangan.")
        print("  Konsekuensi: kelayakan MONOTON naik menuju akar. Bila anak layak,")
        print("  induknya pasti layak; bila induk tidak layak, anaknya juga tidak.")
    return {"pasangan": int(len(pasangan)), "pelanggaran": melanggar}


def main() -> int:
    db, diag = muat()
    panjang = peta_label(db, diag)
    kal = panjang[panjang["fold"] == CALIB_FOLD]

    print(f"Pernyataan diagnostik SCP: {len(diag)}")
    print(f"Pasangan (rekaman,label) seluruh data: {len(panjang):,}")
    print(f"Pada fold {CALIB_FOLD}: {len(kal):,} pasangan, {kal['blok'].nunique():,} blok pasien")

    hasil = {}
    for tingkat in ("superclass", "subclass", "scp_code"):
        m = int(kal[tingkat].nunique())
        tabel = kelayakan(panjang, tingkat, m)
        cetak(tingkat.upper(), tabel, m)
        hasil[tingkat] = {
            "m": m,
            "label": {
                str(nama): {
                    "blok_kalibrasi": int(r["blok"]),
                    "rekaman_kalibrasi": int(r["rekaman"]),
                    "alpha_min": round(float(r["alpha_min"]), 6),
                    "layak": {f"{a:.2f}": bool(r[f"a={a:.2f}"]) for a in ALPHAS},
                    "layak_005_serentak": bool(r["a=0,05 serentak"]),
                }
                for nama, r in tabel.iterrows()
            },
        }

        n_gagal = int((~tabel["a=0.05"]).sum())
        n_gagal_srt = int((~tabel["a=0,05 serentak"]).sum())
        blok_perlu = math.ceil(m / 0.05) - 1
        print(
            f"\n  Pada alpha=0,05 marginal : {n_gagal}/{m} label TIDAK layak"
            f"\n  Pada alpha=0,05 serentak : {n_gagal_srt}/{m} label TIDAK layak"
            f"  (butuh >= {blok_perlu:,} blok per label)"
        )
        hasil[tingkat]["ringkasan"] = {
            "tidak_layak_marginal_005": n_gagal,
            "tidak_layak_serentak_005": n_gagal_srt,
            "blok_dibutuhkan_serentak": blok_perlu,
        }

    hasil["monotonisitas"] = periksa_monotonisitas(panjang)

    keluaran = ROOT / "results" / "raw" / "label_feasibility.json"
    keluaran.parent.mkdir(parents=True, exist_ok=True)
    keluaran.write_text(json.dumps(hasil, indent=2), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
