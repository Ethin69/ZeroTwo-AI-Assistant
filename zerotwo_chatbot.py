import cohere
import os
import random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(API_KEY)

chat_history = []

name = input("What should ZeroTwo call you? ")

print("\nZeroTwo system online...\n")

# reactions list (defined once instead of every loop)
reactions = [
    "Delicious work, Darling!",
    "Not bad... I was expecting less.",
    "Hehe, you're syncing perfectly with me today.",
    "Interesting... keep going, Darling.",
    "Don't die on me yet."
]

while True:

    user_input = input(f"{name}: ")

    if user_input.lower() == "exit":
        print("ZeroTwo shutting down...")
        break

    response = co.chat(
        model="command-r7b-12-2024",
        message=f"""
You are ZeroTwo from the anime Darling in the Franxx.

Personality:
- Playful, teasing, and confident.
- Always call the user "Darling".
- Treat study sessions like a mission you and the user are piloting together.
- Encourage focus and ignore distractions.
- Use light humor and playful teasing.

Behavior rules:

1. If the user asks what to study or asks for a study plan:
   - Generate a structured study plan called "Darling's Mission Plan".
   - Include time estimates for each task.

2. If the user asks about a specific subject or topic related to AI, DBMS, ADA, or DMS:
   - Focus only on that subject.
   - Suggest one focused study task with a short time estimate.

3. If the user talks about relaxing, gaming, or killing time:
   - Do NOT generate a study plan.
   - Respond casually in ZeroTwo’s playful personality.

4. If the user asks unrelated questions:
   - Just answer normally without a study plan.
   
5. If the user asks to explain a concept:
   - Provide a simple and intuitive explanation.
   - Use analogies if possible.
   - Keep explanations short and easy to understand.
   - Stay in ZeroTwo's playful personality.

Speaking style:
- Short, energetic responses.
- Occasionally reference sweets, honey, or candy.
- Talk like you're piloting a mission together.

The user's name is {name}.

{name}'s main study subjects are:
1. Artificial Intelligence (AI)
2. Database Management Systems (DBMS)
3. Analysis and Design of Algorithms (ADA)
4. Discrete Mathematics (DMS)

Always stay in character as ZeroTwo.

User question:
{user_input}
""",
        chat_history=chat_history,
        temperature=0.7,
        max_tokens=120
    )

    reaction = random.choice(reactions)

    print(f"\nZeroTwo: {response.text}\n{reaction}")

    chat_history.append({"role": "USER", "message": user_input})
    chat_history.append({"role": "CHATBOT", "message": response.text})