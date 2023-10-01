#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The run_analysis.py module runs all scripts in the directories
/analysis that relate to computing key descriptive statistics for
key files stored in the data directory /processed.
"""

import pandas as pd
from analysis import (
    get_task_groups_count,
    compute_rti_scores
)


def load_analysis_dataframe(file_path):
    """Load the analysis DataFrame from a pickle file."""
    return pd.read_pickle(file_path)

def main():    
    input_file_path = '../data/processed/dataframes/analysis-df-w-api-data.pkl'
    output_file_path = '../data/processed/dataframes/analysis-df-w-api-data.pkl'
    
    # Load the analysis DataFrame
    analysis_df = load_analysis_dataframe(input_file_path)
    
    # Perform data analysis steps
    analysis_df = get_task_groups_count.create_task_group_category(analysis_df)
    print(get_task_groups_count.return_task_counts(analysis_df))
    
    analysis_df = compute_rti_scores.add_rti_scores(
        analysis_df, compute_rti_scores.compute_rti_scores
    )
    
    # Add a column 'RTI_perc' by applying the 'transform_to_percentage' function
    analysis_df['RTI_perc'] = analysis_df['RTI'].apply(
        compute_rti_scores.transform_to_percentage
    )
    
    # Print the summary table for the entire DataFrame
    print('\Share of routine tasks:')
    print(compute_rti_scores.create_summary_table(analysis_df))
    
    # Print the summary table for rows where 'priority' is True
    print('\nShare of routine tasks across priority services only:')
    priority_df = analysis_df[analysis_df['priority']]
    print(compute_rti_scores.create_summary_table(priority_df))
    
    # Save the updated DataFrame to a pickle file
    analysis_df.to_pickle(output_file_path)


if __name__ == "__main__":
    main()

