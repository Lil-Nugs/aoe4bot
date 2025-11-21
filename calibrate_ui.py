#!/usr/bin/env python3
"""Interactive UI calibration tool for AoE4 Bot.

This script helps you calibrate the positions of UI elements in Age of Empires IV
by clicking on them in a screenshot. The calibrated positions are saved to config.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import cv2
import numpy as np
from src.game_interface import GameInterface
from src.config import Config
import json

class UICalibrator:
    """Interactive UI calibration tool."""

    def __init__(self):
        self.interface = GameInterface(filter_aoe4_only=True)
        self.config = Config()
        self.screenshot = None
        self.display_img = None
        self.ui_positions = {}
        self.current_element = None
        self.click_count = 0
        self.temp_points = []

        # UI elements to calibrate
        self.calibration_steps = [
            {
                'name': 'minimap',
                'instruction': 'Click TOP-LEFT corner of minimap, then BOTTOM-RIGHT corner',
                'clicks_needed': 2,
                'type': 'region'
            },
            {
                'name': 'resources_food',
                'instruction': 'Click on FOOD resource number',
                'clicks_needed': 1,
                'type': 'point'
            },
            {
                'name': 'resources_wood',
                'instruction': 'Click on WOOD resource number',
                'clicks_needed': 1,
                'type': 'point'
            },
            {
                'name': 'resources_gold',
                'instruction': 'Click on GOLD resource number',
                'clicks_needed': 1,
                'type': 'point'
            },
            {
                'name': 'resources_stone',
                'instruction': 'Click on STONE resource number',
                'clicks_needed': 1,
                'type': 'point'
            },
            {
                'name': 'population',
                'instruction': 'Click on POPULATION counter (e.g., "10/200")',
                'clicks_needed': 1,
                'type': 'point'
            },
            {
                'name': 'game_time',
                'instruction': 'Click on GAME TIME display (e.g., "5:30")',
                'clicks_needed': 1,
                'type': 'point'
            },
            {
                'name': 'queue_indicator',
                'instruction': 'Click on QUEUE indicator area (where unit production icons show)',
                'clicks_needed': 1,
                'type': 'point'
            }
        ]

        self.current_step = 0

    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse clicks."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.temp_points.append((x, y))
            self.click_count += 1

            # Draw the click
            cv2.circle(self.display_img, (x, y), 5, (0, 255, 0), -1)

            # Get current step info
            step = self.calibration_steps[self.current_step]

            if self.click_count >= step['clicks_needed']:
                # Save the calibration
                if step['type'] == 'point':
                    self.ui_positions[step['name']] = {
                        'x': self.temp_points[0][0],
                        'y': self.temp_points[0][1]
                    }
                elif step['type'] == 'region':
                    x1, y1 = self.temp_points[0]
                    x2, y2 = self.temp_points[1]
                    self.ui_positions[step['name']] = {
                        'x': min(x1, x2),
                        'y': min(y1, y2),
                        'width': abs(x2 - x1),
                        'height': abs(y2 - y1)
                    }
                    # Draw rectangle
                    cv2.rectangle(self.display_img,
                                (min(x1, x2), min(y1, y2)),
                                (max(x1, x2), max(y1, y2)),
                                (0, 255, 0), 2)

                # Move to next step
                self.current_step += 1
                self.click_count = 0
                self.temp_points = []

                # Reset display
                if self.current_step < len(self.calibration_steps):
                    self.display_img = self.screenshot.copy()
                    self._draw_previous_calibrations()

            cv2.imshow('UI Calibration', self.display_img)

    def _draw_previous_calibrations(self):
        """Draw previously calibrated elements on the display."""
        for name, pos in self.ui_positions.items():
            if 'width' in pos:  # Region
                cv2.rectangle(self.display_img,
                            (pos['x'], pos['y']),
                            (pos['x'] + pos['width'], pos['y'] + pos['height']),
                            (0, 255, 0), 2)
                cv2.putText(self.display_img, name,
                          (pos['x'], pos['y'] - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            else:  # Point
                cv2.circle(self.display_img, (pos['x'], pos['y']), 5, (0, 255, 0), -1)
                cv2.putText(self.display_img, name,
                          (pos['x'] + 10, pos['y']),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    def run(self):
        """Run the calibration process."""
        print("=" * 70)
        print("AoE4 Bot - UI Calibration Tool")
        print("=" * 70)
        print("\nMake sure Age of Empires IV is running and visible!")
        print("Press ENTER when ready to capture screenshot...")
        input()

        # Capture screenshot
        print("\nCapturing game screenshot...")
        state = self.interface.get_game_state()
        self.screenshot = state.screenshot
        self.display_img = self.screenshot.copy()

        # Convert RGB to BGR for OpenCV display
        self.screenshot = cv2.cvtColor(self.screenshot, cv2.COLOR_RGB2BGR)
        self.display_img = self.screenshot.copy()

        print(f"✓ Screenshot captured: {self.screenshot.shape}")

        # Setup window
        cv2.namedWindow('UI Calibration', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('UI Calibration', 1920, 1080)  # Reasonable window size
        cv2.setMouseCallback('UI Calibration', self.mouse_callback)

        print("\n" + "=" * 70)
        print("CALIBRATION INSTRUCTIONS")
        print("=" * 70)
        print("Click on the UI elements as instructed.")
        print("Press 'r' to restart current element")
        print("Press 's' to skip current element")
        print("Press 'q' to quit and save")
        print("=" * 70)

        # Main calibration loop
        while self.current_step < len(self.calibration_steps):
            step = self.calibration_steps[self.current_step]

            # Update instruction
            print(f"\n[{self.current_step + 1}/{len(self.calibration_steps)}] {step['name'].upper()}")
            print(f"→ {step['instruction']}")

            # Add instruction overlay
            self.display_img = self.screenshot.copy()
            self._draw_previous_calibrations()

            # Add text overlay
            overlay = self.display_img.copy()
            cv2.rectangle(overlay, (10, 10), (900, 80), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, self.display_img, 0.3, 0, self.display_img)

            cv2.putText(self.display_img,
                       f"Step {self.current_step + 1}/{len(self.calibration_steps)}: {step['name']}",
                       (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(self.display_img,
                       step['instruction'],
                       (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            cv2.imshow('UI Calibration', self.display_img)

            # Wait for input
            while self.current_step == self.calibration_steps.index(step):
                key = cv2.waitKey(100) & 0xFF

                if key == ord('q'):
                    print("\nQuitting calibration...")
                    self.current_step = len(self.calibration_steps)
                    break
                elif key == ord('r'):
                    print("Restarting current element...")
                    self.click_count = 0
                    self.temp_points = []
                    self.display_img = self.screenshot.copy()
                    self._draw_previous_calibrations()
                    cv2.imshow('UI Calibration', self.display_img)
                elif key == ord('s'):
                    print("Skipping element...")
                    self.current_step += 1
                    self.click_count = 0
                    self.temp_points = []
                    break

        cv2.destroyAllWindows()

        # Save calibration
        self.save_calibration()

    def save_calibration(self):
        """Save calibrated UI positions to config."""
        if not self.ui_positions:
            print("\nNo calibrations to save.")
            return

        print("\n" + "=" * 70)
        print("CALIBRATION RESULTS")
        print("=" * 70)

        for name, pos in self.ui_positions.items():
            print(f"{name}: {pos}")

        # Save to JSON file
        calibration_file = os.path.join(self.config.data_dir, 'ui_calibration.json')
        with open(calibration_file, 'w') as f:
            json.dump(self.ui_positions, f, indent=2)

        print(f"\n✓ Calibration saved to: {calibration_file}")
        print("\nYou can now use these positions in your bot configuration!")

        # Also update the config file if needed
        print("\nWould you like to update config/game_config.yaml with these positions? (y/n)")
        response = input().strip().lower()

        if response == 'y':
            self._update_config()

    def _update_config(self):
        """Update the game config with calibrated positions."""
        # Update minimap region if calibrated
        if 'minimap' in self.ui_positions:
            mm = self.ui_positions['minimap']
            self.config.game.minimap_region = (mm['x'], mm['y'], mm['width'], mm['height'])

        # Update resource positions
        if 'resources_food' in self.ui_positions:
            pos = self.ui_positions['resources_food']
            self.config.game.resources_food_pos = (pos['x'], pos['y'])

        if 'resources_wood' in self.ui_positions:
            pos = self.ui_positions['resources_wood']
            self.config.game.resources_wood_pos = (pos['x'], pos['y'])

        if 'resources_gold' in self.ui_positions:
            pos = self.ui_positions['resources_gold']
            self.config.game.resources_gold_pos = (pos['x'], pos['y'])

        if 'resources_stone' in self.ui_positions:
            pos = self.ui_positions['resources_stone']
            self.config.game.resources_stone_pos = (pos['x'], pos['y'])

        # Update other UI positions
        if 'population' in self.ui_positions:
            pos = self.ui_positions['population']
            self.config.game.population_pos = (pos['x'], pos['y'])

        if 'game_time' in self.ui_positions:
            pos = self.ui_positions['game_time']
            self.config.game.game_time_pos = (pos['x'], pos['y'])

        if 'queue_indicator' in self.ui_positions:
            pos = self.ui_positions['queue_indicator']
            self.config.game.queue_indicator_pos = (pos['x'], pos['y'])

        # Save config
        self.config.save()
        print(f"✓ Config updated and saved to: {self.config.config_path}")


def main():
    calibrator = UICalibrator()
    calibrator.run()


if __name__ == "__main__":
    main()
