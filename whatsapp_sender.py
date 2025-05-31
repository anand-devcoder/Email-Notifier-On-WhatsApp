from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, RECIPIENT_WHATSAPP_NUMBER

def send_whatsapp_message(sender, subject, body, datetime, attachments=None):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Construct initial message without body
    message_header = f"""📧 *New Email Received!*

*From:* {sender}
*Subject:* {subject}
*Received At:* {datetime}

*Message:*
"""
    attachment_text = ""
    if attachments:
        attachment_text = "\n📎 *Attachments:*\n" + "\n".join(f"- {att}" for att in attachments)

    # Calculate remaining allowed length for the body
    max_length = 1590  # Reserve a bit under 1600 for safety
    remaining = max_length - len(message_header) - len(attachment_text)

    if len(body) > remaining:
        body = body[:remaining - 20] + "\n\n[Message truncated]"

    # Final message
    message = message_header + body + attachment_text

    # Send WhatsApp message
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=RECIPIENT_WHATSAPP_NUMBER
    )
