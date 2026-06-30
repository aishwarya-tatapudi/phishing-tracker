# Phishing URL ETL Pipeline

A Python ETL (Extract, Transform, Load) pipeline that processes a phishing URL detection dataset, loads it into a SQLite database, and runs SQL aggregation queries to surface risk patterns distinguishing phishing URLs from legitimate ones.

## What this project does

Phishing detection datasets are usually only used for training ML classifiers. This project instead treats the dataset as a data engineering problem: extract raw feature data, transform it into a labeled, structured format, load it into a queryable database, and use SQL to answer analytical questions about what separates malicious URLs from legitimate ones.
This is a small-scale version of what email providers and browsers do to flag phishing links — using structured data about a URL to detect risk patterns instead of relying on a single signal.
## Pipeline steps

**1. Extract**
Reads `dataset.csv` — 11,055 URL records, each described by 30 binary/categorical features (e.g. `SSLfinal_State`, `having_IP_Address`, `age_of_domain`, `URL_Length`) sourced from a public phishing URL detection dataset.

**2. Transform**
Converts the raw numeric `Result` column (`-1` / `1`) into a readable `label` column (`phishing` / `legitimate`) for clarity in downstream querying.

**3. Load**
Writes the transformed dataset into a local SQLite database (`phishing_analysis.db`), creating a queryable `url_features` table — no server setup required.

**4. Analyze**
Runs SQL aggregation queries directly against the database to answer:
- How many phishing vs. legitimate URLs are in the dataset?
- How do risk signals (SSL state, URL length, domain age) differ by class?
- How many URLs trigger multiple high-risk flags simultaneously?

## Key findings

| Metric | Legitimate | Phishing |
|---|---|---|
| Count | 6,157 | 4,898 |
| Avg. SSL score | 0.83 | -0.48 |
| Avg. domain age score | 0.17 | -0.07 |
| Avg. URL length score | -0.59 | -0.68 |

- Phishing URLs show a sharply worse average SSL certificate score than legitimate URLs.
- Phishing URLs tend to use newer domains than legitimate ones.
- **193 URLs** simultaneously triggered all three high-risk signals (suspicious IP usage, excessive URL length, and poor SSL state) and were confirmed phishing — demonstrating that combining multiple weak signals can reliably flag high-risk URLs.

## Tech stack

- **Python** — pandas for data extraction and transformation
- **SQLite** — lightweight, file-based relational database for the load step
- **SQL** — aggregation, filtering, and grouping queries for analysis

## Files

| File | Description |
|---|---|
| `phishing_pipeline.py` | Main ETL script — extract, transform, load, and query |
| `dataset.csv` | Raw input dataset (30-feature phishing URL data) |
| `phishing_analysis.db` | Generated SQLite database (created when the script runs) |

## How to run

```bash
pip install pandas
python phishing_pipeline.py
```

## Dataset

Phishing Websites Dataset — 11,055 records, 30 features, sourced from the UCI Machine Learning Repository / Kaggle phishing detection dataset collection.
