from datetime import date
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# Load API keys from the local .env file
load_dotenv(override=True)

# Read credentials from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")
model_name = os.getenv("MODEL", "openai/gpt-4o-mini")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is missing from .env")

if not serper_api_key:
    raise ValueError("SERPER_API_KEY is missing from .env")

# Configure the language model using the environment variable
llm = LLM(
    model=model_name,
    api_key=openai_api_key,
)

# Only the Researcher receives the web search tool
search = SerperDevTool()

researcher = Agent(
    role="Technology News Researcher",
    goal=(
        "Find today's three most important and genuinely current "
        "technology news stories from reliable sources."
    ),
    backstory=(
        "You are a technology journalist and research specialist. "
        "You verify publication dates, prioritize significant developments, "
        "avoid duplicate stories, and provide concise factual summaries "
        "with source links."
    ),
    tools=[search],
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Tech Newsletter Writer",
    goal=(
        "Turn the Researcher's findings into a clear, engaging "
        "technology newsletter containing exactly five lines."
    ),
    backstory=(
        "You are an experienced newsletter editor. You write concise, "
        "accessible technology news for busy readers. You use only the "
        "research provided to you and never perform additional research."
    ),
    llm=llm,
    verbose=True,
)

# Task 1: Research today's news

find = Task(
    description=(
        f"Today's actual date is {date.today().strftime('%B %d, %Y')}. "
        "Research the three most important technology news stories "
        "published on this exact date. Use SerperDevTool to search the web. "
        "Verify each article's actual publication date from its source. "
        "Use only credible technology news articles with direct article URLs. "
        "Never use a publisher's homepage, a YouTube video, or a generic landing page "
        "as an article URL. Confirm that each URL points to the specific story and "
        "that the headline and publication date match the source. Do not invent "
        "stories or claim verification when the source cannot be confirmed. "
        "Do not treat an old article as today's news. Do not invent dates, "
        "URLs, or facts. For each story, provide its headline, publisher, "
        "verified publication date, direct article URL, and one-sentence "
        "factual summary. If three qualifying stories cannot be verified, "
        "report that instead of inventing stories."
    ),
    expected_output=(
        "Three research records, each containing a headline, publisher, "
        "verified publication date, direct article URL, and factual summary. "
        "Publication dates must match the actual current date. Clearly state "
        "if three qualifying stories cannot be verified."
    ),
    agent=researcher,
)


# Task 2: Write the newsletter using Task 1's output
write = Task(
    description=(
        "Use only the research provided by the Researcher in the context. "
        "Create a technology newsletter with exactly five non-empty lines. "
        "Line 1: a short newsletter headline. "
        "Lines 2-4: one concise bullet for each of the three researched stories. "
        "Line 5: 'Why it matters:' followed by one concise sentence connecting "
        "the developments or explaining their broader significance. "
        "Do not add an introduction, conclusion, extra blank lines, or a "
        "sixth line. Do not invent details."
    ),
    expected_output=(
        "Exactly five non-empty lines: one headline, three numbered story "
        "lines, and one 'Why it matters:' line. Each story line briefly "
        "summarizes one researched story. No extra text."
    ),
    agent=writer,
    context=[find],
)

# Execute tasks in order
crew = Crew(
    agents=[researcher, writer],
    tasks=[find, write],
    process=Process.sequential,
    verbose=True,
)


if __name__ == "__main__":
    result = crew.kickoff()

    print("\n" + "=" * 50)
    print("RESEARCHER OUTPUT")
    print("=" * 50)
    print(find.output)
    with open("research_output.txt", "w", encoding="utf-8") as file:
        file.write(str(find.output))

    print("\n" + "=" * 50)
    print("TECH IN 5 LINES")
    print("=" * 50)
    print(result)
