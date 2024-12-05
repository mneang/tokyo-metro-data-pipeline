import pandas as pd

def normalize_column_names(df):
    """
    Normalize column names by replacing spaces and special characters with underscores.
    (列名を正規化するためにスペースや特殊文字をアンダースコアに置き換えます)
    """
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("%", "Percentage", regex=False)
    )
    return df

def clean_revenue_data(revenue_data):
    """
    Clean the revenue data by normalizing column names, adding fiscal month mappings,
    and calculating the calendar year.
    (列名を正規化し、会計月のマッピングを追加し、暦年を計算することで収益データをクリーニングします)
    """
    # Normalize column names (列名を正規化)
    revenue_data = normalize_column_names(revenue_data)

    # Add Calendar_Month based on Fiscal_Month (会計月に基づいてカレンダ月を追加)
    fiscal_to_calendar = {
        1: "April", 2: "May", 3: "June", 4: "July",
        5: "August", 6: "September", 7: "October",
        8: "November", 9: "December", 10: "January",
        11: "February", 12: "March",
    }
    revenue_data["Calendar_Month"] = revenue_data["Fiscal_Month"].map(fiscal_to_calendar)

    # Calculate Calendar_Year based on Fiscal_Month (会計月に基づいて暦年を計算)
    revenue_data["Calendar_Year"] = revenue_data.apply(
        lambda row: row["Fiscal_Year"] if row["Fiscal_Month"] > 9 else row["Fiscal_Year"] - 1,
        axis=1,
    )

    # Validate the Calendar_Year mapping (暦年マッピングを検証)
    if revenue_data["Calendar_Year"].isnull().any():
        raise ValueError("Some fiscal months could not be mapped to calendar years. (一部の会計月が暦年にマッピングできませんでした)")

    return revenue_data

def main():
    # Load raw revenue data (生の収益データをロード)
    revenue_path = "./data/processed/revenue_data.csv"
    revenue_data = pd.read_csv(revenue_path)
    print(f"Columns in revenue_data before processing: {revenue_data.columns}")

    # Clean the revenue data (収益データをクリーニング)
    cleaned_revenue = clean_revenue_data(revenue_data)

    print(f"Columns in revenue_data after processing: {cleaned_revenue.columns}")

    # Save the cleaned revenue data (クリーニング済みの収益データを保存)
    output_path = "./data/cleaned/revenues_cleaned.csv"
    cleaned_revenue.to_csv(output_path, index=False)
    print(f"Cleaned revenue data saved to {output_path}. (清潔な収益データが{output_path}に保存されました)")

if __name__ == "__main__":
    main()
