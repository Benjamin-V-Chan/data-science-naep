import pandas as pd
import os

# Define file paths for data storage

# Load the consolidated dataset into a DataFrame

# Extract subject names and grade levels from the "Name" column

# Convert grade values to integers for numerical operations

# Define standard subject names for reference

# Initialize an empty list to store new computed rows

# Function to compute the average scores for a given subject and grade level
    # Filter data for the specified subject
    # Further filter by grade if specified
    # Compute mean values for numeric columns (excluding "Name", "Subject", "Grade")

# Function to compute combined averages for STEM and English subjects
    # Filter data for the first subject
    # Filter data for the second subject
    # Further filter by grade if specified
    # Sum corresponding values from both subjects
    # Compute the average after summing

# Generate subject-wise averages for specified grades
    # Loop through each subject
    # Loop through each grade level
    # Compute and store the average scores

# Generate STEM (Mathematics + Science) and English (Writing + Reading) averages
    # Loop through each grade level
    # Compute and store the STEM average
    # Compute and store the English average

# Generate total scores (Sum of all subjects, then average)
    # Loop through each grade level
    # Compute total scores by summing across all subjects
    # Compute the average for the total scores
    # Store the computed total scores

# Convert new computed rows into a DataFrame

# Append newly computed rows to the original dataset

# Save the updated dataset with new computed features

# Print completion message with output file path