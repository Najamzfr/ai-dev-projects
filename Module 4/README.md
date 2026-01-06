AI Coding Agent (AI Dev Tools Zoomcamp – Module 4)
Overview

This project implements a Python-based AI Coding Agent that converts natural language instructions into real code changes on disk.

Unlike a chatbot, this agent:

Writes actual files

Reads and understands existing project structure

Iteratively improves code based on user feedback

Operates safely inside a controlled filesystem sandbox

The project demonstrates agentic AI design, not just text generation.

What This Agent Can Do

✅ Generate new code files from scratch
✅ Read existing files and modify them
✅ Understand the current project structure
✅ Iteratively improve code until the user stops
✅ Safely operate inside a restricted directory (output/)

This mimics the internal behavior of tools like Cursor or AI-powered IDE assistants, but in a simplified, educational form.

Project Structure
coding-agent/
│
├── agent.py          # Main agent loop and control logic
├── tools.py          # File system tools (read, write, list)
├── prompts.py        # System prompt (agent behavior rules)
├── requirements.txt  # Dependencies
├── .env              # API key (not committed)
└── output/           # Generated / modified code lives here

How the Agent Works (High-Level)

The agent follows this loop:

User Instruction
      ↓
LLM (plans changes)
      ↓
Structured JSON output
      ↓
Python tools execute changes
      ↓
User provides next instruction


Key idea:

The LLM decides what to do, Python executes it.

Core Components Explained
1. agent.py — The Controller

Runs an interactive loop

Accepts user instructions

Reads current project state (files + contents)

Sends context to the LLM

Applies returned changes using tools

This file orchestrates the entire agent lifecycle.

2. tools.py — The Agent’s Hands

Contains safe, sandboxed filesystem operations:

create_file(path, content)

read_file(path)

update_file(path, content)

list_files()

All file access is restricted to the output/ directory to prevent unsafe behavior.

3. prompts.py — The Agent Contract

Defines strict rules for the LLM:

Output JSON only

No explanations or markdown

Modify existing files carefully

Preserve working logic unless told otherwise

Never write outside output/

This transforms the LLM from a chatbot into a reliable planning engine.

Iterative Agent Behavior

The agent supports human-in-the-loop iteration:

Example session:

Create a Python script that prints Hello
→ Agent creates file

Improve the code style
→ Agent edits existing file

Add error handling
→ Agent updates file again

exit


This mirrors real developer workflows.

Safety & Design Principles

🔒 Filesystem sandboxing (output/ only)

🧩 Structured JSON outputs for reliability

🔁 Iterative improvement loop

🧠 LLM as planner, Python as executor

📦 Minimal dependencies, clear architecture

Installation & Setup
1. Install dependencies
pip install -r requirements.txt

2. Set API key

Create a .env file:

OPENAI_API_KEY=your_api_key_here

Running the Agent
python agent.py


Then interactively provide instructions:

What do you want to do? (type 'exit' to stop):


Generated or modified files will appear inside output/.

Technologies Used

Python

OpenAI API (via ToyAIKit)

ToyAIKit (LLM abstraction layer)

Pathlib (safe filesystem handling)