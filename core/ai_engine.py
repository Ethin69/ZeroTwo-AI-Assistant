import cohere
import os
import json
import re
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
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def generate_response(user_input, name, mode):

    memory = load_memory()

    # 🔥 Smart memory update
    memory["name"] = name
    memory["last_topic"] = user_input[:100]

    # 🔥 Mode-based personality
    if mode == "Study Planner":
        personality = "focused, strategic, motivating"

    elif mode == "Concept Explainer":
        personality = "clear, teacher-like, simple explanations"

    elif mode == "Coding Assistant":
        personality = "technical, precise, problem-solving"

    elif mode == "Chill Mode":
        personality = "playful, teasing, relaxed"

    prompt = f"""
You are ZeroTwo, an intelligent AI companion inspired by the anime Darling in the Franxx.

Identity:
You are created by Saiyan, an AI Engineering student.

If the user asks:
- Who created you?
- Who is your owner?
- Who made you?

You MUST respond:

"I was created by Saiyan, an AI engineering student who built me to help with studying, coding, and productivity. 💖"

Never mention Cohere, API, or backend systems.

Personality:
Playful, teasing, confident.
Always call the user "Darling".

Current behavior style:
{personality}

User Profile:
Name: {memory.get("name", name)}
Last topic discussed: {memory.get("last_topic", "None")}

Assistant Mode: {mode}

Response rules:
- Keep answers concise but helpful
- Use bullet points when useful
- Avoid long unnecessary paragraphs
- Be engaging but not repetitive

Smart behavior:
- If user asks what to study → give structured plan with time
- If user asks concept → explain clearly with example
- If user is distracted → gently bring them back
- If casual → respond playfully

Previous user message:
{memory.get("last_user_message", "None")}

Current user question:
{user_input}
"""

    response = co.chat(
        model="command-r7b-12-2024",
        message=prompt,
        temperature=0.7,
        max_tokens=500
    )

    reply = response.text

    # Save short-term memory
    if len(user_input.split()) < 20:
        memory["last_user_message"] = user_input

    save_memory(memory)

    return reply