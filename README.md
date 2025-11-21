# AoE4 Bot - AI for Age of Empires IV

An AI agent that learns to play Age of Empires IV using reinforcement learning (PPO) with screen capture and input simulation.

## Project Goals

### Phase 1 (Current)
- Scout the map
- Pick up sheep
- Avoid enemy town center
- Queue villagers (ensure one is always in queue)

### Phase 2 (Future)
- Manage idle villagers
- Execute build orders
- Optimize resource gathering (villager redistribution)

## Tech Stack

- **ML Framework**: PyTorch with Stable-Baselines3
- **RL Algorithm**: PPO (Proximal Policy Optimization)
- **Game Interface**: Screen capture + keyboard/mouse simulation
- **Environment**: Custom OpenAI Gym wrapper

## Setup

> **⚠️ IMPORTANT:** This project must run on **Windows** to interact with Age of Empires IV.
> If you're in WSL, see [TRANSITION_TO_WINDOWS.md](TRANSITION_TO_WINDOWS.md) for setup instructions.

### Quick Start (Windows)

1. **Install Python 3.8+** from https://python.org (check "Add to PATH")

2. **Run the setup script:**
   ```powershell
   .\setup_windows.bat
   ```

3. **Test screen capture:**
   ```powershell
   .\run_test.bat
   ```

4. **Start training:**
   ```powershell
   .\train.bat
   ```

**For detailed instructions, see:**
- [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md) - Step-by-step guide
- [WINDOWS_SETUP.md](WINDOWS_SETUP.md) - Complete setup documentation
- [TRANSITION_TO_WINDOWS.md](TRANSITION_TO_WINDOWS.md) - If coming from WSL

### Manual Installation (Advanced)

1. Create virtual environment:
```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Configure game settings in `config\game_config.yaml`

## Project Structure

```
aoe4bot/
├── src/
│   ├── game_interface.py    # Screen capture and input simulation
│   ├── aoe4_env.py          # Gym environment wrapper
│   ├── train.py             # Training script
│   ├── config.py            # Configuration management
│   └── utils/               # Utility functions
├── config/                  # Configuration files
├── models/                  # Saved model checkpoints
├── logs/                    # Training logs and tensorboard
└── data/                    # Training data and screenshots
```

## Usage

### Training
```bash
python src/train.py
```

### Testing
```bash
python src/test.py --model models/best_model.zip
```

## Development Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed development plans.

## License

MIT
