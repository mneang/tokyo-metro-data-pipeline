# Tokyo Metro Data Pipeline
## 東京メトロ データパイプライン

**Completed for the GitHub Finish-Up-A-Thon challenge** | [View Dashboard](assets/dashboard/)

Analyze Tokyo Metro passenger and revenue patterns to answer critical business questions: Which lines are most profitable? Where should operational resources be prioritized? How does revenue evolve across fiscal years?

This project demonstrates a **complete data pipeline**: from raw data extraction through ETL, relational database design, exploratory analysis, and business intelligence visualization—ready for stakeholder decision-making.

東京メトロの乗客統計と収益パターンを分析し、重要なビジネス上の質問に答えます。本プロジェクトは、データ抽出からETL、リレーショナルデータベース設計、探索的分析、ビジネスインテリジェンスの可視化までの完全なパイプラインを実装しています。

---

## Business Questions Answered
### ビジネス課題

| Question | Insight |
|----------|---------|
| **Which lines carry the highest passenger demand?** (最高の乗客需要を持つ路線は?) | Identify capacity planning priorities and investment opportunities |
| **Which stations are major passenger hubs?** (主要な乗客ハブとなる駅は?) | Optimize staffing, facilities, and passenger experience at critical stations |
| **How has annual revenue trended?** (年度別収益の推移は?) | Track system-wide financial performance and growth |
| **How do commuter vs. non-commuter streams compare?** (定期・定期外の収益比較は?) | Understand revenue diversification and risk exposure |

---

## Project Architecture
### プロジェクト構成

```
Data Sources
    ↓
[Python ETL Scripts]
    • extract_*.py: Pull raw data from JSON, PDFs, APIs
    • clean_*.py: Normalize station IDs, passenger counts, revenue
    • create_line_data.py: Derive normalized Lines table
    ↓
[Cleaned CSV]
    ↓
[SQLite Database]
    • Relational schema with foreign keys
    • Stations → Lines (many-to-one)
    • Passengers, Revenue (fact tables)
    ↓
[SQL Analytics]
    ↓
[Tableau Dashboard]
    ✓ Passenger demand by line & station
    ✓ Revenue trends & composition
    ✓ Year-over-year growth rates
```

---

## Deliverables
### 成果物

| Artifact | Purpose |
|----------|---------|
| **Data/** | Raw, processed, and cleaned CSVs at each ETL stage |
| **Scripts/** | Python ETL pipeline with validation & error handling |
| **SQL/** | Schema definition + business analytics queries |
| **Database** | `tokyo_metro.db` (SQLite with relational integrity) |
| **ERD** | [Entity-Relationship Diagram](assets/erd/) showing normalized schema |
| **Dashboard** | [Tableau Public](assets/dashboard/) for executive reporting |

---

## Quick Start
### クイックスタート

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Pipeline
```bash
# 1. Extract and clean data
python scripts/extract_station_data.py
python scripts/extract_passenger_data.py
python scripts/extract_revenue_data.py

# 2. Normalize and transform
python scripts/clean_station_data.py
python scripts/clean_passenger_data.py
python scripts/clean_revenue_data.py
python scripts/create_line_data.py

# 3. Load into SQLite
python scripts/import_data_to_sqlite.py

# 4. Run analytics
sqlite3 tokyo_metro.db < sql/business_queries.sql
```

### View Results
- **Database**: `tokyo_metro.db` (inspect with any SQLite client)
- **Analytics**: See `sql/business_queries.sql` for stakeholder-focused queries
- **Dashboard**: Open [assets/dashboard/](assets/dashboard/) in Tableau or browser

---

## Key Features
### 主な特徴

✅ **End-to-end ETL pipeline** with input validation and error handling  
✅ **Normalized relational schema** maintaining referential integrity  
✅ **Bilingual code comments** (English + Japanese) for global collaboration  
✅ **Business-focused SQL queries** with clear naming and bilingual questions  
✅ **Tableau dashboard** for non-technical stakeholder decision-making  
✅ **Robust error handling** in Python scripts (file existence, empty data, schema mismatches)  

---

## Project Journey: Before & After
### プロジェクト完成の経過

**Before (Unfinished State):**
- ❌ ETL scripts lacked validation and error handling
- ❌ Data cleaning logic unclear; duplicates and null handling inconsistent
- ❌ No schema documentation or ERD
- ❌ SQL queries unoptimized and poorly commented
- ❌ No business framing or executive dashboard

**After (GitHub Finish-Up-A-Thon Completion):**
- ✅ Added file existence checks, empty DataFrame validation, schema matching
- ✅ Clarified data normalization rules (e.g., Marunouchi Branch mapping to Mb)
- ✅ Created relational schema with clear constraints
- ✅ Rewrote SQL queries with bilingual comments and stakeholder-focused business questions
- ✅ Built Tableau dashboard linking all insights to actionable business metrics

---

## Caveats & Limitations
### 注意事項

- **Data Scope**: Passenger and revenue data are historical aggregates; real-time data not included
- **Time Coverage**: Fiscal year boundaries may not align with calendar years (documented in Revenue table)
- **Marunouchi Branch Normalization**: Branch stations (Mb03, Mb04, Mb05) are consolidated to Mb line for referential integrity
- **Aggregate Metrics**: Daily passenger averages are system-wide aggregates; station-level micro-variations not captured
- **Manual Data Entry**: Source PDFs and JSON files require periodic re-extraction; no automated refresh

---

## Role of GitHub Copilot
### GitHub Copilotの活用

This project was revived and completed with GitHub Copilot assistance for:
- **Code review**: Identified gaps in error handling and validation across Python scripts
- **Query optimization**: Suggested bilingual SQL comments and stakeholder-focused business logic
- **Documentation**: Helped structure and clarify README, schema documentation, and query intent
- **Best practices**: Recommended Path validation, exception handling, and DataFrame checks for robustness

---

## Next Steps (Optional)
### 今後の展開

- [ ] Integrate real-time passenger tracking API for live dashboards
- [ ] Add predictive models (time-series forecasting for revenue trends)
- [ ] Automate weekly data refresh pipeline with scheduled tasks
- [ ] Expand to include operational metrics (delays, overcrowding alerts)

---

## Acknowledgments

**Data Source**: Tokyo Metro public datasets  
**Challenge**: GitHub Finish-Up-A-Thon  
**Tech Stack**: Python · SQLite · SQL · Tableau · Git  
**Language**: English & Japanese (日本語 & 英語)

---

*Last Updated: 2026-06-06*
