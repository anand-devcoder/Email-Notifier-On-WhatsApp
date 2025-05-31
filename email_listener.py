import imaplib
import email
from email.header import decode_header
from datetime import datetime
import os
import json
from bs4 import BeautifulSoup
from whatsapp_sender import send_whatsapp_message
from config import EMAIL, EMAIL_PASSWORD, IMAP_SERVER

LOG_FILE = "logs/email_log.json"
MAX_BODY_LENGTH = 1500  # Twilio limit safeguard

def clean_text(text):
    if isinstance(text, bytes):
        return text.decode("utf-8", errors="ignore")
    return str(text).strip()

def log_email_to_json(data):
    os.makedirs("logs", exist_ok=True)

    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(LOG_FILE, "r+", encoding="utf-8") as file:
        try:
            existing = json.load(file)
        except json.JSONDecodeError:
            existing = []

        existing.append(data)
        file.seek(0)
        json.dump(existing, file, indent=4, ensure_ascii=False)

def check_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        if status != "OK":
            print("No new emails found.")
            return

        mail_ids = messages[0].split()

        for i in mail_ids:
            res, msg_data = mail.fetch(i, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    try:
                        msg = email.message_from_bytes(response[1])

                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8", errors="ignore")

                        from_ = msg.get("From")
                        date_ = msg.get("Date")
                        dt = datetime.now().isoformat()

                        body = ""
                        attachments = []

                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))

                                # Extract attachments
                                if "attachment" in content_disposition:
                                    filename = part.get_filename()
                                    if filename:
                                        decoded_filename, enc = decode_header(filename)[0]
                                        if isinstance(decoded_filename, bytes):
                                            decoded_filename = decoded_filename.decode(enc or "utf-8", errors="ignore")
                                        attachments.append(decoded_filename)

                                # Extract plain text
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    try:
                                        body = part.get_payload(decode=True).decode(errors="ignore").strip()
                                    except:
                                        body = ""

                                # Fallback to HTML if plain not found
                                elif content_type == "text/html" and not body:
                                    try:
                                        html_content = part.get_payload(decode=True).decode(errors="ignore")
                                        soup = BeautifulSoup(html_content, "html.parser")
                                        body = soup.get_text().strip()
                                    except:
                                        body = ""
                        else:
                            content_type = msg.get_content_type()
                            payload = msg.get_payload(decode=True)
                            if content_type == "text/plain":
                                body = payload.decode(errors="ignore").strip()
                            elif content_type == "text/html":
                                html_content = payload.decode(errors="ignore")
                                soup = BeautifulSoup(html_content, "html.parser")
                                body = soup.get_text().strip()

                        clean_body = clean_text(body)

                        # Handle Twilio message length limit
                        if len(clean_body) > MAX_BODY_LENGTH:
                            clean_body = clean_body[:MAX_BODY_LENGTH] + "\n\n[Message truncated due to size limit]"

                        log_entry = {
                            "from": clean_text(from_),
                            "subject": clean_text(subject),
                            "body": clean_body,
                            "datetime": dt,
                        }

                        if attachments:
                            log_entry["attachments"] = attachments

                        log_email_to_json(log_entry)

                        send_whatsapp_message(
                            sender=clean_text(from_),
                            subject=clean_text(subject),
                            body=clean_body,
                            datetime=dt,
                            attachments=attachments
                        )

                    except Exception as e:
                        print(f"Error parsing email: {e}")

        mail.logout()

    except Exception as e:
        print(f"IMAP Error: {e}")
