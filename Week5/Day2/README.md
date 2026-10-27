# Week 5 - Day 2: AutoGen Agents and Teams

This folder contains Python examples using AutoGen agents, teams, tools, and memory with the `gpt-4o-mini` model.

## Examples

| File | Description |
|---|---|
| `memory_agent.py` | Stores simple user facts in `ListMemory` and asks an assistant to use them. |
| `multiagent_birthday_team.py` | Runs a writer and reviewer in a round-robin team to create and review a birthday message. |
| `round_robin_team.py` | Runs a writer and reviewer to improve a thank-you note, stopping when the reviewer approves or the message limit is reached. |
| `team_opeartions.py` | Streams a writer-reviewer slogan team, resets it, and runs a second slogan task. |
| `web_search_agent.py` | Gives an assistant a DuckDuckGo web-search tool to answer a question using search results. |
| `weather_news/` | A city weather-news agent example with its own [README](./weather_news/README.md). |

## Requirements

- Python 3.10 or later
- An OpenAI API key
- Internet access for model requests and the search examples

Install the packages used by these examples:

```powershell
python -m pip install python-dotenv ddgs "autogen-agentchat" "autogen-ext[openai]" autogen-core
```

## Configure the API key

Create a `.env` file in this folder, or set `OPENAI_API_KEY` in your environment:

```text
OPENAI_API_KEY=your-openai-api-key
```

Do not commit your API key or `.env` file to source control.

## Run an example

Open a terminal in this folder and run the desired script, for example:

```powershell
python .\memory_agent.py
```

Replace `memory_agent.py` with another script name from the examples table. The weather-news script is inside its subfolder:

```powershell
python .\weather_news\weather_news.py
```
