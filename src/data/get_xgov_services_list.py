#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The get_xgov_services_list.py module fetches the HTML content of
public services listed on https://govuk-digital-services.herokuapp.com/
using a GET request and extracts the service name, priority status, 
organisation, topic, and URL.
"""

import requests   # 3rd party packages
import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from data import config    # local imports


__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


extra_urls = config.EXTRA_URLS


def main():

    # Specify base url for X-GOVUK Services list
    base_url="https://govuk-digital-services.herokuapp.com/"

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(base_url).text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "lxml")

    # Extract service URLS
    result = []
    for link in soup.find_all("a"):
        if "projects/" in link.get("href"):
            result.append(link.get("href"))

    # Remove duplicates and preserve order
    seen = set()
    relative_urls = []
    for item in result:
        if item not in seen:
            seen.add(item)
            relative_urls.append(item)

    # Create DataFrame for appending data
    data = {
        'abbr': [],
        'organisation':[],
        'body': [],
        'service_name': [],
        'service_type': [],
        'govuk_start_page_url': [],
        'topic': [],
        'priority': [],
        'retired': [], 
        'customer_type': [],
        'verb': []}
    df = pd.DataFrame(data)

    # Collect data
    for item in relative_urls:

        # Make a GET request to fetch HTML content for each service page
        url = base_url + item[1:]
        html_content = requests.get(url).text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "lxml")

        # Extract service name, priority status, organisation, topic, and URL
        for link in soup.find_all("a"):      
            retired = False 
            service_name = soup.title.text.strip().split(" – ")[0]
            priority = ('prioritised' in soup.text)
            if 'organisation/' in link.get("href"):
                organisation = link.text
            if '/#' in link.get("href") and 'Skip' not in link.text:
                topic = link.text
            if link.text == 'Start page on GOV.UK':
                govuk_start_page_url = link.get("href")   
                if 'https' not in govuk_start_page_url:
                    govuk_start_page_url = None
            if 'govuk-button' in str(link):
                govuk_start_page_url = link.get("href")
            if 'Start pages' in soup.text:
                govuk_start_page_url = soup.text.split(
                    'Start pages:\n\n')[1].split('\n')[0]
            if 'retired' in soup.text:
                retired = True
            if service_name in extra_urls.keys():
                govuk_start_page_url = extra_urls[service_name]
            abbr = np.nan
            body = np.nan
            service_type = np.nan
            customer_type = np.nan
            verb = service_name.split(' ', 1)[0]

        # Exclude services that do not meet eligibility (government internal = 21)
        if topic not in [
            'Government Internal'
        ]:

            # Append to DataFrame
            df.loc[len(df)] = [
                abbr,
                organisation,
                body,
                service_name, 
                service_type,
                govuk_start_page_url, 
                topic, 
                priority, 
                retired,
                customer_type,
                verb
            ]

    # Exculde duplicate links
    df.loc[df['govuk_start_page_url'].duplicated(), 'govuk_start_page_url'] = np.nan

    # Exculde non-existent services
    df = df[df['govuk_start_page_url'].notna()]

    YYYYMM = get_current_month_and_year()

    df.to_excel("../data/raw/{}-xgov-govuk-services-list.xlsx".format(YYYYMM))  
    

def get_current_month_and_year():
    # Get the current date
    current_date = datetime.datetime.now()
    
    # Format the current date as 'YYYYMM'
    formatted_date = current_date.strftime('%Y%m')
    
    return formatted_date
    

if __name__ == "__main__":
    main()