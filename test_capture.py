#!/usr/bin/env python3
"""Test screen capture functionality on 4K monitor."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_interface import GameInterface
import cv2
import time

def main():
    print("=" * 60)
    print("AoE4 Bot - Screen Capture Test")
    print("=" * 60)

    # Initialize game interface
    print("\n[1/4] Initializing game interface...")
    interface = GameInterface()

    print(f"✓ Detected screen size: {interface.screen_width}x{interface.screen_height}")

    # Test full screen capture
    print("\n[2/4] Capturing full screen...")
    start_time = time.time()
    state = interface.get_game_state()
    capture_time = (time.time() - start_time) * 1000  # Convert to ms

    print(f"✓ Screenshot captured in {capture_time:.2f}ms")
    print(f"✓ Screenshot shape: {state.screenshot.shape}")
    print(f"✓ Screenshot dtype: {state.screenshot.dtype}")

    # Save full screenshot
    print("\n[3/4] Saving full screenshot...")
    output_path = "data/test_fullscreen.png"
    os.makedirs("data", exist_ok=True)
    cv2.imwrite(output_path, cv2.cvtColor(state.screenshot, cv2.COLOR_RGB2BGR))
    print(f"✓ Saved to: {output_path}")

    # Test region capture (minimap area for 4K)
    print("\n[4/4] Testing region capture (minimap area)...")
    minimap_region = interface.capture_region(0, 0, 400, 400)
    minimap_path = "data/test_minimap.png"
    cv2.imwrite(minimap_path, cv2.cvtColor(minimap_region, cv2.COLOR_RGB2BGR))
    print(f"✓ Minimap region saved to: {minimap_path}")
    print(f"✓ Minimap shape: {minimap_region.shape}")

    # Performance test
    print("\n" + "=" * 60)
    print("Performance Test (10 captures)")
    print("=" * 60)

    times = []
    for i in range(10):
        start = time.time()
        _ = interface.capture_screen()
        times.append((time.time() - start) * 1000)

    print(f"Average capture time: {sum(times)/len(times):.2f}ms")
    print(f"Min: {min(times):.2f}ms | Max: {max(times):.2f}ms")
    print(f"FPS equivalent: {1000/(sum(times)/len(times)):.1f} captures/second")

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check the saved screenshots in the 'data/' directory")
    print("2. If you have AoE4 running, the full screenshot should show the game")
    print("3. We can now calibrate UI positions for your 4K setup")

if __name__ == "__main__":
    main()
