
import asyncio
import os

from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.research_agent import create_research_agent
from agents.writer_agent import create_writer_agent
from agents.seo_agent import create_seo_agent

load_dotenv()


async def main():
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        # Initialize three agents
        research_agent = create_research_agent(model_client)
        writer_agent = create_writer_agent(model_client)
        seo_agent = create_seo_agent(model_client)

        topic = "Best AI Tools for Small Businesses in 2026"

        # Agent 1: Research
        print("\n========== RESEARCH AGENT ==========\n")

        research_result = await research_agent.run(
            task=(
                f"Research the topic: {topic}. "
                "Find relevant keywords, search intent, "
                "trends, and supporting source URLs."
            )
        )

        research_brief = research_result.messages[-1].content
        print(research_brief)

        # Agent 2: Content Writer
        print("\n========== CONTENT WRITER AGENT ==========\n")

        writer_result = await writer_agent.run(
            task=(
                f"Write an approximately 800-word SEO article "
                f"about: {topic}\n\n"
                f"Research Brief:\n{research_brief}"
            )
        )

        article = writer_result.messages[-1].content
        print(article)

        # Agent 3: SEO Optimization
        print("\n========== SEO OPTIMIZATION AGENT ==========\n")

        seo_result = await seo_agent.run(
            task=(
                "Optimize the following article for SEO.\n\n"
                f"Topic: {topic}\n\n"
                f"Research Brief:\n{research_brief}\n\n"
                f"Original Article:\n{article}"
            )
        )

        optimized_article = seo_result.messages[-1].content
        print(optimized_article)

        print("\n========== THREE-AGENT WORKFLOW COMPLETED ==========\n")

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
