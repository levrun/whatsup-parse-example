#!/usr/bin/env python3
"""
Auto-generated WhatsApp automation script
Generated on: 2025-11-04 23:17:13
Total actions recorded: 2
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

    # Action 1: Click recorded at 2025-11-04T23:17:17.693143
    try:
        # Try to find element by properties
        element = main_win.child_window(
            name='WhatsApp',
            control_type='Window'
        )
        element.click_input()
        print('✓ Clicked on: WhatsApp')
    except Exception:
        # Fallback: click by coordinates
        desktop.from_point(810, 973).click_input()
        print('✓ Clicked at coordinates (810, 973)')
    time.sleep(1)  # Wait between actions

    # Action 2: Click recorded at 2025-11-04T23:17:18.717954
    try:
        # Try to find element by properties
        element = main_win.child_window(
            name='It’s in the CRT cuddle puddle chat. You can find the details discussed there so far.
',
            control_type='Text'
        )
        element.click_input()
        print('✓ Clicked on: It’s in the CRT cuddle puddle chat. You can find the details discussed there so far.
')
    except Exception:
        # Fallback: click by coordinates
        desktop.from_point(894, 885).click_input()
        print('✓ Clicked at coordinates (894, 885)')
    time.sleep(1)  # Wait between actions

    print("✓ All recorded actions completed")

if __name__ == '__main__':
    run_recorded_actions()