import asyncio
import os

from dotenv import load_dotenv
from ddgs import DDGS

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables, including OPENAI_API_KEY.
load_dotenv()

def search_weather_news(city: str) -> str:
    """Search DuckDuckGo News for today's weather news and forecasts
    in the specified city. Return up to five relevant news results
    for the weather news agent to summarize."""

    results = DDGS().news(
        f"{city} weather today",
        max_results=5
    )

    if not results:
        return "No weather news found."

    return "\n\n".join(
        f"Title: {result.get('title', 'No title')}\n"
        f"Description: {result.get('body', 'No description')}\n"
        f"URL: {result.get('url', result.get('href', 'No URL available'))}"
        for result in results
    )


city = input("Which city? ")

model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

agent = AssistantAgent(
    name="weather_news",
    model_client=model_client,
    tools=[search_weather_news],
    system_message=(
       "You are a Weather News Agent. "
        "Use the search_weather_news tool to find current "
        "weather news for the city provided by the user. "
        "Base your answer on the search results. "
        "Do not invent weather conditions or forecasts. "
        "Summarize the findings in exactly three short lines. "
        "Each line must contain one concise sentence. "
        "Mention the city and relevant weather conditions. "
        "If the search results do not provide reliable "
        "current information, say so clearly. "
        "Do not include headings, bullet points, or extra lines."
    ),
    reflect_on_tool_use=True,
)

async def main():
    try:
        # Stream the agent's execution and capture the result
        stream = agent.run_stream(
            task= (  
                f"Find today's weather news for {city}. "
                "Use the search tool and provide exactly three "
                "short lines based on the results."
            )
        )

        async for event in stream:
            # Display tool calls in the expected format
            if event.__class__.__name__ == "ToolCallRequestEvent":
                print("---------- ToolCallRequestEvent (weather_news) ----------")

                for call in event.content:
                    print(f"{call.name}(city='{city}')")

            # Display the final answer as exactly three lines
            elif event.__class__.__name__ == "TaskResult":
                answer = event.messages[-1].content.strip()

                import re
                sentences = re.split(r'(?<=[.!?])\s+', answer)
                sentences = [s.strip() for s in sentences if s.strip()]

                lines = sentences[:3]

                while len(lines) < 3:
                    lines.append(
                        "Further details are unavailable in the search results."
                    )

                print("---------- TextMessage (weather_news) ----------")
                print("\n".join(lines))

    finally:
        await model_client.close()


asyncio.run(main())
