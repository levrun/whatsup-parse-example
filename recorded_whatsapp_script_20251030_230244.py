#!/usr/bin/env python3
"""
Auto-generated WhatsApp automation script
Generated on: 2025-10-30 23:02:44
Total actions recorded: 3
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

    # Action 1: Click recorded at 2025-10-30T23:02:27.473296
    try:
        # Try to find element by properties
        element = main_win.child_window(
            name='🦋🦄🐝Mariam🦋🐛🌻🦢🪶🕊: I think it would be super fun if we at some point had a CRT gala/ award night where we (read:Phil) rents out the Orpheum Theatre for a night and we all dress up hella fancy in ball gowns and tuxedos (the orpheum is so decadent 😍). We can pre-vote for winners in different categories (most deleted posts, most invisible, most attention seeking etc) and award each winner and they have to do an impromptu shadow speech 😏😂, Edited, ‎10‎:‎42‎ ‎PM',
            control_type='ListItem'
        )
        element.click_input()
        print('✓ Clicked on: 🦋🦄🐝Mariam🦋🐛🌻🦢🪶🕊: I think it would be super fun if we at some point had a CRT gala/ award night where we (read:Phil) rents out the Orpheum Theatre for a night and we all dress up hella fancy in ball gowns and tuxedos (the orpheum is so decadent 😍). We can pre-vote for winners in different categories (most deleted posts, most invisible, most attention seeking etc) and award each winner and they have to do an impromptu shadow speech 😏😂, Edited, ‎10‎:‎42‎ ‎PM')
    except Exception:
        # Fallback: click by coordinates
        desktop.from_point(737, 850).click_input()
        print('✓ Clicked at coordinates (737, 850)')
    time.sleep(1)  # Wait between actions

    # Action 2: Click recorded at 2025-10-30T23:02:28.688599
    try:
        # Try to find element by properties
        element = main_win.child_window(
            name='CRT Level 2-5 🦋🦄🐝Mariam🦋🐛🌻🦢🪶🕊 I think it would be super fun if we at some point had a CRT gala/ award night where we (read:Phil) rents out the Orpheum Theatre for a night and we all dress up hella fancy in ball gowns and tuxedos (the orpheum is so decadent 😍). We can pre-vote for winners in different categories (most deleted posts, most invisible, most attention seeking etc) and award each winner and they have to do an impromptu shadow speech 😏😂',
            control_type='ListItem'
        )
        element.click_input()
        print('✓ Clicked on: CRT Level 2-5 🦋🦄🐝Mariam🦋🐛🌻🦢🪶🕊 I think it would be super fun if we at some point had a CRT gala/ award night where we (read:Phil) rents out the Orpheum Theatre for a night and we all dress up hella fancy in ball gowns and tuxedos (the orpheum is so decadent 😍). We can pre-vote for winners in different categories (most deleted posts, most invisible, most attention seeking etc) and award each winner and they have to do an impromptu shadow speech 😏😂')
    except Exception:
        # Fallback: click by coordinates
        desktop.from_point(240, 246).click_input()
        print('✓ Clicked at coordinates (240, 246)')
    time.sleep(1)  # Wait between actions

    # Action 3: Click recorded at 2025-10-30T23:02:29.932736
    try:
        # Try to find element by properties
        element = main_win.child_window(
            name='🦋🦄🐝Mariam🦋🐛🌻🦢🪶🕊: I think it would be super fun if we at some point had a CRT gala/ award night where we (read:Phil) rents out the Orpheum Theatre for a night and we all dress up hella fancy in ball gowns and tuxedos (the orpheum is so decadent 😍). We can pre-vote for winners in different categories (most deleted posts, most invisible, most attention seeking etc) and award each winner and they have to do an impromptu shadow speech 😏😂, Edited, ‎10‎:‎42‎ ‎PM',
            control_type='ListItem'
        )
        element.click_input()
        print('✓ Clicked on: 🦋🦄🐝Mariam🦋🐛🌻🦢🪶🕊: I think it would be super fun if we at some point had a CRT gala/ award night where we (read:Phil) rents out the Orpheum Theatre for a night and we all dress up hella fancy in ball gowns and tuxedos (the orpheum is so decadent 😍). We can pre-vote for winners in different categories (most deleted posts, most invisible, most attention seeking etc) and award each winner and they have to do an impromptu shadow speech 😏😂, Edited, ‎10‎:‎42‎ ‎PM')
    except Exception:
        # Fallback: click by coordinates
        desktop.from_point(736, 818).click_input()
        print('✓ Clicked at coordinates (736, 818)')
    time.sleep(1)  # Wait between actions

    print("✓ All recorded actions completed")

if __name__ == '__main__':
    run_recorded_actions()