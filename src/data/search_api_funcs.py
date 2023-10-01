#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The get_search_api_data.py module contains functions for fetching
values for the fields 'description' and 'popularity' from the GOVUK
Search API: https://docs.publishing.service.gov.uk/repos/search-api.html
"""

import requests   # 3rd party packages
import pandas as pd


__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"



def rank_services_by_popularity(df, column='popularity'):
    df = df.sort_values(by=column, ascending=False).reset_index()
    df['popularity_rank'] = df.index + 1
    df.drop(columns=['index'], inplace=True)

    return df 
    
    
def get_search_api_data(service_name):
    api_url = "https://www.gov.uk/api/search.json"
    params = {
        "q": service_name,
        "fields": "content_store_document_type, description, popularity",
    }

    # Set the rate limit for requests (below 10 requests per second)
    rate_limit = 0.1  # 0.1 seconds per request
    
    try:
        response = requests.get(api_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                first_result = data["results"][0]
                description = first_result.get("description", "")
                popularity = first_result.get("popularity", 0)
                
                return {
                    'description': description,
                    'popularity': popularity,
                }
                
                # Sleep to comply with the rate limit
                time.sleep(rate_limit)
                
            else:
                return {
                    'description': '',
                    'popularity': 0,
                }

        else:
            return {
                'description': '',
                'popularity': 0,
            }
    except requests.exceptions.RequestException as e:
        print("An error occurred during the API request:", str(e))
        return {
            'description': '',
            'popularity': 0,
        }
