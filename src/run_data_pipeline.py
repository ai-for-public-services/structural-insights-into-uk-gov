#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The run_data_pipeline.py module runs all scripts in the directories
/data and /preprocess that relate to collecting data through web-scraping
or API and preprocessing any files stored in the data directory raw/ and
saving them to /processed.
"""

from data import (
    get_xgov_services_list,
)

from preprocess import (
    process_service_task_data,
    process_transactional_data,
    process_govuk_domain_names,
    merge_govuk_domain_files,
    process_government_website_merged,
    process_unique_clicks_data,
    merge_unique_clicks_services_list,
    extract_form_URL_organisations,
)


__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def main():
    # Define a list of functions to call in sequence
    tasks = [
        get_xgov_services_list.main,                # Download list of active services
        process_service_task_data.main,             # Process primary data relating to service tasks
        process_transactional_data.main,            # Process transactional data
        process_govuk_domain_names.main,            # Process government website data
        process_government_website_merged.main,     # Process government websites
        process_unique_clicks_data.main,            # Process unique clicks 2022
        merge_govuk_domain_files.main,              # Merge GOVUK domain names
        merge_unique_clicks_services_list.main,     # Merge unique clicks with services data
        extract_form_URL_organisations.main,        # Extract organisations from GOVUK forms data
    ]

    # Execute each task
    for task in tasks:
        task()


if __name__ == "__main__":
    main()
