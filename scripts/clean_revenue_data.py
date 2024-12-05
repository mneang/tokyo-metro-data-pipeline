import pandas as pd

def create_lines_table(stations_data):
    """
    Create a Lines table from the Stations data.
    (駅データから路線テーブルを作成する)
    """
    # Extract unique Line_IDs and Line Names
    lines_data = stations_data[['Line_IDs', 'Line_Name_En', 'Line_Name_Jp']].drop_duplicates()

    # Handle multiple Line_IDs in a single row
    expanded_lines = []
    for _, row in lines_data.iterrows():
        line_ids = row['Line_IDs'].split(",")  # Split Line_IDs by comma
        line_names_en = row['Line_Name_En'].split(",")  # Split English names
        line_names_jp = row['Line_Name_Jp'].split(",")  # Split Japanese names

        # Ensure all lists have the same length
        if len(line_ids) == len(line_names_en) == len(line_names_jp):
            for line_id, name_en, name_jp in zip(line_ids, line_names_en, line_names_jp):
                expanded_lines.append({
                    'Line_ID': line_id.strip(),
                    'Line_Name_En': name_en.strip(),
                    'Line_Name_Jp': name_jp.strip()
                })
        else:
            print(f"Warning: Mismatched line data for {row['Line_IDs']}")

    # Convert expanded lines to a DataFrame
    lines_data = pd.DataFrame(expanded_lines)

    # Ensure no duplicate Line_IDs
    lines_data = lines_data.drop_duplicates(subset=['Line_ID'])

    return lines_data


def main():
    # Load the cleaned stations data
    stations_cleaned_path = './data/cleaned/stations_cleaned.csv'
    stations_data = pd.read_csv(stations_cleaned_path)

    # Create the Lines table
    lines_data = create_lines_table(stations_data)

    # Save the cleaned lines data
    output_lines_path = './data/cleaned/lines_cleaned.csv'
    lines_data.to_csv(output_lines_path, index=False)
    print("Lines data has been successfully cleaned and saved. (路線データが正常にクリーニングされ保存されました。)")

if __name__ == "__main__":
    main()