import pandas as pd

# Paths for input and output files
input_stations_path = './data/cleaned/stations_cleaned.csv'
output_lines_path = './data/cleaned/lines_cleaned.csv'

def create_lines_table(stations_data):
    """
    Create a Lines table from the Stations data.
    (駅データから路線テーブルを作成する)
    """
    # Extract unique Line_IDs and Line_Names
    lines_data = stations_data[['Line_IDs', 'Line_Name_En', 'Line_Name_Jp']].drop_duplicates()

    # Rename columns for consistency
    lines_data.rename(columns={
        'Line_IDs': 'Line_ID',
        'Line_Names_En': 'Line_Name_En',
        'Line_Names_Jp': 'Line_Name_Jp'
    }, inplace=True)

    # Remove rows with missing Line_IDs
    lines_data = lines_data.dropna(subset=['Line_ID'])

    # Ensure no duplicate Line_IDs
    lines_data = lines_data.drop_duplicates(subset=['Line_ID'])

    return lines_data

def save_lines_table(lines_data):
    """
    Save the Lines table to a CSV file.
    (路線テーブルをCSVファイルに保存する)
    """
    lines_data.to_csv(output_lines_path, index=False, encoding='utf-8')
    print("Lines table created and saved. (路線テーブルが作成され保存されました)")

def main():
    # Load the stations data
    stations_data = pd.read_csv(input_stations_path)

    # Create the Lines table
    lines_data = create_lines_table(stations_data)

    # Save the Lines table
    save_lines_table(lines_data)

if __name__ == '__main__':
    main()
