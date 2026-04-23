import streamlit as st
from teach_mode import teach_mode
from main import generate_answer

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="RAG Assistant", layout="wide")

# -----------------------------
# SIDEBAR (controls)
# -----------------------------
st.sidebar.title("Controls")

mode = st.sidebar.radio("Mode", ["teach", "tool"])

# future toggle ready
style = st.sidebar.radio("Style", ["strict", "helpful"])

# -----------------------------
# HEADER
# -----------------------------
st.title("🧠 RAG Assistant")

# -----------------------------
# SESSION STATE (keeps output)
# -----------------------------
if "output" not in st.session_state:
    st.session_state.output = ""

# -----------------------------
# MAIN OUTPUT WINDOW
# -----------------------------
output_container = st.container()

with output_container:
    st.subheader("Output")

    st.text_area(
        label="",
        value=st.session_state.output,
        height=500,  # BIG window
        key="output_box",
    )

# -----------------------------
# INPUT (bottom)
# -----------------------------
st.divider()

query = st.text_area(
    "Enter command",
    height=100,
    placeholder="e.g. explain my tool_validator.py step by step",
)

run = st.button("Run", use_container_width=True)

# -----------------------------
# EXECUTION
# -----------------------------
if run and query.strip():
    system_files = ["tool_validator.py"]

    if mode == "teach":
        result = teach_mode(query, system_files, generate_answer)
    else:
        result = "Tool mode not wired here yet"

    st.session_state.output = result

