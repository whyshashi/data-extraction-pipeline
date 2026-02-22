"""
LLM-Generated Insights Module

This module provides functionality to analyze financial data from CSV files using Google's 
Gemini API and generate meaningful business insights. It performs variance analysis, 
examines margin and profitability trends, and identifies exceptional items that impact 
financial results.

Key Features:
- Reads financial data from CSV files
- Analyzes year-over-year and period-over-period changes
- Generates data-driven business insights with specific metrics and percentages
- Integrates with Google Gemini LLM for intelligent analysis
- Outputs insights to text files for reporting and documentation

Dependencies:
- pandas: Data manipulation and CSV reading
- google.genai: Google Gemini API client (updated SDK)
- python-dotenv: Environment variable management

Usage:
    from llmgenerated_insights import generate_insights_from_csv
    insights = generate_insights_from_csv('data.csv', 'outputs/insights.txt')
"""

import pandas as pd
from google import genai  # Updated import for the new SDK
import os
from dotenv import load_dotenv

load_dotenv()

def generate_insights_from_csv(filepath,outputpath):
    """Reads a CSV and uses an LLM to generate business insights."""
    print(f"Reading data from {filepath} for LLM analysis...")
    
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise FileNotFoundError(f"Error: The file {filepath} was not found.")

    data_string = df.to_csv(index=False)
    
    # Construct the prompt
    prompt = f"""
    Act as an expert financial analyst. Please review the financial data provided below and generate 3 to 5 meaningful business insights. >
    Focus your analysis on:
    Variance Analysis: Identify the key drivers of growth or decline (the best and worst performing line items or segments based on Year-over-Year/period-over-period changes).
    Margin & Profitability Trends: Highlight overall top-line (revenue) and bottom-line (profit/loss) health, noting any margin compression or expansion.

    Exceptional Items: Point out any significant financial impacts from non-core operations (e.g., other income, unusual expenditures, taxes, or discontinued operations) that skew the overall results.
    Format & Tone:
    Keep the insights concise, professional, and entirely data-driven. Always reference specific figures or percentages from the dataset to back up your claims. Do not summarize the whole table; focus only on the most critical takeaways for a stakeholder.
    
    Here is the data:
    {data_string}
    """
    
    # Set up the Gemini API using the new SDK client
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Error: Please set your GOOGLE_API_KEY environment variable.")
        
    # Initialize the new client
    client = genai.Client(api_key=api_key)
    
    print("Generating insights... (this might take a few seconds)")
    
    # Use the new generate_content syntax and a current model
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )

    os.makedirs(os.path.dirname(outputpath), exist_ok=True)
    
    # Write the insights to the file using UTF-8 encoding
    with open(outputpath, "w", encoding="utf-8") as file:
        file.write(response.text)
    
    return response.text
