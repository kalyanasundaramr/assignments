
import json
import os
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

load_dotenv()

INPUT_FILE = Path("data/raw/unclean_data.csv")
OUTPUT_FILE = Path("data/processed/cleaned_data.csv")
REPORT_FILE = Path("reports/cleaning_report.json")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing from .env")

client = OpenAI()

# --------------------------------------------------
# 2. Extract
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE, dtype=str).fillna("")

required_columns = {"name", "email", "phone", "department"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

original_count = len(df)
df = df.copy()

# --------------------------------------------------
# 3. Deterministic cleaning
# --------------------------------------------------

# Trim leading/trailing whitespace and repeated spaces.
for column in required_columns:
    df[column] = (
        df[column]
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

# Standardize name capitalization.
df["name"] = df["name"].str.title()

# Normalize department labels using approved values.
approved_departments = {
    "operations": "Operations",
    "legal": "Legal",
    "sales": "Sales",
    "finance": "Finance",
    "human resources": "Human Resources",
    "hr": "Human Resources",
    "it": "IT",
}

df["department"] = df["department"].apply(
    lambda value: approved_departments.get(
        value.casefold(), value
    )
)

# Validate emails; do not rewrite addresses automatically.
email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
df["email_valid"] = df["email"].str.match(
    email_pattern, na=False
)

# Normalize phone punctuation while preserving digits.
df["phone"] = df["phone"].apply(
    lambda value: re.sub(r"[^\d+]", "", value)
)

# Flag phone numbers that do not contain 10 digits.
# This is a rule for this sample dataset, not a universal rule.
df["phone_review"] = df["phone"].apply(
    lambda value: len(re.sub(r"\D", "", value)) != 10
)

# --------------------------------------------------
# 4. Select records for OpenAI review
# --------------------------------------------------

review_rows = df[
    (~df["email_valid"]) | df["phone_review"]
]

review_payload = review_rows[
    ["name", "email", "phone", "department"]
].to_dict(orient="records")

ai_review = []

if review_payload:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Review employee contact records for data quality. "
                    "Do not invent or guess missing facts. "
                    "Do not infer a correct phone number or email address. "
                    "Return JSON only with a top-level 'reviews' array. "
                    "For each input record return its name, issues, "
                    "and recommended_action. Use 'manual_review' when "
                    "the correct value cannot be established."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    review_payload, ensure_ascii=False
                ),
            },
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)
    ai_review = result.get("reviews", [])

# --------------------------------------------------
# 5. Load cleaned output and quality report
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Save a clean data file without internal validation columns.
output_columns = [
    "name", "email", "phone", "department"
]
df[output_columns].to_csv(OUTPUT_FILE, index=False)

report = {
    "input_file": str(INPUT_FILE),
    "output_file": str(OUTPUT_FILE),
    "original_records": original_count,
    "output_records": len(df),
    "duplicate_rows_detected": int(
        df[output_columns].duplicated().sum()
    ),
    "invalid_emails": int((~df["email_valid"]).sum()),
    "phones_requiring_review": int(df["phone_review"].sum()),
    "ai_reviews": ai_review,
}

REPORT_FILE.write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("ETL pipeline completed.")
print(f"Input records: {original_count}")
print(f"Output records: {len(df)}")
print(f"Invalid emails: {report['invalid_emails']}")
print(
    "Phones requiring review: "
    f"{report['phones_requiring_review']}"
)
print(f"Cleaned CSV: {OUTPUT_FILE}")
print(f"Quality report: {REPORT_FILE}")
