import requests
from bs4 import BeautifulSoup
import pandas as pd

# === Define constants (定数を定義) ===
URL = "https://www.tokyometro.jp/lang_en/corporate/enterprise/transportation/ranking/index.html"
OUTPUT_FILE = "data/raw/passenger_stats.csv"

# === Fetch webpage content (ウェブページの内容を取得) ===
def fetch_page_content(url):
    """Fetch the HTML content from the Tokyo Metro website (東京メトロのウェブサイトからHTMLを取得する)."""
    response = requests.get(url)
    if response.status_code == 200:
        print("Page fetched successfully (ページ取得成功).")
        return response.content
    else:
        raise Exception(f"Failed to fetch page, status code: {response.status_code}")

# === Parse data table (データテーブルを解析) ===
def parse_passenger_data(html_content):
    """Parse the passenger data table (乗客データのテーブルを解析する)."""
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")  # Locate the table element (テーブル要素を見つける)
    rows = table.find_all("tr")
    
    # Extract header (if present)
    header = [col.text.strip() for col in rows[0].find_all("th")]
    print(f"Header: {header} (ヘッダーを確認)")
    
    # Extract data into a list
    data = []
    for row in rows[1:]:  # Skip header (ヘッダーをスキップ)
        cols = [col.text.strip() for col in row.find_all("td")]
        if len(cols) == 3:  # Ensure the row has the correct number of columns
            data.append(cols)
        else:
            print(f"Skipping row with unexpected number of columns: {cols}")
    
    # Define the columns based on our expectations
    columns = ["Station", "Daily Passenger Avg", "Year-Over-Year Change"]
    df = pd.DataFrame(data, columns=columns)
    return df

# === Save data to CSV (CSVに保存) ===
def save_to_csv(df, filepath):
    """Save the DataFrame to a CSV file (データフレームをCSVファイルに保存する)."""
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath} (データが{filepath}に保存されました).")

# === Main execution (メイン処理) ===
if __name__ == "__main__":
    print("Starting data extraction... (データ抽出を開始します...)")
    html_content = fetch_page_content(URL)
    passenger_data = parse_passenger_data(html_content)
    save_to_csv(passenger_data, OUTPUT_FILE)
    print("Data extraction completed. (データ抽出が完了しました。)")
