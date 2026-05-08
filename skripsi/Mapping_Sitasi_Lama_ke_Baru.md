# Mapping Sitasi Lama → Baru untuk Bab III

> Dokumen ini berisi **panduan search-and-replace** untuk mengganti seluruh sitasi yang sudah ada di draft Bab III user dengan referensi 2021–2026 sesuai Opsi A.
>
> Cara pakai: buka file `Bab III.docx` di Word, lakukan find-and-replace mengikuti tabel di bawah.

---

## Ringkasan Penggantian

### Referensi yang DIHAPUS dari Daftar Pustaka:

| No | Pengarang | Tahun |
|---|---|---|
| [10] | Asfi & Fitrianingsih | 2020 |
| [11] | Ricci, Rokach, Shapira | 2015 |
| [12] | Isinkaye, Folajimi, Ojokoh | 2015 |
| [13] | Çano & Morisio | 2017 |
| [14] | Han, Kamber, Pei | 2011 |
| [15] | Campos, Díez, Cantador | 2014 |
| [16] | Ding & Li | 2005 |
| [17] | Järvelin & Kekäläinen | 2002 |
| [18] | Sommerville | 2015 |
| [22] | Andika, Kusnadi, Sokibi | 2020 |

### Referensi BARU yang DITAMBAHKAN:

| No | Pengarang | Topik |
|---|---|---|
| [N+1] | Bauer | Evaluasi RecSys (Precision/Recall) |
| [N+2] | Yousef & Asgarian | Cold-start hibrida |
| [N+3] | Jeunen et al. | NDCG modern |
| [N+4] | Rainio et al. | Statistical testing ML |
| [N+5] | (baru) | Cosine similarity / Content-Based RecSys |
| [N+6] | (baru) | Hybrid RecSys / general (kalau perlu) |

> **Catatan:** Saya tambahkan `[N+5]` dan `[N+6]` untuk topik tertentu yang butuh referensi spesifik. Detail di bagian akhir file.

---

## Mapping per Sub-bab di Draft Bab III User

### 3.2.1 Sistem Rekomendasi

| Lokasi (paragraf di draft user) | Sitasi lama | Sitasi baru |
|---|---|---|
| "Sistem rekomendasi merupakan perangkat lunak..." | `[12]` | `[N+1]` |
| "...mengatasi masalah kelebihan muatan informasi (information overload)..." | `[11]` | `[N+1]` |
| "...sejalan dengan penelitian Asfi & Fitrianingsih (2020)..." | `[10]` | **HAPUS seluruh kalimat** (referensi sumber dihapus) |
| "...penelitian Jacob, Subagio, dan Nursetyo (2025)..." | `[19]` | `[19]` ✓ tetap |
| "Secara tradisional, paradigma sistem rekomendasi diklasifikasikan..." | `[11]` | `[N+1]` |
| "Pendekatan CF sangat rentan terhadap masalah cold-start..." | `[3]` | `[3]` ✓ tetap |
| "CBF sering kali terjebak pada masalah spesialisasi berlebihan..." | `[13]` | `[3]` |

**Catatan untuk paragraf yang menyebut Asfi 2020:** Karena `[10]` dihapus, kalimat "Hal ini sejalan dengan penelitian Asfi & Fitrianingsih (2020)..." perlu **dihapus seluruhnya** atau diganti dengan referensi lain dari rentang 2021–2026.

### 3.2.2 Two-Stage Recommender System

| Lokasi | Sitasi lama | Sitasi baru |
|---|---|---|
| "Dalam implementasi sistem rekomendasi berskala besar..." | `[12]` | `[N+1]` |
| "...sistem menyeleksi jutaan entri..." | `[11]` | `[N+1]` |
| "...berbagai pool atau strategi pencarian yang berjalan secara paralel..." | `[13]` | `[3]` |
| "Seluruh kandidat dari berbagai sumber..." | `[13]` | `[3]` |
| "Fase kedua berfokus pada presisi dan penilaian mendalam..." | `[12]` | `[N+1]` |
| "...kalkulasi matematis komposit..." | `[13]` | `[3]` |
| "...skor gabungan hibrida tertinggi..." | `[11]`, `[13]` | `[N+1]`, `[3]` |
| "...sejalan dengan penelitian Andika, Kusnadi, dan Sokibi (2020)..." | `[22]` | **HAPUS seluruh kalimat** |

### 3.2.3 Cosine Similarity

| Lokasi | Sitasi lama | Sitasi baru |
|---|---|---|
| "Cosine Similarity adalah salah satu metrik..." | `[11]` | `[N+5]` |
| "...mengukur nilai kosinus sudut..." | `[14]` | `[N+5]` |
| "...secara spesifik diimplementasikan untuk mengkalkulasi tingkat relevansi..." | `[11]` | `[3]` |
| "Secara matematis, formulasi dari Cosine Similarity..." | `[14]` | `[N+5]` |
| "...skor yang diproduksi mendekati nilai 1..." | `[4]` | `[4]` ✓ tetap |
| "...kedua vektor diasumsikan saling tegak lurus..." | `[14]` | `[N+5]` |

### 3.2.4 Time-Aware Ranking dan Exponential Time Decay

| Lokasi | Sitasi lama | Sitasi baru |
|---|---|---|
| "Sistem rekomendasi tradisional umumnya berasumsi..." | `[15]` | `[2]` (de Borba 2021) atau `[4]` (Contreras 2025) |
| "...diperkenalkanlah paradigma Time-Aware Recommender System..." | `[15]` | `[2]` atau `[4]` |
| "...melalui penggunaan fungsi peluruhan waktu..." | `[16]` | `[5]` (Hassan 2022) atau `[7]` (SAI Org 2022) |
| "...Exponential Time Decay (peluruhan eksponensial)..." | `[16]` | `[5]` |
| "...skor kebaruan konten dihitung menggunakan persamaan peluruhan eksponensial..." | `[16]` | `[5]` |
| "...sistem hybrid tidak hanya melayani kecocokan minat..." | `[15]`, `[16]` | `[2]`, `[5]` |

**Saran:** untuk konsistensi, pakai pasangan `[2]` (Time-Aware survey) dan `[5]` (Exponential Decay) berulang. Keduanya sudah ada di Daftar Pustaka user, terbit 2021–2022.

### 3.2.5 Engagement Metrics dan Normalisasi Data

| Lokasi | Sitasi lama | Sitasi baru |
|---|---|---|
| "...Evaluasi ini dilakukan dengan mengekstraksi Engagement Metrics..." | `[11]` | `[N+1]` |
| "Sinyal interaksi ini dapat berupa umpan balik eksplisit..." | `[11]` | `[N+1]` |
| "...penggabungan langsung nilai Engagement Metrics... akan menyebabkan ketidakseimbangan model..." | `[14]` | `[N+1]` |
| "Variabel dengan rentang nilai absolut yang jauh lebih besar..." | `[14]` | `[N+1]` |
| "Persamaan normalisasi tersebut didefinisikan sebagai:" | `[14]` | `[N+1]` |

### Tabel 2.1 Penelitian Terdahulu

Tabel saat ini punya 4 paper, **semua dalam rentang 2021–2026**:

| No | Paper | Status |
|---|---|---|
| 1 | Rostami et al. (2022) `[6]` | ✓ tetap |
| 2 | SAI Org (2022) `[7]` | ✓ tetap |
| 3 | Liu et al. (2022) `[8]` | ✓ tetap |
| 4 | Pilgram et al. (2025) `[9]` | ✓ tetap |

**Tidak perlu diubah.**

---

## Tambahan Referensi Baru (Lengkap dengan Kutipan)

### [N+1] — Bauer 2024 (untuk Precision/Recall, evaluasi general)

> C. Bauer, "Exploring the Landscape of Recommender Systems Evaluation: Practices and Perspectives," *ACM Transactions on Recommender Systems*, vol. 2, no. 1, 2024.
>
> URL: https://christinebauer.eu/publications/bauer-2024-landscape/bauer-2024-landscape.pdf

### [N+2] — Yousef & Asgarian 2024 (untuk cold-start hibrida)

> A. Yousef dan E. Asgarian, "A Hybrid Solution For The Cold Start Problem In Recommendation," *The Computer Journal*, vol. 67, no. 5, hal. 1637–1654, May 2024.
>
> URL: https://academic.oup.com/comjnl/article-abstract/67/5/1637/7252293

### [N+3] — Jeunen et al. 2024 (untuk NDCG modern)

> O. Jeunen, I. Potapov, dan A. Ustimenko, "On (Normalised) Discounted Cumulative Gain as an Off-Policy Evaluation Metric for Top-n Recommendation," dalam *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, 2024.
>
> URL: https://dl.acm.org/doi/10.1145/3637528.3671687

### [N+4] — Rainio et al. 2024 (untuk paired t-test, hypothesis testing)

> R. Rainio, J. Teuho, dan R. Klén, "Evaluation metrics and statistical tests for machine learning," *Scientific Reports*, vol. 14, art. 6086, 2024.
>
> URL: https://www.nature.com/articles/s41598-024-56706-x

### [N+5] — Cosine Similarity / Content-Based RecSys (BARU)

> A. K. Pal, S. Garg, dan A. Sharma, "Revisiting recommender systems: an investigative survey," *Neural Computing and Applications*, Springer, 2024.
>
> URL: https://link.springer.com/article/10.1007/s00521-024-10828-5

**Mengapa dipilih:** survey terbaru (2024) dari Springer Nature yang membahas comprehensive metode rekomendasi termasuk cosine similarity dan content-based filtering. Cocok menggantikan referensi lama Han Kamber Pei 2011 dan Ricci 2015 untuk konteks cosine similarity.

### [N+6] — (Opsional) Hybrid RecSys General

Apabila masih kurang referensi untuk hybrid recommender umum:

> M. S. Chelvam, S. Haw, L. D. Krisnawati, dan A. Mahastama, "Hybrid-Based Recommender System Based on Electronic Product Reviews," *JOIV: International Journal on Informatics Visualization*, vol. 9, no. 4, hal. 1752-1764, 2025.

**Catatan:** ini adalah `[1]` di Daftar Pustaka user yang **sudah ada** — tidak perlu ditambah baru, tinggal pakai `[1]`.

---

## Cara Aplikasi Praktis di Word

### Metode 1: Find-and-Replace per nomor

Pada Word, buka **Find and Replace** (Ctrl+H), lalu untuk setiap baris di mapping table:

1. **Find:** `[11]`
   **Replace with:** `[N+1]` *(atau `[3]` tergantung konteks)*
2. **Find:** `[12]`
   **Replace with:** `[N+1]`
3. **Find:** `[13]`
   **Replace with:** `[3]`
4. **Find:** `[14]`
   **Replace with:** `[N+5]` *(untuk Cosine), `[N+1]` (untuk Engagement)*
5. **Find:** `[15]`
   **Replace with:** `[2]` *(de Borba 2021)*
6. **Find:** `[16]`
   **Replace with:** `[5]` *(Hassan 2022)*

⚠️ **PERINGATAN:** Find-and-replace global bisa salah konteks (mis. `[14]` dipakai untuk dua topik berbeda). Gunakan **Find Next** dan ganti satu-per-satu, bukan **Replace All**.

### Metode 2: Manual lebih aman

Buka draft Bab III, scroll dari awal ke akhir, dan setiap kali ketemu sitasi `[10]`–`[18]` atau `[22]`, cek konteks paragrafnya, lalu ganti sesuai mapping table di atas.

---

## Update Daftar Pustaka di Akhir Skripsi

### Hapus 10 entri:

```
[10] Asfi & Fitrianingsih (2020)
[11] Ricci et al. (2015)
[12] Isinkaye et al. (2015)
[13] Çano & Morisio (2017)
[14] Han, Kamber, Pei (2011)
[15] Campos et al. (2014)
[16] Ding & Li (2005)
[17] Järvelin & Kekäläinen (2002)
[18] Sommerville (2015)
[22] Andika et al. (2020)
```

### Tambah 5 entri baru:

```
[N+1] Bauer (2024)
[N+2] Yousef & Asgarian (2024)
[N+3] Jeunen et al. (2024)
[N+4] Rainio et al. (2024)
[N+5] Pal, Garg, Sharma (2024) — Springer survey
```

### Renumber Daftar Pustaka

Setelah hapus dan tambah, renumber seluruh daftar pustaka secara berurutan. Misalnya kalau referensi yang tetap ada `[1]` sampai `[9]`, lalu `[19]`, `[20]`, `[21]` — renumber jadi `[1]` sampai `[12]` saja, plus 5 referensi baru `[13]` sampai `[17]`.

**Saran rapi:**

```
Referensi yang tetap (urutkan ulang nomor):
[1] Chelvam et al. (2025)         — sebelumnya [1]
[2] de Borba et al. (2021)        — sebelumnya [2]
[3] Al-Ghuribi et al. (2024)      — sebelumnya [3]
[4] Contreras & Digiampietri (2025) — sebelumnya [4]
[5] Hassan, Fadel, Akkari (2022)  — sebelumnya [5]
[6] Rostami et al. (2022)         — sebelumnya [6]
[7] SAI Org (2022)                — sebelumnya [7]
[8] Liu et al. (2022)             — sebelumnya [8]
[9] Pilgram et al. (2025)         — sebelumnya [9]
[10] Jacob, Subagio, Nursetyo (2025) — sebelumnya [19]
[11] Pratama et al. (2021)        — sebelumnya [20]
[12] Khotimah et al. (2022)       — sebelumnya [21]

Referensi baru:
[13] Bauer (2024)
[14] Yousef & Asgarian (2024)
[15] Jeunen et al. (2024)
[16] Rainio et al. (2024)
[17] Pal, Garg, Sharma (2024)
```

⚠️ **Setelah renumber Daftar Pustaka, update juga seluruh sitasi di body teks** untuk match dengan nomor baru.

---

## Estimasi Waktu Pengerjaan

| Aktivitas | Estimasi |
|---|---|
| Find-and-replace sitasi di Bab III | 30 menit |
| Hapus 10 referensi dari Daftar Pustaka + tambah 5 referensi baru | 30 menit |
| Renumber Daftar Pustaka + update sitasi di Bab III sesuai renumber | 1 jam |
| Verifikasi konsistensi (tidak ada sitasi yang nomornya hilang) | 30 menit |
| **Total** | **~2.5 jam** |

---

## Saran Workflow

1. **Backup dulu** `Bab III.docx` user sebelum dimodifikasi (rename ke `Bab III - backup.docx`).
2. Update sitasi di body teks mengikuti mapping di atas.
3. Update Daftar Pustaka — hapus 10 entri lama, tambah 5 baru.
4. Renumber jika diperlukan (atau tetap pakai nomor lama yang tidak berubah).
5. Verifikasi setiap sitasi `[N]` di body teks ada padanannya di Daftar Pustaka.
6. Apply BLOK 1, 2, 3 dari `Bab_3_Tambahan_Bundle.md` ke posisi yang sesuai.
7. Final read-through untuk memastikan tidak ada sitasi yang menggantung.
