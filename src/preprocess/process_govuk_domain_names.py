#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The process_govuk_domain_names.py module removes parish and 
local council .gov.uk domains from the file:
201210-202303-govuk-domain-names.csv
"""

import os
import glob
import pandas as pd


__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def main():
    # Load the file into a dataframe df_domains
    df_domains = pd.read_csv(
        '../data/raw/201210-202303-govuk-domain-names.csv'
    )
    
    # Load the file into a dataframe df_councils
    df_councils = pd.read_excel(
        '../data/processed/202206-uk-local-council-names.xlsx'
    )
    
    # Create a set called 'exclude' with initial entries: 'council', 'parish', 'councils', 'borough', 'district'
    exclude = {'council', 'parish', 'councils', 'borough', 'district'}
    
    # Add all values in the df_councils column 'Body' to the set 'exclude'
    exclude.update(df_councils['Body'].dropna())  # Use dropna to remove NaN values
    
    # Define a function to check if any value in a row contains excluded keywords
    def contains_excluded_keywords(row):
        return any(keyword in str(row) for keyword in exclude)
    
    # Create a boolean mask to filter rows based on excluded keywords
    mask = df_domains.applymap(
        lambda cell: any(keyword in str(cell) for keyword in exclude)
    ).any(axis=1)
    
    # Remove all rows from df_domains that contain any of the values in 'exclude' in any of the columns
    df_domains = df_domains[~mask]
    
    # Save df_domains to file 
    df_domains.to_csv(
        '../data/processed/201210-202303-govuk-domain-names-processed.csv', index=False
    )
    

if __name__ == "__main__":
    main()