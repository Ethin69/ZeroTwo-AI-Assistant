import sys
import os
import threading
import base64
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.ai_engine import generate_response, listen_microphone, stop_speaking, speak

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
            background: rgba(255,255,255,0.98);
            padding: 2rem;
            border-radius: 18px;
            margin-left: 420px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# ---------------- Sidebar ----------------
st.sidebar.title("⚙ ZeroTwo Control Panel")

mode = st.sidebar.selectbox(
    "Assistant Mode",
    ["Study Planner", "Concept Explainer", "Coding Assistant", "Chill Mode"]
)

voice_mode = st.sidebar.toggle("Voice Mode", False)

voice_button = st.sidebar.button(
    "🎤 Speak to ZeroTwo",
    disabled=not voice_mode
)

# 🔇 Stop voice button
stop_voice = st.sidebar.button("🔇 Stop Voice")

if stop_voice:
    stop_speaking()

if st.sidebar.button("Reset Chat"):
    st.session_state.messages = []

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
st.write("Your playful study partner.")

name = st.text_input("What should ZeroTwo call you?", "Darling")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add mode message to chat
if mode_message:
    st.session_state.messages.append({
        "role": "assistant",
        "content": mode_message
    })

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Text input
user_input = st.chat_input("Ask ZeroTwo something...")

# 🎤 Voice input
if voice_mode and voice_button:

    with st.spinner("🎤 ZeroTwo is listening..."):
        spoken_text = listen_microphone()

    if spoken_text:
        st.info(f"🎤 You said: {spoken_text}")
        user_input = spoken_text
    else:
        st.warning("I couldn't hear you clearly, Darling. Try again.")

# ---------------- Process message ----------------
if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    reply = generate_response(user_input, name, mode)

    # ✨ Typing Animation
    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        full_text = ""

        for char in reply:
            full_text += char
            message_placeholder.markdown(full_text)
            time.sleep(0.01)

    # Voice in background
    if voice_mode:
        threading.Thread(target=speak, args=(reply,), daemon=True).start()

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })