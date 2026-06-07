# 東京メトロ 需要・収益分析 / Tokyo Metro Demand & Revenue Analytics

A compact, bilingual data analytics project that turns Tokyo Metro public datasets into a cleaned data pipeline, validated SQLite database, SQL analysis layer, and Tableau dashboard.

東京メトロの公開データをもとに、乗客需要・主要駅・収益推移を分析する日英バイリンガル分析プロジェクトです。

**Dashboard:** [View on Tableau Public](https://public.tableau.com/views/_17808045955120/sheet8?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

---

## Final Dashboard / 最終ダッシュボード

<img width="1536" height="852" alt="Dashboard Final" src="https://github.com/user-attachments/assets/6b68c11c-0a71-46ba-8791-45416159b332" />

This dashboard highlights passenger demand by line, major station hubs, and system-wide revenue trends. Revenue is system-wide, while passenger metrics are station/line-based.

---

## Business Questions / 分析課題

| Question | Why it matters |
|---|---|
| Which lines carry the highest passenger demand? | Supports capacity planning and operational prioritization. |
| Which stations act as major passenger hubs? | Helps identify where staffing, wayfinding, and facility attention matter most. |
| How has revenue changed by fiscal year? | Shows system-wide recovery and financial trend direction. |
| How can cleaned transit data become a stakeholder-ready dashboard? | Demonstrates an end-to-end analytics workflow from ETL to visualization. |

---

## Project Flow / プロジェクト構成

```text
Raw / processed data
        ↓
Python cleaning scripts
        ↓
Cleaned CSV datasets
        ↓
SQLite database + SQL validation
        ↓
Business queries
        ↓
Tableau dashboard
```

---

## Data Model / データモデル

<img width="3000" height="765" alt="tokyo_metro_erd" src="https://github.com/user-attachments/assets/63f3635b-98a6-46c4-8234-0a6d025da3b5" />

The relational model connects passenger records to stations and lines:

```text
Lines → Stations → Passengers
```

<img width="2400" height="1300" alt="revenue_standalone_table" src="https://github.com/user-attachments/assets/45ed681a-f1a6-4cc8-aef7-c650f84c6945" />

Revenue is intentionally modeled separately because the available revenue data is system-wide and not tied to individual stations or lines.

---

## Tech Stack / 使用技術

- **Python / pandas** — data cleaning and transformation
- **SQLite** — database creation and validation
- **SQL** — stakeholder-focused analysis queries
- **Tableau** — final dashboard
- **GitHub Copilot** — code review, validation suggestions, and query/documentation polish

---

## Repository Structure / リポジトリ構成

```text
data/
  raw/          source files
  processed/    intermediate extracted data
  cleaned/      final cleaned CSVs

scripts/        extraction, cleaning, and SQLite loading scripts
sql/            schema and business queries
assets/         ERD, screenshots, dashboard images
tokyo_metro.db  generated SQLite database
```

---

## Run the Pipeline / 実行方法

```bash
pip install -r requirements.txt

python scripts/clean_station_data.py
python scripts/clean_passenger_data.py
python scripts/clean_revenue_data.py
python scripts/create_line_data.py
python scripts/import_data_to_sqlite.py
```

Optional SQL analysis:

```bash
sqlite3 tokyo_metro.db < sql/business_queries.sql
```

---

## Key Outputs / 主な成果物

- Cleaned CSV files for lines, stations, passengers, and revenue
- SQLite database with validated table loads
- SQL queries answering transit/business questions
- ERD documenting table relationships
- Japanese-first bilingual Tableau dashboard

---

## Notes & Limitations / 注意事項

- Japan’s fiscal year runs from **April to March**.
- Revenue data is **system-wide**, not station- or line-specific.
- Passenger charts use available station/line passenger records from the cleaned dataset.
- The dashboard is designed for portfolio and analytical storytelling, not real-time operations.

---

## How GitHub Copilot Helped / Copilotの活用

GitHub Copilot was used as a review and finishing assistant. It helped identify validation improvements in the Python scripts, suggested clearer SQL/business-query structure, and supported documentation polish. I manually reviewed the suggestions and kept the changes that preserved the data model and project scope.

---

## Future Improvements / 今後の改善案

- Add automated refresh steps if newer source data is available.
- Include geospatial coordinates for a future station map.
- Add forecasting once more years of revenue data are available.

---

## Data Source

Tokyo Metro public datasets.
