"""
Synthetic Dataset Generator for Time-Aware Hybrid Ranking System Evaluation

This script generates a reproducible synthetic dataset that matches the
specification in Bab IV section 4.2.2 of the thesis:

  - 100 simulated users distributed across 5 archetypes
  - 1,000 contents distributed uniformly across 5 categories
  - Content publication times spread over the last 30 days
  - Engagement metrics following a power-law distribution
  - Ground truth relevance labels for NDCG computation

Outputs:
  data/users.csv               - user accounts
  data/categories.csv          - 5 categories
  data/contents.csv            - 1,000 contents with metadata
  data/content_categories.csv  - content-category relations
  data/user_category_stats.csv - user interest scores per archetype
  data/ground_truth.csv        - rel(u, c) relevance for every (user, content) pair
  data/seed.sql                - SQL inserts ready to feed into MySQL

Usage:
  python 01_generate_dataset.py

Reproducibility:
  All random operations use seed=42 (see --seed flag for override).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import random
import uuid
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Constants — spec from Bab IV section 4.2.2
# ---------------------------------------------------------------------------

NUM_USERS = 100
NUM_CONTENTS = 1_000
CATEGORIES = [
    ("c1", "Teknologi", "teknologi"),
    ("c2", "Kuliner", "kuliner"),
    ("c3", "Seni", "seni"),
    ("c4", "Olahraga", "olahraga"),
    ("c5", "Edukasi", "edukasi"),
]

# Archetype name -> distribution of interest scores per category.
# Order matches CATEGORIES tuple above (Teknologi, Kuliner, Seni, Olahraga, Edukasi)
ARCHETYPES: dict[str, list[int]] = {
    "Tech Enthusiast": [80, 10, 5, 2, 30],
    "Foodie":          [5, 80, 20, 5, 5],
    "Art Lover":       [5, 15, 80, 2, 25],
    "Sports Fan":      [10, 5, 5, 80, 5],
    "Generalist":      [25, 25, 25, 25, 25],
}
USERS_PER_ARCHETYPE = NUM_USERS // len(ARCHETYPES)  # 20

# Content publication time window
PUBLICATION_WINDOW_DAYS = 30

# Engagement distribution
POWER_LAW_ALPHA = 2.0
LIKE_COUNT_MAX = 5_000        # ceiling for power-law sample
USED_COUNT_MAX = 1_500
WATCH_COUNT_MAX = 20_000

# Rating ~ N(mu=4.2, sigma=0.5) clipped to [3.0, 5.0]
RATING_MEAN = 4.2
RATING_STD = 0.5
RATING_MIN, RATING_MAX = 3.0, 5.0

# Ground truth thresholds (see Persamaan 3.5 in thesis)
GROUND_TRUTH_TOP_K = 3        # how many top categories define "K_top3(u)"


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------

@dataclass
class User:
    id: str
    username: str
    archetype: str

@dataclass
class Content:
    id: str
    title: str
    category_ids: list[str]
    created_at: dt.datetime
    rating_avg: float
    like_count: int
    used_count: int
    watch_count: int


# ---------------------------------------------------------------------------
# Generation routines
# ---------------------------------------------------------------------------

def generate_users(rng: np.random.Generator) -> list[User]:
    """Build NUM_USERS users distributed equally across archetypes."""
    users: list[User] = []
    for archetype, _ in ARCHETYPES.items():
        for i in range(USERS_PER_ARCHETYPE):
            uid = str(uuid.UUID(int=rng.integers(0, 2**128 - 1, dtype=np.uint64)))
            users.append(User(
                id=uid,
                username=f"{archetype.lower().replace(' ', '_')}_{i+1:03d}",
                archetype=archetype,
            ))
    return users


def power_law_sample(rng: np.random.Generator, max_value: int, alpha: float) -> int:
    """Sample a positive integer roughly following P(X=k) ∝ k^-alpha.

    We use inverse-CDF sampling on a discrete distribution truncated at
    max_value. For practical sample sizes this yields the desired
    "few large, many small" behaviour without the heavy tails of an
    unbounded Pareto.
    """
    # Generate value in [1, max_value] from inverse-CDF of power law
    u = rng.uniform()
    # x = (1-u)^(-1/(alpha-1)) for Pareto; clip to discrete range
    raw = (1 - u) ** (-1.0 / (alpha - 1.0))
    val = int(min(max_value, max(1, raw)))
    return val


def generate_contents(rng: np.random.Generator) -> list[Content]:
    """Build NUM_CONTENTS contents with uniform category distribution and
    power-law engagement metrics."""
    contents: list[Content] = []
    now = dt.datetime.now()
    cat_ids = [c[0] for c in CATEGORIES]

    # Distribute 1000 contents uniformly: 200 per category as primary
    for primary_idx, primary_cat in enumerate(cat_ids):
        per_category = NUM_CONTENTS // len(CATEGORIES)  # 200
        for i in range(per_category):
            # 1-3 categories per content, primary_cat always included
            num_cats = int(rng.choice([1, 2, 3], p=[0.5, 0.35, 0.15]))
            secondary_pool = [c for c in cat_ids if c != primary_cat]
            secondaries = list(rng.choice(secondary_pool, size=num_cats - 1, replace=False))
            cats = [primary_cat] + secondaries

            # Uniform publication date over last 30 days
            age_hours = rng.uniform(0, PUBLICATION_WINDOW_DAYS * 24)
            created_at = now - dt.timedelta(hours=age_hours)

            # Rating from clipped normal
            rating = float(np.clip(
                rng.normal(RATING_MEAN, RATING_STD),
                RATING_MIN, RATING_MAX,
            ))

            content = Content(
                id=str(uuid.UUID(int=rng.integers(0, 2**128 - 1, dtype=np.uint64))),
                title=f"{CATEGORIES[primary_idx][1]} Content #{i+1:04d}",
                category_ids=cats,
                created_at=created_at,
                rating_avg=round(rating, 2),
                like_count=power_law_sample(rng, LIKE_COUNT_MAX, POWER_LAW_ALPHA),
                used_count=power_law_sample(rng, USED_COUNT_MAX, POWER_LAW_ALPHA),
                watch_count=power_law_sample(rng, WATCH_COUNT_MAX, POWER_LAW_ALPHA),
            )
            contents.append(content)

    rng.shuffle(contents)  # de-correlate IDs from category order
    return contents


def generate_user_category_stats(users: list[User]) -> list[tuple[str, str, int]]:
    """For each user, expand their archetype distribution into rows.

    Returns: list of (user_id, category_id, score)
    """
    rows: list[tuple[str, str, int]] = []
    cat_ids = [c[0] for c in CATEGORIES]
    for u in users:
        scores = ARCHETYPES[u.archetype]
        for cid, score in zip(cat_ids, scores):
            if score > 0:
                rows.append((u.id, cid, score))
    return rows


def compute_ground_truth(users: list[User], contents: list[Content]) -> list[tuple[str, str, int]]:
    """Compute rel(u, c) for every (user, content) pair following the
    relevance schema in Bab IV section 4.2.2.4:

      rel = 3 if |C(c) ∩ K_top3(u)| >= 2
      rel = 2 if |C(c) ∩ K_top3(u)| == 1
      rel = 1 if |C(c) ∩ K_any(u)| >= 1
      rel = 0 otherwise
    """
    cat_ids = [c[0] for c in CATEGORIES]
    rows: list[tuple[str, str, int]] = []

    for u in users:
        scores = list(zip(cat_ids, ARCHETYPES[u.archetype]))
        # K_top3(u) — top 3 categories by score
        scores_sorted = sorted(scores, key=lambda x: -x[1])
        k_top3 = {cid for cid, sc in scores_sorted[:GROUND_TRUTH_TOP_K] if sc > 0}
        # K_any(u) — any category with score > 0
        k_any = {cid for cid, sc in scores if sc > 0}

        for c in contents:
            content_cats = set(c.category_ids)
            top3_overlap = len(content_cats & k_top3)
            any_overlap = len(content_cats & k_any)

            if top3_overlap >= 2:
                rel = 3
            elif top3_overlap == 1:
                rel = 2
            elif any_overlap >= 1:
                rel = 1
            else:
                rel = 0

            rows.append((u.id, c.id, rel))

    return rows


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_csv(path: Path, header: list[str], rows: list[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def write_seed_sql(out_dir: Path, users: list[User], contents: list[Content],
                    user_stats: list[tuple], ground_truth: list[tuple]) -> None:
    """Emit a single SQL file with INSERT statements ready to seed MySQL.

    Note: this assumes the test database already has the schema created
    (run database/content_db.sql first). The file does not include schema
    DDL — only data.
    """
    out = out_dir / "seed.sql"
    with out.open("w", encoding="utf-8") as f:
        f.write("-- Synthetic dataset for thesis evaluation\n")
        f.write("-- Generated by: 01_generate_dataset.py\n")
        f.write("-- WARNING: this assumes a fresh test DB. It does NOT clean existing rows.\n\n")

        # Categories
        f.write("-- Categories\n")
        for cid, name, slug in CATEGORIES:
            # Use CRC32-like padding for deterministic BINARY(16) values
            padded = cid.replace("c", "0000000000000000000000000000000") + cid[-1]
            f.write(
                f"INSERT IGNORE INTO categories (id, name, slug) VALUES "
                f"(UNHEX('{padded:0<32}'), '{name}', '{slug}');\n"
            )
        f.write("\n")

        # Users
        f.write("-- Users (synthetic)\n")
        for u in users:
            uid_hex = u.id.replace("-", "")
            f.write(
                f"INSERT INTO users (id, username, status, created_at) VALUES "
                f"(UNHEX('{uid_hex}'), '{u.username}', 'active', NOW());\n"
            )
        f.write("\n")

        # Contents
        f.write("-- Contents (synthetic)\n")
        for c in contents:
            cid_hex = c.id.replace("-", "")
            ts = c.created_at.strftime("%Y-%m-%d %H:%M:%S")
            f.write(
                f"INSERT INTO contents "
                f"(id, type, status, title, rating_avg, like_count, used_count, watch_count, created_at) "
                f"VALUES (UNHEX('{cid_hex}'), 'template', 'posted', "
                f"\"{c.title}\", {c.rating_avg}, {c.like_count}, {c.used_count}, "
                f"{c.watch_count}, '{ts}');\n"
            )
        f.write("\n")

        # Content-category relations
        f.write("-- Content-category relations\n")
        for c in contents:
            cid_hex = c.id.replace("-", "")
            for cat in c.category_ids:
                cat_hex = (cat.replace("c", "0000000000000000000000000000000") + cat[-1]).ljust(32, "0")
                f.write(
                    f"INSERT INTO content_categories (content_id, category_id) VALUES "
                    f"(UNHEX('{cid_hex}'), UNHEX('{cat_hex}'));\n"
                )
        f.write("\n")

        # user_category_stats
        f.write("-- User category stats\n")
        for uid, cat, score in user_stats:
            uid_hex = uid.replace("-", "")
            cat_hex = (cat.replace("c", "0000000000000000000000000000000") + cat[-1]).ljust(32, "0")
            f.write(
                f"INSERT INTO user_category_stats (user_id, category_id, score) VALUES "
                f"(UNHEX('{uid_hex}'), UNHEX('{cat_hex}'), {score});\n"
            )

    print(f"[+] Wrote SQL seed: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).parent / "data",
                        help="Output directory (default: ./data)")
    args = parser.parse_args()

    print(f"[+] Generating synthetic dataset (seed={args.seed})")
    rng = np.random.default_rng(args.seed)
    random.seed(args.seed)

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # Users
    users = generate_users(rng)
    print(f"[+] {len(users)} users across {len(ARCHETYPES)} archetypes")

    # Contents
    contents = generate_contents(rng)
    print(f"[+] {len(contents)} contents")

    # User category stats (interest profile)
    user_stats = generate_user_category_stats(users)
    print(f"[+] {len(user_stats)} user_category_stats rows")

    # Ground truth
    ground_truth = compute_ground_truth(users, contents)
    print(f"[+] {len(ground_truth)} ground-truth (user, content) pairs")

    # Sanity: distribution of relevance levels
    rel_counts: dict[int, int] = {}
    for _, _, rel in ground_truth:
        rel_counts[rel] = rel_counts.get(rel, 0) + 1
    print(f"[+] Ground-truth relevance distribution: {dict(sorted(rel_counts.items()))}")

    # Write CSV files
    write_csv(out_dir / "users.csv",
              ["id", "username", "archetype"],
              [(u.id, u.username, u.archetype) for u in users])
    write_csv(out_dir / "categories.csv",
              ["id", "name", "slug"],
              [(cid, name, slug) for cid, name, slug in CATEGORIES])
    write_csv(out_dir / "contents.csv",
              ["id", "title", "created_at", "rating_avg", "like_count", "used_count", "watch_count"],
              [(c.id, c.title, c.created_at.isoformat(),
                c.rating_avg, c.like_count, c.used_count, c.watch_count) for c in contents])
    write_csv(out_dir / "content_categories.csv",
              ["content_id", "category_id"],
              [(c.id, cat) for c in contents for cat in c.category_ids])
    write_csv(out_dir / "user_category_stats.csv",
              ["user_id", "category_id", "score"],
              user_stats)
    write_csv(out_dir / "ground_truth.csv",
              ["user_id", "content_id", "relevance"],
              ground_truth)

    print(f"[+] CSV files written to: {out_dir}/")

    # Write SQL seed
    write_seed_sql(out_dir, users, contents, user_stats, ground_truth)

    print("[+] Done.")


if __name__ == "__main__":
    main()
