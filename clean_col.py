import pandas as pd
import numpy as np

def clean_financial_numbers_deep(val):
    """Converts accounting formats '(123)' and '12%' to standard floats."""
    if pd.isna(val):
        return val
        
    val = str(val).strip()
    
    # Handle 'n/a' or empty strings
    if val.lower() == 'n/a' or val == '':
        return np.nan
        
    # Remove percentage signs
    val = val.replace('%', '')
    
    # Convert (123) to -123
    if val.startswith('(') and val.endswith(')'):
        val = '-' + val[1:-1]
        
    try:
        return float(val)
    except ValueError:
        # Return the original string if it can't be converted (like category names)
        return val

def clean_dataframe():
        df = pd.read_csv("./outputs/segment_table/cleaned_segment_results.csv")
        # Apply the cleaning function to the numerical columns
        cols_to_clean = [
            '2021 $m', '2020 AER $m', '2020 CER $m', 
            '2021 vs 2020 AER %', '2021 vs 2020 CER %'
        ]

        for col in cols_to_clean:
            df[col] = df[col].apply(clean_financial_numbers_deep)

        print(df.head(10))
        print("\nData Types:")
        print(df.dtypes)

        # Save the cleaned DataFrame to CSV
        df.to_csv("./outputs/segment_table/clean_final.csv", index=False)
        print("\nData successfully saved to ./outputs/segment_table/clean_final.csv")