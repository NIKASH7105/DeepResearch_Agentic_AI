# DeepResearch Agent Run Script
# This script runs both backend and frontend

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('backend', 'frontend', 'both')]
    [string]$Service = 'both'
)

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "DeepResearch Agent" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

function Start-Backend {
    Write-Host "Starting Backend..." -ForegroundColor Green
    Set-Location backend
    & .\venv\Scripts\Activate.ps1
    python -m app.main
}

function Start-Frontend {
    Write-Host "Starting Frontend..." -ForegroundColor Green
    Set-Location frontend
    npm run dev
}

switch ($Service) {
    'backend' {
        Start-Backend
    }
    'frontend' {
        Start-Frontend
    }
    'both' {
        Write-Host "To run both services, open two terminals:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Terminal 1 (Backend):" -ForegroundColor Cyan
        Write-Host "  .\scripts\run.ps1 backend"
        Write-Host ""
        Write-Host "Terminal 2 (Frontend):" -ForegroundColor Cyan
        Write-Host "  .\scripts\run.ps1 frontend"
        Write-Host ""
    }
}
