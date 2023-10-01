#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The process_service_task_data.py module loads, preprocesses and
saves to file the two main DataFrames used for the analysis of service
tasks.
"""

import ast
import pickle
import pandas as pd

from data import search_api_funcs   # local imports


__author__ = "Vincent Straub"
__email__ = "vstraub@turing.ac.uk"
__status__ = "Testing"


# Task content list
TASK_CONTENT_LIST = [
    'physical strength', 'physical dexterity', 'physical navigation',
    'information processing', 'problem solving', 'serving/attending',
    'teaching/training/coaching', 'selling/influencing',
    'managing/coordinating', 'caring'
]


def main():
    descriptive_df = format_dataset_into_df(df='descriptive_df')
    analysis_df = format_dataset_into_df(df='analysis_df')

    save_processed_dataset(descriptive_df)
    save_processed_dataset(
        analysis_df,
        path='../data/processed/dataframes/analysis-df-w-api-data.pkl'
    )


def save_processed_dataset(df, 
                           path='../data/processed/dataframes/descriptive-df-w-api-data.pkl'
                          ):
    """
    Pickles the DataFrame to a file to avoid calling the API again.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be saved.
        path (str): The path to save the DataFrame.
    """
    with open(path, 'wb') as file:
        pickle.dump(df, file)


def format_dataset_into_df(df='descriptive_df'):
    """
    Formats and processes the dataset into a DataFrame.

    Parameters:
        df (str): The type of DataFrame to return, either 'descriptive_df' or 'analysis_df'.

    Returns:
        pandas.DataFrame: The formatted DataFrame.
    """
    # Load datasets
    transactional_service_tasks_df = load_dataset('transactional_service_tasks_df')
    all_services_df = load_dataset('all_services_df')
    task_statement_df = load_dataset('task_statement_df')
    rubric_df = load_dataset('rubric_df')

    # Preprocess data
    processed_df = preprocess_transaction_data(transactional_service_tasks_df)

    # Standardize service names
    processed_df['service'] = processed_df['service'].str.lower().str.strip()

    # Remove duplicates
    processed_df = processed_df.drop_duplicates(
        subset=['service'], keep='last').reset_index().drop(columns=['index']
                                                           )
    processed_df = processed_df.drop(columns=['Unnamed: 0'])

    # Convert service_tasks column to list
    processed_df['service_tasks'] = processed_df['service_tasks'].apply(ast.literal_eval)

    all_services_df['service'] = all_services_df['service'].str.lower()

    # Update task group and category columns
    analysis_df = update_task_group_cols(processed_df, task_statement_df)
    analysis_df = update_task_category_cols(analysis_df)

    # Combine DataFrames and remove duplicates
    descriptive_df = pd.concat(
        [all_services_df, analysis_df]
    ).drop_duplicates(
        subset=['service'], keep='last'
    ).reset_index().drop(columns=['index'])

    # Add Search API data
    descriptive_w_api_df = add_search_api_data(descriptive_df, analysis_df)
    analysis_w_api_df = add_search_api_data(descriptive_df, analysis_df, df='analysis_df')

    # Add rubric data
    analysis_w_api_df = pd.merge(analysis_w_api_df, rubric_df, on='service', how='left')
    descriptive_w_api_df = pd.merge(descriptive_w_api_df, rubric_df, on='service', how='left')
    
    # Remove unnecssary columns
    descriptive_w_api_df = descriptive_w_api_df.drop(columns=['Unnamed: 0'])

    if df == 'analysis_df':
        return analysis_w_api_df

    if df == 'descriptive_df':
        return descriptive_w_api_df


def load_dataset(dataset='task_database_df'):
    """
    Loads the specified dataset.

    Parameters:
        dataset (str): The dataset to load.

    Returns:
        pandas.DataFrame: The loaded DataFrame.
    """
    data_dir = '../data/'

    datasets = {
        'task_database_df': 'cddo-data/ISCO-08-task-database-processed-task-groups.xlsx',
        'task_statement_df': 'processed/2023-task-groups-mapping.xlsx',
        'transactional_service_tasks_df': 'raw/202308-task-to-service-assignment.xlsx',
        'all_services_df': 'raw/202308-services-list.xlsx',
        'rubric_df': 'processed/2023-rubric-grading-services-processed.xlsx',
    }

    df = pd.read_excel(data_dir + datasets[dataset], header=0)

    if dataset == 'transactional_service_tasks_df':
        df = df.loc[(df['excluded'] != True) & (df['retired'] == False)]

    return df


def preprocess_transaction_data(dataset, content=TASK_CONTENT_LIST):
    """
    Preprocesses the dataset by performing multiple transformations.

    Parameters:
        dataset (pandas.DataFrame): The input DataFrame.
        content (list): List of task content categories.

    Returns:
        pandas.DataFrame: The preprocessed DataFrame.
    """
    df = process_task_content(dataset, 'task_content_category')
    df = check_list_items(df, 'task_content_category', content)
    df = split_second_item(df, 'task_content_category')

    return df


def add_search_api_data(descriptive_df, analysis_df, df='descriptive_df'):
    """
    Adds description and popularity data to the DataFrames using the Search API.

    Parameters:
        descriptive_df (pandas.DataFrame): The descriptive DataFrame.
        analysis_df (pandas.DataFrame): The analysis DataFrame.
        df (str): The type of DataFrame to update, either 'descriptive_df' or 'analysis_df'.

    Returns:
        pandas.DataFrame: The updated DataFrame.
    """
    # Get description and popularity data for each service using Search API
    descriptive_df['service_data'] = descriptive_df['service'].apply(
        search_api_funcs.get_search_api_data
    )
    descriptive_df[['description', 'popularity']] = descriptive_df['service_data'].apply(
        pd.Series
    )
    descriptive_df.drop(columns=['service_data'], inplace=True)

    # Add popularity rank
    descriptive_df_w_api = search_api_funcs.rank_services_by_popularity(
        descriptive_df
    )

    if df == 'descriptive_df':
        return descriptive_df_w_api

    if df == 'analysis_df':
        # Add popularity to analysis_df
        analysis_df_w_api = analysis_df.merge(
            descriptive_df_w_api[['service', 'popularity']], on='service', how='left'
        )
        return analysis_df_w_api


def process_task_content(dataframe, column_name):
    """
    Processes the task content column by splitting and extracting relevant data.

    Parameters:
        dataframe (pandas.DataFrame): The input DataFrame.
        column_name (str): The column name to process.

    Returns:
        pandas.DataFrame: The DataFrame with processed column.
    """
    dataframe[column_name] = dataframe[column_name].str.split(',').apply(
        lambda x: [string.split(':')[0] for string in x]
    )
    return dataframe


def check_list_items(dataframe, column_name, items_list):
    """
    Checks and updates columns based on the presence of specific items in lists.

    Parameters:
        dataframe (pandas.DataFrame): The input DataFrame.
        column_name (str): The column name to check.
        items_list (list): List of items to check for.

    Returns:
        pandas.DataFrame: The DataFrame with updated columns.
    """
    for item in items_list:
        new_column_name = item.replace(" ", "_")
        dataframe[new_column_name] = dataframe[column_name].apply(
            lambda x: 1 if item in x else 0
        )
    return dataframe


def split_second_item(df, column_name):
    """
    Splits the second item in a list of strings.

    Parameters:
        df (pandas.DataFrame): The input DataFrame.
        column_name (str): The column name to process.

    Returns:
        pandas.DataFrame: The DataFrame with the updated column.
    """
    def process_list(lst):
        if isinstance(lst, list) and all(isinstance(item, str) for item in lst):
            new_list = [item.split("'")[1] for item in lst]
            return new_list
        return lst

    df[column_name] = df[column_name].apply(process_list)
    return df


def update_task_group_cols(df, task_statement_df):
    """
    Update the numeric columns of a DataFrame based on matching task statements.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the 'service tasks' column 
        and numeric columns RM, RC, NRI, NRM, and NRA.
        task_statement_df (pandas.DataFrame): The DataFrame containing 'task_statement' 
        and 'task_group' columns.

    Returns:
        pandas.DataFrame: The input DataFrame 'df' with the numeric columns updated 
        based on matching task statements.
    """
    for index, row in df.iterrows():
        service_tasks = row['service_tasks']
        for task in service_tasks:
            matching_row = task_statement_df[task_statement_df['task_statement'] == task]
            if not matching_row.empty:
                task_group = matching_row['task_group'].iloc[0]
                df.at[index, task_group] += 1
    return df


def update_task_category_cols(df):
    """
    Update numeric columns based on matching task content categories.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing 'task_content_category' 
        and numeric columns.

    Returns:
        pandas.DataFrame: The updated DataFrame with modified numeric columns.
    """
    categories = ['physical strength', 'physical dexterity', 'physical navigation',
                  'information processing', 'problem solving', 'serving/attending',
                  'teaching/training/coaching', 'selling/influencing',
                  'managing/coordinating', 'caring']

    for index, row in df.iterrows():
        for task in row['task_content_category']:
            if task in categories:
                if ' ' in task:
                    task_column_name = task.replace(' ', '_')
                    df.at[index, task_column_name] += 1
                else:
                    df.at[index, task] += 1
    return df


if __name__ == "__main__":
    main()
