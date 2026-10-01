import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Grade Calculator",
    page_icon="🎓",
    layout="centered"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    .stApp {
        background: linear-gradient(135deg, #f5f7fb, #eef2f7);
    }

    .block-container {
        max-width: 750px;
        padding-top: 45px;
        padding-bottom: 50px;
    }

    /* Header */

    .header {
        text-align: center;
        margin-bottom: 35px;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        color: #172033;
    }

    .subtitle {
        font-size: 16px;
        color: #64748b;
        margin-top: 8px;
    }

    /* Input card */

    .card {
        background: white;
        padding: 28px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 21px;
        font-weight: 700;
        color: #172033;
    }

    .card-description {
        font-size: 14px;
        color: #64748b;
        margin-top: 6px;
    }

    /* Result */

    .result-card {
        background: white;
        padding: 35px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        text-align: center;
        margin-top: 25px;
    }

    .result-label {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #94a3b8;
    }

    .grade {
        font-size: 80px;
        font-weight: 900;
        margin: 10px 0;
    }

    .score {
        font-size: 18px;
        color: #374151;
    }

    .feedback {
        color: #64748b;
        margin-top: 8px;
    }

    /* Grading scale */

    .scale-title {
        font-size: 21px;
        font-weight: 700;
        color: #172033;
        margin-top: 35px;
        margin-bottom: 15px;
    }

    .scale-item {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 13px 18px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
    }

    .scale-range {
        color: #475569;
    }

    .scale-grade {
        font-weight: 800;
    }

    /* Footer */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-top: 35px;
    }

    /* Button */

    div.stButton > button {
        width: 100%;
        height: 48px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 700;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="header">'
    '<div class="title">🎓 Grade Calculator</div>'
    '<div class="subtitle">'
    'Enter your mark and discover your grade instantly.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# INPUT CARD
# --------------------------------------------------

st.markdown(
    '<div class="card">'
    '<div class="card-title">📝 Enter Your Mark</div>'
    '<div class="card-description">'
    'Enter a score between 0 and 100.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# FORM
# --------------------------------------------------

with st.form("grade_form"):

    # IMPORTANT:
    # This is a native Streamlit input.
    # Do not hide the label or modify it with CSS.

    mark = st.number_input(
        "Mark",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0,
        help="Enter a number from 0 to 100."
    )

    submitted = st.form_submit_button(
        "✨ Calculate My Grade"
    )


# --------------------------------------------------
# CALCULATE GRADE
# --------------------------------------------------

if submitted:

    if mark >= 90:
        grade = "A"
        color = "#16a34a"
        feedback = "Outstanding! Keep up the excellent work."

    elif mark >= 80:
        grade = "B"
        color = "#2563eb"
        feedback = "Great job! You are doing very well."

    elif mark >= 70:
        grade = "C"
        color = "#ca8a04"
        feedback = "Good work! There is still room to improve."

    elif mark >= 60:
        grade = "D"
        color = "#ea580c"
        feedback = "You passed. Keep working to improve."

    else:
        grade = "E"
        color = "#dc2626"
        feedback = "Keep practicing. You can improve your score."


    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    st.markdown(
        '<div class="result-card">'
        '<div class="result-label">YOUR RESULT</div>'
        f'<div class="grade" style="color:{color};">'
        f'{grade}'
        '</div>'
        f'<div class="score">'
        f'You scored <strong>{mark:g}</strong> out of <strong>100</strong>'
        '</div>'
        f'<div class="feedback">{feedback}</div>'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # SCORE BAR
    # --------------------------------------------------

    st.write("**📊 Your Score**")

    st.progress(int(mark))

    st.caption(f"{mark:g}%")



# --------------------------------------------------
# GRADING SCALE
# --------------------------------------------------

st.markdown(
    '<div class="scale-title">📊 Grading Scale</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="scale-item">'
    '<span class="scale-range">90 – 100</span>'
    '<span class="scale-grade" style="color:#16a34a;">A</span>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="scale-item">'
    '<span class="scale-range">80 – 89</span>'
    '<span class="scale-grade" style="color:#2563eb;">B</span>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="scale-item">'
    '<span class="scale-range">70 – 79</span>'
    '<span class="scale-grade" style="color:#ca8a04;">C</span>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="scale-item">'
    '<span class="scale-range">60 – 69</span>'
    '<span class="scale-grade" style="color:#ea580c;">D</span>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="scale-item">'
    '<span class="scale-range">Below 60</span>'
    '<span class="scale-grade" style="color:#dc2626;">E</span>'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="footer">'
    '🎓 Grade Calculator • Built with Streamlit'
    '</div>',
    unsafe_allow_html=True
)