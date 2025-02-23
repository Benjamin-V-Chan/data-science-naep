import pandas as pd
import os
import re

# Define the folder containing the CSV files
input_data_folder = "data/cleaned/"  # Change this to your actual folder path
output_data_folder = "outputs/consolidated_data/"

# Get a list of all CSV files in the folder
input_csv_files = [f for f in os.listdir(input_data_folder) if f.endswith(".csv")]

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
    df = pd.read_csv(os.path.join(input_data_folder, file), skip_blank_lines=True, header=None)

    # Assign correct column names
    df.columns = ["Year", "Jurisdiction", "Days Absent", "Average Scale Score"]

    # Drop rows that don't contain valid year information
    df = df[df["Year"].astype(str).str.contains(r"^\d{4}$", na=False)]

    # Fill missing values in "Days Absent" with ""
    df["Days Absent"] = df["Days Absent"].fillna("")

    # Convert intervals to standardized labels
    df["Days Absent"] = df["Days Absent"].map(interval_mapping).fillna(df["Days Absent"])

    # Convert "Average Scale Score" to float
    df["Average Scale Score"] = pd.to_numeric(df["Average Scale Score"], errors="coerce")

    # Initialize a row with NaN values for all intervals
    new_row = {col: None for col in final_df.columns}
    new_row["Name"] = name

    # Populate the row with the correct absence interval values
    for _, row in df.iterrows():
        interval = row["Days Absent"]
        score = row["Average Scale Score"]
        if interval in standard_intervals:
            new_row[interval] = score

    # Append to final DataFrame
    final_df = pd.concat([final_df, pd.DataFrame([new_row])], ignore_index=True)

# Save the consolidated data with a dynamic filename
output_filename = "consolidated_data.csv"
output_path = os.path.join(output_data_folder, output_filename)
final_df.to_csv(output_path, index=False)

# Print completion message
print(f"Consolidated CSV saved at: {output_path}")
