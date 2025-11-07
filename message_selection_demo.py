#!/usr/bin/env python3
"""
Message Selection Demo
Demonstrates how to use the WhatsApp recorder to capture selected messages.
"""

import pyperclip
from pywinauto.application import Application
from pywinauto import Desktop
import time

def demo_message_selection():
    """Demo script showing how to select and capture messages."""
    print("🎬 WhatsApp Message Selection Demo")
    print("=" * 40)
    
    try:
        # Connect to WhatsApp
        app = Application(backend="uia").connect(title="WhatsApp")
        main_win = app.WhatsApp
        print("✓ Connected to WhatsApp Desktop")
        
        print("\nInstructions:")
        print("1. Navigate to a chat with messages")
        print("2. Click and drag to select a message")
        print("3. Press Enter in this console to capture the selection")
        print("4. Type 'quit' to exit")
        
        while True:
            user_input = input("\nPress Enter to capture selected text (or 'quit' to exit): ")
            
            if user_input.lower() == 'quit':
                break
                
            try:
                # Copy selected text to clipboard
                main_win.type_keys("^c")
                time.sleep(0.2)
                
                # Get text from clipboard
                selected_text = pyperclip.paste()
                
                if selected_text and selected_text.strip():
                    print(f"\n📋 Captured text:")
                    print("-" * 30)
                    print(selected_text.strip())
                    print("-" * 30)
                    
                    # Save to file
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"demo_selected_message_{timestamp}.txt"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("WhatsApp Selected Message Demo\n")
                        f.write("=" * 30 + "\n")
                        f.write(f"Captured at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 30 + "\n\n")
                        f.write(selected_text.strip())
                    
                    print(f"💾 Saved to: {filename}")
                    
                else:
                    print("❌ No text selected or clipboard empty")
                    print("Try selecting some text in WhatsApp first")
                    
            except Exception as e:
                print(f"❌ Error capturing selection: {e}")
    
    except Exception as e:
        print(f"❌ Could not connect to WhatsApp: {e}")
        print("Make sure WhatsApp Desktop is running")

def test_clipboard():
    """Simple clipboard test."""
    print("\n🧪 Clipboard Test")
    print("-" * 20)
    
    # Test writing to clipboard
    test_text = "Hello from Python!"
    pyperclip.copy(test_text)
    print(f"✓ Copied to clipboard: {test_text}")
    
    # Test reading from clipboard
    clipboard_content = pyperclip.paste()
    print(f"✓ Read from clipboard: {clipboard_content}")
    
    if test_text == clipboard_content:
        print("✅ Clipboard test passed!")
    else:
        print("❌ Clipboard test failed!")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Demo message selection with WhatsApp")
    print("2. Test clipboard functionality")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        demo_message_selection()
    elif choice == "2":
        test_clipboard()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice")