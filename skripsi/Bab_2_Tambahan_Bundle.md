# Bab II — Tambahan Bundle (Ekspansi Tahap 3, 4, 5)

> **Catatan untuk pengerjaan di Word:**
> - File ini berisi **tiga blok ekspansi** yang menggantikan deskripsi singkat tahap 3, 4, dan 5 di draft Bab II:
>   1. **BLOK 1** — Ekspansi Tahap 3 (Perancangan Arsitektur Algoritma)
>   2. **BLOK 2** — Ekspansi Tahap 4 (Implementasi Sistem)
>   3. **BLOK 3** — Ekspansi Tahap 5 (Evaluasi dan Pengujian Eksperimental)
> - Seluruh sitasi sudah memenuhi rentang **2021–2026** (sesuai Opsi A).
> - Penomoran sub-section (2.2.x.y) menyesuaikan struktur akhir Bab II user.
> - Persamaan, gambar, dan tabel harus diketik ulang dengan fitur Word (Equation Editor, Insert Picture/Table).

---

## BLOK 1 — Ekspansi Tahap 3 (Perancangan Arsitektur Algoritma)

> Lokasi penyisipan: **mengganti seluruh isi Tahap "Perancangan Arsitektur Algoritma"** pada draft Bab II user.

---

### 2.2.3 Tahap Perancangan Arsitektur Algoritma

Tahap ini merupakan fase inti yang merancang logika aliran data (data flow) sistem perankingan, dimulai dari permintaan pengguna hingga penyajian daftar konten yang relevan. Perancangan mengadopsi pola **arsitektur rekomendasi dua-tahap (Two-Stage Recommender System)** [3] — yaitu pemisahan proses ke dalam fase **Pembangkitan Kandidat** (*Candidate Generation*) dan fase **Perankingan** (*Ranking*). Pemisahan ini bertujuan menyeimbangkan antara cakupan luas (broad recall) pada fase pertama dengan presisi tinggi (high precision) pada fase kedua, sebagaimana lazim diterapkan pada sistem rekomendasi berskala besar.

Aliran data sistem secara garis besar disajikan pada Gambar 2.x.

```
┌─────────────────────────────┐
│  Permintaan Pengguna (HTTP) │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Validasi & Autentikasi     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐    ┌─────────────────────┐
│  FASE I:                    │ ←─→│  Cache Redis        │
│  Candidate Generation       │    │  (kandidat pra-     │
│  (3 kolam paralel)          │    │   komputasi)         │
└──────────────┬──────────────┘    └─────────────────────┘
               ↓
┌─────────────────────────────┐
│  Deduplikasi Kandidat       │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  FASE II:                   │
│  Hybrid Scoring             │
│  - Cosine Similarity        │
│  - Exponential Time Decay   │
│  - Quality Score            │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Sorting + Cursor Pagination│
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Respons JSON ke Pengguna   │
└─────────────────────────────┘
```

**Gambar 2.x. Diagram Alir Arsitektur Algoritma Perankingan**

#### 2.2.3.1 Fase Pembangkitan Kandidat (Candidate Generation)

Fase pertama berfungsi sebagai **corong penyaring awal** yang mereduksi ruang pencarian dari skala katalog (jutaan konten potensial) menjadi himpunan kandidat berukuran kecil yang siap dievaluasi pada fase berikutnya. Pengumpulan kandidat dilakukan secara paralel dari **tiga kolam sumber** untuk mencegah isolasi preferensi pengguna (filter bubble) [3]:

**a. Kolam Trending (Trending-Based Pool)**

Kolam ini berisi konten dengan **agregasi metrik popularitas tertinggi**, yaitu pengurutan menurun berdasarkan kombinasi `rating_avg`, `used_count`, `watch_count`, dan `like_count`. Kolam Trending menjamin keragaman konten populer global hadir di kandidat akhir, sehingga pengguna tidak hanya melihat konten dari ceruk minatnya sendiri.

Maksimum 300 konten teratas dari kolam ini dimasukkan ke himpunan kandidat awal.

**b. Kolam Kebaruan (Freshness-Based Pool)**

Kolam ini berisi **300 konten paling mutakhir** berdasarkan timestamp publikasi (`created_at`), tanpa pertimbangan personalisasi atau popularitas. Kehadiran kolam ini memastikan konten yang baru diunggah memiliki kesempatan masuk ke fase scoring meskipun belum terakumulasi metrik interaksi.

**c. Kolam Minat (Interest-Based Pool)**

Kolam ini menyaring konten berdasarkan **kategori-kategori minat tertinggi pengguna** berdasarkan profil minat pada tabel `user_category_stats`. Sistem mengambil 12 kategori dengan skor minat tertinggi, kemudian untuk setiap kategori diambil 100 konten terkait paling mutakhir.

Hasil ketiga kolam digabungkan melalui operasi **himpunan-gabungan dengan deduplikasi** sehingga setiap konten hanya muncul satu kali pada himpunan kandidat akhir. Total kandidat yang masuk ke fase berikutnya berkisar antara 300 hingga 900 entri tergantung tumpang tindih antar kolam.

#### 2.2.3.2 Fase Perankingan (Hybrid Scoring)

Setiap konten dalam himpunan kandidat dievaluasi melalui formula **weighted linear combination** dari tiga pilar penilaian, sebagaimana didefinisikan secara teoretis pada Bab III sub-bab 3.2.6:

$$\text{Score}_{\text{final}}(c) = w_{1} \cdot \text{Cosine}(u, c) + w_{2} \cdot S_{\text{fresh}}(c) + w_{3} \cdot \text{Quality}(c)$$

dengan bobot empiris $w_{1} = 0{,}55$, $w_{2} = 0{,}25$, dan $w_{3} = 0{,}20$.

Komponen penilaian dijabarkan sebagai berikut:

1. **Cosine Similarity** ($\text{Cosine}(u, c)$) — mengukur kemiripan vektor minat pengguna terhadap vektor kategori konten (Persamaan 3.1).
2. **Exponential Time Decay** ($S_{\text{fresh}}(c)$) — mengukur kebaruan konten dengan parameter peluruhan $\lambda = 72$ jam (Persamaan 3.2).
3. **Quality Score** ($\text{Quality}(c)$) — kombinasi skor rata-rata penilaian dan engagement metrics ternormalisasi (Persamaan 3.4).

Justifikasi pemilihan bobot dan sifat matematis formula ini dirinci pada Bab III sub-bab 3.2.6.

#### 2.2.3.3 Fase Pengurutan dan Paginasi

Setelah seluruh kandidat memperoleh nilai $\text{Score}_{\text{final}}$, daftar diurutkan secara menurun (descending) dengan **kunci pengurutan komposit** untuk menjamin total ordering:

$$\text{ORDER BY} \quad \text{Score}_{\text{final}}(c) \text{ DESC} \rightarrow t_{c} \text{ DESC} \rightarrow \text{ID}(c) \text{ DESC}$$

Tie-breaker `created_at` dan `id` mencegah ambiguitas urutan ketika dua atau lebih konten memperoleh skor identik. Setelah pengurutan, sistem menerapkan **paginasi berbasis kursor (cursor-based pagination)** yang memungkinkan pengguna melakukan scroll feed secara berkelanjutan tanpa risiko duplikasi atau lewatan baris.

Hasil akhir berupa daftar konten teratas (default: 10 konten per halaman) yang dikemas dalam format **JSON** dan didistribusikan ke aplikasi klien melalui REST API.

#### 2.2.3.4 Penanganan Cold-Start

Untuk pengguna yang belum memiliki riwayat interaksi (cold-start), sistem menerapkan strategi **fallback bertingkat** yang dirinci pada Bab III sub-bab 3.2.1: pengguna anonim dilayani melalui Trending global, pengguna terautentikasi tanpa riwayat dilayani via cache `fyp:trending`, dan pengguna dengan preferensi onboarding mendapat skor dasar pada vektor minat. Pendekatan ini sejalan dengan rekomendasi pada penelitian terbaru tentang penanganan cold-start hibrida [N+2].

---

## BLOK 2 — Ekspansi Tahap 4 (Implementasi Sistem)

> Lokasi penyisipan: **mengganti seluruh isi Tahap "Implementasi Sistem"** pada draft Bab II user.

---

### 2.2.4 Tahap Implementasi Sistem

Tahap ini merealisasikan rancangan algoritma yang didefinisikan pada sub-bab sebelumnya menjadi sistem operasional yang dapat diakses melalui antarmuka REST API. Implementasi mengikuti paradigma **Clean Architecture** yang membagi tanggung jawab kode ke dalam lapisan-lapisan terstruktur, dengan tujuan menjaga *separation of concerns* dan memfasilitasi pengujian unit secara mandiri.

#### 2.2.4.1 Pemilihan Bahasa Pemrograman

Implementasi inti backend menggunakan **bahasa pemrograman Go (Golang) versi 1.24**. Pemilihan Go didasarkan pada karakteristik teknis yang sesuai dengan kebutuhan sistem perankingan real-time:

1. **Kompilasi statis (statically compiled)** — menghasilkan binary terkompilasi yang dieksekusi langsung tanpa interpreter, sehingga latensi runtime lebih rendah dibandingkan bahasa interpretif.
2. **Manajemen konkurensi melalui *goroutines*** — memungkinkan pemanggilan paralel ke berbagai kolam kandidat (Trending, Freshness, Interest) tanpa overhead thread sistem operasi.
3. **Built-in HTTP server yang ringan** — memfasilitasi pengembangan REST API tanpa ketergantungan framework eksternal yang berat.
4. **Manajemen memori otomatis (garbage-collected)** — mengurangi risiko *memory leak* tanpa mengorbankan performa secara signifikan.

#### 2.2.4.2 Arsitektur Lapisan (Layered Architecture)

Sistem dibagi ke dalam tiga lapisan utama:

**a. Lapisan HTTP Handler**

Lapisan terluar yang menerima permintaan HTTP dari aplikasi klien. Tanggung jawabnya meliputi:
- Validasi parameter HTTP (query string, header, autentikasi)
- Decoding cursor pagination
- Memanggil layanan logika bisnis
- Serialisasi respons ke format JSON

**b. Lapisan Service**

Lapisan tengah yang mengimplementasikan **logika bisnis** dan dispatching ke algoritma yang sesuai berdasarkan tipe feed yang diminta (FYP, Trending, Catalog, Following). Lapisan ini juga menangani validasi aturan bisnis seperti pembatasan akses fitur tertentu untuk pengguna dengan status non-aktif.

**c. Lapisan Repository**

Lapisan terdalam yang berinteraksi langsung dengan **persistence layer**. Seluruh kueri agregasi basis data, perhitungan skor hibrida, dan logika scoring algoritmik dieksekusi pada lapisan ini. Pemisahan ini memungkinkan implementasi cache (Redis) dan basis data utama (MySQL) menjadi *implementation detail* yang tidak terlihat oleh lapisan atas.

Pembagian tiga lapisan ini sejalan dengan praktik pengembangan sistem berbasis web modern yang berfokus pada keterbacaan dan kemampuan pemeliharaan kode [21].

#### 2.2.4.3 Komponen Pendukung

Sistem operasional bergantung pada tiga komponen infrastruktur pendukung:

**a. MySQL** — sebagai basis data relasional utama yang menyimpan persistensi data konten, pengguna, kategori, riwayat interaksi, serta tabel relasi yang mendukung kueri JOIN pada fase Candidate Generation.

**b. Redis** — sebagai *in-memory cache* yang menyimpan kandidat yang telah dipra-komputasi (`fyp:trending`, `fyp:fresh`, `fyp:category:{categoryID}`). Penggunaan Redis bertujuan menurunkan latensi rata-rata respons feed dari rentang ratusan milidetik menjadi puluhan milidetik.

**c. REST API** — antarmuka komunikasi dengan aplikasi klien menggunakan format JSON. Endpoint utama yang relevan dengan penelitian ini adalah `GET /api/posts?feed=fyp` yang mengembalikan rekomendasi yang dipersonalisasi sesuai algoritma hibrida. Pendekatan REST API berbasis web ini sejalan dengan penelitian Khotimah et al. (2022) yang menyatakan bahwa arsitektur web responsif efektif untuk distribusi data terstruktur [21].

#### 2.2.4.4 Konfigurasi Bobot Algoritma

Untuk memfasilitasi eksperimen sensitivitas dan ablation pada Tahap Evaluasi, bobot $w_{1}$, $w_{2}$, dan $w_{3}$ pada formula skor hibrida **diparametrisasi melalui environment variable**:

```
FYP_WEIGHT_COSINE=0.55
FYP_WEIGHT_FRESHNESS=0.25
FYP_WEIGHT_QUALITY=0.20
```

Konfigurasi ini memungkinkan penyetelan ulang bobot tanpa perlu mengompilasi ulang binary, sehingga memudahkan eksperimen iteratif. Validasi otomatis pada saat startup memastikan jumlah ketiga bobot sama dengan 1, sesuai kendala normalisasi (Persamaan 3.6).

---

## BLOK 3 — Ekspansi Tahap 5 (Evaluasi dan Pengujian Eksperimental)

> Lokasi penyisipan: **mengganti seluruh isi Tahap "Evaluasi dan Pengujian Eksperimental"** pada draft Bab II user.

---

### 2.2.5 Tahap Evaluasi dan Pengujian Eksperimental

Tahap akhir bertujuan memvalidasi secara empiris bahwa sistem yang diimplementasikan benar-benar memberikan kualitas rekomendasi yang lebih baik dibandingkan algoritma baseline konvensional, serta memenuhi tuntutan kinerja sistem yang dipersyaratkan untuk penyajian feed real-time. Validasi dilaksanakan melalui **empat skenario pengujian** yang saling melengkapi sebagaimana disajikan pada Tabel 2.x.

**Tabel 2.x. Skenario Pengujian Sistem**

| Kode | Skenario | Tujuan Pengujian | Metrik Utama |
|---|---|---|---|
| **S1** | Pengujian Akurasi Rekomendasi | Membandingkan kualitas urutan rekomendasi antara sistem hibrida dengan baseline konvensional | NDCG@K, Precision@K, Recall@K |
| **S2** | Pengujian Sensitivitas Parameter Bobot | Memvalidasi pemilihan bobot $(w_{1}, w_{2}, w_{3})$ secara empiris | NDCG@10 sebagai fungsi $w$ |
| **S3** | Pengujian Ablation (Kontribusi Komponen) | Memvalidasi kontribusi independen tiap pilar (Cosine, Freshness, Quality) | NDCG@10 per varian konfigurasi |
| **S4** | Pengujian Kinerja Sistem | Mengukur latensi dan throughput sistem pada beban kerja bervariasi | Response time (p50, p95, p99), throughput (RPS) |

Empat skenario tersebut dieksekusi secara sekuensial dengan dataset sintetis yang disusun secara deterministik untuk menjamin reproduksibilitas. Detail prosedur dan hasil masing-masing skenario disajikan pada Bab IV.

#### 2.2.5.1 Pengujian Akurasi Rekomendasi (Skenario S1)

Skenario ini mengevaluasi **kualitas urutan rekomendasi** menggunakan tiga metrik standar dari literatur sistem rekomendasi: **NDCG@K**, **Precision@K**, dan **Recall@K** (lihat Bab III sub-bab 3.2.7 untuk landasan teoretis).

Pengujian dilakukan terhadap 100 pengguna sintetis yang dibagi menjadi 5 arketipe (Tech Enthusiast, Foodie, Art Lover, Sports Fan, Generalist), dengan ground truth relevansi $rel(u, c) \in \{0, 1, 2, 3\}$ yang ditetapkan secara deterministik berdasarkan irisan kategori minat pengguna dengan kategori konten.

Sistem hibrida (PROP) dibandingkan dengan **dua baseline** yang sudah tersedia pada implementasi:
- **B1 — Chronological** (`feed=catalog`) — pengurutan berdasarkan waktu publikasi murni
- **B2 — Trending Global** (`feed=trending` anonim) — pengurutan berdasarkan agregasi popularitas

Pemilihan baseline ini bertujuan mengisolasi kontribusi **personalisasi** (PROP vs B1) dan kontribusi **penyesuaian terhadap minat individual** (PROP vs B2).

#### 2.2.5.2 Pengujian Sensitivitas Parameter Bobot (Skenario S2)

Skenario ini melakukan **grid search** pada ruang parameter $(w_{1}, w_{2}, w_{3})$ untuk memvalidasi pemilihan bobot yang diusulkan ($0{,}55$ / $0{,}25$ / $0{,}20$). Variasi bobot diuji pada interval $0{,}1$ hingga $0{,}7$ dengan kendala $w_{1} + w_{2} + w_{3} = 1$.

Untuk setiap kombinasi bobot, sistem direstart dengan environment variable yang sesuai, dataset sintetis dievaluasi, dan nilai NDCG@10 dicatat. Hasil divisualisasikan dalam bentuk *heatmap* tiga dimensi yang menunjukkan area parameter dengan performa optimal.

#### 2.2.5.3 Pengujian Ablation (Skenario S3)

Skenario ini menguji **empat varian konfigurasi** untuk memvalidasi bahwa setiap pilar (Cosine, Freshness, Quality) memberikan kontribusi independen terhadap performa akhir:

| Varian | $w_{1}$ (Cosine) | $w_{2}$ (Freshness) | $w_{3}$ (Quality) |
|---|---|---|---|
| Variant A — Only Cosine | 1,00 | 0,00 | 0,00 |
| Variant B — Cosine + Freshness | 0,70 | 0,30 | 0,00 |
| Variant C — Cosine + Quality | 0,70 | 0,00 | 0,30 |
| Variant D — Hybrid (proposed) | 0,55 | 0,25 | 0,20 |

NDCG@10 dievaluasi pada setiap varian dengan dataset yang sama. Apabila Varian D menghasilkan nilai NDCG@10 secara signifikan lebih tinggi dibandingkan varian A, B, dan C, maka kontribusi dari kombinasi ketiga pilar terbukti.

#### 2.2.5.4 Pengujian Kinerja Sistem (Skenario S4)

Skenario terakhir mengevaluasi **kemampuan sistem dalam menyajikan rekomendasi pada beban produksi**. Pengujian dilakukan menggunakan tools **Apache JMeter 5.6** dengan skenario pemanggilan endpoint `GET /api/posts?feed=fyp` pada beban berurutan: 1, 10, 50, 100, dan 500 pengguna konkuren.

Metrik yang diukur:
- **Response time** — diukur pada persentil ke-50 (p50, median), ke-95 (p95), dan ke-99 (p99) untuk menggambarkan performa typical maupun worst-case.
- **Throughput** — jumlah permintaan yang berhasil diselesaikan per detik (Requests Per Second / RPS).

Pengujian juga dilakukan pada dua kondisi cache:
- **Warm cache** — Redis sudah berisi kandidat pra-komputasi.
- **Cold cache** — Redis dikosongkan sebelum pengujian, sehingga seluruh kueri jatuh ke MySQL.

Komparasi kedua kondisi ini menunjukkan **dampak strategi caching** terhadap performa sistem.

#### 2.2.5.5 Lingkungan Pengujian dan Reproduksibilitas

Seluruh pengujian dieksekusi pada lingkungan tunggal (single-node) dengan spesifikasi yang dirinci pada Bab IV sub-bab 4.2.1. Penggunaan jaringan loopback (`127.0.0.1`) memastikan latensi yang terukur murni merefleksikan waktu pemrosesan internal tanpa dipengaruhi variabel jaringan eksternal.

Untuk menjamin reproduksibilitas, seluruh skrip pembangkitan dataset dan prosedur evaluasi menggunakan **random seed yang ditetapkan** (`seed = 42`). Skrip eksperimen didokumentasikan dalam bentuk Jupyter Notebook yang dilampirkan pada Lampiran skripsi.

---

## Daftar Pustaka yang Dirujuk pada Bundle Bab II

> Pastikan referensi-referensi berikut sudah ada pada Daftar Pustaka utama dengan nomor yang konsisten.

- **[3]** M. Al-Ghuribi, S. A. Noah, dan S. Tiun, "Hybrid Quality-Based Recommender Systems: A Systematic Literature Review," *IEEE Access*, 2024.
- **[21]** U. Khotimah, J. Z. Mutaqin, P. Sokibi, R. Adam, V. Asih, S. Santoso, dan W. Ilham, "Perancangan Sistem Informasi Pelayanan Administrasi Kependudukan Desa Candrajaya Berbasis Web," *Jurnal Pengabdian UCIC*, vol. 1, no. 2, 2022.
- **[N+2]** A. Yousef dan E. Asgarian, "A Hybrid Solution For The Cold Start Problem In Recommendation," *The Computer Journal*, vol. 67, no. 5, hal. 1637–1654, May 2024.

---

## Checklist Setelah di-Paste ke Word

- [ ] **BLOK 1** menggantikan section "Tahap Perancangan Arsitektur Algoritma" yang lama di Bab II.
- [ ] **BLOK 2** menggantikan section "Tahap Implementasi Sistem" yang lama.
- [ ] **BLOK 3** menggantikan section "Tahap Evaluasi dan Pengujian Eksperimental" yang lama.
- [ ] Sesuaikan penomoran sub-section (2.2.3, 2.2.4, 2.2.5) jika urutan akhir Bab II berbeda.
- [ ] Sesuaikan penomoran tabel (Tabel 2.x) dengan tabel-tabel sebelumnya di Bab II.
- [ ] Sesuaikan penomoran gambar (Gambar 2.x — Diagram Alir Arsitektur) dengan gambar-gambar lain di Bab II.
- [ ] Salin diagram alir arsitektur di BLOK 1 menggunakan tools diagram (draw.io / Lucidchart / Figma) dan import sebagai gambar.
- [ ] Persamaan di BLOK 1 (Score_final dan ORDER BY composite) dapat **dihilangkan** dari Bab II karena sudah dirujuk ke Bab III sub-bab 3.2.6 dan 3.2.7. Atau tetap dipertahankan dengan ketik ulang via Equation Editor.
- [ ] Periksa konsistensi notasi desimal (koma untuk Bahasa Indonesia: `0,55`).
- [ ] Verifikasi semua sitasi `[3]`, `[21]`, `[N+2]` sudah ada di Daftar Pustaka utama.
- [ ] Apabila Daftar Pustaka sudah di-renumber sesuai Mapping_Sitasi_Lama_ke_Baru.md, sesuaikan nomor sitasi di sini.

---

## Hubungan dengan Bab III dan Bab IV

| Konten | Berhubungan dengan |
|---|---|
| BLOK 1 — Perancangan Arsitektur Algoritma | Persamaan 3.5 (Hybrid Score) di Bab III sub-bab 3.2.6 |
| BLOK 2 — Implementasi Sistem | Bab IV sub-bab 4.1 (Implementasi Komponen Inti) |
| BLOK 3 — Skenario Pengujian | Bab IV sub-bab 4.2.3 hingga 4.2.6 (eksekusi S1, S2, S3, S4) |

Dengan ekspansi ini, **alur metodologi penelitian menjadi koheren end-to-end** dari rancangan algoritma → implementasi → eksperimen → analisis hasil, sebagaimana seharusnya pada skripsi yang menerapkan metode rekayasa perangkat lunak yang dipadukan dengan riset eksperimental komputasional.

---

## Sebelum Submit

Pastikan:

1. **Bab II Tahap 1** (Identifikasi & Analisis Kebutuhan) — sudah cukup pada draft user, **tidak perlu diubah**.
2. **Bab II Tahap 2** (Pengumpulan & Pra-pemrosesan Data) — sudah cukup pada draft user, **tidak perlu diubah**.
3. **Bab II Tahap 3, 4, 5** — gunakan BLOK 1, BLOK 2, BLOK 3 dari file ini.
4. **Daftar Pustaka** — sudah di-update sesuai Mapping_Sitasi_Lama_ke_Baru.md.
5. **Gambar diagram alir arsitektur** sudah dibuat dan disisipkan ke BLOK 1.

Apabila keempat poin di atas selesai, Bab II dianggap **siap submit** untuk konsultasi dengan dosen pembimbing.
