#!/usr/bin/env python3
"""
Simple WhatsApp Message Extractor
Step-by-step guide to extract messages from WhatsApp
"""

import pyperclip
import time
from datetime import datetime

def manual_message_extractor():
    """Manual message extraction with clear instructions."""
    print("=" * 60)
    print("📱 SIMPLE WHATSAPP MESSAGE EXTRACTOR")
    print("=" * 60)
    
    extracted_messages = []
    
    print("""
🎯 HOW TO EXTRACT MESSAGES:

1. In WhatsApp Desktop:
   - Click and drag to select a message
   - Press Ctrl+C to copy it
   
2. Come back to this window
   - Press Enter to capture the copied message
   
3. Repeat for more messages
   
4. Type 'save' to save all messages
   Type 'quit' to exit
""")
    
    message_number = 1
    
    while True:
        command = input(f"\n[Message {message_number}] Press Enter after copying text (or 'save'/'quit'): ").strip().lower()
        
        if command == 'quit':
            break
        elif command == 'save':
            if extracted_messages:
                save_messages(extracted_messages)
            else:
                print("📭 No messages to save")
            continue
        
        # Try to get text from clipboard
        try:
            clipboard_text = pyperclip.paste()
            
            if clipboard_text and clipboard_text.strip() and len(clipboard_text.strip()) > 3:
                message_text = clipboard_text.strip()
                
                # Check if we already have this message
                if message_text not in [msg['text'] for msg in extracted_messages]:
                    message_info = {
                        'number': message_number,
                        'text': message_text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'length': len(message_text)
                    }
                    extracted_messages.append(message_info)
                    
                    print(f"✅ Captured Message {message_number}:")
                    print(f"   📝 {message_text[:80]}{'...' if len(message_text) > 80 else ''}")
                    print(f"   📊 Length: {len(message_text)} characters")
                    
                    message_number += 1
                else:
                    print("⚠️  This message was already captured")
            else:
                print("❌ No text found in clipboard")
                print("   Make sure you selected and copied text in WhatsApp (Ctrl+C)")
                
        except Exception as e:
            print(f"❌ Error reading clipboard: {e}")
    
    # Final save option
    if extracted_messages:
        save_choice = input(f"\n💾 Save {len(extracted_messages)} extracted messages? (y/n): ").strip().lower()
        if save_choice == 'y':
            save_messages(extracted_messages)
    
    print(f"\n✅ Session complete! Total messages extracted: {len(extracted_messages)}")

def save_messages(messages):
    """Save extracted messages to file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"extracted_whatsapp_messages_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("WhatsApp Extracted Messages\n")
            f.write("=" * 50 + "\n")
            f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total messages: {len(messages)}\n")
            f.write("=" * 50 + "\n\n")
            
            for message in messages:
                f.write(f"Message {message['number']:3d} | {message['timestamp']} | {message['length']} chars\n")
                f.write("-" * 70 + "\n")
                f.write(message['text'] + "\n")
                f.write("\n" + "=" * 70 + "\n\n")
        
        print(f"💾 Saved {len(messages)} messages to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving messages: {e}")
        return None

def show_clipboard_content():
    """Show current clipboard content."""
    try:
        content = pyperclip.paste()
        if content:
            print("📋 Current clipboard content:")
            print("-" * 30)
            print(content[:200] + ('...' if len(content) > 200 else ''))
            print("-" * 30)
            print(f"Length: {len(content)} characters")
        else:
            print("📋 Clipboard is empty")
    except Exception as e:
        print(f"❌ Error reading clipboard: {e}")

def main():
    """Main menu."""
    print("Choose an option:")
    print("1. Extract messages manually")
    print("2. Show current clipboard content")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        manual_message_extractor()
    elif choice == "2":
        show_clipboard_content()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()