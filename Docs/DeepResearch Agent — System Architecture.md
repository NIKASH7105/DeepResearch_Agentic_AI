# DeepResearch Agent — System Architecture

## Autonomous AI Research & Report Generation System

---

# 1. Architecture Overview

The DeepResearch Agent follows a **layered agentic architecture** where the LLM-based agent acts as the central decision-making component and dynamically interacts with external tools, memory, evidence storage, and verification components.

| Layer | Components | Purpose |
|---|---|---|
| **Presentation Layer** | React | User interaction and research dashboard |
| **API Layer** | FastAPI | Communication between frontend and backend |
| **Agent Layer** | LangGraph + LLM | Planning, reasoning, decision-making, orchestration |
| **Tool Layer** | Web Search, Semantic Scholar, arXiv, Crossref, PDF, Python | External information gathering and processing |
| **Evidence Layer** | Evidence Manager, Source Ranker | Organize and evaluate research evidence |
| **Memory Layer** | FAISS + SQLite/PostgreSQL | Store and retrieve research knowledge |
| **Verification Layer** | Claim & Citation Verification | Validate generated information |
| **Generation Layer** | Report Generator | Create final research reports |
| **Output Layer** | PDF / DOCX | Deliver final research results |

---

# 2. High-Level Architecture

```text
                         ┌───────────────────┐
                         │       USER        │
                         │  Research Query   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   React Frontend  │
                         │ Research Dashboard│
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │      FastAPI      │
                         │    Backend API    │
                         └─────────┬─────────┘
                                   │
                                   ▼
                 ┌─────────────────────────────────┐
                 │        RESEARCH AGENT            │
                 │        LangGraph + LLM            │
                 │                                  │
                 │  • Goal Understanding            │
                 │  • Planning                      │
                 │  • Reasoning                     │
                 │  • Tool Selection                │
                 │  • State Management              │
                 └───────────────┬─────────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
               ▼                 ▼                 ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │ External     │  │   Memory     │  │    State     │
        │ Tools        │  │ FAISS + DB   │  │ Management   │
        └──────┬───────┘  └──────────────┘  └──────────────┘
               │
               ▼
        ┌─────────────────────────────────────────┐
        │              TOOL LAYER                 │
        │                                         │
        │ Web Search │ Academic Search │ PDF      │
        │ arXiv      │ Semantic Scholar│ Python   │
        │ Crossref   │ Web Scraper     │          │
        └──────────────────┬──────────────────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │  Evidence Manager  │
                 │                    │
                 │ Claims             │
                 │ Sources            │
                 │ Evidence           │
                 │ Relevance          │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Verification Layer │
                 │                    │
                 │ Claim Verification │
                 │ Citation Checking  │
                 │ Conflict Detection │
                 └─────────┬──────────┘
                           │
                     ┌─────┴─────┐
                     │           │
                Insufficient   Verified
                  Evidence     Evidence
                     │           │
                     ▼           ▼
                  Research    Synthesis
                   Again          │
                     │            │
                     └──────┐     │
                            ▼     ▼
                         ┌───────────────┐
                         │ Report Agent  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌────────────────┐
                         │ Report Generator│
                         └───────┬────────┘
                                 │
                         ┌───────┴───────┐
                         ▼               ▼
                    ┌─────────┐     ┌─────────┐
                    │   PDF   │     │  DOCX   │
                    └─────────┘     └─────────┘
```

---

# 3. User Interface Layer

### Technology
**React**

The frontend provides the interface through which users interact with the research agent.

### Components

- Research query input
- Research depth selection
- Date range selection
- Research progress
- Source explorer
- Research history
- Report viewer
- PDF/DOCX download

### Flow

```text
User
 ↓
Research Query
 ↓
React
 ↓
FastAPI
```

---

# 4. API Layer

### Technology
**FastAPI**

FastAPI acts as the communication layer between the frontend and the agent.

### Responsibilities

- Receive research requests
- Create research sessions
- Send requests to the agent
- Stream research progress
- Return research results
- Manage report downloads
- Handle API errors

### Example

```text
POST /research
GET  /research/{id}
GET  /research/{id}/sources
GET  /research/{id}/report
```

---

# 5. Agent Layer

### Technologies

- LangGraph
- LLM

This is the **brain of the system**.

### Responsibilities

- Understand the user's goal
- Create research plans
- Decide which tools to use
- Execute tools
- Analyze results
- Decide whether more research is required
- Manage research state
- Trigger verification
- Generate final synthesis

### Agent State

```text
ResearchState

├── user_query
├── research_goal
├── research_plan
├── current_task
├── tool_history
├── sources
├── evidence
├── claims
├── conflicts
├── verification_results
└── final_report
```

---

# 6. Tool Layer

The agent interacts with external systems through a standardized tool interface.

```text
                     AGENT
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
          Web Search Academic   PDF
                     Search
              │        │        │
              ├────────┼────────┤
              ▼        ▼        ▼
           Python   Crossref   arXiv
```

### Tools

| Tool | Function |
|---|---|
| Web Search | Find current web information |
| Semantic Scholar | Find academic research |
| arXiv | Retrieve scientific papers |
| Crossref | Retrieve publication metadata |
| Web Scraper | Extract web content |
| PDF Processor | Extract paper content |
| Python | Calculations and analysis |

---

# 7. Research Planning Component

The planner converts a broad research question into smaller research tasks.

### Example

```text
Research Question
       ↓
"Impact of Generative AI on Education"
       ↓
Research Planner
       ↓
┌─────────────────────────────┐
│ 1. Background               │
│ 2. Benefits                 │
│ 3. Risks                    │
│ 4. Learning outcomes        │
│ 5. Academic research        │
│ 6. Conflicting findings     │
│ 7. Research gaps            │
└─────────────────────────────┘
```

The plan can be modified during execution.

---

# 8. Agentic Execution Loop

This is the **core architecture** of DeepResearch Agent.

```text
                    ┌──────────┐
                    │   GOAL   │
                    └────┬─────┘
                         ↓
                    ┌──────────┐
                    │   PLAN   │
                    └────┬─────┘
                         ↓
                  ┌──────────────┐
                  │ SELECT TOOL  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │ EXECUTE TOOL  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │   OBSERVE    │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │   EVALUATE   │
                  └──────┬───────┘
                         ↓
                  Enough Evidence?
                    /          \
                  NO            YES
                  ↓              ↓
             Re-plan          Synthesis
                  │              │
                  └──────►───────┘
```

The agent therefore does not follow a completely fixed sequence. Its next action depends on the results of previous actions.

---

# 9. Evidence Management Layer

The Evidence Manager converts raw information into structured evidence.

### Pipeline

```text
Source
 ↓
Document
 ↓
Relevant Passage
 ↓
Claim
 ↓
Evidence
 ↓
Citation
```

### Stored Information

```text
Evidence

├── source_id
├── claim
├── supporting_text
├── source_type
├── relevance_score
├── credibility_score
└── citation
```

---

# 10. Memory Layer

### Technologies

**FAISS + SQLite/PostgreSQL**

Memory is divided into two components.

### Vector Memory

FAISS stores embeddings for semantic retrieval.

```text
Research Content
      ↓
Embeddings
      ↓
FAISS
      ↓
Semantic Search
```

### Structured Memory

SQLite/PostgreSQL stores:

- Users
- Research sessions
- Sources
- Claims
- Evidence
- Reports
- Metadata

---

# 11. Verification Layer

The verification layer ensures that the final report is supported by evidence.

### Claim Verification

```text
Generated Claim
       ↓
Retrieve Evidence
       ↓
Compare Claim + Evidence
       ↓
     Supported?
      /       \
    YES        NO
     ↓          ↓
  Accept     Research Again
```

### Conflict Detection

```text
Source A → Finding A
Source B → Finding B
          ↓
   Conflict Detection
          ↓
   Additional Research
          ↓
   Balanced Synthesis
```

---

# 12. Synthesis Layer

Once sufficient evidence has been collected, the agent synthesizes the findings.

```text
Sources
   ↓
Evidence
   ↓
Claims
   ↓
Topic Groups
   ↓
Comparative Analysis
   ↓
Key Findings
   ↓
Conclusion
```

The synthesis should distinguish between:

- Strong evidence
- Weak evidence
- Conflicting evidence
- Research gaps

---

# 13. Report Generation Layer

The Report Generator converts the final synthesis into a structured document.

```text
Verified Evidence
       ↓
Research Synthesis
       ↓
Report Structure
       ↓
Citation Insertion
       ↓
Reference Generation
       ↓
PDF / DOCX
```

### Output Formats

- PDF
- DOCX

---

# 14. Data Flow

The complete data flow is:

```text
USER QUERY
    ↓
FRONTEND
    ↓
FASTAPI
    ↓
RESEARCH AGENT
    ↓
RESEARCH PLAN
    ↓
EXTERNAL TOOLS
    ↓
RAW RESULTS
    ↓
EVIDENCE EXTRACTION
    ↓
SOURCE RANKING
    ↓
MEMORY / EVIDENCE STORE
    ↓
VERIFICATION
    ↓
 ┌──┴──────────────┐
 │                 │
Need More?       Complete
 │                 │
 └→ Research       ↓
      Again      SYNTHESIS
                   ↓
              CITATIONS
                   ↓
             REPORT GENERATOR
                   ↓
             PDF / DOCX
```

---

# 15. Complete Agentic Architecture

```text
                           USER
                             │
                             ▼
                     ┌──────────────┐
                     │ React Frontend│
                     └───────┬──────┘
                             │
                             ▼
                     ┌──────────────┐
                     │    FastAPI   │
                     └───────┬──────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │      RESEARCH AGENT     │
                │                         │
                │       LLM + LangGraph   │
                │                         │
                │ Goal → Plan → Act       │
                │ Observe → Evaluate      │
                └────────────┬────────────┘
                             │
              ┌──────────────┼───────────────┐
              │              │               │
              ▼              ▼               ▼
        ┌──────────┐   ┌───────────┐   ┌──────────┐
        │ Web      │   │ Academic  │   │ Document │
        │ Search   │   │ Search    │   │ Tools    │
        └────┬─────┘   └─────┬─────┘   └────┬─────┘
             │               │              │
             └───────────────┼──────────────┘
                             ▼
                    ┌─────────────────┐
                    │ Evidence Manager│
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                 FAISS          SQLite/PostgreSQL
                    │                 │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │   Verification  │
                    │                 │
                    │ Claims          │
                    │ Citations       │
                    │ Conflicts       │
                    └────────┬────────┘
                             │
                       ┌─────┴─────┐
                       │           │
                    Research     Complete
                       │           │
                       └─────┐     │
                             ▼     ▼
                          SYNTHESIS
                             │
                             ▼
                       REPORT AGENT
                             │
                             ▼
                    ┌─────────────────┐
                    │ Report Generator │
                    └────────┬────────┘
                             │
                       ┌─────┴─────┐
                       ▼           ▼
                      PDF         DOCX
```

---

# 16. Core Architectural Principle

The most important principle of the architecture is:

```text
             LLM
              │
              ▼
       DECIDE WHAT TO DO
              │
              ▼
        USE EXTERNAL TOOL
              │
              ▼
       OBSERVE THE RESULT
              │
              ▼
        EVALUATE RESULT
              │
              ▼
      DECIDE WHAT TO DO NEXT
              │
              └───────────────┐
                              │
                              ▼
                           REPEAT
```

This makes **DeepResearch Agent** an actual **tool-using, goal-oriented Agentic AI system**, rather than a conventional chatbot or simple RAG application.