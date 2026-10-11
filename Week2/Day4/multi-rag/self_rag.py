import os
import re

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

# Load environment variables from .env
load_dotenv()

# Check OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Please add it to your .env file."
    )

print("OpenAI API key loaded successfully.")

# Create OpenAI model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=100
)