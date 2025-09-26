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
   pip install selenium
   ```
3. **Download ChromeDriver** matching your Chrome version and place it in `chrome-profile/` or specify the path in `read_whatsapp.py`.
4. **Configure chat name:**
   Edit `config.py` and set `chat_name` to the exact name of your WhatsApp chat/group.

## Usage
1. Run the script:
   ```powershell
   python read_whatsapp.py
   ```
2. On first run, scan the QR code in the browser to log in to WhatsApp Web.
3. The script will scroll and export messages from the configured chat to `messages.txt`.

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
