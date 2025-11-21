@echo off
REM Quick test script for Windows

echo ============================================================
echo AoE4 Bot - Screen Capture Test
echo ============================================================
echo.

REM Activate virtual environment
if not exist venv\Scripts\activate.bat (
    echo [ERROR] Virtual environment not found!
    echo Please run setup_windows.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo Virtual environment activated.
echo.

REM Run test
echo Running screen capture test...
echo.
python test_capture.py

echo.
echo ============================================================
echo Test complete! Check the data\ folder for screenshots.
echo ============================================================
pause
