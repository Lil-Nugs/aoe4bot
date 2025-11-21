# Windows Setup Guide for AoE4 Bot

Since Age of Empires 4 runs on Windows, the bot needs to run on Windows Python (not WSL) to properly capture the game screen and send inputs.

## Prerequisites

1. **Python 3.8 or higher for Windows**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify installation: Open PowerShell and run `python --version`

2. **Age of Empires IV** installed and runnable

3. **Git for Windows** (optional, for version control)
   - Download from: https://git-scm.com/download/win

## Setup Steps

### Step 1: Access the Project from Windows

This project is currently in WSL. You can access it from Windows at:

```
\\wsl$\Ubuntu\home\mattc\aoe4bot
```

**Option A: Copy to Windows**
1. Open File Explorer
2. Navigate to `\\wsl$\Ubuntu\home\mattc\aoe4bot`
3. Copy the entire folder to a Windows location, e.g., `C:\Users\YourName\Projects\aoe4bot`

**Option B: Work directly from WSL path** (slower but keeps everything in one place)
1. Use the WSL path directly from Windows
2. Navigate to `\\wsl$\Ubuntu\home\mattc\aoe4bot` in PowerShell

### Step 2: Run the Setup Script

Open **PowerShell** (or Command Prompt) in the project directory:

```powershell
# Navigate to project directory
cd C:\Users\YourName\Projects\aoe4bot

# Run the setup script
.\setup_windows.bat
```

This will:
- Create a Python virtual environment
- Upgrade pip
- Install all dependencies from requirements.txt
- Verify the installation

### Step 3: Activate the Virtual Environment

Every time you want to use the bot, activate the virtual environment first:

```powershell
venv\Scripts\activate
```

You should see `(venv)` appear in your prompt.

### Step 4: Test Screen Capture

With the virtual environment activated:

```powershell
python test_capture.py
```

This will:
- Capture your 4K screen
- Save test screenshots to `data/` folder
- Show performance metrics
- Verify everything is working

### Step 5: Optional - Tesseract OCR Installation

For reading game text (resources, population, etc.), install Tesseract OCR:

1. Download Tesseract installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location: `C:\Program Files\Tesseract-OCR`
3. Add to PATH or set in config: `C:\Program Files\Tesseract-OCR\tesseract.exe`

## Quick Reference

### Daily Usage

```powershell
# 1. Open PowerShell in project directory
cd C:\Users\YourName\Projects\aoe4bot

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Run training or testing
python src/train.py
# or
python src/train.py --test models/best_model.zip
```

### Deactivate Virtual Environment

```powershell
deactivate
```

### Reinstall Dependencies

```powershell
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

## Troubleshooting

### "Python not found"
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to PATH in System Environment Variables

### "Permission denied" errors
- Run PowerShell as Administrator
- Check antivirus isn't blocking Python

### Screen capture not working
- Make sure you're running on Windows Python, not WSL
- Check that the game window is visible (not minimized)
- Try running the test script: `python test_capture.py`

### PyAutoGUI errors on multiple monitors
- PyAutoGUI should detect your 4K primary monitor automatically
- If issues occur, we can configure specific screen regions

### Import errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## Next Steps

After setup is complete:

1. ✓ Run `python test_capture.py` to verify screen capture works
2. Start AoE4 and run the test again to capture game screen
3. Calibrate UI positions for your 4K setup
4. Begin training the AI!

## Performance Notes

- **4K Resolution**: Screen capture at 4K (3840x2160) will be downscaled to 84x84 for the AI
- **Frame Rate**: Target ~10-30 actions per second during training
- **GPU**: PyTorch will automatically use your GPU if available (NVIDIA CUDA)
- Check GPU usage: `python -c "import torch; print(torch.cuda.is_available())"`

## Windows-Specific Paths

The project uses these directories:
- `models\` - Saved AI models
- `logs\` - Training logs and TensorBoard data
- `data\` - Screenshots and training data
- `config\` - Configuration files

All paths in the code use cross-platform Path objects, so they work on both Windows and Linux.
