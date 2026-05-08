# Bab IV — Section 4.2.1 dan 4.2.2

> **Catatan untuk pengerjaan di Word:**
> - Penomoran section (4.2.1, 4.2.2, dst) menyesuaikan struktur Bab IV final.
> - Tabel di bawah ini wajib disalin ulang menggunakan fitur **Insert → Table** Word, bukan paste-as-text.
> - Sesuaikan angka spesifikasi (RAM, jumlah konten, dll) dengan kondisi nyata kamu sebelum submission.

---

## 4.2 Pengujian dan Evaluasi

Bab ini menguraikan tahapan pengujian terhadap sistem **Time-Aware Hybrid Ranking** yang telah diimplementasikan pada bab sebelumnya. Pengujian dirancang untuk memvalidasi dua aspek utama: (i) **akurasi rekomendasi** yang dihasilkan oleh formula skor hibrida (Persamaan 3.5), dan (ii) **kinerja sistem** dalam menyajikan rekomendasi tersebut secara real-time. Seluruh prosedur pengujian mengadopsi paradigma *black-box testing*, yaitu pengujian berbasis input-output tanpa mengevaluasi struktur internal kode sumber. Pendekatan ini dipilih karena lebih sesuai dengan konvensi evaluasi sistem rekomendasi pada literatur akademik [11], [13] sekaligus memastikan independensi hasil pengujian terhadap detail implementasi.

---

## 4.2.1 Lingkungan Pengujian (Testing Environment)

Lingkungan pengujian dirancang untuk merepresentasikan kondisi operasional sistem pada *production-like environment* dalam skala penelitian akademik. Pengujian dilakukan pada lingkungan tunggal (single-node setup) di mana komponen backend service, basis data MySQL, cache Redis, dan instrumen pengujian dijalankan pada satu mesin yang sama. Konfigurasi ini menjamin konsistensi pengukuran latensi dengan menghilangkan variabel jaringan eksternal yang dapat memengaruhi hasil.

### 4.2.1.1 Spesifikasi Perangkat Keras

Seluruh proses pengujian dieksekusi pada perangkat keras dengan spesifikasi sebagaimana ditunjukkan pada Tabel 4.1.

**Tabel 4.1 Spesifikasi Perangkat Keras Pengujian**

| Komponen | Spesifikasi |
|---|---|
| Processor | Intel Core i5-1135G7 / Apple M1 (8-core, 64-bit) |
| RAM | 16 GB DDR4 |
| Penyimpanan | SSD NVMe 512 GB |
| Sistem Operasi | macOS 14.0 / Ubuntu 22.04 LTS |
| Jaringan | Localhost (loopback `127.0.0.1`) |

Penggunaan jaringan loopback memastikan bahwa latensi yang terukur secara murni merefleksikan waktu pemrosesan internal sistem (CPU, memori, disk I/O), tanpa dipengaruhi variabel laten jaringan eksternal seperti kemacetan atau waktu propagasi paket.

### 4.2.1.2 Spesifikasi Perangkat Lunak

Tabel 4.2 menyajikan tumpukan teknologi (*tech stack*) yang digunakan, baik pada sistem yang diuji (System Under Test) maupun pada instrumen pengujian (Testing Tools).

**Tabel 4.2 Spesifikasi Perangkat Lunak Pengujian**

| Kategori | Komponen | Versi | Peran |
|---|---|---|---|
| **System Under Test** | Go (Golang) | 1.24 | Bahasa kompilasi backend service |
|  | go-chi/chi | v5 | Framework HTTP routing |
|  | MySQL | 8.0 | Basis data utama untuk konten dan relasi |
|  | Redis | 7.x | Cache in-memory kandidat FYP |
| **Testing Instrumentation** | Python | 3.11 | Bahasa skrip evaluasi akurasi rekomendasi |
|  | requests | 2.31 | HTTP client untuk pemanggilan API |
|  | pandas | 2.1 | Manipulasi dataset hasil eksperimen |
|  | numpy | 1.25 | Komputasi numerik |
|  | scikit-learn | 1.3 | Komputasi metrik NDCG, Precision, Recall |
|  | matplotlib | 3.8 | Visualisasi grafik hasil eksperimen |
|  | seaborn | 0.13 | Visualisasi statistik (heatmap, boxplot) |
|  | Jupyter Notebook | 7.0 | Dokumentasi prosedur eksperimen |
| **Performance Testing** | Apache JMeter | 5.6 | Pengujian beban (load testing) |
| **Containerization** | Docker | 27.x | Orkestrasi service |
| **Version Control** | Git | 2.45 | Pengelolaan kode sumber |

Pemilihan **Python** sebagai bahasa skrip pengujian akurasi didasarkan pada ketersediaan ekosistem pustaka yang matang untuk evaluasi sistem rekomendasi, terutama modul `sklearn.metrics.ndcg_score` yang menyediakan implementasi standar metrik *Normalized Discounted Cumulative Gain*. Walaupun sistem inti diimplementasikan menggunakan Go, pemisahan bahasa antara *system under test* dan *testing instrumentation* merupakan praktik umum pada penelitian sistem rekomendasi [11], [16] dan tidak memengaruhi validitas hasil karena pengujian bersifat *black-box* (komunikasi melalui antarmuka HTTP).

### 4.2.1.3 Konfigurasi Service untuk Pengujian

Sebelum pengujian dijalankan, beberapa konfigurasi service di-tuning untuk menjamin reproduksibilitas hasil:

1. **Connection Pooling MySQL** — jumlah koneksi maksimum diatur pada 20 koneksi paralel, sesuai konfigurasi production-like minimal.
2. **TTL Cache Redis** — masa berlaku entri cache diatur pada 5 menit untuk eksperimen *warm cache*, dan dinonaktifkan (TTL = 0) untuk eksperimen *cold cache*.
3. **Logging Level** — diset pada level `INFO` untuk menghindari overhead I/O dari logging `DEBUG`.
4. **Worker Pre-compute** — proses *background worker* yang menyimpan kandidat ke Redis dijalankan satu siklus penuh sebelum pengujian dimulai.

Pengaturan ini didokumentasikan agar hasil eksperimen dapat direplikasi oleh peneliti lain.

---

## 4.2.2 Skenario dan Dataset Pengujian

Karena penelitian ini mengusulkan algoritma baru pada platform yang belum memiliki riwayat interaksi pengguna nyata, dataset pengujian dibangun secara **sintetis (synthetic dataset)** dengan ground truth yang terdefinisi. Pendekatan dataset sintetis mengikuti praktik yang umum digunakan pada penelitian sistem rekomendasi tahap awal [11], [12] dan memungkinkan kontrol penuh terhadap karakteristik distribusi data.

### 4.2.2.1 Rancangan Dataset Sintetis

Dataset dirancang untuk menyimulasikan platform konten kreatif berbasis kecerdasan buatan dengan karakteristik distribusi yang representatif terhadap kondisi operasional. Komposisi dataset disajikan pada Tabel 4.3.

**Tabel 4.3 Komposisi Dataset Sintetis**

| Entitas | Jumlah | Karakteristik Distribusi |
|---|---|---|
| Pengguna (User) | 100 akun | Terbagi ke dalam 5 arketipe dengan distribusi merata (20 akun per arketipe) |
| Konten (Content) | 1.000 item | Distribusi kategori uniform (200 konten per kategori) |
| Kategori (Category) | 5 kategori | Bersifat *mutually exclusive*: Teknologi, Kuliner, Seni, Olahraga, Edukasi |
| Relasi Konten-Kategori | 1.500 baris | Setiap konten dapat dikaitkan dengan 1–3 kategori |
| Skor Minat Pengguna (`user_category_stats`) | dinamis | Diisi sesuai arketipe pada saat seeding |
| Riwayat Interaksi | dinamis | Disimulasikan untuk pengisian metrik engagement |

### 4.2.2.2 Arketipe Pengguna (User Archetypes)

Lima arketipe pengguna didefinisikan untuk merepresentasikan ragam profil minat yang umum dijumpai pada platform konten. Masing-masing arketipe ditandai oleh distribusi skor minat yang unik terhadap kelima kategori, sebagaimana ditunjukkan pada Tabel 4.4.

**Tabel 4.4 Distribusi Skor Minat per Arketipe Pengguna**

| Arketipe | Teknologi | Kuliner | Seni | Olahraga | Edukasi |
|---|---|---|---|---|---|
| Tech Enthusiast | 80 | 10 | 5 | 2 | 30 |
| Foodie | 5 | 80 | 20 | 5 | 5 |
| Art Lover | 5 | 15 | 80 | 2 | 25 |
| Sports Fan | 10 | 5 | 5 | 80 | 5 |
| Generalist | 25 | 25 | 25 | 25 | 25 |

Skor pada Tabel 4.4 secara langsung diisikan pada tabel `user_category_stats` saat fase seeding. Distribusi skor dirancang untuk memenuhi tiga kriteria evaluasi:

1. **Spesialisasi tinggi** (arketipe 1–4) — pengujian terhadap kemampuan sistem mengenali preferensi terfokus.
2. **Distribusi seimbang** (arketipe Generalist) — pengujian terhadap kondisi minat tersebar yang menguji kemampuan sistem menyajikan keberagaman konten.
3. **Cross-interest** (mis. Tech Enthusiast juga menyukai Edukasi) — pengujian terhadap relevansi multi-kategori.

### 4.2.2.3 Distribusi Konten

Konten sintetis dibangun dengan distribusi tiga dimensi: kategori, waktu publikasi, dan popularitas.

**a. Distribusi Kategori**

Konten didistribusikan secara uniform pada kelima kategori. Setiap konten dapat dikaitkan dengan 1 hingga 3 kategori untuk merepresentasikan konten *multi-topical* yang umum dijumpai pada platform nyata.

**b. Distribusi Waktu Publikasi**

Atribut `created_at` setiap konten didistribusikan pada rentang **0 hingga 30 hari** ke belakang dari waktu pengujian, mengikuti **distribusi seragam (uniform)**. Pemilihan rentang 30 hari dilakukan agar variasi nilai *Freshness Score* (Persamaan 3.2) dapat teramati secara meaningful, mengingat parameter peluruhan $\lambda = 72$ jam akan menyebabkan konten berusia di atas 7 hari memiliki skor freshness mendekati nol.

**c. Distribusi Popularitas (Engagement Metrics)**

Atribut interaksi seperti `like_count`, `used_count`, dan `watch_count` didistribusikan mengikuti **hukum pangkat (power law)** untuk menyimulasikan kondisi nyata di mana sebagian kecil konten sangat populer sementara sebagian besar konten memiliki interaksi sedang hingga rendah. Distribusi ini didefinisikan secara formal sebagai:

$$P(X = k) \propto k^{-\alpha}$$

dengan parameter $\alpha = 2{,}0$ yang merupakan eksponen umum pada distribusi kepopuleran konten media sosial. Atribut `rating_avg` didistribusikan pada rentang $[3{,}0, 5{,}0]$ dengan distribusi normal $\mathcal{N}(\mu = 4{,}2, \sigma = 0{,}5)$, mencerminkan kecenderungan rating cenderung tinggi pada konten yang sudah terkurasi.

### 4.2.2.4 Definisi Ground Truth

Untuk dapat menghitung metrik akurasi rekomendasi seperti NDCG, diperlukan definisi *ground truth* — yaitu nilai relevansi yang dianggap "benar" untuk setiap pasangan (pengguna, konten). Pada penelitian ini, nilai relevansi $rel(u, c)$ didefinisikan secara deterministik berdasarkan kecocokan kategori antara profil pengguna dan kategori konten:

$$rel(u, c) = \begin{cases}
3 & \text{jika} \quad |C(c) \cap K_{\text{top3}}(u)| \geq 2 \\
2 & \text{jika} \quad |C(c) \cap K_{\text{top3}}(u)| = 1 \\
1 & \text{jika} \quad |C(c) \cap K_{\text{any}}(u)| \geq 1 \\
0 & \text{selain itu}
\end{cases}$$

**[Notasi Equation Editor]**
```
rel(u, c) = 3   jika |C(c) ∩ K_top3(u)| ≥ 2
rel(u, c) = 2   jika |C(c) ∩ K_top3(u)| = 1
rel(u, c) = 1   jika |C(c) ∩ K_any(u)| ≥ 1
rel(u, c) = 0   selain itu
```

Keterangan:
- $C(c)$ adalah himpunan kategori yang dikaitkan dengan konten $c$.
- $K_{\text{top3}}(u)$ adalah tiga kategori dengan skor minat tertinggi pada profil pengguna $u$.
- $K_{\text{any}}(u)$ adalah seluruh kategori dengan skor minat positif pada profil pengguna $u$.

Dengan skema ini, setiap pasangan (pengguna, konten) menghasilkan nilai relevansi pada skala empat tingkat $\{0, 1, 2, 3\}$ — di mana nilai 3 menandakan relevansi tertinggi dan 0 menandakan tidak relevan. Nilai inilah yang akan menjadi acuan kebenaran (gold standard) saat menghitung metrik NDCG@K pada Sub-bab 4.2.3.

### 4.2.2.5 Skenario Pengujian

Empat skenario pengujian utama didefinisikan untuk mengevaluasi sistem secara komprehensif. Ringkasan skenario disajikan pada Tabel 4.5.

**Tabel 4.5 Skenario Pengujian**

| Kode | Skenario | Tujuan | Metrik Utama | Sub-bab |
|---|---|---|---|---|
| **S1** | Pengujian Akurasi Rekomendasi | Mengevaluasi kualitas urutan rekomendasi sistem hibrida dibandingkan baseline | NDCG@K, Precision@K, Recall@K | 4.2.3 |
| **S2** | Pengujian Sensitivitas Parameter Bobot | Menemukan kombinasi bobot $w_{1}, w_{2}, w_{3}$ yang optimal | NDCG@10 sebagai fungsi $w_i$ | 4.2.4 |
| **S3** | Pengujian Ablation (Kontribusi Komponen) | Memvalidasi bahwa setiap pilar (Cosine, Freshness, Quality) berkontribusi signifikan | NDCG@10 per varian konfigurasi | 4.2.5 |
| **S4** | Pengujian Kinerja Sistem | Mengukur latensi dan throughput sistem pada beban kerja yang bervariasi | Response time (p50, p95, p99), throughput (RPS) | 4.2.6 |

### 4.2.2.6 Strategi Komparasi Baseline (untuk Skenario S1)

Untuk Skenario S1 (Pengujian Akurasi), sistem hibrida yang diusulkan akan dibandingkan terhadap dua baseline yang sudah tersedia pada implementasi sistem. Pemilihan baseline ini didasarkan pada relevansi akademik dan kemudahan reproduksi.

**Tabel 4.6 Strategi Komparasi Baseline**

| Kode | Algoritma | Endpoint | Karakteristik |
|---|---|---|---|
| **B1** | Chronological (kronologis murni) | `GET /api/posts?feed=catalog` | Mengurutkan konten berdasarkan `created_at` secara menurun, tanpa personalisasi |
| **B2** | Trending (popularitas global) | `GET /api/posts?feed=trending` (anonim) | Mengurutkan konten berdasarkan agregasi metrik (rating, used, watch, like), tanpa personalisasi minat |
| **PROP** | Hybrid (sistem yang diusulkan) | `GET /api/posts?feed=fyp` (autentikasi) | Mengkombinasikan Cosine Similarity, Freshness, dan Quality dengan bobot $0{,}55 / 0{,}25 / 0{,}20$ |

Komparasi terhadap baseline B1 (Chronological) menyoroti **kontribusi personalisasi** yang dihasilkan sistem hibrida. Komparasi terhadap baseline B2 (Trending) menyoroti **kontribusi penyesuaian terhadap profil minat individual** yang menjadi pembeda utama dari pendekatan trending konvensional. Apabila sistem hibrida menghasilkan nilai NDCG yang lebih tinggi secara konsisten pada kedua komparasi, hipotesis penelitian dianggap terdukung secara empiris.

### 4.2.2.7 Reproduksibilitas

Seluruh skrip pembangkitan dataset, prosedur pemanggilan API, dan pasca-pemrosesan hasil eksperimen didokumentasikan dalam bentuk Jupyter Notebook yang dilampirkan pada Lampiran skripsi. Setiap eksperimen menggunakan *random seed* yang ditetapkan (`seed = 42`) untuk menjamin bahwa hasil pembangkitan data sintetis dan urutan pemilihan sampel pengujian dapat direplikasi secara identik oleh peneliti lain.

---

## Penutup Sub-bab 4.2.1 dan 4.2.2

Sub-bab ini telah memaparkan lingkungan pengujian yang mencakup spesifikasi perangkat keras, perangkat lunak, dan konfigurasi service, serta merancang dataset sintetis lengkap dengan ground truth yang akan menjadi dasar evaluasi pada sub-bab berikutnya. Sub-bab 4.2.3 hingga 4.2.6 selanjutnya akan menyajikan prosedur eksekusi serta hasil dari masing-masing skenario pengujian (S1 hingga S4).

---

## Daftar Pustaka yang Dirujuk

> Pastikan referensi-referensi berikut sudah tersedia pada Daftar Pustaka utama dengan nomor yang konsisten.

- [11] F. Ricci, L. Rokach, dan B. Shapira, "Recommender systems: introduction and challenges," dalam *Recommender systems handbook*, Boston, MA: Springer, 2015, hal. 1–34.
- [12] F. O. Isinkaye, Y. O. Folajimi, dan B. A. Ojokoh, "Recommendation systems: Principles, methods and evaluation," *Egyptian Informatics Journal*, vol. 16, no. 3, hal. 261–273, 2015.
- [13] E. Çano dan M. Morisio, "Hybrid recommender systems: A systematic literature review," *Intelligent Data Analysis*, vol. 21, no. 6, hal. 1487–1524, 2017.
- [16] K. Järvelin dan J. Kekäläinen, "Cumulated gain-based evaluation of IR techniques," *ACM Transactions on Information Systems (TOIS)*, vol. 20, no. 4, hal. 422–446, 2002.

---

## Checklist Setelah di-Paste ke Word

- [ ] Sesuaikan penomoran section (4.2.1, 4.2.2, dst) jika urutan akhir berbeda.
- [ ] Salin ulang seluruh tabel menggunakan **Insert → Table** Word, jangan paste-as-text.
- [ ] Periksa angka spesifikasi hardware/software — sesuaikan dengan kondisi nyata.
- [ ] Ketik ulang Persamaan ground truth menggunakan **Equation Editor**.
- [ ] Pastikan format penulisan desimal konsisten (koma untuk Bahasa Indonesia: `0,55`).
- [ ] Periksa konsistensi sitasi `[11]`, `[12]`, `[13]`, `[16]` dengan Daftar Pustaka.
- [ ] Tambahkan caption nomor tabel sesuai konvensi skripsi institusi (mis. "Sumber: Penulis, 2026" jika diperlukan).
- [ ] Atur line spacing dan margin sesuai template skripsi.
- [ ] Apabila template skripsi mensyaratkan Daftar Tabel di awal skripsi, tambahkan entri Tabel 4.1 hingga Tabel 4.6 ke daftar tersebut.
