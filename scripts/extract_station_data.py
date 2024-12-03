import json
import csv
import os

# Function to load the JSON file (JSONファイルを読み込む関数)
def load_json(file_path):
    """
    Load JSON data from a file.
    ファイルからJSONデータを読み込む。
    Args:
        file_path (str): Path to the JSON file (JSONファイルのパス)
    Returns:
        dict: Parsed JSON data (解析されたJSONデータ)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path} (ファイルが見つかりません: {file_path})")
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to write data to a CSV file (CSVファイルにデータを書き込む関数)
def write_csv(data, output_path):
    """
    Write extracted station data to a CSV file.
    抽出された駅データをCSVファイルに書き込む。
    Args:
        data (list): List of station data dictionaries (駅データの辞書のリスト)
        output_path (str): Path to the output CSV file (出力CSVファイルのパス)
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers (ヘッダーを書き込む)
        writer.writerow(['Station Code', 'Station Name (EN)', 'Station Name (JP)', 
                         'Line Code', 'Latitude', 'Longitude'])
        # Write each station's information (各駅の情報を書き込む)
        for station in data:
            writer.writerow([
                station['station_code'],
                station['station_name_en'],
                station['station_name_jp'],
                station['line_code'],
                station['latitude'],
                station['longitude']
            ])

# Main function to extract station data (駅データを抽出するメイン関数)
def main():
    """
    Main function to extract station data from a JSON file and save it to a CSV file.
    JSONファイルから駅データを抽出してCSVファイルに保存するメイン関数。
    """
    # Path to the raw JSON file (JSONファイルのパス)
    json_path = 'data/raw/stations.json'  # Adjust if needed (必要に応じて変更)
    
    # Path to the output CSV file (出力CSVファイルのパス)
    csv_output_path = 'data/raw/stations.csv'

    # Load JSON data (JSONデータを読み込む)
    try:
        stations_data = load_json(json_path)
        print("JSON data successfully loaded. (JSONデータの読み込みに成功しました。)")
    except FileNotFoundError as e:
        print(str(e))
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e} (JSONデコードエラー: {e})")
        return

    # Extract necessary information (必要な情報を抽出)
    extracted_data = []
    for line_code, line_info in stations_data['lines'].items():
        for station in line_info['stations']:
            extracted_data.append({
                'station_code': station['code'],  # Station code (駅コード)
                'station_name_en': station['name']['en'],  # Station name in English (英語の駅名)
                'station_name_jp': station['name']['ja'],  # Station name in Japanese (日本語の駅名)
                'line_code': line_code,  # Line code (路線コード)
                'latitude': station['location']['lat'],  # Latitude (緯度)
                'longitude': station['location']['lng']  # Longitude (経度)
            })

    # Save to CSV file (CSVファイルに保存)
    try:
        write_csv(extracted_data, csv_output_path)
        print(f"Station data successfully saved to {csv_output_path}. (駅データが{csv_output_path}に正常に保存されました。)")
    except Exception as e:
        print(f"Error writing to CSV: {e} (CSVへの書き込みエラー: {e})")

# Entry point for the script (スクリプトのエントリーポイント)
if __name__ == '__main__':
    main()
