from pywinauto.application import Application
from pywinauto import Desktop
import time

# Path to WhatsApp Desktop app (default install location)
# If installed from Microsoft Store, use 'WhatsApp.exe' and let pywinauto find it
app_path = r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe"

# Start WhatsApp (or connect if already running)
try:
    app = Application(backend="uia").connect(path="WhatsApp.exe")
    print("Connected to running WhatsApp app.")
except Exception:
    app = Application(backend="uia").start(app_path)
    print("Started WhatsApp app.")
    time.sleep(5)
    app = Application(backend="uia").connect(path="WhatsApp.exe")

# Get the main window using Desktop object
main_win = Desktop(backend="uia").window(title="WhatsApp")
main_win.set_focus()