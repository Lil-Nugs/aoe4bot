#!/usr/bin/env python3
"""Test script to verify UI calibration positions."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import cv2
import numpy as np
from game_interface import GameInterface
from config import Config

def main():
    print("=" * 70)
    print("Testing UI Calibration")
    print("=" * 70)

    # Initialize
    config = Config()
    interface = GameInterface(filter_aoe4_only=True)

    # Focus the game window
    print("\nBringing AoE4 window to front...")
    if interface.focus_game_window():
        print("Game window focused. Capturing in 2 seconds...")
        import time
        time.sleep(2)
    else:
        print("Warning: Could not focus game window")

    print("\nCapturing game screenshot...")
    state = interface.get_game_state()
    screenshot = state.screenshot

    # Convert RGB to BGR for OpenCV
    img = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    print(f"[OK] Screenshot captured: {img.shape}")
    print("\nDrawing calibrated UI positions...")

    # Draw minimap region
    x, y, w, h = config.game.minimap_region
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.putText(img, "MINIMAP", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Draw resource regions
    resources = [
        ('FOOD', config.game.resources_food_region, (0, 255, 255)),
        ('WOOD', config.game.resources_wood_region, (139, 69, 19)),
        ('GOLD', config.game.resources_gold_region, (0, 215, 255)),
        ('STONE', config.game.resources_stone_region, (128, 128, 128))
    ]

    for name, (rx, ry, rw, rh), color in resources:
        cv2.rectangle(img, (rx, ry), (rx + rw, ry + rh), color, 2)
        cv2.putText(img, name, (rx, ry - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Draw population region
    x, y, w, h = config.game.population_region
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
    cv2.putText(img, "POP", (x, y - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    # Draw game time region
    x, y, w, h = config.game.game_time_region
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
    cv2.putText(img, "TIME", (x, y - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # Draw queue indicator region
    x, y, w, h = config.game.queue_indicator_region
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 128, 0), 2)
    cv2.putText(img, "QUEUE", (x, y - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 128, 0), 2)

    # Save the annotated screenshot
    output_file = os.path.join(config.data_dir, 'test_calibration.png')
    cv2.imwrite(output_file, img)
    print(f"\n[OK] Annotated screenshot saved to: {output_file}")

    # Display the image
    print("\nDisplaying calibration overlay...")
    print("Press any key to close the window.")

    cv2.namedWindow('Calibration Test', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Calibration Test', 1920, 1080)
    cv2.imshow('Calibration Test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("\n" + "=" * 70)
    print("CALIBRATION SUMMARY")
    print("=" * 70)
    print(f"Minimap: {config.game.minimap_region}")
    print(f"Food: {config.game.resources_food_region}")
    print(f"Wood: {config.game.resources_wood_region}")
    print(f"Gold: {config.game.resources_gold_region}")
    print(f"Stone: {config.game.resources_stone_region}")
    print(f"Population: {config.game.population_region}")
    print(f"Game Time: {config.game.game_time_region}")
    print(f"Queue: {config.game.queue_indicator_region}")
    print("=" * 70)

    print("\n[OK] Calibration test complete!")
    print("\nNext steps:")
    print("1. Check if the boxes align with the UI elements in the saved image")
    print("2. If positions are off, run calibrate_ui.py again")
    print("3. If positions look good, you're ready to start building the bot logic!")

if __name__ == "__main__":
    main()
