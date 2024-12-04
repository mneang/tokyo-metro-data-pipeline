import json
import csv
import os

def load_json(file_path):
    """Load JSON data from a file. (ファイルからJSONデータを読み込む)"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_station_data(json_data, output_path):
    """
    Extract station data with line details into a CSV file.
    路線情報を含む駅データをCSVファイルに抽出する。
    Args:
        json_data (dict): Parsed JSON data (解析されたJSONデータ)
        output_path (str): Output path for the CSV file (出力CSVファイルのパス)
    """
    stations = json_data.get('stations', {})  # Stations data (駅データ)
    lines = json_data.get('lines', {})        # Lines data (路線データ)
    
    # Create a mapping of station IDs to line details (駅IDと路線情報のマッピングを作成)
    station_to_lines = {}
    for line_id, line_info in lines.items():
        # No longer checking for `stations` list under `lines`
        for station_id in stations.keys():  # Match by station IDs in the global list
            if station_id.startswith(line_id):
                station_to_lines.setdefault(station_id, []).append({
                    "line_id": line_id,
                    "line_name_en": line_info.get("name_en", ""),
                    "line_name_jp": line_info.get("name_jp", "")
                })

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Station_ID', 'English_Name', 'Japanese_Name', 
                      'Line_IDs', 'Line_Names_En', 'Line_Names_Jp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for station_id, station_info in stations.items():
            # Retrieve lines associated with this station (この駅に関連する路線を取得)
            line_details = station_to_lines.get(station_id, [])
            line_ids = [line["line_id"] for line in line_details]
            line_names_en = [line["line_name_en"] for line in line_details]
            line_names_jp = [line["line_name_jp"] for line in line_details]
            
            writer.writerow({
                'Station_ID': station_id,
                'English_Name': station_info.get('name_en', ''),
                'Japanese_Name': station_info.get('name_jp', ''),
                'Line_IDs': ', '.join(line_ids),
                'Line_Names_En': ', '.join(line_names_en),
                'Line_Names_Jp': ', '.join(line_names_jp),
            })
    print("Station data extraction completed successfully. (駅データの抽出が正常に完了しました。)")

def main():
    """
    Main function to extract station data with line details.
    路線情報を含む駅データを抽出するメイン関数。
    """
    json_path = "./data/raw/stations.json"
    output_csv_path = "./data/processed/station_data_with_lines.csv"
    
    if not os.path.exists(json_path):
        print("JSON file not found. Please check the path. (JSONファイルが見つかりません。パスを確認してください)")
        return
    
    try:
        json_data = load_json(json_path)
        print("JSON data successfully loaded. (JSONデータの読み込みに成功しました。)")
        extract_station_data(json_data, output_csv_path)
    except KeyError as e:
        print(f"KeyError: {e} (キーエラー: {e})")
    except Exception as e:
        print(f"An error occurred: {e} (エラーが発生しました: {e})")

if __name__ == "__main__":
    main()
