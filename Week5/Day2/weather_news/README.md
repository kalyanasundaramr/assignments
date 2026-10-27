# Weather News Agent

This example uses an AutoGen assistant agent to search DuckDuckGo News for weather updates in a city and summarize the results in exactly three short lines.

## What it does

- Prompts for a city.
- Searches DuckDuckGo News for current weather stories and forecasts.
- Uses the `gpt-4o-mini` model to summarize the search results.
- Prints the tool call and a three-line summary.

## Requirements

- Python 3.10 or later
- An OpenAI API key
- Internet access

Install the required packages:

```powershell
python -m pip install python-dotenv ddgs autogen-agentchat "autogen-ext[openai]"
```

## Configure the API key

Set `OPENAI_API_KEY` in your environment, or create a `.env` file in this directory:

```text
OPENAI_API_KEY=your-openai-api-key
```

Do not commit your API key or `.env` file to source control.

## Run

From this directory, run:

```powershell
python weather_news.py
```

Enter a city when prompted. The agent searches for weather news and prints its summary. Search results and coverage depend on what is available online at the time.
