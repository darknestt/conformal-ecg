# Kerangka Naskah — peta klaim, bukti, dan ketergantungan

> **Status:** 🟡 KERANGKA · **Dibuat:** 2026-09-30
> **Bukan draf prosa.** Ini peta kerja: untuk tiap bagian, apa yang **sudah tertentu**, apa **buktinya**, dan apa yang **masih menghalangi**.
>
> **Aturan mutlak:** bagian bertanda ❌ tidak boleh ditulis sebelum hasil ada. Menulisnya lebih dulu adalah **HARKing** — merumuskan hipotesis setelah melihat hasil, lalu menyajikannya seolah dirumuskan di muka.

---

## Status kesiapan per bagian

> **2026-10-02 — seluruh bagian berdraf; v3 (penulisan ulang + pemadatan −21% prosa) berlaku.** Penomoran naskah Word: §9 Discussion, §10 Threats, §11 Conclusion. Ablation dihapus (E5 tidak dijalankan, lihat `protocol.md` §12). Draf v2 (`*-draft.md`) ada di riwayat git, commit 9098746.

| § naskah | Bagian | Draf | Catatan |
|---|---|---|---|
| — | Abstract + Index Terms | ✅ [`abstract-conclusion.md`](abstract-conclusion.md) | v3 ±215 kata |
| 1 | Introduction | ✅ [`sec1.md`](sec1.md) | v3: struktur enam paragraf |
| 2 | Related Work | ✅ [`sec2.md`](sec2.md) | v3: −35%, tiga klaim salah dibuang |
| 3–4 | Preliminaries, Problem Formulation | ✅ [`sec3-4.md`](sec3-4.md) | |
| 5 | Methods | ✅ [`sec5.md`](sec5.md) | v3: hasil PTB-XL dipindah ke §8/§10 |
| 6–7 | Datasets, Experimental Setup | ✅ [`sec6-7.md`](sec6-7.md) | v3: paragraf "Cost" ganda dibuang |
| 8 | Results | ✅ [`sec8.md`](sec8.md) | Tabel 8.1–8.6 tidak diubah |
| 9 | Discussion | ✅ [`sec9.md`](sec9.md) | v3: §9.1 tak lagi mengulang §8 |
| 10 | Threats to Validity | ✅ [`sec10.md`](sec10.md) | |
| 11 | Conclusion | ✅ [`abstract-conclusion.md`](abstract-conclusion.md) | |

### Daftar revisi (dikerjakan pada putaran "revisi dan rapikan")

| # | Masalah | Lokasi | Bobot |
|---|---|---|---|
| R1 | ~~Proposition 1 tertulis dua kali~~ ✅ 2026-10-02: §5 merujuk §4; Prop. 1–3 berurutan | sec3-4, sec5 | Selesai |
| R2 | ~~Rujukan ke Proposition 2/2′ yang tidak ada~~ ✅ diganti (6)/(7) | sec8, sec10 | Selesai |
| R3 | Panjang: 13.400 → **12.056 kata / 25 hal.** (Threats v2, §6.4 dipadatkan). Target JBHI ±10 hal. dua kolom masih perlu ±2.000 kata lagi — kandidat: §5.1.3, §6.1–6.3, Kor. 1.x | semua | Sebagian |
| R4 | ~~Penomoran ganda §11/§10~~ ✅ `sec10-draft.md`, builder tanpa pemetaan | builder | Selesai |
| R5 | Klaim "Code ... released" sementara repo privat | §1 | Wajib sebelum submit |
| R6 | [F5] disitasi hanya dari judul; I1, I2, P1 §2 belum dibaca teks penuh | §9, §5 | Wajib sebelum submit |
| R7 | Judul "3–4" dan "6–7" digabung di builder — pertimbangkan satu §3 "Background" | struktur | Rendah |
| R8 | ~~Konsistensi istilah dan ejaan~~ ✅ 2026-10-02: ejaan Amerika (gaya IEEE), kutipan Lee et al. dikembalikan ke ejaan aslinya ("characterizing"); istilah B1/B12/HCP/DEff sudah konsisten | semua | Selesai |

> **Template jurnal belum ditentukan** (arahan dospem 2026-10-02: buat draf dulu). Karena itu R3 lanjutan (pangkas ke batas halaman) **ditunda** sampai jurnal dipilih — memangkas tanpa batas yang jelas berisiko membuang bukti yang justru diminta reviewer.

<details><summary>Tabel status lama (sebelum 2026-10-02)</summary>

| § | Bagian | Siap? | Bergantung pada | Kebal hasil H0? |
|---|---|:---:|---|:---:|
| 1 | Introduction | ⚠️ | Hook bergantung nasib C4 — **kini dipulihkan berkualifikasi** | ❌ |
| 2 | Related Work | ✅ **DRAF ADA** → [`sec2-draft.md`](sec2-draft.md) | `references.md` | ✅ |
| 3 | Preliminaries & Notation | ✅ **DRAF ADA** → [`sec3-4-draft.md`](sec3-4-draft.md) | `theory.md` §0–1 | ✅ |
| 4 | Problem Formulation | ✅ **DRAF ADA** → [`sec3-4-draft.md`](sec3-4-draft.md) | `theory.md` §1, 3, 4.1 | ✅ |
| 5 | Proposed Method | ✅ **DRAF ADA** → [`sec5-draft.md`](sec5-draft.md) | `theory.md` §2–5 | ✅ |
| 6 | Datasets | ✅ **DRAF ADA** → [`sec6-7-draft.md`](sec6-7-draft.md) | Angka final — **sudah dihitung ulang** | ✅ |
| 7 | Experimental Setup | ✅ **DRAF ADA** → [`sec6-7-draft.md`](sec6-7-draft.md) | Backbone final (F2) | ✅ |
| 8 | Results | ✅ **DRAF ADA** → [`sec8-draft.md`](sec8-draft.md) | E1, E2, E4 + invariansi backbone + kontrol permutasi; **E3, E5 belum** | — |
| 9 | Ablation | ❌ | **E5** | — |
| 10 | Discussion | ❌ | §8–9 | — |
| 11 | Threats to Validity | ✅ **DRAF ADA** → [`sec11-draft.md`](sec11-draft.md) | README §11 | ✅ |
| 12 | Conclusion | ❌ | Semuanya | — |

</details>

**Kolom terakhir adalah alasan utama menulis §2–§5 sekarang.** Bila H0 gagal, hanya C4 yang mati; batas kelayakan bersifat kombinatorial dan sudah terbukti pada data nyata tanpa model apa pun. §2–§5 tidak akan terbuang.

---

## §2 Related Work ✅

Empat blok. Setiap entri sudah diverifikasi OpenAlex dan dibaca abstraknya.

| Blok | Isi | Rujukan kunci |
|---|---|---|
| 2.1 | Conformal di bawah pelanggaran exchangeability | Barber dkk. 2023 (AoS) |
| 2.2 | **Conformal hierarkis** | **Lee-Barber-Willett 2026** (fondasi) · Dunn dkk. 2022 (JASA) |
| 2.3 | Conformal multi-label & hierarki label | `10.1016/j.patcog.2021.108271` · arXiv:2410.06296 |
| 2.4 | UQ pada EKG; PTB-XL | Strodthoff dkk. 2021 (JBHI) · Wagner dkk. 2020 |

**Wajib ditulis eksplisit** — jangan dikaburkan:
- Lee-Barber-Willett **sudah menyelesaikan** exchangeability hierarkis (bekas C1). Kita **memakai**, bukan menemukan ulang.
- Paragraf pembeda: mereka murni teoretis dan diuji pada **regresi** (Lorenz 96). Tidak ada yang memeriksa **kapan jaminannya dapat ditegakkan sama sekali** pada data klinis.

---

## §3 Preliminaries & Notation ✅

Sumber: [`theory.md`](../theory.md) §0.

1. Notasi blok: $K$, $N_k$, $n=\sum N_k$, $Z_{k,i}$, $s(\cdot)$, $Q_\beta$
2. Exchangeability hierarkis (Definisi 1 Lee dkk.) — **kutip, jangan turunkan ulang**
3. Ambang HCP (rumus 6) dan Teorema 1 — **kutip dengan atribusi jelas**
4. Hierarki label PTB-XL: superclass → subclass → kode SCP

> ⚠️ Bagian ini **milik orang lain**. Atribusi harus tegas di kalimat pertama tiap subbagian.

---

## §4 Problem Formulation ✅

| Klaim | Sumber | Taraf |
|---|---|---|
| Prop. 1 — $\hat T<\infty \iff \alpha \ge \frac{1}{K_1+1}$ | `theory.md` §1 | 🟢 Terbukti, bebas-distribusi |
| Kor. 1.1 — batas **tidak bergantung $N_k$** | `theory.md` §1 | 🟢 |
| Kor. 1.3 — tereduksi ke $n \ge 1/\alpha-1$ saat $N_k{=}1$ | `theory.md` §1 | 🟢 Diverifikasi numerik |
| Prop. 3 — desain bersilang menuntut partisi *join* | `theory.md` §4.2 | 🟢 Aljabar kekisi |
| Kor. 3.2 — ketidakmungkinan | `theory.md` §4.2 | 🟢 HCP/Dunn · 🔴 klaim universal **DITAHAN** |

**Kalimat yang harus ada persis:** *"Kor. 3.2 kami buktikan untuk keluarga HCP/Dunn. Apakah ia berlaku bagi setiap metode bebas-distribusi yang bersandar pada exchangeability antar-blok masih merupakan pertanyaan terbuka."*

> 🔴 **Gerbang:** jangan longgarkan kalimat itu sebelum statistikawan mereview.

---

## §5 Proposed Method ✅ — bagian terpenting

### 5.1 Tradeoff $K$ vs $N_k$ (C6)

Teorema C6 (a)–(d) dari `theory.md` §3.

> ⚠️ **Pemisahan yang WAJIB eksplisit:** butir (a) bebas-distribusi. Butir (b)–(d) memakai **Asumsi (A)** (model efek acak satu arah). Mencampurnya = sasaran empuk reviewer.

**Sub-klaim: Kish mengukur estimator yang salah.**

$$\mathrm{DEff}_{\text{blok}}(\rho)=\frac{n[1+(H-1)\rho]}{KH} \quad\text{vs}\quad \mathrm{DEff}_{\text{Kish}}=\frac{\sum_k N_k^2}{n}$$

Berimpit **hanya** bila $N_k$ seragam. Pada `site` PTB-XL selisihnya **15,7×**; pada `strat_fold` (nyaris seragam) rasionya **1,000** — validasi internal yang layak ditampilkan.

> 🔧 Sertakan **pencabutan** klaim "dua sumbu tidak berkorelasi". Melaporkan koreksi sendiri jauh lebih kuat daripada berharap tak ada yang memeriksa.

### 5.2 Diagnostik kecukupan blok (C7)

Dua syarat, bukan satu:

| | Isi | Sifat |
|---|---|---|
| **S1 Kelayakan** | $K_1(g) \ge \lceil 1/\alpha\rceil - 1$ | Kombinatorial, **eksak** |
| **S2 Kecukupan** | tiap sumber dependensi bersarang di dalam $g$ | Kombinatorial, **eksak** |

Jual poinnya: verdict **deterministik**, tanpa galat sampling, dan berjalan **sebelum satu pasien pun direkrut**.

### 5.3 Kelayakan per-label pada hierarki (C8)

> 🔧 **2026-10-01.** Seluruh isi bagian ini **Metode, bukan kontribusi** (prior art: Ding dkk. NeurIPS 2023; den Hengst dkk. 2025). Yang dijual hanyalah **temuan empirisnya**.

- ⚠️ Cakupan-superset **sepele** (§5.1 `theory.md`) — Metode
- Prop. 4 — $\alpha \ge 1/(K_1(\ell)+1)$ sebagai **syarat perlu saja**; arah cukup dicabut (pembobotan-ukuran)
- Monotonisitas — satu kalimat, bukan proposisi → frontier kelayakan; 0 pelanggaran dari 23 pasangan
- **Temuan yang dijual:** 24/44 kode SCP gagal syarat perlu pada $\alpha=0{,}05$; `2AVB` $K_1=1$; direplikasi di MIT-BIH: kelas Q $K_1=2$

### 5.4 Algoritma

Pseudokode K1/K2/K3 (README §6.5). Nama metode **belum final**.

---

## §6 Datasets ⚠️

Sudah tertentu: PTB-XL 21.799/18.869 · MIT-BIH 112.647 detak · NSTDB 6 level SNR · 29 pemeriksaan 0 gagal.

Menyusul: angka split final (bergantung keputusan F2).

> Wajib dilaporkan apa adanya: `nurse` kosong 6,8%; site 0/1/2 memuat 93,2% rekaman; kelayakan `site` bertumpu pada 37 site mungil yang tampaknya rezim pengumpulan berbeda.

---

## §7 Experimental Setup ⚠️

Kerangka siap (baseline B1–B15, metrik, uji statistik). Menunggu backbone final F2.

> **Peringatan yang harus masuk naskah:** bootstrap **level pasien**. Bootstrap per-rekaman akan mengulang persis kesalahan yang dikritik paper ini.

---

## §8–§10, §12 ❌ TERKUNCI

Tidak boleh ditulis sebelum E1–E5 selesai. Tidak ada pengecualian.

Yang **boleh** disiapkan sekarang hanyalah **kerangka tabel kosong** — agar bentuk pelaporan ditetapkan sebelum angkanya dilihat, sehingga tidak ada godaan memilih penyajian yang paling menguntungkan:

| Tabel | Isi | Baris/kolom |
|---|---|---|
| T1 | Cakupan vs nominal | metode × $\alpha$ |
| T2 | Ukuran himpunan prediksi | metode × $\alpha$ |
| T3 | Kelayakan per granularitas | granularitas × $\alpha$ |
| T4 | Frontier kelayakan per-label | tingkat hierarki × $m$ |
| T5 | Ablation | 8 konfigurasi K1/K2/K3 |

---

## §11 Threats to Validity ✅

Dari README §11, ditambah yang ditemukan sejak itu:

- Kor. 3.2 baru terbukti untuk keluarga HCP/Dunn (🔴)
- Mengondisikan pada $\ell \in Y$ adalah seleksi bergantung-data (🟡)
- Asumsi (A) tidak bebas-distribusi
- Kelayakan `site` bertumpu pada 37 site mungil
- 411 rekaman (1,9%) tanpa label superclass — dikeluarkan dari evaluasi cakupan karena $Y=\emptyset$ tercakup trivial

---

## Urutan penulisan yang disarankan

1. **§3 → §4 → §5** — sementara eksperimen berjalan. Menerjemahkan `theory.md` ke prosa **memaksa pemeriksaan rantai ketergantungan tiap klaim**; mekanisme inilah yang menangkap kesalahan Kish
2. **§2** — murni dari `references.md`
3. **§11** — kompilasi
4. **§6 → §7** — setelah F2
5. **§8 → §9 → §10** — setelah F3, **tidak sedetik pun lebih awal**
6. **§1 → §12** — terakhir. Introduction ditulis **setelah** tahu apa yang sebenarnya ditemukan

> Menulis Introduction di awal adalah cara paling umum terjebak menjanjikan sesuatu yang tidak terbukti. Riwayat proyek ini sudah memberi dua contoh: C1 dan klaim "dua sumbu tidak berkorelasi".
