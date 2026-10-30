
import os
import re

from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.research_agent import create_research_agent
from agents.writer_agent import create_writer_agent
from agents.seo_agent import create_seo_agent
from agents.reviewer_agent import create_reviewer_agent

load_dotenv()

MAX_REVISIONS = 2


def report_progress(callback, stage, message, progress):
    """
    Report workflow progress to the Streamlit UI.

    Args:
        callback: Optional progress callback function.
        stage: Current agent or workflow stage.
        message: Human-readable progress message.
        progress: Completion percentage (0-100).
    """
    if callback is not None:
        callback(stage, message, progress)

def get_review_decision(review_report: str) -> str:
    """Extract the reviewer's structured final decision."""

    matches = re.findall(
        r"^FINAL_DECISION:\s*(APPROVED|REVISION_REQUIRED)\s*$",
        review_report,
        flags=re.MULTILINE,
    )

    if len(matches) != 1:
        return "REVISION_REQUIRED"

    return matches[0]


async def run_seo_workflow(
    topic: str,
    audience: str = "General audience",
    word_count: int = 800,
    progress_callback=None,
):

    """Run the four-agent SEO workflow with revisions."""

    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    model_client = OpenAIChatCompletionClient(
        model=os.getenv("MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        research_agent = create_research_agent(model_client)
        writer_agent = create_writer_agent(model_client)
        seo_agent = create_seo_agent(model_client)
        reviewer_agent = create_reviewer_agent(model_client)

        # Agent 1: Research
        
        report_progress(
            progress_callback,
            "Research Agent",
            "Searching the web and preparing the research brief...",
            10,
        )
        print("\n[1/4] Research Agent running...")


        research_result = await research_agent.run(
            task=(
                f"Research this SEO topic: {topic}\n"
                f"Target audience: {audience}\n"
                "Identify search intent, keywords, "
                "current trends, sources, and article outline."
            )
        )

        research_brief = research_result.messages[-1].content

        # Agent 2: Writer
        
        report_progress(
            progress_callback,
            "Content Writer Agent",
            "Writing the SEO article using the research brief...",
            35,
        )
        print("\n[2/4] Writer Agent running...")


        writer_result = await writer_agent.run(
            task=(
                f"Write an SEO article about: {topic}\n"
                f"Target audience: {audience}\n"
                f"Target length: {word_count} words\n\n"
                f"Research brief:\n{research_brief}"
            )
        )

        article = writer_result.messages[-1].content

        # Agent 3: SEO Optimization
        
        report_progress(
            progress_callback,
            "SEO Optimization Agent",
            "Optimizing metadata, keywords, headings, and readability...",
            60,
        )
        print("\n[3/4] SEO Agent running...")


        seo_result = await seo_agent.run(
            task=(
                f"Optimize this article for SEO.\n"
                f"Topic: {topic}\n"
                f"Audience: {audience}\n\n"
                f"Research brief:\n{research_brief}\n\n"
                f"Article:\n{article}"
            )
        )

        optimized_article = seo_result.messages[-1].content

        # Agent 4: Initial Review
        
        report_progress(
            progress_callback,
            "Content Reviewer Agent",
            "Evaluating content quality, accuracy, and SEO...",
            80,
        )
        print("\n[4/4] Reviewer Agent running...")


        reviewer_result = await reviewer_agent.run(
            task=(
                f"Review this SEO article.\n"
                f"Topic: {topic}\n"
                f"Audience: {audience}\n\n"
                f"Research brief:\n{research_brief}\n\n"
                f"Optimized article:\n{optimized_article}"
            )
        )

        review_report = reviewer_result.messages[-1].content
        decision = get_review_decision(review_report)

        revision_count = 0
        review_history = [review_report]

        # Automatic Revision Loop
        while (
            decision == "REVISION_REQUIRED"
            and revision_count < MAX_REVISIONS
        ):
            revision_count += 1

            
            report_progress(
                progress_callback,
                f"SEO Revision {revision_count}",
                f"Applying reviewer feedback (revision "
                f"{revision_count} of {MAX_REVISIONS})...",
                min(85 + revision_count * 5, 95),
            )

            print(
                f"\n[REVISION {revision_count}/{MAX_REVISIONS}] "
                "SEO Agent revising content..."
            )


            # Reuse SEO Agent with reviewer feedback
            revision_result = await seo_agent.run(
                task=(
                    "Revise the SEO article using the "
                    "reviewer's feedback.\n\n"
                    f"Topic: {topic}\n"
                    f"Audience: {audience}\n"
                    f"Target length: {word_count} words\n\n"
                    f"Research brief:\n{research_brief}\n\n"
                    f"Current article:\n{optimized_article}\n\n"
                    f"Reviewer feedback:\n{review_report}\n\n"
                    "Fix the identified issues. "
                    "Return the complete revised SEO metadata, "
                    "article, and verification notes."
                )
            )

            optimized_article = revision_result.messages[-1].content

           
            report_progress(
                progress_callback,
                f"Review {revision_count + 1}",
                "Evaluating the revised article...",
                min(88 + revision_count * 5, 98),
            )

            print(
                f"\n[REVIEW {revision_count + 1}] "
                "Reviewer Agent evaluating revised content..."
            )


            reviewer_result = await reviewer_agent.run(
                task=(
                    "Review the latest revised article "
                    "as a complete standalone submission.\n\n"
                    f"Topic: {topic}\n"
                    f"Audience: {audience}\n\n"
                    f"Research brief:\n{research_brief}\n\n"
                    f"Revised article:\n{optimized_article}\n\n"
                    "Apply the original approval criteria. "
                    "Return the complete review report "
                    "with exactly one FINAL_DECISION line."
                )
            )

            review_report = reviewer_result.messages[-1].content
            review_history.append(review_report)
            decision = get_review_decision(review_report)

        report_progress(
            progress_callback,
            "Completed",
            f"Workflow finished: {decision}",
            100,
        )


        print("\n========== WORKFLOW COMPLETED ==========")
        print(f"Final Decision: {decision}")
        print(f"Revisions Performed: {revision_count}")

        return {
            "topic": topic,
            "audience": audience,
            "research": research_brief,
            "article": article,
            "optimized_article": optimized_article,
            "review": review_report,
            "review_history": review_history,
            "decision": decision,
            "revision_count": revision_count,
        }

    finally:
        await model_client.close()
