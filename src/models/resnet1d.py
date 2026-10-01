"""Backbone ResNet 1-D untuk EKG (F2).

Tiga kapasitas dipakai di naskah: `SmallECGNet` (~0,1 jt), `resnet1d34` (~7,2 jt),
`resnet1d50` (~16,0 jt). Rentang itu disengaja: klaim paper menyangkut perilaku
kalibrasi, bukan akurasi klasifikasi, sehingga yang perlu diuji adalah apakah
temuannya bertahan lintas kapasitas model — bukan seberapa baik satu model terbaik.

Tolok ukur perangkat ada di `scripts/benchmark_backbone.py`.
"""

from __future__ import annotations

import torch
from torch import nn

LEBAR_TAHAP = (64, 128, 256, 512)


class BlokDasar(nn.Module):
    """Blok residual dua-konvolusi (dipakai resnet1d18/34)."""

    ekspansi = 1

    def __init__(self, masuk: int, lebar: int, stride: int = 1) -> None:
        super().__init__()
        self.conv1 = nn.Conv1d(masuk, lebar, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm1d(lebar)
        self.conv2 = nn.Conv1d(lebar, lebar, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(lebar)
        self.relu = nn.ReLU(inplace=True)
        self.pintas = _pintas(masuk, lebar * self.ekspansi, stride)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        sisa = x if self.pintas is None else self.pintas(x)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        return self.relu(x + sisa)


class BlokLeher(nn.Module):
    """Blok residual leher-botol 1x1-3x1-1x1 (dipakai resnet1d50/101)."""

    ekspansi = 4

    def __init__(self, masuk: int, lebar: int, stride: int = 1) -> None:
        super().__init__()
        keluar = lebar * self.ekspansi
        self.conv1 = nn.Conv1d(masuk, lebar, 1, bias=False)
        self.bn1 = nn.BatchNorm1d(lebar)
        self.conv2 = nn.Conv1d(lebar, lebar, 3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(lebar)
        self.conv3 = nn.Conv1d(lebar, keluar, 1, bias=False)
        self.bn3 = nn.BatchNorm1d(keluar)
        self.relu = nn.ReLU(inplace=True)
        self.pintas = _pintas(masuk, keluar, stride)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        sisa = x if self.pintas is None else self.pintas(x)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.bn3(self.conv3(x))
        return self.relu(x + sisa)


def _pintas(masuk: int, keluar: int, stride: int) -> nn.Sequential | None:
    """Proyeksi jalur pintas; None bila bentuknya sudah cocok."""
    if stride == 1 and masuk == keluar:
        return None
    return nn.Sequential(
        nn.Conv1d(masuk, keluar, 1, stride=stride, bias=False),
        nn.BatchNorm1d(keluar),
    )


class ResNet1D(nn.Module):
    """ResNet 1-D. Panjang masukan bebas berkat pengumpulan rata-rata adaptif."""

    def __init__(
        self,
        blok: type[nn.Module],
        lapisan: tuple[int, int, int, int],
        n_leads: int = 12,
        n_classes: int = 5,
        dropout: float = 0.3,
        lebar_awal: int = 64,
    ) -> None:
        super().__init__()
        self._masuk = lebar_awal
        self.batang = nn.Sequential(
            nn.Conv1d(n_leads, lebar_awal, 7, stride=2, padding=3, bias=False),
            nn.BatchNorm1d(lebar_awal),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(3, stride=2, padding=1),
        )
        self.fitur = nn.Sequential(
            *(
                self._tahap(blok, lebar, n, stride=1 if i == 0 else 2)
                for i, (lebar, n) in enumerate(zip(LEBAR_TAHAP, lapisan))
            ),
            nn.AdaptiveAvgPool1d(1),
        )
        self.kepala = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(LEBAR_TAHAP[-1] * blok.ekspansi, n_classes),
        )

    def _tahap(self, blok: type[nn.Module], lebar: int, n: int, stride: int) -> nn.Sequential:
        blok_blok = [blok(self._masuk, lebar, stride)]
        self._masuk = lebar * blok.ekspansi
        blok_blok += [blok(self._masuk, lebar) for _ in range(n - 1)]
        return nn.Sequential(*blok_blok)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, n_leads, panjang) -> logit (B, n_classes)."""
        return self.kepala(self.fitur(self.batang(x)))

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def resnet1d34(n_leads: int = 12, n_classes: int = 5, dropout: float = 0.3) -> ResNet1D:
    return ResNet1D(BlokDasar, (3, 4, 6, 3), n_leads, n_classes, dropout)


def resnet1d50(n_leads: int = 12, n_classes: int = 5, dropout: float = 0.3) -> ResNet1D:
    return ResNet1D(BlokLeher, (3, 4, 6, 3), n_leads, n_classes, dropout)
