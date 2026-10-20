import os
import json
import csv
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
client = OpenAI()

# 2. Input data to process
products = [
    "Eco-friendly stainless steel water bottle, 32 oz, keeps drinks cold for 24 hours. Price: $24.99. Color: Matte Black.",
    "Wireless Bluetooth Over-Ear Headphones with active noise cancellation, 40-hour battery life. Cost is $149.50. Color: Silver.",
    "Ergonomic mesh office chair with lumbar support and adjustable armrests. Price: $199.99. Color: Gray."
]

output_filename = "extracted_products.csv"

print("--- Starting AI Automation & CSV Export ---\n")

# 3. Create/Open CSV file for writing
with open(output_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    # Define CSV column names
    fieldnames = ["product_name", "capacity_or_feature", "price", "color"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write column headers to CSV
    writer.writeheader()

    # 4. Process each product and write immediately to CSV
    for index, product_desc in enumerate(products, start=1):
        print(f"Processing Item {index}...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system", 
                    "content": "You are an automated data extraction tool. Extract product details and return JSON with exact keys: 'product_name', 'capacity_or_feature', 'price', and 'color'."
                },
                {
                    "role": "user", 
                    "content": product_desc
                }
            ]
        )
        
        # Parse JSON output from AI
        extracted_data = json.loads(response.choices[0].message.content)
        
        # Write the dictionary row into our CSV
        writer.writerow(extracted_data)

print(f"\n Success! All data processed and saved to '{output_filename}'.")