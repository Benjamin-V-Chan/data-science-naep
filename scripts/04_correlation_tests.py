import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Define file paths
data_folder = "outputs/consolidated_data/"
output_folder = "outputs/correlation_test/"
os.makedirs(output_folder, exist_ok=True)

# Load dataset
consolidated_file = os.path.join(data_folder, "consolidated_subject_averages.csv")
df = pd.read_csv(consolidated_file)

# Define absenteeism interval columns
interval_cols = ["0", "1-2", "3-4", "5-10", "More than 10"]

# Set "Name" as index and keep only interval columns
df = df.set_index("Name")[interval_cols]

# Compute correlation with absenteeism (Pearson correlation)
correlation_results = df.T.corrwith(pd.Series([0, 1.5, 3.5, 7.5, 12], index=df.columns))

# Calculate percentage drop from 0 absences to More than 10 absences
df["Percentage Drop (%)"] = ((df["0"] - df["More than 10"]) / df["0"]) * 100

# Sort subjects by absolute correlation strength
correlation_results_sorted = correlation_results.sort_values()
percentage_drop_sorted = df["Percentage Drop (%)"].sort_values(ascending=False)

# Categorize correlation strength
def categorize_correlation(value):
    if value <= -0.7:
        return "Strong Negative Correlation 📉"
    elif value <= -0.4:
        return "Moderate Negative Correlation"
    elif value <= -0.2:
        return "Weak Negative Correlation"
    elif value <= 0.2:
        return "Little to No Correlation"
    elif value <= 0.4:
        return "Weak Positive Correlation"
    elif value <= 0.7:
        return "Moderate Positive Correlation"
    else:
        return "Strong Positive Correlation 📈"

# Save correlation results to a text file with UTF-8 encoding
correlation_results_path = os.path.join(output_folder, "correlation_strength.txt")
with open(correlation_results_path, "w", encoding="utf-8") as f:
    f.write("Correlation Strength Between Absenteeism and Scale Scores\n")
    f.write("=" * 70 + "\n\n")
    for subject, value in correlation_results_sorted.items():
        f.write(f"{subject}: {value:.2f} ({categorize_correlation(value)})\n")
    
    f.write("\nPercentage Drop in Scores from 0 Absences to More than 10 Absences\n")
    f.write("=" * 70 + "\n\n")
    for subject, drop in percentage_drop_sorted.items():
        f.write(f"{subject}: {drop:.2f}%\n")

print(f"Correlation strength results saved to: {correlation_results_path}")