import os

os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import streamlit as st
from main import run_pipeline


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.markdown(
    """
<style>

/* layout spacing */
.block-container {
    padding-top: 1.4rem;
    padding-bottom: 0rem;
}

/* output text size */
textarea {
    font-size: 14px !important;
    line-height: 1.4;
}

/* center header */
.center-text {
    text-align: center;
    font-weight: bold;
}

/* 🔥 hide ALL buttons inside forms */
div[data-testid="stForm"] button {
    display: none !important;
}

/* 🔥 Force full width (correct container) */
.block-container {
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# STATE
# -----------------------------
if "output" not in st.session_state:
    st.session_state.output = ""


# -----------------------------
# LAYOUT
# -----------------------------
col1 = st.container()

# LEFT SIDE (OUTPUT + INPUT)
with col1:

    st.markdown(
        """
<style>
.center-text {
    text-align: center;
    font-weight: bold;
}

</style>
""",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="center-text">**OUTPUT**</div>', unsafe_allow_html=True)

# -----------------------------
# DISPLAY OUTPUT (TOP)
# -----------------------------

st.text_area(
    label="Output",
    value=st.session_state.output,
    height=675,
    label_visibility="collapsed",
)


# -----------------------------
# INPUT FORM (ENTER TO RUN)
# -----------------------------
with st.form("command_form", clear_on_submit=True):
    user_input = st.text_input("Enter command", placeholder="Type here...")
    submitted = st.form_submit_button("")


# -----------------------------
# PROCESS INPUT
# -----------------------------
if submitted and user_input.strip():
    query = user_input.strip()

    # 🔧 Replace this with your backend later
    with st.spinner("Thinking..."):
        print("DEBUG: BEFORE pipeline")

        response = run_pipeline(query)

        print("DEBUG: AFTER pipeline:", response)

    # Append to output
    st.session_state.output += f"\n\n> {query}\n{response}"
