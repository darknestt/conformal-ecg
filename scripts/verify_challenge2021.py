"""Diagnostik C7 pada PhysioNet/CinC Challenge 2021 -- HEADER SAJA, tanpa sinyal.

Dataset ini dipakai sebagai KASUS KEGAGALAN STRUKTURAL, bukan sebagai dataset
generalisasi tingkat pasien. Pembedaan itu penting dan harus dipegang: header
Challenge 2021 TIDAK memuat pengenal pasien, sehingga klaim generalisasi
tingkat pasien tidak dapat didukung datanya.

Yang diuji adalah prasyarat S0 (theory.md par. 4.1):

    S0  Keteramatan: partisi sumber dependensi terukur terhadap metadata

S0 tidak pernah "gagal" -- ia TERPENUHI atau TAK TERAMATI. Bila tak teramati,
Prop. 0 menyatakan S2 TIDAK DAPAT DIPUTUSKAN: bukan gagal, bukan lolos. Untuk
jaminan yang dipakai pada keputusan klinis, "tidak dapat ditentukan" wajib
diperlakukan sebagai gagal.

Biaya: hanya berkas .hea (sekitar 760 B per rekaman) diunduh, bukan .mat.
Seluruh dataset 12,6 GB TIDAK diperlukan untuk vonis ini -- dan itu justru
demonstrasi utama nilai C7.

Tahap 1 (default) hanya MEMERIKSA struktur tanpa mengunduh massal.
Tahap 2 (--unduh) mengambil header untuk folder non-duplikat.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
KELUARAN = ROOT / "data" / "raw" / "challenge2021_headers"
BASE = "https://physionet.org/files/challenge-2021/1.0.3/"
UA = {"User-Agent": "riset/1.0 (mailto:bloodszidan@gmail.com)"}

# Folder ptb-xl DIKECUALIKAN: duplikat dataset utama, akan membatalkan klaim
# independensi bila ikut dihitung sebagai sumber terpisah.
FOLDER = ["cpsc_2018", "cpsc_2018_extra", "st_petersburg_incart", "ptb",
          "georgia", "chapman_shaoxing", "ningbo"]
DIKECUALIKAN = ["ptb-xl"]

for _a in (sys.stdout, sys.stderr):
    if hasattr(_a, "reconfigure"):
        _a.reconfigure(encoding="utf-8", errors="replace")


def ambil(path: str, timeout: int = 45, coba: int = 5) -> str | None:
    """PhysioNet memutus koneksi pada permintaan beruntun; perlu jeda dan coba-ulang."""
    for percobaan in range(coba):
        try:
            rq = urllib.request.Request(BASE + path, headers=UA)
            with urllib.request.urlopen(rq, timeout=timeout) as r:
                isi = r.read().decode(errors="replace")
            time.sleep(0.15)
            return isi
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(1.5 * (percobaan + 1))
        except (urllib.error.URLError, ConnectionResetError, TimeoutError, OSError):
            time.sleep(1.5 * (percobaan + 1))
    return None


def daftar_rekaman(folder: str) -> list[str]:
    """Cari RECORDS di beberapa lokasi; kembalikan nama relatif terhadap folder."""
    isi = ambil(f"training/{folder}/RECORDS")
    if isi:
        baris = [b.strip() for b in isi.splitlines() if b.strip()]
        # RECORDS tingkat folder dapat memuat nama subfolder ("g1/") alih-alih rekaman.
        if baris and all(b.endswith("/") for b in baris[:3]):
            semua = []
            for sub in baris:
                isi2 = ambil(f"training/{folder}/{sub}RECORDS")
                if isi2:
                    semua += [f"{sub}{b.strip()}" for b in isi2.splitlines() if b.strip()]
            return semua
        return baris
    return []


def daftar_global() -> dict[str, list[str]]:
    """RECORDS tingkat akar memuat jalur lengkap; dikelompokkan per folder sumber."""
    isi = ambil("RECORDS") or ambil("training/RECORDS")
    if not isi:
        return {}
    per: dict[str, list[str]] = {}
    for b in isi.splitlines():
        b = b.strip()
        if not b:
            continue
        bagian = b.replace("training/", "", 1).split("/")
        if len(bagian) >= 2:
            per.setdefault(bagian[0], []).append("/".join(bagian[1:]))
    return per


def medan_header(teks: str) -> dict[str, str]:
    return {m.group(1).lower(): m.group(2).strip()
            for m in re.finditer(r"^#\s*([A-Za-z]+)\s*:\s*(.*)$", teks, re.M)}


def perluas(folder: str, entri: list[str]) -> tuple[list[str], list[str]]:
    """RECORDS akar memuat jalur subfolder ('g1/'), bukan rekaman. Turun satu tingkat.

    Mengembalikan (rekaman, subfolder_gagal). Kegagalan WAJIB dikembalikan, bukan
    diabaikan -- subfolder yang gagal terambil menghasilkan hitungan kurang yang
    tampak sah.
    """
    if not entri or not all(e.endswith("/") for e in entri[:3]):
        return entri, []
    semua: list[str] = []
    gagal: list[str] = []
    for sub in entri:
        isi = ambil(f"training/{folder}/{sub}RECORDS")
        if isi:
            semua += [f"{sub}{b.strip()}" for b in isi.splitlines() if b.strip()]
        else:
            gagal.append(sub)
    return semua, gagal


def tahap1() -> dict:
    print("== TAHAP 1: struktur dan medan header (tanpa unduhan massal) ==\n")
    hasil = {}
    global_map = daftar_global()
    if global_map:
        print(f"  RECORDS tingkat akar terbaca: {len(global_map)} folder\n")

    total = 0
    ada_gagal = False
    for f in FOLDER:
        entri = global_map.get(f) or daftar_rekaman(f)
        n_sub = len(entri) if entri and entri[0].endswith("/") else 0
        rec, gagal = perluas(f, entri)
        hasil[f] = {"n_rekaman": len(rec), "n_subfolder": n_sub,
                    "subfolder_gagal": gagal, "contoh": rec[:2]}
        total += len(rec)
        ada_gagal |= bool(gagal)
        ket = f"   ({n_sub} subfolder)" if n_sub else ""
        peringatan = f"  <<< {len(gagal)} SUBFOLDER GAGAL: {gagal}" if gagal else ""
        print(f"  {f:<22} {len(rec):>7,} rekaman{ket}"
              + (f"   contoh: {rec[0]}" if rec else "   (RECORDS tidak terbaca)")
              + peringatan)
    print(f"\n  TOTAL non-duplikat: {total:,} rekaman")
    print(f"  Dikecualikan: {DIKECUALIKAN} (duplikat PTB-XL)")
    if ada_gagal:
        print("\n  ⚠️  HITUNGAN TIDAK LENGKAP — sebagian subfolder gagal terambil.")
        print("     Angka di atas adalah BATAS BAWAH, jangan dikutip sebagai final.")
    hasil["hitungan_lengkap"] = not ada_gagal
    hasil["total_rekaman_non_duplikat"] = total

    # Fallback: bila RECORDS tak terbaca, ambil satu header yang jalurnya sudah diketahui
    # agar pemeriksaan medan tetap berbasis berkas nyata, bukan asumsi.
    contoh = next((f for f in FOLDER if hasil[f]["contoh"]), None)
    teks = None
    if contoh:
        nama = hasil[contoh]["contoh"][0]
        teks = ambil(f"training/{contoh}/{nama}.hea")
        sumber_contoh = f"{contoh}/{nama}.hea"
    if teks is None:
        sumber_contoh = "chapman_shaoxing/g1/JS00001.hea"
        teks = ambil(f"training/{sumber_contoh}")

    if teks:
        medan = medan_header(teks)
        print(f"\n  Medan header pada {sumber_contoh} ({len(teks)} B):")
        for k, v in medan.items():
            print(f"    #{k:<6} = {v[:60]}")
        hasil["medan_header"] = list(medan)
        hasil["ukuran_header_B"] = len(teks)
        hasil["header_contoh"] = sumber_contoh

    print("\n== Vonis S0 ==")
    if "medan_header" not in hasil:
        # Tanpa satu pun header terbaca, TIDAK ADA vonis yang sah.
        print("  TIDAK ADA header yang berhasil dibaca.")
        print("  -> Vonis DITAHAN. Ketiadaan bukti bukan bukti ketiadaan;")
        print("     menyimpulkan S0 gagal di sini adalah kesalahan penalaran.")
        hasil["S0_vonis"] = "DITAHAN_tidak_ada_data"
        return hasil

    medan = set(hasil["medan_header"])
    punya_pasien = bool(medan & {"patient", "patientid", "subject", "id"})
    print(f"  Medan tersedia         : {sorted(medan)}")
    print(f"  Pengenal pasien ada?   : {'YA' if punya_pasien else 'TIDAK'}")
    if not punya_pasien:
        print("  -> S0 TAK TERAMATI untuk sumber dependensi 'pasien'.")
        print("     S0 tidak pernah 'gagal' -- ia terpenuhi atau tak teramati.")
        print("     Menurut Prop. 0, S2 karena itu TIDAK DAPAT DIPUTUSKAN:")
        print("     tak dapat diketahui apakah ada pasien yang menyumbang beberapa")
        print("     rekaman. Ini BUKAN bukti bahwa rekamannya independen.")
        print("     Aturan keputusan: tidak dapat ditentukan -> tidak lolos.")
    hasil["S0_vonis"] = "TERPENUHI" if punya_pasien else "TAK_TERAMATI"

    k = len([f for f in FOLDER if hasil[f]["n_rekaman"] > 0])
    if k:
        print(f"\n  Satu-satunya partisi teramati adalah SUMBER: K = {k}")
        print(f"  Karena K1 <= K, maka alpha_min >= 1/(K+1) = {1 / (k + 1):.4f}")
        print("  -> Dengan partisi teramati yang tersedia, dan di bawah kondisi")
        print("     kelayakan sampel-hingga yang dipakai penelitian ini, target")
        print(f"     alpha < {1 / (k + 1):.4f} tidak memenuhi syarat kelayakan.")
        print("     Ini BUKAN klaim bahwa dataset tak dapat dipakai untuk conformal.")
        hasil["K_sumber"] = k
        hasil["alpha_min_batas_bawah"] = 1.0 / (k + 1)
    else:
        print("\n  Jumlah sumber tidak terbaca -> batas alpha_min DITAHAN.")

    hasil["S0_pengenal_pasien"] = punya_pasien
    return hasil


def tahap2(pekerja: int) -> dict:
    KELUARAN.mkdir(parents=True, exist_ok=True)
    print("\n== TAHAP 2: unduh header saja ==")
    tugas = []
    for f in FOLDER:
        for nama in daftar_rekaman(f):
            tugas.append((f, nama))
    print(f"  {len(tugas):,} header akan diunduh "
          f"(~{len(tugas) * 760 / 1024 / 1024:.0f} MiB, bukan 12,6 GB)")

    def kerja(t):
        f, nama = t
        tujuan = KELUARAN / f / f"{pathlib.PurePosixPath(nama).name}.hea"
        if tujuan.exists():
            return True
        teks = ambil(f"training/{f}/{nama}.hea", timeout=60)
        if teks is None:
            return False
        tujuan.parent.mkdir(parents=True, exist_ok=True)
        sementara = tujuan.with_suffix(".partial")
        sementara.write_text(teks, encoding="utf-8")
        sementara.replace(tujuan)
        return True

    ok = gagal = 0
    with cf.ThreadPoolExecutor(max_workers=pekerja) as ex:
        for n, hasil in enumerate(ex.map(kerja, tugas), 1):
            ok += hasil
            gagal += not hasil
            if n % 2000 == 0:
                print(f"    {n:,}/{len(tugas):,}  ok={ok:,} gagal={gagal:,}", flush=True)
    print(f"  selesai: ok={ok:,} gagal={gagal:,}")
    return {"diunduh": ok, "gagal": gagal}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--unduh", action="store_true",
                    help="jalankan tahap 2 (unduh header); default hanya periksa")
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()

    hasil = tahap1()
    if args.unduh:
        hasil.update(tahap2(args.workers))

    keluaran = ROOT / "results" / "raw" / "challenge2021_s0.json"
    keluaran.parent.mkdir(parents=True, exist_ok=True)
    keluaran.write_text(json.dumps(hasil, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nTersimpan: {keluaran.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
