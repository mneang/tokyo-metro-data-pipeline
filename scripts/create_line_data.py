import os
import pandas as pd

# Paths for input and output files (入力ファイルと出力ファイルのパス)
INPUT_STATIONS_PATH = "./data/cleaned/stations_cleaned.csv"
OUTPUT_LINES_PATH = "./data/cleaned/lines_cleaned.csv"


def create_lines_table(stations_data):
    """
    Create a normalized Lines table from cleaned station data.
    (クリーン済み駅データから正規化された路線テーブルを作成します)

    The cleaned station data should already have one Line_ID per station row.
    (クリーン済み駅データでは、各駅行に1つのLine_IDがある前提です)
    """
    required_columns = ["Line_IDs", "Line_Names_En", "Line_Names_Jp"]

    # Validate required columns before transformation.
    # 変換前に必要な列を検証します。
    missing_columns = [col for col in required_columns if col not in stations_data.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns in station data: {missing_columns} "
            f"(駅データに必要な列が不足しています: {missing_columns})"
        )

    # Extract line metadata and rename fields for the Lines table.
    # 路線メタデータを抽出し、Linesテーブル用に列名を変更します。
    lines_data = (
        stations_data[required_columns]
        .drop_duplicates()
        .rename(
            columns={
                "Line_IDs": "Line_ID",
                "Line_Names_En": "Line_Name_En",
                "Line_Names_Jp": "Line_Name_Jp",
            }
        )
    )

    # Strip whitespace for reliable SQL joins.
    # SQL結合を安定させるため、前後の空白を削除します。
    for col in ["Line_ID", "Line_Name_En", "Line_Name_Jp"]:
        lines_data[col] = lines_data[col].astype(str).str.strip()

    # Enforce one row per Line_ID.
    # Line_IDごとに1行であることを保証します。
    duplicate_line_ids = lines_data[
        lines_data["Line_ID"].duplicated(keep=False)
    ].sort_values("Line_ID")

    if not duplicate_line_ids.empty:
        print("Duplicate Line_ID values found. (重複するLine_IDが見つかりました。)")
        print(duplicate_line_ids)
        raise ValueError(
            "Line_ID must be unique before SQLite loading. "
            "(SQLiteに読み込む前にLine_IDは一意である必要があります。)"
        )

    # Sort for readable output.
    # 読みやすい出力のために並び替えます。
    lines_data = lines_data.sort_values("Line_ID").reset_index(drop=True)

    return lines_data


def save_lines_table(lines_data):
    """
    Save the Lines table to CSV.
    (路線テーブルをCSVに保存します)
    """
    os.makedirs(os.path.dirname(OUTPUT_LINES_PATH), exist_ok=True)
    lines_data.to_csv(OUTPUT_LINES_PATH, index=False, encoding="utf-8")

    print(
        f"Lines data cleaned and saved to {OUTPUT_LINES_PATH}. "
        f"(路線データをクリーニングし、{OUTPUT_LINES_PATH} に保存しました。)"
    )
    print(f"Rows saved: {len(lines_data)} (保存行数: {len(lines_data)})")


def main():
    """
    Run line data creation.
    (路線データ作成を実行します)
    """
    print("Starting line data creation. (路線データ作成を開始します。)")

    # Validate input file exists
    # (入力ファイルの存在を確認)
    from pathlib import Path
    input_path = Path(INPUT_STATIONS_PATH)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_STATIONS_PATH} (入力ファイルが見つかりません: {INPUT_STATIONS_PATH})"
        )

    stations_data = pd.read_csv(INPUT_STATIONS_PATH)

    # Validate input data is not empty
    # (入力データが空でないことを確認)
    if stations_data.empty:
        raise ValueError(
            f"Input file is empty: {INPUT_STATIONS_PATH} (入力ファイルが空です: {INPUT_STATIONS_PATH})"
        )

    lines_data = create_lines_table(stations_data)
    save_lines_table(lines_data)

    print("Line data creation completed. (路線データ作成が完了しました。)")


if __name__ == "__main__":
    main()