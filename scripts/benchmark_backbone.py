"""Ukur kelayakan backbone pada perangkat ini.

Menentukan apakah rencana eksperimen (melatih backbone resmi skala xresnet1d101)
dapat dijalankan, atau harus diganti dengan backbone yang lebih kecil disertai
justifikasi eksplisit di naskah.

Keluaran: waktu maju+mundur per batch, estimasi waktu per epoch PTB-XL dan MIT-BIH.
"""

from __future__ import annotations

import json
import os
import platform
import time
from pathlib import Path

import torch
import torch.nn as nn

AKAR = Path(__file__).resolve().parent.parent
KELUARAN = AKAR / "results" / "raw" / "benchmark_backbone.json"

# PTB-XL: 12 lead, 1000 cuplikan (100 Hz x 10 s); fold 1-6 = 17.418 rekaman.
PTBXL_LATIH = 17_418
PTBXL_LEAD = 12
PTBXL_PANJANG = 1_000

# MIT-BIH: 1 kanal MLII, jendela 256; DS1 = 51.000 detak.
MITDB_LATIH = 51_000
MITDB_LEAD = 1
MITDB_PANJANG = 256

# Sengaja kecil: tujuannya menentukan kelayakan, bukan angka presisi tinggi.
BATCH = 32
BATCH_UKUR = 3
BATCH_PEMANASAN = 1


class BlokDasar(nn.Module):
    ekspansi = 1

    def __init__(self, masuk: int, lebar: int, langkah: int = 1):
        super().__init__()
        self.conv1 = nn.Conv1d(masuk, lebar, 3, stride=langkah, padding=1, bias=False)
        self.bn1 = nn.BatchNorm1d(lebar)
        self.conv2 = nn.Conv1d(lebar, lebar, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(lebar)
        self.relu = nn.ReLU(inplace=True)
        self.pintas = None
        if langkah != 1 or masuk != lebar * self.ekspansi:
            self.pintas = nn.Sequential(
                nn.Conv1d(masuk, lebar * self.ekspansi, 1, stride=langkah, bias=False),
                nn.BatchNorm1d(lebar * self.ekspansi),
            )

    def forward(self, x):
        sisa = x if self.pintas is None else self.pintas(x)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        return self.relu(x + sisa)


class BlokLeher(nn.Module):
    ekspansi = 4

    def __init__(self, masuk: int, lebar: int, langkah: int = 1):
        super().__init__()
        keluar = lebar * self.ekspansi
        self.conv1 = nn.Conv1d(masuk, lebar, 1, bias=False)
        self.bn1 = nn.BatchNorm1d(lebar)
        self.conv2 = nn.Conv1d(lebar, lebar, 3, stride=langkah, padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(lebar)
        self.conv3 = nn.Conv1d(lebar, keluar, 1, bias=False)
        self.bn3 = nn.BatchNorm1d(keluar)
        self.relu = nn.ReLU(inplace=True)
        self.pintas = None
        if langkah != 1 or masuk != keluar:
            self.pintas = nn.Sequential(
                nn.Conv1d(masuk, keluar, 1, stride=langkah, bias=False),
                nn.BatchNorm1d(keluar),
            )

    def forward(self, x):
        sisa = x if self.pintas is None else self.pintas(x)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.bn3(self.conv3(x))
        return self.relu(x + sisa)


class ResNet1D(nn.Module):
    def __init__(self, blok, lapisan, n_lead: int, n_kelas: int, lebar_awal: int = 64):
        super().__init__()
        self.masuk = lebar_awal
        self.batang = nn.Sequential(
            nn.Conv1d(n_lead, lebar_awal, 7, stride=2, padding=3, bias=False),
            nn.BatchNorm1d(lebar_awal),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(3, stride=2, padding=1),
        )
        tahap = []
        for i, (lebar, n) in enumerate(zip([64, 128, 256, 512], lapisan)):
            tahap.append(self._buat_tahap(blok, lebar, n, langkah=1 if i == 0 else 2))
        self.tahap = nn.Sequential(*tahap)
        self.kepala = nn.Sequential(
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(512 * blok.ekspansi, n_kelas),
        )

    def _buat_tahap(self, blok, lebar, n, langkah):
        blok_blok = [blok(self.masuk, lebar, langkah)]
        self.masuk = lebar * blok.ekspansi
        blok_blok += [blok(self.masuk, lebar) for _ in range(n - 1)]
        return nn.Sequential(*blok_blok)

    def forward(self, x):
        return self.kepala(self.tahap(self.batang(x)))


def ukur(model: nn.Module, n_lead: int, panjang: int) -> dict:
    """Waktu rata-rata satu langkah maju+mundur, detik."""
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    kriteria = nn.BCEWithLogitsLoss()
    x = torch.randn(BATCH, n_lead, panjang)
    y = torch.randint(0, 2, (BATCH, model.kepala[-1].out_features)).float()

    for _ in range(BATCH_PEMANASAN):
        optimizer.zero_grad()
        kriteria(model(x), y).backward()
        optimizer.step()

    mulai = time.perf_counter()
    for _ in range(BATCH_UKUR):
        optimizer.zero_grad()
        kriteria(model(x), y).backward()
        optimizer.step()
    total = time.perf_counter() - mulai

    return {
        "parameter": sum(p.numel() for p in model.parameters()),
        "detik_per_batch": total / BATCH_UKUR,
    }


def main() -> None:
    torch.manual_seed(0)
    print(f"platform        : {platform.platform()}")
    print(f"torch           : {torch.__version__}")
    print(f"thread dipakai  : {torch.get_num_threads()}")
    print(f"CPU logis       : {os.cpu_count()}")
    print(f"batch           : {BATCH}  (ukur {BATCH_UKUR} batch sesudah {BATCH_PEMANASAN} pemanasan)")
    print()

    kandidat = [
        ("SmallECGNet-setara (BasicBlock [1,1,1,1], lebar 16)",
         lambda: ResNet1D(BlokDasar, [1, 1, 1, 1], PTBXL_LEAD, 5, lebar_awal=16)),
        ("resnet1d34  (BasicBlock [3,4,6,3])",
         lambda: ResNet1D(BlokDasar, [3, 4, 6, 3], PTBXL_LEAD, 5)),
        ("resnet1d50  (Bottleneck [3,4,6,3])",
         lambda: ResNet1D(BlokLeher, [3, 4, 6, 3], PTBXL_LEAD, 5)),
        ("xresnet1d101-skala (Bottleneck [3,4,23,3])",
         lambda: ResNet1D(BlokLeher, [3, 4, 23, 3], PTBXL_LEAD, 5)),
    ]

    hasil = []
    for nama, bangun in kandidat:
        catatan = ukur(bangun(), PTBXL_LEAD, PTBXL_PANJANG)
        batch_per_epoch = -(-PTBXL_LATIH // BATCH)
        menit = catatan["detik_per_batch"] * batch_per_epoch / 60.0
        catatan.update(nama=nama, menit_per_epoch_ptbxl=menit)
        hasil.append(catatan)
        print(f"{nama:<52} {catatan['parameter']:>12,} par  "
              f"{catatan['detik_per_batch']:>7.3f} s/batch  "
              f"{menit:>8.1f} menit/epoch")

    print()
    print("Estimasi 30 epoch PTB-XL (fold 1-6, 17.418 rekaman):")
    for catatan in hasil:
        jam = catatan["menit_per_epoch_ptbxl"] * 30 / 60.0
        vonis = "LAYAK" if jam <= 12 else ("BERAT" if jam <= 48 else "TIDAK LAYAK")
        print(f"  {catatan['nama']:<52} {jam:>7.1f} jam   {vonis}")

    KELUARAN.parent.mkdir(parents=True, exist_ok=True)
    KELUARAN.write_text(json.dumps({
        "torch": torch.__version__,
        "thread": torch.get_num_threads(),
        "cpu_logis": os.cpu_count(),
        "batch": BATCH,
        "ptbxl_latih": PTBXL_LATIH,
        "hasil": hasil,
    }, indent=2), encoding="utf-8")
    print(f"\nDitulis: {KELUARAN.relative_to(AKAR)}")


if __name__ == "__main__":
    main()
