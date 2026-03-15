# ❤️ ZeroTwo AI Companion

ZeroTwo AI Companion is an AI-powered study assistant inspired by the character **ZeroTwo from *Darling in the Franxx***.
It helps students with **studying, coding, explaining concepts, and productivity**, while maintaining a playful AI personality.

The application is built using **Streamlit** and integrates an **LLM (Cohere)** to generate intelligent responses.

---

## 🌐 Live Demo

Try the deployed application:

https://zerotwo-ai-companion.streamlit.app

---

## ✨ Features

### 🤖 AI Assistant

* Intelligent responses powered by **Cohere LLM**
* Friendly **ZeroTwo-inspired personality**
* Calls the user **“Darling”** during conversations

### 📚 Multiple Assistant Modes

Switch between different modes depending on your needs:

* **Study Planner** → Generates structured study plans
* **Concept Explainer** → Explains technical topics clearly
* **Coding Assistant** → Helps with programming and debugging
* **Chill Mode** → Casual conversation mode

### 🧠 Persistent Memory

The assistant remembers previous user interactions using a **JSON memory system**, allowing more contextual responses.

### 🎤 Voice Interaction

* Voice input using **Speech Recognition**
* AI responses can be spoken using **Neural Text-to-Speech**

### 🎨 Modern UI

* Custom **anime-themed interface**
* **ZeroTwo background**
* Clean **chat interface**
* Typing-style response animation

### ☁️ Cloud Deployment

The app is deployed on **Streamlit Cloud** so it can be accessed from anywhere.

---

## 🏗️ Project Architecture

```
ZeroTwo-AI/
│
├── app/
│   └── streamlit_app.py        # Streamlit UI
│
├── core/
│   └── ai_engine.py            # AI logic and LLM integration
│
├── assets/
│   └── zerotwo_bg.png          # UI background image
│
├── data/
│   └── memory.json             # Persistent memory storage
│
├── requirements.txt            # Project dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

* **Python**
* **Streamlit**
* **Cohere LLM API**
* **SpeechRecognition**
* **Edge-TTS**
* **JSON memory system**

---

## 🚀 Installation (Local Setup)

Clone the repository:

```bash
git clone https://github.com/yourusername/zerotwo-ai-companion.git
cd zerotwo-ai-companion
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
COHERE_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app/streamlit_app.py
```

---

## 🔐 Environment Variables

The application requires a **Cohere API key**.

```
COHERE_API_KEY=your_api_key_here
```

For deployment on Streamlit Cloud, add this key under **App Secrets**.

---

## 🎯 Future Improvements

Planned upgrades include:

* Long-term vector memory
* Better conversational context
* Advanced voice system
* AI tool integrations
* Local LLM support

---

## 👨‍💻 Author

**Ethin**

AI Engineering Student interested in building intelligent systems, AI companions, and creative AI products.

---

## ⭐ Inspiration

Inspired by the character **ZeroTwo** from *Darling in the Franxx* and the idea of creating an AI companion that helps with learning and productivity.

---

## 📜 License

This project is for educational and portfolio purposes.
