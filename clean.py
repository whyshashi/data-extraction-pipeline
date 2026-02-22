import csv
import re
import pandas as pd
import io


def clean_csv():
    
    input_file = "./outputs/segment_table/tablua_segment_results.csv"
    output_file = "./outputs/segment_table/cleaned_segment_results.csv"

    # The clean headers in final CSV
    headers = [
        "Category", "Note", "2021 $m", 
        "2020 AER $m", "2020 CER $m", 
        "2021 vs 2020 AER %", "2021 vs 2020 CER %"
    ]

    def clean_number(val):
        """Removes thousands separators (commas) from numbers."""
        return val.replace(',', '')

    def clean_category(val):
        """Removes the embedded 'note (i)' text from the category names."""
        return re.sub(r'\s*note \([ivx]+\)', '', val).strip()

    cleaned_data = [headers]

    print("Cleaning data...")

    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        
        # Skip the first 5 rows (the messy headers from Tabula)
        for _ in range(5):
            next(reader, None)
            
        for row in reader:
            # Skip completely empty rows
            if not any(row):
                continue
                
            # Pad the row with empty strings in case Tabula truncated empty trailing columns
            row += [''] * (6 - len(row))
            
            category = clean_category(row[0])
            note = row[1].strip()
            val_2021 = clean_number(row[2].strip())
            
            # Split the combined 2020 AER and CER values (Column index 3)
            val_2020_combined = row[3].strip()
            val_2020_aer, val_2020_cer = "", ""
            if val_2020_combined:
                parts = val_2020_combined.split()
                val_2020_aer = clean_number(parts[0])
                if len(parts) > 1:
                    val_2020_cer = clean_number(parts[1])
                    
            # Split the combined 2021 vs 2020 percentage values (Column index 5)
            # Note: Index 4 is usually the empty comma space in the raw data
            val_pct_combined = row[5].strip()
            val_pct_aer, val_pct_cer = "", ""
            if val_pct_combined:
                parts = val_pct_combined.split()
                val_pct_aer = parts[0]
                if len(parts) > 1:
                    val_pct_cer = parts[1]

            cleaned_data.append([
                category, note, val_2021, 
                val_2020_aer, val_2020_cer, 
                val_pct_aer, val_pct_cer
            ])


    # Write the cleaned data to a new CSV
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_data)

    print(f"Data successfully cleaned and saved to {output_file}!")


def clean_consolidated_csv():
    input_file = "./outputs/consolidated_table/consolidated_table.csv"
    output_file = "./outputs/consolidated_table/cleaned_consolidated_table.csv"

    # Helper function to clean financial strings
    def clean_con_value(val):
        if pd.isna(val) or val == "" or str(val).strip() == '""':
            return None
        s = str(val).strip().replace('"', '')
        if not s or s == '-':
            return 0.0
        
        # 1. Remove currency symbols and commas FIRST
        s = s.replace(',', '').replace('$', '').replace('¢', '').strip()
        
        # 2. THEN handle negative numbers in parentheses: (100) -> -100
        is_negative = False
        if s.startswith('(') and s.endswith(')'):
            is_negative = True
            s = s[1:-1]
            
        try:
            num = float(s)
            return -num if is_negative else num
        except ValueError:
            return None

    # 1. Load data from the actual file path
    # We use names if the raw CSV doesn't have reliable headers
    try:
        df = pd.read_csv(input_file, names=['Item', 'Note', '2021', '2020'], header=None)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        return

    # 2. Clean Labels (Remove footnote markers like 'note (i)')
    df['Item'] = df['Item'].str.replace(r'\s*note\s*\([ivx]+\)', '', regex=True, flags=re.IGNORECASE).str.strip()

    # 3. Clean numeric columns
    df['2021_Clean'] = df['2021'].apply(clean_con_value)
    df['2020_Clean'] = df['2020'].apply(clean_con_value)

    # 4. Filter out header-like rows that appear mid-table
    # Added 'Note' and the actual column headers to the filter
    df = df[~df['Item'].isin(['', 'Note', 'Continuing operations:', 'Item'])]

    # 5. Add a 'Unit' column based on section
    df['Unit'] = '$m'
    eps_start_mask = df['Item'].str.contains('Earnings per share', na=False, case=False)
    if eps_start_mask.any():
        eps_start_idx = df[eps_start_mask].index[0]
        df.loc[eps_start_idx:, 'Unit'] = 'cents'

    # Final output cleanup
    df_final = df[['Item', 'Note', '2021_Clean', '2020_Clean', 'Unit']].copy()
    df_final.columns = ['Item', 'Note', '2021', '2020', 'Unit']
    
    # Drop rows where everything is null (empty lines from PDF)
    df_final = df_final.dropna(subset=['2021', '2020'], how='all')

    # Save to CSV
    df_final.to_csv(output_file, index=False)
    print(f"Cleaned data saved to: {output_file}")
    print(df_final.head(15))