# Transitioning from WSL to Windows

You've set up the project in WSL, but since Age of Empires 4 runs on Windows, you need to run the Python code on Windows to capture the game and send inputs.

## Why Windows?

- ✅ Direct access to game window for screen capture
- ✅ Can send keyboard/mouse inputs to the game
- ✅ Better performance (no WSL overhead)
- ✅ PyAutoGUI works natively with Windows applications
- ❌ WSL can't interact with Windows GUI applications effectively

## Option 1: Copy Project to Windows (Recommended)

### Step 1: Copy the Project

1. **Open File Explorer**
2. **Navigate to:** `\\wsl$\Ubuntu\home\mattc\aoe4bot`
3. **Copy the entire folder** to a Windows location:
   - Suggested: `C:\Users\YourName\Projects\aoe4bot`
   - Or: `D:\Projects\aoe4bot`
   - Or your Desktop: `C:\Users\YourName\Desktop\aoe4bot`

### Step 2: Install Python on Windows

1. Download from: https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Complete installation
5. Verify in PowerShell: `python --version`

### Step 3: Run Setup

1. **Open PowerShell**
   - Right-click in the project folder
   - Select "Open PowerShell window here"

2. **Run setup script:**
   ```powershell
   .\setup_windows.bat
   ```

3. **Wait 5-10 minutes** for dependencies to install

### Step 4: Test

```powershell
.\run_test.bat
```

Open AoE4 and run the test again to verify it captures the game!

## Option 2: Work Directly from WSL Path

You can work directly from the WSL path in Windows without copying:

### Step 1: Open PowerShell in WSL Directory

```powershell
cd \\wsl$\Ubuntu\home\mattc\aoe4bot
```

### Step 2: Run Setup

```powershell
.\setup_windows.bat
```

**Note:** This creates a Windows virtual environment in the WSL folder, which is fine but may be slightly slower.

## What About the WSL Virtual Environment?

The `venv` folder you created in WSL is **Linux-based** and won't work on Windows. You need a separate Windows virtual environment.

- **WSL venv:** `venv/` (Linux Python packages)
- **Windows venv:** `venv\` (Windows Python packages)

They can coexist in the same project directory if you're working from the WSL path.

## File System Notes

### Accessing Files

| Location | WSL Path | Windows Path |
|----------|----------|--------------|
| Project Root | `/home/mattc/aoe4bot` | `\\wsl$\Ubuntu\home\mattc\aoe4bot` |
| Screenshots | `/home/mattc/aoe4bot/data` | `\\wsl$\Ubuntu\home\mattc\aoe4bot\data` |
| Models | `/home/mattc/aoe4bot/models` | `\\wsl$\Ubuntu\home\mattc\aoe4bot\models` |

### Line Endings

Windows uses `CRLF` line endings, WSL/Linux uses `LF`. Git handles this automatically, but if you see warnings:

```bash
# In WSL (optional cleanup)
git config core.autocrlf true
```

## Development Workflow

### Recommended Setup

1. **Code editing:** Use VS Code on Windows
   - Install "Remote - WSL" extension to edit WSL files
   - Or edit Windows copy directly

2. **Run training:** Windows PowerShell
   ```powershell
   cd C:\Users\YourName\Projects\aoe4bot
   venv\Scripts\activate
   python src\train.py
   ```

3. **Git/Version Control:** Either WSL or Windows
   - Use Git from Windows if project is copied to Windows
   - Or use Git from WSL if working from WSL path

## Quick Commands Reference

### Windows (PowerShell)

```powershell
# Activate venv
venv\Scripts\activate

# Run training
python src\train.py

# Test capture
python test_capture.py

# Deactivate
deactivate
```

### WSL (if you need it for other tasks)

```bash
# Activate venv
source venv/bin/activate

# Can't run game capture here!
# This is only useful for non-GUI tasks
```

## What to Do Next

1. ✅ Follow **Option 1** or **Option 2** above
2. ✅ Run `setup_windows.bat`
3. ✅ Test with `run_test.bat`
4. ✅ Start training!

See `QUICK_START_WINDOWS.md` for a step-by-step guide.
