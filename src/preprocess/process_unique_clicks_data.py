#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The process_unique_clicks_data.py module loads, preprocesses and
saves the 202110-202209-govuk-unique-visitors.xlsx. 
"""

import pandas as pd

__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def main():
    # Load the Excel file into a DataFrame
    input_file = '../data/raw/202110-202209-govuk-unique-visitors.xlsx'
    df = pd.read_excel(input_file)

    # Combine rows with the same 'Page' and sum 'Unique clicks'
    df_processed = df.groupby('Page').agg({
        'Link clicked': 'first',
        'First organisation': 'first',
        'Page title': 'first',
        'Unique clicks': 'sum'
    }).reset_index()

    # Save the processed DataFrame to a new Excel file
    output_file = '../data/processed/202110-202209-govuk-unique-visitors-processed.xlsx'
    df_processed.to_excel(output_file, index=False)
    

if __name__ == "__main__":
    main()
