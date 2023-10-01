#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The extract_form_URL_organisations.py module accesses the webpage
for all forms and finds the respective host organisation, adds
this to the dataframe and saves it to file.
"""

import argparse
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Default input and output file paths
DEFAULT_INPUT_FILE = '../data/raw/202211-form-services-pageviews.xlsx'
DEFAULT_OUTPUT_FILE = '../data/processed/202211-form-services-pageviews-processed.xlsx'


def load_data(file_path):
    """
    Load data from an Excel file and preprocess it.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    data = pd.read_excel(file_path)
    data = data.iloc[1:]
    data.rename(columns={'Unnamed: 2': 'views', data.columns.unique()[0]: 'form'}, inplace=True)
    data['views'] = data['views'].astype(int)
    data.rename(columns={'form': 'URL'}, inplace=True)
    data.drop(columns=['Unnamed: 1'], inplace=True)
    data['URL'] = data['URL'].str.replace('^/print', '')  # Remove '/print'
    return data


def extract_organization_name(url):
    """
    Extract the organization name from a URL.

    Args:
        url (str): URL to access and extract organization information.

    Returns:
        str or None: Extracted organization name or None if not found.
    """
    full_url = 'https://www.gov.uk' + url
    response = requests.get(full_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        organization_tag = soup.find(name="meta", attrs={"name": "govuk:primary-publishing-organisation"})

        if organization_tag:
            organization_name = organization_tag.get('content')
            return organization_name

    return None


def main():
    # Load and preprocess data
    form_df = load_data(DEFAULT_INPUT_FILE)
    
    # Extract organization names
    form_df['organisation'] = form_df['URL'].apply(extract_organization_name)
    
    # Save the result to an Excel file
    form_df.to_excel(DEFAULT_OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()