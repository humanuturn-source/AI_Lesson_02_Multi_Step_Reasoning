Install Instructions
AI Lesson 01: AI Agent
The following intructions are for MAC

Step 1: Prerequisites
Before starting, ensure you have the following installed on your system:

Package Manager: Homebrew
Python: Python 3.10 or higher (python3 --version)
Step 2: Install & Start Ollama
Install Ollama via Homebrew:

brew install ollama
Start the background service:

ollama serve
💡 Note: Keep this terminal process running, or run it as a background service. Open a new terminal tab/window for the remaining steps.

** Run the LLMs**

ollama pull gemma4
Run Agent

python3 agent.py

