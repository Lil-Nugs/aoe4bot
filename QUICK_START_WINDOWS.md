# Quick Start Guide (Windows)

## 1. First-Time Setup (5-10 minutes)

### Prerequisites
- Python 3.8+ installed (https://www.python.org/downloads/)
- Check "Add Python to PATH" during installation

### Access Project

The project is in WSL. Access it from Windows at:
```
\\wsl$\Ubuntu\home\mattc\aoe4bot
```

**Recommended:** Copy it to Windows for better performance:
```
C:\Users\YourName\Projects\aoe4bot
```

### Run Setup

1. Open **PowerShell** in the project directory
2. Run:
   ```powershell
   .\setup_windows.bat
   ```
3. Wait 5-10 minutes for dependencies to install

## 2. Test Screen Capture

```powershell
.\run_test.bat
```

This will:
- Capture your 4K screen
- Save screenshots to `data\` folder
- Show performance metrics

**Tip:** Run this with Age of Empires 4 open to verify game capture!

## 3. Start Training

```powershell
# Start new training
.\train.bat

# Or manually:
venv\Scripts\activate
python src\train.py
```

## 4. Monitor Training

While training is running:

```powershell
# In a new PowerShell window
venv\Scripts\activate
tensorboard --logdir logs
```

Then open browser to: http://localhost:6006

## Common Commands

```powershell
# Activate virtual environment
venv\Scripts\activate

# Test screen capture
python test_capture.py

# Train from scratch
python src\train.py

# Resume training
python src\train.py --resume models\checkpoint_model.zip

# Test a trained model
python src\train.py --test models\final_model.zip

# Deactivate virtual environment
deactivate
```

## Troubleshooting

### "python not found"
- Reinstall Python with "Add to PATH" checked
- Restart PowerShell after installation

### Virtual environment issues
```powershell
# Delete and recreate
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Screen capture errors
- Make sure you're running on **Windows Python**, not WSL
- Run PowerShell as Administrator if permission errors occur

## Next Steps

1. ✅ Complete setup
2. ✅ Test screen capture with AoE4 running
3. 📋 Calibrate UI positions (see config\game_config.yaml)
4. 🚀 Start training!

For detailed information, see:
- `WINDOWS_SETUP.md` - Complete setup guide
- `README.md` - Project overview
- `ROADMAP.md` - Development plan
