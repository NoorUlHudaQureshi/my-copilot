# 🤖 AI Copilot: Agentic AI Assistant

A beginner-friendly, full-stack AI assistant featuring a modular agentic architecture. It combines text chat, AI vision, real-time voice, and a customizable skill system.

## 🚀 Features

- **AI Chat:** Interactive text conversation powered by local LLMs.
- **AI Vision:** Upload images and have the AI analyze them in real-time.
- **Agentic Skills:** A registry-based framework allowing the AI to use tools (e.g., time, calculator).
- **Real-time Voice:** LiveKit integration for low-latency audio interaction.
- **Hybrid AI:** Local-first approach using **Ollama (gemma3:1b)** with cloud fallback capabilities.

## 🛠️ Tech Stack

- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS 4, shadcn/ui.
- **Backend:** FastAPI, Python 3.13, `uv` (package manager).
- **Real-time:** LiveKit.
- **Local AI:** Ollama.

## 📦 Getting Started

### Prerequisites
- **Python 3.13+** (installed via `uv`)
- **Node.js 24+**
- **Ollama** (installed and running `gemma3:1b`)
- **LiveKit Cloud/Self-hosted** account (for voice features)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your LiveKit and Cloud AI keys
   ```
4. Start the server:
   ```bash
   uv run fastapi dev
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure environment variables:
   ```bash
   cp .env.example .env.local # if available, or create manually
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```

## 🧠 Agent Architecture

The assistant uses a **Registry Pattern** for its skills. Adding a new capability is as simple as creating a new class in `backend/app/skills/library/` and registering it.

**Flow:** 
`User Prompt` $\rightarrow$ `LLM` $\rightarrow$ `Tool Call Request` $\rightarrow$ `Skill Registry` $\rightarrow$ `Execution` $\rightarrow$ `LLM` $\rightarrow$ `Final Answer`.

## 🛡️ Project Rules
- No secrets in git.
- Run tests after every change.
- Keep logic minimal and type-safe.
