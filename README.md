ZeroTwo: Terminal-Based AI
ZeroTwo is a lightweight, Python-powered assistant designed for the command line. By leveraging the Cohere LLM API, it provides a persistent conversational experience directly in your terminal.

Core Functionality
Contextual Memory: Unlike basic scripts, ZeroTwo tracks conversation history, allowing for multi-turn dialogues and follow-up questions.
Personalized Interaction: Configured to act as a focused assistant rather than a generic search engine.
CLI First: Built for developers who want AI access without leaving their environment.

Technical Setup

The project is built on a streamlined stack for fast deployment and easy iteration:
Language: Python 3.x
Engine: Cohere API (LLM)
Environment: Developed in VS Code; version controlled via Git.

Live Interaction Example
User: My exam is tomorrow.
ZeroTwo: Focus on reviewing key concepts and practicing past papers. You've got this.

Roadmap

I'm currently looking at expanding the utility of the tool with these specific updates:
Streamlit Integration: Moving from the CLI to a clean web dashboard.
Study Planner: A dedicated mode to generate schedules based on syllabi.
Local LLM Support: Implementing Ollama or Llama.cpp to allow the assistant to run 100% offline.