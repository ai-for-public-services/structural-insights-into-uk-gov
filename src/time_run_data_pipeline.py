#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
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


def measure_execution_time(function):
    start_time = time.time()
    function()
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


def main():
    # Define a list of functions to call in sequence
    tasks = [
        ("Download list of active services", get_xgov_services_list.main),
        ("Process primary data relating to service tasks", process_service_task_data.main),
        ("Process transactional data", process_transactional_data.main),
        ("Process government website data", process_govuk_domain_names.main),
        ("Process government websites", process_government_website_merged.main),
        ("Process unique clicks 2022", process_unique_clicks_data.main),
        ("Merge GOVUK domain names", merge_govuk_domain_files.main),
        ("Merge unique clicks with services data", merge_unique_clicks_services_list.main),
        ("Extract organisations from GOVUK forms data", extract_form_URL_organisations.main),
    ]

    # Directory to save the PDF report
    report_dir = "../reports"

    # Ensure the reports directory exists, create it if not
    os.makedirs(report_dir, exist_ok=True)

    # Create a PDF report with the specified path
    report_path = os.path.join(report_dir, "data_pipeline_execution_report.pdf")
    doc = SimpleDocTemplate(report_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Header
    story.append(Paragraph("Execution Time Report", styles["Title"]))

    # Measure execution time for each function and add to the report
    for task_name, task_function in tasks:
        execution_time = measure_execution_time(task_function)
        report_line = f"<b>{task_name}:</b> {execution_time:.2f} seconds"
        story.append(Paragraph(report_line, styles["Normal"]))

    # Build the PDF
    doc.build(story)


if __name__ == "__main__":
    main()

