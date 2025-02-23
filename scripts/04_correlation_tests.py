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

### Bar Chart - Correlation Strength ###
plt.figure(figsize=(12, 6))
sns.barplot(x=correlation_results_sorted.index, y=correlation_results_sorted.values, palette="coolwarm")
plt.axhline(y=0, color="black", linestyle="--")
plt.xlabel("Subjects")
plt.ylabel("Pearson Correlation with Absenteeism")
plt.title("Correlation Strength: Absenteeism Impact on Scale Scores")
plt.xticks(rotation=90)
plt.grid(True)
barchart_path = os.path.join(output_folder, "correlation_strength_bar_chart.png")
plt.savefig(barchart_path, dpi=300, bbox_inches="tight")
plt.show()

### Heatmap - Correlation Matrix ###
plt.figure(figsize=(10, 6))
sns.heatmap(df[interval_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Heatmap: Absenteeism vs. Scale Scores")
heatmap_path = os.path.join(output_folder, "correlation_heatmap.png")
plt.savefig(heatmap_path, dpi=300, bbox_inches="tight")
plt.show()

### Line Plot - Score Trends Across Intervals ###
plt.figure(figsize=(12, 6))
for subject in df.index:
    plt.plot(interval_cols, df.loc[subject, interval_cols], marker="o", label=subject)
plt.xlabel("Absenteeism Interval (Ordinal)")
plt.ylabel("Scale Score")
plt.title("Scale Score Decline Across Absenteeism Intervals")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
lineplot_path = os.path.join(output_folder, "lineplot_score_trend.png")
plt.savefig(lineplot_path, dpi=300, bbox_inches="tight")
plt.show()

### Bar Chart - Percentage Drop ###
plt.figure(figsize=(12, 6))
sns.barplot(x=percentage_drop_sorted.index, y=percentage_drop_sorted.values, palette="magma")
plt.xlabel("Subjects")
plt.ylabel("Percentage Drop in Scores (%)")
plt.title("Percentage Drop in Scores: 0 Absences vs. More than 10 Absences")
plt.xticks(rotation=90)
plt.grid(True)
percentage_drop_path = os.path.join(output_folder, "percentage_drop_bar_chart.png")
plt.savefig(percentage_drop_path, dpi=300, bbox_inches="tight")
plt.show()

### Box Plot - Score Distribution per Absenteeism Interval ###
df_melted = df[interval_cols].melt(var_name="Absenteeism Interval", value_name="Scale Score")
plt.figure(figsize=(12, 6))
sns.boxplot(x="Absenteeism Interval", y="Scale Score", data=df_melted, order=interval_cols)
plt.title("Distribution of Scale Scores by Absenteeism Interval")
plt.grid(True)
boxplot_path = os.path.join(output_folder, "boxplot_scale_distribution.png")
plt.savefig(boxplot_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"All visualizations saved in: {output_folder}")