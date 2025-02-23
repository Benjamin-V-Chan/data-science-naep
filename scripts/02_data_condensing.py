import pandas as pd
import os
import re

# Define the folder containing the CSV files
data_folder = "data/cleaned/"  # Change this to your actual folder path

# Get a list of all CSV files in the folder
input_csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

# Mapping for days absent intervals to ensure consistency
interval_mapping = {
    "None": "0",
    "": "0",  # Handle blank spaces as "0 days"
    "1-2 days": "1-2",
    "3-4 days": "3-4", 
    "5-10 days": "5-10",
    "More than 10 days": "More than 10",
    "1 or 2 days": "1-2",
    "3 or 4 days": "3-4",
    "5 or 10 days": "5-10",
    "More than 10 days": "More than 10"
}

# Define standardized absence intervals for the final DataFrame
standard_intervals = ["0", "1-2", "3-4", "5-10", "More than 10"]

# Initialize an empty DataFrame with fixed columns
final_df = pd.DataFrame(columns=["Name"] + standard_intervals)

# Keep track of the first subject/grade for naming the output file
first_subject_grade = None

print(input_csv_files)
