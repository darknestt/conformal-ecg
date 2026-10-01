"""Pelatihan generik untuk seluruh backbone.

Dipisah dari skrip eksperimen agar dua hal yang menyentuh kebenaran dapat diuji:
akumulasi gradien (batch efektif identik dengan protokol asli walau RAM terbatas)
dan lanjut-dari-titik-simpan (pelatihan belasan jam tidak boleh mulai ulang dari nol).
"""

from __future__ import annotations

import os
import time
from collections.abc import Callable
from pathlib import Path

import numpy as np
import torch
from torch import nn

AmbilX = Callable[[np.ndarray], torch.Tensor]


def langkah_akumulasi(
    model: nn.Module,
    rugi_fn: nn.Module,
    xb: torch.Tensor,
    yb: torch.Tensor,
    mikro: int,
) -> float:
    """Hitung gradien batch penuh lewat mikro-batch; kembalikan rugi rata-rata batch.

    Untuk rugi berreduksi rata-rata, gradiennya sama dengan gradien batch penuh.
    Satu-satunya perbedaan: statistik BatchNorm dihitung per mikro-batch.
    """
    n = len(xb)
    total = 0.0
    for m in range(0, n, mikro):
        xm, ym = xb[m : m + mikro], yb[m : m + mikro]
        rugi = rugi_fn(model(xm), ym)
        (rugi * (len(xm) / n)).backward()
        total += rugi.detach().item() * len(xm)
    return total / n


@torch.no_grad()
def rugi_terbatch(
    model: nn.Module,
    rugi_fn: nn.Module,
    ambil_x: AmbilX,
    y: np.ndarray,
    idx: np.ndarray,
    batch: int,
) -> float:
    """Rugi rata-rata atas idx, dievaluasi per batch agar RAM tidak meledak."""
    total = 0.0
    for m in range(0, len(idx), batch):
        ambil = idx[m : m + batch]
        total += float(rugi_fn(model(ambil_x(ambil)), torch.from_numpy(y[ambil]))) * len(ambil)
    return total / len(idx)


def _simpan_atomik(objek: dict, tujuan: Path) -> None:
    sementara = tujuan.with_name(tujuan.name + ".tmp")
    torch.save(objek, sementara)
    os.replace(sementara, tujuan)


def latih(
    model: nn.Module,
    ambil_x: AmbilX,
    y: np.ndarray,
    idx_latih: np.ndarray,
    idx_val: np.ndarray,
    *,
    rugi_fn: nn.Module,
    epochs: int,
    batch: int,
    mikro: int,
    seed: int,
    sabar_maks: int = 5,
    lr: float = 1e-3,
    titik_simpan: Path | None = None,
    maks_batch: int | None = None,
    log: Callable[[str], None] = print,
) -> tuple[nn.Module, dict]:
    """Adam + early stopping pada rugi validasi; bobot terbaik dipulihkan di akhir.

    Bila `titik_simpan` diberikan, keadaan lengkap disimpan tiap epoch dan
    pemanggilan berikutnya melanjutkan dari sana.
    """
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    rng = np.random.default_rng(seed)
    ep_awal, terbaik, bobot, sabar, riwayat = 1, float("inf"), None, 0, []

    if titik_simpan is not None and titik_simpan.exists():
        keadaan = torch.load(titik_simpan, weights_only=False)
        model.load_state_dict(keadaan["model"])
        opt.load_state_dict(keadaan["opt"])
        rng.bit_generator.state = keadaan["rng"]
        torch.set_rng_state(keadaan["torch_rng"])
        ep_awal, terbaik, bobot, sabar, riwayat = (
            keadaan["epoch"] + 1, keadaan["terbaik"], keadaan["bobot"],
            keadaan["sabar"], keadaan["riwayat"],
        )
        log(f"  dilanjutkan dari epoch {keadaan['epoch']} (val terbaik {terbaik:.4f})")

    berhenti_dini = bool(riwayat) and sabar >= sabar_maks
    for ep in range(ep_awal, epochs + 1):
        if berhenti_dini:
            break
        t0 = time.perf_counter()
        model.train()
        urut = rng.permutation(len(idx_latih))
        n_batch = -(-len(urut) // batch)
        if maks_batch is not None:
            n_batch = min(n_batch, maks_batch)

        total, n_dilihat = 0.0, 0
        for b in range(n_batch):
            ambil = np.sort(idx_latih[urut[b * batch : (b + 1) * batch]])
            opt.zero_grad()
            rugi = langkah_akumulasi(
                model, rugi_fn, ambil_x(ambil), torch.from_numpy(y[ambil]), mikro
            )
            opt.step()
            total += rugi * len(ambil)
            n_dilihat += len(ambil)

        model.eval()
        rv = rugi_terbatch(model, rugi_fn, ambil_x, y, idx_val, batch=max(mikro, 64))
        detik = time.perf_counter() - t0
        riwayat.append({"epoch": ep, "latih": total / n_dilihat, "val": rv, "detik": detik})
        log(f"  epoch {ep:>2}  latih={total / n_dilihat:.4f}  val={rv:.4f}  ({detik:.0f} d)")

        if rv < terbaik - 1e-4:
            terbaik, sabar = rv, 0
            bobot = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            sabar += 1
            berhenti_dini = sabar >= sabar_maks
            if berhenti_dini:
                log(f"  early stopping di epoch {ep}")

        if titik_simpan is not None:
            _simpan_atomik(
                {
                    "model": model.state_dict(), "opt": opt.state_dict(), "epoch": ep,
                    "terbaik": terbaik, "bobot": bobot, "sabar": sabar, "riwayat": riwayat,
                    "rng": rng.bit_generator.state, "torch_rng": torch.get_rng_state(),
                },
                titik_simpan,
            )

    if bobot is not None:
        model.load_state_dict(bobot)
    model.eval()
    return model, {"val_terbaik": terbaik, "epoch_dijalankan": len(riwayat), "riwayat": riwayat}
