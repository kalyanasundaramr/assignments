
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# Load API key and model settings from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL", "openai/gpt-4o-mini")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

# Ask the user for a destination
city = input("Which city? ").strip()

if not city:
    raise ValueError("Please enter a city name.")

# Create the Travel Planner agent
planner = Agent(
    role="Travel Planner",
    goal="Recommend exactly three interesting places to visit in the city requested by the user.",
    backstory=(
        "You are an experienced travel planner who helps first-time visitors "
        "discover a city's most worthwhile attractions. You write for travelers "
        "who want practical, concise suggestions, including why each place is "
        "special and one useful visiting tip."
    ),
    llm=LLM(
        model=model_name,
        api_key=api_key,
    ),
    verbose=True,
)

# Create one task for the agent
task = Task(
    description=(
        "Recommend exactly three places to visit in {city}. "
        "Choose relevant attractions and provide a brief reason to visit "
        "and one practical tip for each place. Avoid lengthy introductions."
    ),
    expected_output=(
        "Exactly three numbered suggestions, numbered 1 to 3. "
        "Each suggestion must include the place name, a short reason to visit, "
        "and one practical visiting tip. Do not include a fourth place "
        "or a lengthy introduction or conclusion."
    ),
    agent=planner,
)

# Assemble the crew and run the task
crew = Crew(
    agents=[planner],
    tasks=[task],
    verbose=True,
)

result = crew.kickoff(inputs={"city": city})

print("\n--- TRAVEL PLANNER RECOMMENDATIONS ---")
print(result)
