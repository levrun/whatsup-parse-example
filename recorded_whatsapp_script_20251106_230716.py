#!/usr/bin/env python3
"""
Auto-generated WhatsApp automation script
Generated on: 2025-11-06 23:07:16
Total actions recorded: 1
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

    # Action 1: Click recorded at 2025-11-06T23:07:20.621338
    try:
        # Try to find element by properties
        element = main_win.child_window(
            name='Thank you for sharing this. Wow. This is really inspiring. I really admire your courage and vulnerability to talk with your dad. Now I feel closer to you. Respect 🫡
',
            control_type='Text'
        )
        element.click_input()
        print('✓ Clicked on: Thank you for sharing this. Wow. This is really inspiring. I really admire your courage and vulnerability to talk with your dad. Now I feel closer to you. Respect 🫡
')
    except Exception:
        # Fallback: click by coordinates
        desktop.from_point(975, 862).click_input()
        print('✓ Clicked at coordinates (975, 862)')
    time.sleep(1)  # Wait between actions

    print("✓ All recorded actions completed")

if __name__ == '__main__':
    run_recorded_actions()