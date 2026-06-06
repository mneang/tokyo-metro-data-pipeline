import os
import pandas as pd

# Paths for input and output files (入力ファイルと出力ファイルのパス)
INPUT_STATION_PATH = "./data/processed/station_data_with_lines.csv"
OUTPUT_STATION_PATH = "./data/cleaned/stations_cleaned.csv"


def normalize_station_lines(row):
    """
    Normalize line fields for each station row.
    (各駅行の路線フィールドを正規化します)

    Important:
    - Station_ID should remain unique.
    - Marunouchi Branch stations such as Mb03, Mb04, and Mb05 should map to Mb only.
    - This prevents duplicate Station_ID values in SQLite.

    重要:
    - Station_IDは一意に保ちます。
    - Mb03、Mb04、Mb05などの丸ノ内線分岐線の駅はMbのみに紐づけます。
    - これによりSQLiteでStation_IDの重複を防ぎます。
    """
    station_id = str(row["Station_ID"]).strip()

    # Marunouchi Branch stations should belong to Mb only.
    # 丸ノ内線分岐線の駅はMbのみに所属させます。
    if station_id.startswith("Mb"):
        row["Line_IDs"] = "Mb"
        row["Line_Names_En"] = "Marunouchi Line Branch Line"
        row["Line_Names_Jp"] = "丸ノ内線分岐線"

    return row


def clean_station_data(station_data):
    """
    Clean station data for relational database loading.
    (リレーショナルデータベースに読み込むために駅データをクリーニングします)
    """
    # Standardize possible column-name variants.
    # 可能性のある列名の揺れを標準化します。
    station_data = station_data.rename(
        columns={
            "Line_ID": "Line_IDs",
            "Line_Name_En": "Line_Names_En",
            "Line_Name_Jp": "Line_Names_Jp",
        }
    )

    required_columns = [
        "Station_ID",
        "English_Name",
        "Japanese_Name",
        "Line_IDs",
        "Line_Names_En",
        "Line_Names_Jp",
    ]

    # Validate required columns before cleaning.
    # クリーニング前に必要な列を検証します。
    missing_columns = [col for col in required_columns if col not in station_data.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns} "
            f"(必要な列が不足しています: {missing_columns})"
        )

    # Keep only the columns needed for the relational model.
    # リレーショナルモデルに必要な列のみを保持します。
    cleaned_data = station_data[required_columns].copy()

    # Strip whitespace from text fields.
    # テキスト項目の前後の空白を削除します。
    for col in required_columns:
        cleaned_data[col] = cleaned_data[col].astype(str).str.strip()

    # Normalize Marunouchi Branch stations.
    # 丸ノ内線分岐線の駅を正規化します。
    cleaned_data = cleaned_data.apply(normalize_station_lines, axis=1)

    # Remove exact duplicate rows.
    # 完全に重複した行を削除します。
    cleaned_data = cleaned_data.drop_duplicates()

    # Enforce one row per Station_ID for SQLite primary key integrity.
    # SQLiteの主キー整合性のため、Station_IDごとに1行にします。
    duplicate_station_ids = cleaned_data[
        cleaned_data["Station_ID"].duplicated(keep=False)
    ].sort_values("Station_ID")

    if not duplicate_station_ids.empty:
        print("Duplicate Station_ID values found. (重複するStation_IDが見つかりました。)")
        print(
            duplicate_station_ids[
                ["Station_ID", "English_Name", "Line_IDs", "Line_Names_En"]
            ]
        )
        raise ValueError(
            "Station_ID must be unique before SQLite loading. "
            "(SQLiteに読み込む前にStation_IDは一意である必要があります。)"
        )

    return cleaned_data


def save_cleaned_data(cleaned_data):
    """
    Save cleaned station data to CSV.
    (クリーン済み駅データをCSVに保存します)
    """
    os.makedirs(os.path.dirname(OUTPUT_STATION_PATH), exist_ok=True)
    cleaned_data.to_csv(OUTPUT_STATION_PATH, index=False, encoding="utf-8")

    print(
        f"Station data cleaned and saved to {OUTPUT_STATION_PATH}. "
        f"(駅データをクリーニングし、{OUTPUT_STATION_PATH} に保存しました。)"
    )
    print(f"Rows saved: {len(cleaned_data)} (保存行数: {len(cleaned_data)})")


def main():
    """
    Run station data cleaning.
    (駅データのクリーニングを実行します)
    """
    print("Starting station data cleaning. (駅データのクリーニングを開始します。)")

    # Validate input file exists
    # (入力ファイルの存在を確認)
    from pathlib import Path
    input_path = Path(INPUT_STATION_PATH)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_STATION_PATH} (入力ファイルが見つかりません: {INPUT_STATION_PATH})"
        )

    station_data = pd.read_csv(INPUT_STATION_PATH)

    # Validate input data is not empty
    # (入力データが空でないことを確認)
    if station_data.empty:
        raise ValueError(
            f"Input file is empty: {INPUT_STATION_PATH} (入力ファイルが空です: {INPUT_STATION_PATH})"
        )

    cleaned_data = clean_station_data(station_data)
    save_cleaned_data(cleaned_data)

    print("Station data cleaning completed. (駅データのクリーニングが完了しました。)")


if __name__ == "__main__":
    main()