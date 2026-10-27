import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv


async def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print("SUCCESS: OPENAI_API_KEY is loaded.")
        print("Key starts with sk-:", api_key.startswith("sk-"))
    else:
        print("ERROR: OPENAI_API_KEY was not found.")

    # Initialize the model client
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )

    try:
        # Create the assistant agent
        assistant = AssistantAgent(
            name="first_agent",
            model_client=model_client,
            system_message="You are a helpful AI assistant.",
        )

        # Ask the agent a question
        result = await assistant.run(
            task="Give me a fun fact about the moon"
        )

        # Print the agent's response
        print(result.messages[-1].content)

    finally:
        # Close the model client
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())