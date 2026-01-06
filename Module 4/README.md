# AI Coding Agent

*AI Dev Tools Zoomcamp – Module 4*

## Overview

This project implements a Python-based AI Coding Agent that converts natural language instructions into actual code changes on disk. Unlike traditional chatbots, this agent can read, create, and modify files within a controlled sandbox environment, demonstrating practical agentic AI design.

## What This Agent Can Do

✅ **Generate new code files** from natural language descriptions
✅ **Read and modify existing files** with context awareness
✅ **Understand current project structure** and maintain consistency
✅ **Iteratively improve code** based on user feedback
✅ **Safely operate** within a restricted filesystem sandbox (`output/` directory)

The agent mimics the behavior of AI-powered IDE assistants like Cursor, but in a simplified, educational implementation.

## Project Structure

```
Module 4/
│
├── agent.py              # Main agent loop and orchestration logic
├── tools.py              # Sandboxed filesystem operations
├── prompts.py            # System prompt defining agent behavior rules
├── requirements.txt      # Python dependencies
├── .env                  # API key configuration (not committed)
├── output/               # Sandbox directory for generated/modified code
│   ├── app/
│   └── ...               # Generated projects appear here
└── README.md             # This file
```

## How It Works

The agent follows a structured workflow:

```
User Instruction
      ↓
Read Project State (files + contents)
      ↓
Send Context to LLM (GPT-4o-mini)
      ↓
LLM Plans Changes → Structured JSON Response
      ↓
Python Tools Execute File Operations
      ↓
User Provides Next Instruction
```

**Key Principle:** The LLM acts as the planner, while Python handles the execution.

## Core Components

### 1. `agent.py` — The Controller
- Runs an interactive command loop
- Reads current project state from `output/` directory
- Sends contextual information to OpenAI's API
- Parses structured JSON responses from the LLM
- Applies file changes using the tools module

### 2. `tools.py` — Safe File Operations
Provides sandboxed filesystem functions:
- `create_file(path, content)` — Creates/overwrites files
- `read_file(path)` — Reads file contents
- `list_files()` — Lists all files in the sandbox
- All operations are restricted to the `output/` directory

### 3. `prompts.py` — Agent Behavior Rules
Defines strict constraints for the LLM:
- Output only valid JSON (no explanations or markdown)
- All files must reside in `output/` directory
- Preserve existing logic unless explicitly instructed to change
- Support iterative improvements
- Handle multiple file operations in a single response

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

## Running the Agent

Start the interactive agent:
```bash
python agent.py
```

You'll see:
```
What do you want to do? (type 'exit' to stop):
```

### Example Session

```
What do you want to do? (type 'exit' to stop): Create a Python script that adds three numbers

✅ Updated 1 file(s)

What do you want to do? (type 'exit' to stop): Add input validation to handle non-numeric inputs

✅ Updated 1 file(s)

What do you want to do? (type 'exit' to stop): exit
```

Generated files appear in the `output/` directory.

## Safety & Design Principles

🔒 **Filesystem Sandboxing** — All operations restricted to `output/` directory
🧩 **Structured JSON Protocol** — Reliable LLM responses via enforced format
🔁 **Iterative Development** — Human-in-the-loop improvement cycle
🧠 **LLM as Planner** — Language model decides, Python executes
📦 **Minimal Dependencies** — Clean, focused architecture

## Technologies Used

- **Python** — Core implementation
- **OpenAI API** — GPT-4o-mini for code planning
- **python-dotenv** — Environment variable management
- **pathlib** — Safe filesystem path handling

## Learning Outcomes

This module demonstrates:
- Agentic AI design patterns
- LLM integration with structured outputs
- Safe filesystem operations
- Interactive development workflows
- JSON-based communication protocols

The agent showcases how AI can be transformed from a conversational tool into a practical coding assistant through careful system design and constraint enforcement.