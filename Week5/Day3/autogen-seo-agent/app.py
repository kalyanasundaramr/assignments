import time
import asyncio
import streamlit as st

from workflows.seo_workflow import run_seo_workflow

import re


def extract_seo_scores(review_report: str) -> dict:
    """
    Extract category scores from the Reviewer Agent's
    Markdown review report.
    """

    categories = {
        "Content Quality": r"Content Quality",
        "SEO Optimization": r"SEO Optimization",
        "Readability": r"Readability",
        "Accuracy": r"Accuracy",
        "Structure & Engagement": (
            r"Structure\s*(?:and|&)\s*Engagement"
        ),
    }

    scores = {}

    for category, pattern in categories.items():
        match = re.search(
            rf"{pattern}\s*:\s*(\d{{1,2}})\s*/\s*20\b",
            review_report,
            flags=re.IGNORECASE,
        )

        if match:
            value = int(match.group(1))
            if 0 <= value <= 20:
                scores[category] = value

    return scores


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SEO AI Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------


st.markdown(
    """
    <style>
    /* Global typography and layout */
    .stApp {
        background: #0B1220;
        color: #F1F5F9;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Readable headings and paragraphs */
    h1, h2, h3, h4, p {
        color: #F1F5F9;
    }

    h1 {
        font-weight: 800;
        letter-spacing: -1px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111C30;
        border-right: 1px solid #26354B;
    }

    section[data-testid="stSidebar"] * {
        color: #E2E8F0;
    }

    /* Form containers */
    div[data-testid="stForm"] {
        background: #131F33;
        border: 1px solid #2C3C54;
        border-radius: 18px;
        padding: 24px;
    }

    /* Input labels */
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #CBD5E1 !important;
        font-weight: 600;
    }

    /* Text inputs */
    div[data-testid="stTextInput"] input {
        background: #1E2B42;
        color: #F8FAFC;
        border: 1px solid #40516A;
        border-radius: 10px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #172338;
        border: 1px solid #30415B;
        border-radius: 16px;
        padding: 22px;
        min-height: 125px;
    }

    div[data-testid="stMetricLabel"] p {
        color: #A5B4C8 !important;
        font-size: 14px;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 800;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #CBD5E1 !important;
        font-weight: 600;
        padding: 12px 18px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #A5B4FC !important;
        border-bottom: 2px solid #818CF8;
    }

    /* Primary buttons */
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(
            90deg, #4F46E5, #7C3AED
        );
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        min-height: 48px;
        font-weight: 700;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {
        background: #6366F1;
        color: #FFFFFF !important;
    }

    /* Download buttons */
    div.stDownloadButton > button {
        background: #253650;
        color: #F8FAFC;
        border: 1px solid #475569;
        border-radius: 10px;
    }

    /* Expander panels */
    div[data-testid="stExpander"] {
        background: #172338;
        border: 1px solid #30415B;
        border-radius: 12px;
    }

    /* Dividers */
    hr {
        border-color: #30415B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.title("🚀 SEO AI Studio")
    st.caption("AutoGen Multi-Agent Platform")

    st.divider()

    st.subheader("AI Agents")

    st.markdown("🔎 Research Agent")
    st.markdown("✍️ Content Writer Agent")
    st.markdown("📈 SEO Optimization Agent")
    st.markdown("✅ Content Reviewer Agent")

    st.divider()

    st.info(
        "Powered by Microsoft AutoGen, "
        "OpenAI GPT-4o-mini, DuckDuckGo, "
        "and Streamlit."
    )


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🚀 AI-Powered SEO Content Generator")

st.markdown(
    """
    Generate research-backed, SEO-friendly content
    using four specialized AI agents.
    """
)

st.divider()


# --------------------------------------------------
# Input Form
# --------------------------------------------------

st.subheader("📝 Content Configuration")

with st.form("seo_form"):

    topic = st.text_input(
        "Content Topic",
        placeholder=(
            "Example: Best AI Tools "
            "for Small Businesses in 2026"
        ),
    )

    col1, col2 = st.columns(2)

    with col1:
        audience = st.text_input(
            "Target Audience",
            value="Small Business Owners",
        )

    with col2:
        word_count = st.selectbox(
            "Article Length",
            options=[500, 800, 1200, 1500, 2000],
            index=1,
        )

    submitted = st.form_submit_button(
        "🚀 Generate SEO Content",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# Execute Multi-Agent Workflow
# --------------------------------------------------


# --------------------------------------------------
# Execute Multi-Agent Workflow with Live Progress
# --------------------------------------------------

if submitted:
 
    if not topic.strip():
        st.warning("Please enter a content topic.")

    else:
       
        st.markdown("### 🤖 Agent Execution Monitor")

        progress_bar = st.progress(0)
        
        stage_placeholder = st.empty()
        message_placeholder = st.empty()

        agent_names = [
            "Research Agent",
            "Content Writer Agent",
            "SEO Optimization Agent",
            "Content Reviewer Agent",
        ]

        agent_status = {
            name: "Waiting" for name in agent_names
        }

        agent_details = st.empty()

        def update_progress(stage, message, percentage):
            progress_bar.progress(
                max(0, min(100, int(percentage)))
            )

            stage_placeholder.markdown(
                f"**Current stage:** {stage}"
            )

            message_placeholder.info(message)

            
            if stage in agent_status:
                current_index = agent_names.index(stage)

                # Mark all previous agents as completed
                for previous_agent in agent_names[:current_index]:
                    agent_status[previous_agent] = "Completed"

                # Mark the current agent as running
                agent_status[stage] = "Running"


            elif stage.startswith("SEO Revision"):
                agent_status["SEO Optimization Agent"] = (
                    "Revising"
                )

            elif stage.startswith("Review "):
                agent_status["Content Reviewer Agent"] = (
                    "Reviewing"
                )

            elif stage == "Completed":
                for name in agent_status:
                    agent_status[name] = "Completed"

            
            with agent_details.container():
                cols = st.columns(2, gap="medium")

                for index, name in enumerate(agent_names):
                    current_status = agent_status[name]

                    if current_status == "Completed":
                        status_icon = "✅"
                        status_color = "#34D399"
                    elif current_status in ("Running", "Revising", "Reviewing"):
                        status_icon = "🔄"
                        status_color = "#A5B4FC"
                    else:
                        status_icon = "⏳"
                        status_color = "#94A3B8"

                    agent_icons = {
                        "Research Agent": "🔎",
                        "Content Writer Agent": "✍️",
                        "SEO Optimization Agent": "📈",
                        "Content Reviewer Agent": "🛡️",
                    }

                    agent_descriptions = {
                        "Research Agent": "Web research and keyword discovery",
                        "Content Writer Agent": "SEO-focused article creation",
                        "SEO Optimization Agent": "Metadata and content optimization",
                        "Content Reviewer Agent": "Quality assurance and approval",
                    }

                    with cols[index % 2]:
                        st.markdown(
                            f"""
                            <div style="
                                background:#172338;
                                border:1px solid #30415B;
                                border-radius:16px;
                                padding:20px;
                                margin-bottom:12px;
                                min-height:140px;
                            ">
                                <div style="
                                    font-size:16px;
                                    font-weight:700;
                                    color:#F8FAFC;
                                ">
                                    {agent_icons[name]} {name}
                                </div>
                                <div style="
                                    color:#94A3B8;
                                    font-size:13px;
                                    margin-top:8px;
                                ">
                                    {agent_descriptions[name]}
                                </div>
                                <div style="
                                    color:{status_color};
                                    font-weight:600;
                                    margin-top:16px;
                                ">
                                    {status_icon} {current_status}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )


        
        try:
            
            start_time = time.perf_counter()
 
            result = asyncio.run(
                run_seo_workflow(
                    topic=topic.strip(),
                    audience=audience.strip() or "General audience",
                    word_count=word_count,
                    progress_callback=update_progress,
                )
            )

            execution_time = time.perf_counter() - start_time

            result["execution_time"] = round(execution_time, 2)

            st.session_state["seo_result"] = result

        except Exception as error:
            st.error(f"Error executing workflow: {error}")


# --------------------------------------------------
# Results Dashboard
# --------------------------------------------------

if "seo_result" in st.session_state:

    result = st.session_state["seo_result"]

    
    # ----------------------------------------------
    # Workflow Execution Summary
    # ----------------------------------------------

    st.markdown("### 📊 Workflow Execution Summary")

    decision = result.get("decision", "UNKNOWN")
    execution_time = result.get("execution_time")
    revision_count = result.get("revision_count", 0)

    final_article = result.get("optimized_article", "")
    article_word_count = len(final_article.split())

    summary_col1, summary_col2, summary_col3, summary_col4 = (
        st.columns(4, gap="medium")
    )

    with summary_col1:
        st.metric(
            "Approval Status",
            decision.replace("_", " ").title(),
        )

    with summary_col2:
        st.metric(
            "Execution Time",
            (
                f"{execution_time:.1f} sec"
                if execution_time is not None
                else "N/A"
            ),
        )

    with summary_col3:
        st.metric(
            "Revision Attempts",
            revision_count,
        )

    with summary_col4:
        st.metric(
            "Final Article Words",
            f"{article_word_count:,}",
        )

    if decision == "APPROVED":
        st.success(
            "✅ Article approved by the AI Content Reviewer."
        )
    elif decision == "REVISION_REQUIRED":
        st.warning(
            "⚠️ Article requires further editorial review."
        )
    else:
        st.info(f"Review status: {decision}")


    st.divider()

    st.subheader("📊 Generated Content Dashboard")

    
    # ----------------------------------------------
    # SEO Quality Scorecard
    # ----------------------------------------------

    scores = extract_seo_scores(result["review"])

    st.markdown("### 🎯 SEO Quality Scorecard")

    if len(scores) == 5:

        total_score = sum(scores.values())

       
        # Overall AI Editorial Quality Score
        total_score = sum(scores.values())

        st.metric(
            "Overall Editorial Quality Score",
            f"{total_score}/100",
        )

        st.caption(
            "AI Reviewer assessment across five quality "
            "categories. This is not a Google ranking score."
        )

        st.markdown("#### 📈 Quality Breakdown")

        left_col, right_col = st.columns(2)

        score_items = list(scores.items())

        with left_col:
            for category, score in score_items[:3]:
                st.markdown(f"**{category}: {score}/20**")
                st.progress(score / 20)

        with right_col:
            for category, score in score_items[3:]:
                st.markdown(f"**{category}: {score}/20**")
                st.progress(score / 20)

    else:
        st.info(
            "SEO category scores could not be fully "
            "extracted from the review report."
        )

    
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🔎 Research",
            "✍️ Article",
            "📈 SEO Optimization",
            "✅ Review Report",
        ]
    )

    with tab1:
        st.subheader("Research Agent Output")
        st.markdown(result["research"])

    with tab2:
        st.subheader("Content Writer Output")
        st.markdown(result["article"])

    with tab3:
        st.subheader("SEO Optimized Content")
        st.markdown(result["optimized_article"])

        st.download_button(
            label="⬇️ Download SEO Article",
            data=result["optimized_article"],
            file_name="seo_optimized_article.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab4:
        st.subheader("Content Review Report")
        st.markdown(result["review"])

        st.download_button(
            label="⬇️ Download Review Report",
            data=result["review"],
            file_name="seo_review_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

        
        # ---------------------------------------
        # Review History
        # ---------------------------------------

        st.divider()
        st.markdown("### 🔄 Review & Revision History")

        review_history = result.get(
            "review_history",
            [result["review"]]
        )

        revision_count = result.get(
            "revision_count",
            0
        )

        st.caption(
            f"Total reviews: {len(review_history)} | "
            f"Revisions performed: {revision_count}"
        )

        for index, report in enumerate(review_history):

            review_scores = extract_seo_scores(report)

            total_score = (
                sum(review_scores.values())
                if len(review_scores) == 5
                else None
            )

            if index == 0:
                review_title = "Initial Review"
            else:
                review_title = f"Review After Revision {index}"

            score_label = (
                f"{total_score}/100"
                if total_score is not None
                else "Score unavailable"
            )

            with st.expander(
                f"📋 {review_title} — {score_label}",
                expanded=(
                    index == len(review_history) - 1
                ),
            ):

                if total_score is not None:
                    st.metric(
                        "Editorial Quality Score",
                        f"{total_score}/100"
                    )

                st.markdown(report)

