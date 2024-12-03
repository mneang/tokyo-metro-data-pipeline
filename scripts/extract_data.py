import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# === Constants ===
URL = "https://www.tokyometro.jp/lang_en/corporate/enterprise/transportation/ranking/index.html"
OUTPUT_FILE = "data/raw/passenger_stats.csv"

# === Functions ===
def fetch_page_content(url):
    """Fetch the HTML content from the Tokyo Metro website."""
    response = requests.get(url)
    if response.status_code == 200:
        print("Page fetched successfully (ページ取得成功).")
        return response.content
    else:
        raise Exception(f"Failed to fetch page, status code: {response.status_code}")

def parse_passenger_data(html_content):
    """Parse the passenger data table."""
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    
    data = []
    for row in rows[1:]:
        cols = [col.text.strip() for col in row.find_all("td")]
        if len(cols) == 5:  # Ensure the row has 5 columns
            data.append([cols[2], cols[3], cols[4]])  # Select relevant columns
        else:
            print(f"Skipping row with unexpected number of columns: {cols}")
    
    columns = ["Station", "Daily Passenger Avg", "Year-Over-Year Change"]
    df = pd.DataFrame(data, columns=columns)
    return df

def save_to_csv(df, filepath):
    """Save the DataFrame to a CSV file."""
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}.")

# === Main Execution ===
if __name__ == "__main__":
    print("Starting data extraction... (データ抽出を開始します...)")
    html_content = fetch_page_content(URL)
    passenger_data = parse_passenger_data(html_content)
    save_to_csv(passenger_data, OUTPUT_FILE)
    print("Data extraction completed. (データ抽出が完了しました。)")
