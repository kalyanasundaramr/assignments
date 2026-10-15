
import pandas as pd
from pathlib import Path

input_file = Path("data/processed/cleaned_data.csv")
output_file = Path("data/processed/records_for_review.csv")

df = pd.read_csv(input_file, dtype=str).fillna("")

# Email validation
email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
invalid_email = ~df["email"].str.match(email_pattern, na=False)

# Phone validation: this project currently assumes 10 digits
phone_digits = df["phone"].str.replace(r"\D", "", regex=True)
invalid_phone = phone_digits.str.len() != 10

# Keep records that need review
review_df = df[invalid_email | invalid_phone].copy()

review_df["email_valid"] = ~invalid_email[review_df.index]
review_df["phone_valid"] = ~invalid_phone[review_df.index]
review_df["review_status"] = "Manual review required"

output_file.parent.mkdir(parents=True, exist_ok=True)
review_df.to_csv(output_file, index=False)

print(f"Records needing review: {len(review_df)}")
print(f"Saved to: {output_file}")
print("\nRecords to review:")
print(review_df.to_string(index=False))
