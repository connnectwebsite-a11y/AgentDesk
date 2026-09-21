# 🛠️ AgentDesk


## 🌐 Live Demo

Try AgentDesk here:

https://agentdesk-9o07.onrender.com

> The demo runs on a free Render instance and may take around 50 seconds to wake after a period of inactivity.


AgentDesk is a multi-agent AI IT support system that researches technical problems using official documentation, generates troubleshooting instructions, and performs automated quality assurance before responding to the user.

## 🚀 Features

- Multi-agent IT troubleshooting
- Automatic ticket triage
- Diagnostic reasoning
- Device and operating-system routing
- Live technical documentation search
- Official-source verification
- Source relevance checking
- Evidence-grounded troubleshooting
- Automated QA
- Automatic answer revision
- Final response verification
- Gradio web interface
- SQLite ticket management
- Support-note history

## 🤖 Multi-Agent Architecture

User IT Problem
↓
Triage Agent
↓
Diagnostic Agent
↓
Device / Knowledge Router
↓
Documentation Search
↓
Official Source Verification
↓
Source Relevance Agent
↓
Knowledge Agent
↓
QA Agent
↓
Revision Agent (when required)
↓
Final QA
↓
Customer Response

## 🧰 Technology

- Python
- Groq API
- Tavily Search API
- Gradio
- SQLite

## 📁 Project Structure

AgentDesk/
├── app.py
├── agents.py
├── pipeline.py
├── knowledge.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md

## 🔐 API Keys

AgentDesk does not store API keys directly in the source code.

Set these environment variables before running the application:

GROQ_API_KEY
TAVILY_API_KEY

## ▶️ Installation

Install the dependencies:

pip install -r requirements.txt

Then run:

python app.py

## 🎯 Project Goal

AgentDesk demonstrates how multiple AI agents can cooperate in an IT-support workflow while grounding troubleshooting recommendations in relevant official documentation and applying automated quality-control checks.

## ⚠️ Current Status

AgentDesk is a portfolio project and prototype. AI-generated troubleshooting should be reviewed before use in production environments.
