#!/usr/bin/env python3
"""Test screenshot capture from AoE4 window."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import cv2
from game_interface import GameInterface

print("Testing screenshot capture...")
print("=" * 70)

# Create interface with AoE4 filtering
interface = GameInterface(filter_aoe4_only=True)

# Capture screenshot
state = interface.get_game_state()
screenshot = state.screenshot

print(f"Screenshot captured: {screenshot.shape}")
print(f"Monitor region: {interface.monitor}")

# Save screenshot
output_file = "data/test_screenshot_aoe4.png"
img_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
cv2.imwrite(output_file, img_bgr)

print(f"Screenshot saved to: {output_file}")
print("\nPlease check the saved image to verify it captured the game window.")
print("If it shows your terminal instead of the game, the window detection needs adjustment.")
