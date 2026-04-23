@echo off
REM Setup script for Football News Website (Windows)

echo ======================================
echo Football News Website - Setup Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo Initializing database...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✓ Database initialized')"

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 2. Create an admin user:
echo    flask create-admin
echo.
echo 3. Start the server:
echo    python main.py
echo.
echo 4. Open your browser to:
echo    http://localhost:5000
echo.
echo ======================================
pause
