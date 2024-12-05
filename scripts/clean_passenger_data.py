import pandas as pd
import os

# Paths for input and output files
input_passenger_path = './data/processed/passenger_stats.csv'  # Updated to use 'processed' folder
input_stations_path = './data/processed/station_data_with_lines.csv'  # Updated to use 'processed' folder
output_passenger_path = './data/cleaned/passengers_cleaned.csv'

def clean_passenger_data(passenger_data, station_data):
    """
    Clean the passenger data and map it to Station_IDs from station data.
    (乗客データをクリーンアップし、駅データのStation_IDにマッピングする)
    """
    # Normalize column names (列名を正規化する)
    passenger_data.rename(columns={
        'Station': 'English_Name',
        'Daily Passenger Avg': 'daily_passenger_avg',
        'Year-Over-Year Change': 'year_over_year_change'
    }, inplace=True)

    # Merge passenger data with stations data to map Station_ID
    # (駅データとマージしてStation_IDをマッピングする)
    merged_data = pd.merge(passenger_data, station_data[['Station_ID', 'English_Name']],
                           on='English_Name', how='left')

    # Check for unmatched stations (一致しない駅のチェック)
    unmatched = merged_data[merged_data['Station_ID'].isnull()]
    if not unmatched.empty:
        print("Unmatched stations found: (一致しない駅が見つかりました):")
        print(unmatched[['English_Name']])

    # Drop unmatched rows or handle them as needed (一致しない行を削除または処理)
    cleaned_data = merged_data.dropna(subset=['Station_ID'])

    return cleaned_data

def save_cleaned_data(cleaned_data):
    """
    Save the cleaned passenger data to a CSV file.
    (クリーンアップされた乗客データをCSVファイルに保存する)
    """
    cleaned_data.to_csv(output_passenger_path, index=False, encoding='utf-8')
    print("Passenger data cleaned and saved. (乗客データがクリーンアップされ保存されました)")

def main():
    # Load datasets (データセットを読み込む)
    passenger_data = pd.read_csv(input_passenger_path)
    station_data = pd.read_csv(input_stations_path)

    # Clean the data (データをクリーンアップする)
    cleaned_data = clean_passenger_data(passenger_data, station_data)

    # Save the cleaned data (クリーンアップされたデータを保存する)
    save_cleaned_data(cleaned_data)

if __name__ == '__main__':
    main()
