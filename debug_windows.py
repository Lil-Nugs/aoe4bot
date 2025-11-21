#!/usr/bin/env python3
"""Debug script to list all windows and find AoE4."""
import pygetwindow as gw

print("=" * 70)
print("All Windows:")
print("=" * 70)

all_windows = gw.getAllWindows()
for i, win in enumerate(all_windows):
    if win.title:  # Only show windows with titles
        try:
            title = win.title.encode('ascii', 'replace').decode('ascii')
            print(f"{i}: '{title}'")
            print(f"   Position: ({win.left}, {win.top})")
            print(f"   Size: {win.width}x{win.height}")
            print()
        except Exception as e:
            print(f"{i}: [Unable to display title - encoding error]")
            print()

print("=" * 70)
print("Searching for 'Age of Empires IV' windows:")
print("=" * 70)

aoe_windows = gw.getWindowsWithTitle("Age of Empires IV")
if aoe_windows:
    for i, win in enumerate(aoe_windows):
        print(f"{i}: '{win.title}'")
        print(f"   Position: ({win.left}, {win.top})")
        print(f"   Size: {win.width}x{win.height}")
        print(f"   Visible: {win.visible if hasattr(win, 'visible') else 'unknown'}")
        print()
else:
    print("No windows found with 'Age of Empires IV' in title")

print("\nTry different search terms:")
search_terms = ["Age of Empires", "AoE", "Empire"]
for term in search_terms:
    windows = gw.getWindowsWithTitle(term)
    if windows:
        print(f"\nFound {len(windows)} window(s) with '{term}':")
        for win in windows:
            print(f"  - '{win.title}' ({win.width}x{win.height})")
