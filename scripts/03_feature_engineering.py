import pandas as pd
import os

# Define file paths
input_data_folder = "outputs/consolidated_data/"  # Adjust as needed
output_data_folder = "outputs/consolidated_data/"
consolidated_file = os.path.join(input_data_folder, "consolidated_data.csv")

# Load consolidated dataset
df = pd.read_csv(consolidated_file)

# Extract subject names and grade levels
df["Subject"] = df["Name"].str.extract(r"([A-Za-z\s.]+)")
df["Grade"] = df["Name"].str.extract(r"(\d+)$").astype(float)

# Define subjects to average
subjects = ["Mathematics", "Reading", "Science", "U.S. History", "Writing"]

# Define interval columns (all except "Name", "Subject", and "Grade")
interval_cols = [col for col in df.columns if col not in ["Name", "Subject", "Grade"]]

# Initialize a list for new rows
new_rows = []

# Compute subject-wise averages (across all grades)
for subject in subjects:
    sub_df = df[df["Subject"].str.strip() == subject]
    avg_scores = sub_df[interval_cols].mean().to_dict()  # Compute mean scale scores
    new_rows.append({"Name": subject, **avg_scores})

# Compute "Total" row (average of Reading, Science, U.S. History, and Writing)
total_df = df[df["Subject"].isin(["Reading", "Science", "U.S. History", "Writing"])]
total_avg_scores = total_df[interval_cols].mean().to_dict()
new_rows.append({"Name": "Total", **total_avg_scores})

# Compute STEM row (Average of Science & Mathematics across all grades)
stem_df = df[df["Subject"].isin(["Mathematics", "Science"])]
stem_avg_scores = stem_df[interval_cols].mean().to_dict()
new_rows.append({"Name": "STEM", **stem_avg_scores})

# Compute English row (Average of Reading & Writing across all grades)
english_df = df[df["Subject"].isin(["Reading", "Writing"])]
english_avg_scores = english_df[interval_cols].mean().to_dict()
new_rows.append({"Name": "English", **english_avg_scores})

# Compute Grade-Specific Totals (Avg of Mathematics, Reading, Science, U.S. History, Writing for each grade)
for grade in [4, 8, 12]:
    grade_df = df[(df["Grade"] == grade) & df["Subject"].isin(subjects)]
    grade_avg_scores = grade_df[interval_cols].mean().to_dict()
    new_rows.append({"Name": f"Total{int(grade)}", **grade_avg_scores})

    # Compute STEM row for each grade
    stem_grade_df = df[(df["Grade"] == grade) & df["Subject"].isin(["Mathematics", "Science"])]
    stem_grade_avg_scores = stem_grade_df[interval_cols].mean().to_dict()
    new_rows.append({"Name": f"STEM{int(grade)}", **stem_grade_avg_scores})

    # Compute English row for each grade
    english_grade_df = df[(df["Grade"] == grade) & df["Subject"].isin(["Reading", "Writing"])]
    english_grade_avg_scores = english_grade_df[interval_cols].mean().to_dict()
    new_rows.append({"Name": f"English{int(grade)}", **english_grade_avg_scores})

# Convert new rows to DataFrame
new_df = pd.DataFrame(new_rows)

# Remove 'Subject' and 'Grade' columns before merging
df = df.drop(columns=["Subject", "Grade"], errors="ignore")

# Ensure new rows match original column structure
new_df = new_df[df.columns]

# Append the new rows to the original DataFrame
final_df = pd.concat([df, new_df], ignore_index=True)

# Save the new dataset
output_file = os.path.join(output_data_folder, "consolidated_subject_averages.csv")
final_df.to_csv(output_file, index=False)

# Print completion message
print(f"Updated CSV with original data + subject & grade-specific totals saved at: {output_file}")
