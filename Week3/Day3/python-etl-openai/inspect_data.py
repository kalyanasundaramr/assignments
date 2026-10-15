
import pandas as pd
from pathlib import Path

# Locate the input CSV
file_path = Path("data/raw/unclean_data.csv")

# Check that the file exists
if not file_path.exists():
    raise FileNotFoundError(f"CSV file not found: {file_path.resolve()}")

# Load the CSV
df = pd.read_csv(file_path)

# Display basic information
print("\n--- DATASET OVERVIEW ---")
print(f"Number of records: {len(df)}")
print(f"Number of columns: {len(df.columns)}")

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- FIRST 5 RECORDS ---")
print(df.head().to_string())

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

print("\n--- DATA TYPES ---")
print(df.dtypes)
    