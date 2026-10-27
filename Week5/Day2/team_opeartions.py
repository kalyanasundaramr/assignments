
import asyncio
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


# Load environment variables from .env
load_dotenv()


async def main():
    # 1. Configure the OpenAI model
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )

    try:
        # 2. Create the Writer agent
        writer = AssistantAgent(
            name="writer",
            model_client=model_client,
            system_message=(
                "Write one short, catchy slogan. "
                "Improve it if the reviewer suggests changes."
            ),
        )

        # 3. Create the Reviewer agent
        reviewer = AssistantAgent(
            name="reviewer",
            model_client=model_client,
            system_message=(
                "Review the slogan written by the writer. "
                "If the slogan is catchy, memorable, and appropriate, "
                "reply with APPROVE. "
                "Otherwise, suggest one specific improvement."
            ),
        )

        # 4. Create the team
        team = RoundRobinGroupChat(
            participants=[writer, reviewer],
            termination_condition=TextMentionTermination("APPROVE"),
        )

        # 5. Run the first task and display the conversation live
        print("\n--- COFFEE SHOP SLOGAN ---\n")

        await Console(
            team.run_stream(
                task="Create a slogan for a coffee shop."
            )
        )

        # 6. Reset the team before starting a new task
        print("\n--- RESETTING TEAM ---\n")

        await team.reset()

        # 7. Run a new, unrelated task
        print("--- BOOK STORE SLOGAN ---\n")

        result = await team.run(
            task="Create a slogan for a book store."
        )

        # 8. Display the final message
        print("\n--- FINAL RESULT ---\n")
        print(result.messages[-1].content)

    finally:
        # 9. Close the model client
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
