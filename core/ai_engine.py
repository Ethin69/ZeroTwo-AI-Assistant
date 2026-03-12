import cohere
import os
import json
import pyttsx3
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(API_KEY)

MEMORY_FILE = "data/memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    # Try to use a female voice if available
    if len(voices) > 1:
        engine.setProperty("voice", voices[1].id)

    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()


def generate_response(user_input, name, mode, voice_mode):

    memory = load_memory()

    prompt = f"""
You are ZeroTwo from the anime Darling in the Franxx.

Personality:
Playful, teasing, confident.
Always call the user Darling.

User name: {name}

Assistant Mode: {mode}

Behavior rules based on mode:

Study Planner:
Generate structured study plans and task breakdowns.

Concept Explainer:
Explain technical or academic concepts clearly with examples.

Coding Assistant:
Help with programming, debugging, and algorithms.

Chill Mode:
Respond casually and playfully like ZeroTwo.

Always remain helpful and concise while maintaining ZeroTwo's personality.

Previous user message: {memory.get("last_user_message", "None")}

User question:
{user_input}
"""

    response = co.chat(
        model="command-r7b-12-2024",
        message=prompt,
        temperature=0.7,
        max_tokens=200
    )

    reply = response.text

    # Speak only if voice mode is ON
    if voice_mode:
        speak(reply)

    # Save memory
    memory["last_user_message"] = user_input
    save_memory(memory)

    return reply