# Quick Start Guide

Get DeepResearch Agent running in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- OpenAI API key OR Anthropic API key

## Automated Setup (Recommended)

### Windows PowerShell

```powershell
# Run the setup script
.\scripts\setup.ps1
```

This will:
- ✅ Check Python and Node.js installations
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies
- ✅ Create necessary directories
- ✅ Set up environment files

## Manual Setup

### Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=your_key_here
```

### Frontend Setup

```powershell
# Navigate to frontend
cd frontend

# Dependencies are already installed (from npm create vite)
# If not, run:
# npm install

# Create .env file
cp .env.example .env
```

## Configuration

Edit `backend/.env`:

```env
# Choose your LLM provider
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=your-anthropic-key-here

# Set provider
LLM_PROVIDER=openai  # or anthropic
LLM_MODEL=gpt-4-turbo-preview  # or claude-3-sonnet-20240229
```

## Running the Application

### Option 1: Using Scripts

**Terminal 1 - Backend:**
```powershell
.\scripts\run.ps1 backend
```

**Terminal 2 - Frontend:**
```powershell
.\scripts\run.ps1 frontend
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m app.main
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Test the Setup

### Test Backend
```powershell
cd backend
pytest
```

### Test API Manually
```powershell
# Health check
curl http://localhost:8000/api/health

# Or visit http://localhost:8000/docs for interactive API testing
```

## Usage

1. Open http://localhost:5173 in your browser
2. Enter a research query (e.g., "What is the impact of AI on education?")
3. Select research depth
4. Click "Start Research"
5. Watch the agent work!

## Current Status

**Phase 1 Complete** ✅
- Backend API running
- Frontend UI functional
- Session management working
- Progress tracking interface ready

**Coming in Phase 2:**
- LLM agent integration
- Research planning
- Goal understanding

## Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Check that Python 3.10+ is installed: `python --version`
- Verify .env file has API keys

### Frontend won't start
- Ensure Node.js 18+ is installed: `node --version`
- Try deleting `node_modules` and running `npm install` again

### API key errors
- Double-check your API key in `backend/.env`
- Ensure no extra spaces or quotes around the key
- Verify the key is valid by testing it directly

### Port already in use
- Backend (8000): Change `API_PORT` in `backend/.env`
- Frontend (5173): It will auto-select another port

## Next Steps

1. ✅ Complete Phase 1 setup
2. 📝 Review the PRD in `Docs/` folder
3. 🚀 Ready for Phase 2 development!

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review the architecture in `Docs/DeepResearch Agent — System Architecture.md`
- See the development roadmap in `Docs/DeepResearch Agent — Development Roadmap.md`

---

**Happy Researching!** 🔬✨
