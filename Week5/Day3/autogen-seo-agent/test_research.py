
import asyncio
import os

from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.research_agent import create_research_agent

load_dotenv()


async def main():
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        research_agent = create_research_agent(model_client)

        print("\nStarting SEO Research Agent...\n")

        result = await research_agent.run(
            task=(
                "Research the topic: "
                "'Best AI Tools for Small Businesses in 2026'. "
                "Identify SEO keywords, current trends, "
                "search intent, and supporting sources."
            )
        )

        print("\n========== AGENT EXECUTION ==========\n")

        for message in result.messages:
            print(f"\nMessage Type: {type(message).__name__}")
            print(f"Source: {message.source}")
            print(f"Content:\n{message.content}")

        print("\n========== RESEARCH COMPLETED ==========\n")

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
