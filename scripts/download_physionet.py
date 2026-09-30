"""Pengunduh dataset PhysioNet lewat mirror AWS Open Data (paralel, dapat dilanjutkan).

Endpoint `get-zip` PhysioNet membuat arsip secara dinamis dan sangat lambat
(terukur ~33 KB/s). Bucket publik `physionet-open` menyajikan berkas statis dan
jauh lebih cepat. Skrip ini melisting bucket lewat REST API S3 (tanpa AWS CLI,
tanpa kredensial), lalu mengunduh secara paralel.

Untuk PTB-XL, folder `records500/` dilewati secara default karena penelitian ini
memakai 100 Hz sebagai konfigurasi utama. Ini memangkas unduhan dari ~3,0 GB
menjadi sekitar sepertiganya.

Pemakaian:
    python scripts/download_physionet.py                 # ptbxl + mitdb + nstdb
    python scripts/download_physionet.py ptbxl
    python scripts/download_physionet.py ptbxl --with-500hz
    python scripts/download_physionet.py --workers 32
    python scripts/download_physionet.py --dry-run
"""

from __future__ import annotations

import argparse
import http.client
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

BUCKET_HOST = "physionet-open.s3.amazonaws.com"
BUCKET_URL = f"https://{BUCKET_HOST}"
S3_NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
USER_AGENT = "hicorc-research-downloader/1.0"

_thread_state = threading.local()


def _get_conn() -> http.client.HTTPSConnection:
    """Koneksi HTTPS persisten per-thread; menghindari TLS handshake per berkas."""
    conn = getattr(_thread_state, "conn", None)
    if conn is None:
        conn = http.client.HTTPSConnection(BUCKET_HOST, timeout=90)
        _thread_state.conn = conn
    return conn


def _drop_conn() -> None:
    conn = getattr(_thread_state, "conn", None)
    if conn is not None:
        try:
            conn.close()
        except OSError:
            pass
    _thread_state.conn = None


def install_dns_cache() -> None:
    """Paksa IPv4 dan cache hasil resolusi.

    Resolver di jaringan ini gagal intermiten (`getaddrinfo failed`) dan AAAA
    lookup memperparahnya. Satu resolusi berhasil per host sudah cukup untuk
    seluruh sesi.
    """
    original = socket.getaddrinfo
    cache: dict[tuple[str, int], list] = {}

    def cached_ipv4(host, port, family=0, type=0, proto=0, flags=0):  # noqa: A002, ANN001, ANN202
        key = (host, port)
        if key in cache:
            return cache[key]
        last_exc: Exception | None = None
        for attempt in range(6):
            try:
                result = original(host, port, socket.AF_INET, type, proto, flags)
                cache[key] = result
                return result
            except socket.gaierror as exc:
                last_exc = exc
                time.sleep(min(0.5 * 2**attempt, 5))
        raise last_exc  # type: ignore[misc]

    socket.getaddrinfo = cached_ipv4


@dataclass(frozen=True)
class Dataset:
    key: str
    name: str
    prefix: str
    dest: str
    exclude: tuple[str, ...] = ()


DATASETS: dict[str, Dataset] = {
    "ptbxl": Dataset(
        key="ptbxl",
        name="PTB-XL v1.0.3",
        prefix="ptb-xl/1.0.3/",
        dest="ptbxl",
        exclude=("records500/",),
    ),
    "mitdb": Dataset(
        key="mitdb",
        name="MIT-BIH Arrhythmia v1.0.0",
        prefix="mitdb/1.0.0/",
        dest="mitdb",
    ),
    "nstdb": Dataset(
        key="nstdb",
        name="MIT-BIH Noise Stress Test v1.0.0",
        prefix="nstdb/1.0.0/",
        dest="nstdb",
    ),
}


def human(size: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:,.1f} {unit}"
        size /= 1024
    return f"{size:,.1f} GB"


def list_objects(prefix: str) -> list[tuple[str, int]]:
    """Ambil seluruh (key, size) di bawah prefix, menangani paginasi S3."""
    objects: list[tuple[str, int]] = []
    token: str | None = None

    while True:
        params = {"list-type": "2", "prefix": prefix, "max-keys": "1000"}
        if token:
            params["continuation-token"] = token
        url = f"{BUCKET_URL}/?{urllib.parse.urlencode(params)}"

        root = None
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
                    root = ET.fromstring(resp.read())
                break
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                if attempt == 4:
                    raise
                print(f"      (percobaan {attempt + 1} gagal: {exc}; mencoba lagi)")
                time.sleep(2**attempt)

        if root is None:
            break

        for item in root.findall("s3:Contents", S3_NS):
            key_el = item.find("s3:Key", S3_NS)
            size_el = item.find("s3:Size", S3_NS)
            if key_el is None or key_el.text is None:
                continue
            size = int(size_el.text) if size_el is not None and size_el.text else 0
            if size > 0:  # lewati penanda folder
                objects.append((key_el.text, size))

        truncated = root.findtext("s3:IsTruncated", default="false", namespaces=S3_NS)
        if truncated.lower() != "true":
            break
        token = root.findtext("s3:NextContinuationToken", namespaces=S3_NS)
        if not token:
            break

    return objects


class Progress:
    """Pelacak kemajuan yang aman untuk banyak thread."""

    def __init__(self, total_files: int, total_bytes: int) -> None:
        self.total_files = total_files
        self.total_bytes = total_bytes
        self.done_files = 0
        self.done_bytes = 0
        self.failed: list[str] = []
        self.start = time.monotonic()
        self._lock = threading.Lock()
        self._last_render = 0.0

    def update(self, nbytes: int, error: str | None = None) -> None:
        with self._lock:
            self.done_files += 1
            self.done_bytes += nbytes
            if error:
                self.failed.append(error)
            now = time.monotonic()
            if now - self._last_render > 0.5 or self.done_files == self.total_files:
                self._last_render = now
                self._render()

    def _render(self) -> None:
        elapsed = max(time.monotonic() - self.start, 0.001)
        rate = self.done_bytes / elapsed
        pct = 100 * self.done_bytes / self.total_bytes if self.total_bytes else 100.0
        remaining = (self.total_bytes - self.done_bytes) / rate if rate > 0 else 0
        bar = "#" * int(pct / 2.5)
        sys.stdout.write(
            f"\r    [{bar:<40}] {pct:5.1f}%  "
            f"{self.done_files}/{self.total_files} berkas  "
            f"{human(self.done_bytes)}  {human(rate)}/s  sisa ~{remaining / 60:.1f} mnt   "
        )
        sys.stdout.flush()


def download_one(key: str, size: int, out_path: Path, progress: Progress) -> None:
    if out_path.exists() and out_path.stat().st_size == size:
        progress.update(size)
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(out_path.suffix + ".part")
    path = "/" + urllib.parse.quote(key)

    for attempt in range(5):
        try:
            conn = _get_conn()
            conn.request("GET", path, headers={"User-Agent": USER_AGENT, "Connection": "keep-alive"})
            resp = conn.getresponse()
            body = resp.read()  # wajib dibaca penuh agar koneksi bisa dipakai ulang
            if resp.status != 200:
                raise OSError(f"HTTP {resp.status}")
            if len(body) != size:
                raise OSError(f"ukuran tidak cocok: {len(body)} != {size}")
            tmp.write_bytes(body)
            tmp.replace(out_path)
            progress.update(size)
            return
        except (OSError, http.client.HTTPException, TimeoutError) as exc:
            _drop_conn()
            if attempt == 4:
                tmp.unlink(missing_ok=True)
                progress.update(size, error=f"{key}: {exc}")
                return
            time.sleep(min(2**attempt, 8))


def fetch_dataset(ds: Dataset, root: Path, workers: int, dry_run: bool) -> bool:
    print(f"\n==> {ds.name}")
    print(f"    Melisting s3://physionet-open/{ds.prefix} ...")

    try:
        objects = list_objects(ds.prefix)
    except Exception as exc:  # noqa: BLE001
        print(f"    [GAGAL] Tidak dapat melisting bucket: {exc}")
        return False

    if not objects:
        print("    [GAGAL] Tidak ada objek ditemukan. Periksa prefix.")
        return False

    kept, skipped_bytes, skipped_n = [], 0, 0
    for key, size in objects:
        rel = key[len(ds.prefix) :]
        if any(rel.startswith(x) for x in ds.exclude):
            skipped_bytes += size
            skipped_n += 1
            continue
        kept.append((key, size, root / ds.dest / rel))

    total = sum(s for _, s, _ in kept)
    print(f"    Ditemukan {len(objects):,} objek; akan diunduh {len(kept):,} ({human(total)})")
    if skipped_n:
        print(f"    Dilewati  {skipped_n:,} objek ({human(skipped_bytes)}) karena: {', '.join(ds.exclude)}")

    if dry_run:
        print("    [DRY-RUN] Tidak ada yang diunduh.")
        return True

    progress = Progress(len(kept), total)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(download_one, k, s, p, progress) for k, s, p in kept]
        for fut in as_completed(futures):
            fut.result()
    _drop_conn()

    print()
    if progress.failed:
        print(f"    [!] {len(progress.failed)} berkas gagal:")
        for err in progress.failed[:10]:
            print(f"        {err}")
        if len(progress.failed) > 10:
            print(f"        ... dan {len(progress.failed) - 10} lainnya")
        print("    Jalankan ulang perintah yang sama untuk mencoba lagi (berkas lengkap dilewati).")
        return False

    print(f"    [OK] Selesai -> {root / ds.dest}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "datasets",
        nargs="*",
        choices=[*DATASETS, []],
        default=list(DATASETS),
        help="Dataset yang diunduh (default: semua)",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "raw",
    )
    parser.add_argument("--workers", type=int, default=16, help="Jumlah unduhan paralel")
    parser.add_argument(
        "--with-500hz",
        action="store_true",
        help="Ikut unduh PTB-XL records500/ (menambah ~2 GB, tidak dipakai penelitian ini)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Hanya tampilkan rencana")
    args = parser.parse_args()

    install_dns_cache()
    selected = args.datasets or list(DATASETS)

    print("\n  Pengunduh Dataset PhysioNet - mirror AWS Open Data")
    print("  -------------------------------------------------")
    print(f"  Tujuan  : {args.data_dir}")
    print(f"  Paralel : {args.workers} koneksi")
    print(f"  Dataset : {', '.join(selected)}")

    args.data_dir.mkdir(parents=True, exist_ok=True)

    ok = True
    for name in selected:
        ds = DATASETS[name]
        if name == "ptbxl" and args.with_500hz:
            ds = Dataset(ds.key, ds.name, ds.prefix, ds.dest, exclude=())
        ok &= fetch_dataset(ds, args.data_dir, args.workers, args.dry_run)

    print("\n  Selesai." if ok else "\n  Selesai dengan kesalahan.")
    if not args.dry_run:
        print("  Langkah berikutnya: python scripts/verify_datasets.py\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
