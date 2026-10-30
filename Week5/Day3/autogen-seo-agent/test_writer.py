
import asyncio
import os

from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.research_agent import create_research_agent
from agents.writer_agent import create_writer_agent

load_dotenv()


async def main():
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        # Step 1: Initialize agents
        research_agent = create_research_agent(model_client)
        writer_agent = create_writer_agent(model_client)

        topic = "Best AI Tools for Small Businesses in 2026"

        # Step 2: Run Research Agent
        print("\n========== RESEARCH AGENT ==========\n")

        research_result = await research_agent.run(
            task=f"Research this SEO article topic: {topic}"
        )

        research_brief = research_result.messages[-1].content

        print(research_brief)

        # Step 3: Pass research to Writer Agent
        print("\n========== WRITER AGENT ==========\n")

        writer_result = await writer_agent.run(
            task=(
                f"Write an SEO-friendly article about: {topic}\n\n"
                "Target length: approximately 800 words.\n\n"
                f"Research Brief:\n{research_brief}"
            )
        )

        article = writer_result.messages[-1].content

        print(article)

        print("\n========== WORKFLOW COMPLETED ==========\n")

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
