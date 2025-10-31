#!/usr/bin/env python3
"""
PyWinAuto Recorder for WhatsApp Desktop
This script helps you record interactions with WhatsApp and generate automation code.
"""

import time
import json
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
        print("- Press CTRL+R to stop recording")
        print("- Press ESC to cancel recording")
        print("-" * 50)
        
        self.recording = True
        self.recorded_actions = []
        
        # Set up hotkeys
        keyboard.add_hotkey('ctrl+r', self.stop_recording)
        keyboard.add_hotkey('esc', self.cancel_recording)
        
        # Record mouse clicks
        mouse.on_click(self.record_mouse_click)
        
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
        
        print(f"\n🟢 RECORDING STOPPED - {len(self.recorded_actions)} actions recorded")
        self.generate_script()
    
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
            return
        
        script_content = self.create_script_template()
        
        # Save the recorded script
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recorded_whatsapp_script_{timestamp}.py"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Save raw data for debugging
        data_filename = f"recorded_actions_{timestamp}.json"
        with open(data_filename, 'w', encoding='utf-8') as f:
            json.dump(self.recorded_actions, f, indent=2)
        
        print(f"✓ Generated script: {filename}")
        print(f"✓ Raw data saved: {data_filename}")
        
    def create_script_template(self):
        """Create a Python script from recorded actions."""
        script_lines = [
            "#!/usr/bin/env python3",
            '"""',
            f"Auto-generated WhatsApp automation script",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
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
    
    print("\nChoose an option:")
    print("1. Record interactions (creates automated script)")
    print("2. Manual UI inspector (explore WhatsApp elements)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            recorder = WhatsAppRecorder()
            if recorder.connect_to_whatsapp():
                recorder.start_recording()
            break
            
        elif choice == "2":
            manual_inspector()
            break
            
        elif choice == "3":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()