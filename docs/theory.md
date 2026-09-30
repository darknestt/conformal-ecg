# Fondasi Teoretis — C6 dan C7

> **Status:** 🟡 DRAF F1 · **Dibuat:** 2026-09-30
> **Prasyarat baca:** Lee, Barber & Willett (2026), `10.1145/3786352`, Teorema 1 dan Discussion.
>
> ⚠️ **Setiap pernyataan di bawah ditandai taraf pembuktiannya.** Yang bertanda 🔴 **belum** merupakan hasil yang sah untuk diklaim di naskah, dan menunggu review pembimbing berlatar statistika (Langkah 2, README §16).

---

## 0. Notasi

| Simbol | Arti |
|---|---|
| $K$ | jumlah blok; $K_1$ = jumlah blok pada set **kalibrasi** |
| $N_k$ | jumlah pengamatan di blok $k$; $n = \sum_k N_k$ |
| $Z_{k,i}$ | pengamatan ke-$i$ di blok $k$ |
| $s(\cdot)$ | fungsi nonconformity |
| $s_{k,i}$ | $s(Z_{k,i})$ |
| $\alpha$ | tingkat miscoverage sasaran |
| $Q_\beta(F)$ | $\inf\{t : F(t) \ge \beta\}$ |
| $\bar F_k(t)$ | $\frac{1}{N_k}\sum_i \mathbb{1}\{s_{k,i} \le t\}$ — CDF empiris **dalam** blok $k$ |

Ambang HCP (Lee dkk., rumus 6):

$$\hat T \;=\; Q_{1-\alpha}\!\left(\underbrace{\sum_{k=1}^{K_1}\sum_{i=1}^{N_k} \frac{1}{(K_1+1)N_k}\,\delta_{s_{k,i}}}_{\text{bagian berhingga}} \;+\; \frac{1}{K_1+1}\,\delta_{+\infty}\right)$$

---

## 1. Proposisi 1 — Batas kelayakan

> 🟢 **TERBUKTI.** Aljabar dasar; diverifikasi numerik di [tests/test_conformal.py](../tests/test_conformal.py).

**Proposisi 1.** $\hat T < \infty$ jika dan hanya jika
$$\alpha \;\ge\; \frac{1}{K_1+1}.$$

**Bukti.** Massa total pada atom berhingga adalah
$$\sum_{k}\sum_{i}\frac{1}{(K_1+1)N_k} \;=\; \sum_{k}\frac{N_k}{(K_1+1)N_k} \;=\; \frac{K_1}{K_1+1}.$$
Tulis $M = \max_{k,i} s_{k,i}$ dan $\hat F$ untuk CDF berbobot tersebut. Maka $\hat F(t) \le \frac{K_1}{K_1+1}$ untuk setiap $t<\infty$, dengan kesamaan pada $t = M$. Karena $Q_{1-\alpha}(\hat F) = \inf\{t: \hat F(t) \ge 1-\alpha\}$, ambangnya berhingga bila dan hanya bila $\frac{K_1}{K_1+1} \ge 1-\alpha$, yaitu $\alpha \ge \frac{1}{K_1+1}$. $\blacksquare$

**Korolari 1.1 (tidak bergantung pada $N_k$).** Ruas kanan tidak memuat $N_k$ sama sekali. **Menambah pengukuran per blok tidak pernah memperbaiki kelayakan**, berapa pun banyaknya.

**Korolari 1.2.** Blok minimum: $K_{\min}(\alpha) = \lceil 1/\alpha \rceil - 1$. Untuk $\alpha = 0{,}05$ dibutuhkan 19 blok, bukan 20.

**Korolari 1.3 (konsistensi dengan split conformal).** Bila $N_k = 1\ \forall k$ maka $K_1 = n$ dan syaratnya menjadi $\alpha \ge \frac{1}{n+1}$, yaitu $n \ge 1/\alpha - 1$ — persis syarat baku split conformal. ✅ Diverifikasi numerik.

> 🔧 **Koreksi 2026-09-30.** Seluruh dokumen sebelumnya menulis syarat ini sebagai $\alpha > \frac{1}{K_1+1}$ (**ketat**). Keliru. Tepat di $\alpha = \frac{1}{K_1+1}$, massa berhingga $\frac{K_1}{K_1+1}$ **persis menyamai** $1-\alpha$, sehingga ambangnya jatuh di $M$ — berhingga. Cakupan terukur pada $K_1{=}19,\ \alpha{=}0{,}05$: **0,9512** $\ge 0{,}95$. Tidak ada verdict di tabel PTB-XL yang berubah, karena tak satu pun granularitas jatuh tepat di batas.

---

## 2. Proposisi 2 — Design effect memerlukan asumsi tambahan

> 🟡 **TERBUKTI DI BAWAH MODEL TAMBAHAN.** Bagian ini **tidak lagi bebas-distribusi** — ia memakai model efek acak satu arah. Dipakai sebagai **panduan desain**, bukan sebagai bagian dari jaminan.

Bagian berhingga dari $\hat F$ dapat ditulis ulang:
$$\hat F(t)\big|_{\text{berhingga}} \;=\; \frac{1}{K_1+1}\sum_{k} \bar F_k(t) \;=\; \frac{K_1}{K_1+1}\cdot\underbrace{\frac{1}{K_1}\sum_k \bar F_k(t)}_{\textstyle \hat G(t)}.$$

Jadi ambang HCP sepenuhnya ditentukan oleh $\hat G$ — **rata-rata CDF antar-blok**, bukan CDF gabungan seluruh titik. Setiap blok menyumbang bobot sama.

**Asumsi (A).** Untuk $t$ tetap, indikator $X_{k,i} = \mathbb{1}\{s_{k,i}\le t\}$ memenuhi: (i) blok saling bebas dan identik; (ii) di dalam blok, $\operatorname{Corr}(X_{k,i}, X_{k,j}) = \rho(t)$ untuk $i\ne j$; (iii) $\mathbb{E}X_{k,i} = F(t)$.

**Proposisi 2 (blok seragam).** Di bawah (A) dengan $N_k = N$ untuk semua $k$:
$$\operatorname{Var}\big(\hat G(t)\big) \;=\; \frac{\sigma^2(t)\,\big[1 + (N-1)\rho(t)\big]}{K N}, \qquad \sigma^2(t) = F(t)\big(1-F(t)\big).$$

**Bukti.** $\operatorname{Var}(\bar F_k(t)) = \frac{1}{N^2}\big[N\sigma^2 + N(N-1)\rho\sigma^2\big] = \frac{\sigma^2[1+(N-1)\rho]}{N}$. Blok bebas, sehingga $\operatorname{Var}(\hat G) = \operatorname{Var}(\bar F_k)/K$. $\blacksquare$

**Proposisi 2′ (blok tak seragam).** Di bawah (A) dengan $N_k$ sembarang:
$$\operatorname{Var}\big(\hat G(t)\big) \;=\; \frac{\sigma^2(t)\,\big[1 + (H-1)\rho(t)\big]}{K H}, \qquad H = \frac{K}{\sum_k N_k^{-1}}$$
dengan $H$ = **rata-rata harmonik** ukuran blok.

**Bukti.**
$$\operatorname{Var}(\hat G) = \frac{1}{K^2}\sum_k \frac{\sigma^2[1+(N_k-1)\rho]}{N_k} = \frac{\sigma^2}{K^2}\Big[(1-\rho)\sum_k \tfrac{1}{N_k} + \rho K\Big] = \frac{\sigma^2}{K}\Big[\frac{1-\rho}{H} + \rho\Big]. \;\blacksquare$$

Rumus seragam bertahan persis dengan $N \mapsto H$. Perhatikan $H$ **didominasi blok terkecil** — pada `site` PTB-XL, $H = 11{,}1$ walaupun rata-rata aritmetiknya 427,1.

### 2.1 ❗ Kish mengukur estimator yang SALAH

> 🔧 **KOREKSI 2026-09-30.** Versi pertama dokumen ini menyamakan $\mathrm{DEff}_{\text{Kish}}$ dengan kasus $\rho{=}1$ dari Prop. 2. Itu **hanya benar untuk blok seragam**. Untuk blok tak seragam keduanya adalah kuantitas berbeda — dan selisihnya mencapai **15,7×** pada PTB-XL.

Ada **dua** estimator yang harus dibedakan:

| | Rumus | Dipakai oleh |
|---|---|---|
| Terboboti-**blok** | $\hat G = \frac{1}{K}\sum_k \bar F_k$ | **HCP** (lihat penulisan ulang $\hat F$ di atas) |
| Terboboti-**observasi** | $\bar X = \frac{1}{n}\sum_k\sum_i X_{k,i}$ | Kish / survei berklaster baku |

Relatif terhadap $n$ titik independen ($\sigma^2/n$):

$$\mathrm{DEff}_{\text{blok}}(\rho) = \frac{n\,[1+(H-1)\rho]}{K H} \;\xrightarrow{\ \rho\to1\ }\; \frac{n}{K} = \bar N \quad\text{(rata-rata \textbf{aritmetik})}$$

$$\mathrm{DEff}_{\text{pooled}}(\rho) = (1-\rho) + \rho\,\frac{\sum_k N_k^2}{n} \;\xrightarrow{\ \rho\to1\ }\; \frac{\sum_k N_k^2}{n} = \mathrm{DEff}_{\text{Kish}} \quad\text{(rata-rata \textbf{terboboti-ukuran})}$$

Keduanya berimpit **hanya** bila $N_k$ seragam. Karena HCP memakai $\hat G$, **$\mathrm{DEff}_{\text{Kish}}$ bukan ukuran efisiensi yang tepat untuk HCP pada blok tak seragam.**

**Pengukuran pada PTB-XL** ([scripts/design_effect_nonuniform.py](../scripts/design_effect_nonuniform.py)):

| Granularitas | $K$ | $\bar N$ (aritmetik) | $H$ (harmonik) | Kish | $\mathrm{DEff}_{\text{blok}}$ $\rho{=}1$ | Rasio |
|---|---:|---:|---:|---:|---:|---:|
| `patient_id` | 18.869 | 1,16 | 1,07 | 1,4 | 1,2 | 1,2× |
| `site` | 51 | 427,10 | 11,11 | 6.687,0 | **427,1** | **15,7×** |
| `nurse` | 12 | 1.693,83 | 744,55 | 5.185,3 | 1.693,8 | 3,1× |
| `device` | 11 | 1.981,73 | 219,92 | 3.900,6 | 1.981,7 | 2,0× |
| `strat_fold` | 10 | 2.179,90 | 2.179,87 | 2.179,9 | 2.179,9 | **1,0×** |

> `strat_fold` berukuran nyaris seragam, dan di sana kedua rumus **berimpit persis** (rasio 1,000). Ini validasi internal bahwa turunannya benar.

### 2.2 Kish tetap buta terhadap $\rho$ — dan itu menjelaskan E11a

**Korolari 2.1.** Untuk blok seragam, $\mathrm{DEff}_{\text{Kish}} = N$, yaitu kasus $\rho = 1$ dari Prop. 2. Karena $\rho\in[0,1]$,
$$1 + (N-1)\rho(t) \;\le\; N,$$
dengan kesamaan bila dan hanya bila $\rho(t)=1$. Jadi $\mathrm{DEff}_{\text{Kish}}$ adalah **batas atas**, bukan estimasi — fungsi dari **ukuran blok semata**, secara struktural **buta terhadap $\rho$**.

Ini menjelaskan Temuan 5 (README §5.6) secara rigoros. Hipotesis "dependensi meluruh terhadap interval antar-rekaman" diuji dengan $\mathrm{DEff}_{\text{Kish}}$ per bin dan hasilnya datar (2,25 / 2,71 / 2,73 / 2,77). **Itu memang harus terjadi**: ukuran blok nyaris seragam antar bin (2,14–2,44), dan Kish tidak melihat apa pun selain ukuran blok. Hipotesisnya tidak terbantahkan — ia **tidak teruji**.

**E11b karenanya harus mengestimasi $\rho(t)$ secara langsung.** Estimator ANOVA satu arah untuk desain tak seimbang tersedia di [src/conformal/icc.py](../src/conformal/icc.py), dengan CI bootstrap **pada level blok** (meresample titik akan mengulang kesalahan yang justru dikritik paper ini). Diuji memulihkan $\rho$ sejati pada $\{0;0{,}2;0{,}5;0{,}8\}$ dalam toleransi 0,05.

> Prop. 2 memakai ICC dari **indikator** $\mathbb{1}\{s\le t\}$, bukan ICC skor mentah. Keduanya kuantitas berbeda; `icc_at_threshold` dan `icc_curve` menyediakan yang benar.

---

## 3. Teorema C6 — Desain studi menentukan inferensi

> 🟡 Butir (a) 🟢 terbukti. Butir (b)–(d) bergantung pada Asumsi (A).

Ini jawaban langsung atas pertanyaan terbuka di Discussion Lee-Barber-Willett.

**Teorema.** Tinjau desain berparameter $(K, N)$ dengan $n = KN$.

**(a) Validitas hanya diatur $K$.** Jaminan non-trivial ada $\iff \alpha \ge \frac{1}{K+1}$. Sepenuhnya bebas dari $N$. *(Proposisi 1)*

**(b) Ada lantai varians yang tak dapat ditembus.** Untuk $K$ tetap,
$$\lim_{N\to\infty} \operatorname{Var}\big(\hat G(t)\big) \;=\; \frac{\sigma^2(t)\,\rho(t)}{K} \;>\; 0 \quad \text{bila } \rho(t)>0 .$$
Pengukuran berulang tak berhingga banyaknya **tidak** membawa varians ke nol.

**(c) Di bawah anggaran total $n$ tetap, blok banyak-dangkal lemah-dominan.**
$$\operatorname{Var}\big(\hat G(t)\big) \;=\; \frac{\sigma^2(t)\big[1+(N-1)\rho(t)\big]}{n}$$
naik monoton terhadap $N$ bila $\rho(t)>0$. Jadi memperbesar $K$ sambil memperkecil $N$ memperbaiki **kedua** sumbu sekaligus — tidak ada tradeoff.

**(d) Di bawah kendala jumlah subjek, tradeoff-nya nyata dan menguntungkan $K$.** Bila $K$ terbatas oleh biaya rekrutmen, menambah $N$ tidak dapat memulihkan kelayakan *(Kor. 1.1)* dan tidak dapat menurunkan varians di bawah $\sigma^2\rho/K$ *(butir b)*.

> **Rumusan ringkas — inilah klaim C6:** dalam inferensi bebas-distribusi pada data berhierarki, $K$ dan $N_k$ **bukan** dua cara setara membeli informasi. $K$ membeli **eksistensi** jaminan; $N_k$ hanya membeli **ketajaman**, dengan hasil yang berkurang dan berhenti pada lantai positif. Tidak ada jumlah pengukuran berulang yang dapat menggantikan blok.

### 3.1 🔧 Klaim "dua sumbu tidak berkorelasi" DICABUT

Versi sebelumnya menyertakan klaim empiris tambahan: *"urutan menurut design effect berlawanan dengan urutan menurut kelayakan $\alpha$"*, dengan contoh `site` (DEff 6.687, layak) versus `device` (DEff 3.901, tidak layak).

**Klaim itu artefak dari memakai $\mathrm{DEff}_{\text{Kish}}$** — ukuran milik estimator yang tidak dipakai HCP. Dengan $\mathrm{DEff}_{\text{blok}}$ yang benar:

| Granularitas | $\mathrm{DEff}_{\text{blok}}$ | $\alpha{=}0{,}05$ |
|---|---:|:---:|
| `patient_id` | 1,2 | ✅ |
| `site` | 427,1 | ✅ |
| `nurse` | 1.693,8 | ❌ |
| `device` | 1.981,7 | ❌ |
| `strat_fold` | 2.179,9 | ❌ |

| | Urutan |
|---|---|
| Menurut Kish | `patient_id` < `strat_fold` < `device` < `nurse` < `site` |
| Menurut $\mathrm{DEff}_{\text{blok}}$ | `patient_id` < `site` < `nurse` < `device` < `strat_fold` |

Dengan ukuran yang benar, **kedua granularitas yang layak justru dua yang paling efisien**. Urutannya **sejalan**, bukan berlawanan.

**Dan itu memang seharusnya.** Pada $\rho=1$, $\mathrm{DEff}_{\text{blok}} = n/K$ — turun monoton terhadap $K$, sementara kelayakan naik monoton terhadap $K$. Keduanya **digerakkan variabel yang sama**, sehingga mustahil berlawanan. Inilah persis isi butir (c): tidak ada tradeoff.

> **Ini pemeriksaan koherensi yang lolos, bukan kekalahan.** Teorema memprediksi "tidak ada tradeoff"; tabel empiris memprediksi "urutan berlawanan"; keduanya bertentangan. Penyelesaiannya menunjukkan tabel empirislah yang memakai kuantitas salah. C6 kehilangan daya jual "kontra-intuitif", tetapi menjadi **konsisten secara internal** — dan konsistensi itu yang diperiksa reviewer.

**Yang tetap bertahan sebagai isi C6:** butir (a)–(d) seluruhnya, Prop. 2′ (rata-rata harmonik), pemisahan $\mathrm{DEff}_{\text{blok}}$ vs Kish (temuan baru yang berguna bagi siapa pun yang memakai HCP pada blok tak seragam), dan Kor. 3.2 (ketidakmungkinan pada desain bersilang) yang tidak menyentuh efisiensi sama sekali.

> ⚠️ **Batas kejujuran.** Butir (a) bebas-distribusi. Butir (b)–(d) memerlukan Asumsi (A) — model parametrik ringan. Naskah **wajib** memisahkan keduanya secara eksplisit; mencampurnya akan menjadi sasaran empuk reviewer.

---

## 4. C7 — Diagnostik kecukupan blok

### 4.1 Dua syarat, bukan satu

Pengelompokan $g$ dapat dipakai untuk kalibrasi hanya bila **keduanya** terpenuhi:

| Syarat | Isi | Sifat |
|---|---|---|
| **S1 Kelayakan** | $K_1(g) \ge \lceil 1/\alpha\rceil - 1$ | Kombinatorial, **eksak**, tanpa galat sampling |
| **S2 Kecukupan** | setiap sumber dependensi bersarang di dalam $g$ | Kombinatorial, **eksak** |

S1 saja tidak cukup, dan inilah yang membedakan C7 dari sekadar menghitung blok.

**Definisi (kecukupan).** Partisi $\mathcal{Q}$ **cukup** bagi sumber dependensi berpartisi $\mathcal{P}$ bila $\mathcal{P}$ menghaluskan $\mathcal{Q}$ — yaitu setiap blok $\mathcal{P}$ termuat seluruhnya dalam satu blok $\mathcal{Q}$.

Bila tidak cukup, pengamatan yang bergantung tersebar ke blok berbeda dan **diperlakukan sebagai independen** — persis kesalahan yang hendak dikoreksi.

### 4.2 Desain bersilang memaksa pemakaian partisi gabungan

> 🟢 **TERBUKTI.** Aljabar kekisi partisi.

**Proposisi 3.** Agar $\mathcal{Q}$ cukup bagi $\mathcal{P}_1$ **dan** $\mathcal{P}_2$ sekaligus, $\mathcal{Q}$ harus lebih kasar daripada keduanya. Partisi terhalus yang memenuhi itu adalah **join** $\mathcal{P}_1 \vee \mathcal{P}_2$ pada kekisi partisi — yaitu komponen terhubung dari graf yang menautkan dua pengamatan bila mereka berbagi blok $\mathcal{P}_1$ atau berbagi blok $\mathcal{P}_2$.

**Korolari 3.1.** $K(\mathcal{P}_1\vee\mathcal{P}_2) \le \min\big(K(\mathcal{P}_1),\, K(\mathcal{P}_2)\big)$, sehingga
$$\alpha_{\min}(\mathcal{P}_1\vee\mathcal{P}_2) \;\ge\; \max\big(\alpha_{\min}(\mathcal{P}_1),\, \alpha_{\min}(\mathcal{P}_2)\big).$$

**Korolari 3.2 (ketidakmungkinan).** Bila $K_1(\mathcal{P}_1\vee\mathcal{P}_2) < \lceil 1/\alpha\rceil - 1$, maka **tidak ada** kalibrasi HCP yang memberi jaminan non-trivial pada tingkat $\alpha$ sambil mengendalikan kedua sumber dependensi. Ini batas **desain studi**, bukan kekurangan metode.

> 🔴 **BELUM TERBUKTI — butuh statistikawan.** Saya menduga Kor. 3.2 berlaku bagi **setiap** metode bebas-distribusi yang validitasnya bersandar pada exchangeability antar-blok, bukan hanya HCP — karena argumen leave-one-block-out memaksa massa $\ge \frac{1}{K_1+1}$ pada $+\infty$. Analoginya adalah ketaktergantikan $n \ge 1/\alpha - 1$ pada split conformal. **Sampai terbukti, naskah hanya boleh mengklaimnya untuk keluarga HCP/Dunn.**

### 4.3 Instansiasi pada PTB-XL

Dihitung oleh [scripts/check_nesting.py](../scripts/check_nesting.py); mentah di `results/raw/block_nesting.json`.

**Granularitas PTB-XL TIDAK bersarang.** Pelanggaran persarangan (pasien yang menyeberang):

| Pasien menyeberang | Jumlah |
|---|---:|
| >1 `site` | **46** |
| >1 `nurse` | **247** |
| >1 `device` | **174** |
| >1 `strat_fold` | **0** ✅ |

Hanya `patient_id` $\subset$ `strat_fold` yang bersarang. Akibatnya memblok per `site` **tidak** cukup bagi dependensi pasien.

**Jumlah blok partisi gabungan** ($K_1$ = fold 9, set kalibrasi):

| Sumber yang dikendalikan | $K_1$ | Blok terbesar | $\alpha_{\min}$ | $\alpha{=}0{,}05$ |
|---|---:|---:|---:|:---:|
| `patient_id` | 1.942 | 8 | 0,00051 | ✅ |
| `patient_id` + `nurse` | 204 | 1.467 | 0,00488 | ✅ |
| `patient_id` + `site` | 34 | 843 | 0,02857 | ✅ |
| `patient_id` + `device` | **5** | 889 | **0,16667** | ❌ |
| keempatnya | **1** | 2.183 | **0,50000** | ❌ |

**Tiga bacaan yang layak masuk naskah:**

1. **Mengendalikan pasien + perangkat sekaligus mustahil pada $\alpha \le 0{,}167$.** 174 pasien menyeberang perangkat, dan union-find merantai 11 perangkat menjadi hanya **5** komponen.
2. **Mengendalikan keempat sumber meruntuhkan set kalibrasi menjadi SATU blok.** $\alpha_{\min} = 0{,}5$ — tidak ada jaminan bermakna yang mungkin, pada metode apa pun dalam keluarga ini.
3. `patient_id` + `nurse` layak ($K_1{=}204$) tetapi satu blok memuat **1.467 dari 2.183** rekaman kalibrasi (67%). Layak belum tentu berguna — S1 dan design effect memang dua hal berbeda.

> Angka $K_1 = 1.942$ untuk `patient_id` tunggal **cocok persis** dengan hasil `feasibility_alpha.py` yang dihitung lewat jalur berbeda. Ini pemeriksaan silang bahwa union-find-nya benar.

### 4.4 Prosedur diagnostik

```
MASUKAN : label blok untuk setiap sumber dependensi kandidat D = {d1..dm}
          tingkat alpha sasaran
KELUARAN: himpunan pengelompokan yang admissible, terurut

1. Untuk setiap himpunan bagian S dari D yang ingin dikendalikan:
2.     Q  <- komponen terhubung dari gabungan partisi di S        (Prop. 3)
3.     K1 <- jumlah blok Q pada set KALIBRASI
4.     S1 <- [ alpha >= 1/(K1+1) ]                                (Prop. 1)
5.     S2 <- terpenuhi menurut konstruksi
6.     DEff <- n / n_eff(Q)            // batas atas efisiensi     (Kor. 2.1)
7.     Jika S1: catat (S, K1, DEff)
8. Urutkan yang admissible menurut cakupan sumber, lalu DEff
```

**Sifat yang membuatnya berguna bagi praktisi:**

- Berjalan **tanpa model, tanpa skor, tanpa label hasil** — hanya label blok dan $\alpha$.
- Verdict S1 dan S2 bersifat **eksak dan deterministik**: tidak ada galat sampling, tidak ada p-value. Tidak lazim untuk sebuah diagnostik, dan layak ditonjolkan.
- Dapat dijalankan **saat merancang studi**, sebelum satu pasien pun direkrut.

---

## 5. C8 — Perluasan ke multi-label berhierarki

### 5.1 Cakupan-superset tereduksi ke HCP secara persis — dan itu harus dikatakan terus terang

> 🟢 **TERBUKTI, tetapi sepele.**

Teorema 1 HCP tidak pernah menyentuh struktur $\mathcal{Y}$. Ia hanya menuntut (i) exchangeability hierarkis antar-blok dan (ii) $s$ tetap terhadap data kalibrasi. Maka untuk sasaran **cakupan-superset**
$$\mathbb{P}\big(Y_{\text{test}} \subseteq \hat C(X_{\text{test}})\big) \;\ge\; 1-\alpha,$$
definisikan skor skalar
$$s(x, Y) \;=\; \max_{\ell \in Y} s_\ell(x),$$
dengan $s_\ell$ nonconformity per-label. Karena $\{Y \subseteq \hat C\} \iff \max_{\ell\in Y} s_\ell(x) \le T$, HCP berlaku **tanpa modifikasi apa pun**.

> ⚠️ **Jangan jual ini sebagai kontribusi.** Rencana cadangan README ("bila C8 ternyata sepele, jadikan bagian Metode") **berlaku untuk sasaran ini**. Mengklaimnya sebagai perluasan non-trivial akan langsung terbaca oleh reviewer.

Isi C8 yang sesungguhnya ada di sasaran berikutnya.

### 5.2 Jaminan per-label TIDAK tereduksi — dan melahirkan batas kelayakan baru

> 🟡 Prop. 1 diterapkan per-stratum; kehati-hatian exchangeability dicatat di §5.5.

Untuk cakupan **terkondisi-label**
$$\mathbb{P}\big(\ell \in \hat C(X) \,\big|\, \ell \in Y\big) \;\ge\; 1-\alpha,$$
kalibrasi hanya boleh memakai titik kalibrasi yang benar-benar memuat $\ell$. Blok yang tersedia karenanya menyusut menjadi blok yang **memuat** $\ell$.

**Proposisi 4 (kelayakan per-label).** Tulis $K_1(\ell)$ = jumlah blok kalibrasi yang memuat setidaknya satu pengamatan berlabel $\ell$. Jaminan terkondisi-label non-trivial pada tingkat $\alpha$ ada bila dan hanya bila
$$\alpha \;\ge\; \frac{1}{K_1(\ell)+1}.$$

*Bukti:* terapkan Prop. 1 pada stratum $\ell$. $\blacksquare$

**Ini bukan formalitas.** Label langka punya $K_1(\ell)$ kecil, dan kelayakannya dapat gagal walaupun $K_1$ global berlimpah. Kuantitasnya **terhitung dari metadata saja** — tanpa model, tanpa skor, tanpa pelatihan.

### 5.3 Hierarki membuat kelayakan monoton — sehingga ada *frontier*

> 🟢 **TERBUKTI** dan diverifikasi empiris (0 pelanggaran dari 23 pasangan).

**Proposisi 5.** Bila $\ell'$ anak dari $\ell$ pada pohon label (setiap pengamatan berlabel $\ell'$ juga berlabel $\ell$), maka
$$K_1(\ell') \;\le\; K_1(\ell) \quad\Longrightarrow\quad \alpha_{\min}(\ell') \;\ge\; \alpha_{\min}(\ell).$$

*Bukti:* setiap blok yang memuat $\ell'$ memuat $\ell$. $\blacksquare$

**Korolari 5.1 (frontier kelayakan).** Kelayakan **monoton naik menuju akar**. Bila sebuah label layak, seluruh leluhurnya layak; bila sebuah label tidak layak, seluruh keturunannya tidak layak. Karenanya terdapat **antirantai** pada pohon yang memisahkan wilayah layak dari wilayah tidak layak — dan posisinya dapat dipetakan sebelum model dilatih.

**Korolari 5.2 (penutupan hierarkis gratis dari sisi kelayakan).** Penutupan ke atas (K2/C2) hanya menambahkan leluhur. Menurut Prop. 5 leluhur selalu setidaknya selayak keturunannya, sehingga penutupan **tidak pernah** memasukkan label yang tak-layak ke dalam himpunan. Biayanya murni efisiensi, bukan kelayakan.

### 5.4 Multiplisitas menaikkan ambang secara drastis

> 🟢 **TERBUKTI** (union bound).

Menjamin $m$ label **serentak** pada tingkat gabungan $\alpha$ menuntut $\alpha/m$ per label, sehingga syaratnya menjadi
$$K_1(\ell) \;\ge\; \left\lceil \frac{m}{\alpha} \right\rceil - 1 \quad \text{untuk setiap } \ell .$$

Pertumbuhannya linear terhadap $m$ dan segera menjadi menentukan.

### 5.5 Instansiasi pada PTB-XL

Dihitung oleh [scripts/label_feasibility.py](../scripts/label_feasibility.py); mentah di `results/raw/label_feasibility.json`.
Kalibrasi = fold 9 · blok = `patient_id` · 44 pernyataan diagnostik SCP · 3.070 pasangan (rekaman, label) pada 1.917 blok.

| Tingkat | $m$ | Tak-layak $\alpha{=}0{,}05$ **marginal** | Tak-layak $\alpha{=}0{,}05$ **serentak** | Blok/label untuk serentak |
|---|---:|---:|---:|---:|
| **Superclass** | 5 | **0 / 5** | **0 / 5** | 99 |
| **Subclass** | 23 | 6 / 23 | **22 / 23** | 459 |
| **Kode SCP** | 44 | **24 / 44** | **43 / 44** | 879 |

**Frontier-nya terletak di antara superclass dan subclass.** Superclass seluruhnya aman bahkan serentak ($K_1$: NORM 905 · MI 486 · STTC 473 · CD 449 · HYP 242). Pada kode SCP, **mayoritas label tak-layak bahkan tanpa koreksi multiplisitas** — `2AVB` hanya punya **1** blok kalibrasi ($\alpha_{\min} = 0{,}5$), `INJIN`/`3AVB`/`INJLA`/`INJIL`/`PMI` masing-masing 2 blok.

**Konsekuensi langsung untuk desain eksperimen:**

1. Klaim terkondisi-label pada tingkat **superclass** sah dan dapat dipertahankan.
2. Klaim terkondisi-label pada tingkat **kode SCP** tidak dapat dipertahankan pada $\alpha$ lazim — dan itu **bukan** karena modelnya lemah. Melaporkan cakupan per-kode-SCP tanpa menyebut $K_1(\ell)$ akan menyesatkan.
3. Bila jaminan serentak diinginkan, **hanya tingkat superclass yang tersedia**.

> Monotonisitas Prop. 5 diperiksa pada seluruh 23 pasangan subclass→superclass: **0 pelanggaran**.

### 5.6 Kehati-hatian yang wajib dicatat

> 🟡 Mengondisikan pada $\ell \in Y$ adalah **seleksi bergantung-data**. Pada conformal terkondisi-kelas (Mondrian) hal ini baku dan sah asalkan stratifikasi dilakukan **sebelum** melihat skor. Di sini satu blok dapat memuat rekaman berlabel $\ell$ **dan** tidak; unit exchangeable di dalam stratum menjadi *irisan* blok dengan stratum. Argumennya masuk akal karena blok tetap i.i.d., tetapi **perlu ditulis formal dan direview** sebelum diklaim.

---

## 6. Daftar keterbatasan yang harus dinyatakan di naskah

| # | Keterbatasan | Tindakan |
|---|---|---|
| 1 | Teorema C6 (b–d), Prop. 2 dan 2′ memakai Asumsi (A); tidak bebas-distribusi | Pisahkan secara eksplisit di §Metode |
| 2 | ~~Prop. 2 diturunkan untuk $N_k$ seragam~~ | ✅ Diselesaikan oleh Prop. 2′ (rata-rata harmonik) |
| 3 | $\rho(t)$ bergantung pada $t$ dan pada model | E11b mengestimasinya; jangan klaim nilai tunggal |
| 4 | Kor. 3.2 baru terbukti untuk keluarga HCP/Dunn | 🔴 Jangan klaim universal sebelum direview statistikawan |
| 5 | Kelayakan `site` bertumpu pada 37 site mungil yang `nurse`-nya kosong | Laporkan; kemungkinan rezim pengumpulan berbeda |
| 6 | §5.1 (cakupan-superset) **sepele** — HCP berlaku tanpa modifikasi | Jangan jual sebagai kontribusi; jadikan bagian Metode |
| 7 | §5.2 mengondisikan pada $\ell \in Y$ = seleksi bergantung-data | 🟡 Tulis argumen exchangeability intra-stratum secara formal |
| 8 | Prop. 4–5 memakai blok = `patient_id`; hasilnya berubah untuk granularitas lain | Jalankan ulang diagnostik bila granularitas berubah |

---

## 7. Yang belum dikerjakan di F1

- [x] ~~**C8** — perluasan HCP ke multi-label berhierarki~~ ✅ §5
- [x] ~~Proposisi 2 untuk $N_k$ tak seragam~~ ✅ Prop. 2′ (rata-rata harmonik), §2
- [x] ~~Estimator $\rho(t)$ beserta CI~~ ✅ [src/conformal/icc.py](../src/conformal/icc.py)
- [ ] 🔴 Review statistikawan atas Kor. 3.2 dan §5.6
- [ ] Rumusan formal C2 (penutupan hierarkis) sebagai lema, memakai Kor. 5.2
- [ ] Kunci judul dan nama metode setelah C6/C7/C8 final
