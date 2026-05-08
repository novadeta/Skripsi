# 3.2.6 Skor Hibrida Final (Hybrid Final Score)

> **Catatan untuk pengerjaan di Word:**
> - Seluruh persamaan dalam dokumen ini wajib **diketik ulang menggunakan Equation Editor** (Insert → Equation), **bukan** dengan menyalin karakter unicode.
> - Format input untuk Equation Editor disertakan di bawah setiap persamaan dalam blok **[Notasi Equation Editor]**.
> - Penomoran persamaan di bawah ini melanjutkan urutan dari sub-bab sebelumnya. Sesuaikan kalau urutan akhir berbeda.
> - Format sitasi mengikuti gaya IEEE (numbered) yang sudah dipakai pada Bab III.

---

## 3.2.6 Skor Hibrida Final (Hybrid Final Score)

Setelah ketiga pilar penilaian — kemiripan minat (Cosine Similarity), kebaruan konten (Exponential Time Decay), dan kualitas interaksi (Quality Score) — terkalkulasi pada rentang ternormalisasi $[0, 1]$, langkah terakhir pada fase Ranking adalah **menggabungkan ketiga skor tersebut menjadi satu metrik komposit tunggal** yang menjadi dasar pengurutan akhir konten. Penggabungan ini menggunakan paradigma **weighted linear combination** sebagaimana dikategorikan oleh Burke [13] dalam taksonomi sistem rekomendasi hibrida sebagai *weighted hybrid recommender*. Pada paradigma ini, output dari beberapa teknik rekomendasi dihitung secara bersamaan, kemudian dijumlahkan dengan bobot yang telah ditentukan untuk membentuk skor relevansi tunggal [12].

Persamaan formal skor hibrida final pada penelitian ini didefinisikan sebagai berikut:

$$\text{Score}_{\text{final}}(c) = w_{1} \cdot \text{Cosine}(u, c) + w_{2} \cdot S_{\text{fresh}}(c) + w_{3} \cdot \text{Quality}(c) \quad \text{(Persamaan 3.5)}$$

**[Notasi Equation Editor]**
```
Score_final(c) = w_1 · Cosine(u, c) + w_2 · S_fresh(c) + w_3 · Quality(c)
```

Keterangan persamaan:

- $\text{Score}_{\text{final}}(c)$ adalah skor akhir konten kandidat $c$ untuk pengguna $u$, yang dihasilkan pada rentang $[0, 1]$.
- $\text{Cosine}(u, c)$ adalah skor kemiripan minat antara vektor preferensi pengguna $u$ dan vektor kategori konten $c$, sebagaimana didefinisikan pada Persamaan 3.1.
- $S_{\text{fresh}}(c)$ adalah skor kebaruan konten $c$ yang dihitung melalui fungsi peluruhan eksponensial pada Persamaan 3.2.
- $\text{Quality}(c)$ adalah skor kualitas konten $c$ yang dihitung melalui kombinasi rata-rata penilaian dan metrik interaksi yang dinormalisasi pada Persamaan 3.4.
- $w_{1}$, $w_{2}$, dan $w_{3}$ adalah konstanta pembobotan yang masing-masing menunjukkan kontribusi relatif dari pilar minat, kebaruan, dan kualitas terhadap skor akhir.

Konstanta pembobotan tersebut tunduk pada kendala normalisasi sebagai berikut:

$$w_{1} + w_{2} + w_{3} = 1, \quad w_{i} \in [0, 1] \quad \forall i \in \{1, 2, 3\} \quad \text{(Persamaan 3.6)}$$

**[Notasi Equation Editor]**
```
w_1 + w_2 + w_3 = 1,    w_i ∈ [0, 1]    ∀ i ∈ {1, 2, 3}
```

Kendala ini memastikan bahwa skor akhir tetap berada pada interval $[0, 1]$ — sifat ini penting agar nilai skor dapat dibandingkan secara langsung antar konten dan diinterpretasi secara konsisten oleh tahap pengurutan (sorting) berikutnya.

### 3.2.6.1 Pemilihan Nilai Konstanta Pembobotan

Pada penelitian ini, ditetapkan nilai konstanta pembobotan sebagai berikut:

$$w_{1} = 0{,}55 \quad ; \quad w_{2} = 0{,}25 \quad ; \quad w_{3} = 0{,}20 \quad \text{(Persamaan 3.7)}$$

**[Notasi Equation Editor]**
```
w_1 = 0,55    ;    w_2 = 0,25    ;    w_3 = 0,20
```

Pemilihan kombinasi nilai ini didasarkan pada tiga pertimbangan teoretis dan empiris:

**a. Dominansi Pilar Minat (Cosine Similarity)**

Bobot tertinggi sebesar **0,55** dialokasikan pada komponen Cosine Similarity. Justifikasi pemilihan ini bersumber dari karakteristik dasar sistem rekomendasi yang berorientasi *content-based filtering* — di mana kemiripan profil minat pengguna terhadap atribut konten merupakan sinyal relevansi paling representatif untuk personalisasi [11], [13]. Dengan kontribusi sebesar 55%, pilar Cosine memastikan bahwa konten yang ditampilkan pada feed pengguna **selaras dengan riwayat ketertarikan kategoris pengguna**, sehingga menjawab tujuan utama personalisasi.

**b. Kontribusi Moderat Pilar Kebaruan (Freshness)**

Bobot sebesar **0,25** dialokasikan pada komponen Freshness Score. Pemilihan bobot moderat ini bertujuan untuk **memberikan visibilitas yang adil bagi konten baru** tanpa mengorbankan relevansi minat. Sesuai dengan rekomendasi Campos et al. [15] dalam survei time-aware recommender system, pendekatan *time as weight* memerlukan kalibrasi yang berhati-hati: bobot temporal yang terlalu tinggi cenderung mendominasi skor akhir dan menyebabkan konten lama yang berkualitas tetapi sangat relevan menjadi tertekan, sedangkan bobot terlalu rendah memunculkan kembali masalah dominasi konten lama (filter bubble temporal). Bobot 0,25 dipilih karena cukup signifikan untuk mencegah dominasi konten lama, namun masih lebih kecil dari pilar relevansi sehingga tidak menggeser fokus utama personalisasi.

**c. Kontribusi Penyaring Kualitas (Quality Score)**

Bobot sebesar **0,20** dialokasikan pada komponen Quality Score. Pilar ini diposisikan terutama sebagai **mekanisme penyaring (filter) terhadap konten berkualitas rendah**, bukan sebagai penentu utama urutan. Karena Quality Score sudah berfungsi sebagai pembanding antar konten dengan tingkat relevansi yang serupa (yaitu sebagai *tie-breaker* implisit), kontribusi 20% telah memadai untuk membedakan konten populer berkualitas tinggi dari konten dengan jumlah interaksi rendah.

### 3.2.6.2 Sifat Matematis Skor Hibrida Final

Persamaan 3.5 memiliki beberapa sifat matematis yang menjamin perilaku sistem yang stabil:

**a. Domain dan Rentang Nilai (Range)**

Karena setiap komponen skor (Cosine, Freshness, Quality) telah ternormalisasi pada interval $[0, 1]$ dan jumlah bobot $w_{i}$ sama dengan 1, maka skor akhir juga selalu berada pada rentang yang sama:

$$\text{Score}_{\text{final}}(c) \in [0, 1] \quad \forall c$$

**b. Monotonisitas (Monotonicity)**

Skor hibrida bersifat *monotonically non-decreasing* terhadap setiap pilarnya — yaitu, peningkatan nilai pada salah satu pilar tanpa mengubah pilar lain akan selalu meningkatkan (atau setidaknya tidak menurunkan) skor akhir. Sifat ini secara intuitif konsisten dengan ekspektasi sistem: konten yang lebih relevan, lebih baru, atau lebih berkualitas seharusnya mendapatkan skor yang lebih tinggi.

**c. Interpretabilitas**

Pendekatan linear combination memungkinkan **dekomposisi skor** untuk keperluan analisis dan debugging. Apabila suatu konten muncul atau tidak muncul pada feed, kontribusi masing-masing pilar dapat dihitung secara terpisah, sehingga sistem dapat dievaluasi secara transparan — properti yang sulit dicapai pada pendekatan berbasis deep learning yang umumnya bersifat *black-box* [3], [13].

### 3.2.6.3 Justifikasi Pemilihan Pendekatan Linear Combination

Sebagai alternatif penggabungan skor, terdapat beberapa pendekatan lain yang dapat dipertimbangkan, yaitu *switching hybrid* (memilih satu metode berdasarkan konteks), *cascade hybrid* (memurnikan output secara bertahap), dan *meta-level hybrid* (menggunakan output suatu metode sebagai input metode lain) [13]. Penelitian ini memilih *weighted linear combination* berdasarkan tiga pertimbangan praktis berikut:

1. **Latensi Komputasi Rendah** — Operasi penjumlahan terbobot memiliki kompleksitas $O(1)$ per konten, sehingga total kompleksitas fase scoring tetap linear terhadap jumlah kandidat, $O(n)$. Hal ini krusial untuk arsitektur backend yang menuntut respons feed berlatensi rendah secara real-time.

2. **Determinisme Output** — Untuk masukan yang sama, sistem akan menghasilkan keluaran yang identik, sehingga proses A/B testing, *debugging*, dan *reproducibility* hasil eksperimen menjadi lebih terjamin dibandingkan pendekatan stokastik atau berbasis pelatihan model.

3. **Kemudahan Tuning** — Konstanta pembobotan dapat dimodifikasi secara independen tanpa memerlukan pelatihan ulang model, memungkinkan iterasi cepat selama fase eksperimen dan pengujian.

### 3.2.6.4 Aplikasi pada Tahap Sorting

Setelah seluruh konten kandidat memperoleh nilai $\text{Score}_{\text{final}}$, daftar diurutkan secara menurun (descending). Untuk menjaga determinisme output ketika beberapa konten memiliki skor identik, sistem menerapkan urutan pengurutan komposit (composite sort key) sebagai berikut:

$$\text{ORDER BY} \quad \text{Score}_{\text{final}}(c) \text{ DESC} \quad \rightarrow \quad t_{c} \text{ DESC} \quad \rightarrow \quad \text{ID}(c) \text{ DESC} \quad \text{(Persamaan 3.8)}$$

**[Notasi Equation Editor]**
```
ORDER BY Score_final(c) DESC → t_c DESC → ID(c) DESC
```

Dengan $t_{c}$ adalah waktu pembuatan (timestamp) konten dan $\text{ID}(c)$ adalah identifikasi unik. Tie-breaker berlapis ini menjamin **total ordering** pada himpunan kandidat sehingga proses paginasi berbasis kursor dapat berjalan tanpa duplikasi atau lewatan baris (lihat Sub-bab 3.2.7 mengenai *Cursor-Based Pagination*).

Konten yang menempati posisi paling atas pada urutan akhir inilah yang disajikan kepada pengguna sebagai feed pada halaman utama (For You Page).

---

## Pemetaan Persamaan ke Implementasi Kode

> Bagian ini opsional — bisa diletakkan di Bab IV (Implementasi). Disertakan di sini untuk referensi.

| Persamaan | Komponen | Lokasi Implementasi (modul Repository) |
|---|---|---|
| Persamaan 3.1 | Cosine Similarity | `cosineScore(userScores, userNorm, categoryIDs)` |
| Persamaan 3.2 | Exponential Time Decay | `freshnessScore(createdAt time.Time)` |
| Persamaan 3.4 | Quality Score | `qualityScore(ratingAvg, likeCount, maxLike)` |
| Persamaan 3.5 | Hybrid Final Score | Loop scoring di dalam `GetFYP(...)` |
| Persamaan 3.8 | Composite Sort | `sort.Slice(scored, ...)` di `GetFYP(...)` |

---

## Daftar Pustaka yang Dirujuk pada Sub-Bab Ini

> Pastikan referensi-referensi berikut tersedia pada Daftar Pustaka utama dengan nomor yang konsisten.

- [3] M. Al-Ghuribi, S. A. Noah, dan S. Tiun, "Hybrid Quality-Based Recommender Systems: A Systematic Literature Review," *IEEE Access*, 2024.
- [11] F. Ricci, L. Rokach, dan B. Shapira, "Recommender systems: introduction and challenges," dalam *Recommender systems handbook*, Boston, MA: Springer, 2015, hal. 1-34.
- [12] F. O. Isinkaye, Y. O. Folajimi, dan B. A. Ojokoh, "Recommendation systems: Principles, methods and evaluation," *Egyptian Informatics Journal*, vol. 16, no. 3, hal. 261-273, 2015.
- [13] E. Çano dan M. Morisio, "Hybrid recommender systems: A systematic literature review," *Intelligent Data Analysis*, vol. 21, no. 6, hal. 1487-1524, 2017.
- [15] P. G. Campos, F. Díez, dan I. Cantador, "Time-aware recommender systems: a comprehensive survey and analysis of existing evaluation protocols," *User Modeling and User-Adapted Interaction*, vol. 24, no. 1-2, hal. 67-119, 2014.

---

## Checklist Setelah di-Paste ke Word

- [ ] Sesuaikan penomoran persamaan (3.5, 3.6, 3.7, 3.8) dengan urutan persamaan sebelumnya di Bab III.
- [ ] Ketik ulang setiap persamaan menggunakan **Equation Editor**, jangan paste-as-text.
- [ ] Atur format huruf miring (italic) untuk variabel ($w$, $c$, $u$, dll) sesuai konvensi matematika.
- [ ] Pastikan setiap nomor sitasi `[3]`, `[11]`, `[12]`, `[13]`, `[15]` sudah konsisten dengan nomor yang dipakai di Daftar Pustaka utama.
- [ ] Verifikasi alignment paragraf (rata kanan-kiri / justify).
- [ ] Spasi antar persamaan dan paragraf mengikuti template skripsi institusi (umumnya line spacing 1,5 atau 2).
- [ ] Periksa apakah notasi desimal harus pakai koma (`0,55`) atau titik (`0.55`) — di skripsi Bahasa Indonesia umumnya pakai koma.
