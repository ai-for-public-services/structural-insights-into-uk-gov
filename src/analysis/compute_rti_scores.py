#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The compute_rti_scores.py module computes the Routine-Task Intensity
score for each service based on the count for each service task
category.
"""

import pandas as pd

__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def transform_to_percentage(variable):
    """
    Transform a variable to a percentage.
    
    Parameters:
        variable (float): The variable to transform.

    Returns:
        float: The transformed percentage.
    """
    percentage = ((variable + 1) / 2) * 100
    return percentage


def add_rti_scores(df, compute_function):
    """
    Compute RTI scores for each row in the DataFrame using the given compute function.
    
    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        compute_function (function): The function to compute RTI scores for a row.
        
    Returns:
        pandas.DataFrame: The updated DataFrame with added RTI score columns.
    """
    # Apply the compute_function to each row and expand the result
    rti_scores = df.apply(lambda row: compute_function(row, df), axis=1, result_type='expand')

    # Rename the columns for better clarity
    rti_scores.columns = ['RTI_NRA', 'RTI_RM', 'RTI_NRM', 'RTI_RC', 'RTI_NRI', 'RTI']

    # Concatenate the computed scores with the original dataframe
    df = pd.concat([df, rti_scores], axis=1)
    
    return df


def compute_rti_scores(row, df, metric='RTI'):
    """
    Compute RTI scores for a given row.
    
    Parameters:
        row (pandas.Series): The row of data.
        df (pandas.DataFrame): The DataFrame containing the data.
        metric (str): The metric name.

    Returns:
        list: A list of RTI scores.
    """
    service = row['service']

    k = df.loc[df['service'] == service]
    n = float(k.task_count)
    
    RTI_NRA = float(k.NRA) / n
    RTI_RM = float(k.RM) / n
    RTI_NRM = float(k.NRM) / n
    RTI_RC = float(k.RC) / n
    RTI_NRI = float(k.NRI) / n

    RTI = RTI_RC + RTI_RM - RTI_NRA - RTI_NRI - RTI_NRM

    return [RTI_NRA, RTI_RM, RTI_NRM, RTI_RC, RTI_NRI, RTI]


def create_summary_table(dataframe):
    # Create the summary table
    summary_table = pd.DataFrame({
        'Share of routine tasks': ['0%', '<50%', '≥50%', '≥75%', '100%'],
        'Number of services': [0, 0, 0, 0, 0],
        '% of services': [0, 0, 0, 0, 0]
    })
    
    # Calculate the number of rows where RTI_perc falls into each category
    count_0 = len(dataframe[dataframe['RTI_perc'] == 0])
    count_less_than_50 = len(dataframe[dataframe['RTI_perc'] < 50])
    count_greater_than_or_equal_50 = len(dataframe[dataframe['RTI_perc'] >= 50])
    count_greater_than_or_equal_75 = len(dataframe[dataframe['RTI_perc'] >= 75])
    count_100 = len(dataframe[dataframe['RTI_perc'] == 100])

    # Declare column names
    col1_name = 'Share of routine tasks'
    col2_name = 'Number of services'
    
    # Fill in the 'Number of services' column
    summary_table.loc[summary_table[col1_name] == '0%', col2_name] = count_0
    summary_table.loc[summary_table[col1_name] == '<50%', col2_name] = count_less_than_50
    summary_table.loc[summary_table[col1_name] == '≥50%', col2_name] = count_greater_than_or_equal_50
    summary_table.loc[summary_table[col1_name] == '≥75%', col2_name] = count_greater_than_or_equal_75
    summary_table.loc[summary_table[col1_name] == '100%', col2_name] = count_100
    
    # Fill in the '% of services' column
    total_rows = len(dataframe)
    summary_table['% of services'] = [
        count_0 / total_rows * 100,
        count_less_than_50 / total_rows * 100,
        count_greater_than_or_equal_50 / total_rows * 100,
        count_greater_than_or_equal_75 / total_rows * 100,
        count_100 / total_rows * 100
    ]
    
    return summary_table
    

if __name__ == "__main__":
    pass