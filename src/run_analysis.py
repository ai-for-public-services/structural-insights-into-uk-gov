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
    
    try:
        # def main():    
        input_file_path = '../data/processed/dataframes/analysis-df-w-api-data.pkl'
        output_file_path = '../data/processed/dataframes/analysis-df-w-api-data.pkl'
        
        # Load the analysis DataFrame
        analysis_df = load_analysis_dataframe(input_file_path)
        
        # Perform data analysis steps
        analysis_df = get_task_groups_count.create_task_group_category(analysis_df)
        print(get_task_groups_count.return_task_counts(analysis_df))
        
        
        if 'RTI' not in analysis_df.columns:
            analysis_df = compute_rti_scores.add_rti_scores(
                analysis_df, compute_rti_scores.compute_rti_scores
            )
        
        if 'RTI_perc' not in analysis_df.columns:
            # Add a column 'RTI_perc' by applying the 'transform_to_percentage' function
            analysis_df['RTI_perc'] = analysis_df['RTI'].apply(
                compute_rti_scores.transform_to_percentage
            )
        
        if 'RTI_rescaled' not in analysis_df.columns:
            # Add a column 'RTI_rescaled' by transforming the RTI_perc column
            analysis_df['RTI_rescaled'] = analysis_df['RTI_perc'].apply(
                lambda x: x / 100 if 0 <= x <= 100 else x
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
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

