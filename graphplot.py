import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import os


# Clean financial numbers function
def clean_financial_numbers(val):
    if pd.isna(val):
        return np.nan
    val = str(val).strip()
    if val.lower() == 'n/a' or val == '':
        return np.nan
    val = val.replace('%', '')
    if val.startswith('(') and val.endswith(')'):
        val = '-' + val[1:-1]
    try:
        return float(val)
    except ValueError:
        return val

def createGraph():
    df = pd.read_csv("./outputs/segment_table/clean_final.csv")
    # Clean columns
    cols_to_clean = ['2021 $m', '2020 AER $m', '2020 CER $m', '2021 vs 2020 AER %', '2021 vs 2020 CER %']
    for col in cols_to_clean:
        df[col] = df[col].apply(clean_financial_numbers)

    # Extract Continuing Operations segments
    segments_df = df.iloc[2:9].copy() 
    segments_df.set_index('Category', inplace=True)

    # Plot 1: Segment Profit Comparison (2021 vs 2020 AER)
    plt.figure(figsize=(10, 6))
    width = 0.35
    x = np.arange(len(segments_df.index))

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, segments_df['2020 AER $m'], width, label='2020 (AER) $m', color='lightsteelblue')
    rects2 = ax.bar(x + width/2, segments_df['2021 $m'], width, label='2021 $m', color='royalblue')

    ax.set_ylabel('Profit ($m)')
    ax.set_title('Segment Profit Comparison: 2021 vs 2020 (AER)')
    ax.set_xticks(x)
    ax.set_xticklabels(segments_df.index, rotation=45, ha="right")
    ax.legend()

    plt.tight_layout()
    plt.savefig('./outputs/segment_table/segment_profit_comparison.png')
    plt.close('all')

    # Plot 2: YoY Growth Percentage
    plt.figure(figsize=(10, 6))
    colors = ['crimson' if val < 0 else 'mediumseagreen' for val in segments_df['2021 vs 2020 AER %']]
    bars = plt.bar(segments_df.index, segments_df['2021 vs 2020 AER %'], color=colors)

    plt.axhline(0, color='black', linewidth=1)
    plt.ylabel('Growth (%)')
    plt.title('Year-over-Year Profit Growth by Segment (AER %)')
    plt.xticks(rotation=45, ha="right")

    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (2 if yval > 0 else -4), f'{int(yval)}%', ha='center', va='bottom' if yval > 0 else 'top', fontsize=10)

    plt.tight_layout()
    plt.savefig('./outputs/segment_table/segment_growth_yoy.png')
    plt.close('all')

    print("Visualizations created successfully.")


def createGraph_consolidated():
    output_dir = "./outputs/consolidated_table/"
    os.makedirs(output_dir, exist_ok=True)

    # Load the cleaned data
    data_path = f"{output_dir}cleaned_consolidated_table.csv"
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Could not find {data_path}")
        exit()

    # 1. Select key high-level metrics for the visualization
    key_metrics = [
        "Gross premiums earned",
        "Total revenue, net of reinsurance",
        "Total charges net of reinsurance",
        "Profit after tax from continuing operations",
        "(Loss) profit for the year"
    ]

    # Filter the data and drop duplicates
    chart_df = df[df['Item'].isin(key_metrics)].drop_duplicates(subset=['Item']).copy()

    # Sort the values for a cleaner, staggered look on the bar chart
    chart_df = chart_df.sort_values(by='2021', ascending=True)

    # 2. Extract values for the pure matplotlib plotting
    labels = chart_df['Item'].tolist()
    vals_2020 = chart_df['2020'].tolist()
    vals_2021 = chart_df['2021'].tolist()

    # 3. Setup bar positions and width
    y = np.arange(len(labels))
    height = 0.35  # Thickness of the bars

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the grouped horizontal bars (one slightly above the label tick, one slightly below)
    rects1 = ax.barh(y + height/2, vals_2020, height, label='2020', color='#87CEFA')
    rects2 = ax.barh(y - height/2, vals_2021, height, label='2021', color='#4682B4')

    # 4. Add labels, title, and customize axes
    ax.set_xlabel('Amount ($m)', fontsize=12, fontweight='bold')
    ax.set_title('Key Financial Metrics: 2020 vs 2021 ($ Millions)', fontsize=14, fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=11)
    ax.legend()

    # Automatically attach text labels to the ends of the bars
    ax.bar_label(rects1, padding=3, fmt='%g')
    ax.bar_label(rects2, padding=3, fmt='%g')

    # 5. Finalize layout and save
    plt.tight_layout() # Ensures labels don't get cut off

    image_filename = f"{output_dir}financial_metrics_2020_vs_2021.png"
    plt.savefig(image_filename, dpi=300)

    print(f"Success! The chart has been saved as a high-resolution PNG at:\n{image_filename}")

    # Clear the plot from memory
    plt.clf()