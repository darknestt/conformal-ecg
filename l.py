import sys, urllib.request, urllib.error
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = {"User-Agent": "riset/1.0 (mailto:bloodszidan@gmail.com)"}
B = "https://physionet.org/files/challenge-2021/1.0.3/"
def coba(path, tampil=200):
    try:
        with urllib.request.urlopen(urllib.request.Request(B+path, headers=UA), timeout=45) as r:
            d = r.read().decode(errors="replace")
        print(f"OK  {path}  ({len(d):,} B)")
        print("    " + d[:tampil].replace("\n","\n    "))
        return d
    except urllib.error.HTTPError as e:
        print(f"{e.code} {path}")
    except Exception as e:
        print(f"ERR {path} {type(e).__name__}")
    return None
for p in ["RECORDS", "training/RECORDS", "training/chapman_shaoxing/RECORDS",
          "training/chapman_shaoxing/g1/RECORDS", "SHA256SUMS.txt"]:
    coba(p); print()
