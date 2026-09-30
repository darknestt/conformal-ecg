"""Backbone kecil untuk studi kelayakan (Langkah 4).

Sengaja kecil (~100k parameter) agar dapat dilatih di CPU dalam waktu wajar.
Tujuannya BUKAN mengejar AUROC benchmark, melainkan menghasilkan skor
nonconformity yang masuk akal untuk menguji H0. Backbone benchmark
(xresnet1d101 dkk.) baru dipakai di F2.
"""

from __future__ import annotations

import torch
from torch import nn


def _blok(masuk: int, keluar: int, kernel: int, stride: int = 1) -> nn.Sequential:
    return nn.Sequential(
        nn.Conv1d(masuk, keluar, kernel, stride=stride, padding=kernel // 2, bias=False),
        nn.BatchNorm1d(keluar),
        nn.ReLU(inplace=True),
    )


class SmallECGNet(nn.Module):
    """CNN 1-D untuk EKG 12-lead 10 detik @ 100 Hz."""

    def __init__(self, n_leads: int = 12, n_classes: int = 5, dropout: float = 0.3) -> None:
        super().__init__()
        self.fitur = nn.Sequential(
            _blok(n_leads, 32, 7, stride=2),  # 1000 -> 500
            nn.MaxPool1d(2),  # -> 250
            _blok(32, 64, 5),
            nn.MaxPool1d(2),  # -> 125
            _blok(64, 128, 5),
            nn.MaxPool1d(2),  # -> 62
            _blok(128, 128, 3),
            nn.AdaptiveAvgPool1d(1),
        )
        self.kepala = nn.Sequential(nn.Flatten(), nn.Dropout(dropout), nn.Linear(128, n_classes))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, n_leads, panjang) -> logit (B, n_classes)."""
        return self.kepala(self.fitur(x))

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
