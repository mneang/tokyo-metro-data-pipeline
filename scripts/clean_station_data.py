import pandas as pd
import os

def clean_station_data(input_path, output_path):
    # Load the raw data
    print("Loading raw station data... (生データをロード中...)")
    stations = pd.read_csv(input_path)
    
    # Initialize a list to store cleaned rows
    cleaned_rows = []
    
    # Process each row
    for _, row in stations.iterrows():
        line_ids = row['Line_IDs'].split(', ')
        line_names_en = row['Line_Names_En'].split(', ')
        line_names_jp = row['Line_Names_Jp'].split(', ')
        
        # Check for multiple Line_IDs (e.g., 'M, Mb')
        for line_id, line_name_en, line_name_jp in zip(line_ids, line_names_en, line_names_jp):
            # Create a new row for each line
            new_row = row.copy()
            new_row['Line_IDs'] = line_id.strip()
            new_row['Line_Names_En'] = line_name_en.strip()
            new_row['Line_Names_Jp'] = line_name_jp.strip()
            cleaned_rows.append(new_row)
    
    # Create a cleaned DataFrame
    cleaned_data = pd.DataFrame(cleaned_rows)
    
    # Save the cleaned data
    print("Saving cleaned station data... (クリーンデータを保存中...)")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cleaned_data.to_csv(output_path, index=False)
    print("Station data cleaning completed. (駅データのクリーニングが完了しました。)")

def main():
    input_path = './data/processed/station_data_with_lines.csv'
    output_path = './data/cleaned/stations_cleaned.csv'
    clean_station_data(input_path, output_path)

if __name__ == "__main__":
    main()