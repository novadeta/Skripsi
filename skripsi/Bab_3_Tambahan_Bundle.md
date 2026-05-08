# Bab III — Tambahan Bundle (Referensi 2021–2026)

> **Catatan untuk pengerjaan di Word:**
> - File ini berisi **tiga blok konten** yang harus disisipkan ke Bab III:
>   1. **Ekspansi 3.2.1** — paragraf tambahan tentang Cold-Start Strategy
>   2. **Section baru 3.2.7** — Metrik Evaluasi Sistem Rekomendasi
>   3. **Section baru 3.2.8** — Pengujian Hipotesis Statistik
> - **Seluruh sitasi** sudah diperbarui menggunakan referensi tahun **2021–2026**.
> - Referensi lama ([11] Ricci 2015, [13] Çano 2017, [14] Han Kamber Pei 2011, [17] Järvelin Kekäläinen 2002) **dihapus**, diganti dengan paper terbaru.
> - Penomoran sitasi `[N+x]` mengindikasikan referensi baru yang harus ditambahkan ke Daftar Pustaka utama (lihat bagian akhir file).

---

## BLOK 1 — Ekspansi Section 3.2.1 (Cold-Start Strategy)

> Lokasi penyisipan: **di akhir Sub-bab 3.2.1 Sistem Rekomendasi**, setelah paragraf yang membahas keterbatasan CF dan CBF.

---

Untuk mengatasi masalah cold-start pada pengguna baru, sistem yang diusulkan menerapkan strategi penanganan **bertingkat (multi-tier fallback strategy)** yang dirancang sesuai konteks ketersediaan data setiap pengguna. Pendekatan ini sejalan dengan rekomendasi pada literatur sistem rekomendasi hibrida modern [3], yang menyatakan bahwa fallback bertingkat merupakan teknik efektif untuk menjaga ketersediaan rekomendasi pada kondisi data minim. Tiga tingkatan strategi yang diterapkan adalah sebagai berikut:

**a. Cold-Start Pengguna Anonim**

Apabila pengguna mengakses sistem tanpa autentikasi (anonymous user), profil minat berbentuk vektor preferensi belum tersedia. Pada kondisi ini, sistem secara otomatis melayani feed melalui **algoritma trending global**, yaitu pengurutan konten berdasarkan kombinasi metrik popularitas (rating, used count, watch count, like count) tanpa melibatkan komponen Cosine Similarity. Strategi ini memastikan bahwa pengguna baru tetap memperoleh rekomendasi konten populer yang relevan secara umum [N+1].

**b. Cold-Start Pengguna Terautentikasi Tanpa Riwayat**

Untuk pengguna yang telah mendaftar tetapi belum memiliki rekam jejak interaksi, vektor preferensi $\vec{U}$ memiliki norma $||\vec{U}|| = 0$. Pada kondisi ini, perhitungan Cosine Similarity (Persamaan 3.1) menghasilkan nilai nol untuk seluruh konten, sehingga formula skor hibrida (Persamaan 3.5) tidak dapat membedakan relevansi antar konten kandidat. Sebagai mitigasi, sistem mendeteksi kondisi $||\vec{U}|| = 0$ dan secara otomatis mengaktifkan **jalur fallback ke kandidat trending** yang telah dipra-komputasi pada cache. Dengan demikian, sistem tetap menyajikan rekomendasi tanpa menunggu pengumpulan data interaksi.

**c. Cold-Start dengan Preferensi Eksplisit dari Onboarding**

Untuk meminimalkan periode cold-start, sistem juga menyediakan mekanisme **penangkapan preferensi eksplisit** pada saat proses *onboarding* (registrasi awal). Pengguna diminta memilih kategori-kategori minat secara langsung. Preferensi ini disimpan pada tabel `user_category_preferences` dan ditambahkan sebagai **skor dasar (base score)** ke vektor preferensi pengguna $\vec{U}$. Penambahan skor dasar memberikan dorongan awal pada perhitungan Cosine Similarity sehingga personalisasi dapat aktif segera setelah registrasi, jauh sebelum pengguna menghasilkan riwayat interaksi yang substansial. Pendekatan hibrida semacam ini terbukti efektif untuk mempersingkat masa cold-start sebagaimana dilaporkan dalam survei terbaru [3], [N+2].

Kombinasi tiga strategi tersebut menjamin bahwa sistem **selalu memiliki jalur penyajian rekomendasi yang valid**, baik untuk pengguna baru maupun pengguna yang sudah terestablish. Pendekatan ini sekaligus menjadi salah satu pembeda utama penelitian ini dengan sistem rekomendasi yang hanya mengandalkan Collaborative Filtering murni.

---

## BLOK 2 — Section Baru 3.2.7 Metrik Evaluasi Sistem Rekomendasi

> Lokasi penyisipan: **setelah Sub-bab 3.2.6 Skor Hibrida Final**.

---

### 3.2.7 Metrik Evaluasi Sistem Rekomendasi

Setelah formula skor hibrida didefinisikan, langkah berikutnya pada metodologi penelitian adalah **melakukan validasi empiris** terhadap kualitas rekomendasi yang dihasilkan. Validasi ini memerlukan metrik kuantitatif yang dapat membandingkan urutan rekomendasi sistem dengan urutan ideal berdasarkan ground truth. Berdasarkan tinjauan literatur evaluasi sistem rekomendasi terbaru, tiga metrik dominan yang digunakan pada periode 2017–2022 adalah Precision (36% dari paper yang disurvei), NDCG (35%), dan Recall (30%) [N+1]. Penelitian ini mengadopsi ketiga metrik tersebut secara bersamaan: **Precision@K**, **Recall@K**, dan **Normalized Discounted Cumulative Gain (NDCG@K)** [N+1], [N+3].

Pemilihan ketiga metrik didasarkan pada karakteristik komplementer mereka — Precision menilai akurasi konten, Recall menilai cakupan, dan NDCG menilai kualitas urutan. Kombinasi ini memberikan gambaran multidimensi dari performa sistem [N+3].

#### 3.2.7.1 Precision@K dan Recall@K

**Precision@K** merupakan metrik dasar yang mengukur **proporsi konten yang relevan** dalam himpunan K rekomendasi teratas yang disajikan kepada pengguna. Secara formal, Precision@K didefinisikan melalui persamaan berikut [N+1]:

$$\text{Precision@K} = \frac{|\{c \in R_{K} : rel(u, c) > 0\}|}{K} \quad \text{(Persamaan 3.x)}$$

**[Notasi Equation Editor]**
```
Precision@K = |{c ∈ R_K : rel(u, c) > 0}| / K
```

**Recall@K** mengukur dimensi yang berbeda, yaitu **proporsi konten relevan yang berhasil ditemukan sistem** dari seluruh konten relevan yang ada pada katalog [N+1]:

$$\text{Recall@K} = \frac{|\{c \in R_{K} : rel(u, c) > 0\}|}{|\{c \in D : rel(u, c) > 0\}|} \quad \text{(Persamaan 3.x)}$$

**[Notasi Equation Editor]**
```
Recall@K = |{c ∈ R_K : rel(u, c) > 0}| / |{c ∈ D : rel(u, c) > 0}|
```

Keterangan persamaan:
- $R_{K}$ adalah himpunan K konten teratas yang direkomendasikan oleh sistem.
- $D$ adalah himpunan seluruh konten pada katalog.
- $rel(u, c)$ adalah nilai relevansi (ground truth) konten $c$ untuk pengguna $u$.
- $K$ adalah jumlah konten teratas yang dievaluasi.

Hasil Precision@K dan Recall@K berada pada rentang $[0, 1]$. Nilai mendekati 1 mengindikasikan performa sistem yang baik. Kedua metrik ini bersifat komplementer: sistem dengan Precision tinggi tetapi Recall rendah berarti rekomendasinya akurat namun terbatas, sedangkan sistem dengan Recall tinggi tetapi Precision rendah berarti cakupannya luas namun mengandung banyak konten tidak relevan. Idealnya, sistem unggul pada kedua metrik secara seimbang.

Perlu dicatat bahwa Precision dan Recall **tidak mempertimbangkan urutan** konten dalam top-K. Sebuah konten relevan yang muncul pada posisi pertama maupun pada posisi terakhir K mendapatkan kontribusi yang setara. Karakteristik ini menjadi keterbatasan kedua metrik ketika diterapkan pada sistem rekomendasi modern yang menampilkan konten secara berurutan, seperti pada feed media sosial [N+1].

#### 3.2.7.2 Normalized Discounted Cumulative Gain (NDCG@K)

Untuk menjawab keterbatasan Precision dan Recall dalam mengukur kualitas urutan, penelitian ini menggunakan metrik **NDCG@K** yang menjadi standar evaluasi sistem perankingan modern [N+3]. NDCG@K secara eksplisit memberikan **bobot penalti** pada konten relevan yang muncul pada posisi rendah, sehingga metrik ini sensitif terhadap urutan rekomendasi — sesuai dengan kebutuhan validasi sistem perankingan.

Komputasi NDCG@K terdiri dari tiga tahapan persamaan yang saling terkait:

**Tahap 1 — Discounted Cumulative Gain (DCG@K)**

DCG@K menghitung *gain* (perolehan relevansi) yang terdiskon berdasarkan posisi konten pada urutan rekomendasi:

$$DCG@K = \sum_{i=1}^{K} \frac{2^{rel_{i}} - 1}{\log_{2}(i+1)} \quad \text{(Persamaan 3.x)}$$

**[Notasi Equation Editor]**
```
DCG@K = Σ_{i=1}^{K} (2^rel_i - 1) / log_2(i+1)
```

di mana $rel_{i}$ adalah nilai relevansi konten yang menempati posisi ke-$i$ pada urutan rekomendasi sistem. Faktor diskon $\log_{2}(i+1)$ menyebabkan kontribusi konten pada posisi rendah berkurang secara logaritmik — dengan demikian, konten relevan di posisi 1 berkontribusi jauh lebih besar daripada di posisi 10.

**Tahap 2 — Ideal Discounted Cumulative Gain (IDCG@K)**

IDCG@K adalah nilai DCG **ideal** yang diperoleh apabila seluruh konten diurutkan sempurna berdasarkan relevansi dari yang tertinggi hingga terendah:

$$IDCG@K = \sum_{i=1}^{K} \frac{2^{rel_{i}^{*}} - 1}{\log_{2}(i+1)} \quad \text{(Persamaan 3.x)}$$

**[Notasi Equation Editor]**
```
IDCG@K = Σ_{i=1}^{K} (2^rel*_i - 1) / log_2(i+1)
```

di mana $rel_{i}^{*}$ menunjukkan nilai relevansi ke-$i$ pada urutan ideal (sorted descending).

**Tahap 3 — Normalisasi**

Skor akhir NDCG@K diperoleh dengan membagi nilai aktual DCG@K terhadap nilai idealnya:

$$NDCG@K = \frac{DCG@K}{IDCG@K} \quad \text{(Persamaan 3.x)}$$

**[Notasi Equation Editor]**
```
NDCG@K = DCG@K / IDCG@K
```

Hasil NDCG@K berada pada rentang $[0, 1]$, dengan interpretasi:
- $NDCG@K = 1$ : urutan rekomendasi identik dengan urutan ideal — performa sempurna.
- $NDCG@K = 0$ : tidak ada konten relevan ($rel > 0$) yang masuk ke top-K.
- Nilai antara 0 dan 1 mengindikasikan kualitas urutan secara proporsional.

Normalisasi terhadap IDCG memungkinkan **perbandingan lintas-pengguna** menjadi adil — pengguna dengan ground truth yang berbeda struktur tetap dapat dibandingkan karena kedua skor (aktual dan ideal) berada pada skala yang seragam [N+3].

#### 3.2.7.3 Pemilihan Skala Relevansi (Graded vs Binary)

Pada literatur evaluasi sistem rekomendasi, ground truth relevansi dapat direpresentasikan dalam dua bentuk: **biner** ($rel \in \{0, 1\}$) atau **bertingkat** ($rel \in \{0, 1, 2, \ldots, n\}$, dikenal sebagai *graded relevance*). Penelitian ini memilih pendekatan **graded relevance** dengan empat tingkat $\{0, 1, 2, 3\}$ sebagaimana akan dirinci pada Bab IV.

Pemilihan graded relevance didasarkan pada dua pertimbangan teoretis:
1. **Kompatibilitas dengan NDCG** — formula DCG menggunakan $2^{rel} - 1$ yang menghasilkan diferensiasi skor yang signifikan antar tingkat relevansi (contoh: $rel=3$ menghasilkan gain 7, $rel=2$ menghasilkan 3). Diferensiasi ini hanya bermakna pada graded relevance.
2. **Representasi realistis** — pada platform konten nyata, relevansi konten terhadap minat pengguna jarang bersifat biner. Konten dapat *sangat relevan*, *relevan moderat*, *agak relevan*, atau *tidak relevan*. Skala bertingkat lebih akurat menangkap nuansa ini [N+3].

#### 3.2.7.4 Pemilihan Nilai K

Penelitian ini mengevaluasi sistem pada tiga nilai K yang berbeda: **K = 5**, **K = 10**, dan **K = 20**. Pemilihan ini merepresentasikan tiga skenario penggunaan praktis:
- **K = 5** — first-screen recommendations, paling penting untuk perangkat mobile dengan layar terbatas.
- **K = 10** — typical feed page size, menjadi baseline benchmark industri pada aplikasi media sosial.
- **K = 20** — extended scroll, mengukur kualitas pada cakupan yang lebih luas saat pengguna melakukan eksplorasi dalam.

Pelaporan hasil pada ketiga nilai K bertujuan memvalidasi **konsistensi performa sistem** pada berbagai kedalaman, sesuai dengan rekomendasi praktik evaluasi pada literatur terbaru [N+1].

---

## BLOK 3 — Section Baru 3.2.8 Pengujian Hipotesis Statistik

> Lokasi penyisipan: **setelah Sub-bab 3.2.7 Metrik Evaluasi**.

---

### 3.2.8 Pengujian Hipotesis Statistik

Memperoleh nilai metrik evaluasi (Precision, Recall, NDCG) yang lebih tinggi pada satu sistem dibandingkan sistem lain **belum cukup** untuk menyimpulkan superioritas secara sah. Perbedaan rerata antara dua sistem dapat saja merupakan **kebetulan** akibat variasi sampel pengguna yang dipakai untuk pengujian. Untuk membedakan **perbedaan yang nyata** dari **fluktuasi acak**, diperlukan pendekatan **pengujian hipotesis statistik (statistical hypothesis testing)** [N+4].

Pengujian hipotesis statistik bertujuan menjawab pertanyaan: *"Apakah perbedaan performa yang terobservasi cukup besar untuk dianggap signifikan, atau dapat dijelaskan oleh variasi acak semata?"*

#### 3.2.8.1 Hipotesis Nol dan Hipotesis Alternatif

Setiap pengujian statistik dimulai dengan perumusan dua hipotesis yang saling eksklusif [N+4]:

**Hipotesis Nol ($H_{0}$)** — pernyataan bahwa **tidak ada perbedaan** antara dua sistem yang diuji. Pada penelitian ini, hipotesis nol untuk komparasi sistem hibrida (PROP) dengan baseline (B) dirumuskan sebagai:

$$H_{0}: \mu_{\text{PROP}} = \mu_{\text{B}}$$

**[Notasi Equation Editor]**
```
H_0: μ_PROP = μ_B
```

di mana $\mu_{\text{PROP}}$ dan $\mu_{\text{B}}$ adalah rata-rata nilai NDCG@K populasi untuk sistem proposed dan baseline.

**Hipotesis Alternatif ($H_{1}$)** — pernyataan bahwa **terdapat perbedaan** antara kedua sistem. Karena penelitian ini secara spesifik berhipotesis bahwa sistem hibrida lebih baik dari baseline, digunakan pengujian satu sisi (one-tailed):

$$H_{1}: \mu_{\text{PROP}} > \mu_{\text{B}}$$

**[Notasi Equation Editor]**
```
H_1: μ_PROP > μ_B
```

Tujuan pengujian adalah **menolak (reject)** $H_{0}$ apabila bukti empiris cukup kuat untuk mendukung $H_{1}$.

#### 3.2.8.2 Paired t-Test

Pemilihan jenis pengujian statistik bergantung pada karakteristik data. Pada penelitian ini, setiap **pengguna sintetis dievaluasi pada kedua sistem** (proposed dan baseline) dengan dataset yang sama. Karakteristik ini menyebabkan data berbentuk **berpasangan (paired data)** — yaitu setiap pengguna menghasilkan dua observasi yang saling terkait. Untuk konfigurasi data semacam ini, pengujian yang tepat adalah **paired t-test** [N+4].

Paired t-test mengevaluasi apakah **rata-rata selisih** antar kedua observasi pada setiap unit (pengguna) berbeda secara signifikan dari nol. Statistik uji $t$ dihitung melalui persamaan berikut [N+4]:

$$t = \frac{\bar{d}}{s_{d} / \sqrt{N}} \quad \text{(Persamaan 3.x)}$$

**[Notasi Equation Editor]**
```
t = d̄ / (s_d / √N)
```

Keterangan:
- $\bar{d}$ adalah rata-rata selisih nilai metrik antara sistem PROP dan baseline pada setiap pengguna:

$$\bar{d} = \frac{1}{N} \sum_{i=1}^{N} (NDCG_{\text{PROP},i} - NDCG_{\text{B},i})$$

- $s_{d}$ adalah standar deviasi selisih:

$$s_{d} = \sqrt{\frac{1}{N-1} \sum_{i=1}^{N} (d_{i} - \bar{d})^{2}}$$

- $N$ adalah jumlah pengguna yang diuji (pada penelitian ini, $N = 100$).
- $d_{i} = NDCG_{\text{PROP},i} - NDCG_{\text{B},i}$ adalah selisih untuk pengguna ke-$i$.

#### 3.2.8.3 Tingkat Signifikansi dan p-value

Hasil komputasi statistik $t$ kemudian dibandingkan dengan **distribusi t-student** untuk memperoleh nilai **p-value**, yaitu probabilitas memperoleh nilai $t$ sebesar yang teramati (atau lebih ekstrem) **dengan asumsi $H_{0}$ benar**. Interpretasinya:
- **p-value kecil** (< ambang batas) → bukti kuat untuk **menolak $H_{0}$**.
- **p-value besar** (> ambang batas) → bukti tidak cukup untuk menolak $H_{0}$; perbedaan teramati mungkin akibat variasi acak.

Ambang batas yang umum digunakan pada penelitian ilmu komputer dan rekayasa adalah **tingkat signifikansi $\alpha = 0{,}05$** [N+4]. Nilai ini berarti kita menerima risiko 5% untuk salah menolak $H_{0}$ ketika sebenarnya benar (kesalahan Tipe I). Dengan demikian, kriteria keputusan pengujian adalah:

$$\text{Keputusan} = \begin{cases}
\text{Tolak } H_{0} & \text{apabila } p\text{-value} < 0{,}05 \\
\text{Gagal Tolak } H_{0} & \text{apabila } p\text{-value} \geq 0{,}05
\end{cases}$$

**[Notasi Equation Editor]**
```
Keputusan = Tolak H_0          jika p-value < 0,05
            Gagal Tolak H_0    jika p-value ≥ 0,05
```

Pemilihan $\alpha = 0{,}05$ merupakan konvensi yang diterima luas pada literatur empiris dan dianggap memberikan keseimbangan antara sensitivitas (kemampuan mendeteksi perbedaan nyata) dan ketegasan (menghindari kesimpulan palsu) [N+4].

#### 3.2.8.4 Asumsi dan Keterbatasan

Paired t-test memiliki beberapa **asumsi statistik** yang perlu diperhatikan:
1. **Data berpasangan** — pasangan observasi berasal dari unit yang sama (terpenuhi pada penelitian ini, karena setiap pengguna diuji pada kedua sistem).
2. **Distribusi selisih mendekati normal** — distribusi $d_{i}$ tidak menyimpang signifikan dari distribusi normal. Asumsi ini cenderung terpenuhi ketika $N \geq 30$ berdasarkan **Teorema Limit Pusat (Central Limit Theorem)**, sehingga $N = 100$ pada penelitian ini memenuhi kriteria.
3. **Independensi antar pasangan** — hasil pengujian satu pengguna tidak memengaruhi hasil pengguna lain. Terpenuhi karena setiap pengguna sintetis bersifat independen.

Apabila salah satu asumsi tidak terpenuhi, alternatif non-parametrik seperti **Wilcoxon Signed-Rank Test** dapat digunakan. Namun pada konteks penelitian ini, ketiga asumsi paired t-test telah terpenuhi sehingga metode parametrik dipilih karena memiliki *statistical power* yang lebih tinggi dibanding alternatif non-parametriknya [N+4].

---

## Daftar Referensi Baru yang Harus Ditambahkan ke Daftar Pustaka

Empat referensi baru di bawah ini wajib ditambahkan ke Daftar Pustaka utama. Nomor `[N+x]` adalah placeholder — sesuaikan dengan nomor urut akhir setelah disisipkan ke daftar.

### [N+1] — Survei evaluasi sistem rekomendasi (untuk Precision/Recall)

> C. Bauer, "Exploring the Landscape of Recommender Systems Evaluation: Practices and Perspectives," *ACM Transactions on Recommender Systems*, vol. 2, no. 1, 2024.
>
> URL: https://christinebauer.eu/publications/bauer-2024-landscape/bauer-2024-landscape.pdf

**Mengapa dipilih:** menyajikan analisis komprehensif (57 paper, 2017–2022) tentang metrik evaluasi yang dipakai pada penelitian sistem rekomendasi, termasuk distribusi penggunaan Precision (36%), NDCG (35%), dan Recall (30%). Memberi dasar empiris untuk pemilihan tiga metrik pada penelitian ini.

### [N+2] — Cold-start hybrid solution (terbaru)

> A. Yousef dan E. Asgarian, "A Hybrid Solution For The Cold Start Problem In Recommendation," *The Computer Journal*, vol. 67, no. 5, hal. 1637–1654, May 2024.
>
> URL: https://academic.oup.com/comjnl/article-abstract/67/5/1637/7252293

**Mengapa dipilih:** paper terbaru (2024) yang khusus membahas penanganan cold-start dengan pendekatan hibrida — sangat sesuai dengan arsitektur sistem yang diusulkan pada penelitian ini.

### [N+3] — Survei evaluasi top-N recommendation (untuk NDCG)

> O. Jeunen et al., "On (Normalised) Discounted Cumulative Gain as an Off-Policy Evaluation Metric for Top-n Recommendation," *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, 2024.
>
> URL: https://dl.acm.org/doi/10.1145/3637528.3671687

**Mengapa dipilih:** publikasi terbaru pada konferensi top-tier (SIGKDD 2024) yang menganalisis NDCG sebagai metrik evaluasi sistem rekomendasi top-N. Menggantikan kebutuhan sitasi pada paper original Järvelin-Kekäläinen 2002 sambil tetap memberi referensi otoritatif modern.

### [N+4] — Statistical testing untuk evaluasi ML

> R. Rainio, J. Teuho, dan R. Klén, "Evaluation metrics and statistical tests for machine learning," *Scientific Reports*, vol. 14, art. 6086, 2024.
>
> URL: https://www.nature.com/articles/s41598-024-56706-x

**Mengapa dipilih:** paper terbaru dari Nature Scientific Reports (2024) yang membahas metrik evaluasi dan uji statistik untuk pembelajaran mesin. Menyediakan landasan formal untuk paired t-test, $\alpha = 0{,}05$, dan asumsi statistik — semuanya dengan referensi berkualitas tinggi yang mudah diverifikasi.

---

## Daftar Referensi yang Tetap Dipakai

> Referensi-referensi berikut sudah ada pada Daftar Pustaka user dan **masih dalam rentang 2021–2026**, sehingga tetap dipakai dengan nomor sitasi yang sama.

- **[3]** M. Al-Ghuribi, S. A. Noah, dan S. Tiun, "Hybrid Quality-Based Recommender Systems: A Systematic Literature Review," *IEEE Access*, 2024.

---

## Referensi Lama yang HARUS DIHAPUS

> Referensi-referensi berikut **dihapus** karena terbit di luar rentang 2021–2026. Apabila masih disitasi di bagian lain skripsi (Bab III, Bab II), perlu dicari pengganti dari Daftar Referensi yang Tetap Dipakai atau Referensi Baru di atas.

| Nomor | Pengarang | Tahun | Status |
|---|---|---|---|
| [10] | Asfi & Fitrianingsih | 2020 | ❌ Hapus |
| [11] | Ricci, Rokach, Shapira | 2015 | ❌ Hapus |
| [12] | Isinkaye, Folajimi, Ojokoh | 2015 | ❌ Hapus |
| [13] | Çano & Morisio | 2017 | ❌ Hapus |
| [14] | Han, Kamber, Pei | 2011 | ❌ Hapus |
| [15] | Campos, Díez, Cantador | 2014 | ❌ Hapus |
| [16] | Ding & Li | 2005 | ❌ Hapus |
| [17] | Järvelin & Kekäläinen | 2002 | ❌ Hapus |
| [18] | Sommerville | 2015 | ❌ Hapus |
| [22] | Andika, Kusnadi, Sokibi | 2020 | ❌ Hapus |

---

## ⚠️ PERINGATAN: Konsekuensi Terhadap Bab III dan Bab II

Karena 10 referensi lama dihapus, **bagian-bagian skripsi yang sudah ditulis user perlu di-revisi** untuk mengganti sitasi yang hilang. Daftar bagian terdampak:

### Pada Bab III (Landasan Teori) — Section yang sudah ditulis user

Pada draft Bab III user, terdapat sitasi-sitasi lama berikut yang sekarang harus diganti:

- **3.2.1 Sistem Rekomendasi**: sitasi `[10]`, `[11]`, `[12]`, `[13]` → ganti dengan `[3]`, `[N+1]`, `[N+2]`
- **3.2.2 Two-Stage Recommender**: sitasi `[11]`, `[12]`, `[13]` → ganti dengan `[3]`, `[N+1]`
- **3.2.3 Cosine Similarity**: sitasi `[11]`, `[14]` → ganti dengan `[3]`, `[N+1]` *(catatan: kalau dosen minta paper original cosine similarity, perlu cari pengganti baru)*
- **3.2.4 Time-Aware Ranking**: sitasi `[15]`, `[16]` → bisa diganti dengan `[2]` de Borba 2021, `[5]` Hassan 2022, atau `[7]` SAI Org 2022
- **3.2.5 Engagement Metrics**: sitasi `[14]` → ganti dengan `[N+1]` atau `[3]`

### Pada Bab II (Metodologi)

- **Daftar Pustaka**: hapus 10 referensi yang ditandai `❌`. Tambahkan 4 referensi baru `[N+1]` hingga `[N+4]`.

### Tabel 3.1 (Penelitian Terdahulu)

User saat ini punya 4 paper di tabel komparasi:
- [6] Rostami 2022 ✓ tetap
- [7] SAI Org 2022 ✓ tetap
- [8] Liu 2022 ✓ tetap
- [9] Pilgram 2025 ✓ tetap

Semua masih dalam rentang 2021–2026, **tidak perlu diubah**.

---

## Catatan Penting tentang Pengecualian Referensi Klasik

Beberapa konsep dalam skripsi ini berasal dari **paper seminal** yang berusia di luar 5 tahun terakhir:

| Konsep | Paper Seminal | Tahun |
|---|---|---|
| NDCG | Järvelin & Kekäläinen | 2002 |
| Cosine Similarity (formalisasi modern) | Salton & McGill | 1983 |

Pada **banyak universitas**, paper seminal seperti ini diperbolehkan tetap disitasi meskipun di luar 5 tahun, dengan justifikasi bahwa konsep tersebut adalah landasan asli yang tidak tergantikan. **Disarankan berkonsultasi dengan dosen pembimbing** apakah:

- **(A)** Aturan 5 tahun harus diterapkan ketat, atau
- **(B)** Paper seminal diperbolehkan dengan catatan tertentu

Apabila opsi **(A)** yang diterapkan, gunakan strategi penggantian yang sudah dibuat di atas (referensi `[N+3]` Jeunen 2024 untuk NDCG menggantikan Järvelin-Kekäläinen 2002).

Apabila opsi **(B)** disetujui dosen pembimbing, beberapa referensi seminal (terutama `[17]` Järvelin-Kekäläinen) dapat **dipertahankan** dengan catatan eksplisit di bab pendahuluan bahwa paper-paper seminal tersebut dipakai karena merepresentasikan landasan asli konsep yang dipakai.

---

## Checklist Setelah di-Paste ke Word

- [ ] **BLOK 1** disisipkan setelah paragraf cold-start di Sub-bab 3.2.1.
- [ ] **BLOK 2** menjadi Sub-bab baru 3.2.7 setelah 3.2.6 Skor Hibrida Final.
- [ ] **BLOK 3** menjadi Sub-bab baru 3.2.8 setelah 3.2.7.
- [ ] Sesuaikan penomoran Persamaan 3.x dengan urutan persamaan akhir di Bab III.
- [ ] Ketik ulang **seluruh persamaan** menggunakan **Insert → Equation** Word, jangan paste-as-text.
- [ ] **Tambahkan 4 referensi baru** (`[N+1]` Bauer 2024, `[N+2]` Yousef & Asgarian 2024, `[N+3]` Jeunen et al. 2024, `[N+4]` Rainio et al. 2024) ke Daftar Pustaka utama.
- [ ] **Hapus 10 referensi lama** ([10], [11], [12], [13], [14], [15], [16], [17], [18], [22]) dari Daftar Pustaka.
- [ ] Update sitasi di **bagian Bab III dan Bab II yang sudah ada** untuk mengganti referensi lama dengan referensi baru.
- [ ] Konsultasi dosen pembimbing tentang **pengecualian paper seminal** — apakah Järvelin-Kekäläinen 2002 boleh tetap dipakai.
- [ ] Periksa konsistensi notasi desimal (koma untuk Bahasa Indonesia: `0,05`).

---

## Hubungan dengan Bab Lain

| Konten Tambahan | Mendukung Bagian Mana |
|---|---|
| BLOK 1 — Cold-Start Strategy | Bab II Tahap 4 (Implementasi); Bab IV pengujian dengan pengguna sintetis baru |
| BLOK 2 — Metrik Evaluasi | Bab IV Sub-bab 4.2.3 (Pengujian Akurasi) — formula NDCG dirujuk dari sini |
| BLOK 3 — Pengujian Hipotesis | Bab IV Sub-bab 4.2.3.2 (Prosedur Langkah 6 — Uji Signifikansi); justifikasi $\alpha = 0{,}05$ |

Dengan tiga blok ini, **seluruh konsep yang dipakai pada Bab IV memiliki fondasi teoretis di Bab III**, sehingga tidak ada terminologi atau formula yang muncul "tanpa rujukan teoretis" — kondisi yang sering menjadi sasaran pertanyaan dosen penguji.
