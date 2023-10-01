# Directory Structure

The project directory structure is organized as follows:

- `/src`: Contains the main Python scripts.
- `/reports`: Reserved for generated figures and reports (including an execution_report.pdf for run_data_pipeline.py)
- `/notebooks`: Contains Jupyter notebooks (e.g., '02-figure-2.ipynb').
- `/dsindexenv`: Virtual environment for the project (not shown in the description).
- `/docs`: Documentation for the project (not detailed in the description).
- `/data`: Contains subfolders for raw, processed, miscellaneous, and archived data.

Within the `/src` directory, you will find subfolders:
- `/data`: Data collection scripts.
- `/analysis`: Scripts for computing key descriptive statistics.
- `/preprocess`: Data preprocessing scripts.

## Key Python Files

### run_data_pipeline.py

- **Purpose**: This script is responsible for running data collection and preprocessing tasks. It orchestrates the execution of various functions related to collecting data through web scraping or APIs and preprocessing files stored in the 'raw' directory, saving them to the 'processed' directory.

### run_analysis.py

- **Purpose**: This script performs data analysis on key files stored in the 'processed' directory. It calculates important statistics and generates a summary table. The key tasks include creating task group categories, returning task counts, computing RTI scores, and producing summary tables for the entire dataset and for rows where 'priority' is True.

### time_data_pipeline.py

- **Purpose**: This script measures the execution time of data processing tasks and generates an execution time report. It times the execution of various functions related to data collection and preprocessing and presents the results in a PDF report.

## Usage

To run the scripts, execute them in the project's virtual environment from the /src directory, ensuring that all dependencies are installed.

```bash
python run_data_pipeline.py
python run_analysis.py
python time_data_pipeline.py
```

##  Author

- **Author**: Vincent Straub
- **Email**: vstraub@turing.ac.uk

## Status

- **Status**: Testing

Please ensure that all necessary dependencies and libraries are properly installed before running the script. Additionally, make sure that the `/data` and `/preprocess` directories contain the required modules and scripts for data collection and preprocessing tasks.

For any questions or issues related to this script, you can contact the author via the provided email address.

Happy data processing!
