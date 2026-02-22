from extract_table import extract_table_from_pdf
from graphplot import createGraph, createGraph_consolidated
from clean_col import clean_dataframe
from clean import clean_csv,clean_consolidated_csv
from llmgenerated_insights import generate_insights_from_csv
import os

# source file
input_file = "./docs/prudential-plc-ar-2021.pdf"

# main execution function for segment table 
def segmentTable():
    """Main segment table pipeline execution function."""
    # Define your file paths
    os.makedirs(os.path.dirname("./outputs/segment_table/segment_table"), exist_ok=True)

    try:
        # extract the table from the PDF, clean it, create a graph, and generate insights
        extract_table_from_pdf()
        clean_csv()
        clean_dataframe()
        createGraph()
        generate_insights_from_csv("./outputs/segment_table/clean_final.csv","./outputs/segment_table/llm_insights.txt")
        
    except Exception as e:
        print(f"Error: {e} ")
        return

# main execution function for consolidated table
def consolidatedTable():
    """Main consolidated table pipeline execution function."""
    # Define your file paths
    os.makedirs(os.path.dirname("./outputs/consolidated_table/consolidated_table"), exist_ok=True)

    try:
        # extract the table from the PDF, clean it, create a graph, and generate insights
        extract_table_from_pdf(input_file, output_csv="./outputs/consolidated_table/consolidated_table.csv", page_num=239)
        clean_consolidated_csv()
        createGraph_consolidated()
        generate_insights_from_csv("./outputs/consolidated_table/cleaned_consolidated_table.csv","./outputs/consolidated_table/llm_insights.txt")
        
    except Exception as e:
        print(f"Error: {e} occurred while processing {input_file}")
        return








