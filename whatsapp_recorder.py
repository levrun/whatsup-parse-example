#!/usr/bin/env python3
"""
PyWinAuto Recorder for WhatsApp Desktop
This script helps you record interactions with WhatsApp and generate automation code.
"""

import time
import json
import os
import pyperclip
from datetime import datetime
from pywinauto.application import Application
from pywinauto import Desktop
import keyboard
import mouse

class WhatsAppRecorder:
    def __init__(self):
        self.recorded_actions = []
        self.app = None
        self.recording = False
        self.history_file = "recording_history.json"
        self.current_message = ""
        self.captured_text = []
        self.selected_messages = []
        
    def detect_selected_message(self):
        """Detect and capture selected message content."""
        if not self.app:
            print("❌ Not connected to WhatsApp")
            return None
        
        try:
            main_win = self.app.WhatsApp
            
            # Method 1: Try to get selected text from clipboard
            print("📋 Attempting to copy selected text...")
            
            # Clear clipboard first
            pyperclip.copy("")
            time.sleep(0.1)
            
            # Send Ctrl+C to copy selected text
            main_win.type_keys("^c")
            time.sleep(0.3)  # Wait longer for clipboard
            
            selected_text = pyperclip.paste()
            print(f"📋 Clipboard content: '{selected_text[:50]}...'")
            
            if selected_text and selected_text.strip() and len(selected_text.strip()) > 3:
                # Clean up the text and check if it's a message
                clean_text = selected_text.strip()
                
                # Check if we already have this message
                existing_texts = [item['text'] for item in self.selected_messages]
                if clean_text not in existing_texts:
                    message_info = {
                        'text': clean_text,
                        'timestamp': datetime.now().isoformat(),
                        'method': 'clipboard'
                    }
                    self.selected_messages.append(message_info)
                    print(f"✅ Captured selected message: {clean_text[:80]}...")
                    return message_info
                else:
                    print("⚠️  Message already captured")
                    return None
            else:
                print("❌ No meaningful text found in clipboard")
                
        except Exception as e:
            print(f"❌ Error in clipboard method: {e}")
        
        print("ℹ️  Tip: Make sure to select text in WhatsApp before pressing F1")
        return None
    
    def save_selected_messages(self):
        """Save selected messages to a file."""
        if not self.selected_messages:
            return None
        
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        selected_filename = f"selected_messages_{timestamp}.txt"
        
        try:
            with open(selected_filename, 'w', encoding='utf-8') as f:
                f.write("WhatsApp Selected Messages\n")
                f.write("=" * 30 + "\n")
                f.write(f"Recorded on: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total selected messages: {len(self.selected_messages)}\n")
                f.write("=" * 30 + "\n\n")
                
                for i, message in enumerate(self.selected_messages, 1):
                    f.write(f"{i:3d}. [{message['timestamp']}] [{message['method']}]\n")
                    f.write(f"     {message['text']}\n\n")
            
            print(f"📌 Selected messages saved to: {selected_filename}")
            return selected_filename
        except Exception as e:
            print(f"Error saving selected messages: {e}")
            return None
        
    def record_key_press(self, event):
        """Record keyboard input."""
        if not self.recording:
            return
        
        key_name = event.name
        
        # Special combination for capturing selected messages
        if key_name == 'f2':  # Changed from F1 to F2 to avoid conflicts
            print(f"🔍 F2 pressed - attempting to capture selected message...")
            message_info = self.detect_selected_message()
            if message_info:
                action = {
                    'type': 'selected_message',
                    'timestamp': datetime.now().isoformat(),
                    'text': message_info['text'],
                    'detection_method': message_info['method']
                }
                self.recorded_actions.append(action)
                print(f"✅ Successfully recorded selected message action")
            else:
                print(f"❌ Could not capture selected message - make sure text is selected first")
            return
        
        # Handle regular key presses
        if key_name == 'space':
            self.current_message += ' '
        elif key_name == 'backspace':
            if self.current_message:
                self.current_message = self.current_message[:-1]
        elif key_name == 'enter':
            if self.current_message.strip():
                # Save completed message
                action = {
                    'type': 'message',
                    'timestamp': datetime.now().isoformat(),
                    'text': self.current_message.strip()
                }
                self.recorded_actions.append(action)
                self.captured_text.append(self.current_message.strip())
                print(f"💬 Recorded message: {self.current_message.strip()[:50]}...")
                self.current_message = ""
        elif len(key_name) == 1 and key_name.isprintable():
            # Regular character
            self.current_message += key_name
        elif key_name in ['shift', 'ctrl', 'alt', 'tab', 'caps lock']:
            # Ignore modifier keys for message capture
            pass
        else:
            # Record special key as action
            action = {
                'type': 'keypress',
                'timestamp': datetime.now().isoformat(),
                'key': key_name
            }
            self.recorded_actions.append(action)
            print(f"⌨️  Recorded key: {key_name}")
    
    def save_captured_text(self):
        """Save captured text messages to a file."""
        if not self.captured_text:
            return None
        
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        text_filename = f"captured_messages_{timestamp}.txt"
        
        try:
            with open(text_filename, 'w', encoding='utf-8') as f:
                f.write("WhatsApp Captured Messages\n")
                f.write("=" * 30 + "\n")
                f.write(f"Recorded on: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total messages: {len(self.captured_text)}\n")
                f.write("=" * 30 + "\n\n")
                
                for i, message in enumerate(self.captured_text, 1):
                    f.write(f"{i:3d}. {message}\n")
            
            print(f"📝 Captured text saved to: {text_filename}")
            return text_filename
        except Exception as e:
            print(f"Error saving captured text: {e}")
            return None
        
    def load_history(self):
        """Load existing recording history."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Warning: Could not load history file: {e}")
            return []
    
    def save_to_history(self, session_info):
        """Save recording session to history file."""
        try:
            history = self.load_history()
            history.append(session_info)
            
            # Keep only last 50 sessions to prevent file from growing too large
            if len(history) > 50:
                history = history[-50:]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Recording session saved to history: {self.history_file}")
        except Exception as e:
            print(f"Warning: Could not save to history file: {e}")
    
    def show_last_recording(self):
        """Display information about the last recording session."""
        history = self.load_history()
        if not history:
            print("No recording history found.")
            return
        
        last_session = history[-1]
        print("\n" + "=" * 50)
        print("📝 LAST RECORDING SESSION")
        print("=" * 50)
        print(f"Date: {last_session['timestamp']}")
        print(f"Actions recorded: {last_session['action_count']}")
        print(f"Duration: {last_session.get('duration', 'Unknown')}")
        print(f"Script file: {last_session['script_file']}")
        print(f"Data file: {last_session['data_file']}")
        
        if last_session.get('actions_summary'):
            print("\nActions performed:")
            for i, action in enumerate(last_session['actions_summary'][:5], 1):
                print(f"  {i}. {action}")
            if len(last_session['actions_summary']) > 5:
                print(f"  ... and {len(last_session['actions_summary']) - 5} more actions")
    
    def show_recording_history(self):
        """Display all recording sessions."""
        history = self.load_history()
        if not history:
            print("No recording history found.")
            return
        
        print("\n" + "=" * 60)
        print("📚 RECORDING HISTORY")
        print("=" * 60)
        
        for i, session in enumerate(reversed(history[-10:]), 1):  # Show last 10 sessions
            print(f"\n{i:2d}. {session['timestamp']}")
            print(f"    Actions: {session['action_count']}, Duration: {session.get('duration', 'Unknown')}")
            print(f"    Script: {session['script_file']}")
            if session.get('actions_summary'):
                preview = session['actions_summary'][0] if session['actions_summary'] else "No actions"
                print(f"    First action: {preview[:60]}...")
        
        if len(history) > 10:
            print(f"\n... and {len(history) - 10} older sessions")
        
        print(f"\nTotal sessions recorded: {len(history)}")
        print(f"History file: {self.history_file}")
        
    def connect_to_whatsapp(self):
        """Connect to WhatsApp Desktop."""
        try:
            self.app = Application(backend="uia").connect(title="WhatsApp")
            print("✓ Connected to WhatsApp Desktop")
            return True
        except Exception as e:
            print(f"✗ Could not connect to WhatsApp: {e}")
            print("Please make sure WhatsApp Desktop is running and logged in.")
            return False
    
    def start_recording(self):
        """Start recording user interactions."""
        print("\n🔴 RECORDING STARTED")
        print("Instructions:")
        print("- Perform your WhatsApp actions (click chats, scroll, etc.)")
        print("- Type messages (they will be captured when you press Enter)")
        print("- Select a message and press F2 to capture selected text")
        print("- Press CTRL+R to stop recording")
        print("- Press ESC to cancel recording")
        print("-" * 50)
        
        self.recording = True
        self.recorded_actions = []
        self.current_message = ""
        self.captured_text = []
        self.selected_messages = []
        self.start_time = datetime.now()
        
        # Set up hotkeys
        keyboard.add_hotkey('ctrl+r', self.stop_recording)
        keyboard.add_hotkey('esc', self.cancel_recording)
        
        # Record mouse clicks
        mouse.on_click(self.record_mouse_click)
        
        # Record keyboard presses
        keyboard.hook(self.record_key_press)
        
        print("🎤 Keyboard recording active - type messages and they'll be captured!")
        print("📌 Press F2 after selecting a message to capture it!")
        
        # Keep recording until stopped
        while self.recording:
            time.sleep(0.1)
    
    def record_mouse_click(self):
        """Record mouse click events."""
        if not self.recording:
            return
            
        x, y = mouse.get_position()
        
        # Try to identify the UI element at this position
        try:
            desktop = Desktop(backend="uia")
            element = desktop.from_point(x, y)
            
            action = {
                'type': 'click',
                'timestamp': datetime.now().isoformat(),
                'position': {'x': x, 'y': y},
                'element_info': {
                    'control_type': element.element_info.control_type,
                    'name': element.element_info.name,
                    'automation_id': element.element_info.automation_id,
                    'class_name': element.element_info.class_name,
                }
            }
            
            self.recorded_actions.append(action)
            print(f"📍 Recorded click at ({x}, {y}) on {element.element_info.control_type}")
            
        except Exception as e:
            # Fallback: just record the coordinates
            action = {
                'type': 'click',
                'timestamp': datetime.now().isoformat(),
                'position': {'x': x, 'y': y},
                'element_info': None
            }
            self.recorded_actions.append(action)
            print(f"📍 Recorded click at ({x}, {y}) - element detection failed")
    
    def stop_recording(self):
        """Stop recording and generate script."""
        self.recording = False
        mouse.unhook_all()
        keyboard.unhook_all()
        
        # Save any remaining message being typed
        if self.current_message.strip():
            action = {
                'type': 'message',
                'timestamp': datetime.now().isoformat(),
                'text': self.current_message.strip()
            }
            self.recorded_actions.append(action)
            self.captured_text.append(self.current_message.strip())
            print(f"💬 Saved incomplete message: {self.current_message.strip()}")
        
        end_time = datetime.now()
        duration = str(end_time - self.start_time).split('.')[0]  # Remove microseconds
        
        print(f"\n🟢 RECORDING STOPPED - {len(self.recorded_actions)} actions recorded")
        print(f"� Messages typed: {len(self.captured_text)}")
        print(f"📌 Messages selected: {len(self.selected_messages)}")
        print(f"Recording duration: {duration}")
        
        if self.recorded_actions:
            script_file, data_file = self.generate_script()
            text_file = self.save_captured_text()
            selected_file = self.save_selected_messages()
            
            # Create session info for history
            session_info = {
                'timestamp': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
                'duration': duration,
                'action_count': len(self.recorded_actions),
                'message_count': len(self.captured_text),
                'selected_count': len(self.selected_messages),
                'script_file': script_file,
                'data_file': data_file,
                'text_file': text_file,
                'selected_file': selected_file,
                'actions_summary': [self.get_action_summary(action) for action in self.recorded_actions[:10]]
            }
            
            # Save to history
            self.save_to_history(session_info)
            
            # Show last recording info
            print("\n" + "=" * 50)
            print("📋 SESSION SUMMARY")
            print("=" * 50)
            print(f"Actions recorded: {len(self.recorded_actions)}")
            print(f"Messages typed: {len(self.captured_text)}")
            print(f"Messages selected: {len(self.selected_messages)}")
            print(f"Duration: {duration}")
            print(f"Script generated: {script_file}")
            print(f"Data saved: {data_file}")
            if text_file:
                print(f"Typed messages saved: {text_file}")
            if selected_file:
                print(f"Selected messages saved: {selected_file}")
                
            # Show captured messages preview
            if self.captured_text:
                print(f"\n💬 Typed messages preview:")
                for i, msg in enumerate(self.captured_text[:3], 1):
                    print(f"   {i}. {msg[:60]}{'...' if len(msg) > 60 else ''}")
                if len(self.captured_text) > 3:
                    print(f"   ... and {len(self.captured_text) - 3} more typed messages")
            
            # Show selected messages preview
            if self.selected_messages:
                print(f"\n📌 Selected messages preview:")
                for i, msg in enumerate(self.selected_messages[:3], 1):
                    print(f"   {i}. {msg['text'][:60]}{'...' if len(msg['text']) > 60 else ''}")
                if len(self.selected_messages) > 3:
                    print(f"   ... and {len(self.selected_messages) - 3} more selected messages")
        else:
            print("No actions were recorded.")
    
    def get_action_summary(self, action):
        """Create a human-readable summary of an action."""
        if action['type'] == 'click':
            if action.get('element_info') and action['element_info'].get('name'):
                element_name = action['element_info']['name'][:50]  # Truncate long names
                return f"Click on: {element_name}"
            else:
                return f"Click at ({action['position']['x']}, {action['position']['y']})"
        elif action['type'] == 'message':
            message_preview = action['text'][:50] + ('...' if len(action['text']) > 50 else '')
            return f"Typed: {message_preview}"
        elif action['type'] == 'selected_message':
            message_preview = action['text'][:50] + ('...' if len(action['text']) > 50 else '')
            return f"Selected: {message_preview}"
        elif action['type'] == 'keypress':
            return f"Key press: {action['key']}"
        return f"Unknown action: {action['type']}"
    
    def cancel_recording(self):
        """Cancel recording without generating script."""
        self.recording = False
        mouse.unhook_all()
        keyboard.unhook_all()
        
        print("\n🟡 RECORDING CANCELLED")
    
    def generate_script(self):
        """Generate Python script from recorded actions."""
        if not self.recorded_actions:
            print("No actions were recorded.")
            return None, None
        
        script_content = self.create_script_template()
        
        # Save the recorded script
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        script_filename = f"recorded_whatsapp_script_{timestamp}.py"
        data_filename = f"recorded_actions_{timestamp}.json"
        
        with open(script_filename, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Save raw data for debugging
        with open(data_filename, 'w', encoding='utf-8') as f:
            json.dump(self.recorded_actions, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Generated script: {script_filename}")
        print(f"✓ Raw data saved: {data_filename}")
        
        return script_filename, data_filename
        
    def create_script_template(self):
        """Create a Python script from recorded actions."""
        script_lines = [
            "#!/usr/bin/env python3",
            '"""',
            f"Auto-generated WhatsApp automation script",
            f"Generated on: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total actions recorded: {len(self.recorded_actions)}",
            '"""',
            "",
            "from pywinauto.application import Application",
            "from pywinauto import Desktop",
            "import time",
            "",
            "def run_recorded_actions():",
            '    """Execute the recorded WhatsApp actions."""',
            "    # Connect to WhatsApp",
            '    try:',
            '        app = Application(backend="uia").connect(title="WhatsApp")',
            '        print("✓ Connected to WhatsApp Desktop")',
            '    except Exception as e:',
            '        print(f"✗ Could not connect to WhatsApp: {e}")',
            '        return',
            "",
            "    main_win = app.WhatsApp",
            "    desktop = Desktop(backend='uia')",
            "",
            "    # Execute recorded actions",
        ]
        
        for i, action in enumerate(self.recorded_actions):
            if action['type'] == 'click':
                script_lines.extend(self.generate_click_code(action, i))
            elif action['type'] == 'message':
                script_lines.extend(self.generate_message_code(action, i))
            elif action['type'] == 'selected_message':
                script_lines.extend(self.generate_selected_message_code(action, i))
            elif action['type'] == 'keypress':
                script_lines.extend(self.generate_keypress_code(action, i))
        
        script_lines.extend([
            "",
            '    print("✓ All recorded actions completed")',
            "",
            "if __name__ == '__main__':",
            "    run_recorded_actions()"
        ])
        
        return '\n'.join(script_lines)
    
    def generate_click_code(self, action, index):
        """Generate Python code for a click action."""
        lines = [
            f"",
            f"    # Action {index + 1}: Click recorded at {action['timestamp']}"
        ]
        
        if action['element_info'] and action['element_info']['name']:
            # Try to click by element name/properties
            element_info = action['element_info']
            lines.extend([
                f"    try:",
                f"        # Try to find element by properties",
                f"        element = main_win.child_window(",
                f"            name='{element_info['name']}',",
                f"            control_type='{element_info['control_type']}'",
                f"        )",
                f"        element.click_input()",
                f"        print('✓ Clicked on: {element_info['name']}')",
                f"    except Exception:",
                f"        # Fallback: click by coordinates",
                f"        desktop.from_point({action['position']['x']}, {action['position']['y']}).click_input()",
                f"        print('✓ Clicked at coordinates ({action['position']['x']}, {action['position']['y']})')",
                f"    time.sleep(1)  # Wait between actions"
            ])
        else:
            # Click by coordinates only
            lines.extend([
                f"    desktop.from_point({action['position']['x']}, {action['position']['y']}).click_input()",
                f"    print('✓ Clicked at coordinates ({action['position']['x']}, {action['position']['y']})')",
                f"    time.sleep(1)  # Wait between actions"
            ])
        
        return lines
    
    def generate_message_code(self, action, index):
        """Generate Python code for typing a message."""
        message = action['text'].replace("'", "\\'")  # Escape single quotes
        lines = [
            f"",
            f"    # Action {index + 1}: Type message recorded at {action['timestamp']}",
            f"    try:",
            f"        # Find the message input box and type the message",
            f"        input_box = main_win.child_window(control_type='Edit')",
            f"        input_box.click_input()",
            f"        input_box.type_keys('{message}')",
            f"        print('✓ Typed message: {message[:50]}{'...' if len(message) > 50 else ''}')",
            f"    except Exception as e:",
            f"        print(f'✗ Could not type message: {{e}}')",
            f"    time.sleep(1)  # Wait between actions"
        ]
        return lines
    
    def generate_keypress_code(self, action, index):
        """Generate Python code for a key press."""
        key = action['key']
        lines = [
            f"",
            f"    # Action {index + 1}: Key press '{key}' recorded at {action['timestamp']}",
            f"    try:",
            f"        # Send key press to the active window",
            f"        main_win.type_keys('{{{key.upper()}}}')",
            f"        print('✓ Pressed key: {key}')",
            f"    except Exception as e:",
            f"        print(f'✗ Could not press key {key}: {{e}}')",
            f"    time.sleep(0.5)  # Wait between key presses"
        ]
        return lines
    
    def generate_selected_message_code(self, action, index):
        """Generate Python code for capturing selected message."""
        expected_text = action['text'][:30].replace("'", "\\'")  # Truncate and escape
        lines = [
            f"",
            f"    # Action {index + 1}: Capture selected message recorded at {action['timestamp']}",
            f"    try:",
            f"        # Method 1: Try to get selected text via clipboard",
            f"        import pyperclip",
            f"        main_win.type_keys('^c')  # Ctrl+C to copy",
            f"        time.sleep(0.2)",
            f"        selected_text = pyperclip.paste()",
            f"        if selected_text and '{expected_text}' in selected_text:",
            f"            print(f'✓ Captured selected message: {{selected_text[:50]}}...')",
            f"            # Save to file or process as needed",
            f"        else:",
            f"            print('⚠️  Selected text may have changed')",
            f"    except Exception as e:",
            f"        print(f'✗ Could not capture selected message: {{e}}')",
            f"    time.sleep(1)  # Wait between actions"
        ]
        return lines

def manual_inspector():
    """Manual UI element inspector."""
    print("\n🔍 MANUAL UI INSPECTOR")
    print("This will help you identify WhatsApp UI elements manually.")
    print("-" * 50)
    
    try:
        app = Application(backend="uia").connect(title="WhatsApp")
        main_win = app.WhatsApp
        
        print("✓ Connected to WhatsApp Desktop")
        print("\nAvailable UI elements:")
        print("=" * 30)
        main_win.print_control_identifiers(depth=3)
        
        # Interactive element finder
        print("\n" + "=" * 50)
        print("INTERACTIVE ELEMENT FINDER")
        print("Enter element properties to find specific controls:")
        
        while True:
            element_name = input("\nEnter element name (or 'quit' to exit): ").strip()
            if element_name.lower() == 'quit':
                break
                
            try:
                elements = main_win.children(name=element_name)
                if elements:
                    print(f"Found {len(elements)} elements with name '{element_name}':")
                    for i, elem in enumerate(elements):
                        info = elem.element_info
                        print(f"  {i+1}. Type: {info.control_type}, ID: {info.automation_id}")
                else:
                    print(f"No elements found with name '{element_name}'")
            except Exception as e:
                print(f"Error searching for element: {e}")
                
    except Exception as e:
        print(f"✗ Could not connect to WhatsApp: {e}")

def main():
    """Main recorder interface."""
    print("=" * 60)
    print("🎬 WhatsApp Desktop Recorder & Inspector")
    print("=" * 60)
    
    recorder = WhatsAppRecorder()
    
    print("\nChoose an option:")
    print("1. Record interactions (creates automated script)")
    print("2. Manual UI inspector (explore WhatsApp elements)")
    print("3. View last recording")
    print("4. View recording history")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            if recorder.connect_to_whatsapp():
                recorder.start_recording()
            break
            
        elif choice == "2":
            manual_inspector()
            break
            
        elif choice == "3":
            recorder.show_last_recording()
            
        elif choice == "4":
            recorder.show_recording_history()
            
        elif choice == "5":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1-5.")
            
        # Allow user to continue after viewing history
        if choice in ["3", "4"]:
            input("\nPress Enter to return to main menu...")
            print("\nChoose an option:")
            print("1. Record interactions (creates automated script)")
            print("2. Manual UI inspector (explore WhatsApp elements)")
            print("3. View last recording")
            print("4. View recording history")
            print("5. Exit")

if __name__ == "__main__":
    main()