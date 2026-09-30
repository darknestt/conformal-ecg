import sys
from pathlib import Path

# Paket belum di-install; tambahkan akar repositori agar `src` dapat diimpor.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
