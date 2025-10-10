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
