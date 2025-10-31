# WhatsApp Chat Reader

This app allows you to read and export messages from a WhatsApp Web chat using Python and Selenium.

## Features
- Select a chat by name (configured in `config.py`)
- Export all visible messages with sender, date, time, text, and emojis
- Save messages to `messages.txt`
- Persistent login using a Chrome profile (no need to scan QR code every run)

## Setup
1. **Install Python 3.13+**
2. **Install dependencies:**
   ```powershell
   # For WhatsApp Web method
   pip install selenium
   
   # For WhatsApp Desktop method (Windows only)
   pip install pywinauto
   ```
3. **Download ChromeDriver** matching your Chrome version and place it in `chrome-profile/` or specify the path in `read_whatsapp.py` (only needed for web method).
4. **Configure chat name:**
   Edit `config.py` and set `chat_name` to the exact name of your WhatsApp chat/group.

## Usage

### Method 1: WhatsApp Web (Browser-based)
1. Run the script:
   ```powershell
   python read_whatsapp.py
   ```
2. On first run, scan the QR code in the browser to log in to WhatsApp Web.
3. The script will scroll and export messages from the configured chat to `messages.txt`.

### Method 2: WhatsApp Desktop App (Windows only)
This method uses the native WhatsApp Desktop application instead of the web version.

**Prerequisites:**
- Windows operating system
- WhatsApp Desktop app installed (download from Microsoft Store or WhatsApp.com)
- Python package `pywinauto` installed:
  ```powershell
  pip install pywinauto
  ```

**Usage:**
1. Make sure WhatsApp Desktop is installed and you're logged in
2. Run the desktop script:
   ```powershell
   python read_whatsapp_desktop.py
   ```
3. The script will connect to or start the WhatsApp Desktop app and focus on the main window

**Note:** The desktop script currently provides the foundation for automating WhatsApp Desktop. You may need to extend it to add specific chat selection and message extraction functionality similar to the web version.

**Using Recorder Tools for Development:**
To help create or extend the WhatsApp Desktop automation, you can use several recording approaches:

### Method 1: Interactive Recorder (Recommended)
```powershell
# Install recorder dependencies
pip install keyboard mouse

# Run the interactive recorder
python whatsapp_recorder.py
```

This tool offers:
- **Real-time recording**: Records your mouse clicks and generates Python code
- **UI element detection**: Automatically identifies clicked elements
- **Script generation**: Creates ready-to-run automation scripts
- **Manual inspector**: Explore WhatsApp UI elements interactively

### Method 2: Code Generator & Inspector
```powershell
# Run the code generator and inspector
python simple_recorder.py
```

This provides:
- **UI element exploration**: Lists all available WhatsApp controls
- **Code snippet generation**: Creates common automation code patterns
- **Template creation**: Generates complete automation script templates

### Method 3: Built-in PyWinAuto Inspector
```powershell
# Launch visual inspector
python -c "from pywinauto import inspect; inspect.main()"
```

### Recording Workflow:
1. **Start recording**: Run `python whatsapp_recorder.py` and choose option 1
2. **Perform actions**: Click on chats, scroll through messages, etc.
3. **Stop recording**: Press `Ctrl+R` to generate the automation script
4. **Review & customize**: Edit the generated script for your needs
5. **Test automation**: Run your generated script

The recorder will create files like:
- `recorded_whatsapp_script_YYYYMMDD_HHMMSS.py` - Executable automation script
- `recorded_actions_YYYYMMDD_HHMMSS.json` - Raw recording data for debugging

## How to Run Pywinauto

### Basic Usage Examples:

**1. Inspect WhatsApp Desktop Elements:**
```powershell
# Run this to explore WhatsApp UI elements
python -c "from pywinauto import Application; from pywinauto.application import Application; app = Application(backend='uia').connect(title='WhatsApp'); app.WhatsApp.print_control_identifiers()"
```

**2. Use Built-in Inspector:**
```powershell
# Launch pywinauto inspector to visually explore UI elements
python -c "from pywinauto import inspector; inspector.main()"
```

**3. Test Your Script:**
```powershell
# Run your WhatsApp automation
python read_whatsapp_desktop.py

# Or run the comprehensive examples file
python pywinauto_examples.py
```

**4. Interactive Development:**
```python
# Open Python interpreter and test commands interactively
python
>>> from pywinauto.application import Application
>>> from pywinauto import Desktop
>>> app = Application(backend="uia").connect(title="WhatsApp")
>>> main_win = app.WhatsApp
>>> main_win.print_control_identifiers()  # See all available controls
```

### Common Pywinauto Commands for WhatsApp:

```python
# Connect to WhatsApp
app = Application(backend="uia").connect(title="WhatsApp")
main_win = app.WhatsApp

# Find and click a chat (replace "Chat Name" with actual chat name)
chat = main_win.child_window(title="Chat Name", control_type="ListItem")
chat.click_input()

# Scroll in chat area
chat_area = main_win.child_window(control_type="List")
chat_area.scroll('up', 'page', 5)  # Scroll up 5 pages

# Get message text
messages = main_win.children(control_type="Text")
for msg in messages:
    print(msg.window_text())
```

## Notes
- The script uses a persistent Chrome profile (`chrome-profile/`) so you only need to log in once.
- Change the chat by editing `config.py`.
- Output is saved to `messages.txt`.
- Sensitive files and folders are excluded from git via `.gitignore`.

## Troubleshooting
- If messages are not exported, check your ChromeDriver version and chat name spelling.
- For more messages, increase the scroll count in the script.
- If WhatsApp Web layout changes, you may need to update selectors in the script.

## License
MIT
