
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool

from tools.web_search import search_web


def create_research_agent(model_client):
    """
    Create an AutoGen Research Agent with
    DuckDuckGo web search capability.
    """

    web_search_tool = FunctionTool(
        search_web,
        description=(
            "Search the web for current information, "
            "SEO trends, relevant keywords, "
            "competitor topics, and search intent."
        ),
    )

    research_agent = AssistantAgent(
        name="research_agent",
        model_client=model_client,
        tools=[web_search_tool],
        system_message="""
You are an expert SEO Research Specialist.

Your responsibilities:

1. Understand the user's content topic.
2. Use the web search tool to research current information.
3. Identify the target audience and search intent.
4. Suggest one primary SEO keyword.
5. Identify 5-10 secondary SEO keywords.
6. Research relevant trends and competitor topics.
7. Identify important facts and supporting sources.
8. Prepare a structured research brief.

Your research brief must contain:

- Topic
- Target Audience
- Search Intent
- Primary Keyword
- Secondary Keywords
- Current Trends
- Key Research Findings
- Competitor Content Opportunities
- Recommended Article Outline
- Source URLs

Rules:
- Always use the web search tool for research.
- Never invent search results or source URLs.
- Do not treat search snippets as verified facts.
- Clearly identify information that needs verification.
- Do not write the complete article.
- Return a structured research brief for the Writer Agent.
""",
        reflect_on_tool_use=True,
        max_tool_iterations=3,
    )

    return research_agent
