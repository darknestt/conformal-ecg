import numpy as np
import pytest
import torch
from torch import nn

from src.train import langkah_akumulasi, latih


def _model_tanpa_bn(seed=0):
    torch.manual_seed(seed)
    return nn.Sequential(nn.Flatten(), nn.Linear(12, 8), nn.ReLU(), nn.Linear(8, 3))


def _data(n=96, seed=0):
    g = np.random.default_rng(seed)
    x = g.standard_normal((n, 12)).astype(np.float32)
    y = (g.random((n, 3)) < 0.3).astype(np.float32)
    return x, y


@pytest.mark.parametrize("mikro", [1, 7, 16, 64])
def test_akumulasi_sama_dengan_batch_penuh(mikro):
    """Tanpa BatchNorm, gradien akumulasi harus identik dengan batch penuh."""
    x, y = _data(64)
    xb, yb = torch.from_numpy(x), torch.from_numpy(y)
    rugi_fn = nn.BCEWithLogitsLoss()

    acuan = _model_tanpa_bn()
    rugi_fn(acuan(xb), yb).backward()

    uji = _model_tanpa_bn()
    rugi = langkah_akumulasi(uji, rugi_fn, xb, yb, mikro)

    assert rugi == pytest.approx(float(rugi_fn(acuan(xb), yb).detach()), rel=1e-5)
    for pa, pu in zip(acuan.parameters(), uji.parameters(), strict=True):
        assert torch.allclose(pa.grad, pu.grad, atol=1e-6)


def test_akumulasi_sisa_mikro_tak_rata_tetap_benar():
    """Batch 10, mikro 4 -> potongan 4,4,2; bobot harus proporsional ukuran."""
    x, y = _data(10)
    xb, yb = torch.from_numpy(x), torch.from_numpy(y)
    rugi_fn = nn.BCEWithLogitsLoss()
    acuan, uji = _model_tanpa_bn(), _model_tanpa_bn()
    rugi_fn(acuan(xb), yb).backward()
    langkah_akumulasi(uji, rugi_fn, xb, yb, 4)
    for pa, pu in zip(acuan.parameters(), uji.parameters(), strict=True):
        assert torch.allclose(pa.grad, pu.grad, atol=1e-6)


def _jalankan(tmp, epochs, x, y, seed=0):
    model = _model_tanpa_bn(seed)
    return latih(
        model, lambda i: torch.from_numpy(x[i]), y,
        np.arange(0, 80), np.arange(80, 96),
        rugi_fn=nn.BCEWithLogitsLoss(), epochs=epochs, batch=16, mikro=8,
        seed=seed, sabar_maks=100, titik_simpan=tmp, log=lambda _s: None,
    )


def test_lanjut_dari_titik_simpan_identik_dengan_tanpa_jeda(tmp_path):
    """Latih 4 epoch sekaligus == latih 2 epoch, berhenti, lanjut 2 epoch."""
    x, y = _data()
    utuh, info_utuh = _jalankan(tmp_path / "a.pt", 4, x, y)

    _jalankan(tmp_path / "b.pt", 2, x, y)
    lanjut, info_lanjut = _jalankan(tmp_path / "b.pt", 4, x, y)

    assert info_lanjut["epoch_dijalankan"] == 4
    assert [r["val"] for r in info_lanjut["riwayat"]] == pytest.approx(
        [r["val"] for r in info_utuh["riwayat"]], rel=1e-6
    )
    for pa, pb in zip(utuh.parameters(), lanjut.parameters(), strict=True):
        assert torch.allclose(pa, pb, atol=1e-6)


def test_bobot_terbaik_dipulihkan(tmp_path):
    x, y = _data()
    model, info = _jalankan(tmp_path / "c.pt", 6, x, y)
    terbaik = min(r["val"] for r in info["riwayat"])
    assert info["val_terbaik"] == pytest.approx(terbaik)
    assert not model.training


def test_early_stopping_bertahan_setelah_dilanjutkan(tmp_path):
    """Bila sudah berhenti dini, pemanggilan ulang tidak boleh melatih lagi."""
    x, y = _data()
    titik = tmp_path / "d.pt"
    kw = dict(rugi_fn=nn.BCEWithLogitsLoss(), batch=16, mikro=8, seed=0,
              sabar_maks=1, titik_simpan=titik, log=lambda _s: None, lr=0.0)
    ambil = lambda i: torch.from_numpy(x[i])  # noqa: E731
    _, info1 = latih(_model_tanpa_bn(), ambil, y, np.arange(80), np.arange(80, 96), epochs=10, **kw)
    _, info2 = latih(_model_tanpa_bn(), ambil, y, np.arange(80), np.arange(80, 96), epochs=10, **kw)
    assert info1["epoch_dijalankan"] == 2
    assert info2["epoch_dijalankan"] == 2


def test_maks_batch_membatasi_satu_epoch(tmp_path):
    x, y = _data()
    _, info = latih(
        _model_tanpa_bn(), lambda i: torch.from_numpy(x[i]), y,
        np.arange(80), np.arange(80, 96), rugi_fn=nn.BCEWithLogitsLoss(),
        epochs=1, batch=16, mikro=8, seed=0, maks_batch=2, log=lambda _s: None,
    )
    assert info["epoch_dijalankan"] == 1
