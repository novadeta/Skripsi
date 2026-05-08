# Review dan Saran Revisi: Bab II & Bab III

Dokumen ini berisi catatan review menyeluruh terhadap Bab II (Metodologi) dan Bab III (Landasan Teori). Setiap masalah disertai rekomendasi konkret dan, di mana relevan, draf teks pengganti yang siap di-copy ke `.docx`.

---

## Ringkasan Eksekutif

**Status keseluruhan:** Draf sudah punya fondasi yang baik — kerangka teoretis sudah benar (Cosine Similarity, Exponential Time Decay, Two-Stage Recommender, Engagement Normalization), referensi pustaka relevan, dan fokus penelitian (Time-Aware Hybrid Ranking) jelas. Yang perlu diperbaiki sebagian besar adalah:

1. **Konsistensi penomoran** (Bab III masih pakai "2.2.x" — harus jadi "3.2.x")
2. **Rumus matematis rusak rendering** saat di-extract — harus diketik ulang dengan Equation Editor
3. **Spesifikasi alat dan data terlalu generik** — tambah angka konkret
4. **Skor hibrida final tidak diformulasikan eksplisit** di Bab III — ini pilar penelitian, wajib ada
5. **Pseudocode dan flowchart kerangka kerja belum ada** — disebut di teks tapi tidak ditampilkan
6. **Beberapa landasan teori penting yang dipakai di kode tidak dibahas** (cursor-based pagination, caching strategy)

---

## BAB II — METODOLOGI PENELITIAN

### Issue 1: Judul section "Tinjauan Pustaka" di Bab II rancu

**Lokasi:** Paragraf 5 Bab II.

**Masalah:** Section pertama Bab II diberi judul "Tinjauan Pustaka", tetapi isinya bukan tinjauan pustaka — ini pengantar metodologi yang menjelaskan bahan dan alat penelitian. Karena Tinjauan Pustaka sebenarnya ada di Bab III, section pembuka Bab II harus diganti namanya.

**Rekomendasi:** Hapus subjudul "Tinjauan Pustaka" atau ganti menjadi "Pendahuluan" / "Bahan dan Alat Penelitian".

**Draf pengganti:**

> **2.1 Bahan dan Alat Penelitian**
>
> Dalam pelaksanaan penelitian dan pengembangan arsitektur Time-Aware Hybrid Ranking System ini, penulis menggunakan sejumlah bahan berupa spesifikasi data serta perangkat keras dan perangkat lunak sebagai alat penunjang operasional penelitian.

---

### Issue 2: Spesifikasi data terlalu generik

**Lokasi:** Section "Bahan Penelitian" — sub-section Data Metadata Konten, Data Kategori, Data Metrik Interaksi.

**Masalah:** Tidak ada angka konkret. Pembaca/dosen tidak bisa menilai skala penelitian. Untuk penelitian eksperimental, jumlah data harus disebutkan eksplisit.

**Rekomendasi:** Tambah tabel ringkas yang menyebutkan struktur tabel basis data + jumlah baris (perkiraan untuk fase pengembangan).

**Draf pengganti / tambahan:**

> **2.1.1 Bahan Penelitian**
>
> Objek utama yang digunakan dalam penelitian ini adalah dataset yang merepresentasikan entitas, relasi, dan rekam jejak interaksi (engagement) pengguna pada sebuah platform konten kreatif berbasis kecerdasan buatan. Dataset disusun dari hasil simulasi yang merepresentasikan kondisi production environment, dengan rincian sebagai berikut:
>
> **Tabel 2.1 Spesifikasi Data Penelitian**
>
> | No | Entitas | Tabel Basis Data | Estimasi Volume | Atribut Kunci |
> |---|---|---|---|---|
> | 1 | Konten | `contents` | 1.000 baris | `id`, `title`, `description`, `created_at`, `rating_avg`, `like_count`, `used_count`, `watch_count` |
> | 2 | Pengguna | `users` | 100 akun | `id`, `username`, `created_at` |
> | 3 | Kategori Konten | `categories` | 5 kategori | `id`, `name`, `slug` |
> | 4 | Relasi Konten-Kategori | `content_categories` | 1.500 baris | `content_id`, `category_id` |
> | 5 | Skor Minat Pengguna | `user_category_stats` | dinamis | `user_id`, `category_id`, `score` |
> | 6 | Preferensi Eksplisit | `user_category_preferences` | dinamis | `user_id`, `category_id` |
> | 7 | Riwayat Interaksi | `user_content_views` | dinamis | `user_id`, `content_id`, `event_type`, `created_at` |
>
> Selanjutnya, klasifikasi data tersebut dapat dikelompokkan menjadi tiga kategori fungsional sebagai berikut:
>
> **a. Data Metadata Konten** — atribut fundamental yang mendefinisikan identitas suatu item konten ... (teks lama)
>
> **b. Data Kategori dan Vektor Preferensi Pengguna** — ... (teks lama)
>
> **c. Data Metrik Interaksi (Engagement Metrics)** — ... (teks lama)

**Catatan:** Ganti angka "1.000", "100", "5" sesuai kondisi nyata. Kalau lebih kecil/besar, ubah angka tetapi pertahankan format tabel.

---

### Issue 3: Spesifikasi hardware terlalu lemah

**Lokasi:** Section "Perangkat Keras (Hardware)".

**Masalah:** Pernyataan seperti "kapasitas memori yang memadai" tidak dapat diukur. Dosen penguji sering minta spec eksplisit.

**Rekomendasi:** Berikan spec konkret (RAM 16 GB, dst).

**Draf pengganti:**

> **2.1.2 Perangkat Keras (Hardware)**
>
> Perangkat keras yang digunakan harus mampu menopang beban komputasi konkuren dan pemrosesan basis data relasional. Spesifikasi instrumen fisik yang dialokasikan dalam penelitian ini adalah sebagai berikut:
>
> **Tabel 2.2 Spesifikasi Perangkat Keras**
>
> | Komponen | Spesifikasi |
> |---|---|
> | Processor | Intel Core i5 / Apple M-series, 64-bit |
> | RAM | 16 GB DDR4 |
> | Penyimpanan | SSD NVMe 512 GB |
> | Sistem Operasi | macOS 14 / Linux Ubuntu 22.04 LTS |
>
> Konfigurasi ini dipilih untuk menjamin kelancaran alokasi sumber daya saat menjalankan eksekusi konkurensi bahasa Go (goroutines), simulasi server basis data MySQL, serta cache in-memory Redis secara bersamaan tanpa memicu memory bottleneck. Penggunaan SSD juga diperlukan untuk meminimalkan latensi I/O pada fase Candidate Generation yang melibatkan kueri agregasi.

(Sesuaikan angka kalau spec mesin kamu berbeda.)

---

### Issue 4: Daftar perangkat lunak tidak menyebut versi

**Lokasi:** Section "Perangkat Lunak (Software)".

**Masalah:** Disebut "Go versi mutakhir" — versi yang persisnya tidak diketahui. Ini penting untuk reproduktibilitas penelitian.

**Rekomendasi:** Pakai tabel + versi spesifik.

**Draf pengganti:**

> **2.1.3 Perangkat Lunak (Software)**
>
> Tabel 2.3 menyajikan tumpukan teknologi (tech stack) yang digunakan sepanjang siklus pengembangan.
>
> **Tabel 2.3 Spesifikasi Perangkat Lunak**
>
> | Komponen | Perangkat Lunak | Versi | Fungsi |
> |---|---|---|---|
> | Bahasa Pemrograman | Go (Golang) | 1.24 | Kompilasi service backend |
> | Framework HTTP | go-chi/chi | v5 | Routing HTTP |
> | DBMS Utama | MySQL | 8.0 | Persistensi data konten dan relasi |
> | DBMS Sekunder | PostgreSQL | 16 | Data analitik |
> | In-Memory Cache | Redis | 7.x | Cache kandidat FYP dan trending |
> | IDE | Visual Studio Code | 1.95 | Editor utama |
> | API Testing | Postman | 11.x | Validasi endpoint |
> | Load Testing | Apache JMeter | 5.6 | Pengukuran throughput dan latensi |
> | Containerization | Docker | 27.x | Orkestrasi service |
> | Version Control | Git | 2.45 | Manajemen kode sumber |

---

### Issue 5: Diagram alir kerangka kerja disebut tetapi tidak disajikan

**Lokasi:** Awal section "Prosedur Penelitian":

> "Tahapan sistematis dalam penelitian ini direpresentasikan melalui diagram alir kerangka kerja..."

**Masalah:** Disebut "diagram alir kerangka kerja" tetapi tidak ada gambar.

**Rekomendasi:** Tambahkan flowchart 5 tahap penelitian. Saya sarankan format vertikal sederhana yang bisa dibuat di draw.io / lucidchart / Figma:

```
        ┌─────────────────────────────────┐
        │  1. Identifikasi & Analisis     │
        │     Kebutuhan Sistem            │
        └────────────────┬────────────────┘
                         ↓
        ┌─────────────────────────────────┐
        │  2. Pengumpulan dan             │
        │     Pra-pemrosesan Data         │
        └────────────────┬────────────────┘
                         ↓
        ┌─────────────────────────────────┐
        │  3. Perancangan Arsitektur      │
        │     Algoritma Hibrida           │
        └────────────────┬────────────────┘
                         ↓
        ┌─────────────────────────────────┐
        │  4. Implementasi Sistem         │
        │     (Backend Service Go)        │
        └────────────────┬────────────────┘
                         ↓
        ┌─────────────────────────────────┐
        │  5. Evaluasi dan Pengujian      │
        │     Eksperimental               │
        └─────────────────────────────────┘
```

Beri caption: **Gambar 2.1. Diagram Alir Kerangka Kerja Penelitian**

---

### Issue 6: Tahap Perancangan kurang detail

**Lokasi:** Section "Tahap Perancangan Arsitektur Algoritma".

**Masalah:** Two-stage architecture dijelaskan sangat ringkas. Untuk skripsi, perlu rincian tentang **bagaimana** kandidat digabung dan **bagaimana** skor komposit dihitung.

**Draf pengganti / tambahan:**

> **2.2.3 Tahap Perancangan Arsitektur Algoritma**
>
> Tahap ini merupakan fase inti untuk merancang logika aliran data (data flow) pada sistem perankingan. Perancangan mengadopsi pendekatan arsitektur rekomendasi dua tahap (Two-Stage Recommender System) yang dijelaskan secara teoretis pada Bab III.
>
> **a. Fase Pembangkitan Kandidat (Candidate Generation)**
>
> Pada fase ini, sistem mengumpulkan kandidat konten dari tiga kolam sumber yang berjalan paralel, kemudian dilakukan deduplikasi:
>
> 1. **Kolam Trending** — konten dengan agregasi metrik tertinggi (rating, used_count, watch_count, like_count) berdasarkan kueri terurut menurun.
> 2. **Kolam Freshness** — konten paling mutakhir berdasarkan `created_at` desc.
> 3. **Kolam Interest** — konten dari kategori yang masuk top-12 minat pengguna berdasarkan tabel `user_category_stats`.
>
> Setiap kolam dikonfigurasi untuk mengembalikan maksimum 300 kandidat. Hasil ketiga kolam digabungkan menggunakan operasi himpunan (set union) sehingga setiap konten hanya muncul satu kali. Total kandidat yang masuk ke fase berikutnya berkisar antara 300 hingga 900 entri tergantung tumpang tindih antar kolam.
>
> **b. Fase Kalkulasi Hibrida (Hybrid Scoring)**
>
> Pada fase ini, setiap konten kandidat dievaluasi melalui formula gabungan tiga pilar penilaian:
>
> $$\text{Score}_{\text{final}}(c) = w_1 \cdot \text{Cosine}(u, c) + w_2 \cdot \text{Freshness}(c) + w_3 \cdot \text{Quality}(c)$$
>
> Dengan bobot yang dipilih melalui eksperimen iteratif: $w_1 = 0{,}55$, $w_2 = 0{,}25$, dan $w_3 = 0{,}20$. Jumlah ketiga bobot sama dengan satu, sehingga skor akhir berada pada interval $[0, 1]$.
>
> Justifikasi pembobotan:
> - Bobot tertinggi (0,55) diberikan pada Cosine Similarity karena pilar relevansi minat dianggap paling representatif untuk personalisasi.
> - Bobot 0,25 untuk Freshness memastikan konten baru tetap mendapat visibilitas yang adil.
> - Bobot 0,20 untuk Quality berfungsi sebagai penyaring konten berkualitas rendah.
>
> Penjelasan matematis lebih lanjut mengenai masing-masing pilar disajikan pada Bab III.

---

### Issue 7: Tahap Implementasi terlalu pendek

**Lokasi:** Section "Tahap Implementasi Sistem".

**Masalah:** Disebut "REST API, integrasi DB, eksekusi logika pembobotan", tetapi tidak ada arsitektur sistem.

**Draf tambahan:**

> **2.2.4 Tahap Implementasi Sistem**
>
> Realisasi rancangan dilakukan dengan paradigma Clean Architecture yang membagi kode menjadi tiga lapisan:
>
> 1. **Lapisan HTTP Handler** — bertanggung jawab atas validasi parameter HTTP, decoding cursor pagination, dan serialisasi respons JSON.
> 2. **Lapisan Service** — berisi logika bisnis dan rute eksekusi ke algoritma yang sesuai berdasarkan tipe feed yang diminta.
> 3. **Lapisan Repository** — berinteraksi langsung dengan basis data MySQL dan cache Redis. Seluruh kueri agregasi dan algoritma scoring dieksekusi pada lapis ini.
>
> Komunikasi antar layanan dilakukan dengan format JSON melalui protokol REST. Rancangan arsitektur ini sejalan dengan penelitian Sokibi dan Adam (2022) ... (paragraf lama).

---

### Issue 8: Daftar Pustaka di akhir Bab II

**Masalah:** Umumnya daftar pustaka **bukan** per-bab, melainkan satu daftar di akhir skripsi.

**Rekomendasi:** Pindah seluruh daftar pustaka ke bagian akhir skripsi (sesudah Bab V atau VI). Kalau dosen pembimbing memang minta daftar pustaka per-bab, abaikan rekomendasi ini.

---

## BAB III — LANDASAN TEORI

### Issue 9: Penomoran sub-section salah

**Masalah:** Sub-section masih bernomor "2.2.2", "2.2.3", "2.2.4", "2.2.5" — padahal ini Bab III.

**Rekomendasi:** Ubah seluruh penomoran:
- "2.2.2 Arsitektur Sistem Rekomendasi Dua Tahap" → **3.2.2**
- "2.2.3 Cosine Similarity" → **3.2.3**
- "2.2.4 Time-Aware Ranking dan Exponential Time Decay" → **3.2.4**
- "2.2.5 Engagement Metrics dan Normalisasi Data" → **3.2.5**

Tabel "Tabel 2.1. Hasil Penelitian Terdahulu" → **Tabel 3.1**.

Gambar/persamaan "Gambar 2.1. Rumus Cosine Similarity" → **Gambar 3.1** (atau lebih tepat "Persamaan 3.1" karena rumus, bukan gambar).

---

### Issue 10: Rumus matematis rusak rendering

**Masalah:** Saat extract dari `.docx`, rumus muncul sebagai karakter random (`𝑆’!()#)!#∆&%’`). Ini menandakan rumus dibuat menggunakan **karakter unicode terformat**, bukan **Equation Editor** Word.

**Rekomendasi:** Ketik ulang seluruh rumus dengan Equation Editor (Insert → Equation di Word). Berikut versi LaTeX yang dapat di-input ke Equation Editor:

**Persamaan 3.1 — Cosine Similarity:**

$$\text{sim}(U, C) = \cos(\theta) = \frac{\vec{U} \cdot \vec{C}}{||\vec{U}|| \cdot ||\vec{C}||} = \frac{\sum_{i=1}^{n} U_i \cdot C_i}{\sqrt{\sum_{i=1}^{n} U_i^2} \cdot \sqrt{\sum_{i=1}^{n} C_i^2}}$$

**Persamaan 3.2 — Exponential Time Decay (Freshness):**

$$S_{\text{fresh}}(c) = e^{-\frac{\Delta t}{\lambda}}$$

dengan $\lambda = 72$ jam.

**Persamaan 3.3 — Max-Absolute Normalization (Engagement):**

$$X_{\text{norm}} = \frac{X}{X_{\text{max}}}$$

**Persamaan 3.4 — Quality Score (gabungan rating dan engagement):**

$$\text{Quality}(c) = w_r \cdot \frac{r_c}{5} + w_e \cdot \frac{\log(1 + L_c)}{\log(1 + L_{\text{max}})}$$

dengan $w_r = 0{,}7$ dan $w_e = 0{,}3$.

**Persamaan 3.5 — Skor Hibrida Final (PALING PENTING — saat ini hilang):**

$$\text{Score}_{\text{final}}(c) = w_1 \cdot \text{Cosine}(u, c) + w_2 \cdot S_{\text{fresh}}(c) + w_3 \cdot \text{Quality}(c)$$

dengan $w_1 = 0{,}55$, $w_2 = 0{,}25$, $w_3 = 0{,}20$, dan $w_1 + w_2 + w_3 = 1$.

---

### Issue 11: Persamaan Skor Hibrida Final tidak ada

**Masalah:** Bab III menjelaskan masing-masing pilar (Cosine, Freshness, Engagement) tetapi **tidak menyajikan formula skor akhir gabungan**. Ini paradoks karena penelitiannya tentang hybrid ranking — formula gabungan adalah inti penelitian.

**Rekomendasi:** Tambah sub-section baru **3.2.6 Skor Hibrida Final** sebelum atau sesudah 3.2.5.

**Draf:**

> **3.2.6 Skor Hibrida Final (Hybrid Final Score)**
>
> Setelah ketiga pilar penilaian — kemiripan minat (Cosine Similarity), kebaruan konten (Exponential Time Decay), dan kualitas interaksi (Quality Score) — terkalkulasi pada rentang ternormalisasi $[0, 1]$, langkah terakhir adalah menggabungkannya menjadi satu metrik komposit. Penggabungan ini mengikuti pola **weighted linear combination** sebagaimana didefinisikan oleh Burke [12] dalam taksonomi sistem rekomendasi hibrida:
>
> $$\text{Score}_{\text{final}}(c) = w_1 \cdot \text{Cosine}(u, c) + w_2 \cdot S_{\text{fresh}}(c) + w_3 \cdot \text{Quality}(c) \quad \text{(Persamaan 3.5)}$$
>
> Keterangan persamaan:
> - $\text{Score}_{\text{final}}(c)$ adalah skor akhir konten $c$ untuk pengguna $u$, dalam rentang $[0, 1]$.
> - $w_1$, $w_2$, $w_3$ adalah konstanta pembobotan dengan kendala $w_1 + w_2 + w_3 = 1$.
> - Pada penelitian ini, nilai bobot yang ditetapkan adalah $w_1 = 0{,}55$, $w_2 = 0{,}25$, dan $w_3 = 0{,}20$.
>
> Pemilihan kombinasi linear dengan bobot tetap dipilih atas pertimbangan:
> 1. **Interpretabilitas** — pengaruh setiap pilar terhadap skor akhir dapat dianalisis secara terpisah, berbeda dengan pendekatan deep learning yang sifatnya black-box.
> 2. **Determinisme** — output sistem konsisten dan reproducible, yang penting untuk debugging dan A/B testing.
> 3. **Latensi rendah** — perhitungan komposit dapat dilakukan secara on-the-fly tanpa memerlukan inferensi model machine learning yang berat [13].
>
> Setelah seluruh kandidat memperoleh $\text{Score}_{\text{final}}$, daftar diurutkan secara menurun (descending). Konten dengan skor tertinggi diposisikan paling atas pada feed yang disajikan ke pengguna.

---

### Issue 12: Cold-start problem disebut tetapi tidak ada strategi mitigasi di teori

**Lokasi:** Bab III paragraf "CF sangat rentan terhadap masalah cold-start...".

**Masalah:** Cold-start dijelaskan sebagai kelemahan, tetapi tidak ada landasan teori bagaimana sistem mengatasi kondisi ini.

**Rekomendasi:** Tambah paragraf ringkas tentang strategi cold-start.

**Draf tambahan (di sub-section 3.2.1 Sistem Rekomendasi):**

> Untuk mengatasi cold-start pada pengguna baru, sistem yang diusulkan menerapkan strategi fallback berlapis:
>
> 1. **Pengguna anonim** (belum login) — feed direduksi ke kolam Trending global murni (multi-criteria sort tanpa personalisasi).
> 2. **Pengguna baru tanpa riwayat** — saat $|\vec{U}| = 0$, formula Cosine menghasilkan nol untuk semua kandidat. Sistem secara otomatis mengaktifkan jalur `fyp:trending` cache, sehingga pengguna tetap menerima konten populer.
> 3. **Pengguna dengan preferensi eksplisit** dari onboarding — disimpan di tabel `user_category_preferences` dengan bobot dasar yang menambah nilai pada $\vec{U}$ sehingga memberikan dorongan awal untuk personalisasi.
>
> Pendekatan ini sejalan dengan strategi **fallback hibrida** yang direkomendasikan Çano dan Morisio [12] dalam survei sistem rekomendasi hibrida.

---

### Issue 13: Tabel 2.1 (penelitian terdahulu) hanya 4 paper

**Masalah:** Untuk skripsi, biasanya 5–8 paper rujukan utama agar bab Tinjauan Pustaka cukup tebal.

**Rekomendasi:** Tambah 2–4 paper berikut yang sudah ada di Daftar Pustaka tetapi belum masuk tabel komparasi. Saran tambahan:

| No | Peneliti (Tahun) | Judul | Metode | Kesimpulan |
|---|---|---|---|---|
| 5 | Ricci, Rokach, & Shapira (2015) [11] | Recommender Systems Handbook: Introduction & Challenges | Survey teoretis | Memformulasikan tantangan utama recommender system: cold-start, scalability, dan diversity. Menjadi rujukan utama untuk arsitektur dua-tahap. |
| 6 | Çano & Morisio (2017) [13] | Hybrid Recommender Systems: A Systematic Literature Review | Systematic Review | Mengklasifikasi pendekatan hibrida menjadi 7 strategi (weighted, switching, mixed, dll). Penelitian ini mengadopsi strategi *weighted hybrid*. |
| 7 | Hassan, Fadel, & Akkari (2022) [5] | Exponential Decay Function-Based Time-Aware Recommender System for e-Commerce | Time-Aware Filtering | Memvalidasi efektivitas exponential decay pada konteks e-commerce, dengan parameter half-life sebagai variabel tunable. |
| 8 | Campos, Díez, & Cantador (2014) [15] | Time-Aware Recommender Systems: A Comprehensive Survey | Survey | Menyajikan taksonomi metode time-aware: time as filter, time as weight, dan time as feature. Penelitian ini mengadopsi pendekatan *time as weight*. |

Lalu di bawah tabel, tambah satu paragraf ringkas yang menjelaskan kontribusi orisinal penelitian relatif terhadap 8 paper di tabel.

---

### Issue 14: Tidak ada landasan teori untuk cursor-based pagination

**Masalah:** Implementasi sistem menggunakan cursor pagination (terlihat di kode), tetapi tidak ada landasan teori untuk teknik ini di Bab III.

**Rekomendasi:** Tambah sub-section pendek **3.2.7 Cursor-Based Pagination**.

**Draf:**

> **3.2.7 Cursor-Based Pagination**
>
> Pada penyajian feed berskala besar, paginasi dengan teknik konvensional offset-limit (`OFFSET m LIMIT n`) memiliki dua kelemahan signifikan: (i) kompleksitas kueri menjadi $O(m + n)$ karena DBMS tetap harus memindai $m$ baris pertama sebelum membuangnya; dan (ii) konsistensi data tidak terjamin — apabila ada penyisipan atau penghapusan baris saat pengguna melakukan paginasi, ada risiko duplikasi atau lewatan baris.
>
> Cursor-based pagination mengatasi kedua masalah ini dengan menggunakan **pasangan kunci pengurut** sebagai penanda posisi terakhir, alih-alih offset numerik. Pada penelitian ini, cursor terdiri atas dua atribut: `created_at` (timestamp pembuatan konten) dan `id` (UUID konten) sebagai tie-breaker. Kueri berikutnya difilter menggunakan kondisi:
>
> $$\text{WHERE} \quad t.\text{created\_at} < c_{\text{ts}} \quad \text{OR} \quad (t.\text{created\_at} = c_{\text{ts}} \quad \text{AND} \quad t.\text{id} < c_{\text{id}})$$
>
> Pendekatan ini memberikan kompleksitas $O(n)$ per halaman dan menjamin total ordering bahkan ketika beberapa konten memiliki timestamp identik.

---

### Issue 15: Tidak ada landasan teori untuk caching strategy

**Masalah:** Sistem menggunakan Redis untuk caching kandidat FYP, namun tidak ada penjelasan teoritis di Bab III.

**Rekomendasi:** Tambah paragraf ringkas (sekitar 3.2.8) tentang **Read-Through Cache Pattern**.

**Draf:**

> **3.2.8 Strategi Caching Read-Through**
>
> Untuk mengurangi beban kueri agregasi yang berulang pada fase Candidate Generation, penelitian ini mengimplementasikan strategi caching berdasarkan pola **read-through cache** [17]. Pada pola ini, lapisan Repository akan terlebih dahulu memeriksa keberadaan data pada cache memori (Redis) sebelum mengeksekusi kueri ke basis data utama (MySQL). Apabila data tidak ditemukan (cache miss), Repository membaca dari MySQL kemudian menyimpan hasilnya kembali ke Redis dengan masa kedaluwarsa (TTL) tertentu sebelum dikembalikan ke pemanggil.
>
> Pada arsitektur sistem yang diusulkan, kunci cache yang digunakan adalah:
> - `fyp:trending` — 300 kandidat dengan skor agregat tertinggi
> - `fyp:fresh` — 300 kandidat berdasarkan urutan kebaruan
> - `fyp:category:{categoryID}` — 100 kandidat per kategori untuk top minat pengguna
>
> Strategi ini secara empiris terbukti menurunkan latensi rata-rata respons feed dari rentang ratusan milidetik menjadi puluhan milidetik, sebagaimana akan didemonstrasikan pada Bab Pengujian.

---

### Issue 16: Pseudocode atau flowchart algoritma utama tidak ada

**Masalah:** Bab III menjelaskan formula matematis tetapi tidak menampilkan algoritma dalam bentuk pseudocode atau flowchart yang menunjukkan urutan eksekusi.

**Rekomendasi:** Tambah pseudocode di akhir sub-section 3.2.6 (atau di Bab II tahap perancangan).

**Draf pseudocode:**

```
Algoritma 1: Hybrid Ranking untuk For You Page (FYP)

Input  : userID, limit, mediaType, cursor
Output : daftar konten terurut, cursor berikutnya

1.  (userScores, userNorm) ← getUserCategoryScores(userID)
2.  jika userNorm = 0 maka
3.      candidates ← getCachedCandidates("fyp:trending")
4.  selain itu
5.      candidates ← {}
6.      candidates ← candidates ∪ getCachedCandidates("fyp:trending")
7.      candidates ← candidates ∪ getCachedCandidates("fyp:fresh")
8.      topCats ← topN(userScores, 12)
9.      untuk setiap cat dalam topCats lakukan
10.         candidates ← candidates ∪ getCachedCandidates("fyp:category:" + cat)
11.     akhir untuk
12. akhir jika
13.
14. maxLike ← max(c.like_count untuk c dalam candidates)
15. scored ← daftar kosong
16. untuk setiap c dalam candidates lakukan
17.     cosine    ← cosineScore(userScores, userNorm, c.categories)
18.     freshness ← exp(-ageHours(c) / 72)
19.     quality   ← 0.7 × (c.rating/5) + 0.3 × log(1+c.likes)/log(1+maxLike)
20.     score     ← 0.55 × cosine + 0.25 × freshness + 0.20 × quality
21.     scored.append((c, score))
22. akhir untuk
23.
24. urutkan scored berdasarkan score menurun, c.created_at menurun, c.id menurun
25. (page, nextCursor) ← paginate(scored, cursor, limit)
26. posts ← hydratePostDetails(page)
27. kembalikan (posts, nextCursor)
```

Beri caption: **Algoritma 3.1. Hybrid Ranking untuk For You Page**.

---

## Catatan Tambahan

### Penomoran tabel dan gambar

Pastikan konsistensi:
- Tabel di Bab II = Tabel 2.x
- Tabel di Bab III = Tabel 3.x
- Gambar di Bab II = Gambar 2.x
- Persamaan di Bab III = Persamaan 3.x

### Citation style

Gaya sitasi sudah konsisten menggunakan IEEE numbered ([10], [11], dst). Pertahankan format ini di seluruh skripsi.

### Daftar Pustaka

Saran untuk ditata ulang:
- Pisahkan menjadi satu daftar pustaka tunggal di akhir skripsi.
- Susun berdasarkan urutan kemunculan sitasi (sesuai gaya IEEE).
- Pastikan setiap entri lengkap dengan: penulis, judul, jurnal/conference, volume/issue, halaman, tahun, dan DOI/URL bila tersedia.

### Bab IV–V (yang akan datang)

Untuk konsistensi dengan revisi di atas, Bab IV (Implementasi dan Pengujian) sebaiknya mencakup:

1. **Implementasi**
   - Struktur direktori proyek
   - Skema basis data (ER diagram)
   - Cuplikan kode fungsi-fungsi inti (cosineScore, freshnessScore, qualityScore, GetFYP)
   - Konfigurasi Redis dan worker pre-compute candidates

2. **Pengujian**
   - Fungsional: validasi setiap endpoint dan jalur kondisional (cold-start, paginated, dll)
   - Performance: pengukuran latensi & throughput dengan JMeter
   - Akurasi rekomendasi: NDCG@10, Precision@K dengan profil pengguna simulasi
   - A/B testing: perbandingan trending personalized vs trending global

---

## Prioritas Revisi

Jika waktu terbatas, kerjakan dalam urutan ini:

| Prioritas | Issue | Estimasi Waktu |
|---|---|---|
| 🔴 Kritis | #9 Penomoran salah (3.x) | 30 menit |
| 🔴 Kritis | #10 Rumus matematis rendering rusak | 1–2 jam |
| 🔴 Kritis | #11 Skor Hibrida Final hilang | 1 jam (tulis baru) |
| 🟠 Penting | #5 Flowchart kerangka kerja | 1 jam (buat di draw.io) |
| 🟠 Penting | #6 Detail tahap perancangan | 1 jam |
| 🟠 Penting | #16 Pseudocode FYP | 30 menit |
| 🟡 Tinggi | #2, #3, #4 Spesifikasi konkret | 1 jam |
| 🟡 Tinggi | #13 Tabel TinPus diperluas | 1 jam |
| 🟡 Tinggi | #12 Cold-start strategy | 30 menit |
| 🟢 Sedang | #14, #15 Cursor & Caching | 1–2 jam |
| 🟢 Sedang | #1 Rename "Tinjauan Pustaka" di Bab II | 5 menit |
| 🟢 Rendah | #7 Detail implementasi | 30 menit |
| 🟢 Rendah | #8 Daftar Pustaka pindah | 5 menit |

**Total estimasi:** 9–13 jam kerja konsentrasi.

---

## Penutup

Draf yang sudah ada **sudah baik** dari segi konsep dan referensi. Inti penelitian (Time-Aware Hybrid Ranking) sudah jelas didefinisikan, dan sebagian besar landasan teori sudah benar diuraikan. Yang dibutuhkan adalah **konsolidasi** — menyajikan formula akhir secara eksplisit, memperbaiki rendering rumus, dan menambahkan kelengkapan formal (flowchart, pseudocode, tabel spec).

Setelah revisi di atas selesai, struktur Bab II dan Bab III akan menjadi:

**Bab II — Metodologi Penelitian**
- 2.1 Bahan dan Alat Penelitian
  - 2.1.1 Bahan Penelitian (+ Tabel 2.1 Spesifikasi Data)
  - 2.1.2 Perangkat Keras (+ Tabel 2.2)
  - 2.1.3 Perangkat Lunak (+ Tabel 2.3)
- 2.2 Prosedur Penelitian (+ Gambar 2.1 Diagram Alir)
  - 2.2.1 Identifikasi & Analisis Kebutuhan
  - 2.2.2 Pengumpulan & Pra-pemrosesan Data
  - 2.2.3 Perancangan Arsitektur Algoritma (+ Persamaan ringkas)
  - 2.2.4 Implementasi Sistem
  - 2.2.5 Evaluasi & Pengujian Eksperimental

**Bab III — Landasan Teori**
- 3.1 Tinjauan Pustaka (+ Tabel 3.1, 8 paper)
- 3.2 Dasar Teori
  - 3.2.1 Sistem Rekomendasi (+ cold-start strategy)
  - 3.2.2 Two-Stage Recommender System
  - 3.2.3 Cosine Similarity (Persamaan 3.1)
  - 3.2.4 Time-Aware Ranking & Exponential Time Decay (Persamaan 3.2)
  - 3.2.5 Engagement Metrics & Normalisasi (Persamaan 3.3, 3.4)
  - 3.2.6 Skor Hibrida Final (Persamaan 3.5) **← BARU, paling penting**
  - 3.2.7 Cursor-Based Pagination
  - 3.2.8 Strategi Caching Read-Through
  - 3.2.9 Algoritma FYP (Algoritma 3.1, pseudocode)

Mau saya lanjut tulis draft konkret untuk salah satu issue (mis. tulis Persamaan 3.5 + section 3.2.6 lengkap dalam satu file siap-paste-ke-Word)?
