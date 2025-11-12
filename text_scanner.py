#!/usr/bin/env python3
"""
WhatsApp Window Text Scanner
Scans the entire WhatsApp window for visible text
"""

from pywinauto.application import Application
import time
from datetime import datetime
import re

def scan_whatsapp_window():
    """Scan WhatsApp window for all visible text."""
    print("🔍 Scanning WhatsApp window for text...")
    
    try:
        # Connect to WhatsApp
        app = Application(backend="uia").connect(title="WhatsApp")
        main_win = app.WhatsApp
        print("✅ Connected to WhatsApp Desktop")
        
        print("📋 Scanning all text elements...")
        
        # Get all descendants and their text
        all_texts = []
        elements = main_win.descendants()
        
        print(f"📊 Found {len(elements)} UI elements to check")
        
        for i, element in enumerate(elements):
            try:
                text = element.window_text()
                if text and len(text.strip()) > 5:
                    all_texts.append({
                        'text': text.strip(),
                        'control_type': element.element_info.control_type,
                        'index': i
                    })
                    
                # Show progress every 100 elements
                if i % 100 == 0:
                    print(f"   Processed {i}/{len(elements)} elements...")
                    
            except Exception:
                continue
        
        print(f"📝 Found {len(all_texts)} text elements")
        
        # Filter and display potential messages
        messages = []
        for item in all_texts:
            text = item['text']
            
            # Filter for message-like content
            if (len(text) > 20 and
                not text.startswith(('WhatsApp', 'Search', 'Type a message')) and
                not re.match(r'^\d{1,2}:\d{2}', text)):
                
                messages.append(text)
        
        print(f"🎯 Identified {len(messages)} potential messages:")
        print("=" * 80)
        
        for i, msg in enumerate(messages, 1):
            print(f"\nMessage {i:3d}:")
            print("-" * 40)
            print(msg[:200] + "..." if len(msg) > 200 else msg)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whatsapp_scan_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("WhatsApp Window Text Scan\n")
            f.write("=" * 30 + "\n")
            f.write(f"Scanned on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total potential messages: {len(messages)}\n")
            f.write("=" * 30 + "\n\n")
            
            for i, msg in enumerate(messages, 1):
                f.write(f"Message {i:3d}:\n")
                f.write("-" * 20 + "\n")
                f.write(msg + "\n")
                f.write("\n" + "=" * 50 + "\n\n")
        
        print(f"\n💾 All text saved to: {filename}")
        
        return messages
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def inspect_whatsapp_structure():
    """Inspect WhatsApp UI structure to understand layout."""
    print("🔍 Inspecting WhatsApp UI structure...")
    
    try:
        app = Application(backend="uia").connect(title="WhatsApp")
        main_win = app.WhatsApp
        
        print("📋 WhatsApp UI Structure:")
        main_win.print_control_identifiers(depth=3)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def live_text_monitor():
    """Monitor WhatsApp text in real-time."""
    print("🔴 Starting live text monitor...")
    print("Press Ctrl+C to stop")
    
    try:
        app = Application(backend="uia").connect(title="WhatsApp")
        main_win = app.WhatsApp
        
        previous_texts = set()
        
        while True:
            try:
                # Get current texts
                current_texts = set()
                elements = main_win.descendants()
                
                for element in elements:
                    try:
                        text = element.window_text()
                        if text and len(text.strip()) > 20:
                            current_texts.add(text.strip())
                    except:
                        continue
                
                # Find new texts
                new_texts = current_texts - previous_texts
                
                if new_texts:
                    print(f"\n🆕 New text detected at {datetime.now().strftime('%H:%M:%S')}:")
                    for text in new_texts:
                        print(f"   📝 {text[:100]}...")
                
                previous_texts = current_texts
                time.sleep(2)  # Check every 2 seconds
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️  Error in monitoring: {e}")
                time.sleep(5)
                
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main menu."""
    print("=" * 60)
    print("🔍 WHATSAPP TEXT SCANNER")
    print("=" * 60)
    
    print("Choose scanning method:")
    print("1. Full window text scan (one-time)")
    print("2. Inspect UI structure")
    print("3. Live text monitor (real-time)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        scan_whatsapp_window()
    elif choice == "2":
        inspect_whatsapp_structure()
    elif choice == "3":
        live_text_monitor()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()