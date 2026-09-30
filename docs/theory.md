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

### 2.3 ✅ Validasi empiris Prop. 2′ — dan kegagalan ICC sebagai sumbu

**Ini pengujian paling tajam yang tersedia bagi Prop. 2′**, karena teorinya diminta meramalkan di titik yang membuat ukuran saingannya keliru.

Sumbu pertama yang dicoba adalah $\rho$ sendiri. Di dalam MIT-BIH, sumbu itu bekerja — defisit cakupan naik monoton terhadap $\rho$, Spearman $+0{,}88/+0{,}78/+0{,}80$. Tetapi sumbu itu **runtuh ketika PTB-XL dimasukkan**:

| Sumber | $\rho$ | Defisit $\alpha{=}0{,}15$ |
|---|---:|---:|
| MIT-BIH, $p{=}0{,}2$ | 0,3351 | **+0,0048** |
| **PTB-XL (pasien)** | **0,3525** | **−0,0012** |

$\rho$ hampir sama, defisit berlawanan tanda. **ICC saja bukan sumbu yang benar.**

Prop. 2′ menjelaskannya tanpa parameter tambahan. Karena $H$ adalah rata-rata **harmonik**:

$$\mathrm{DEff} = 1 + (H-1)\rho \quad\Longrightarrow\quad
\begin{cases}
\text{PTB-XL:} & H = 1{,}05 \Rightarrow \mathrm{DEff} = 1{,}02\\[2pt]
\text{MIT-BIH:} & H = 1.355 \Rightarrow \mathrm{DEff} = 703{,}93
\end{cases}$$

Isinya dapat dinyatakan dalam satu kalimat: **dependensi baru merusak kalibrasi bila ada pengulangan di dalam blok untuk dikorelasikan.** Pada blok nyaris-tunggal, $\rho$ setinggi apa pun tidak berakibat, karena $H-1 \approx 0$ meredamnya.

Pada sumbu $\mathrm{DEff}$, kedua dataset jatuh pada satu kurva monoton:

| Sumber | $H$ | $\rho$ | $\mathrm{DEff}$ | Defisit $\alpha{=}0{,}15$ |
|---|---:|---:|---:|---:|
| PTB-XL (pasien) | 1,05 | 0,3525 | **1,02** | −0,0012 |
| MIT-BIH $p{=}1$ | 1.355 | 0,0001 | 1,10 | +0,0001 |
| MIT-BIH $p{=}0{,}5$ | 1.355 | 0,1334 | 181,60 | −0,0004 |
| MIT-BIH $p{=}0{,}2$ | 1.355 | 0,3351 | 454,67 | +0,0048 |
| MIT-BIH $p{=}0$ | 1.355 | 0,5192 | **703,93** | **+0,0102** |

Spearman gabungan: $+0{,}84 / +0{,}80 / +0{,}85$, seluruhnya $p < 0{,}002$.

#### Mengapa ini bukan pemilihan sumbu pasca-hoc

$\mathrm{DEff} = 1+(H-1)\rho$ **sudah tertulis sebagai Prop. 2′ di dokumen ini sebelum data tersebut dikumpulkan**. Urutannya: ICC dicoba lebih dulu, gagal menyatukan, lalu proposisi yang sudah ada menjelaskan kegagalannya. Rata-rata harmonik bukan pilihan bebas — ia **turunan** dari $\operatorname{Var}(\hat G)$, dan justru perbedaan harmonik-vs-aritmetik itulah yang membuat PTB-XL jatuh di $\mathrm{DEff}{\approx}1$.

Sekalipun demikian, penetapan sumbu ini terjadi **sesudah** melihat hasil dan tercatat demikian di [protocol.md §12](protocol.md).

#### Ketimpangan $N_k$ bukan mekanisme terpisah

Faktorial 2×2 ([experiments/factorial_mitdb.py](../experiments/factorial_mitdb.py)) memisahkan klasterisasi dari ketimpangan ukuran blok pada $n$ yang disamakan:

| Faktor | Besar efek | Signifikan |
|---|---|---|
| Klasterisasi | −0,0122 … −0,0155 | **3/3** |
| Ketimpangan $N_k$ | −0,0026 … −0,0044 | 0/3 |
| Interaksi | −0,0052 … −0,0079 | 0/3 |

Lengan teracak mengenai nominal nyaris sempurna **termasuk saat blok timpang**. Itu konsisten dengan Prop. 2′: ketimpangan masuk hanya lewat $H$, dan $H$ hanya berpengaruh melalui hasil kalinya dengan $\rho$. Tanpa $\rho$, ketimpangan tidak mengerjakan apa pun.

#### Keterbatasan yang wajib dinyatakan

1. Defisit **per titik tidak signifikan sendiri-sendiri**; seluruh CI memuat nol. Buktinya terletak pada tren monoton, yang memang merupakan kriteria pra-registrasi.
2. PTB-XL menyumbang **1 dari 12 titik**; korelasi gabungan digerakkan gradien internal MIT-BIH. Peran PTB-XL adalah **uji ramalan** lintas modalitas, tugas, dan jenis blok — bukan tren independen.
3. Titik MIT-BIH dihasilkan dengan **melemahkan dependensi secara sintetis**, bukan dengan mengamati kohort ber-$\rho$ berbeda.

### 2.4 ✅ Ketegaran terhadap pilihan estimator ICC

Tabel §2.3 memakai ICC **skor mentah**. Prop. 2 sebenarnya dinyatakan untuk ICC **indikator** $\mathbb{1}\{s\le t\}$ — selisih yang dicatat sendiri di akhir §2.2, dan persis celah yang akan ditanyakan reviewer statistik.

Seluruh kurva dihitung ulang dengan besaran yang benar, memakai ambang **tetap** $t = $ kuantil $(1-\alpha)$ dari seluruh skor evaluasi agar $\rho$ menjadi sifat data, bukan sifat satu split ([experiments/robustness_indicator_icc.py](../experiments/robustness_indicator_icc.py)).

| $\alpha$ | Spearman (ICC skor) | **Spearman (ICC indikator)** | $p$ |
|---|---:|---:|---:|
| 0,10 | +0,8392 | **+0,8951** | $8{,}4\times10^{-5}$ |
| 0,15 | +0,8042 | **+0,8042** | $1{,}6\times10^{-3}$ |
| 0,20 | +0,8462 | **+0,7063** | $1{,}0\times10^{-2}$ |

**Lulus 3/3 pada kedua estimator.** Nilai $\rho$ memang berubah — PTB-XL turun dari 0,3525 (skor) ke 0,19–0,20 (indikator) — tetapi $\mathrm{DEff}$-nya tetap $\approx 1{,}01$ dan posisinya pada kurva tidak bergeser.

> Konsekuensinya terhadap Asumsi (A): ramalan Prop. 2′ bertahan pada besaran yang **memang diminta teorinya**, bukan pada aproksimasi yang lebih mudah dihitung. Asumsi (A) tetap merupakan pilihan pemodelan dan tetap dinyatakan sebagai keterbatasan, tetapi hasil utama tidak bergantung pada kemudahan itu.

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

### 4.0 Status formal tiap komponen — audit

> Ditulis 2026-09-30 untuk menjawab risiko yang sah: sebuah "diagnostik" dapat tampak berguna padahal hanya merupakan kumpulan kondisi intuitif tanpa status matematis yang jelas. Tabel ini menyatakan status setiap komponen secara terbuka.

| Komponen | Status | Sumber |
|---|---|---|
| **S1** Kelayakan | 🟢 **Teorema** — konsekuensi langsung Prop. 1 | Teorema 1 [A0] |
| **S2** Kecukupan | � **Definisi + Prop. 3**, sah **hanya di bawah model [A0]** | §4.0b serangan 3 |
| **S0** Keteramatan | 🟡 **Klaim dokumentasi**, bukan teorema | §4.0b serangan 2 |
| **Prop. 0′** Harga ketakteramatan | 🟢 **Korolari Prop. 3** — batas lewat join kelas $\mathfrak{P}$ | §4.0b serangan 1 & 4 |
| Urutan $S_0 \to S_1 \to S_2$ | 🟡 **Aturan keputusan** | pilihan desain, bukan teorema |
| Pemeringkatan granularitas admissible | 🟡 **Heuristik** berbasis Prop. 2′ | bukan optimalitas terbukti |

> Status di atas adalah hasil **sesudah** audit adversarial §4.0b. Versi pertama menandai S0 dan S2 sebagai 🟢; keduanya diturunkan setelah serangan berhasil menembusnya.

**Yang tidak diklaim:** bahwa urutan pemeriksaan ini optimal, bahwa ia lengkap (mungkin ada syarat keempat), atau bahwa pemeringkatannya menghasilkan pilihan terbaik dalam arti apa pun yang terbukti. Ia adalah **prosedur yang dapat diaudit**, bukan algoritma optimal.

---

### 4.0b Audit adversarial — tiga celah yang saya temukan sendiri

> Dikerjakan 2026-09-30 dengan berperan sebagai reviewer yang berusaha menunjukkan bahwa C7 **hanya tampak formal**. Ketiga serangan di bawah berhasil menembus rumusan versi pertama. Perbaikannya disertakan.

#### Serangan 1 — "Proposisi 0 benar, tetapi nyaris tanpa isi"

**Serangan.** Bukti Prop. 0 memakai $\mathcal{P}_\bot$ (seluruhnya tunggal) melawan $\mathcal{P}_\top$ (satu blok). Tetapi $\mathcal{P}_\bot$ berarti **tidak ada dependensi sama sekali**. Jadi yang dibandingkan adalah "nihil dependensi" versus "dependensi total". Pernyataan seperti itu berlaku bagi **sembarang** besaran tak teramati dan tidak mengatakan apa pun khusus tentang conformal prediction. Ia hanya merumuskan ulang "Anda tidak dapat mengetahui apa yang tidak Anda amati".

**Diterima.** Prop. 0 diturunkan statusnya menjadi **catatan**, bukan hasil. Penggantinya menyatakan sesuatu yang operasional — tetapi rumusan pertamanya sendiri mengandung cacat kuantifier, lihat serangan 4.

#### Serangan 4 — "Prop. 0′ menyelundupkan dua asumsi"

**Serangan.** Rumusan pertama Prop. 0′ berbunyi: *tanpa kendala, jaminan tereduksi ke kasus terburuk $\mathcal{P}_\top$, sehingga $\alpha \ge \tfrac12$.* Langkah itu bukan aritmetika melainkan **kuantifier**, dan menyelundupkan dua hal:

1. bahwa $\mathcal{P}_\top$ **termasuk** kelas partisi yang admissible;
2. bahwa jaminan dituntut berlaku **seragam** atas seluruh kelas itu.

Keduanya pilihan, bukan konsekuensi. Lebih buruk lagi, asumsi (1) sering **absurd secara domain**: $\mathcal{P}_\top$ pada Challenge 2021 berarti satu pasien menghasilkan 66.416 EKG di tujuh institusi.

**Diterima.** Rumusan diperbaiki sehingga tidak lagi memaksakan kasus terburuk, melainkan mengikuti Prop. 3 yang sudah ada.

> 🟢 **Proposisi 0′ (harga ketakteramatan, direvisi).** Misalkan $\mathfrak{P}$ kelas partisi yang admissible di bawah model [A0] **dan** konsisten dengan metadata teramati. Bila jaminan dituntut berlaku tanpa mengetahui $\mathcal{P}$ yang sebenarnya, maka partisi kalibrasi $\mathcal{Q}$ wajib memenuhi S2 bagi **setiap** $\mathcal{P}\in\mathfrak{P}$. Menurut Prop. 3 hal itu menuntut
> $$\mathcal{Q} \;\succeq\; \bigvee_{\mathcal{P}\in\mathfrak{P}} \mathcal{P}, \qquad\text{sehingga}\qquad \alpha \;\ge\; \frac{1}{K_1\!\left(\bigvee_{\mathcal{P}\in\mathfrak{P}} \mathcal{P}\right)+1}.$$
>
> *Bukti.* Jaminan HCP menuntut $\mathcal{P} \preceq \mathcal{Q}$. Agar berlaku bagi setiap anggota $\mathfrak{P}$, $\mathcal{Q}$ harus lebih kasar daripada seluruhnya; partisi terhalus dengan sifat itu adalah join-nya (Prop. 3). Kor. 3.1 memberi batas $K_1$-nya. $\square$

**Korolari 0′.1.** Bila $\mathfrak{P}$ tidak dibatasi sama sekali sehingga memuat $\mathcal{P}_\top$, maka join-nya adalah $\mathcal{P}_\top$, $K_1 = 1$, dan batasnya menjadi $\alpha \ge \tfrac12$.

**Rumusan yang boleh masuk naskah** — perhatikan syaratnya dinyatakan, bukan diandaikan:

> *If no restriction is imposed on the unobserved partition and the single-block partition is admissible, the worst-case feasibility bound reduces to $K_1 = 1$, yielding $\alpha \ge 1/2$.*

Yang **tidak boleh** ditulis: *"S0 tak teramati, karena itu $\alpha \ge 0{,}5$."* Selisih kalimatnya kecil; selisih matematisnya besar.

#### Akibat sesungguhnya dari kegagalan S0

Dalam praktik, pengetahuan domain **menyingkirkan** $\mathcal{P}_\top$. Tetapi $\mathfrak{P}$ kemudian menjadi objek yang **ditetapkan oleh asumsi**, bukan dihitung dari data. Inilah konsekuensi sebenarnya, dan ia lebih tajam daripada angka $\tfrac12$:

> **Kegagalan S0 mengubah $K_1$ dari besaran terhitung menjadi asumsi yang wajib dinyatakan.**

Naskah karena itu tidak boleh melaporkan satu angka $\alpha_{\min}$ untuk dataset tanpa pengenal blok. Yang harus dilaporkan adalah **asumsi tentang $\mathfrak{P}$** beserta batas yang mengikutinya — dan pembaca dapat menilai kelayakan asumsi itu sendiri.

#### Serangan 2 — "Definisi keteramatan itu hampa"

**Serangan.** Pada dataset berhingga, $M$ memuat pengenal rekaman yang unik per baris. Lapangan-$\sigma$ yang dibangkitkannya adalah lapangan-$\sigma$ diskret, sehingga **setiap** partisi bersifat $\sigma(M)$-terukur. Definisi S0 versi pertama karena itu dipenuhi secara trivial oleh apa pun, dan tidak menyaring apa-apa.

**Diterima — ini celah paling serius dari ketiganya.** Definisi diperbaiki menjadi relatif terhadap himpunan variabel yang **dideklarasikan**, bukan terhadap seluruh metadata.

**Definisi (keteramatan, direvisi).** Misalkan $V \subseteq M$ himpunan variabel metadata **substantif** — yaitu $M$ dikurangi pengenal yang unik per rekaman. Sumber dependensi berpartisi $\mathcal{P}$ disebut **$V$-teramati** bila terdapat fungsi **yang ditetapkan di muka** $f$ sehingga keanggotaan blok tiap pengamatan sama dengan $f(V)$.

Pengecualian pengenal-unik itu bukan kerapian teknis. Pengenal unik membangkitkan partisi **terhalus**, yang tepat merupakan asumsi "setiap rekaman independen" — asumsi yang justru hendak diuji. Membiarkannya masuk membuat S0 selalu lolos dengan cara yang menjawab pertanyaan yang salah.

> ⚠️ **Batas kejujuran yang wajib dinyatakan di naskah.** Sesudah perbaikan ini pun, S0 **bukan sifat matematis yang dapat dibuktikan dari data**. Tanpa label pasien, saya tidak dapat membuktikan bahwa partisi pasien tidak memfaktor melalui $V$ — saya hanya dapat menyatakan bahwa **tidak ada variabel yang terdokumentasi sebagai pengenal pasien**. S0 karena itu adalah **klaim tentang dokumentasi dan provenans**, bukan teorema. Menyajikannya sebagai teorema akan menyesatkan.

#### Serangan 3 — "S2 tidak terdefinisi dengan baik"

**Serangan.** S2 menuntut $\mathcal{P} \preceq \mathcal{Q}$ dengan $\mathcal{P}$ "struktur dependensi". Tetapi dependensi pada umumnya **bukan berbentuk partisi**. Dua pengamatan dapat bergantung tanpa berada dalam blok bersama mana pun — misalnya dependensi spasial yang meluruh terhadap jarak, atau dependensi temporal berekor panjang. Pada kasus semacam itu tidak ada $\mathcal{P}$ yang dapat ditulis, sehingga S2 tidak memiliki makna.

**Diterima.** S2 memang hanya terdefinisi di bawah model tertentu, dan model itu selama ini saya andaikan tanpa menyebutnya.

**Prasyarat model (dinyatakan eksplisit).** S2 mengandaikan **exchangeability hierarkis** sebagaimana dirumuskan Lee, Barber & Willett [A0]: dependensi dibangkitkan struktur blok laten, dan pengamatan bersifat exchangeable **di dalam** blok serta blok-bloknya exchangeable antar satu sama lain. Di bawah model itu $\mathcal{P}$ terdefinisi dengan baik dan S2 bermakna.

Di luar model itu — dependensi spasial kontinu, deret waktu berekor panjang, graf tanpa struktur komunitas — **C7 tidak berlaku**, dan naskah harus menyatakannya. Kerangka rujukan yang tepat di sana adalah [A1] (conformal di luar exchangeability) atau [A7]/[A8], bukan C7.

> Ini bukan kelemahan yang ditambal, melainkan ruang lingkup yang dipertegas. HCP sendiri berdiri di atas asumsi yang sama; C7 tidak dapat lebih umum daripada fondasinya.

#### Ringkasan status sesudah audit

| Komponen | Sebelum | **Sesudah audit** |
|---|---|---|
| Prop. 0 | 🟢 hasil | 🟡 **catatan** — benar tetapi nyaris tanpa isi |
| **Prop. 0′** (rumusan pertama) | — | ❌ **dicabut** — menyelundupkan dua asumsi kuantifier |
| **Prop. 0′** (direvisi, via join $\mathfrak{P}$) | — | 🟢 **hasil** — korolari Prop. 3, syaratnya eksplisit |
| S0 | 🟢 definisi terukur | 🟡 **klaim dokumentasi**, bukan teorema |
| S1 | 🟢 teorema | 🟢 tidak berubah |
| S2 | 🟢 definisi | 🟡 **terdefinisi hanya di bawah model [A0]** |

Empat serangan dilancarkan, **keempatnya menembus**. Itu hasil yang benar: rumusan versi pertama **memang** lebih longgar daripada yang saya klaim.

> Serangan 4 datang **setelah** tiga lubang pertama ditutup, dan menembus tambalannya sendiri. Ini mengingatkan bahwa menambal cacat dapat memperkenalkan cacat baru — audit harus diulang terhadap perbaikannya, bukan berhenti pada rumusan lama.

#### Hubungan C7 ↔ C6

C7 bukan kontribusi terpisah yang kebetulan bertetangga dengan C6. Ia adalah **C6 yang dijadikan dapat diperiksa**, ditambah dua prasyarat yang C6 andaikan secara diam-diam.

| C6 menyatakan | C7 menjadikannya |
|---|---|
| Validitas dibatasi $K_1$, bukan $N_k$ (butir a) | **S1** — kondisi yang dihitung per granularitas |
| Efisiensi diatur $\mathrm{DEff}=1+(H-1)\rho$ (butir b–d) | Kunci pengurutan granularitas admissible |
| *(diandaikan)* blok dapat dibentuk dari data | **S0** |
| *(diandaikan)* blok menampung seluruh dependensi | **S2** |

Dua baris terakhir adalah isi sesungguhnya C7. C6 merumuskan batasnya; C6 tidak pernah menanyakan apakah blok yang dibutuhkan **ada** dan **cukup**.

---

### 4.1 Tiga syarat, bukan satu

Pengelompokan $g$ dapat dipakai untuk kalibrasi hanya bila **ketiganya** terpenuhi:

| Syarat | Isi | Sifat |
|---|---|---|
| **S0 Keteramatan** | partisi sumber dependensi **terukur** terhadap metadata | Definisi terukur |
| **S1 Kelayakan** | $K_1(g) \ge \lceil 1/\alpha\rceil - 1$ | Kombinatorial, **eksak**, tanpa galat sampling |
| **S2 Kecukupan** | setiap sumber dependensi bersarang di dalam $g$ | Kombinatorial, **eksak** |

S1 saja tidak cukup, dan inilah yang membedakan C7 dari sekadar menghitung blok.

#### S0 — prasyarat yang semula tersembunyi

> 🔧 **DITAMBAHKAN 2026-09-30.** Versi pertama C7 hanya memuat S1 dan S2. Kelalaian itu tidak pernah terlihat karena PTB-XL dan MIT-BIH sama-sama mencatat pengenal pasien, sehingga S0 selalu terpenuhi secara diam-diam.

**Definisi (keteramatan).** Misalkan $V \subseteq M$ himpunan variabel metadata **substantif** — yaitu metadata dikurangi pengenal yang unik per rekaman. Sumber dependensi berpartisi $\mathcal{P}$ disebut **$V$-teramati** bila terdapat fungsi **yang ditetapkan di muka** $f$ sehingga keanggotaan blok tiap pengamatan sama dengan $f(V)$.

Pengecualian pengenal-unik bersifat menentukan: pengenal unik membangkitkan partisi terhalus, yang tepat merupakan asumsi "setiap rekaman independen" — asumsi yang justru hendak diuji. Lihat §4.0b serangan 2 untuk alasan lengkap dan untuk batas kejujurannya.

Setiap partisi kalibrasi $\mathcal{Q}$ yang dapat dibangun praktisi **wajib** $V$-teramati — tidak mungkin mengelompokkan menurut sesuatu yang tidak tercatat.

> 🟡 **Catatan (ketakterputusan).** Bila $\mathcal{P}$ tidak $V$-teramati, pernyataan "$\mathcal{P}$ menghaluskan $\mathcal{Q}$" tidak dapat diputuskan dari data: $\mathcal{P}_\bot$ membuatnya berlaku, $\mathcal{P}_\top$ membuatnya gagal, dan keduanya konsisten dengan metadata yang sama. Pernyataan ini **benar tetapi nyaris tanpa isi** — ia berlaku bagi sembarang besaran tak teramati. Yang operasional adalah **Prop. 0′** di §4.0b: kegagalan S0 mengubah $K_1$ dari besaran **terhitung** menjadi **asumsi yang wajib dinyatakan**.

Konsekuensinya bersifat **epistemik, bukan negatif**:

| | Keluaran diagnostik | Artinya |
|---|---|---|
| S1 gagal | **TIDAK** | Terbukti tidak ada jaminan non-trivial |
| S2 gagal | **TIDAK** | Terbukti dependensi tidak terkendali |
| **S0 tak teramati** | **TIDAK DAPAT DITENTUKAN** | Bukan bukti aman, **dan bukan bukti gagal** |

> ⚠️ **S0 tidak pernah "gagal".** Ia hanya **terpenuhi** atau **tak teramati**. Menulis "S0 gagal" menyiratkan telah dibuktikan adanya dependensi tak terkendali — padahal yang terjadi justru sebaliknya: tidak ada yang dapat dibuktikan. Prop. 0 menyatakan persis itu.

**Aturan keputusan** (🟡 pilihan desain, bukan teorema). Untuk jaminan yang dipakai pada keputusan klinis, "tidak dapat ditentukan" diperlakukan sebagai **tidak lolos**. Asumsi diam-diam bahwa sumber dependensi tak tercatat berarti tak ada adalah persis asumsi yang membuat conformal naif keliru sejak awal.

> Perhatikan asimetrinya: S0 tidak dapat dipenuhi dengan analisis yang lebih cermat, berapa pun usahanya. Ia hanya dapat dipenuhi dengan **mengubah cara data dikumpulkan**. Itulah sebabnya diagnostik ini berguna justru **sebelum** studi dijalankan, bukan sesudah.

**Definisi (kecukupan).** Partisi $\mathcal{Q}$ **cukup** bagi sumber dependensi berpartisi $\mathcal{P}$ bila $\mathcal{P}$ menghaluskan $\mathcal{Q}$ — yaitu setiap blok $\mathcal{P}$ termuat seluruhnya dalam satu blok $\mathcal{Q}$.

> 🟡 **Prasyarat model.** Definisi ini hanya bermakna bila dependensi memang **berstruktur blok**, yaitu di bawah exchangeability hierarkis [A0]. Dependensi spasial kontinu atau deret waktu berekor panjang tidak dapat ditulis sebagai partisi, dan di sana C7 **tidak berlaku**. Lihat §4.0b serangan 3.

Bila tidak cukup, pengamatan yang bergantung tersebar ke blok berbeda dan **diperlakukan sebagai independen** — persis kesalahan yang hendak dikoreksi.

### 4.2 Desain bersilang memaksa pemakaian partisi gabungan

> 🟢 **TERBUKTI.** Aljabar kekisi partisi.

**Proposisi 3.** Agar $\mathcal{Q}$ cukup bagi $\mathcal{P}_1$ **dan** $\mathcal{P}_2$ sekaligus, $\mathcal{Q}$ harus lebih kasar daripada keduanya. Partisi terhalus yang memenuhi itu adalah **join** $\mathcal{P}_1 \vee \mathcal{P}_2$ pada kekisi partisi — yaitu komponen terhubung dari graf yang menautkan dua pengamatan bila mereka berbagi blok $\mathcal{P}_1$ atau berbagi blok $\mathcal{P}_2$.

**Korolari 3.1.** $K(\mathcal{P}_1\vee\mathcal{P}_2) \le \min\big(K(\mathcal{P}_1),\, K(\mathcal{P}_2)\big)$, sehingga
$$\alpha_{\min}(\mathcal{P}_1\vee\mathcal{P}_2) \;\ge\; \max\big(\alpha_{\min}(\mathcal{P}_1),\, \alpha_{\min}(\mathcal{P}_2)\big).$$

**Korolari 3.2 (ketidakmungkinan).** Bila $K_1(\mathcal{P}_1\vee\mathcal{P}_2) < \lceil 1/\alpha\rceil - 1$, maka **tidak ada** kalibrasi HCP yang memberi jaminan non-trivial pada tingkat $\alpha$ sambil mengendalikan kedua sumber dependensi. Ini batas **desain studi**, bukan kekurangan metode.

> 🔴 **Ruang lingkup dikunci.** Saya menduga Kor. 3.2 berlaku bagi **setiap** metode bebas-distribusi yang validitasnya bersandar pada exchangeability antar-blok, bukan hanya HCP — karena argumen leave-one-block-out memaksa massa $\ge \frac{1}{K_1+1}$ pada $+\infty$. Dugaan itu **tidak diklaim di naskah**. Naskah hanya mengklaimnya untuk keluarga HCP/Dunn, dan menyatakan sisanya sebagai pertanyaan terbuka.

#### ✅ Verifikasi konstruktif pada PTB-XL — 2026-09-30

Kor. 3.2 adalah **klaim eksistensi**, sehingga dapat ditegakkan sepenuhnya oleh satu contoh terverifikasi tanpa memerlukan argumen umum. PTB-XL adalah contoh itu.

[scripts/verify_corollary32.py](../scripts/verify_corollary32.py) mengenumerasi **seluruh $2^4-1 = 15$ join** dari himpunan bagian sumber $\{\texttt{patient\_id}, \texttt{site}, \texttt{nurse}, \texttt{device}\}$ pada fold 9 (1.960 rekaman sesudah membuang metadata sumber kosong), lalu memeriksa S1 dan S2 satu per satu:

| Granularitas | $K_1$ | S2? | $\alpha_{\min}$ |
|---|---:|:-:|---:|
| `patient_id` | 1.739 | tidak | 0,00057 |
| `nurse` | 12 | tidak | 0,07692 |
| `device` | 10 | tidak | 0,09091 |
| `site` | 3 | tidak | 0,25000 |
| `patient_id` ∨ `device` | 6 | tidak | 0,14286 |
| `patient_id` ∨ `nurse` | 2 | tidak | 0,33333 |
| **`site` ∨ `nurse`** | **1** | **YA** | **0,50000** |
| … 7 join lain yang memenuhi S2 | 1 | YA | 0,50000 |

**Hasil: 8 granularitas memenuhi S2, seluruhnya $K_1 = 1$. Nol granularitas memenuhi S1 dan S2 sekaligus** pada $\alpha \in \{0{,}01;\,0{,}05;\,0{,}10;\,0{,}20\}$.

Granularitas **terhalus** yang memenuhi S2 adalah `site` ∨ `nurse`, dan ia sudah runtuh menjadi satu blok. Setiap pemenuh S2 lainnya lebih kasar lagi, sehingga $K_1$-nya tidak mungkin lebih besar. Ketidakmungkinan karena itu **ekshaustif pada kekisi ini**, bukan hasil pemeriksaan sebagian.

> ⚠️ **Kesalahan yang tertangkap saat menyusunnya.** Versi pertama skrip menghitung join dengan menggabungkan label (`"a|b"`). Itu menghasilkan **irisan** — yakni *meet*, partisi terhalus yang memperhalus keduanya — bukan *join*. Arahnya terbalik. Gejalanya: `patient_id` ∨ `site` memberi $K{=}1.739$, sama persis dengan `patient_id` sendiri, padahal join sejati harus **lebih kasar**. Akibatnya tabel melaporkan **nol** granularitas pemenuh S2, termasuk join seluruh sumber — yang secara konstruksi mustahil. Tabel itu sendiri yang mengungkap bugnya. Join yang benar dihitung sebagai komponen terhubung (union-find).

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
MASUKAN : daftar sumber dependensi yang DIDUGA ada, D = {d1..dm}
          metadata yang tersedia M
          tingkat alpha sasaran
KELUARAN: himpunan pengelompokan yang admissible, terurut
          ATAU vonis TIDAK DAPAT DITENTUKAN

0. S0 <- [ partisi tiap sumber di D terukur terhadap metadata M ]
1. Jika S0 tak teramati untuk sumber d:
2.     KELUARKAN "TIDAK DAPAT DITENTUKAN untuk d" dan BERHENTI
3.     // bukan "gagal" dan bukan "aman" -- lihat Prop. 0
4. Untuk setiap himpunan bagian S dari D yang ingin dikendalikan:
5.     Q  <- komponen terhubung dari gabungan partisi di S        (Prop. 3)
6.     K1 <- jumlah blok Q pada set KALIBRASI
7.     S1 <- [ alpha >= 1/(K1+1) ]                                (Prop. 1)
8.     S2 <- terpenuhi menurut konstruksi
9.     DEff <- 1 + (H - 1) * rho       // efisiensi                (Prop. 2')
10.    Jika S1: catat (S, K1, DEff)
11. Urutkan yang admissible menurut cakupan sumber, lalu DEff
```

**Sifat yang membuatnya berguna bagi praktisi:**

- Berjalan **tanpa model, tanpa skor, tanpa label hasil** — hanya label blok dan $\alpha$.
- Verdict S1 dan S2 bersifat **eksak dan deterministik**: tidak ada galat sampling, tidak ada p-value. Tidak lazim untuk sebuah diagnostik, dan layak ditonjolkan.
- Dapat dijalankan **saat merancang studi**, sebelum satu pasien pun direkrut.
- **Langkah 0 hanya memerlukan header berkas**, bukan sinyalnya. Pada dataset besar, vonis dapat diperoleh dengan mengunduh sebagian kecil ukuran dataset.

### 4.5 Tiga mode kegagalan yang berbeda

Ketiganya menghasilkan "jangan pakai granularitas ini", tetapi implikasinya bagi perancang studi sama sekali berbeda.

| Mode | Gagal pada | Dapat diperbaiki dengan |
|---|---|---|
| **Tak teramati** | S0 | Mengubah **pengumpulan data** — mencatat pengenal blok |
| **Kekurangan blok** | S1 | Merekrut lebih banyak **blok** (bukan lebih banyak pengukuran) |
| **Desain bersilang** | S2 | Mengubah **desain**; sering tidak dapat diperbaiki setelah data terkumpul |

Pembedaan ini yang menjadikan C7 alat perancangan, bukan sekadar pemeriksa. Vonis "tidak layak" tanpa menyebut **sumbu mana** yang gagal tidak memberi tahu praktisi apa yang harus diubah.

> Hanya S1 dan S2 yang benar-benar "gagal". S0 **tak teramati** — lihat Prop. 0.

### 4.6 ✅ Instansiasi kedua — Challenge 2021 sebagai studi kasus batas keteramatan

Diagnostik yang hanya pernah mengeluarkan vonis "lolos" tidak membuktikan apa pun. PTB-XL memberi kasus **terpenuhi** pada `patient_id`; PhysioNet/CinC Challenge 2021 memberi kasus **tak teramati**, yaitu kegagalan pada sumbu yang sama sekali berbeda.

Dihitung oleh [scripts/verify_challenge2021.py](../scripts/verify_challenge2021.py); mentah di `results/raw/challenge2021_s0.json`.

**Struktur terverifikasi** (folder `ptb-xl` dikecualikan karena duplikat dataset utama):

| Sumber | Rekaman |
|---|---:|
| `ningbo` | 34.905 |
| `georgia` | 10.344 |
| `chapman_shaoxing` | 10.247 |
| `cpsc_2018` | 6.877 |
| `cpsc_2018_extra` | 3.453 |
| `ptb` | 516 |
| `st_petersburg_incart` | 74 |
| **Total non-duplikat** | **66.416** |

> Pemeriksaan silang: $66.416 + 21.837 = 88.253$ — persis total resmi dataset.

**Isi header (760 B, diperiksa langsung):** `#Age`, `#Sex`, `#Dx`, `#Rx`, `#Hx`, `#Sx`. **Tidak ada pengenal pasien.**

#### Vonis

**S0 TAK TERAMATI** untuk sumber dependensi *pasien*: tidak ada variabel yang terdokumentasi sebagai pengenal pasien. Menurut Prop. 0′, $K_1$ karena itu berhenti menjadi besaran terhitung dan berubah menjadi **asumsi tentang kelas $\mathfrak{P}$** yang wajib dinyatakan. Yang benar dinyatakan: *tidak dapat diketahui* apakah ada pasien yang menyumbang beberapa rekaman.

> Ini **bukan** klaim bahwa cakupan pasti rusak. Datanya bisa saja baik-baik saja. Yang hilang adalah **jaminannya**.
>
> Perhatikan pula bahwa batas $\alpha \ge \tfrac12$ dari Kor. 0′.1 **tidak** berlaku begitu saja di sini: ia menuntut $\mathcal{P}_\top$ admissible, yang pada dataset ini absurd secara domain (satu pasien dengan 66.416 EKG di tujuh institusi). Yang benar dilaporkan adalah bahwa $\mathfrak{P}$ tidak dapat ditetapkan dari data.

Satu-satunya partisi yang teramati adalah **sumber**, dengan $K = 7$. Karena $K_1 \le K$ selalu,

$$\alpha_{\min} \;=\; \frac{1}{K_1+1} \;\ge\; \frac{1}{8} \;=\; 0{,}125$$

> ⚠️ **Ruang lingkup klaim — rumusan yang boleh masuk naskah.** *Dengan partisi teramati yang tersedia pada metadata Challenge 2021, dan di bawah kondisi kelayakan sampel-hingga yang dipakai penelitian ini, target $\alpha < 0{,}125$ tidak memenuhi syarat kelayakan untuk jaminan non-trivial pada tingkat blok tersebut.*
>
> Yang **tidak boleh** ditulis: *"Challenge 2021 terbukti tidak dapat dipakai untuk conformal prediction."* Itu terlalu luas. Kesimpulannya bergantung pada **partisi yang teramati** dan pada **kerangka jaminan yang dipakai** — keduanya harus disebut.

Batas ini hanya memakai monotonisitas $K_1 \le K$ dan tidak bergantung pada rancangan split.

#### Biaya vonis

| | |
|---|---:|
| Data yang benar-benar diunduh | **~0,5 MB** (70 berkas indeks + 1 header) |
| Ukuran dataset penuh | **12,6 GB** |
| Rasio | **~25.000×** |

Inilah demonstrasi terkuat nilai praktis C7: vonis definitif diperoleh **sebelum** mengunduh dataset, **sebelum** preprocessing, dan **sebelum** melatih model.

> ⚠️ **Dua kesalahan tertangkap saat menyusunnya.**
>
> **Pertama**, versi awal skrip mencetak "S0 GAGAL" padahal belum berhasil membaca satu header pun — vonis itu adalah cabang *default* saat data kosong, bukan temuan. Ketiadaan bukti disajikan sebagai bukti ketiadaan. Skrip kini **menahan vonis** bila tidak ada header terbaca.
>
> **Kedua**, `cpsc_2018_extra` semula terhitung **453** alih-alih 3.453. PhysioNet memutus koneksi pada permintaan beruntun, tiga subfolder gagal terambil, dan kegagalannya **diabaikan diam-diam** sehingga menghasilkan hitungan kurang yang tampak sah. Ketahuan karena enam folder lain cocok persis dengan rujukan sementara satu meleset tepat 3.000. Skrip kini melaporkan subfolder yang gagal dan menandai hitungan sebagai tidak lengkap.

#### Posisi di naskah

Challenge 2021 **bukan** dataset generalisasi tingkat pasien — datanya tidak mendukung klaim itu. Ia juga **bukan** bukti empiris utama. Posisinya adalah **studi kasus diagnostik** yang menjelaskan *mengapa* S0 diperlukan:

> *Challenge 2021 memperlihatkan batas struktural diagnostik ini: ketika metadata tidak memuat variabel pengelompokan yang diperlukan untuk membentuk blok sadar-dependensi, S0 tidak dapat diverifikasi secara empiris. Ini wajib dilaporkan sebagai **batas keteramatan**, bukan sebagai bukti bahwa rekamannya independen.*

| Dataset | Peran | S0 |
|---|---|---|
| PTB-XL | Kasus utama; dependensi pasien + multi-label + hierarki | ✅ terpenuhi |
| MIT-BIH | Validasi dependensi kuat; blok = rekaman | ✅ terpenuhi |
| **Challenge 2021** | **Studi kasus batas keteramatan** | ⚠️ **tak teramati** |

| Kondisi | Tafsir |
|---|---|
| S0 terpenuhi | Struktur partisi dapat diamati |
| **S0 tak teramati** | **Pengenal tak tersedia → dependensi tak dapat diverifikasi** |
| S1 gagal | Target $\alpha$ tidak layak pada jumlah blok tersebut |
| S2 gagal | Struktur dependensi yang relevan belum terkendali |
| S0–S2 terpenuhi | Dataset memenuhi prasyarat diagnostik |

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
| 4 | Kor. 3.2 terbukti untuk keluarga HCP/Dunn, dan **terverifikasi konstruktif pada PTB-XL** (§4.2) | ✅ Klaim eksistensi tegak. Perumuman ke seluruh metode bebas-distribusi tetap **pertanyaan terbuka**, dinyatakan demikian di naskah |
| 5 | Kelayakan `site` bertumpu pada 37 site mungil yang `nurse`-nya kosong | Laporkan; kemungkinan rezim pengumpulan berbeda |
| 6 | §5.1 (cakupan-superset) **sepele** — HCP berlaku tanpa modifikasi | Jangan jual sebagai kontribusi; jadikan bagian Metode |
| 7 | §5.2 mengondisikan pada $\ell \in Y$ = seleksi bergantung-data | 🟡 Tulis argumen exchangeability intra-stratum secara formal |
| 8 | Prop. 4–5 memakai blok = `patient_id`; hasilnya berubah untuk granularitas lain | Jalankan ulang diagnostik bila granularitas berubah |

---

## 7. Yang belum dikerjakan di F1

- [x] ~~**C8** — perluasan HCP ke multi-label berhierarki~~ ✅ §5
- [x] ~~Proposisi 2 untuk $N_k$ tak seragam~~ ✅ Prop. 2′ (rata-rata harmonik), §2
- [x] ~~Estimator $\rho(t)$ beserta CI~~ ✅ [src/conformal/icc.py](../src/conformal/icc.py)
- [x] ~~🔴 Review statistikawan atas Kor. 3.2~~ ✅ **Tidak lagi menjadi penghalang.** Klaim eksistensi diverifikasi ekshaustif pada kekisi PTB-XL (§4.2); perumumannya tidak diklaim, melainkan dinyatakan terbuka
- [ ] 🟡 Review statistikawan atas §5.6
- [ ] Rumusan formal C2 (penutupan hierarkis) sebagai lema, memakai Kor. 5.2
- [ ] Kunci judul dan nama metode setelah C6/C7/C8 final
