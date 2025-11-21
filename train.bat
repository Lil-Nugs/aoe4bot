@echo off
REM Quick training script for Windows

echo ============================================================
echo AoE4 Bot - Training Script
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

REM Check for command line arguments
if "%1"=="" (
    echo Starting new training session...
    echo.
    python src\train.py
) else if "%1"=="--test" (
    if "%2"=="" (
        echo [ERROR] Please specify model path for testing
        echo Usage: train.bat --test models\your_model.zip
        pause
        exit /b 1
    )
    echo Testing model: %2
    echo.
    python src\train.py --test %2
) else if "%1"=="--resume" (
    if "%2"=="" (
        echo [ERROR] Please specify model path to resume
        echo Usage: train.bat --resume models\your_model.zip
        pause
        exit /b 1
    )
    echo Resuming training from: %2
    echo.
    python src\train.py --resume %2
) else (
    echo Unknown argument: %1
    echo.
    echo Usage:
    echo   train.bat                           - Start new training
    echo   train.bat --test MODEL_PATH         - Test a trained model
    echo   train.bat --resume MODEL_PATH       - Resume training
    pause
    exit /b 1
)

pause
