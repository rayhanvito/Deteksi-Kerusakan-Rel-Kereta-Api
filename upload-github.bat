@echo off
REM GitHub Upload Script for Railway Track Inspection System

cd /d "c:\Users\rayha\Documents\Detector Rail Kereta Api"

echo.
echo ========================================
echo   Preparing for GitHub Upload
echo ========================================
echo.

REM Initialize git if not already
if not exist .git (
    echo [1/5] Initializing Git repository...
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
) else (
    echo [1/5] Git repository already initialized
)

echo [2/5] Adding all files...
git add .

echo [3/5] Creating initial commit...
git commit -m "Initial commit: Railway Track Inspection System - AI-powered fault detection with YOLOv5"

echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Create repository on GitHub:
echo    - Go to https://github.com/new
echo    - Name: railway-track-inspection
echo    - Description: AI-Powered Railway Track Fault Detection System
echo    - Choose: Public or Private
echo    - Click "Create repository"
echo.
echo 2. Add remote and push:
echo    git remote add origin https://github.com/YOUR_USERNAME/railway-track-inspection.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Or if repository already exists:
echo    git remote add origin https://github.com/YOUR_USERNAME/railway-track-inspection.git
echo    git push -u origin main
echo.
echo ========================================
echo.
echo Local commits ready!
echo Run the commands above to push to GitHub.
echo.

pause
