"""
AutoGen Web Search Agent

Uses DuckDuckGo to search the web and AutoGen with OpenAI GPT-4o-mini
to answer questions using the search results.
"""

import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables, including OPENAI_API_KEY.
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("SUCCESS: OPENAI_API_KEY is loaded.")
    print("Key starts with sk-:", api_key.startswith("sk-"))
else:
    print("ERROR: OPENAI_API_KEY was not found.")

# Define a web search tool using DuckDuckGo (no search API key required).
def web_search(query: str) -> str:
    """Search the web and return the top three results as text."""

    from ddgs import DDGS

    results = DDGS().text(query, max_results=3)

    if not results:
        return "No results found."

    # Format the search results so the agent can read them.
    return "\n\n".join(
        f"{result['title']}\n{result['body']}\n{result['href']}"
        for result in results
    )

# 
async def main() -> None: 
    """Create the agent, perform a web search, and display the answer."""

    # Initialize the OpenAI model client.
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )

    try:
        # Create an assistant agent with the web search tool.
        searcher = AssistantAgent(
            name="searcher",
            model_client=model_client,
            tools=[web_search],
            reflect_on_tool_use=True,
            system_message=(
                "You answer questions using the web_search tool. "
                "Use the search results to answer the question accurately.  "
                "Keep answers short. If the results do not establish the "
                "answer, explain the uncertainty."
            ),
        )

        # Ask the agent to search the web and answer the question.
        result = await searcher.run(
            task="Who won the latest FIFA World Cup? Search the web."
        )

        # Print the final response.
        print(result.messages[-1].content)

    finally:
        # Release model client resources.
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())