import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

    
load_dotenv()

# Step 1: Read the API key from the environment
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Set it in Windows PowerShell before running."
    )


# Step 2: Create the OpenAI model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# Step 3: Write a clear prompt
prompt = """
Suggest exactly 5 healthy breakfast ideas.

Define healthy as a balanced breakfast with nutritious
ingredients and a good source of protein and fibre
where practical. Prefer familiar Indian breakfast foods.

Requirements:
- Number the ideas from 1 to 5.
- Write exactly one line per idea.
- Do not include an introduction or conclusion.
- Return only the five numbered ideas.
"""


# Step 4: Invoke the model and inspect the message object
reply = llm.invoke(prompt)

print("Full message object:")
print(reply)

# Step 5: Print only the response text
print("\nFive Healthy Breakfast Ideas:")
print(reply.content)
