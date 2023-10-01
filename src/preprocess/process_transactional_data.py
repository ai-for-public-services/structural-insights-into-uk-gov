#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The process_transactional_data.py module filters the file
201204-201703-service-transactions by removing rows with 
missing values, renaming columns and replacing empty values.
"""

import os
import glob
import numpy as np
import pandas as pd


__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def main():
    # Load raw data
    transactions_df = pd.read_csv(
        ('../data/raw/201204-201703-service-transactions-raw.csv'), dtype='unicode'
    ) 
    # Rename  columns
    transactions_df.columns = [i.replace(
        '_vol', '') for i in transactions_df.columns
                              ]
    transactions_df.columns = [i.replace(
        '_', '') for i in transactions_df.columns
                              ]
    # Replace values
    transactions_df = transactions_df.apply(lambda x: x.str.replace(',', ''))
    transactions_df = transactions_df.apply(lambda x: x.str.replace('-', ''))
    transactions_df = transactions_df.rename(columns={'Servicename':'Service'})
    transactions_df = transactions_df.replace(r'^\s*$', np.nan, regex=True)
    # Drop empty rows
    transactions_df = transactions_df.dropna(how ='all')
    transactions_df = transactions_df.dropna(
        subset=transactions_df.iloc[:, 10:].columns, how ='all'
    )
    # Save to file
    transactions_df.to_csv(
        '../data/processed/201204-201703-service-transactions-processed.csv',
    encoding='utf-8', index=False
)   
    
    
if __name__ == "__main__":
    main()