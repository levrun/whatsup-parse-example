#!/usr/bin/env python3
"""
PyWinAuto Examples for WhatsApp Desktop Automation
This file contains practical examples of how to use pywinauto with WhatsApp Desktop.
"""

from pywinauto.application import Application
from pywinauto import Desktop
import time

def connect_to_whatsapp():
    """Connect to or start WhatsApp Desktop application."""
    try:
        # Try to connect to existing WhatsApp instance
        app = Application(backend="uia").connect(title="WhatsApp")
        print("✓ Connected to running WhatsApp app.")
        return app
    except Exception as e:
        print(f"Could not connect to WhatsApp: {e}")
        print("Make sure WhatsApp Desktop is running and logged in.")
        return None

def inspect_whatsapp_ui(app):
    """Print all UI elements in WhatsApp for inspection."""
    if not app:
        return
    
    try:
        main_win = app.WhatsApp
        print("\n=== WhatsApp UI Elements ===")
        main_win.print_control_identifiers(depth=2)
    except Exception as e:
        print(f"Error inspecting UI: {e}")

def find_chat_by_name(app, chat_name):
    """Find and select a specific chat by name."""
    if not app:
        return None
    
    try:
        main_win = app.WhatsApp
        # Look for chat in the chat list
        chat_items = main_win.children(control_type="ListItem")
        
        for item in chat_items:
            if chat_name.lower() in item.window_text().lower():
                print(f"✓ Found chat: {item.window_text()}")
                return item
        
        print(f"✗ Chat '{chat_name}' not found")
        return None
    except Exception as e:
        print(f"Error finding chat: {e}")
        return None

def get_visible_messages(app):
    """Extract visible messages from the current chat."""
    if not app:
        return []
    
    try:
        main_win = app.WhatsApp
        messages = []
        
        # Find message containers (this may need adjustment based on WhatsApp's UI structure)
        text_elements = main_win.children(control_type="Text")
        
        for element in text_elements:
            text = element.window_text().strip()
            if text and len(text) > 2:  # Filter out empty or very short texts
                messages.append(text)
        
        return messages
    except Exception as e:
        print(f"Error getting messages: {e}")
        return []

def main():
    """Main example function demonstrating pywinauto usage."""
    print("=== PyWinAuto WhatsApp Desktop Examples ===\n")
    
    # Example 1: Connect to WhatsApp
    print("1. Connecting to WhatsApp Desktop...")
    app = connect_to_whatsapp()
    
    if not app:
        print("Cannot proceed without WhatsApp connection.")
        return
    
    # Example 2: Inspect UI elements
    print("\n2. Inspecting WhatsApp UI elements...")
    inspect_whatsapp_ui(app)
    
    # Example 3: Find a specific chat (from config.py)
    try:
        from config import chat_name
        print(f"\n3. Looking for chat: '{chat_name}'")
        chat = find_chat_by_name(app, chat_name)
        
        if chat:
            print("Clicking on the chat...")
            chat.click_input()
            time.sleep(2)
            
            # Example 4: Get visible messages
            print("\n4. Getting visible messages...")
            messages = get_visible_messages(app)
            
            print(f"Found {len(messages)} message elements:")
            for i, msg in enumerate(messages[:10]):  # Show first 10 messages
                print(f"  {i+1}. {msg[:100]}...")  # Truncate long messages
                
    except ImportError:
        print("No config.py found, skipping chat-specific examples")
    except Exception as e:
        print(f"Error in chat operations: {e}")

if __name__ == "__main__":
    main()