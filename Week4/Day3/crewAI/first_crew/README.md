## Week 4 – Day 3: CrewAI Travel Planner Agent

### Objective
Built a travel planning agent using CrewAI that recommends exactly three places to visit in a user-selected city.

### Implementation
- Created a Travel Planner agent with a role, goal, and backstory.
- Defined one task with a clear description and expected output.
- Assembled the agent and task into a Crew.
- Used `crew.kickoff()` to execute the task.
- Loaded the OpenAI API key and model configuration from `.env` using `python-dotenv`.
- Used `verbose=True` to display the agent's execution details.

### Testing
Ran the script with three cities:
- Chennai
- Jaipur
- Mumbai

Verified that the agent generated three relevant travel suggestions with a reason to visit and a practical tip for each place.

### Key Learnings
- How to create a CrewAI Agent, Task, and Crew.
- How agent roles, goals, and backstories guide outputs.
- How task descriptions and expected outputs control response structure.
- How to pass user input into a task using `crew.kickoff(inputs={...})`.
- How to keep API credentials in environment variables.

### Run the Project
```powershell
python travel_planner.py
```

### Security
The OpenAI API key is stored in `.env` and must not be committed to GitHub.