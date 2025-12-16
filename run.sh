#!/bin/bash

# Railway Track Inspection System - Quick Start Script
# Linux/Mac Bash Script

echo ""
echo "========================================"
echo "  Railway Track Inspection System"
echo "  Quick Start"
echo "========================================"
echo ""

# Check Python
if ! command -v python3.10 &> /dev/null; then
    echo "[ERROR] Python 3.10+ not found. Please install it first."
    exit 1
fi

# Install dependencies
echo "[1/3] Installing dependencies..."
cd backend
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
cd ..

# Start Backend
echo "[2/3] Starting Backend API (port 8000)..."
python3.10 backend/main.py &
BACKEND_PID=$!
sleep 3

# Start Frontend
echo "[3/3] Starting Frontend (port 3000)..."
cd frontend
python3.10 -m http.server 3000 &
FRONTEND_PID=$!
cd ..

sleep 2

echo ""
echo "========================================"
echo "  ✓ System Ready!"
echo "  "
echo "  Frontend: http://127.0.0.1:3000"
echo "  Backend:  http://127.0.0.1:8000"
echo "  API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "  Press Ctrl+C to stop all services"
echo "========================================"
echo ""

# Trap to cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

# Wait for processes
wait
