@echo off
REM Railway Track Inspection System - Quick Start Script
REM Windows Batch File

echo.
echo ========================================
echo   Railway Track Inspection System
echo   Quick Start
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    exit /b 1
)

REM Install dependencies
echo [1/4] Installing dependencies...
cd backend
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)
cd ..

REM Start Backend
echo [2/4] Starting Backend API (port 8000)...
start "Backend API" cmd /k "cd backend && python main.py"
timeout /t 3 /nobreak

REM Start Frontend
echo [3/4] Starting Frontend (port 3000)...
start "Frontend" cmd /k "cd frontend && python -m http.server 3000"
timeout /t 2 /nobreak

REM Open Browser
echo [4/4] Opening browser...
start "" "http://127.0.0.1:3000"

echo.
echo ========================================
echo   ✓ System Ready!
echo   
echo   Frontend: http://127.0.0.1:3000
echo   Backend:  http://127.0.0.1:8000
echo   API Docs: http://127.0.0.1:8000/docs
echo ========================================
echo.
pause
