"""Uji korektness baseline conformal hierarkis B12-B15 dan diagnostik C7.

Prasyarat pembekuan protokol (docs/protocol.md §13). Seluruh uji berjalan pada
data sintetis dengan struktur blok yang diketahui, sehingga kebenarannya dapat
diperiksa terhadap pernyataan formal di makalah asli — bukan terhadap intuisi.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.conformal import (
    block_sufficiency,
    double_conformal,
    hcp,
    icc_at_threshold,
    icc_curve,
    intraclass_correlation,
    label_sufficiency,
    minimum_blocks,
    pooling_cdfs,
    repeated_subsampling,
    split_conformal,
    subsampling_once,
    weighted_quantile,
)


def hierarchical_scores(k, n, rng, tau=1.0, sigma=0.3):
    """K blok x N pengukuran. `tau` besar relatif `sigma` = korelasi intra-blok kuat."""
    effect = rng.normal(0.0, tau, size=k)
    scores = effect[:, None] + rng.normal(0.0, sigma, size=(k, n))
    blocks = np.repeat(np.arange(k), n)
    return scores.ravel(), blocks


# --------------------------------------------------------------------------
# Kuantil berbobot
# --------------------------------------------------------------------------


def test_kuantil_tanpa_bobot_setara_kuantil_biasa():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    w = np.ones(4)
    assert weighted_quantile(x, w, 0.5) == 2.0
    assert weighted_quantile(x, w, 0.75) == 3.0
    assert weighted_quantile(x, w, 1.0 - 1e-15) == 4.0


def test_kuantil_mengembalikan_inf_bila_massa_tak_tercapai():
    # Atom +inf bermassa 0,5; level 0,9 tidak terjangkau oleh nilai berhingga.
    assert weighted_quantile(np.array([1.0, np.inf]), np.array([0.5, 0.5]), 0.9) == np.inf


# --------------------------------------------------------------------------
# B12 HCP — pernyataan formal dari Lee, Barber & Willett (2026)
# --------------------------------------------------------------------------


def test_hcp_identik_split_conformal_bila_tiap_blok_satu_titik():
    """Makalah menyatakan: bila N_k = 1 untuk semua k, HCP tereduksi ke split conformal."""
    rng = np.random.default_rng(0)
    scores = rng.normal(size=60)
    blocks = np.arange(60)  # satu titik per blok

    for alpha in (0.01, 0.05, 0.1, 0.2):
        assert hcp(scores, blocks, alpha).threshold == split_conformal(scores, alpha).threshold


def test_hcp_selalu_lebih_konservatif_daripada_split_naif():
    """Massa +inf HCP = 1/(K+1) >= 1/(n+1) milik split, sehingga ambangnya tak pernah lebih kecil."""
    rng = np.random.default_rng(1)
    scores, blocks = hierarchical_scores(30, 6, rng)

    for alpha in (0.05, 0.1, 0.2):
        assert hcp(scores, blocks, alpha).threshold >= split_conformal(scores, alpha).threshold


@pytest.mark.parametrize("alpha", [0.001, 0.01, 0.02])
def test_h1_ambang_menjadi_takhingga_di_bawah_batas_kelayakan(alpha):
    """H1 protokol: bila alpha < 1/(K+1), himpunan prediksi wajib trivial."""
    rng = np.random.default_rng(2)
    scores, blocks = hierarchical_scores(k=11, n=40, rng=rng)  # K=11 -> alpha_min = 1/12

    result = hcp(scores, blocks, alpha)
    assert alpha < result.alpha_min
    assert result.is_trivial
    assert not result.is_feasible


def test_ambang_berhingga_tepat_di_atas_batas_kelayakan():
    rng = np.random.default_rng(3)
    scores, blocks = hierarchical_scores(k=11, n=40, rng=rng)

    result = hcp(scores, blocks, alpha=0.09)  # 0,09 > 1/12 = 0,0833
    assert result.is_feasible
    assert np.isfinite(result.threshold)


@pytest.mark.parametrize("k", [9, 19, 39, 99])
def test_batas_kelayakan_TIDAK_ketat(k):
    """Tepat pada alpha = 1/(K+1), ambangnya BERHINGGA -- bukan +inf.

    Massa berhingga totalnya K/(K+1), yang persis menyamai level 1-alpha.
    Karena kuantil didefinisikan dengan `>=`, level itu tercapai di skor
    maksimum. Jadi syaratnya alpha >= 1/(K+1), sejajar dengan syarat baku
    split conformal n >= 1/alpha - 1.
    """
    scores = np.arange(1.0, k + 1.0)
    blocks = np.arange(k)

    di_batas = hcp(scores, blocks, alpha=1.0 / (k + 1))
    assert np.isfinite(di_batas.threshold)
    assert di_batas.threshold == scores.max()
    assert di_batas.is_feasible

    sedikit_di_bawah = hcp(scores, blocks, alpha=1.0 / (k + 1) - 1e-9)
    assert sedikit_di_bawah.is_trivial


def test_cakupan_tetap_sah_tepat_di_batas_kelayakan():
    """Rezim batas bukan sekadar berhingga secara teknis -- cakupannya benar."""
    k, alpha, trials = 19, 0.05, 20_000
    rng = np.random.default_rng(7)
    blocks = np.arange(k)

    tertutup = 0
    for _ in range(trials):
        tertutup += rng.normal() <= hcp(rng.normal(size=k), blocks, alpha).threshold

    cakupan = tertutup / trials
    assert alpha == pytest.approx(1.0 / (k + 1))
    assert cakupan >= 1 - alpha - 3 * np.sqrt(0.95 * 0.05 / trials)


def test_ambang_menurun_secara_monoton_terhadap_alpha():
    rng = np.random.default_rng(4)
    scores, blocks = hierarchical_scores(50, 4, rng)

    thresholds = [hcp(scores, blocks, a).threshold for a in (0.05, 0.1, 0.2, 0.3)]
    assert all(a >= b for a, b in zip(thresholds, thresholds[1:]))


def test_teorema_1_batas_cakupan_dua_sisi():
    """Teorema 1: 1-alpha <= cakupan <= 1-alpha + 2/(K+1) untuk titik uji dari blok baru."""
    k, n, alpha, trials = 20, 5, 0.2, 4000
    rng = np.random.default_rng(12345)
    tau, sigma = 1.0, 0.3

    tertutup = 0
    for _ in range(trials):
        effect = rng.normal(0.0, tau, size=k)
        scores = (effect[:, None] + rng.normal(0.0, sigma, size=(k, n))).ravel()
        blocks = np.repeat(np.arange(k), n)

        # Titik uji berasal dari blok yang belum pernah terlihat.
        s_test = rng.normal(0.0, tau) + rng.normal(0.0, sigma)
        tertutup += s_test <= hcp(scores, blocks, alpha).threshold

    cakupan = tertutup / trials
    galat_mc = 3.0 * np.sqrt(0.85 * 0.15 / trials)

    assert cakupan >= 1 - alpha - galat_mc, f"HCP kurang-cakup: {cakupan:.4f}"
    assert cakupan <= 1 - alpha + 2 / (k + 1) + galat_mc, f"HCP terlalu longgar: {cakupan:.4f}"


# --------------------------------------------------------------------------
# B13-B15 — metode Dunn dkk. (2022)
# --------------------------------------------------------------------------


def test_proposisi_1_pooling_cdfs_setara_hcp_dengan_alpha_disesuaikan():
    """Lee dkk. Proposisi 1: Pooling CDFs == HCP dengan alpha' = alpha + (1-alpha)/(K+1)."""
    rng = np.random.default_rng(5)
    scores, blocks = hierarchical_scores(40, 5, rng)

    for alpha in (0.05, 0.1, 0.2):
        k = 40
        alpha_aksen = alpha + (1 - alpha) / (k + 1)
        assert pooling_cdfs(scores, blocks, alpha).threshold == pytest.approx(
            hcp(scores, blocks, alpha_aksen).threshold
        )


def test_pooling_kurang_konservatif_daripada_hcp():
    rng = np.random.default_rng(6)
    scores, blocks = hierarchical_scores(25, 4, rng)

    for alpha in (0.05, 0.1, 0.2):
        assert pooling_cdfs(scores, blocks, alpha).threshold <= hcp(scores, blocks, alpha).threshold


def test_double_conformal_paling_konservatif():
    """Union bound alpha/2 + alpha/2 membuat B15 tak pernah kurang konservatif daripada HCP.

    Blok sengaja dibuat besar (N=60) agar B15 menghasilkan ambang BERHINGGA;
    tanpa itu uji ini lolos secara hampa karena hanya membandingkan inf >= x.
    """
    rng = np.random.default_rng(7)
    scores, blocks = hierarchical_scores(60, 60, rng)

    for alpha in (0.1, 0.2, 0.3):
        b15 = double_conformal(scores, blocks, alpha)
        assert np.isfinite(b15.threshold), "uji akan hampa bila B15 trivial"
        assert b15.threshold >= hcp(scores, blocks, alpha).threshold


def test_b15_punya_dua_syarat_kelayakan_bukan_satu():
    """Temuan yang memperkuat C6.

    HCP hanya menuntut K+1 > 1/alpha. Double Conformal menuntut DUA hal sekaligus,
    karena mengambil kuantil (1-alpha/2) dua kali:

        K   + 1 >= 2/alpha   (lintas blok)
        N_k + 1 >= 2/alpha   (dalam blok)

    Syarat kedua tidak punya padanan di HCP. Jadi B15 dapat gagal total
    walau jumlah bloknya berlimpah -- selama tiap blok terlalu dangkal.
    """
    alpha = 0.2
    perlu = 2.0 / alpha  # = 10

    # Blok berlimpah (K=500) tetapi tiap blok terlalu dangkal (N=5 -> N+1=6 < 10).
    dangkal, blok_dangkal = hierarchical_scores(500, 5, np.random.default_rng(20))
    hasil_dangkal = double_conformal(dangkal, blok_dangkal, alpha)
    assert 5 + 1 < perlu
    assert hasil_dangkal.is_trivial
    assert hasil_dangkal.extra["blok_trivial"] == 500  # setiap blok jatuh ke +inf

    # HCP pada data yang sama justru berhasil: K=500 jauh melampaui 1/alpha.
    assert np.isfinite(hcp(dangkal, blok_dangkal, alpha).threshold)

    # Kedua syarat terpenuhi -> B15 berhingga.
    dalam, blok_dalam = hierarchical_scores(50, 20, np.random.default_rng(21))
    hasil_dalam = double_conformal(dalam, blok_dalam, alpha)
    assert 20 + 1 >= perlu and 50 + 1 >= perlu
    assert np.isfinite(hasil_dalam.threshold)
    assert hasil_dalam.extra["blok_trivial"] == 0


def test_subsampling_once_membuang_data_tetapi_tetap_deterministik_per_seed():
    scores, blocks = hierarchical_scores(30, 7, np.random.default_rng(8))

    a = subsampling_once(scores, blocks, 0.1, rng=np.random.default_rng(99))
    b = subsampling_once(scores, blocks, 0.1, rng=np.random.default_rng(99))

    assert a.threshold == b.threshold
    assert a.extra["n_terpakai"] == 30
    assert a.extra["n_dibuang"] == 30 * 7 - 30


def test_repeated_subsampling_mendekati_hcp_untuk_banyak_pengulangan():
    """Lee dkk. Proposisi 2: untuk B besar, Repeated Subsampling menghampiri HCP."""
    rng = np.random.default_rng(9)
    scores, blocks = hierarchical_scores(40, 5, rng)

    rs = repeated_subsampling(scores, blocks, 0.1, n_repeats=4000, rng=np.random.default_rng(10))
    target = hcp(scores, blocks, 0.1)

    sebaran = scores.std()
    assert abs(rs.threshold - target.threshold) < 0.25 * sebaran


def test_pooling_boleh_kurang_cakup_tetapi_dalam_batas_proposisi_1():
    """B13 memang dapat turun di bawah 1-alpha -- itu harga karena tak ada atom +inf.

    Batas sahnya: cakupan >= 1 - alpha - (1-alpha)/(K+1).
    Simulasi terukur memberi ~0,79 untuk alpha=0,2 dan K=20 (batas bawah 0,762).
    """
    k, n, alpha, trials = 20, 5, 0.2, 2000
    rng = np.random.default_rng(31337)
    blocks = np.repeat(np.arange(k), n)

    tertutup = 0
    for _ in range(trials):
        effect = rng.normal(0.0, 1.0, size=k)
        scores = (effect[:, None] + rng.normal(0.0, 0.3, size=(k, n))).ravel()
        s_test = rng.normal(0.0, 1.0) + rng.normal(0.0, 0.3)
        tertutup += s_test <= pooling_cdfs(scores, blocks, alpha).threshold

    cakupan = tertutup / trials
    batas_bawah = 1 - alpha - (1 - alpha) / (k + 1)
    galat_mc = 3.0 * np.sqrt(0.8 * 0.2 / trials)
    assert cakupan >= batas_bawah - galat_mc, f"melanggar Proposisi 1: {cakupan:.4f}"


def test_seluruh_metode_trivial_serempak_di_bawah_batas_kelayakan():
    rng = np.random.default_rng(11)
    scores, blocks = hierarchical_scores(k=8, n=50, rng=rng)  # alpha_min = 1/9 = 0,111

    for metode in (hcp, subsampling_once, double_conformal):
        assert metode(scores, blocks, alpha=0.05).is_trivial


# --------------------------------------------------------------------------
# C7 — uji diagnostik kecukupan blok
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("alpha", "diharapkan"),
    [(0.5, 1), (0.1, 9), (0.05, 19), (0.03, 33), (0.01, 99)],
)
def test_jumlah_blok_minimum(alpha, diharapkan):
    k = minimum_blocks(alpha)
    assert k == diharapkan
    assert alpha >= 1.0 / (k + 1)  # K blok cukup
    assert alpha < 1.0 / k  # K-1 blok tidak cukup


@pytest.mark.parametrize("alpha", [0.5, 0.2, 0.1, 0.05, 0.03, 0.01])
def test_jumlah_blok_minimum_cocok_dengan_perilaku_sebenarnya(alpha):
    """Angka yang dikembalikan harus cocok dengan K terkecil yang benar-benar
    menghasilkan ambang berhingga -- bukan sekadar hasil aljabar di atas kertas."""
    k = minimum_blocks(alpha)

    assert np.isfinite(hcp(np.arange(1.0, k + 1.0), np.arange(k), alpha).threshold)
    if k > 1:
        assert not np.isfinite(hcp(np.arange(1.0, k), np.arange(k - 1), alpha).threshold)


def test_diagnostik_mereproduksi_angka_ptbxl_untuk_situs():
    """Ukuran blok situs pada fold 9: K=40 -> alpha_min = 1/41 = 0,02439."""
    blocks = np.repeat(np.arange(40), 55)
    d = block_sufficiency(blocks, alpha=0.05, grouping="site")

    assert d.n_blocks == 40
    assert d.alpha_min == pytest.approx(0.02439, abs=1e-5)
    assert d.feasible
    assert not block_sufficiency(blocks, alpha=0.01).feasible


def test_diagnostik_memisahkan_validitas_dari_efisiensi():
    """Inti C6: blok sedikit-besar bisa GAGAL meski design effect lebih baik
    daripada blok banyak-besar yang justru LAYAK."""
    sedikit_besar = np.repeat(np.arange(11), 300)  # K=11, DEff = 300
    banyak_besar = np.repeat(np.arange(40), 800)  # K=40, DEff = 800

    a = block_sufficiency(sedikit_besar, alpha=0.05, grouping="device")
    b = block_sufficiency(banyak_besar, alpha=0.05, grouping="site")

    assert a.design_effect < b.design_effect  # a lebih efisien
    assert not a.feasible and b.feasible  # namun justru a yang mustahil


def test_design_effect_satu_untuk_blok_tunggal_seragam():
    d = block_sufficiency(np.arange(100), alpha=0.05)
    assert d.design_effect == pytest.approx(1.0)
    assert d.n_eff == pytest.approx(100.0)


# --------------------------------------------------------------------------
# C8 -- kelayakan per-label
# --------------------------------------------------------------------------


def hierarki_label(rng, n=400):
    """Induk `sering` memuat seluruh anak `jarang` -- hierarki sejati."""
    blocks = np.repeat(np.arange(n // 2), 2)
    jarang = rng.random(n) < 0.03
    sering = jarang | (rng.random(n) < 0.4)  # superset dari `jarang`
    return blocks, np.column_stack([sering, jarang])


def test_prop5_kelayakan_monoton_naik_menuju_akar():
    """K1(anak) <= K1(induk), sehingga alpha_min(anak) >= alpha_min(induk)."""
    blocks, labels = hierarki_label(np.random.default_rng(40))
    induk, anak = label_sufficiency(blocks, labels, 0.05, ["sering", "jarang"])

    assert np.all(labels[:, 1] <= labels[:, 0]), "prasyarat: anak subset induk"
    assert anak.n_blocks <= induk.n_blocks
    assert anak.alpha_min >= induk.alpha_min


def test_label_langka_dapat_tak_layak_meski_blok_global_berlimpah():
    """Inti C8: K1 global besar tidak menjamin K1(l) memadai."""
    blocks = np.arange(2000)
    labels = np.zeros((2000, 2), dtype=bool)
    labels[:, 0] = True  # muncul di seluruh 2.000 blok
    labels[:5, 1] = True  # hanya 5 blok

    umum, langka = label_sufficiency(blocks, labels, 0.05, ["umum", "langka"])
    assert umum.feasible and umum.n_blocks == 2000
    assert not langka.feasible and langka.n_blocks == 5
    assert langka.alpha_min == pytest.approx(1 / 6)


def test_koreksi_serentak_menaikkan_ambang_secara_linear():
    """Union bound: menjamin m label sekaligus menuntut alpha/m per label.

    Dipilih 50 blok per label agar berada TEPAT di antara kedua ambang:
    marginal butuh 19 blok (lolos), serentak m=4 butuh 79 blok (gagal).
    """
    blocks = np.arange(300)
    labels = np.zeros((300, 4), dtype=bool)
    labels[:50] = True

    marginal = label_sufficiency(blocks, labels, 0.05)
    serentak = label_sufficiency(blocks, labels, 0.05, simultaneous=True)

    assert marginal[0].blocks_required == 19
    assert serentak[0].blocks_required == 79  # = ceil(4/0,05) - 1
    assert all(d.alpha == pytest.approx(0.05 / 4) for d in serentak)

    assert all(d.feasible for d in marginal)
    assert not any(d.feasible for d in serentak)


def test_label_sufficiency_menolak_masukan_tak_sepadan():
    with pytest.raises(ValueError, match="tidak sepadan"):
        label_sufficiency(np.arange(10), np.ones((7, 2), dtype=bool), 0.05)
    with pytest.raises(ValueError, match="tidak muncul"):
        label_sufficiency(np.arange(10), np.zeros((10, 1), dtype=bool), 0.05)


# --------------------------------------------------------------------------
# Korelasi intra-blok -- masukan Prop. 2 dan E11b
# --------------------------------------------------------------------------


def efek_acak(k, n, rho_sejati, rng):
    """Model efek acak satu arah dengan ICC = rho_sejati tepat."""
    var_antar = rho_sejati
    var_dalam = 1.0 - rho_sejati
    efek = rng.normal(0.0, np.sqrt(var_antar), size=k)
    nilai = efek[:, None] + rng.normal(0.0, np.sqrt(var_dalam), size=(k, n))
    return nilai.ravel(), np.repeat(np.arange(k), n)


@pytest.mark.parametrize("rho_sejati", [0.0, 0.2, 0.5, 0.8])
def test_icc_memulihkan_rho_sejati(rho_sejati):
    nilai, blocks = efek_acak(600, 8, rho_sejati, np.random.default_rng(50))
    hasil = intraclass_correlation(nilai, blocks)
    assert hasil.icc == pytest.approx(rho_sejati, abs=0.05)


def test_icc_satu_bila_blok_sepenuhnya_redundan():
    """Semua titik identik di dalam blok -> tidak ada informasi tambahan."""
    efek = np.random.default_rng(51).normal(size=200)
    nilai = np.repeat(efek, 5)
    blocks = np.repeat(np.arange(200), 5)
    assert intraclass_correlation(nilai, blocks).icc == pytest.approx(1.0)


def test_n0_sama_dengan_ukuran_blok_saat_seragam():
    nilai, blocks = efek_acak(100, 7, 0.3, np.random.default_rng(52))
    assert intraclass_correlation(nilai, blocks).n0 == pytest.approx(7.0)


def test_icc_bekerja_pada_blok_tak_seragam():
    rng = np.random.default_rng(53)
    ukuran = rng.integers(1, 12, size=400)
    efek = rng.normal(0.0, np.sqrt(0.4), size=400)
    nilai = np.concatenate(
        [efek[b] + rng.normal(0.0, np.sqrt(0.6), size=ukuran[b]) for b in range(400)]
    )
    blocks = np.repeat(np.arange(400), ukuran)

    hasil = intraclass_correlation(nilai, blocks)
    assert hasil.icc == pytest.approx(0.4, abs=0.08)
    assert 1.0 < hasil.n0 < float(ukuran.max())


def test_ci_bootstrap_memuat_rho_sejati_dan_meresample_blok():
    nilai, blocks = efek_acak(300, 6, 0.35, np.random.default_rng(54))
    hasil = intraclass_correlation(
        nilai, blocks, n_bootstrap=300, rng=np.random.default_rng(55)
    )
    assert hasil.ci is not None
    assert hasil.ci[0] <= 0.35 <= hasil.ci[1]
    assert hasil.ci[0] < hasil.icc < hasil.ci[1]


def test_rho_terhadap_ambang_berbeda_dari_icc_skor_mentah():
    """Prop. 2 memakai ICC INDIKATOR 1{s<=t}, bukan ICC skor mentah."""
    skor, blocks = efek_acak(500, 6, 0.6, np.random.default_rng(56))
    mentah = intraclass_correlation(skor, blocks).icc
    pada_median = icc_at_threshold(skor, blocks, float(np.median(skor))).icc

    assert mentah == pytest.approx(0.6, abs=0.05)
    assert pada_median != pytest.approx(mentah, abs=1e-6)  # kuantitas berbeda
    assert 0.0 <= pada_median <= 1.0


def test_kurva_icc_melewati_beberapa_kuantil():
    skor, blocks = efek_acak(400, 5, 0.5, np.random.default_rng(57))
    kurva = icc_curve(skor, blocks)
    assert len(kurva) >= 4
    assert all(0.0 <= rho <= 1.0 for _, _, rho in kurva)
    assert [q for q, _, _ in kurva] == sorted(q for q, _, _ in kurva)


def test_icc_menolak_blok_tunggal_dan_blok_berisi_satu_titik():
    with pytest.raises(ValueError, match="butuh >= 2 blok"):
        intraclass_correlation(np.arange(5.0), np.zeros(5))
    with pytest.raises(ValueError, match="ragam intra-blok"):
        intraclass_correlation(np.arange(5.0), np.arange(5))
