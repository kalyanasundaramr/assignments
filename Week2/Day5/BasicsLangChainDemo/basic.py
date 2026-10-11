
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# --------------------------------------------------
# 1. Load environment variables from .env
# --------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="AI Chef Assistant (OpenAI)",
    page_icon="🍳",
    layout="centered",
)

st.title("🍳 Your AI Chef Assistant")
st.caption(
    "Powered by OpenAI | Ask about recipes, ingredients, "
    "cooking tips, and healthy meals."
)

# Check that the API key exists
if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "OPENAI_API_KEY is missing. "
        "Please add your API key to the .env file."
    )
    st.stop()


# --------------------------------------------------
# 2. Initialize LangChain components
# --------------------------------------------------

@st.cache_resource
def init_langchain():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
    )

    prompt_template = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert chef and cooking assistant. "
            "Suggest practical recipes, explain cooking techniques, "
            "recommend ingredient substitutions, and provide "
            "healthy meal ideas. Consider the user's previous "
            "messages when answering. Mention potential allergens "
            "when relevant."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    chain = prompt_template | llm | StrOutputParser()

    return chain


base_chain = init_langchain()


# --------------------------------------------------
# 3. Manage conversation memory
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = InMemoryChatMessageHistory()


def get_session_history(session_id: str):
    # Each browser session uses its own Streamlit history object.
    return st.session_state.chat_history


conversational_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# --------------------------------------------------
# 4. Display previous messages
# --------------------------------------------------

for message in st.session_state.chat_history.messages:
    role = "user" if message.type == "human" else "assistant"

    with st.chat_message(role):
        st.markdown(message.content)


# --------------------------------------------------
# 5. Handle new user input
# --------------------------------------------------

user_input = st.chat_input(
    "What ingredients do you have?"
)

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        config = {
            "configurable": {
                "session_id": "ai_chef_session"
            }
        }

        try:
            response = st.write_stream(
                conversational_chain.stream(
                    {"input": user_input},
                    config=config,
                )
            )

        except Exception as error:
            st.error(
                "Sorry, I could not generate a response. "
                "Check your API key, internet connection, "
                "model access, and API quota."
            )
            st.caption(f"Error details: {error}")


# --------------------------------------------------
# 6. Clear conversation
# --------------------------------------------------

if st.button("Clear conversation"):
    st.session_state.chat_history.clear()
    st.rerun()
