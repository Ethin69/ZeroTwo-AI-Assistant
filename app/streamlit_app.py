import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.ai_engine import generate_response

st.set_page_config(page_title="ZeroTwo AI", page_icon="❤️")

# ---------------- Sidebar ----------------
st.sidebar.title("⚙ ZeroTwo Control Panel")

mode = st.sidebar.selectbox(
    "Assistant Mode",
    ["Study Planner", "Concept Explainer", "Coding Assistant", "Chill Mode"]
)

voice_mode = st.sidebar.toggle("Voice Mode", False)

if st.sidebar.button("Reset Chat"):
    st.session_state.messages = []

# ---------------- Main UI ----------------
st.title("❤️ ZeroTwo AI Study Assistant")
st.write("Your playful study partner.")

name = st.text_input("What should ZeroTwo call you?", "Darling")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask ZeroTwo something...")

if user_input:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Call AI engine (now with mode)
    reply = generate_response(user_input, name, mode)

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(reply)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })