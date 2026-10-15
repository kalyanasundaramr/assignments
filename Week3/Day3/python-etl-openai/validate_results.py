
import pandas as pd

file_path = "data/processed/cleaned_data.csv"
df = pd.read_csv(file_path, dtype=str).fillna("")

email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
email_invalid = ~df["email"].str.match(email_pattern, na=False)

phone_digits = df["phone"].str.replace(r"\D", "", regex=True)
phone_invalid = phone_digits.str.len() != 10

print("ETL QUALITY VALIDATION")
print("-" * 35)
print(f"Total records: {len(df)}")
print(f"Invalid email records: {email_invalid.sum()}")
print(f"Invalid phone records: {phone_invalid.sum()}")
print(f"Records with either issue: {(email_invalid | phone_invalid).sum()}")
print(f"Records passing both checks: {(~(email_invalid | phone_invalid)).sum()}")
print(f"Exact duplicate rows: {df.duplicated().sum()}")
print("\nDepartment distribution:")
print(df["department"].value_counts().to_string())
