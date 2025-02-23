import pandas as pd
import os

input_csv_files = [f for f in os.listdir("data/raw/") if f.endswith(".csv")]

print(input_csv_files)
for input_csv_path in input_csv_files:
    
    # Initialize DataFrame
    print(input_csv_path)
    
    # Load CSV while skipping metadata rows (adjust skiprows as needed)
    df = pd.read_csv('data/raw/' + input_csv_path, skiprows=lambda x: x < 8, header=None)
    print(df)

    # Drop fully empty columns
    df = df.dropna(how="all", axis=1)

    # Identify the first row that contains column headers
    df.columns = df.iloc[0]  # Use the first valid row as column names
    df = df[1:].reset_index(drop=True)  # Remove the original header row

    # Find the first row containing "NOTE" and remove all rows after it
    note_index = df[df.iloc[:, 0].astype(str).str.contains("NOTE", na=False)].index

    if not note_index.empty:
        df = df.loc[: note_index[0] - 1]  # Keep rows only before the "NOTE"

    # Drop any remaining empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    print(df)

    # Output Data
    csv_path_split = input_csv_path.split(',')
    print(csv_path_split)

    subject_split = csv_path_split[0].split('_')
    subject = subject_split[-1]
    print(subject)
    
    grade_split = csv_path_split[1].split()
    grade = grade_split[-1]
    print(grade)

    output_csv_path = f"data/cleaned/{subject}{grade}.csv"
    df.to_csv(output_csv_path, index=False)