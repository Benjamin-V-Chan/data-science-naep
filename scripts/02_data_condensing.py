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


# Process each CSV file
for file in input_csv_files:
    
    print(f"\nProcessing: {file}")

    # Extract subject and grade level from the filename (handles "U.S. HistoryX")
    filename_without_ext = os.path.splitext(file)[0]  # Remove file extension
    match = re.match(r"(.+?)(\d+)$", filename_without_ext)  # Extracts multi-word subjects + grade level
    
    if match:
        subject = match.group(1).strip()  # Extracts subject (multi-word friendly)
        grade_level = match.group(2)      # Extracts grade level
        name = f"{subject}{grade_level}"  # Combine into Name column
        if first_subject_grade is None:
            first_subject_grade = name  # Store first dataset's name for final CSV filename
    else:
        print(f"Skipping {file}: Filename format not recognized")
        continue

    # Read CSV, skipping blank lines and unnecessary headers
    df = pd.read_csv(os.path.join(data_folder, file), skip_blank_lines=True, header=None)

    # Assign correct column names
    df.columns = ["Year", "Jurisdiction", "Days Absent", "Average Scale Score"]
    