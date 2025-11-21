@echo off
REM Windows setup script for AoE4 Bot

echo ============================================================
echo AoE4 Bot - Windows Setup
echo ============================================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Python found:
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

REM Activate virtual environment and install dependencies
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

echo [4/5] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [5/5] Installing dependencies (this may take several minutes)...
echo This will download PyTorch and other ML libraries...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo To activate the virtual environment, run:
echo     venv\Scripts\activate
echo.
echo To test screen capture, run:
echo     python test_capture.py
echo.
echo To start training, run:
echo     python src\train.py
echo.
echo See WINDOWS_SETUP.md for detailed instructions.
echo ============================================================
pause
