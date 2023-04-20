#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The merge_govuk_domain_files.py module combines all CSV files
containing govuk domain names into a single CSV file.
"""

import os
import glob
import pandas as pd


__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def main():

    # find all govuk-domain-names.csv files in the folder
    # use glob pattern matching -> extension = 'csv'
    # save result in list -> all_filenames
    extension = 'csv'
    all_filenames = [i for i in glob.glob('**/*govuk-domain-names.{}'.format(extension))]


    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    # export to csv
    combined_csv.to_csv("201210-202303-govuk-domain-names.csv", index=False, encoding='utf-8-sig')
    

if __name__ == "__main__":
    main()