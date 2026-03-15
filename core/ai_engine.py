import cohere
import os
import json
import speech_recognition as sr
import re
import asyncio
import edge_tts
from dotenv import load_dotenv
from playsound import playsound

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


# 🔊 Voice generation
async def edge_speak(text):

    # Clean markdown
    cleaned_text = re.sub(r"\*+", "", text)
    cleaned_text = re.sub(r"#+", "", cleaned_text)
    cleaned_text = re.sub(r"\d+\.", "", cleaned_text)

    # remove awkward punctuation
    cleaned_text = re.sub(r"[:;()\[\]{}]", "", cleaned_text)

    # convert line breaks to pauses
    cleaned_text = cleaned_text.replace("\n", ". ")

    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    communicate = edge_tts.Communicate(
        text=cleaned_text,
        voice="en-US-JennyNeural",
        rate="+6%",
        pitch="+1Hz"
    )

    await communicate.save("voice.mp3")


def speak(text):

    try:

        asyncio.run(edge_speak(text))

        playsound("voice.mp3")

        if os.path.exists("voice.mp3"):
            os.remove("voice.mp3")

    except Exception:
        pass


# 🔇 Stop speaking (not needed anymore but kept for compatibility)
def stop_speaking():
    pass


# 🎤 Voice input
def listen_microphone():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening... Speak now")

        recognizer.adjust_for_ambient_noise(source)

        try:

            audio = recognizer.listen(source, timeout=5)

            text = recognizer.recognize_google(audio)

            print("You said:", text)

            return text

        except sr.WaitTimeoutError:
            return None

        except sr.UnknownValueError:
            return None

        except sr.RequestError:
            return None


def generate_response(user_input, name, mode):

    memory = load_memory()

    prompt = f"""
You are ZeroTwo, an intelligent AI companion inspired by the anime Darling in the Franxx.
You help with studying, coding, learning, and conversation.

Personality:
Playful, teasing, confident.
Always call the user "Darling".

User name: {name}

Assistant Mode: {mode}

Important rules:
1. Always respond to the CURRENT user question.
2. Do NOT continue older topics unless the user clearly asks about them again.
3. Use previous context only if it is relevant to the current question.
4. Keep answers concise, helpful, and slightly playful like ZeroTwo.

Assistant Modes:

Study Planner:
Create structured study plans and task breakdowns.

Concept Explainer:
Explain technical or academic concepts clearly with examples.

Coding Assistant:
Help with programming, debugging, and algorithms.

Chill Mode:
Respond casually and playfully.

Previous user message (reference only):
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

    if len(user_input.split()) < 20:
        memory["last_user_message"] = user_input
        save_memory(memory)

    return reply