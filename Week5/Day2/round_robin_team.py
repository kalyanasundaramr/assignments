"""
AutoGen Round-Robin Team
Week 5 - Day 2

The writer creates a thank-you note, and the reviewer
checks whether the note is polite.

The team stops when:
1. The reviewer mentions APPROVE, or
2. The team reaches 6 messages.
"""

import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination,
)
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main() -> None:
    """Create and run the writer-reviewer team."""

    # Load environment variables from .env.
    load_dotenv()

    # Initialize the OpenAI model client.
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )

    try:
        # Agent 1: Writer
        writer = AssistantAgent(
            name="writer",
            model_client=model_client,
            system_message=(
                "Write a short thank-you note. "
                "Improve it if asked."
            ),
        )

        # Agent 2: Reviewer
        reviewer = AssistantAgent(
            name="reviewer",
            model_client=model_client,
            system_message=(
                "If the note is polite, reply APPROVE. "
                "Otherwise, suggest one change."
            ),
        )

        # Stop when APPROVE appears or after 6 messages.
        stop = (
            TextMentionTermination("APPROVE")
            | MaxMessageTermination(6)
        )

        # Create the team using round-robin execution.
        team = RoundRobinGroupChat(
            participants=[writer, reviewer],
            termination_condition=stop,
        )

        # Run the team.
        result = await team.run(
            task="Write a thank-you note to a teacher."
        )

        # Display the result summary.
        print("Total messages:", len(result.messages))
        print("Why it stopped:", result.stop_reason)

        # Display the conversation.
        print("\n--- Team Conversation ---")

        for message in result.messages:
            source = getattr(message, "source", "unknown")
            content = getattr(message, "content", "")
            print(f"\n{source}:\n{content}")

    finally:
        # Release model client resources.
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
