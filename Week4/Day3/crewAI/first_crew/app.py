import streamlit as st
from crewai.project import load_crew
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CrewAI LinkedIn Writer",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ CrewAI LinkedIn Content Writer")
st.write(
    "Enter a topic and let your AI Researcher and "
    "LinkedIn Content Writer create a post for you."
)

topic = st.text_area(
    "What topic should the agents work on?",
    placeholder="Example: AI in logistics and supply chain management",
    height=100,
)

if st.button("Generate LinkedIn Post", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        try:
            with st.spinner("Your AI agents are working..."):
                crew, _ = load_crew(source="crew.jsonc")
                result = crew.kickoff(inputs={"topic": topic.strip()})

            st.success("LinkedIn post generated!")
            st.subheader("Your LinkedIn Post")
            st.markdown(str(result))
            st.download_button(
                "Download post as text",
                data=str(result),
                file_name="linkedin_post.txt",
                mime="text/plain",
            )
        except Exception as e:
            st.error("The crew could not complete the request.")
            st.exception(e)
