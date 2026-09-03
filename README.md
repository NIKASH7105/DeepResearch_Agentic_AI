# DeepResearch Agent

**Autonomous AI Research & Report Generation System**

An agentic AI system that autonomously performs multi-step research on user-provided topics using external tools, evidence verification, and generates comprehensive, cited PDF research reports.

---

## 🎯 Project Overview

DeepResearch Agent executes a complete autonomous agentic loop:

**Plan → Act → Observe → Evaluate → Repeat → Generate**

Unlike conventional Q&A chatbots, this system:
- **Decomposes** complex user queries into structured sub-questions.
- **Searches & Scrapes** web and academic data dynamically via external search engines.
- **Extracts Evidence** into granular facts tied directly to source IDs (`[1]`, `[2]`).
- **Evaluates Information Quality** and identifies knowledge gaps to run follow-up research iterations.
- **Synthesizes Findings** into structured reports with inline numerical citations.
- **Generates Publication-Ready PDFs** complete with metadata tables, research plan breakdowns, cited text, auto-retrieved images, and references.

---

## 🎨 Modern Deep Space UI

The frontend has been redesigned with a **Deep Space Glassmorphism** theme:
- **Visual Design**: Dark space palette (`#060810`), animated background mesh, glowing indigo/cyan/violet accents, and backdrop-blur cards.
- **Interactive Depth Selector**: Card-based toggle for Quick (3–5 sources), Standard (8–15 sources), and Deep (15+ sources) research modes.
- **Real-Time Stage Timeline**: Visual progress radial arc and vertical step indicator tracking Planning → Searching → Analyzing → Verifying → Synthesizing.
- **Tabbed Results View**: Tabbed display for the final **Report**, **Research Plan**, real-time **Agent Terminal Log**, and **Source Cards**.
- **One-Click PDF Export**: Direct download for generated PDF reports.

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────┐
│              React 18 + Vite Frontend                    │
│      (TanStack Query, Deep Space Glassmorphism UI)       │
└──────────────────────────┬───────────────────────────────┘
                           │ Async REST / API Polling
┌──────────────────────────▼───────────────────────────────┐
│                    FastAPI Backend                       │
│    (CORS Middleware, Session Manager, File Streaming)    │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│               LangGraph Agentic Workflow                 │
│  Plan ──► Research ──► Evaluate ──► Gap Search ──► Synthesize│
└────┬─────────────────────────────────────────────────┬───┘
     │                                                 │
┌────▼──────────────────────┐             ┌────────────▼──────────────┐
│     External Tools        │             │  ReportLab PDF Engine     │
│ - DuckDuckGo Web Search   │             │ - Custom Layout Templates │
│ - DuckDuckGo Image Search │             │ - Auto Image Resizing     │
│ - Ollama / LLM Inference  │             │ - Evidence Tables         │
└───────────────────────────┘             └───────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Agentic Workflow**: LangGraph & LangChain Core
- **LLM Engine**: Ollama (e.g., `llama3.2`), OpenAI, or Anthropic
- **Search & Media**: DuckDuckGo Search (`ddgs`) & Async `httpx`
- **PDF Generation**: ReportLab & PIL (Pillow)
- **ASGI Server**: Uvicorn

### Frontend
- **Framework**: React 18 + Vite
- **Data Fetching & State**: TanStack Query (React Query v5) & Axios
- **Styling**: Custom CSS (Vanilla CSS, Glassmorphism design system, Inter & JetBrains Mono fonts)
- **Icons**: Lucide React

---

## 🚀 Quick Start Guide

### 1. Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **LLM Service**: Local [Ollama](https://ollama.ai/) running `llama3.2` (default) or an API key for OpenAI / Anthropic.

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create & activate virtual environment
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template (if needed)
cp .env.example .env
```

Ensure Ollama is running locally:
```bash
ollama run llama3.2
```

Start the FastAPI backend server:
```bash
python -m app.main
```
> Backend runs at `http://localhost:8000` (API Docs at `http://localhost:8000/docs`).

### 3. Frontend Setup

In a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
> Frontend will be available at `http://localhost:5173`.

---

## 📁 Project Structure

```
Agentic Ai/
├── backend/
│   ├── app/
│   │   ├── agents/          # LangGraph research graph, planner, & researcher
│   │   ├── api/             # FastAPI routers (research & health endpoints)
│   │   ├── models/          # Pydantic data models & state schema
│   │   ├── services/        # Evidence extractor & ReportLab PDF generator
│   │   ├── tools/           # DuckDuckGo web search & image search integrations
│   │   ├── config.py        # Settings management
│   │   └── main.py          # FastAPI application entry point & CORS configuration
│   ├── reports/             # Generated PDF reports output folder
│   ├── temp/                # Cached search images & temporary assets
│   ├── .env.example         # Backend environment variables template
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # ResearchForm, ResearchProgress, ResearchResults
│   │   ├── services/        # Axios API client
│   │   ├── App.jsx          # Main application layout & screen manager
│   │   ├── App.css          # App layout styles & component rules
│   │   └── index.css        # Global CSS variables, fonts & animations
│   ├── package.json         # Frontend dependencies & scripts
│   └── vite.config.js       # Vite configuration
├── Docs/                    # Project documentation & PRD
└── README.md                # Project documentation
```

---

## 📡 Key API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/research/start` | Initialize a new research session |
| `GET` | `/api/research/{session_id}` | Retrieve session details, research plan, and reasoning logs |
| `GET` | `/api/research/{session_id}/status` | Poll real-time progress percentage and current task |
| `GET` | `/api/research/{session_id}/sources` | Retrieve retrieved sources and extracted evidence |
| `GET` | `/api/research/{session_id}/download/pdf` | Download generated PDF report |
| `GET` | `/api/health` | Backend service health check |

---

## 📜 License

This project is open-source and intended for academic and educational purposes.
