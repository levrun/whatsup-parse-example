#!/usr/bin/env python3
"""
Quick test of message selection functionality
"""

import pyperclip
import time
from pywinauto.application import Application

def test_selection():
    """Test if we can capture selected text from WhatsApp."""
    
    print("🧪 Testing WhatsApp message selection...")
    
    try:
        # Connect to WhatsApp
        app = Application(backend="uia").connect(title="WhatsApp")
        main_win = app.WhatsApp
        print("✅ Connected to WhatsApp Desktop")
        
        print("\n📋 Instructions:")
        print("1. Go to WhatsApp and select some text (click and drag)")
        print("2. Come back here and press Enter")
        
        input("Press Enter when you have selected text in WhatsApp...")
        
        # Clear clipboard
        pyperclip.copy("")
        time.sleep(0.1)
        
        # Copy selected text
        print("📋 Copying selected text...")
        main_win.type_keys("^c")
        time.sleep(0.3)
        
        # Get from clipboard
        selected_text = pyperclip.paste()
        
        if selected_text and selected_text.strip():
            print(f"✅ SUCCESS! Captured text:")
            print("-" * 50)
            print(selected_text.strip())
            print("-" * 50)
            print(f"Length: {len(selected_text.strip())} characters")
            
            # Save to file
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"test_selected_message_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Test Selected Message\n")
                f.write("=" * 20 + "\n")
                f.write(f"Captured at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 20 + "\n\n")
                f.write(selected_text.strip())
            
            print(f"💾 Saved to: {filename}")
            
        else:
            print("❌ No text captured")
            print("Make sure you selected text in WhatsApp before pressing Enter")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure WhatsApp Desktop is running")

if __name__ == "__main__":
    test_selection()