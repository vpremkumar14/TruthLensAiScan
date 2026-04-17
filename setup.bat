@echo off
REM Setup script for TruthLens AI Scan (Windows)

echo.
echo 🚀 TruthLens AI Scan - Setup Script (Windows)
echo =============================================
echo.

REM Backend setup
echo 1️⃣  Setting up Backend...
cd backend

REM Create virtual environment
echo    Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo    Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo    Installing Python dependencies...
pip install -r requirements.txt

REM Create placeholder model
echo    Creating placeholder model...
python create_model.py

echo    ✓ Backend setup complete!
echo.

REM Frontend setup
echo 2️⃣  Setting up Frontend...
cd ..\frontend

REM Install dependencies
echo    Installing Node dependencies...
call npm install

echo    ✓ Frontend setup complete!
echo.

echo ✨ Setup complete!
echo.
echo To start the application:
echo 1. Backend:  cd backend ^&^& venv\Scripts\activate ^&^& python app.py
echo 2. Frontend: cd frontend ^&^& npm run dev
echo.
echo Then open: http://localhost:3000
echo.
pause
