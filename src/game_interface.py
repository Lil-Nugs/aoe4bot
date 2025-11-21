"""Game interface for screen capture and input simulation."""
import time
import numpy as np
import cv2
import mss
import pyautogui
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class GameState:
    """Current game state extracted from screen."""
    screenshot: np.ndarray
    resources: dict = None  # {food, wood, gold, stone}
    population: Tuple[int, int] = (0, 0)  # (current, max)
    game_time: float = 0.0
    villager_queue: int = 0

    # Detected entities
    sheep_positions: list = None
    scout_position: Tuple[int, int] = None
    tc_position: Tuple[int, int] = None
    enemy_tc_position: Tuple[int, int] = None


class GameInterface:
    """Interface for capturing game state and sending inputs to AoE4."""

    def __init__(self, window_title: str = "Age of Empires IV", filter_aoe4_only: bool = True):
        self.window_title = window_title
        self.filter_aoe4_only = filter_aoe4_only
        self.sct = mss.mss()
        self.game_window = None

        # Disable pyautogui safety features for faster execution
        pyautogui.PAUSE = 0.01
        pyautogui.FAILSAFE = True  # Move mouse to corner to stop

        self.screen_width, self.screen_height = pyautogui.size()

        # Try to find and focus on the AoE4 window
        if self.filter_aoe4_only:
            self._find_game_window()
            if self.game_window:
                self.monitor = {
                    "top": self.game_window['top'],
                    "left": self.game_window['left'],
                    "width": self.game_window['width'],
                    "height": self.game_window['height']
                }
                print(f"Found AoE4 window at ({self.game_window['left']}, {self.game_window['top']}) "
                      f"with size {self.game_window['width']}x{self.game_window['height']}")
            else:
                print("Warning: AoE4 window not found, using full screen capture")
                self.monitor = {"top": 0, "left": 0,
                               "width": self.screen_width,
                               "height": self.screen_height}
        else:
            self.monitor = {"top": 0, "left": 0,
                           "width": self.screen_width,
                           "height": self.screen_height}

    def _find_game_window(self):
        """Find the Age of Empires IV window."""
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(self.window_title)
            if windows:
                win = windows[0]
                # Store window position and size
                self.game_window = {
                    'left': win.left,
                    'top': win.top,
                    'width': win.width,
                    'height': win.height
                }
                return True
        except ImportError:
            print("Warning: pygetwindow not installed. Install with: pip install pygetwindow")
        except Exception as e:
            print(f"Error finding game window: {e}")

        self.game_window = None
        return False

    def capture_screen(self) -> np.ndarray:
        """Capture the game screen."""
        screenshot = self.sct.grab(self.monitor)
        img = np.array(screenshot)
        # Convert BGRA to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return img

    def capture_region(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """Capture a specific region of the screen."""
        monitor = {"top": y, "left": x, "width": width, "height": height}
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return img

    def get_game_state(self) -> GameState:
        """Capture and parse current game state."""
        screenshot = self.capture_screen()

        # TODO: Implement OCR and computer vision for extracting:
        # - Resources (top bar)
        # - Population (top bar)
        # - Game time
        # - Unit positions (minimap or main screen)
        # - Queue status

        state = GameState(screenshot=screenshot)
        return state

    def click(self, x: int, y: int, button: str = 'left', clicks: int = 1):
        """Click at screen position."""
        pyautogui.click(x, y, clicks=clicks, button=button)
        time.sleep(0.05)

    def double_click(self, x: int, y: int):
        """Double click at screen position."""
        self.click(x, y, clicks=2)

    def right_click(self, x: int, y: int):
        """Right click at screen position."""
        self.click(x, y, button='right')

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int,
             duration: float = 0.2):
        """Drag from start to end position (for box selection)."""
        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()
        pyautogui.moveTo(end_x, end_y, duration=duration)
        pyautogui.mouseUp()

    def press_key(self, key: str):
        """Press a keyboard key."""
        pyautogui.press(key)
        time.sleep(0.05)

    def hotkey(self, *keys):
        """Press a combination of keys."""
        pyautogui.hotkey(*keys)
        time.sleep(0.05)

    # High-level game actions
    def select_town_center(self):
        """Select the town center (using hotkey)."""
        self.press_key('h')  # Default AoE4 hotkey for TC

    def queue_villager(self):
        """Queue a villager at town center."""
        self.select_town_center()
        time.sleep(0.1)
        self.press_key('q')  # Villager hotkey (may need adjustment)

    def select_scout(self):
        """Select the scout unit."""
        # Method 1: Use control group (if set)
        self.press_key('1')

        # Method 2: Find and click scout on minimap
        # TODO: Implement vision-based selection

    def move_to_position(self, x: int, y: int):
        """Move selected unit to position."""
        self.right_click(x, y)

    def attack_move(self, x: int, y: int):
        """Attack-move to position."""
        self.press_key('a')
        time.sleep(0.05)
        self.click(x, y)

    def select_units_box(self, x1: int, y1: int, x2: int, y2: int):
        """Select units with box selection."""
        self.drag(x1, y1, x2, y2)

    def select_idle_villager(self):
        """Select idle economy unit (villager, fishing ship, trader)."""
        self.press_key('.')  # Default idle economy unit hotkey

    def set_rally_point(self, x: int, y: int):
        """Set rally point for selected building."""
        self.right_click(x, y)

    def check_villager_queue(self) -> int:
        """Check if villager is in queue (requires OCR/vision)."""
        # TODO: Implement vision-based queue detection
        return 0

    def focus_game_window(self):
        """Bring game window to focus."""
        # This is platform-specific and may need adjustment
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(self.window_title)
            if windows:
                windows[0].activate()
                time.sleep(0.5)
                return True
        except ImportError:
            print("pygetwindow not installed, skipping window focus")
        return False


class VisionHelper:
    """Computer vision utilities for game state detection."""

    @staticmethod
    def preprocess_for_ocr(img: np.ndarray) -> np.ndarray:
        """Preprocess image for OCR."""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Enhance contrast
        gray = cv2.equalizeHist(gray)
        # Threshold
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return binary

    @staticmethod
    def detect_sheep(img: np.ndarray) -> list:
        """Detect sheep positions in image (simplified)."""
        # TODO: Implement template matching or CNN-based detection
        # For now, return empty list
        return []

    @staticmethod
    def detect_units(img: np.ndarray, unit_type: str) -> list:
        """Detect units of specific type."""
        # TODO: Implement unit detection
        return []

    @staticmethod
    def analyze_minimap(minimap_img: np.ndarray) -> dict:
        """Analyze minimap for explored regions and unit positions."""
        # TODO: Implement minimap analysis
        return {
            'explored_percent': 0.0,
            'unit_positions': [],
            'enemy_positions': []
        }


if __name__ == "__main__":
    # Test the interface
    interface = GameInterface()
    print(f"Screen size: {interface.screen_width}x{interface.screen_height}")

    # Test screen capture
    state = interface.get_game_state()
    print(f"Screenshot shape: {state.screenshot.shape}")

    # Save test screenshot
    cv2.imwrite("test_screenshot.png", cv2.cvtColor(state.screenshot, cv2.COLOR_RGB2BGR))
    print("Test screenshot saved as test_screenshot.png")
