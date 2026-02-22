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
