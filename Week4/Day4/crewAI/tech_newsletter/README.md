# Tech Newsletter — Two-Agent CrewAI

## Objective
Build a two-agent AI workflow that researches technology news and writes a concise five-line newsletter.

## Agents
- **Researcher:** Uses SerperDevTool to search for technology news and gather headlines, publishers, dates, article URLs, and summaries.
- **Writer:** Uses the Researcher's findings to produce a short newsletter with three stories and a “Why it matters” takeaway.

## Technologies
- Python
- CrewAI
- OpenAI GPT-4o mini
- SerperDevTool
- python-dotenv

## Setup
1. Install the required dependencies: `crewai`, `crewai-tools`, and `python-dotenv`.
2. Create a `.env` file with `OPENAI_API_KEY`, `MODEL`, and