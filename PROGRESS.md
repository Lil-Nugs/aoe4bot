# AoE4 Bot - Development Progress

## Project Goal
Create an AI bot that learns to play Age of Empires IV using reinforcement learning (PPO). Initial scope: scout sheep exploration challenge - queue villagers, explore with scout, collect sheep, avoid enemy TC.

## Completed ✓

### Project Setup
- [x] Basic project structure with src/, models/, logs/, data/ directories
- [x] Virtual environment with dependencies (stable-baselines3, opencv, mss, pyautogui, etc.)
- [x] Core files: config.py, game_interface.py, aoe4_env.py, train.py
- [x] Git repository initialized

### Screen Capture System
- [x] GameInterface class with mss-based screen capture
- [x] Window filtering - captures only AoE4 window (not entire screen)
- [x] Fast capture performance (~20-30ms on 4K)
- [x] Region capture support (for minimap, UI elements, etc.)
- [x] Test script validates capture works (test_capture.py)

### UI Calibration System
- [x] Interactive calibration tool (calibrate_ui.py)
- [x] Calibrates OCR regions for reading game state:
  - Minimap region
  - Resources (food, wood, gold, stone)
  - Population counter
  - Game time
  - Queue indicator
- [x] Config system with hotkeys for actions:
  - Using keyboard shortcuts (H, Q, ., A, etc.) - faster than clicking!
  - OCR for reading state (resources, population, etc.)

### Configuration
- [x] GameConfig with UI positions and hotkeys
- [x] TrainingConfig with PPO hyperparameters
- [x] RewardConfig for reward shaping
- [x] YAML save/load support

## In Progress ⏳

### Next Immediate Steps
1. **Run UI Calibration**
   - Start AoE4 in a practice match
   - Run `python calibrate_ui.py`
   - Click on UI elements to calibrate OCR regions
   - Save calibration to config

2. **Implement OCR for Game State**
   - Add pytesseract or easyocr for text recognition
   - Parse resources (food, wood, gold, stone)
   - Parse population (current/max)
   - Parse game time
   - Detect queue status (villager queued or not)

3. **Test Basic Actions**
   - Test hotkeys: select TC (H), queue villager (Q), idle economy (.)
   - Verify actions work in-game
   - Test action timing and delays

## Upcoming Features 🔮

### Computer Vision
- [ ] Minimap analysis (explored regions, unit positions)
- [ ] Sheep detection (template matching or color detection)
- [ ] Scout position detection on minimap
- [ ] Enemy TC position detection

### Gym Environment
- [ ] Observation space (screenshot + parsed state)
- [ ] Action space (discrete: queue villager, move scout, etc.)
- [ ] Reward function implementation
- [ ] Episode reset logic (restart game)
- [ ] Step function (take action, get new state, calculate reward)

### RL Training
- [ ] PPO agent setup with stable-baselines3
- [ ] CNN feature extractor for visual input
- [ ] Training loop with tensorboard logging
- [ ] Model checkpointing
- [ ] Evaluation episodes

### Advanced Features
- [ ] Handle fishing ships and traders (idle economy hotkey includes these)
- [ ] Multi-TC management
- [ ] More sophisticated sheep collection strategies
- [ ] Danger zone detection near enemy TC

## Technical Notes

### Design Decisions
- **Keyboard over Clicking**: Using hotkeys for all actions (faster, more reliable)
- **OCR for State**: Reading UI text for resources/population (calibrated positions)
- **Window Filtering**: Only capture AoE4 window to reduce noise and improve performance
- **4K Resolution**: Currently configured for 3840x2160, but calibration adapts to any resolution

### Dependencies
- Python 3.x
- stable-baselines3 (PPO)
- opencv-python (computer vision)
- mss (fast screen capture)
- pyautogui (input simulation)
- pygetwindow (window management)
- pytesseract or easyocr (OCR - to be added)

### File Structure
```
aoe4bot/
├── src/
│   ├── config.py          # Configuration management
│   ├── game_interface.py  # Screen capture & input
│   ├── aoe4_env.py        # Gym environment
│   └── train.py           # Training script
├── calibrate_ui.py        # UI calibration tool
├── test_capture.py        # Screen capture test
├── models/                # Saved model checkpoints
├── logs/                  # Training logs
└── data/                  # Screenshots, calibration data
```

## Known Issues & Considerations

1. **Idle Economy Hotkey**: The '.' key selects ALL idle economy units (villagers, fishing ships, traders), not just villagers. Need to handle this when implementing fishing/trade.

2. **OCR Not Yet Implemented**: Currently no text recognition - this is the next critical step.

3. **No Game Reset**: Need to implement automatic game restart between episodes (possibly using game menus or external scripting).

4. **Performance**: Need to profile and optimize to hit target ~10 FPS for RL training.

---

**Last Updated**: 2025-11-20
