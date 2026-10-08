from langchain_google_genai import ChatGoogleGenerativeAI


# Create the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)


# Three different prompts
prompts = [
    "Explain what Python is in simple terms for a beginner.",
    "What are three practical uses of artificial intelligence?",
    "A shop has 48 boxes with 24 items in each box. If 375 items are sold, how many items remain?"
]


# Send each prompt to Gemini
for i, prompt in enumerate(prompts, start=1):

    print(f"\n--- Run {i} ---")
    print(f"Prompt: {prompt}")

    response = llm.invoke(prompt)

    print("Answer:")
    print(response.content)