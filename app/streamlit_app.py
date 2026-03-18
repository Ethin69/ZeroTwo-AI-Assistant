import sys
import os
import base64
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.ai_engine import generate_response

st.set_page_config(page_title="ZeroTwo AI", page_icon="❤️")

# ---------------- Background Styling ----------------
def set_background():

    image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "zerotwo_bg.png")

    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            background: rgba(255,255,255,0.85);
            backdrop-filter: blur(12px);
            padding: 2rem;
            border-radius: 20px;
            margin-left: 300px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }}

        h1, h2, h3 {{
            font-weight: 600;
        }}

        p {{
            font-size: 15px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# ---------------- Header Banner ----------------
st.image("assets/zerotwo_banner.png", use_container_width=True)

# ---------------- Sidebar ----------------
st.sidebar.title("⚙ ZeroTwo Control Panel")

mode = st.sidebar.selectbox(
    "Assistant Mode",
    ["Study Planner", "Concept Explainer", "Coding Assistant", "Chill Mode"]
)

if st.sidebar.button("Reset Chat"):
    st.session_state.messages = []

# Creator Section
st.sidebar.markdown("---")
st.sidebar.subheader("👨‍💻 Creator")
st.sidebar.write("Saiyan")
st.sidebar.caption("AI Engineering Student")
st.sidebar.caption("Building AI companions 🚀")

# ---------------- Mode Change Detection ----------------
if "last_mode" not in st.session_state:
    st.session_state.last_mode = mode

mode_message = None

if mode != st.session_state.last_mode:

    if mode == "Study Planner":
        mode_message = "📚 Darling, what subject should we conquer today?"

    elif mode == "Concept Explainer":
        mode_message = "🧠 Tell me a concept, Darling. I'll explain it clearly."

    elif mode == "Coding Assistant":
        mode_message = "💻 Ready to code, Darling? Show me the problem."

    elif mode == "Chill Mode":
        mode_message = "😌 Finally relaxing, Darling. What should we talk about?"

    st.session_state.last_mode = mode

# ---------------- Main UI ----------------
st.title("❤️ ZeroTwo AI Companion")
st.write("Your intelligent AI companion for learning, coding, and productivity.")

name = st.text_input("What should ZeroTwo call you?", "Darling")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Darling 💖 I'm ZeroTwo, your AI companion created by Saiyan. What shall we explore today?"
        }
    ]

# Add mode message
if mode_message:
    st.session_state.messages.append({
        "role": "assistant",
        "content": mode_message
    })

# ---------------- Display chat with avatars ----------------
for msg in st.session_state.messages:

    if msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="assets/zerotwo_avatar.png"):
            st.write(msg["content"])
    else:
        with st.chat_message("user", avatar="🧑"):
            st.write(msg["content"])

# Input
user_input = st.chat_input("Ask ZeroTwo something...")

# ---------------- Process message ----------------
if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user", avatar="🧑"):
        st.write(user_input)

    reply = generate_response(user_input, name, mode)

    # 🔥 Typing animation + avatar
    with st.chat_message("assistant", avatar="assets/zerotwo_avatar.png"):

        message_placeholder = st.empty()
        full_text = ""

        for char in reply:
            full_text += char
            message_placeholder.markdown(full_text)
            time.sleep(0.005)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })