#!/usr/bin/env python3
"""
WhatsApp Message Extractor
A simple tool to extract selected messages from WhatsApp Desktop
"""

import pyperclip
import time
import keyboard
from datetime import datetime
from pywinauto.application import Application

class MessageExtractor:
    def __init__(self):
        self.extracted_messages = []
        self.app = None
        self.running = False
    
    def connect_to_whatsapp(self):
        """Connect to WhatsApp Desktop."""
        try:
            self.app = Application(backend="uia").connect(title="WhatsApp")
            print("✅ Connected to WhatsApp Desktop")
            return True
        except Exception as e:
            print(f"❌ Could not connect to WhatsApp: {e}")
            print("Please make sure WhatsApp Desktop is running and logged in.")
            return False
    
    def extract_selected_message(self):
        """Extract currently selected message."""
        try:
            if not self.app:
                print("❌ Not connected to WhatsApp")
                return
            
            main_win = self.app.WhatsApp
            
            # Method 1: Use Ctrl+C to copy selected text
            print("📋 Copying selected text...")
            main_win.type_keys("^c")  # Ctrl+C
            time.sleep(0.3)  # Wait for clipboard
            
            # Get text from clipboard
            selected_text = pyperclip.paste()
            
            if selected_text and selected_text.strip():
                message_text = selected_text.strip()
                
                # Check if we already have this message
                if message_text not in [msg['text'] for msg in self.extracted_messages]:
                    message_info = {
                        'text': message_text,
                        'timestamp': datetime.now().isoformat(),
                        'length': len(message_text)
                    }
                    self.extracted_messages.append(message_info)
                    
                    print(f"✅ Extracted message #{len(self.extracted_messages)}:")
                    print(f"   📝 {message_text[:100]}{'...' if len(message_text) > 100 else ''}")
                    print(f"   📊 Length: {len(message_text)} characters")
                else:
                    print("⚠️  Message already extracted")
            else:
                print("❌ No text selected or clipboard empty")
                print("   Try selecting a message in WhatsApp first")
        
        except Exception as e:
            print(f"❌ Error extracting message: {e}")
    
    def save_messages(self):
        """Save extracted messages to file."""
        if not self.extracted_messages:
            print("📭 No messages to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"extracted_whatsapp_messages_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("WhatsApp Extracted Messages\n")
                f.write("=" * 50 + "\n")
                f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total messages: {len(self.extracted_messages)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, message in enumerate(self.extracted_messages, 1):
                    f.write(f"Message {i:3d} | {message['timestamp']} | {message['length']} chars\n")
                    f.write("-" * 80 + "\n")
                    f.write(message['text'] + "\n")
                    f.write("\n" + "=" * 80 + "\n\n")
            
            print(f"💾 Saved {len(self.extracted_messages)} messages to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving messages: {e}")
            return None
    
    def start_interactive_extraction(self):
        """Start interactive message extraction."""
        if not self.connect_to_whatsapp():
            return
        
        self.running = True
        
        print("\n" + "=" * 60)
        print("🎯 INTERACTIVE MESSAGE EXTRACTION MODE")
        print("=" * 60)
        print("Instructions:")
        print("1. Go to WhatsApp and select a message (click and drag)")
        print("2. Press SPACE to extract the selected message")
        print("3. Press S to save all extracted messages")
        print("4. Press Q to quit")
        print("-" * 60)
        
        # Set up hotkeys
        keyboard.add_hotkey('space', self.extract_selected_message)
        keyboard.add_hotkey('s', self.save_messages)
        keyboard.add_hotkey('q', self.quit_extraction)
        
        print("🎤 Hotkeys active! Select messages in WhatsApp and press SPACE")
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            keyboard.unhook_all()
            print("\n✅ Message extraction stopped")
    
    def quit_extraction(self):
        """Stop the extraction process."""
        self.running = False
        print(f"\n🛑 Stopping extraction... {len(self.extracted_messages)} messages extracted")

def manual_extraction():
    """Manual step-by-step extraction."""
    extractor = MessageExtractor()
    
    if not extractor.connect_to_whatsapp():
        return
    
    print("\n" + "=" * 60)
    print("📋 MANUAL MESSAGE EXTRACTION")
    print("=" * 60)
    print("Instructions:")
    print("1. Select a message in WhatsApp (click and drag to highlight)")
    print("2. Come back here and press Enter")
    print("3. Repeat for more messages")
    print("4. Type 'save' to save all messages")
    print("5. Type 'quit' to exit")
    print("-" * 60)
    
    while True:
        command = input(f"\n[{len(extractor.extracted_messages)} messages] Press Enter to extract selected message (or 'save'/'quit'): ").strip().lower()
        
        if command == 'quit':
            break
        elif command == 'save':
            extractor.save_messages()
        else:
            extractor.extract_selected_message()
    
    if extractor.extracted_messages:
        save_choice = input(f"\nSave {len(extractor.extracted_messages)} extracted messages? (y/n): ").strip().lower()
        if save_choice == 'y':
            extractor.save_messages()

def main():
    """Main menu."""
    print("=" * 60)
    print("📱 WHATSAPP MESSAGE EXTRACTOR")
    print("=" * 60)
    print("Choose extraction method:")
    print("1. Interactive mode (use SPACE key)")
    print("2. Manual mode (step by step)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        extractor = MessageExtractor()
        extractor.start_interactive_extraction()
    elif choice == "2":
        manual_extraction()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()