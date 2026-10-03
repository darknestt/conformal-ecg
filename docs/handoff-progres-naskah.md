# Catatan Serah Terima: Progres Naskah Jurnal

> Dokumen ini merangkum seluruh progres, keputusan, dan perubahan naskah sampai **3 Oktober 2026**
> (commit `37d11bd`). Tujuannya agar pekerjaan bisa dilanjutkan atau direvisi oleh AI agent lain
> tanpa kehilangan konteks. Baca bagian **2 (Aturan Wajib)** sebelum mengubah apa pun.

---

## 1. Identitas Naskah

| Hal | Isi |
|---|---|
| Judul | *Block-Level Feasibility of Conformal Calibration on Clinical ECG Data: An Empirical Audit* |
| Jenis | Audit empiris + teori kelayakan. **Tidak** mengusulkan metode conformal baru. |
| Target | Jurnal internasional bereputasi (Scopus Q1). **Jurnal dan template belum ditentukan** (arahan dosen pembimbing). |
| Bahasa naskah | Inggris (ejaan Amerika) |
| Bahasa komunikasi dengan pengguna | Indonesia |
| Repo | `github.com/darknestt/conformal-ecg` (**privat**), branch `main` |
| Berkas naskah Word | `docs/paper/manuscript-draft.docx` (dihasilkan otomatis, jangan diedit manual) |
| Status terakhir | 19 halaman, 9 gambar, 9 tabel, 35 rujukan, abstrak 246 kata, ±10.845 kata (hitungan Word) |

### Pertanyaan riset
- **RQ1**: Dapatkah jaminan coverage tingkat blok (hierarchical conformal prediction, HCP) ditegakkan pada sumber data EKG klinis pada tingkat galat lazim?
- **RQ2**: Apakah mengabaikan struktur blok menurunkan coverage, dan melalui mekanisme apa?

### Tiga kontribusi (sesuai §1)
1. **Audit kelayakan berbasis metadata saja** (RQ1; §3, §5.1).
2. **Atribusi under-coverage ke dependensi melalui repetisi** (RQ2; §5.2–§5.4).
3. **Dua peringatan untuk evaluasi metode conformal pada data berklaster** (§5.3, §6.2): keunggulan HCP sebagian besar mekanis; interval dari split berulang bukan interval populasi.

---

## 2. Aturan Wajib (jangan dilanggar)

1. **Jangan pernah mengarang** dataset, tautan, DOI, angka, atau paper. Bila tidak bisa diverifikasi, tulis **"BELUM TERVERIFIKASI"**.
2. **Jangan menurunkan mutu naskah**; setiap perubahan harus mempertahankan atau menaikkan nilai untuk Scopus Q1.
3. **Draf harus netral jurnal** (arahan dosen): jangan menambahkan Highlights, Ethics Statement, CRediT, Competing Interest, Funding, deklarasi AI generatif, atau placeholder DOI. Bagian ini akan diisi dosen saat submisi.
4. **Jangan memakai nomor baris** di docx (pengguna tidak menyukainya).
5. **Aturan narasi float**: kalimat terakhir sebelum setiap Gambar/Tabel harus **menyebut** gambar/tabel itu dan apa isinya; tafsiran ditulis sesudahnya.
6. **Pernyataan formal** (Proposition 1–3 + bukti, Corollary 1–2, Definition, "Scope of Corollary 2") dan persamaan (1)–(6), (A.1) **tidak boleh diubah isinya**.
7. Kalimat kondisional inti PTB-XL **wajib kata per kata**: *"If patient, site, nurse, and device are all treated as dependence sources, no admissible calibration grouping exists at any conventional α."*
8. **Jangan menyebut hasil split-level sebagai "significant"** untuk populasi. Interval Monte Carlo hanya berlaku bersyarat pada 22 rekaman DS2.
9. **Jangan menjual "count subjects, not beats" sebagai temuan kita** (sudah ditunjukkan oleh Sim & Kim [E6]). Pembeda kita: join sumber bersilang, K₁ per label, null permutasi + faktorial, dose–response design effect.
10. **Protokol analisis tidak pernah dibekukan atau diregistrasi publik.** Naskah memakai frasa: *"internal, version-controlled analysis protocol; not publicly registered or formally frozen"*. Jangan menulis "pre-registered".
11. **Corollary 2 hanya dibuktikan untuk HCP**; perluasan ke konstruksi Dunn et al. dinyatakan sebagai pertanyaan terbuka.
12. Ulasan dari AI lain: **verifikasi dulu** setiap klaimnya ke docx/sumber. Contoh: klaim "rujukan [39]–[47] hilang" dan "gambar masih placeholder" ternyata **salah** (AI lain membaca teks PDF yang terpotong).
13. Rujukan baru: verifikasi metadata via Crossref/OpenAlex lebih dulu, lalu jalankan `python .\scripts\verify_scopus.py`.
14. **Tiga tingkat bukti** (§1) harus konsisten di seluruh naskah: yang *terbukti* (Prop. 1–3, Cor. 1–2), yang *teramati* pada rekaman yang diaudit (§5), dan yang *tidak diklaim* (tanda defisit MIT-BIH di tingkat populasi; peran kausal design effect). Jangan menulis "ignoring blocks causes under-coverage" sebagai klaim umum.
15. Istilah *mechanical* = bagian selisih B12−B1 yang bertahan di bawah null yang mempertahankan geometri blok; berasal dari koreksi blok-hingga, **bukan** berarti HCP tidak valid.

---

## 3. Lingkungan dan Cara Membangun

### Lingkungan
- Windows, PowerShell 5.1, Python 3.14.6, PyTorch 2.14.0 (CPU), NumPy 2.5.2, SciPy 1.18.1, scikit-learn 1.9.1, pandas 3.0.6, wfdb 4.3.1; CPU Intel Core i5-7200U.
- Set `$env:PYTHONIOENCODING='utf-8'` sebelum menjalankan skrip (keluaran memuat karakter Unicode).

### Membangun naskah Word
```powershell
$env:PYTHONIOENCODING='utf-8'
python .\scripts\make_figures.py     # semua gambar dari results/raw/*.json
python .\scripts\build_docx.py       # -> docs/paper/manuscript-draft.docx
```
- Bila docx sedang terbuka di Word, `build_docx.py` menampilkan galat "sedang terbuka". Tutup Word dulu, atau bangun ke lokasi lain: `python .\scripts\build_docx.py "$env:TEMP\naskah_cek.docx"`.

### Pemeriksaan wajib sebelum commit
```powershell
python -m pytest tests/ -q              # harus 77 passed
python .\scripts\check_consistency.py   # harus "Seluruh angka cocok dengan data"
```

### Konvensi commit
- Pesan commit dalam bahasa Indonesia. Push ke `origin main`. Exit code 1 setelah `git push ... | Select-String` biasanya hanya karena stderr; cek dengan `git status -sb`.

---

## 4. Struktur Sumber Naskah

Semua sumber ada di `docs/paper/`. **Edit file `.md`, lalu bangun ulang docx.** Blok `## Catatan penyusunan` (bahasa Indonesia) di akhir tiap file **tidak** ikut ke docx.

| File | Isi |
|---|---|
| `abstract-conclusion.md` | Abstract, Keywords, §7 Conclusion, Data and Code Availability |
| `sec1.md` | §1 Introduction (RQ1/RQ2, 3 kontribusi, **Fig. 1**) |
| `sec2.md` | §2 Related Work (2.1 dependensi & data hierarkis; 2.2 multi-label, klinis, EKG; "Position of this study") |
| `sec3.md` | §3 Problem Formulation and HCP Feasibility (Prop. 1–3, Cor. 1–2, persamaan (1)–(6), **Fig. 2**) |
| `sec4.md` | §4 Audit Design (dataset, protokol, model, statistik, reproduksibilitas; **Fig. 3**, Tabel 4.1–4.2) |
| `sec5.md` | §5 Results (5.1–5.5; **Fig. 4–9**, Tabel 5.1–5.6) |
| `sec6.md` | §6 Discussion (6.1 temuan, 6.2 dua pitfall, 6.3 implikasi + 4 cek praktis, 6.4 keterbatasan) |
| `appendix.md` | Appendix A (A.1 kasus batas, A.2 varians (A.1), A.3 bobot sama + contoh kontra), B (kesimpulan sementara MIT-BIH, Tabel B.1), C (observabilitas Challenge 2021) |
| `references.json` | Metadata rujukan (Crossref/arXiv/DataCite), dikunci dengan kode seperti `A0`, `E6` |
| `figures/` | PNG 300 dpi hasil `make_figures.py` |

### Konvensi penulisan di sumber `.md`
- Sitasi memakai **kode**: `[A0]`, `[I1, A13]`, `[A0, Thm. 1]`. Builder mengubahnya menjadi `[n]` menurut urutan kemunculan pertama, dan menyusun daftar pustaka gaya numerik dari `references.json`.
- Tabel: `**Table 5.4.** Caption...` → di docx menjadi "Table 6" (nomor Arab berurutan). Rujukan "Table 5.4" di teks ikut diganti otomatis.
- Gambar: `![**Fig. n.** Caption](figures/figN_nama.png)`. **Nomor gambar ditulis manual**; bila menyisipkan gambar, nomori ulang caption, rujukan teks, nama file, dan pemanggilan di `make_figures.py`.
- Lebar gambar ditentukan nama file: yang mengandung `join_schematic`, `block_geometry`, `feasibility_frontier`, `dose_response` = 3,4 in (satu kolom); lainnya 5,8 in.
- **Caption tabel tidak boleh memuat `$math$`** (Word memindahkannya ke depan label tabel).
- Jangan pakai `\tfrac` (di Word jadi 1/K_1+1 tanpa kurung).
- Baris yang diawali "(4)" akan dianggap daftar bernomor oleh pandoc; hindari.

### Gaya docx (diatur `scripts/build_docx.py`)
- Times New Roman, isi 10 pt, caption 9 pt; spasi paragraf 0 pt sebelum / 4 pt sesudah (bawaan pandoc 9/9 pt membuang ±3 halaman); rata kiri-kanan.
- Baris tabel tidak boleh terpotong; tabel ≤7 baris disatukan; paragraf sesudah tabel diberi jarak 6 pt.
- Tanpa nomor baris.

---

## 5. Isi Naskah Saat Ini

### Gambar (9)
| No. | File | Isi | Bagian |
|---|---|---|---|
| Fig. 1 | `fig1_audit_workflow.png` | Alur audit dua tahap (gaya panel, warna lembut; meniru gambar referensi ResearchGate) | §1 |
| Fig. 2 | `fig2_join_schematic.png` | Skema Proposition 2: 8 rekaman hipotetis, join pasien × perangkat | §3.3 |
| Fig. 3 | `fig3_block_geometry.png` | **Baru**: ukuran blok terurut (log–log) PTB-XL patient/site/nurse/device dan MIT-BIH record; garis K_min(0,05)=19 | §4.1 |
| Fig. 4 | `fig4_feasibility_frontier.png` | Batas kelayakan α_min = 1/(K₁+1) | §5.1 |
| Fig. 5 | `fig5_label_feasibility.png` | Blok kalibrasi per label hierarki PTB-XL | §5.1 |
| Fig. 6 | `fig6_coverage.png` | Coverage − nominal, B1 vs B12 | §5.2 |
| Fig. 7 | `fig7_attribution.png` | (a) efek faktorial 2×2; (b) selisih B12−B1 asli vs permutasi | §5.3 |
| Fig. 8 | `fig8_dose_response.png` | Defisit B1 vs design effect | §5.4 |
| Fig. 9 | `fig9_robustness.png` | (a) defisit per backbone + CI jackknife; (b) sensitivitas checkpoint | §5.5 |

Fungsi di `make_figures.py` (urutan loop): `fig1_alur, fig_join, fig_geometri, fig2_kelayakan, fig4_label, fig5_cakupan, fig_atribusi, fig6_dosis, fig7_backbone` (nama fungsi tidak sama dengan nomor gambar; lihat nama file yang disimpan).

### Tabel (9)
| Docx | Sumber | Isi |
|---|---|---|
| Table 1 | 4.1 | Peran & geometri blok tiga dataset |
| Table 2 | 4.2 | Prosedur statistik |
| Table 3 | 5.1 | Kelayakan HCP per pengelompokan (PTB-XL fold 9) |
| Table 4 | 5.2 | Label yang gagal Proposition 3 |
| Table 5 | 5.3 | Coverage dan ukuran set |
| Table 6 | 5.4 | Defisit B1 vs null permutasi: Monte Carlo + jackknife level rekaman |
| Table 7 | 5.5 | Korelasi Spearman (deskriptif) |
| Table 8 | 5.6 | Diskriminasi per backbone |
| Table 9 | B.1 | Kesimpulan sementara MIT-BIH dan kontrol yang membatalkannya |

### Persamaan
(1) ambang HCP, (2) jaminan Lee et al., (3) syarat kelayakan α ≥ 1/(K₁+1), **(4) DEff block/pooled**, **(5) superset coverage**, **(6) label-conditional**, (A.1) varians. Dinomori ulang menurut urutan kemunculan pada 3 Okt 2026 (sebelumnya DEff = (6)).

### Angka kunci (sudah diverifikasi ke JSON; jangan diubah tanpa cek ulang)
- PTB-XL v1.0.3: 21.799 rekaman, 18.869 pasien (1,155 rekaman/pasien; 88,8% satu rekaman); 51 site, 12 nurse, 11 device; fold 9 = 2.183 rekaman.
- MIT-BIH v1.0.0: 44 rekaman non-pacu, 100.693 detak; DS1/DS2 22 rekaman masing-masing; kalibrasi K₁ = 11 → α_min = 1/12.
- Join empat sumber PTB-XL → 1 blok; 24 dari 44 kode SCP gagal di α = 0,05; 43/44 dengan Bonferroni.
- Defisit B1 vs null permutasi (SmallECGNet, Monte Carlo): +1,49 / +2,21 / +2,37 pp (α = 0,10/0,15/0,20).
- Jackknife level rekaman: defisit 0,60–1,83 pp, setengah-lebar CI 3,7–5,7 pp, semua CI memuat nol (Holm p ≥ 0,59).
- Coverage berbobot blok: defisit 1,43–2,61 pp; HCP berbobot blok ≥ 1−α di semua sel.
- Porsi mekanis selisih B12−B1: 81–107% (backbone utama), 75–110% (tiga backbone).
- Faktorial: klaster −1,22/−1,55/−1,49 pp; ketimpangan −0,44/−0,26/−0,27 pp; interaksi −0,79/−0,54/−0,52 pp.
- Spearman DEff (12 titik): 0,84 / 0,80 / 0,85. ICC PTB-XL 0,352; DEff PTB-XL 1,02 vs MIT-BIH 703,93.
- Backbone: SmallECGNet (±0,10 M param), ResNet1D-34 (7,2 M), ResNet1D-50 (16,0 M).

### Daftar rujukan (35) — nomor di docx ↔ kode di sumber
| No. | Kode | Penulis (tahun) | Venue |
|---|---|---|---|
| [1] | F1 | Strodthoff (2021) | IEEE J. Biomed. Health Inform. |
| [2] | H1 | Wagner (2020) | Sci Data |
| [3] | G1 | Lambert (2024) | Artificial Intelligence in Medicine |
| [4] | G2 | Lekadir (2025) | BMJ |
| [5] | A11 | Fontana (2023) | Bernoulli |
| [6] | E1 | Vazquez (2022) | J Healthc Inform Res |
| [7] | E7 | El Allam (2026) | Biomedical Signal Processing and Control |
| [8] | E9 | El Allam (2026) | Measurement |
| [9] | E8 | Kinalioğlu (2026) | Physiol. Meas. |
| [10] | E6 | Sim (2026) | IEEE Access |
| [11] | A1 | Barber (2023) | Ann. Statist. |
| [12] | A0 | Lee (2026) | ACM J. Data Sci. |
| [13] | A0b | Dunn (2023) | J. Am. Stat. Assoc. |
| [14] | H2 | Wagner (2022) | PhysioNet |
| [15] | H3 | Moody (1992) | PhysioNet |
| [16] | H5 | Reyna (2022) | PhysioNet |
| [17] | A4 | Lei (2021) | J. R. Stat. Soc. B |
| [18] | A7 | Mao (2024) | J. Am. Stat. Assoc. |
| [19] | A8 | Lunde (2025) | J. Am. Stat. Assoc. |
| [20] | A3 | Bhattacharyya (2026) | Electron. J. Statist. |
| [21] | B1 | Papadopoulos (2026) | Phil. Trans. R. Soc. A |
| [22] | B2 | Baheri (2025) | Results in Applied Mathematics |
| [23] | F2 | Dias (2021) | Comput. Methods Programs Biomed. |
| [24] | F10 | Li (2022) | Comput. Methods Programs Biomed. |
| [25] | F3 | Wang (2021) | Neurocomputing |
| [26] | C1 | Angelopoulos (2026) | Phil. Trans. R. Soc. A |
| [27] | C4 | Xu (2023) | IEEE Trans. Pattern Anal. Mach. Intell. |
| [28] | E5 | Shahbazi (2026) | Sci Rep |
| [29] | I2 | White (2005) | Clinical Trials |
| [30] | I1 | Kerry (2001) | Statist. Med. |
| [31] | A13 | Zhan (2021) | PLoS ONE |
| [32] | P1 | Noonan (2026) | arXiv |
| [33] | P2 | Zheng (2026) | arXiv |
| [34] | A12 | Ding (2023) | NeurIPS 36 |
| [35] | A9 | Marques F. (2025) | Statistics & Probability Letters |

**Dibuang pada 3 Okt 2026 (arahan dosen, 47 → 35)**: A2, B3, B5, B6, B7 (preprint), C2, D2, D4, E2, E3, F5, F6. Metadatanya masih ada di `references.json` tetapi tidak dikutip; builder hanya mencantumkan rujukan yang dikutip. **Jangan buang**: A0, A0b (teori inti), H1–H5 (dataset, wajib lisensi), E6–E9 (pembanding terdekat), P1, P2, I1, I2, A9, A12 (atribusi teori).

---

## 6. Riwayat Pekerjaan (kronologis)

| Commit | Ringkasan |
|---|---|
| `2bbdbec` | v4: restrukturisasi 11 → 7 bab + lampiran |
| `351fe87` | v5: aturan narasi sebelum setiap float |
| `3edc1f0` | v6: gambar skema join dan atribusi |
| `849c156` | v7: parafrase penuh (kemiripan 8-gram 70% → 9%); Fig. robustness dua panel |
| `261e1c1` | Pra-spesifikasi jackknife level rekaman **sebelum** dijalankan |
| `7a6684f`, `ac7b39f` | v8 (P1): hasil jackknife; naskah dibingkai ulang (hapus "significant/pre-registered"; estimand coverage; Corollary 2 hanya HCP) |
| `b5904a5` | P2: rincian reproduksibilitas dicek ke kode (versi software/data, loss, batch) |
| `647a1e5` | P3–P5: pemadatan struktural, abstrak ≤ 250 kata |
| `8852d79` | Fig. 1 = alur audit dua tahap di §1; skema join menjadi Fig. 2 |
| `9be36df` | Fig. 1 didesain ulang meniru gambar referensi (panel berbingkai, judul pil, hub-satelit, siklus) dengan palet lembut |
| `1fc1c60`, `a407735` | Tanggapan review AI lain: persamaan dinomori urut; §4.3 menjelaskan backbone sengaja tidak dituning untuk diskriminasi |
| `4d143e2` | (Sempat) format Elsevier/AIIM: Highlights, deklarasi, nomor baris |
| `17f8901` | **Dibatalkan** ke draf netral jurnal (arahan dosen): Highlights & bagian administratif dihapus |
| `8ce38ae` | Pemadatan ke 20 halaman: nomor baris dihapus, spasi paragraf diperbaiki, huruf 10 pt, prosa dipadatkan & diparafrasekan (kemiripan 12%), **Fig. 3 baru** (`experiments/block_geometry.py`), gambar lama 3–8 → 4–9 |
| `37d11bd` | Rujukan 47 → 35; caption 694 → 434 kata; 19 halaman |
| (sesudah `f624660`) | Tanggapan review AI lain (7 titik serangan reviewer): §1 memisahkan tiga tingkat bukti (terbukti / teramati / tidak diklaim); §2 "Position" menyebut tambahan relatif terhadap Lee et al.; §5.3 judul jadi "Attributing the deficit to dependence" dan istilah *mechanical* didefinisikan; §5.4 dose–response ditegaskan mekanistik, bukan validasi eksternal/kausal; §6.1 klaim repetisi dibatasi pada dua sumber yang diaudit; §6.4 riwayat analisis dibingkai sebagai jejak audit |

### Keputusan penting yang sudah final
- **Jurnal target belum dipilih.** AIIM (Elsevier) sempat menjadi kandidat (terverifikasi aktif di daftar Scopus Agustus 2026), tetapi dibatalkan karena dosen meminta draf netral. Kuartil SJR kandidat **BELUM TERVERIFIKASI** (situs SCImago/ScienceDirect memblokir akses otomatis).
- Fig. 3 tetap **satu kolom** (pilihan pengguna); akan pas di template dua kolom.
- Klaim "B12 memperbaiki B1" **dicabut** (75–110% mekanis). Bukti yang dipakai: defisit B1 vs null permutasi.

---

## 7. Pekerjaan yang Masih Tertunda

### Diisi dosen/penulis saat submisi (jangan dimasukkan ke draf)
1. DOI/identitas arsip kode (Data and Code Availability saat ini hanya menyatakan akan diarsipkan sebelum publikasi).
2. Pernyataan etika institusi (draf hanya menyebut data publik ter-de-identifikasi, tanpa data baru).
3. CRediT, competing interest, funding.
4. Deklarasi penggunaan AI generatif bila jurnal mewajibkan (harus jujur menyebut alat dan tujuannya).
5. Highlights/graphical abstract bila jurnal memintanya.

### Tindakan pengguna
- **R5**: jadikan repo publik atau arsipkan di Zenodo (perlu persetujuan pengguna; naskah menyatakan kode dirilis).
- **R6**: baca teks lengkap rujukan **I1, I2, P1** untuk memastikan klaim yang merujuknya sesuai isi paper (F5 sudah tidak dikutip).
- Pilih jurnal target → sesuaikan ke template (gaya rujukan, batas kata, struktur abstrak) → penghalusan bahasa (P6).
- Masukan dosen atas draf 19 halaman.

### Catatan teknis
- PTB-XL **fold 10 belum pernah disentuh** (cadangan evaluasi konfirmatori). Jangan dipakai tanpa keputusan eksplisit.
- Scheduled task Windows `Sqopus-BackboneInvariance` pernah dibuat untuk melanjutkan pelatihan setelah restart; pelatihan sudah selesai, cek dan hapus bila masih ada.
- Ada ruang kosong kecil di bawah beberapa halaman (gambar pindah halaman). Wajar untuk draf Word.

---

## 8. Skrip Bantu

### Di dalam repo
| Skrip | Fungsi |
|---|---|
| `scripts/make_figures.py` | Semua gambar dari `results/raw/*.json` (tidak ada angka diketik tangan) |
| `scripts/build_docx.py` | Susun `.md` → docx (sitasi, nomor tabel, persamaan, gaya) |
| `scripts/check_consistency.py` | Cek angka di dokumen proyek vs data |
| `scripts/verify_scopus.py` | Cek indeks Scopus rujukan via daftar sumber resmi `data/external/scopus_source_list_Aug2026.xlsx` |
| `scripts/fetch_references.py` | Ambil metadata rujukan ke `references.json` |
| `experiments/*.py` | Eksperimen; hasil di `results/raw/` (termasuk `jackknife_records/`, `backbone_invariance/`, `block_geometry.json`) |

### Skrip sementara (di `%TEMP%`, **tidak ada di repo**; buat ulang bila perlu)
| Skrip | Fungsi |
|---|---|
| `cek_halaman.ps1` | Bangun docx ke `%TEMP%`, ekspor PDF via Word COM (`ExportAsFixedFormat`, format 17), hitung halaman & kata, ukur ruang kosong |
| `peta_halaman.py pdf [hal…]` | Daftar judul/gambar per halaman + render PNG halaman tertentu (pymupdf) |
| `cek_rujukan_gambar.py` | Pastikan paragraf sebelum tiap float menyebut float itu |
| `audit_v8.py` | Bandingkan naskah vs commit `849c156`: angka, sitasi, persamaan, frasa wajib, kata terlarang |
| `kemiripan2.py [-v]` | Persentase kalimat dengan ≥50% 8-gram sama dengan draf lama |
| `analisis_rujukan.py` | Frekuensi & lokasi tiap rujukan; total kata caption |
| `peta_rujukan.py` | Peta kode rujukan → nomor di docx |

---

## 9. Panduan Singkat untuk Agent Berikutnya

1. Baca bagian 2 dan blok `## Catatan penyusunan` di tiap file `docs/paper/*.md`.
2. Edit hanya file `.md` (atau `make_figures.py` untuk gambar), lalu bangun ulang docx.
3. Setiap perubahan angka harus ditelusuri ke `results/raw/*.json`.
4. Setelah edit: pytest (77 lulus), `check_consistency.py`, cek narasi float, hitung halaman (target ≤ 19–20), lalu commit + push.
5. Laporkan ke pengguna dalam bahasa Indonesia, ringkas, dan jujur tentang apa yang belum terverifikasi.
