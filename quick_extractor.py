#!/usr/bin/env python3
"""
Quick WhatsApp Message Extractor
Simple and direct approach to extract messages from WhatsApp
"""

from pywinauto.application import Application
from datetime import datetime
import time

def quick_extract():
    """Quick extraction of WhatsApp messages."""
    print("🚀 Quick WhatsApp Message Extractor")
    print("=" * 40)
    
    try:
        # Connect to WhatsApp
        print("🔌 Connecting to WhatsApp...")
        app = Application(backend="uia").connect(title="WhatsApp")
        main_win = app.WhatsApp
        print("✅ Connected!")
        
        # Method 1: Get all ListItems (most likely to contain messages)
        print("📋 Scanning for messages...")
        
        messages = []
        
        # Try different element types that might contain messages
        element_types = ["ListItem", "Text", "Edit", "Document"]
        
        for element_type in element_types:
            try:
                elements = main_win.descendants(control_type=element_type)
                print(f"   Found {len(elements)} {element_type} elements")
                
                for element in elements:
                    try:
                        text = element.window_text()
                        if text and len(text.strip()) > 20:
                            # Basic filtering
                            clean_text = text.strip()
                            if (not clean_text.startswith(('Search', 'Type', 'WhatsApp')) and
                                len(clean_text) > 25 and
                                clean_text not in messages):
                                messages.append(clean_text)
                    except:
                        continue
                        
            except Exception as e:
                print(f"   ⚠️  Error with {element_type}: {e}")
        
        # Remove duplicates and sort by length (longer texts are more likely to be messages)
        unique_messages = list(set(messages))
        unique_messages.sort(key=len, reverse=True)
        
        print(f"🎯 Found {len(unique_messages)} potential messages")
        
        if unique_messages:
            print("\n📝 TOP 10 EXTRACTED MESSAGES:")
            print("=" * 60)
            
            for i, msg in enumerate(unique_messages[:10], 1):
                preview = msg[:100] + "..." if len(msg) > 100 else msg
                print(f"\n{i:2d}. [{len(msg)} chars] {preview}")
            
            if len(unique_messages) > 10:
                print(f"\n... and {len(unique_messages) - 10} more messages")
            
            # Save to file
            save_choice = input(f"\n💾 Save all {len(unique_messages)} messages to file? (y/n): ")
            if save_choice.lower() == 'y':
                save_messages(unique_messages)
        else:
            print("❌ No messages found")
            print("💡 Try opening a chat with messages visible")
        
        return unique_messages
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def save_messages(messages):
    """Save messages to file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quick_extracted_messages_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("WhatsApp Quick Extraction\n")
            f.write("=" * 30 + "\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Messages: {len(messages)}\n")
            f.write("=" * 30 + "\n\n")
            
            for i, msg in enumerate(messages, 1):
                f.write(f"Message {i:3d} ({len(msg)} chars):\n")
                f.write("-" * 40 + "\n")
                f.write(msg + "\n")
                f.write("\n" + "=" * 50 + "\n\n")
        
        print(f"✅ Saved to: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Error saving: {e}")
        return None

def inspect_elements():
    """Quick inspection of WhatsApp elements."""
    print("🔍 Inspecting WhatsApp UI...")
    
    try:
        app = Application(backend="uia").connect(title="WhatsApp")
        main_win = app.WhatsApp
        
        print("📊 Element counts:")
        
        element_types = [
            "ListItem", "Text", "Edit", "Document", "Button", 
            "Image", "Group", "Pane", "List", "ScrollBar"
        ]
        
        for elem_type in element_types:
            try:
                elements = main_win.descendants(control_type=elem_type)
                print(f"   {elem_type:12} : {len(elements):4d} elements")
            except:
                print(f"   {elem_type:12} : ERROR")
        
        print("\n🎯 Looking for message-like elements...")
        
        # Focus on ListItems as they often contain messages
        try:
            list_items = main_win.descendants(control_type="ListItem")
            print(f"\n📋 Found {len(list_items)} ListItems:")
            
            for i, item in enumerate(list_items[:5]):  # Show first 5
                try:
                    text = item.window_text()
                    if text:
                        preview = text[:80] + "..." if len(text) > 80 else text
                        print(f"   {i+1:2d}. {preview}")
                except:
                    print(f"   {i+1:2d}. [Could not read text]")
                    
            if len(list_items) > 5:
                print(f"   ... and {len(list_items) - 5} more items")
                
        except Exception as e:
            print(f"❌ Error inspecting ListItems: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function."""
    print("Choose an option:")
    print("1. Quick extract messages")
    print("2. Inspect UI elements")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        quick_extract()
    elif choice == "2":
        inspect_elements()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()