import pandas as pd
from pathlib import Path

# Get project folder
project_folder = Path(__file__).resolve().parent.parent

# Dataset location
file_path = project_folder / "data" / "raw" / "healthcare_patient_data.csv"

print("Dataset path:")
print(file_path)

print("\nDoes file exist?")
print(file_path.exists())

# Load dataset
df = pd.read_csv(file_path)

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE ROWS ==========")
print(df.duplicated().sum())

print("\n========== BASIC STATISTICS ==========")
print(df.describe())
