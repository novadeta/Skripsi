# Bab IV — Section 4.2.3 Pengujian Akurasi Rekomendasi

> **Catatan untuk pengerjaan di Word:**
> - Penomoran section (4.2.3.x) menyesuaikan struktur Bab IV final.
> - Seluruh persamaan wajib diketik ulang menggunakan **Insert → Equation** Word, bukan paste-as-text.
> - Tabel di bawah adalah **template** yang akan diisi setelah eksperimen dijalankan.

---

## 4.2.3 Pengujian Akurasi Rekomendasi

Pengujian akurasi (Skenario S1) bertujuan untuk **memvalidasi secara empiris** bahwa formula skor hibrida (Persamaan 3.5) menghasilkan urutan rekomendasi yang lebih relevan dibandingkan dengan algoritma baseline yang konvensional. Pengujian dijalankan terhadap 100 pengguna sintetis yang telah dideskripsikan pada Sub-bab 4.2.2, di mana ground truth relevansi $rel(u, c) \in \{0, 1, 2, 3\}$ untuk setiap pasangan (pengguna, konten) telah ditetapkan secara deterministik.

Sub-bab ini terdiri atas empat bagian: (i) definisi metrik evaluasi yang digunakan, (ii) prosedur eksekusi pengujian, (iii) format pelaporan hasil, dan (iv) hasil dan pembahasan.

---

### 4.2.3.1 Metrik Evaluasi

Tiga metrik standar dari literatur Information Retrieval dan Recommender Systems digunakan untuk mengevaluasi kualitas rekomendasi: **NDCG@K**, **Precision@K**, dan **Recall@K**. Pemilihan ketiga metrik ini saling melengkapi — NDCG menilai kualitas urutan (rank quality), Precision menilai akurasi top-K, dan Recall menilai cakupan terhadap konten relevan.

#### a. Normalized Discounted Cumulative Gain @K (NDCG@K)

NDCG@K adalah metrik standar untuk mengevaluasi sistem perankingan dengan **graded relevance** (relevansi bertingkat) [16]. Metrik ini memberikan bobot penalti pada konten relevan yang muncul pada posisi rendah, sehingga menilai bukan hanya konten apa yang direkomendasikan, tetapi juga **urutannya**.

Komputasi NDCG@K terdiri dari tiga langkah:

**Langkah 1 — Discounted Cumulative Gain (DCG@K):**

$$DCG@K = \sum_{i=1}^{K} \frac{2^{rel_{i}} - 1}{\log_{2}(i+1)} \quad \text{(Persamaan 4.1)}$$

**[Notasi Equation Editor]**
```
DCG@K = Σ_{i=1}^{K} (2^rel_i - 1) / log_2(i+1)
```

di mana $rel_{i}$ adalah nilai relevansi konten yang menempati posisi ke-$i$ pada hasil rekomendasi sistem (dari ground truth $rel(u, c) \in \{0, 1, 2, 3\}$).

**Langkah 2 — Ideal Discounted Cumulative Gain (IDCG@K):**

$$IDCG@K = \sum_{i=1}^{K} \frac{2^{rel_{i}^{*}} - 1}{\log_{2}(i+1)} \quad \text{(Persamaan 4.2)}$$

**[Notasi Equation Editor]**
```
IDCG@K = Σ_{i=1}^{K} (2^rel*_i - 1) / log_2(i+1)
```

di mana $rel_{i}^{*}$ adalah nilai relevansi pada posisi ke-$i$ jika **seluruh** konten dari ground truth diurutkan secara menurun berdasarkan relevansi (urutan ideal).

**Langkah 3 — Normalisasi (NDCG@K):**

$$NDCG@K = \frac{DCG@K}{IDCG@K} \quad \text{(Persamaan 4.3)}$$

**[Notasi Equation Editor]**
```
NDCG@K = DCG@K / IDCG@K
```

Hasil NDCG@K berada pada rentang $[0, 1]$:
- **NDCG@K = 1** menandakan urutan rekomendasi sistem identik dengan urutan ideal.
- **NDCG@K = 0** menandakan tidak ada konten relevan (rel > 0) yang masuk top-K.
- Nilai antara mengindikasikan kualitas perankingan secara proporsional.

#### b. Precision@K

Precision@K mengukur **proporsi konten relevan** dalam K rekomendasi teratas:

$$\text{Precision@K} = \frac{|\{c \in R_{K} : rel(u, c) > 0\}|}{K} \quad \text{(Persamaan 4.4)}$$

**[Notasi Equation Editor]**
```
Precision@K = |{c ∈ R_K : rel(u, c) > 0}| / K
```

di mana:
- $R_{K}$ adalah himpunan K konten teratas yang direkomendasikan oleh sistem.
- $rel(u, c)$ adalah nilai ground truth relevansi konten $c$ untuk pengguna $u$.

Berbeda dengan NDCG, Precision **tidak mempertimbangkan urutan** dalam top-K. Sebuah konten relevan di posisi 1 maupun di posisi K menyumbang nilai yang sama. Karena itu Precision dilaporkan bersama NDCG sebagai komplementaritas: NDCG sensitif terhadap urutan, Precision sensitif terhadap proporsi.

#### c. Recall@K

Recall@K mengukur **proporsi konten relevan yang ditemukan** sistem dari seluruh konten relevan yang ada di dataset:

$$\text{Recall@K} = \frac{|\{c \in R_{K} : rel(u, c) > 0\}|}{|\{c \in D : rel(u, c) > 0\}|} \quad \text{(Persamaan 4.5)}$$

**[Notasi Equation Editor]**
```
Recall@K = |{c ∈ R_K : rel(u, c) > 0}| / |{c ∈ D : rel(u, c) > 0}|
```

di mana $D$ adalah seluruh dataset konten yang dievaluasi.

Recall melengkapi Precision dengan mengukur **cakupan** (coverage). Sistem dengan Precision tinggi tetapi Recall rendah berarti rekomendasinya akurat tetapi terbatas (banyak konten relevan terlewat); sistem dengan Recall tinggi tetapi Precision rendah berarti sebaliknya. Idealnya, sistem unggul pada kedua metrik.

#### d. Pemilihan Nilai K

Penelitian ini menggunakan tiga nilai K — **K = 5, K = 10, K = 20** — untuk merepresentasikan tiga skenario penggunaan:

- **K = 5** — first-screen recommendations, paling penting untuk user experience pada perangkat mobile.
- **K = 10** — typical feed page size, baseline industri umum untuk benchmark.
- **K = 20** — extended scroll, mengukur kualitas pada cakupan yang lebih luas.

Pelaporan hasil pada ketiga nilai K akan memperlihatkan **konsistensi performa sistem** pada berbagai kedalaman.

---

### 4.2.3.2 Prosedur Pengujian

Prosedur pengujian akurasi diorganisir dalam enam langkah operasional yang dijelaskan di bawah ini. Seluruh prosedur diotomatisasi melalui skrip `02_evaluate_accuracy.py` yang dilampirkan pada Lampiran B skripsi.

**Langkah 1 — Persiapan System Under Test**

Sebelum pengujian dimulai, sistem backend dijalankan dengan konfigurasi default:

```bash
# Bobot default yang diusulkan
FYP_WEIGHT_COSINE=0.55
FYP_WEIGHT_FRESHNESS=0.25
FYP_WEIGHT_QUALITY=0.20
go run cmd/main.go
```

Database test diisi dengan dataset sintetis hasil eksekusi `01_generate_dataset.py` (lihat Sub-bab 4.2.2). Cache Redis dibiarkan dalam kondisi *warm cache* dengan menjalankan worker pre-compute satu siklus penuh sebelum pengujian.

**Langkah 2 — Konfigurasi Baseline**

Tiga konfigurasi sistem dievaluasi sebagaimana dijelaskan pada Tabel 4.6 (Sub-bab 4.2.2.6):

| Kode | Konfigurasi | Endpoint API |
|---|---|---|
| **B1** | Chronological murni | `GET /api/posts?feed=catalog` |
| **B2** | Trending global | `GET /api/posts?feed=trending` (anonim) |
| **PROP** | Hybrid (proposed) | `GET /api/posts?feed=fyp` (autentikasi) |

Karena ketiga endpoint sudah tersedia pada implementasi sistem, baseline tidak memerlukan reimplementasi.

**Langkah 3 — Iterasi per Pengguna**

Untuk setiap pengguna sintetis $u$ dari 100 akun (lihat Tabel 4.4), skrip evaluasi menjalankan:

1. Memanggil endpoint baseline dan endpoint proposed dengan limit = 20 (untuk dapat menghitung ketiga nilai K sekaligus).
2. Menerima respons JSON yang berisi daftar konten terurut.
3. Mengekstrak `content_id` dari posisi 1 hingga 20.
4. Melakukan lookup ke ground truth dataset untuk setiap `content_id`.
5. Menghasilkan vektor $[rel_{1}, rel_{2}, \ldots, rel_{20}]$ yang menjadi masukan komputasi metrik.

**Langkah 4 — Komputasi Metrik per Pengguna**

Untuk setiap pengguna $u$ dan setiap konfigurasi (B1, B2, PROP), nilai NDCG@5, NDCG@10, NDCG@20, Precision@5, Precision@10, Precision@20, Recall@5, Recall@10, dan Recall@20 dihitung. Komputasi NDCG menggunakan fungsi `sklearn.metrics.ndcg_score` dari pustaka scikit-learn dengan parameter `k=K`.

**Langkah 5 — Agregasi Lintas Pengguna**

Skor metrik tiap pengguna dirata-ratakan untuk mendapatkan **mean metric** per konfigurasi. Pelaporan menggunakan dua statistik:

$$\overline{NDCG@K} = \frac{1}{N} \sum_{u=1}^{N} NDCG@K(u) \quad \text{(Persamaan 4.6)}$$

dengan $N = 100$ adalah jumlah pengguna sintetis. Standar deviasi $\sigma$ juga dihitung untuk menggambarkan konsistensi performa lintas pengguna.

**Langkah 6 — Uji Signifikansi Statistik**

Untuk menentukan apakah perbedaan rata-rata antar konfigurasi bersifat **signifikan secara statistik** (bukan kebetulan), dilakukan **paired t-test** antara NDCG@10 sistem proposed dan masing-masing baseline:

$$t = \frac{\bar{d}}{s_{d} / \sqrt{N}} \quad \text{(Persamaan 4.7)}$$

**[Notasi Equation Editor]**
```
t = d̄ / (s_d / √N)
```

di mana:
- $\bar{d}$ adalah rata-rata selisih nilai NDCG@10 antara sistem proposed dan baseline pada tiap pengguna.
- $s_{d}$ adalah standar deviasi selisih.
- $N = 100$ adalah jumlah sampel (pengguna).

Perbedaan dianggap **signifikan** apabila $p$-value $< 0{,}05$. Komputasi t-test menggunakan fungsi `scipy.stats.ttest_rel`.

---

### 4.2.3.3 Format Pelaporan Hasil

Hasil eksperimen disajikan dalam tiga bentuk: tabel ringkasan metrik, grafik perbandingan visual, dan analisis signifikansi statistik.

#### a. Template Tabel Ringkasan Metrik

**Tabel 4.7 Hasil NDCG@K untuk Tiga Konfigurasi (Mean ± Standar Deviasi)**

| Konfigurasi | NDCG@5 | NDCG@10 | NDCG@20 |
|---|---|---|---|
| B1 — Chronological | _xxx ± xxx_ | _xxx ± xxx_ | _xxx ± xxx_ |
| B2 — Trending Global | _xxx ± xxx_ | _xxx ± xxx_ | _xxx ± xxx_ |
| **PROP — Hybrid (proposed)** | **_xxx ± xxx_** | **_xxx ± xxx_** | **_xxx ± xxx_** |

**Tabel 4.8 Hasil Precision@K dan Recall@K**

| Konfigurasi | P@5 | P@10 | P@20 | R@5 | R@10 | R@20 |
|---|---|---|---|---|---|---|
| B1 — Chronological | _xxx_ | _xxx_ | _xxx_ | _xxx_ | _xxx_ | _xxx_ |
| B2 — Trending Global | _xxx_ | _xxx_ | _xxx_ | _xxx_ | _xxx_ | _xxx_ |
| **PROP — Hybrid (proposed)** | **_xxx_** | **_xxx_** | **_xxx_** | **_xxx_** | **_xxx_** | **_xxx_** |

#### b. Template Grafik Perbandingan

Hasil divisualisasikan melalui dua grafik utama:

**Gambar 4.x — Perbandingan NDCG@K antar konfigurasi**

Grafik batang berkelompok (grouped bar chart) dengan sumbu-X berisi tiga nilai K (5, 10, 20) dan tiga batang per kelompok untuk B1, B2, dan PROP. Sumbu-Y menampilkan nilai NDCG@K rata-rata.

**Gambar 4.y — Distribusi NDCG@10 per pengguna**

Box plot yang menunjukkan distribusi nilai NDCG@10 dari 100 pengguna untuk setiap konfigurasi. Box plot dipilih karena dapat menampilkan median, kuartil, dan outlier secara bersamaan — informatif untuk menilai konsistensi performa.

#### c. Template Tabel Uji Signifikansi

**Tabel 4.9 Hasil Paired t-test pada NDCG@10**

| Komparasi | $\bar{d}$ | $s_{d}$ | $t$-statistic | $p$-value | Signifikan? |
|---|---|---|---|---|---|
| PROP vs B1 | _xxx_ | _xxx_ | _xxx_ | _xxx_ | _Ya/Tidak_ |
| PROP vs B2 | _xxx_ | _xxx_ | _xxx_ | _xxx_ | _Ya/Tidak_ |

Pengisian "Signifikan?" mengikuti aturan:
- **Ya** jika $p < 0{,}05$
- **Tidak** jika $p \geq 0{,}05$

#### d. Template Analisis per Arketipe Pengguna

Untuk memberi wawasan **per-segmen**, hasil juga dipecah berdasarkan arketipe pengguna:

**Tabel 4.10 NDCG@10 per Arketipe Pengguna pada Konfigurasi PROP**

| Arketipe | Mean NDCG@10 | Std Dev |
|---|---|---|
| Tech Enthusiast | _xxx_ | _xxx_ |
| Foodie | _xxx_ | _xxx_ |
| Art Lover | _xxx_ | _xxx_ |
| Sports Fan | _xxx_ | _xxx_ |
| Generalist | _xxx_ | _xxx_ |

Tabel ini berfungsi untuk memvalidasi bahwa sistem **konsisten** memberikan rekomendasi berkualitas pada seluruh arketipe — bukan hanya unggul pada satu segmen tertentu.

---

### 4.2.3.4 Hasil dan Pembahasan

> **Catatan:** Bagian ini diisi setelah eksperimen dijalankan. Berikut struktur penulisan yang disarankan.

#### a. Hasil Komparasi Baseline

Hasil pengujian pada 100 pengguna sintetis disajikan pada Tabel 4.7 dan 4.8. _[Deskripsi naratif berdasarkan angka aktual hasil eksperimen.]_

Berdasarkan Tabel 4.7, sistem hibrida yang diusulkan (PROP) menghasilkan nilai NDCG@10 sebesar _[xxx]_, lebih tinggi _[xx%]_ dibandingkan baseline Chronological (B1) yang hanya mencapai _[xxx]_, dan _[xx%]_ lebih tinggi dibandingkan Trending Global (B2) sebesar _[xxx]_. Pola peningkatan ini konsisten pada ketiga nilai K (5, 10, 20), menunjukkan bahwa sistem hibrida unggul tidak hanya pada lapisan teratas (K=5) tetapi juga pada kedalaman yang lebih besar.

#### b. Analisis Statistik

Hasil paired t-test (Tabel 4.9) menunjukkan bahwa perbedaan nilai NDCG@10 antara sistem PROP terhadap baseline B1 _[signifikan/tidak signifikan]_ secara statistik dengan $p$-value = _[xxx]_. Demikian pula komparasi PROP vs B2 menghasilkan $p$-value = _[xxx]_. Hasil ini _[mendukung/tidak mendukung]_ hipotesis penelitian bahwa kombinasi Cosine Similarity, Exponential Time Decay, dan Quality Score menghasilkan rekomendasi yang lebih relevan dibandingkan algoritma baseline.

#### c. Analisis per Arketipe

Tabel 4.10 menyajikan performa sistem pada lima arketipe pengguna. _[Deskripsi mana arketipe yang paling/paling kurang baik direspon sistem.]_ Konsistensi nilai NDCG@10 pada seluruh arketipe — dengan rentang _[xxx]_ hingga _[xxx]_ — mengindikasikan bahwa sistem **tidak bias terhadap arketipe tertentu**, sejalan dengan tujuan personalisasi yang berkeadilan.

#### d. Diskusi Kelemahan dan Implikasi

Pengujian ini memiliki beberapa keterbatasan yang perlu diakui:

1. **Dataset sintetis** — meskipun dirancang untuk merepresentasikan distribusi nyata, dataset sintetis tidak sepenuhnya menangkap kompleksitas perilaku pengguna asli, seperti pergeseran minat (concept drift) dan perilaku eksplorasi.
2. **Ground truth deterministik** — pendekatan ini lebih cocok untuk memvalidasi *correctness* algoritma daripada efek psikologis preferensi manusia. Pengujian dengan pengguna nyata melalui *user study* atau A/B testing pada produksi disarankan sebagai langkah lanjutan.
3. **Ukuran dataset** — 100 pengguna dan 1.000 konten merupakan skala terbatas. Pada skala produksi (jutaan konten), kompleksitas komputasi dapat memengaruhi performa cosine similarity terhadap latensi.

Meski demikian, hasil pengujian ini memberikan **bukti empiris awal** bahwa pendekatan hibrida yang diusulkan layak dipertimbangkan untuk implementasi produksi, dengan catatan diperlukan pemantauan dan tuning lanjutan sesuai data nyata.

---

## Daftar Pustaka yang Dirujuk

> Pastikan referensi-referensi berikut sudah tersedia pada Daftar Pustaka utama dengan nomor yang konsisten.

- [16] K. Järvelin dan J. Kekäläinen, "Cumulated gain-based evaluation of IR techniques," *ACM Transactions on Information Systems (TOIS)*, vol. 20, no. 4, hal. 422–446, 2002.

---

## Checklist Setelah di-Paste ke Word

- [ ] Sesuaikan penomoran section (4.2.3.1, 4.2.3.2, dst) jika urutan akhir berbeda.
- [ ] Sesuaikan penomoran persamaan (4.1, 4.2, 4.3, ...) dengan urutan persamaan sebelumnya di Bab IV.
- [ ] Sesuaikan penomoran tabel (4.7 — 4.10) dengan tabel-tabel sebelumnya di Bab IV.
- [ ] Ketik ulang seluruh persamaan menggunakan **Insert → Equation** Word.
- [ ] Tabel hasil (4.7, 4.8, 4.9, 4.10) **biarkan kosong** sampai eksperimen dijalankan, lalu isi dengan angka aktual.
- [ ] Bagian "4.2.3.4 Hasil dan Pembahasan" — tulis ulang naratif berdasarkan angka aktual setelah eksperimen.
- [ ] Pasang **Gambar 4.x** dan **Gambar 4.y** setelah grafik dihasilkan dari `matplotlib`.
- [ ] Pastikan format penulisan desimal konsisten (koma untuk Bahasa Indonesia: `0,05`).
- [ ] Periksa konsistensi sitasi `[16]` dengan Daftar Pustaka utama.
- [ ] Apabila template skripsi mensyaratkan Daftar Tabel/Gambar, tambahkan entri Tabel 4.7-4.10 dan Gambar 4.x-4.y ke daftar tersebut.

---

## Hubungan dengan Skrip Eksperimen

Section ini akan diisi dengan hasil dari skrip yang akan dibuat selanjutnya:

| Skrip | Tugas | Output |
|---|---|---|
| `01_generate_dataset.py` ✅ | Generate dataset sintetis + ground truth | `data/*.csv`, `data/seed.sql` |
| `02_evaluate_accuracy.py` ⏳ | Hit endpoint API + hitung NDCG/Precision/Recall + paired t-test | `results/accuracy_results.csv`, plot PNG |

Setelah skrip 02 dijalankan, angka pada Tabel 4.7 — 4.10 dan grafik 4.x — 4.y akan terisi otomatis dari output skrip.
