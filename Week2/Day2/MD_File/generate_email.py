import os
from openai import OpenAI


# 1. Read the Markdown prompt
with open("email_generation_prompt.md", "r", encoding="utf-8") as file:
    prompt = file.read()


# 2. Get user's email requirements
print("Email Generation")
print("=" * 50)

user_requirement = input(
    "Enter your email requirement: "
)


# 3. Combine the Markdown prompt and user's requirement
combined_prompt = f"""
{prompt}

## User's Email Requirement

{user_requirement}

Generate the final email based on all the instructions above.
Return only the email, including the subject line.
"""


# 4. Connect to the AI model
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


response = client.responses.create(
    model="gpt-5.6",
    input=combined_prompt
)


# Get generated email
generated_email = response.output_text


# 5. Display the generated email
print("\nGenerated Email")
print("=" * 50)
print(generated_email)
print("=" * 50)


# 6. Optionally save the email
save_email = input("\nDo you want to save this email as email.txt? (y/n): ")

if save_email.lower() == "y":
    with open("email.txt", "w", encoding="utf-8") as file:
        file.write(generated_email)

    print("\nEmail saved successfully as email.txt")
else:
    print("\nEmail was not saved.")