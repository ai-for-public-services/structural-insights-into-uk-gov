#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The get_task_groups_count.py module creates task groups for each 
service.
"""

import pandas as pd

__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


def create_task_group_category(df):
    """
    Create the 'task_group_category' column in the DataFrame.
    
    Parameters:
        df (pandas.DataFrame): The DataFrame to be updated.
    """
    # Create the 'task_group_category' column filled with empty lists
    df['task_group_category'] = [[] for _ in range(len(df))]

    # Iterate over each row and columns,
    # adding only 'NRA', 'RM', 'NRM', 'RC', or 'NRI' to 'task_group_category'
    for index, row in df.iterrows():
        for col in ['NRA', 'RM', 'NRM', 'RC', 'NRI']:
            if row[col] != 0:
                row['task_group_category'].append(col)

    return df


def return_task_counts(df, column_name='service_tasks', num_top_items=10):
    # Calculate the length of each list in the 'service_tasks' column
    df['task_count'] = df[column_name].apply(len)
    
    # Create a DataFrame with 'service' and 'task_count' columns
    task_counts_df = df[['service', 'task_count']]
    
    # Sort the DataFrame by 'task_count' column in descending order
    task_counts_df = task_counts_df.sort_values(by='task_count', ascending=False)
    
    # Display the top items DataFrame
    df = task_counts_df.head(num_top_items)

    print(df)


if __name__ == "__main__":
    pass