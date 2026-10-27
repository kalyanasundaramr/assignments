"""
AutoGen Memory Agent

Demonstrates how to use ListMemory and MemoryContent
to store user facts and provide them to an AssistantAgent.
"""

import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.memory import ListMemory, MemoryContent


# Load environment variables, including OPENAI_API_KEY.
load_dotenv()


async def main() -> None:
    """Create memory, store user facts, and run the assistant."""

    # Initialize the OpenAI model client.
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )

    try:
        # 1. Create a memory store.
        memory = ListMemory()

        # 2. Add facts to the memory.
        await memory.add(
            MemoryContent(
                content="The user's name is Kalyan.",
                mime_type="text/plain",
            )
        )

        await memory.add(
            MemoryContent(
                content="The user loves cricket.",
                mime_type="text/plain",
            )
        )

        # 3. Create an assistant and provide its memory.
        agent = AssistantAgent(
            name="assistant",
            model_client=model_client,
            memory=[memory],
            system_message="You are a friendly assistant.",
        )

        # 4. Ask a question that uses the remembered facts.
        result = await agent.run(
            task="What is my name, and suggest a sport I would enjoy."
        )

        # 5. Display the assistant's response.
        print(result.messages[-1].content)

    finally:
        # Close the model client.
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
