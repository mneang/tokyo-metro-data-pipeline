import sqlite3
import pandas as pd

def import_csv_to_sqlite(db_path, csv_path, table_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

def main():
    db_path = "./tokyo_metro.db"
    import_csv_to_sqlite(db_path, "./data/cleaned/lines_cleaned.csv", "Lines")
    import_csv_to_sqlite(db_path, "./data/cleaned/stations_cleaned.csv", "Stations")
    import_csv_to_sqlite(db_path, "./data/cleaned/passengers_cleaned.csv", "Passengers")
    import_csv_to_sqlite(db_path, "./data/cleaned/revenues_cleaned.csv", "Revenue")
    print("Data imported successfully.")

if __name__ == "__main__":
    main()
