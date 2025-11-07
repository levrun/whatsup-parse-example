#!/usr/bin/env python3
"""
Auto-generated WhatsApp automation script
Generated on: 2025-11-06 23:23:20
Total actions recorded: 6
"""

from pywinauto.application import Application
from pywinauto import Desktop
import time

def run_recorded_actions():
    """Execute the recorded WhatsApp actions."""
    # Connect to WhatsApp
    try:
        app = Application(backend="uia").connect(title="WhatsApp")
        print("✓ Connected to WhatsApp Desktop")
    except Exception as e:
        print(f"✗ Could not connect to WhatsApp: {e}")
        return

    main_win = app.WhatsApp
    desktop = Desktop(backend='uia')

    # Execute recorded actions

    # Action 1: Key press 'up' recorded at 2025-11-06T23:23:23.006976
    try:
        # Send key press to the active window
        main_win.type_keys('{UP}')
        print('✓ Pressed key: up')
    except Exception as e:
        print(f'✗ Could not press key up: {e}')
    time.sleep(0.5)  # Wait between key presses

    # Action 2: Key press 'up' recorded at 2025-11-06T23:23:23.176842
    try:
        # Send key press to the active window
        main_win.type_keys('{UP}')
        print('✓ Pressed key: up')
    except Exception as e:
        print(f'✗ Could not press key up: {e}')
    time.sleep(0.5)  # Wait between key presses

    # Action 3: Key press 'up' recorded at 2025-11-06T23:23:23.742481
    try:
        # Send key press to the active window
        main_win.type_keys('{UP}')
        print('✓ Pressed key: up')
    except Exception as e:
        print(f'✗ Could not press key up: {e}')
    time.sleep(0.5)  # Wait between key presses

    # Action 4: Key press 'up' recorded at 2025-11-06T23:23:23.895942
    try:
        # Send key press to the active window
        main_win.type_keys('{UP}')
        print('✓ Pressed key: up')
    except Exception as e:
        print(f'✗ Could not press key up: {e}')
    time.sleep(0.5)  # Wait between key presses

    # Action 5: Key press 'up' recorded at 2025-11-06T23:23:24.426915
    try:
        # Send key press to the active window
        main_win.type_keys('{UP}')
        print('✓ Pressed key: up')
    except Exception as e:
        print(f'✗ Could not press key up: {e}')
    time.sleep(0.5)  # Wait between key presses

    # Action 6: Key press 'up' recorded at 2025-11-06T23:23:24.569098
    try:
        # Send key press to the active window
        main_win.type_keys('{UP}')
        print('✓ Pressed key: up')
    except Exception as e:
        print(f'✗ Could not press key up: {e}')
    time.sleep(0.5)  # Wait between key presses

    print("✓ All recorded actions completed")

if __name__ == '__main__':
    run_recorded_actions()