"""Loader PTB-XL 100 Hz: metadata, label superclass, dan sinyal dengan cache.

Keputusan yang dibekukan di sini (lihat docs/protocol.md):
- 100 Hz (`filename_lr`), bukan 500 Hz
- Target = 5 superclass diagnostik. Ini satu-satunya tingkat yang kelayakan
  per-labelnya aman bahkan di bawah koreksi serentak (docs/theory.md par. 5.5).
- Band-pass 0,5-40 Hz + normalisasi per-lead
- Blok = `patient_id`; split memakai `strat_fold` resmi

Sinyal mentah disimpan apa adanya di cache; pemrosesan dilakukan terpisah agar
perubahan filter tidak memaksa pembacaan ulang 21.799 berkas WFDB.
"""

from __future__ import annotations

import ast
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]
PTBXL = ROOT / "data" / "raw" / "ptbxl"
INTERIM = ROOT / "data" / "interim"

SUPERCLASS = ["NORM", "MI", "STTC", "CD", "HYP"]
FS = 100
PANJANG = 1000  # 10 detik @ 100 Hz
BANDPASS = (0.5, 40.0)


def load_metadata() -> pd.DataFrame:
    """Metadata + lima kolom biner superclass + `n_superclass`."""
    df = pd.read_csv(PTBXL / "ptbxl_database.csv", index_col="ecg_id")
    scp = pd.read_csv(PTBXL / "scp_statements.csv", index_col=0)
    kelas = scp[scp["diagnostic"] == 1]["diagnostic_class"].to_dict()

    kode = df["scp_codes"].apply(ast.literal_eval)
    for s in SUPERCLASS:
        df[s] = kode.apply(lambda d, s=s: any(kelas.get(k) == s for k in d)).astype(np.int8)
    df["n_superclass"] = df[SUPERCLASS].sum(axis=1)
    return df


def _cache_path(nama: str) -> pathlib.Path:
    INTERIM.mkdir(parents=True, exist_ok=True)
    return INTERIM / nama


def build_raw_cache(df: pd.DataFrame, force: bool = False) -> pathlib.Path:
    """Baca seluruh WFDB 100 Hz sekali, simpan sebagai satu array float32.

    Ditulis ke berkas sementara lalu di-rename. Tanpa ini, pembangunan yang
    terputus meninggalkan berkas berukuran penuh yang tampak lengkap dan akan
    dipakai apa adanya pada run berikutnya -- hasilnya rusak secara diam-diam.
    """
    import wfdb

    keluaran = _cache_path("ptbxl_100hz_raw.npy")
    if keluaran.exists() and not force:
        return keluaran

    sementara = keluaran.with_suffix(".npy.partial")
    n = len(df)
    arr = np.lib.format.open_memmap(
        sementara, mode="w+", dtype=np.float32, shape=(n, PANJANG, 12)
    )
    for i, nama in enumerate(df["filename_lr"]):
        sinyal, _ = wfdb.rdsamp(str(PTBXL / nama))
        arr[i] = sinyal.astype(np.float32)
        if (i + 1) % 2000 == 0:
            print(f"  {i + 1:,}/{n:,}", flush=True)
    arr.flush()
    del arr
    sementara.replace(keluaran)
    return keluaran


def build_processed_cache(df: pd.DataFrame, force: bool = False) -> pathlib.Path:
    """Band-pass 0,5-40 Hz lalu normalisasi per-lead per-rekaman."""
    from scipy.signal import butter, sosfiltfilt

    keluaran = _cache_path("ptbxl_100hz_proc.npy")
    if keluaran.exists() and not force:
        return keluaran

    mentah = np.load(build_raw_cache(df), mmap_mode="r")
    sos = butter(3, BANDPASS, btype="bandpass", fs=FS, output="sos")

    sementara = keluaran.with_suffix(".npy.partial")
    arr = np.lib.format.open_memmap(
        sementara, mode="w+", dtype=np.float32, shape=mentah.shape
    )
    blok = 1000
    for mulai in range(0, len(mentah), blok):
        potongan = np.asarray(mentah[mulai : mulai + blok], dtype=np.float64)
        potongan = sosfiltfilt(sos, potongan, axis=1)
        mu = potongan.mean(axis=1, keepdims=True)
        sd = potongan.std(axis=1, keepdims=True)
        arr[mulai : mulai + blok] = ((potongan - mu) / np.maximum(sd, 1e-6)).astype(np.float32)
    arr.flush()
    del arr
    sementara.replace(keluaran)
    return keluaran


def load_signals(df: pd.DataFrame, processed: bool = True) -> np.ndarray:
    jalur = build_processed_cache(df) if processed else build_raw_cache(df)
    return np.load(jalur, mmap_mode="r")


def split_indices(df: pd.DataFrame, train, calib: int, test: int) -> dict[str, np.ndarray]:
    """Indeks posisi (bukan ecg_id) per bagian, memakai `strat_fold` resmi."""
    fold = df["strat_fold"].to_numpy()
    return {
        "train": np.flatnonzero(np.isin(fold, train)),
        "calib": np.flatnonzero(fold == calib),
        "test": np.flatnonzero(fold == test),
    }
