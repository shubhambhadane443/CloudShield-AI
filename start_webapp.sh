#!/usr/bin/env bash
# CloudShield AI - Start Web Application (Linux/macOS)

set -e

echo "Starting CloudShield AI Web Application..."
echo

# Check dependencies
command -v python3 >/dev/null 2>&1 || { echo "ERROR: Python 3 not found"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "ERROR: Node.js not found"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "ERROR: npm not found"; exit 1; }

echo "[1/4] Installing backend dependencies..."
cd backend
pip install -q -r requirements.txt
cd ..

echo "[2/4] Installing frontend dependencies..."
cd frontend
npm install --silent
cd ..

echo "[3/4] Starting backend server (port 8000)..."
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

echo "[4/4] Starting frontend server (port 3000)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo
echo "=========================================="
echo "CloudShield AI Web Application Started!"
echo "=========================================="
echo
echo "Backend API:  http://localhost:8000"
echo "Frontend UI:  http://localhost:3000"
echo "API Docs:     http://localhost:8000/docs"
echo
echo "Press Ctrl+C to stop servers..."

# Trap SIGINT to cleanup
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'; exit 0" INT

wait