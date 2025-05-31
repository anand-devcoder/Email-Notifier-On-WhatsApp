![photo_2025-05-31_12-24-53](https://github.com/user-attachments/assets/88739373-d9cc-45c2-8fef-178c257e4eca)
📧🔔 Project: Email Notification on WhatsApp<br><br>
✅ Overview:<br>
This project automates the process of forwarding incoming email notifications directly to WhatsApp in real-time. It is built using Python, IMAP for email reading, and Twilio’s WhatsApp API to send messages. The goal is to keep users instantly informed about important emails without constantly checking their inbox.
<br><br>
🔧 Key Features:<br>
✅ Real-time monitoring of incoming emails using IMAP.
<br>
✅ Extracts email details: Sender, Subject, Body, and Date/Time.
<br>
✅ Sends formatted notifications to a specified WhatsApp number via Twilio.
<br>
✅ Supports Gmail with 2FA, using app-specific password or OAuth2.
<br>
✅ Option to detect and forward image attachments from emails.
<br><br>
🖼️ Image Handling:<br>
The script checks for image attachments (e.g., .jpg, .png, .jpeg) in incoming emails.
<br>
It downloads the image temporarily and sends it via WhatsApp using Twilio's media URL feature.
<br>
Optional: Store the image to a local folder and serve via a static URL or upload it to a cloud storage (like Imgur, AWS S3) for sharing.
<br><br>
⚙️ Tech Stack:<br>
Python (IMAPClient, email, Twilio)
<br>
Twilio API (WhatsApp sandbox for development)
<br>
Gmail IMAP or any IMAP-supported service
