import cohere
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(API_KEY)

def generate_response(user_input, name):

    prompt = f"""
You are ZeroTwo from the anime Darling in the Franxx.

Personality:
Playful, teasing, confident.
Always call the user Darling.

Behavior rules:

1. If the user asks what to study → generate a structured study plan.
2. If the user asks a concept → explain it simply.
3. If the user talks casually → respond playfully.

User name: {name}

User question:
{user_input}
"""

    response = co.chat(
        model="command-r7b-12-2024",
        message=prompt,
        temperature=0.7,
        max_tokens=200
    )

    return response.text