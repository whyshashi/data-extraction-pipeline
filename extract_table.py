"""
Module: extract_table.py
Description:
    Extracts tabular data from PDF documents and converts them to CSV format.
    Uses the tabula library to identify and extract tables from specified PDF pages.

Main Functions:
    extract_table_from_pdf(pdf_path, output_csv, page_num):
        Extracts a table from a specified page in a PDF file and saves it as a CSV.
        
        Parameters:
            pdf_path (str): Path to the input PDF file. 
                           Default: "./docs/prudential-plc-ar-2021.pdf"
            output_csv (str): Path to save the extracted CSV file.
                             Default: "./outputs/segment_table/tablua_segment_results.csv"
            page_num (int): The PDF page number to extract the table from.
                           Default: 254

Dependencies:
    - tabula-py: Used for PDF table extraction and conversion to CSV
"""

import tabula

def extract_table_from_pdf(pdf_path="./docs/prudential-plc-ar-2021.pdf", output_csv="./outputs/segment_table/tablua_segment_results.csv",page_num=254):
    # extract table from pdf

    print("Extracting table...")

    tabula.convert_into(
        input_path=pdf_path,
        output_path=output_csv,
        output_format="csv",
        pages=page_num,
        stream=True
    )

    print(f"Extraction complete! Saved to {output_csv}")
