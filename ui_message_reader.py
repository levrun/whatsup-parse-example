#!/usr/bin/env python3
"""
Direct WhatsApp UI Message Reader
Uses pywinauto to directly read messages from WhatsApp's UI elements
"""

from pywinauto.application import Application
from pywinauto import Desktop
import time
from datetime import datetime
import re

class WhatsAppUIReader:
    def __init__(self):
        self.app = None
        self.main_win = None
        self.extracted_messages = []
    
    def connect_to_whatsapp(self):
        """Connect to WhatsApp Desktop."""
        try:
            self.app = Application(backend="uia").connect(title="WhatsApp")
            self.main_win = self.app.WhatsApp
            print("✅ Connected to WhatsApp Desktop")
            return True
        except Exception as e:
            print(f"❌ Could not connect to WhatsApp: {e}")
            return False
    
    def scan_all_ui_elements(self):
        """Scan all UI elements and find potential messages."""
        print("🔍 Scanning WhatsApp UI elements...")
        
        try:
            # Get all text elements from the main window
            all_elements = self.main_win.descendants()
            message_candidates = []
            
            for element in all_elements:
                try:
                    # Get element text
                    text = element.window_text()
                    
                    if text and len(text.strip()) > 10:  # Filter for meaningful text
                        element_info = {
                            'text': text.strip(),
                            'control_type': element.element_info.control_type,
                            'automation_id': getattr(element.element_info, 'automation_id', ''),
                            'class_name': getattr(element.element_info, 'class_name', ''),
                            'rectangle': element.rectangle()
                        }
                        message_candidates.append(element_info)
                        
                except Exception:
                    continue
            
            print(f"📊 Found {len(message_candidates)} potential message elements")
            return message_candidates
            
        except Exception as e:
            print(f"❌ Error scanning UI: {e}")
            return []
    
    def filter_messages(self, candidates):
        """Filter candidates to find actual messages."""
        print("🔽 Filtering for actual messages...")
        
        messages = []
        seen_texts = set()
        
        for candidate in candidates:
            text = candidate['text']
            
            # Skip duplicates
            if text in seen_texts:
                continue
            
            # Filter criteria for messages
            if (len(text) > 20 and  # Reasonable length
                not text.startswith('WhatsApp') and  # Not app title
                not text.startswith('Search') and  # Not search box
                not re.match(r'^\d{1,2}:\d{2}$', text) and  # Not just time
                'automation_id' in candidate):  # Has some structure
                
                messages.append({
                    'text': text,
                    'timestamp': datetime.now().isoformat(),
                    'ui_info': candidate
                })
                seen_texts.add(text)
        
        print(f"📝 Identified {len(messages)} potential messages")
        return messages
    
    def get_message_area_elements(self):
        """Focus on the message area specifically."""
        print("🎯 Looking for message area...")
        
        try:
            # Try to find common message area identifiers
            message_containers = []
            
            # Method 1: Find by common class names or automation IDs
            potential_containers = [
                "message", "bubble", "chat", "conversation", 
                "MessageList", "BubbleList", "ChatArea"
            ]
            
            for container_id in potential_containers:
                try:
                    elements = self.main_win.descendants(auto_id=container_id)
                    message_containers.extend(elements)
                except:
                    pass
                
                try:
                    elements = self.main_win.descendants(class_name=container_id)
                    message_containers.extend(elements)
                except:
                    pass
            
            # Method 2: Find ListItems which often contain messages
            try:
                list_items = self.main_win.descendants(control_type="ListItem")
                print(f"📋 Found {len(list_items)} list items")
                
                messages = []
                for item in list_items:
                    try:
                        text = item.window_text()
                        if text and len(text.strip()) > 15:
                            # Try to extract message content
                            clean_text = self.clean_message_text(text)
                            if clean_text:
                                messages.append({
                                    'text': clean_text,
                                    'raw_text': text,
                                    'timestamp': datetime.now().isoformat(),
                                    'source': 'ListItem'
                                })
                    except:
                        continue
                
                return messages
                
            except Exception as e:
                print(f"⚠️  Error finding list items: {e}")
                return []
                
        except Exception as e:
            print(f"❌ Error finding message area: {e}")
            return []
    
    def clean_message_text(self, raw_text):
        """Clean and extract actual message content."""
        try:
            # Remove timestamp patterns
            text = re.sub(r'\d{1,2}:\d{2}\s*(AM|PM)?', '', raw_text)
            
            # Remove sender name patterns (Name:)
            text = re.sub(r'^[^:]+:\s*', '', text)
            
            # Remove "Edited" markers
            text = re.sub(r',?\s*Edited\s*,?', '', text)
            
            # Remove status indicators
            text = re.sub(r'\s*(✓|✓✓)\s*$', '', text)
            
            # Clean up whitespace
            text = ' '.join(text.split())
            
            # Return if meaningful content remains
            if len(text.strip()) > 10:
                return text.strip()
            
            return None
            
        except:
            return None
    
    def extract_messages_interactive(self):
        """Interactive message extraction with real-time scanning."""
        if not self.connect_to_whatsapp():
            return
        
        print("\n" + "=" * 60)
        print("🎯 INTERACTIVE UI MESSAGE EXTRACTION")
        print("=" * 60)
        
        while True:
            print(f"\nCurrent extracted messages: {len(self.extracted_messages)}")
            print("Options:")
            print("1. Scan current view for messages")
            print("2. Show extracted messages")
            print("3. Save messages to file")
            print("4. Clear extracted messages")
            print("5. Exit")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == "1":
                # Scan for messages
                messages = self.get_message_area_elements()
                
                if messages:
                    print(f"\n📊 Found {len(messages)} potential messages:")
                    for i, msg in enumerate(messages[:10], 1):
                        preview = msg['text'][:80] + "..." if len(msg['text']) > 80 else msg['text']
                        print(f"   {i:2d}. {preview}")
                    
                    if len(messages) > 10:
                        print(f"   ... and {len(messages) - 10} more messages")
                    
                    # Ask which messages to extract
                    extract_choice = input(f"\nExtract all {len(messages)} messages? (y/n/select): ").strip().lower()
                    
                    if extract_choice == 'y':
                        # Add all unique messages
                        new_count = 0
                        for msg in messages:
                            if msg['text'] not in [m['text'] for m in self.extracted_messages]:
                                self.extracted_messages.append(msg)
                                new_count += 1
                        print(f"✅ Added {new_count} new messages")
                        
                    elif extract_choice == 'select':
                        # Let user select specific messages
                        indices = input("Enter message numbers (e.g., 1,3,5-8): ").strip()
                        selected_messages = self.parse_message_selection(indices, messages)
                        
                        new_count = 0
                        for msg in selected_messages:
                            if msg['text'] not in [m['text'] for m in self.extracted_messages]:
                                self.extracted_messages.append(msg)
                                new_count += 1
                        print(f"✅ Added {new_count} selected messages")
                else:
                    print("❌ No messages found in current view")
                    print("💡 Try scrolling or opening a different chat")
            
            elif choice == "2":
                self.show_extracted_messages()
            
            elif choice == "3":
                if self.extracted_messages:
                    self.save_messages()
                else:
                    print("📭 No messages to save")
            
            elif choice == "4":
                self.extracted_messages = []
                print("🗑️  Cleared all extracted messages")
            
            elif choice == "5":
                break
            
            else:
                print("❌ Invalid choice")
    
    def parse_message_selection(self, selection_string, messages):
        """Parse user selection like '1,3,5-8' into message list."""
        selected = []
        
        try:
            parts = selection_string.split(',')
            for part in parts:
                if '-' in part:
                    # Range selection
                    start, end = map(int, part.split('-'))
                    for i in range(start-1, min(end, len(messages))):
                        if 0 <= i < len(messages):
                            selected.append(messages[i])
                else:
                    # Single selection
                    index = int(part) - 1
                    if 0 <= index < len(messages):
                        selected.append(messages[index])
        except:
            print("❌ Invalid selection format")
        
        return selected
    
    def show_extracted_messages(self):
        """Display all extracted messages."""
        if not self.extracted_messages:
            print("📭 No messages extracted yet")
            return
        
        print(f"\n📝 EXTRACTED MESSAGES ({len(self.extracted_messages)} total)")
        print("=" * 60)
        
        for i, msg in enumerate(self.extracted_messages, 1):
            print(f"\nMessage {i:3d} | {msg.get('source', 'Unknown')} | {len(msg['text'])} chars")
            print("-" * 50)
            print(msg['text'])
            
        print("\n" + "=" * 60)
    
    def save_messages(self):
        """Save extracted messages to file."""
        if not self.extracted_messages:
            print("📭 No messages to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whatsapp_ui_messages_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("WhatsApp Messages - Direct UI Extraction\n")
                f.write("=" * 50 + "\n")
                f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total messages: {len(self.extracted_messages)}\n")
                f.write("Method: Direct UI element reading\n")
                f.write("=" * 50 + "\n\n")
                
                for i, message in enumerate(self.extracted_messages, 1):
                    f.write(f"Message {i:3d} | {message.get('source', 'Unknown')} | {len(message['text'])} chars\n")
                    f.write(f"Timestamp: {message['timestamp']}\n")
                    f.write("-" * 70 + "\n")
                    f.write(message['text'] + "\n")
                    f.write("\n" + "=" * 70 + "\n\n")
            
            print(f"💾 Saved {len(self.extracted_messages)} messages to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving messages: {e}")
            return None

def main():
    """Main function."""
    print("=" * 60)
    print("📱 WHATSAPP DIRECT UI MESSAGE READER")
    print("=" * 60)
    print("This tool reads messages directly from WhatsApp's UI elements")
    print("No clipboard or selection needed!")
    
    reader = WhatsAppUIReader()
    reader.extract_messages_interactive()

if __name__ == "__main__":
    main()