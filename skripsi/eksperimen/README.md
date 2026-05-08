# Eksperimen — Time-Aware Hybrid Ranking System

Folder ini berisi seluruh skrip eksperimen yang digunakan pada Bab IV skripsi untuk memvalidasi sistem rekomendasi hibrida.

## Struktur

```
eksperimen/
├── README.md                     # File ini
├── requirements.txt              # Dependencies Python
├── 01_generate_dataset.py        # ✅ Dataset synthetic + ground truth
├── 02_evaluate_accuracy.py       # ⏳ Belum dibuat — NDCG/Precision/Recall
├── 03_sensitivity_analysis.py    # ⏳ Belum dibuat — sweep weights
├── 04_ablation_study.py          # ⏳ Belum dibuat — kontribusi pilar
└── data/                         # Output dari skrip 01 (di-gitignore)
    ├── users.csv
    ├── categories.csv
    ├── contents.csv
    ├── content_categories.csv
    ├── user_category_stats.csv
    ├── ground_truth.csv
    └── seed.sql
```

## Setup

```bash
# 1. Buat virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verifikasi
python --version  # 3.11+
python -c "import numpy, pandas, sklearn; print('OK')"
```

## Reproduksibilitas

Seluruh skrip menggunakan `seed = 42` secara default. Untuk override:

```bash
python 01_generate_dataset.py --seed 123
```

Hasil akhir akan **identik** untuk seed yang sama, sesuai prinsip reproduksibilitas yang dijelaskan pada Bab IV section 4.2.2.7.

---

## Skrip 01 — Generate Dataset

**Tujuan:** Membangkitkan dataset sintetis sesuai spesifikasi Bab IV section 4.2.2:

- 100 pengguna terbagi 5 arketipe (Tech Enthusiast, Foodie, Art Lover, Sports Fan, Generalist)
- 1.000 konten dengan distribusi kategori uniform
- Waktu publikasi tersebar 0-30 hari ke belakang
- Engagement metrics (like, used, watch) mengikuti power-law $\alpha = 2.0$
- Rating $\sim \mathcal{N}(4.2, 0.5)$ clipped pada $[3.0, 5.0]$
- Ground truth relevance $rel(u, c) \in \{0, 1, 2, 3\}$ untuk setiap pasangan

**Cara jalankan:**

```bash
python 01_generate_dataset.py
```

**Output console (contoh):**

```
[+] Generating synthetic dataset (seed=42)
[+] 100 users across 5 archetypes
[+] 1000 contents
[+] 480 user_category_stats rows
[+] 100000 ground-truth (user, content) pairs
[+] Ground-truth relevance distribution: {0: 35234, 1: 38912, 2: 18540, 3: 7314}
[+] CSV files written to: ./data/
[+] Wrote SQL seed: ./data/seed.sql
[+] Done.
```

**File yang dihasilkan:**

| File | Isi | Pemakai |
|---|---|---|
| `users.csv` | id, username, archetype | Skrip 02-04 sebagai daftar user yang diuji |
| `categories.csv` | id, name, slug | Referensi kategori |
| `contents.csv` | id, title, metadata, engagement | Untuk debugging dan analisis distribusi |
| `content_categories.csv` | content_id, category_id | Relasi |
| `user_category_stats.csv` | user_id, category_id, score | Profil minat awal user (di-seed ke MySQL) |
| `ground_truth.csv` | user_id, content_id, relevance | **Acuan kebenaran** untuk hitung NDCG |
| `seed.sql` | INSERT statements | Seeder MySQL untuk *system under test* |

**Apply ke MySQL (test database):**

```bash
# Asumsi MySQL berjalan di Docker
docker exec -i mysql mysql -uroot -proot content_db < data/seed.sql
```

⚠️ **Peringatan:** `seed.sql` **tidak** menghapus data lama. Jalankan pada database test yang fresh, atau bersihkan dulu dengan:

```sql
TRUNCATE TABLE user_category_stats;
TRUNCATE TABLE content_categories;
DELETE FROM contents WHERE type = 'template';
DELETE FROM users WHERE username LIKE '%_001' OR username LIKE '%_002';  -- dst
```

---

## Catatan Implementasi

**Power-law sampling** — implementasi pada `power_law_sample()` menggunakan inverse-CDF dari distribusi Pareto, di-clip pada nilai maksimum. Untuk dataset 1.000 baris pendekatan ini menghasilkan distribusi yang representatif tanpa overhead library tambahan.

**Ground truth schema** — mengikuti Persamaan 3.5 di Bab III. Skala 4-tingkat $\{0, 1, 2, 3\}$ dipilih karena `sklearn.metrics.ndcg_score` membutuhkan **graded relevance** (bukan binary) untuk perhitungan IDCG yang akurat.

**Catatan SQL UUID format** — skrip menggunakan format BINARY(16) sesuai schema MySQL existing yang dipakai sistem. Helper `UUID_TO_BIN(...)` dan `BIN_TO_UUID(...)` di MySQL akan memproses format ini.

**Sanity check distribusi** — setelah generate, perhatikan output "Ground-truth relevance distribution". Distribusi ideal:

- `rel = 0` (~35%) → konten tidak relevan
- `rel = 1` (~40%) → relevan ringan
- `rel = 2` (~18%) → relevan sedang
- `rel = 3` (~7%) → sangat relevan

Kalau distribusi sangat skewed (mis. 90% rel=0), berarti random seed atau kategori user-konten tidak overlap memadai — perlu tuning parameter.

---

## Selanjutnya

Skrip yang akan dibangun setelah ini:

1. **`02_evaluate_accuracy.py`** — hit endpoint API (`/api/posts?feed=fyp`, `?feed=catalog`, `?feed=trending`), hitung NDCG@K, Precision@K, Recall@K untuk tiap user, lalu rata-ratakan.

2. **`03_sensitivity_analysis.py`** — sweep nilai $w_1, w_2, w_3$ via env var `FYP_WEIGHT_*`, restart service tiap konfigurasi, ukur NDCG, lalu plot heatmap atau line chart.

3. **`04_ablation_study.py`** — empat varian: only-cosine, +freshness, +quality, full-hybrid. Bandingkan NDCG@10.

Lihat file `INSTRUKSI_EKSPERIMEN.md` (akan dibuat) untuk panduan menjalankan eksperimen end-to-end.
