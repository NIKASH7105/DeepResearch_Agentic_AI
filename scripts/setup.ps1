# DeepResearch Agent Setup Script
# This script sets up both backend and frontend

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "DeepResearch Agent Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Setting up Backend" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Setup backend
Set-Location backend

Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠ Please edit backend/.env and add your API keys" -ForegroundColor Yellow
}

# Create necessary directories
Write-Host "Creating data directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path data, temp, reports, logs | Out-Null

Set-Location ..

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Setup frontend
Set-Location frontend

# Create .env if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
}

Set-Location ..

Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit backend/.env and add your API keys (OPENAI_API_KEY or ANTHROPIC_API_KEY)"
Write-Host "2. Start the backend:" -ForegroundColor Cyan
Write-Host "   cd backend"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   python -m app.main"
Write-Host ""
Write-Host "3. Start the frontend (in a new terminal):" -ForegroundColor Cyan
Write-Host "   cd frontend"
Write-Host "   npm run dev"
Write-Host ""
Write-Host "The API will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "The frontend will be available at: http://localhost:5173" -ForegroundColor Green
