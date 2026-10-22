# CrewAI Multi-Agent LinkedIn Content Writer

## Objective
Built a multi-agent AI workflow using CrewAI to research a topic and generate a professional LinkedIn post.

## Agents
- **AI Researcher:** Researches the given topic and identifies key insights, examples, and practical takeaways.
- **LinkedIn Content Writer:** Uses the research findings to write an engaging LinkedIn post with a hook, key insights, and a closing question.

## Workflow
1. Accept a topic as input.
2. Research the topic using the AI Researcher.
3. Pass the research findings to the LinkedIn Content Writer.
4. Generate the final LinkedIn post.

## Technologies
- Python 3.12
- CrewAI 1.15.28
- OpenAI GPT-4o mini
- JSONC configuration
- Python virtual environment (`venv`)

## Execution
Run the project from the `first_crew` directory with the existing virtual environment activated:

```powershell
crewai run
```

Example topic: `AI in logistics and supply chain management`

## Learning Outcomes
- Created and configured multiple AI agents.
- Defined tasks and assigned them to agents.
- Used sequential task execution to pass research findings between agents.
- Configured an LLM and API key using environment settings.
- Successfully executed a two-agent workflow and generated a LinkedIn post.

## Important Note
Verify factual claims, statistics, and examples against reliable sources before publishing AI-generated content.
