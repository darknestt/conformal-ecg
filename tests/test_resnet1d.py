import pytest
import torch

from src.models.resnet1d import BlokDasar, BlokLeher, resnet1d34, resnet1d50
from src.models.small_ecg_net import SmallECGNet

# Nilai acuan dari scripts/benchmark_backbone.py; mengunci kapasitas yang
# dilaporkan di naskah agar tidak berubah diam-diam.
PARAM_ACUAN = {"resnet1d34": 7_225_733, "resnet1d50": 15_969_413}

PTBXL = (12, 1000)
MITDB = (1, 256)


@pytest.mark.parametrize("bangun", [resnet1d34, resnet1d50])
@pytest.mark.parametrize(("n_leads", "panjang"), [PTBXL, MITDB])
def test_bentuk_keluaran(bangun, n_leads, panjang):
    model = bangun(n_leads=n_leads, n_classes=5)
    keluar = model(torch.randn(4, n_leads, panjang))
    assert keluar.shape == (4, 5)


@pytest.mark.parametrize(("nama", "bangun"), [("resnet1d34", resnet1d34), ("resnet1d50", resnet1d50)])
def test_jumlah_parameter_terkunci(nama, bangun):
    assert bangun(n_leads=12, n_classes=5).n_params() == PARAM_ACUAN[nama]


def test_kapasitas_menaik_tajam():
    """Rentang kapasitas harus lebar; itu dasar klaim invariansi lintas backbone."""
    kecil = SmallECGNet(n_leads=12, n_classes=5).n_params()
    assert kecil < resnet1d34().n_params() < resnet1d50().n_params()
    assert resnet1d50().n_params() / kecil > 100


@pytest.mark.parametrize("bangun", [resnet1d34, resnet1d50])
def test_gradien_mengalir_ke_semua_parameter(bangun):
    model = bangun(n_leads=12, n_classes=5)
    model(torch.randn(2, 12, 1000)).sum().backward()
    tanpa_grad = [n for n, p in model.named_parameters() if p.grad is None]
    assert tanpa_grad == []


def test_pintas_dilewati_bila_bentuk_sudah_cocok():
    assert BlokDasar(64, 64, stride=1).pintas is None
    assert BlokDasar(64, 64, stride=2).pintas is not None
    assert BlokLeher(256, 64, stride=1).pintas is None  # 64 * ekspansi 4 == 256
    assert BlokLeher(64, 64, stride=1).pintas is not None


@pytest.mark.parametrize("panjang", [256, 500, 1000, 1024])
def test_panjang_masukan_bebas(panjang):
    model = resnet1d34(n_leads=12, n_classes=5)
    assert model(torch.randn(2, 12, panjang)).shape == (2, 5)


def test_eval_menerima_batch_tunggal():
    """Kalibrasi konformal menilai satu rekaman pada satu waktu."""
    model = resnet1d50(n_leads=12, n_classes=5).eval()
    with torch.no_grad():
        assert model(torch.randn(1, 12, 1000)).shape == (1, 5)


def test_dropout_tidak_aktif_saat_eval():
    model = resnet1d34(n_leads=12, n_classes=5, dropout=0.9).eval()
    x = torch.randn(3, 12, 1000)
    with torch.no_grad():
        assert torch.allclose(model(x), model(x))
