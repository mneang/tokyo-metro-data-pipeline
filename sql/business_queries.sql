-- =========================================================
-- Tokyo Metro Data Pipeline - Business Validation Queries
-- 東京メトロ データパイプライン - ビジネス検証クエリ
-- =========================================================

-- クエリ1: 路線別の乗客需要ランキング
-- Query 1: Passenger demand by line
-- 
-- ビジネス問: どの路線が最も高い乗客需要を持っているか？
-- Business Question: Which lines carry the highest passenger demand?
--
SELECT
    s.Line_Names_Jp || ' - ' || s.Line_Names_En AS line_name,
    COUNT(DISTINCT p.Station_ID) AS station_count,
    SUM(CAST(REPLACE(p.Daily_Passenger_Avg, ',', '') AS INTEGER)) AS total_daily_passengers,
    ROUND(
        SUM(CAST(REPLACE(p.Daily_Passenger_Avg, ',', '') AS INTEGER)) 
        / COUNT(DISTINCT p.Station_ID),
        0
    ) AS avg_passengers_per_station
FROM Passengers p
JOIN Stations s
    ON p.Station_ID = s.Station_ID
GROUP BY
    s.Line_Names_Jp,
    s.Line_Names_En
ORDER BY
    total_daily_passengers DESC;


-- クエリ2: 乗客需要が最も高い駅トップ10
-- Query 2: Top stations by passenger demand
--
-- ビジネス問: 運営、人員配置、乗客体験の観点で優先すべき駅はどこか？
-- Business Question: Which stations should be prioritized for operations, staffing, and passenger experience?
--
SELECT
    p.English_Name AS station_name,
    s.Line_Names_En || ' (' || s.Line_Names_Jp || ')' AS line,
    SUM(CAST(REPLACE(p.Daily_Passenger_Avg, ',', '') AS INTEGER)) AS total_daily_passengers
FROM Passengers p
JOIN Stations s
    ON p.Station_ID = s.Station_ID
GROUP BY
    p.English_Name,
    s.Line_Names_En,
    s.Line_Names_Jp
ORDER BY
    total_daily_passengers DESC
LIMIT 10;


-- クエリ3: システム全体の年度別収益推移
-- Query 3: System-wide annual revenue trend
--
-- ビジネス問: 旅客運輸収入は会計年度ごとにどのように変化しているか？
-- Business Question: How has system-wide passenger transportation revenue changed by fiscal year?
--
SELECT
    Fiscal_Year,
    SUM(Total_Revenue) AS annual_total_revenue_million_yen,
    ROUND(AVG(Total_YoY_Percentage), 1) AS avg_yoy_growth_percentage
FROM Revenue
GROUP BY
    Fiscal_Year
ORDER BY
    Fiscal_Year;


-- クエリ4: 会計年度別の収益構成（定期・定期外）
-- Query 4: Revenue mix by fiscal year (commuter vs. non-commuter)
--
-- ビジネス問: 定期・定期外の収益構成は時系列でどのように変化しているか？
-- Business Question: How do commuter and non-commuter revenue streams compare over time?
--
SELECT
    Fiscal_Year,
    SUM(Commuter_Revenue) AS commuter_revenue_million_yen,
    SUM(Non_Commuter_Revenue) AS non_commuter_revenue_million_yen,
    SUM(Total_Revenue) AS total_revenue_million_yen,
    ROUND(
        100.0 * SUM(Commuter_Revenue) / SUM(Total_Revenue),
        1
    ) AS commuter_share_percentage,
    ROUND(
        100.0 * SUM(Non_Commuter_Revenue) / SUM(Total_Revenue),
        1
    ) AS non_commuter_share_percentage
FROM Revenue
GROUP BY
    Fiscal_Year
ORDER BY
    Fiscal_Year;
