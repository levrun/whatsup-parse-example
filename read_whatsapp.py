
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Set up the Chrome WebDriver for Selenium 4+ with persistent profile
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument(r'--user-data-dir=c:/dev/ai/whatsup/chrome-profile')
service = Service('c:/dev/ai/whatsup/chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)


# Read chat name from config file
import importlib.util
import sys
config_path = 'c:/dev/ai/whatsup/config.py'
spec = importlib.util.spec_from_file_location('config', config_path)
config = importlib.util.module_from_spec(spec)
sys.modules['config'] = config
spec.loader.exec_module(config)
chat_name = config.chat_name

# Open WhatsApp Web
driver.get('https://web.whatsapp.com/')
print("Scan the QR code to log in...")




# Wait for user to scan QR code
time.sleep(20)

# Wait for the sidebar to appear (up to 60 seconds)
try:
    pane_side = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "pane-side"))
    )
    print("Sidebar loaded.")
except Exception as e:
    print("Sidebar did not load:", e)
    driver.quit()
    exit()






# Only select chat name spans, not message preview spans
chat_name_elements = driver.find_elements(By.XPATH, '//div[@id="pane-side"]//span[@title and not(@aria-label)]')

print(f"Found {len(chat_name_elements)} chat elements.")
# Save all chat names to chat_names.txt
with open('c:/dev/ai/whatsup/chat_names.txt', 'w', encoding='utf-8') as f:
    for chat in chat_name_elements:
        chat_title = chat.get_attribute('title')
        f.write(chat_title + '\n')

target_chat = None
for chat in chat_name_elements:
    if chat.get_attribute('title') == chat_name:
        target_chat = chat
        break

if target_chat:
    print(f"Opening chat: {chat_name}")
    target_chat.click()
    time.sleep(5)  # Wait for messages to load
    # Get all visible messages in the chat (try more flexible selector)
    message_containers = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')
    print(f"Found {len(message_containers)} message containers in CRT Level 2-5:")
    # Scroll up to load more messages (try alternative selectors)
    chat_area = None
    try:
        chat_area = driver.find_element(By.XPATH, '//div[@role="region" and @tabindex="-1"]')
    except Exception:
        try:
            chat_area = driver.find_element(By.XPATH, '//div[contains(@class, "_ak8h")]')
        except Exception:
            print("Could not find chat area for scrolling. Will print visible messages only.")

    if chat_area:
        for _ in range(5):
            driver.execute_script("arguments[0].scrollTop = 0;", chat_area)
            time.sleep(2)

    # Extract sender and message text/emoji from each container
    print(f"Found {len(message_containers)} message containers in CRT Level 2-5:")
    # Save messages to a txt file
    # Scroll up to load all messages
    chat_area = None
    try:
        chat_area = driver.find_element(By.XPATH, '//div[@role="region" and @tabindex="-1"]')
    except Exception:
        try:
            chat_area = driver.find_element(By.XPATH, '//div[contains(@class, "_ak8h")]')
        except Exception:
            print("Could not find chat area for scrolling. Will print visible messages only.")

    if chat_area:
        for _ in range(30):  # Scroll up 30 times to load more messages
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop - 1000;", chat_area)
            time.sleep(1)

    # After scrolling, fetch and process message containers
    message_containers = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')

    with open('c:/dev/ai/whatsup/messages.txt', 'w', encoding='utf-8') as f:
        for container in message_containers:
            # Sender name
            name_spans = container.find_elements(By.XPATH, './/span[contains(@class, "_ahxy")]')
            sender = name_spans[0].text if name_spans else None
            if sender:
                f.write(f"\n--- {sender} ---\n")
            # Message text and emoji
            message_spans = container.find_elements(By.XPATH, './/span[contains(@class, "_ao3e") and contains(@class, "selectable-text")]')
            for msg in message_spans:
                text = msg.text
                emojis = msg.find_elements(By.TAG_NAME, 'img')
                emoji_alts = [e.get_attribute('alt') for e in emojis if e.get_attribute('alt')]
                # Find date and time from data-pre-plain-text attribute in parent div
                parent_div = msg.find_element(By.XPATH, './ancestor::div[contains(@class, "copyable-text")]')
                pre_plain = parent_div.get_attribute('data-pre-plain-text') if parent_div else ''
                # Format: [HH:MM, YYYY-MM-DD] sender: 
                msg_time = ''
                msg_date = ''
                if pre_plain:
                    import re
                    match = re.match(r'\[(\d{2}:\d{2}), (\d{4}-\d{2}-\d{2})\]', pre_plain)
                    if match:
                        msg_time = match.group(1)
                        msg_date = match.group(2)
                if text:
                    f.write(f"[{msg_date} {msg_time}] {text}\n")
                if emoji_alts:
                    f.write('Emojis: ' + ' '.join(emoji_alts) + '\n')
    print('Messages saved to messages.txt')
else:
    print("Chat 'CRT Level 2-5' not found.")

# driver.quit()  # Commented out to keep the browser open
