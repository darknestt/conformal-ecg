"""Pengunduh MIT-BIH Noise Stress Test Database (NSTDB) langsung dari PhysioNet.

NSTDB tidak tersedia di bucket terbuka `physionet-open` (sudah diperiksa untuk
prefix `nstdb`, `nstdb/`, `noise`, `mit-bih-noise` — semuanya kosong), sehingga
harus diambil dari physionet.org. Endpoint `get-zip` membuat arsip secara dinamis
dan sangat lambat, maka skrip ini mengunduh berkas per berkas secara paralel.

Dataset kecil (67,7 MB, ~60 berkas) sehingga unduhan paralel jauh lebih cepat
daripada satu aliran ZIP.

Pemakaian:
    python scripts/download_nstdb.py
    python scripts/download_nstdb.py --workers 8
"""

from __future__ import annotations

import argparse
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = "https://physionet.org/files/nstdb/1.0.0"
USER_AGENT = "hicorc-research-downloader/1.0"

# Dua belas rekaman EKG bernoise: basis 118 dan 119, enam level SNR masing-masing.
SNR_SUFFIXES = ["24", "18", "12", "06", "00", "_6"]
ECG_RECORDS = [f"{base}e{snr}" for base in ("118", "119") for snr in SNR_SUFFIXES]
NOISE_RECORDS = ["bw", "ma", "em"]

EXTRA_FILES = [
    "ANNOTATORS",
    "RECORDS",
    "SHA256SUMS.txt",
    "nstdb.doc",
    "nstdb.txt",
    "nstdbgen",
    "nstdbgen-",
]


def build_file_list() -> list[str]:
    files: list[str] = []
    for rec in ECG_RECORDS:
        files += [f"{rec}.dat", f"{rec}.hea", f"{rec}.atr", f"{rec}.xws"]
    for rec in NOISE_RECORDS:
        files += [f"{rec}.dat", f"{rec}.hea", f"{rec}.hea-", f"{rec}.xws"]
    return files + EXTRA_FILES


def install_dns_cache() -> None:
    """Paksa IPv4 dan cache resolusi; resolver di jaringan ini gagal intermiten."""
    original = socket.getaddrinfo
    cache: dict[tuple[str, int], list] = {}

    def cached_ipv4(host, port, family=0, type=0, proto=0, flags=0):  # noqa: A002, ANN001, ANN202
        key = (host, port)
        if key not in cache:
            last: Exception | None = None
            for attempt in range(6):
                try:
                    cache[key] = original(host, port, socket.AF_INET, type, proto, flags)
                    break
                except socket.gaierror as exc:
                    last = exc
                    time.sleep(min(0.5 * 2**attempt, 5))
            else:
                raise last  # type: ignore[misc]
        return cache[key]

    socket.getaddrinfo = cached_ipv4


class Counter:
    def __init__(self, total: int) -> None:
        self.total = total
        self.done = 0
        self.bytes = 0
        self.failed: list[str] = []
        self.optional_missing: list[str] = []
        self.start = time.monotonic()
        self._lock = threading.Lock()

    def tick(self, name: str, nbytes: int, status: str) -> None:
        with self._lock:
            self.done += 1
            self.bytes += nbytes
            if status == "failed":
                self.failed.append(name)
            elif status == "missing":
                self.optional_missing.append(name)
            elapsed = max(time.monotonic() - self.start, 0.001)
            sys.stdout.write(
                f"\r    {self.done}/{self.total} berkas  "
                f"{self.bytes / 1024 / 1024:.1f} MB  "
                f"{self.bytes / 1024 / elapsed:.0f} KB/s   "
            )
            sys.stdout.flush()


def download(name: str, dest: Path, counter: Counter) -> None:
    out = dest / name
    if out.exists() and out.stat().st_size > 0:
        counter.tick(name, out.stat().st_size, "cached")
        return

    url = f"{BASE}/{name}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=180) as resp:  # noqa: S310
                data = resp.read()
            out.write_bytes(data)
            counter.tick(name, len(data), "ok")
            return
        except urllib.error.HTTPError as exc:
            if exc.code == 404:  # sebagian berkas pelengkap memang tidak ada
                counter.tick(name, 0, "missing")
                return
            if attempt == 3:
                counter.tick(name, 0, "failed")
                return
            time.sleep(2**attempt)
        except (urllib.error.URLError, TimeoutError, OSError):
            if attempt == 3:
                counter.tick(name, 0, "failed")
                return
            time.sleep(2**attempt)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "raw" / "nstdb",
    )
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    install_dns_cache()
    args.data_dir.mkdir(parents=True, exist_ok=True)

    files = build_file_list()
    print("\n  MIT-BIH Noise Stress Test Database v1.0.0")
    print("  -----------------------------------------")
    print(f"  Sumber  : {BASE}")
    print(f"  Tujuan  : {args.data_dir}")
    print(f"  Berkas  : {len(files)} ({len(ECG_RECORDS)} rekaman EKG + {len(NOISE_RECORDS)} rekaman noise)")
    print(f"  Paralel : {args.workers} koneksi\n")

    counter = Counter(len(files))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(download, f, args.data_dir, counter) for f in files]
        for fut in as_completed(futures):
            fut.result()

    print("\n")
    if counter.optional_missing:
        print(f"  [INFO] {len(counter.optional_missing)} berkas pelengkap tidak ada di server (normal):")
        print(f"         {', '.join(counter.optional_missing)}")
    if counter.failed:
        print(f"  [!] {len(counter.failed)} berkas gagal: {', '.join(counter.failed[:10])}")
        print("      Jalankan ulang perintah yang sama untuk mencoba lagi.")
        return 1

    total_mb = sum(p.stat().st_size for p in args.data_dir.glob("*")) / 1024 / 1024
    print(f"  [OK] Selesai. Total {total_mb:.1f} MB di {args.data_dir}")
    print("  Langkah berikutnya: python scripts/verify_datasets.py\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
