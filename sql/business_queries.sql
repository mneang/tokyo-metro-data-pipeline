-- =========================================================
-- Tokyo Metro Data Pipeline - Business Validation Queries
-- 東京メトロ データパイプライン - ビジネス検証クエリ
-- =========================================================

-- Query 1: Passenger demand by line
-- クエリ1: 路線別の乗客需要
-- Business question:
-- Which lines carry the highest passenger demand?
-- どの路線が最も高い乗客需要を持っているか？
SELECT
    s.Line_Names_Jp || ' - ' || s.Line_Names_En AS line_name,
    SUM(CAST(REPLACE(p.daily_passenger_avg, ',', '') AS INTEGER)) AS total_daily_passengers
FROM Passengers p
JOIN Stations s
    ON p.Station_ID = s.Station_ID
GROUP BY
    s.Line_Names_Jp,
    s.Line_Names_En
ORDER BY
    total_daily_passengers DESC;


-- Query 2: Top stations by passenger demand
-- クエリ2: 乗客需要が最も高い駅
-- Business question:
-- Which stations should be prioritized for operations, staffing, and passenger experience?
-- 運営、人員配置、乗客体験の観点で優先すべき駅はどこか？
SELECT
    p.English_Name AS station_name_en,
    SUM(CAST(REPLACE(p.daily_passenger_avg, ',', '') AS INTEGER)) AS total_daily_passengers
FROM Passengers p
GROUP BY
    p.English_Name
ORDER BY
    total_daily_passengers DESC
LIMIT 10;


-- Query 3: System-wide annual revenue trend
-- クエリ3: システム全体の年度別収益推移
-- Business question:
-- How has system-wide passenger transportation revenue changed by fiscal year?
-- 旅客運輸収入は会計年度ごとにどのように変化しているか？
SELECT
    Fiscal_Year,
    SUM(Total_Revenue) AS annual_total_revenue_million_yen,
    ROUND(AVG(Total_YoY_Percentage), 1) AS avg_total_yoy_percentage
FROM Revenue
GROUP BY
    Fiscal_Year
ORDER BY
    Fiscal_Year;


-- Query 4: Revenue mix by fiscal year
-- クエリ4: 会計年度別の収益構成
-- Business question:
-- How do commuter and non-commuter revenue streams compare over time?
-- 定期・定期外収益は時系列でどのように変化しているか？
SELECT
    Fiscal_Year,
    SUM(Commuter_Revenue) AS commuter_revenue_million_yen,
    SUM(Non_Commuter_Revenue) AS non_commuter_revenue_million_yen,
    SUM(Total_Revenue) AS total_revenue_million_yen,
    ROUND(
        100.0 * SUM(Non_Commuter_Revenue) / SUM(Total_Revenue),
        1
    ) AS non_commuter_share_percentage
FROM Revenue
GROUP BY
    Fiscal_Year
ORDER BY
    Fiscal_Year;
