# DeepResearch Agent

**Autonomous AI Research & Report Generation System**

An agentic AI system that autonomously performs multi-step research on user-provided topics using external tools and generates evidence-backed, cited research reports.

## 🎯 Project Overview

DeepResearch Agent demonstrates the complete agentic cycle:

**Plan → Act → Observe → Evaluate → Repeat → Generate**

Unlike conventional chatbots, this system:
- Creates autonomous research plans
- Selects and uses external tools dynamically
- Searches web and academic sources
- Retrieves and analyzes research papers
- Extracts and verifies evidence
- Identifies conflicting information
- Performs additional research when needed
- Synthesizes findings with proper citations
- Generates structured research reports

## 🏗️ Architecture

```
Frontend (React + Vite)
    ↓
FastAPI Backend
    ↓
Research Agent (LangGraph + LLM)
    ↓
External Tools (Web Search, Academic APIs, PDF Processing)
    ↓
Evidence Management & Verification
    ↓
Report Generation (PDF/DOCX)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn
- OpenAI API key or Anthropic API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file from example:
```bash
cp .env.example .env
```

6. Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_key_here
# or
ANTHROPIC_API_KEY=your_key_here
```

7. Run the backend:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file from example:
```bash
cp .env.example .env
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📁 Project Structure

```
DeepResearch-Agent/
├── backend/
│   ├── app/
│   │   ├── agents/         # Agent logic and LangGraph workflows
│   │   ├── api/           # FastAPI routes
│   │   ├── models/        # Data models
│   │   ├── services/      # Business logic
│   │   ├── tools/         # External tool integrations
│   │   └── utils/         # Utility functions
│   ├── tests/            # Backend tests
│   ├── requirements.txt  # Python dependencies
│   └── .env.example     # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API client
│   │   └── utils/        # Frontend utilities
│   ├── package.json     # Node dependencies
│   └── .env.example    # Frontend environment variables
└── Docs/               # Project documentation
```

## 🔧 Development Phases

- [x] **Phase 1**: Project Foundation ✅
- [ ] **Phase 2**: Basic LLM Agent
- [ ] **Phase 3**: External Tool Integration
- [ ] **Phase 4**: Agentic Research Loop
- [ ] **Phase 5**: Evidence & Memory System
- [ ] **Phase 6**: Verification Layer
- [ ] **Phase 7**: Report Generation
- [ ] **Phase 8**: UI & Evaluation

## 🛠️ Technologies

### Backend
- **FastAPI** - Modern web framework
- **LangChain & LangGraph** - Agent framework
- **OpenAI/Anthropic** - LLM providers
- **FAISS** - Vector similarity search
- **SQLAlchemy** - Database ORM
- **PyMuPDF** - PDF processing
- **BeautifulSoup** - Web scraping

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **TanStack Query** - Data fetching
- **Axios** - HTTP client
- **Lucide React** - Icons

## 📚 Features

### Current (Phase 1)
- ✅ Project structure and configuration
- ✅ FastAPI backend with health endpoints
- ✅ React frontend with modern UI
- ✅ Research session management
- ✅ Progress tracking interface

### Coming Soon
- 🔄 Autonomous research planning
- 🔄 Multi-source research (Web, Academic, arXiv)
- 🔄 PDF extraction and analysis
- 🔄 Evidence verification
- 🔄 Conflict detection
- 🔄 Citation generation
- 🔄 PDF/DOCX report generation

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📖 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

This is an academic project. Contributions, suggestions, and feedback are welcome!

## 📄 License

This project is for educational purposes.

## 🎓 Academic Context

This project demonstrates:
- **Agentic AI Architecture** - Autonomous decision-making and tool use
- **Multi-step Planning** - Breaking down complex research tasks
- **Tool Integration** - Dynamic tool selection and execution
- **Evidence-based Generation** - Verifying claims against sources
- **Iterative Refinement** - Learning from observations and adjusting plans

## 📞 Support

For questions or issues, please refer to the documentation in the `Docs/` directory.

---

**Version**: 1.0.0  
**Status**: Phase 1 Complete ✅
