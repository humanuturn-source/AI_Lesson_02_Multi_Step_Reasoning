# Install Instructions

## AI Lesson 01: AI Agent

The following intructions are for MAC

## Step 1: Prerequisites

Before starting, ensure you have the following installed on your system:

- **Package Manager:** [Homebrew](https://brew.sh/)
- **Python:** Python 3.10 or higher (`python3 --version`)
---

## Step 2: Install & Start Ollama

1. **Install Ollama** via Homebrew:
   ```bash
   brew install ollama
   ```

2. **Start the background service:**
   ```bash
   ollama serve
   ```
   > 💡 **Note:** Keep this terminal process running, or run it as a background service. Open a new terminal tab/window for the remaining steps.

3. ** Run the LLMs**
    ```bash
    ollama pull gemma4
    ```

4. Run Agent

   ```
   python3 agent.py

   ```
---

