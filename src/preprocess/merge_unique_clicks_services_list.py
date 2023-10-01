#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The merge_unique_clicks_service_list.py module maps GOVUK unique clicks data from the
file 202110-202209-govuk-unique-visitors-processed to the file 202308-services-list.
"""

import pandas as pd

__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def main():    
    # Load services_df from '202308-services-list.xlsx'
    services_path = '../data/raw/202308-services-list.xlsx'
    services_df = pd.read_excel(services_path)
    
    # Load clicks_df from '202110-202209-govuk-unique-visitors-processed.xlsx'
    clicks_path = '../data/processed/202110-202209-govuk-unique-visitors-processed.xlsx'
    clicks_df = pd.read_excel(clicks_path)
    
    # Create a dictionary to store the sum of 'Unique clicks' for each 'Link clicked'
    clicks_sum_dict = clicks_df.groupby('Link clicked')['Unique clicks'].sum().to_dict()
    
    # Function to update 'unique_clicks_2021' in services_df
    def update_unique_clicks(row):
        link_clicked = row['govuk_start_page_url']
        if link_clicked in clicks_sum_dict:
            return clicks_sum_dict[link_clicked]
        else:
            return 0
    
    # Apply the update_unique_clicks function to calculate 'unique_clicks_2021'
    services_df['unique_clicks_2021'] = services_df.apply(update_unique_clicks, axis=1)
    
    # Save services_df to Excel as '202308-services-list-processed.xlsx'
    output_path = '../data/processed/202308-services-list-processed.xlsx'
    services_df.to_excel(output_path, index=False)
    

if __name__ == "__main__":
    main()
