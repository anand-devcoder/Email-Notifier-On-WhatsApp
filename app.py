import time
from email_listener import check_emails

print("📬 Email to WhatsApp Notifier Running...")

while True:
    try:
        check_emails()
        time.sleep(15)  # check every 15 seconds
    except Exception as e:
        print("Error:", e)
