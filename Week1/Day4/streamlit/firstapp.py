import streamlit as st

# Page configuration
st.set_page_config(
    page_title="My First Streamlit App",
    page_icon="🌟",
    layout="centered"
)

# Title
st.title("🌟 My First Streamlit App")

st.header("Welcome to Streamlit!")

st.subheader(
    "This is a simple web application built using Streamlit."
)

st.write(
    "This app demonstrates how to create an interactive "
    "web application using Python and Streamlit."
)

st.markdown(
    "You can use **Markdown** to format text."
)

st.text("This is a simple text component.")

st.code(
    "print('Hello, Streamlit!')",
    language="python"
)

st.divider()

# User Information
st.header("User Information")

# Name
name = st.text_input(
    "Enter your name:",
    placeholder="Enter your name here"
)

# Age
age = st.number_input(
    "Enter your age:",
    min_value=1,
    max_value=100,
    value=18
)

# Checkbox
terms = st.checkbox(
    "I agree to the terms and conditions"
)

# Display message when checkbox is selected
if terms:
    st.success("✅ Thank you for agreeing!")

# Submit button
if st.button("Submit", type="primary"):

    if name == "":
        st.warning("Please enter your name.")

    elif not terms:
        st.warning(
            "Please agree to the terms and conditions."
        )

    else:
        st.success(
            f"Hello, {name}! 👋"
        )

        st.info(
            f"You are {age} years old."
        )

        st.balloons()