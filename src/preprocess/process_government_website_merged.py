#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The process_government_website_merged.py module preprocess the file
201202-201809-central-government-websites.csv by removing rows with 
missing values for key columns.
"""

import os
import glob
import pandas as pd


__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def main():

    # load merged CSV
    merger = pd.read_csv('../data/raw/201202-201809-central-government-websites-raw.csv')
    # remove rows with missing data for URL column
    merger_filtered_URL = merger.loc[(merger['URL'].apply(lambda x: isinstance(x, str)))]
    # remove rows with missing data for Year column
    merge_filtered_year = merger_filtered_URL.loc[merger_filtered_URL['Year'].notnull()]
    # save to file
    merge_filtered_year.to_csv(
        '../data/processed/201202-201809-central-government-websites.csv'
    )
    
    
if __name__ == "__main__":
    main()