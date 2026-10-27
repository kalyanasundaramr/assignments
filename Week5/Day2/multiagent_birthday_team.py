
"""
AutoGen Round-Robin Team
Purpose: Generate and review a birthday message for a friend.
"""

import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main() -> None:
    """Run the writer and reviewer agents."""

    # Load environment variables from .env.
    load_dotenv()

    # Initialize the OpenAI model client.
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )

    try:
        # Agent 1: The writer
        #      
        writer = AssistantAgent(
            name="writer",
            model_client=model_client,
            system_message=(
                "You write a short birthday message. "
                "Improve it if the reviewer asks."
            ),
        )

        # Agent 2: The reviewer
        reviewer = AssistantAgent(
            name="reviewer",
            model_client=model_client,
            system_message=(
                "Review the message. If it is good, reply with "
                "the single word APPROVE. Otherwise, suggest one change."
            ),
        )

        # Stop when the reviewer says APPROVE.
        stop = TextMentionTermination("APPROVE")

        # Build the team: writer, reviewer, writer, reviewer, ...
        team = RoundRobinGroupChat(
            participants=[writer, reviewer],
            termination_condition=stop,
        )

        # Run the team.
        result = await team.run(
            task="Write a warm birthday message for my friend Sam."
        )

        # Print the entire conversation.
        print("\n--- Birthday Message Team Conversation ---\n")

        for message in result.messages:
            print(f"[{message.source}] {message.content}\n")

        print("Why the team stopped:", result.stop_reason)

    finally:
        # Close the model client.
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
