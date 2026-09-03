# DeepResearch Agent — Comprehensive Project Documentation

## 1. Executive Summary & Project Objectives (What is Wanted)

### 1.1 Problem Statement
Traditional LLM chat interfaces (e.g., standard ChatGPT or Claude windows) suffer from three critical limitations when handling complex research queries:
1. **Single-Turn Limitation & Shallow Search:** They provide generic surface-level answers based on single web queries without pursuing multi-depth follow-up inquiries.
2. **Hallucination & Lack of Verifiable Evidence:** They often assert facts without direct, traceable attribution to live web or literature sources.
3. **Static Output:** They produce raw unformatted markdown text rather than structured, publication-ready research reports containing embedded visual media, metadata tables, and verified citations.

### 1.2 Core Vision & Solution
**DeepResearch Agent** is an autonomous, multi-agent AI research system designed to solve these problems by executing a continuous **Plan → Act → Observe → Evaluate → Repeat → Generate** loop.

The system autonomously:
- Deconstructs complex user prompts into multi-angle research sub-questions.
- Dynamically queries external tools (web search, image acquisition engines, web scrapers).
- Extracts granular facts and evidence points per retrieved source.
- Evaluates the adequacy of retrieved information and self-corrects by searching for missing knowledge gaps.
- Synthesizes an evidence-backed report with inline numerical citations (`[1]`, `[2]`).
- Compiles the final findings into a formatted PDF document containing structured metadata tables and relevant visual media.

---

## 2. System Architecture & Tech Stack (What is Used Where)

### 2.1 Technology Stack Breakdown

| Layer | Technology / Library | Purpose & Responsibility |
| :--- | :--- | :--- |
| **Frontend Framework** | React 18 + Vite | High-performance user interface and state management |
| **Data Fetching** | TanStack Query (React Query) | Real-time polling (2s intervals) for research progress and status |
| **HTTP Client** | Axios | Async REST communication with the FastAPI backend |
| **UI Components & Icons** | Lucide React + Vanilla CSS | Clean, responsive UI elements, spinning loaders, and status indicators |
| **Backend Framework** | FastAPI | Async Python web framework for API routing and background tasks |
| **Agentic Workflow** | LangGraph + LangChain Core | State machine managing cyclic planning, tool execution, and evaluation |
| **LLM Provider Engine** | Ollama / OpenAI / Anthropic | Language models driving sub-question generation, evidence extraction & synthesis |
| **Web Search Tool** | DuckDuckGo Search (`ddgs`) | Free, rate-friendly search integration retrieving web pages and snippets |
| **Image Retrieval** | DuckDuckGo Images + `httpx` | Asynchronous image search and cached downloading for PDF inclusion |
| **Evidence Processing** | Custom Parsing Services | Fact extraction pipeline mapping bullet points to source IDs |
| **PDF Generation Engine** | ReportLab + PIL (Pillow) | Programmatic PDF creation, layout templates, image scaling, and table formatting |

---

### 2.2 Directory & Component Mapping

```
Agentic Ai/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI application entrypoint & middleware
│   │   ├── config.py                # Environment configuration & API settings
│   │   ├── api/
│   │   │   ├── research.py          # REST endpoints (/start, /{id}, /download/pdf)
│   │   │   └── health.py            # API health check endpoint
│   │   ├── agents/
│   │   │   ├── agent_graph.py       # LangGraph state graph definition & nodes
│   │   │   ├── planner.py           # Sub-question decomposition logic
│   │   │   └── researcher.py        # Background task execution runner
│   │   ├── tools/
│   │   │   ├── web_search.py        # DuckDuckGo web search wrapper
│   │   │   └── image_search.py      # DDG image search & downloader service
│   │   ├── services/
│   │   │   ├── evidence_extractor.py# Fact extraction & citation generator
│   │   │   └── pdf_generator.py     # ReportLab PDF report compiler
│   │   └── models/
│   │       ├── research.py          # Pydantic models (ResearchSession, Source)
│   │       └── state.py             # Agent graph state definitions
│   └── requirements.txt             # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Main application state & tab coordinator
│   │   ├── components/
│   │   │   ├── ResearchForm.jsx     # User query & depth selection form
│   │   │   ├── ResearchProgress.jsx # Real-time progress bar & thinking logs
│   │   │   └── ResearchResults.jsx  # Final cited report & PDF download view
│   │   └── services/
│   │       └── api.js               # Frontend API client endpoints
│   └── package.json                 # Node.js dependencies
└── Docs/                            # Project documentation & specs
```

---

## 3. End-to-End Execution Process (The Workflow)

```
[ User Input ]
      │
      ▼
1. POST /api/research/start ──► Spawns Async Background Task
      │
      ▼
2. Planner Node (plan_research) ──► Generates 3-5 Sub-Questions
      │
      ▼
3. Researcher Node (conduct_research) ──► Web Search + Fact Extraction per Source
      │
      ▼
4. Evaluator Node (evaluate_research)
      │
      ├─── [ Needs More Info & Iterations < Max ] ──► Gap Analysis Node (research_more) ──┐
      │                                                                                  │
      └─── [ Sufficient Sources / Max Iterations ]                                        │
                 │                                                                       │
                 ▼                                                                       │
5. Synthesizer Node (synthesize_answer) ◄────────────────────────────────────────────────┘
      │  (Generates markdown answer with [1], [2] citations)
      ▼
6. PDF Generation Engine (generate_report)
      │  (Fetches images via ImageSearchTool, builds ReportLab Document)
      ▼
[ Styled PDF Download Delivered to User UI ]
```

### Detailed Workflow Stages:

1. **Session Initialization:**
   - User enters query (e.g. *"Impact of Quantum Computing on Financial Cybersecurity"*) and selects depth (`quick`, `standard`, `deep`).
   - `ResearchForm.jsx` sends a POST request to `/api/research/start`.
   - FastAPI generates a UUID `session_id`, initializes an in-memory `ResearchSession` object with state `PENDING`, and launches `run_research` in `BackgroundTasks`.

2. **Decomposition & Planning (`plan_research`):**
   - LangGraph graph invokes `plan_research` node.
   - Prompt sent to LLM to create 3 to 5 targeted sub-questions.
   - Progress updated to 10%, status set to `PLANNING`.

3. **Autonomous Search & Fact Extraction (`conduct_research`):**
   - For each sub-question, `WebSearchTool` queries DuckDuckGo for top web results.
   - For every web snippet returned, `extract_evidence()` prompts the LLM to extract 2-3 concise facts.
   - Source objects are populated with unique IDs, URLs, snippets, and extracted key evidence.
   - Progress updated to 30%, status set to `RESEARCHING`.

4. **Quality Evaluation & Iterative Loop (`evaluate_research` & `research_more`):**
   - The evaluator counts total collected sources and facts.
   - If total sources $\ge 6$ or max iterations (2) reached $\rightarrow$ sets quality to `SUFFICIENT`.
   - Otherwise, triggers `research_more` node which analyzes missing information gaps, generates 2 new focused search queries, and loops back to `conduct_research`.

5. **Citation Synthesis (`synthesize_answer`):**
   - `generate_cited_answer()` combines all collected sources and facts into a unified prompt context.
   - LLM generates a comprehensive markdown synthesis where every factual claim ends with bracketed citations (`[1]`, `[2]`).

6. **Media Acquisition & PDF Compilation (`PDFReportGenerator`):**
   - Triggered via GET `/api/research/{session_id}/download/pdf`.
   - `ImageSearchTool` searches DuckDuckGo Images, downloads top relevant graphics asynchronously (`httpx`), and saves them to local temp storage.
   - `PDFReportGenerator` uses ReportLab to assemble:
     - **Cover Title Page:** Blue primary header, document metadata table, hero image.
     - **Research Plan Section:** Numbered list of sub-questions explored.
     - **Findings Section:** Styled body paragraphs with inline citations and embedded graphics.
     - **References Section:** Complete reference list detailing titles, URLs, and key facts.

7. **UI Presentation:**
   - `ResearchProgress.jsx` polls status every 2 seconds, displaying progress percentage and live agent reasoning steps.
   - `ResearchResults.jsx` displays the final cited text, interactive source cards with evidence bullets, and a PDF download button.

---

## 4. Concrete Example Dry Run Trace

### Input Parameters
- **Query:** *"Impact of Quantum Computing on Financial Cybersecurity"*
- **Depth:** Standard
- **Session ID:** `eb719a42-9a81-4b12-b91c-3c84e1b82190`

### Step 1: Planning Output (`planner.py`)
LLM returns 3 sub-questions:
1. *How do quantum algorithms like Shor's algorithm threaten current RSA and ECC financial encryption?*
2. *What is Post-Quantum Cryptography (PQC) and how are central banks implementing it?*
3. *What are the timeline estimates for quantum supremacy affecting banking security systems?*

### Step 2: Tool Execution & Evidence Extraction (`conduct_research`)
- **Query 1 Execution:** DuckDuckGo returns article *"Quantum Threats to Financial Infrastructure"*.
  - *Extracted Fact 1:* Shor's algorithm efficiently factors large integers, breaking 2048-bit RSA keys.
  - *Extracted Fact 2:* Financial wire transfers rely heavily on RSA-2048 for digital signatures.
- **Query 2 Execution:** DuckDuckGo returns article *"NIST Post-Quantum Cryptography Standards"*.
  - *Extracted Fact 1:* NIST finalized initial PQC standards including CRYSTALS-Kyber and Dilithium.
  - *Extracted Fact 2:* US Federal Reserve initiated migration trials for quantum-resistant algorithms.

### Step 3: Evaluation Node (`evaluate_research`)
- Iteration 1 complete. Total sources collected: 6.
- Evaluation status: `SUFFICIENT`. Graph transitions to `synthesize`.

### Step 4: Cited Synthesis Output (`synthesize_answer`)
> "Quantum computing presents an existential threat to modern financial cybersecurity, primarily due to Shor's algorithm which can break RSA and ECC encryption standards [1]. Financial institutions process trillions in daily transactions relying on these asymmetric algorithms [1]. In response, central banks and NIST have standardized Post-Quantum Cryptography (PQC) algorithms such as CRYSTALS-Kyber to harden infrastructure against future quantum attacks [2]."

### Step 5: ReportLab PDF Document Generation
- `ImageSearchTool` downloads `quantum_cybersecurity.jpg`.
- `PDFReportGenerator` compiles `research_report_eb719a42.pdf` (Title, Summary Table, Research Plan, Findings, Embedded Image, References).

---

## 5. Verification & Summary Checklist

- [x] Clear explanation of system purpose and goals (**What is Wanted**).
- [x] Complete tech stack breakdown and component file mapping (**What is Used Where**).
- [x] End-to-end multi-agent lifecycle flowchart and explanation (**The Process**).
- [x] Concrete step-by-step example dry run (**Example Dry Run**).
- [x] Executable PDF documentation generator (`scripts/generate_docs_pdf.py`).
