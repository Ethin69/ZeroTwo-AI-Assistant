import cohere

API_KEY = "8k0iIyzBR8IgKQ83rmEgIwuiNHp3ESVjFpZrew4F"

co = cohere.Client(API_KEY)
chat_history = []

name = input("What should ZeroTwo call you? ")

print("\nZeroTwo system online...\n")

while True:

    user_input = input(f"{name}: ")

    if user_input.lower() == "exit":
        print("ZeroTwo shutting down...")
        break

    response = co.chat(
        model="command-r7b-12-2024",
        message=f"""
You are ZeroTwo, a tactical AI assistant.

Speak concisely.
Call the user {name}.
Help with studying, productivity, and planning.

User question:
{user_input}
""",
chat_history=chat_history,
        temperature=0.7,
        max_tokens=120
    )

    print("\nZeroTwo:", response.text)
    chat_history.append({"role": "USER", "message": user_input})
    chat_history.append({"role": "CHATBOT", "message": response.text})