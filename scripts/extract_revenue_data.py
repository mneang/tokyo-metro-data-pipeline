import pdfplumber
import pandas as pd
import os
import re

# Directories
PDF_DIR = "data/raw"  # PDFファイルが保存されているフォルダ
CSV_OUTPUT = "data/processed/revenue_data.csv"  # 出力されるCSVファイル

# Ensure output directory exists (出力フォルダを確認)
os.makedirs(os.path.dirname(CSV_OUTPUT), exist_ok=True)

def extract_fiscal_year(file_name):
    """
    Extract the fiscal year from the file name.
    ファイル名から会計年度を抽出します。
    Args:
        file_name (str): File name of the PDF (PDFファイル名)
    Returns:
        int: Starting fiscal year (会計年度の開始年)
    """
    match = re.search(r"\d{4}", file_name)
    return int(match.group(0)) - 1 if match else None  # Adjust to previous calendar year (e.g., 2021 -> 2020 fiscal start)

def calculate_fiscal_year_and_month(start_year, month_index):
    """
    Calculate the correct fiscal year and month based on fiscal rules.
    Args:
        start_year (int): Starting fiscal year (e.g., 2020 for FY 2021).
        month_index (int): Month index (1-based, e.g., 1 for January, 12 for December).
    Returns:
        tuple: Fiscal year and fiscal month or None if the month is outside the fiscal period.
    """
    if 4 <= month_index <= 12:  # April to December (same calendar year as start_year)
        fiscal_year = start_year + 1  # FY runs from April to March (next year is fiscal year label)
        fiscal_month = month_index - 3  # Adjust to Fiscal Month (April = 1)
    elif 1 <= month_index <= 3:  # January to March (previous calendar year for fiscal period)
        fiscal_year = start_year + 1
        fiscal_month = month_index + 9  # Adjust to Fiscal Month (January = 10)
    else:
        # Invalid month index
        return None, None

    return fiscal_year, fiscal_month

def extract_fiscal_year(file_name):
    """
    Extract the fiscal year from the file name.
    Args:
        file_name (str): File name of the PDF (e.g., "2021 revenue data.pdf").
    Returns:
        int: Starting calendar year of the fiscal period (e.g., 2020 for FY 2021).
    """
    match = re.search(r"\d{4}", file_name)
    if match:
        fiscal_year = int(match.group(0))  # Extract the fiscal year (e.g., "2021")
        return fiscal_year - 1  # Fiscal year label corresponds to year+1 (e.g., 2021 → start year 2020)
    return None

def parse_revenue_line(line, start_year):
    """
    Parse a line containing monthly revenue data.
    Args:
        line (str): Line of text to parse.
        start_year (int): Starting calendar year of the fiscal period (e.g., 2020 for FY 2021).
    Returns:
        dict: Parsed data or None if the line is not valid.
    """
    try:
        parts = line.split()
        if len(parts) < 6:
            return None  # Line does not contain enough parts

        # Extract the month and calculate fiscal year
        month_str = parts[0]  # e.g., "4月" or "April"
        match = re.search(r"\d+", month_str)  # Look for numeric part in the month string
        if not match:
            print(f"Skipping invalid month string: {month_str}")
            return None
        month_index = int(match.group())  # Extract the numeric part (e.g., "4" from "4月")

        fiscal_year, fiscal_month = calculate_fiscal_year_and_month(start_year, month_index)
        if fiscal_year is None or fiscal_month is None:
            print(f"Skipping out-of-range month: {month_str}")
            return None

        # Parse revenue and YoY data
        commuter_revenue = int(parts[1].replace(",", ""))
        commuter_yoy = float(parts[2].replace("%", "").replace("+", ""))
        non_commuter_revenue = int(parts[3].replace(",", ""))
        non_commuter_yoy = float(parts[4].replace("%", "").replace("+", ""))
        total_revenue = int(parts[5].replace(",", ""))
        total_yoy = float(parts[6].replace("%", "").replace("+", ""))

        return {
            "Fiscal Year": fiscal_year,
            "Fiscal Month": fiscal_month,  # Keep fiscal month (1-12 for Apr-Mar)
            "Commuter Revenue": commuter_revenue,
            "Commuter YoY (%)": commuter_yoy,
            "Non-Commuter Revenue": non_commuter_revenue,
            "Non-Commuter YoY (%)": non_commuter_yoy,
            "Total Revenue": total_revenue,
            "Total YoY (%)": total_yoy,
        }
    except ValueError as e:
        print(f"Skipping malformed line: {line} - {e}")
        return None

def extract_revenue_data_with_pdfplumber(pdf_dir):
    """
    Extract revenue data from PDFs using pdfplumber.
    pdfplumberを使用してPDFから収入データを抽出します。
    Args:
        pdf_dir (str): Directory containing PDF files (PDFファイルが保存されているフォルダ)
    Returns:
        pd.DataFrame: Extracted revenue data (抽出された収入データ)
    """
    data = []

    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            start_year = extract_fiscal_year(pdf_file)
            if start_year is None:
                print(f"Skipping {pdf_file} due to missing year. (年が見つからないためスキップします)")
                continue

            pdf_path = os.path.join(pdf_dir, pdf_file)
            print(f"Processing {pdf_file} (Starting Year: {start_year})... (処理中: {pdf_file} 開始年度: {start_year})")
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text is None:
                        print(f"No readable text found on page {page_num + 1} of {pdf_file}. (ページに読めるテキストがありません)")
                        continue

                    lines = text.split("\n")
                    for line in lines:
                        print(f"Processing line: {line} (行を処理中)")
                        if "月" in line or "Quarter" in line or "FY" in line:
                            parsed_data = parse_revenue_line(line, start_year)
                            if parsed_data:
                                data.append(parsed_data)

    return pd.DataFrame(data)

def main():
    """
    Main function to extract and save revenue data.
    収入データを抽出して保存するメイン関数。
    """
    print("Starting extraction of revenue data... (収入データの抽出を開始します...)")
    revenue_data = extract_revenue_data_with_pdfplumber(PDF_DIR)
    if not revenue_data.empty:
        revenue_data.to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
        print(f"Revenue data successfully saved to {CSV_OUTPUT}. (収入データが正常に保存されました: {CSV_OUTPUT})")
    else:
        print("No data extracted. Check PDF structure or parsing logic. (データが抽出されませんでした。PDFの構造または解析ロジックを確認してください。)")

if __name__ == "__main__":
    main()
