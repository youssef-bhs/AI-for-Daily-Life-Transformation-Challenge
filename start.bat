@echo off
echo ================================================
echo  SmartStudent AI - Quick Start
echo ================================================
echo.

echo [1/2] Starting Backend (FastAPI)...
cd backend
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
)
call venv\Scripts\activate
pip install -r requirements.txt -q
start "SmartStudent Backend" cmd /k "venv\Scripts\activate && python main.py"
cd ..

echo.
echo [2/2] Starting Frontend (React)...
cd frontend
if not exist node_modules (
    npm install
)
start "SmartStudent Frontend" cmd /k "npm start"
cd ..

echo.
echo ================================================
echo  Both servers starting...
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:3000
echo  API Docs: http://localhost:8000/docs
echo ================================================
pause
