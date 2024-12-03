import fitz  # PyMuPDF
import pandas as pd
import os

# Directory setup
PDF_DIR = "data/raw"  # Directory containing uploaded PDFs
CSV_OUTPUT = "data/processed/revenue_data.csv"

# Ensure directories exist
os.makedirs(os.path.dirname(CSV_OUTPUT), exist_ok=True)

def extract_revenue_data(pdf_dir):
    """
    Extract revenue data from all PDFs in the specified directory.
    Args:
        pdf_dir (str): Directory containing revenue PDFs.
    Returns:
        pd.DataFrame: Extracted revenue data.
    """
    data = []
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            doc = fitz.open(pdf_path)
            print(f"Processing {pdf_file}...")
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text = page.get_text("text")
                
                # Parse the text for relevant lines (adjust logic as needed)
                lines = text.split("\n")
                for line in lines:
                    if "月" in line and "定期" in line and "合計" not in line:
                        parts = line.split()
                        if len(parts) >= 4:  # Adjust if structure changes
                            try:
                                month = parts[0]
                                commuter_revenue = int(parts[1].replace(",", ""))
                                non_commuter_revenue = int(parts[2].replace(",", ""))
                                total_revenue = int(parts[3].replace(",", ""))
                                data.append({
                                    "Month": month,
                                    "Commuter Revenue": commuter_revenue,
                                    "Non-Commuter Revenue": non_commuter_revenue,
                                    "Total Revenue": total_revenue
                                })
                            except ValueError:
                                print(f"Skipping malformed line: {line}")
    
    return pd.DataFrame(data)

def main():
    print("Starting extraction of revenue data...")
    revenue_data = extract_revenue_data(PDF_DIR)
    if not revenue_data.empty:
        revenue_data.to_csv(CSV_OUTPUT, index=False)
        print(f"Data successfully saved to {CSV_OUTPUT}")
    else:
        print("No data extracted. Check PDF structure or directory content.")

if __name__ == "__main__":
    main()
