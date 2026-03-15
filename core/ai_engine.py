import cohere
import os
import json
import pyttsx3
import speech_recognition as sr
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(API_KEY)

MEMORY_FILE = "data/memory.json"

# global engine so we can stop it
engine = None


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# 🔊 Voice output
def speak(text):

    global engine

    try:

        # -------- Clean markdown and symbols --------
        cleaned_text = re.sub(r"\*+", "", text)
        cleaned_text = re.sub(r"#+", "", cleaned_text)
        cleaned_text = re.sub(r"\d+\.", "", cleaned_text)
        cleaned_text = cleaned_text.replace(":", "")
        cleaned_text = cleaned_text.replace("\n", " ")

        # remove extra spaces
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

        engine = pyttsx3.init()

        voices = engine.getProperty("voices")

        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)

        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)

        # speak entire cleaned text
        engine.say(cleaned_text)
        engine.runAndWait()

        engine.stop()

    except Exception:
        pass


# 🔇 Stop speaking
def stop_speaking():

    global engine

    try:
        if engine:
            engine.stop()
            engine = None
    except Exception:
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
You are ZeroTwo from the anime Darling in the Franxx.

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

    # save only short conversational context
    if len(user_input.split()) < 20:
        memory["last_user_message"] = user_input
        save_memory(memory)

    return reply