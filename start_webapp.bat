@echo off
REM CloudShield AI - Start Web Application
REM This script starts both backend and frontend servers

echo Starting CloudShield AI Web Application...
echo.

REM Check if Python is available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

REM Check if Node.js is available
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found in PATH
    pause
    exit /b 1
)

echo [1/4] Installing backend dependencies...
cd backend
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..

echo [2/4] Installing frontend dependencies...
cd frontend
npm install --silent 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..

echo [3/4] Starting backend server (port 8000)...
start "CloudShield Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [4/4] Starting frontend server (port 3000)...
start "CloudShield Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==========================================
echo CloudShield AI Web Application Started!
echo ==========================================
echo.
echo Backend API:  http://localhost:8000
echo Frontend UI:  http://localhost:3000
echo API Docs:     http://localhost:8000/docs
echo.
echo Press any key to stop servers and exit...
pause >nul

echo Stopping servers...
taskkill /f /im uvicorn.exe >nul 2>nul
taskkill /f /im node.exe >nul 2>nul
echo Done.