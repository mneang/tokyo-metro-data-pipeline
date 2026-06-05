import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = "./tokyo_metro.db"
SCHEMA_PATH = "./sql/create_schema.sql"

TABLE_LOADS = [
    ("Lines", "./data/cleaned/lines_cleaned.csv"),
    ("Stations", "./data/cleaned/stations_cleaned.csv"),
    ("Passengers", "./data/cleaned/passengers_cleaned.csv"),
    ("Revenue", "./data/cleaned/revenues_cleaned.csv"),
]


def reset_database(db_path: str, schema_path: str) -> sqlite3.Connection:
    """
    Create a fresh SQLite database from the schema file.
    (スキーマファイルから新しいSQLiteデータベースを作成します)
    """
    db_file = Path(db_path)

    if db_file.exists():
        db_file.unlink()
        print(f"Removed existing database: {db_path} (既存のデータベースを削除しました: {db_path})")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(schema_path, "r", encoding="utf-8") as schema_file:
        conn.executescript(schema_file.read())

    print("Database schema created successfully. (データベーススキーマを正常に作成しました。)")
    return conn


def load_csv_to_table(conn: sqlite3.Connection, table_name: str, csv_path: str) -> None:
    """
    Load a cleaned CSV file into an existing SQLite table.
    (クリーン済みCSVファイルを既存のSQLiteテーブルに読み込みます)
    """
    df = pd.read_csv(csv_path)

    # Preserve schema constraints by appending into existing tables.
    # 既存テーブルに追加することでスキーマ制約を維持します。
    df.to_sql(table_name, conn, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows into {table_name}. ({table_name}に{len(df)}行を読み込みました。)")


def validate_row_counts(conn: sqlite3.Connection) -> None:
    """
    Print row counts for each database table.
    (各データベーステーブルの行数を表示します)
    """
    print("\nRow count validation (行数検証):")

    for table_name, _ in TABLE_LOADS:
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()[0]
        print(f"- {table_name}: {row_count} rows")


def main() -> None:
    """
    Rebuild the SQLite database from cleaned CSV outputs.
    (クリーン済みCSV出力からSQLiteデータベースを再構築します)
    """
    conn = reset_database(DB_PATH, SCHEMA_PATH)

    for table_name, csv_path in TABLE_LOADS:
        load_csv_to_table(conn, table_name, csv_path)

    validate_row_counts(conn)

    conn.close()
    print("\nSQLite database rebuilt successfully. (SQLiteデータベースの再構築が完了しました。)")


if __name__ == "__main__":
    main()