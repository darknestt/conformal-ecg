"""Loader MIT-BIH: ekstraksi detak per rekaman dengan blok = rekaman.

Dipakai untuk menguji H0b pada ujung spektrum dependensi yang berlawanan
dari PTB-XL:

    PTB-XL  : K = 1.942 blok, N_k = 1,12   -> rasio bobot HCP/split 1,12x
    MIT-BIH : K =    22 blok, N_k = 2.260  -> rasio bobot          1.929x

Keputusan yang dibekukan:
- Split inter-pasien de Chazal dkk. (2004): DS1 latih, DS2 kalibrasi/uji
- 4 rekaman berpacu (102, 104, 107, 217) dikecualikan sesuai rekomendasi AAMI
- Kanal dipilih menurut NAMA "MLII", bukan indeks. Rekaman 114 berurutan
  [V5, MLII]; memakai indeks 0 akan diam-diam melatih pada lead yang salah.
- Jendela 256 sampel berpusat di anotasi R (0,71 s @ 360 Hz)
- Band-pass 0,5-40 Hz + normalisasi z per detak, sama seperti PTB-XL
"""

from __future__ import annotations

import pathlib

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
MITDB = ROOT / "data" / "raw" / "mitdb"
INTERIM = ROOT / "data" / "interim"

FS = 360
JENDELA = 256
SETENGAH = JENDELA // 2
BANDPASS = (0.5, 40.0)
KANAL = "MLII"

BERPACU = ("102", "104", "107", "217")

DS1 = ["101", "106", "108", "109", "112", "114", "115", "116", "118", "119", "122",
       "124", "201", "203", "205", "207", "208", "209", "215", "220", "223", "230"]
DS2 = ["100", "103", "105", "111", "113", "117", "121", "123", "200", "202", "210",
       "212", "213", "214", "219", "221", "222", "228", "231", "232", "233", "234"]

KELAS = ["N", "S", "V", "F", "Q"]
AAMI = {
    "N": set("NLRej"),
    "S": set("AaJS"),
    "V": {"V", "E"},
    "F": {"F"},
    "Q": {"/", "f", "Q"},
}
_PETA = {s: k for k, ss in AAMI.items() for s in ss}


def _cache() -> pathlib.Path:
    INTERIM.mkdir(parents=True, exist_ok=True)
    return INTERIM / f"mitdb_beats_{JENDELA}.npz"


def _baca_rekaman(nama: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Kembalikan (jendela, label, posisi) untuk satu rekaman."""
    import wfdb
    from scipy.signal import butter, sosfiltfilt

    rec = wfdb.rdrecord(str(MITDB / nama))
    if KANAL not in rec.sig_name:
        raise ValueError(f"rekaman {nama} tidak punya kanal {KANAL}: {rec.sig_name}")
    sinyal = rec.p_signal[:, rec.sig_name.index(KANAL)].astype(np.float64)

    sos = butter(3, BANDPASS, btype="bandpass", fs=FS, output="sos")
    sinyal = sosfiltfilt(sos, sinyal)

    ann = wfdb.rdann(str(MITDB / nama), "atr")
    jendela, label, posisi = [], [], []
    for p, s in zip(ann.sample, ann.symbol, strict=True):
        k = _PETA.get(s)
        if k is None:
            continue
        a, b = p - SETENGAH, p + SETENGAH
        if a < 0 or b > len(sinyal):
            continue  # detak di tepi rekaman -- dibuang, bukan di-pad
        w = sinyal[a:b]
        sd = w.std()
        jendela.append((w - w.mean()) / (sd if sd > 1e-6 else 1.0))
        label.append(KELAS.index(k))
        posisi.append(p)

    return (
        np.asarray(jendela, dtype=np.float32),
        np.asarray(label, dtype=np.int64),
        np.asarray(posisi, dtype=np.int64),
    )


def build_cache(force: bool = False) -> pathlib.Path:
    keluaran = _cache()
    if keluaran.exists() and not force:
        return keluaran

    semua_x, semua_y, semua_rec = [], [], []
    for nama in DS1 + DS2:
        x, y, _ = _baca_rekaman(nama)
        semua_x.append(x)
        semua_y.append(y)
        semua_rec.append(np.full(len(y), int(nama), dtype=np.int64))
        print(f"  {nama}: {len(y):,} detak", flush=True)

    # np.savez menambahkan ".npz" bila nama tidak berakhiran itu -- nama sementara
    # karenanya harus tetap berakhiran .npz, bukan .npz.partial.
    sementara = keluaran.with_suffix("").with_suffix(".partial.npz")
    np.savez(
        sementara,
        x=np.concatenate(semua_x),
        y=np.concatenate(semua_y),
        rec=np.concatenate(semua_rec),
    )
    sementara.replace(keluaran)
    return keluaran


def load_beats() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Kembalikan (x, y, rec): jendela detak, kelas AAMI, nomor rekaman (= blok)."""
    d = np.load(build_cache())
    return d["x"], d["y"], d["rec"]
