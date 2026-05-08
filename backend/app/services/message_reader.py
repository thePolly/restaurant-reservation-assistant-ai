import imaplib
import email
import os
from email.utils import parseaddr


def fetch_unread_emails(limit: int = 3):
    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"))
    mail.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    email_ids = email_ids[-limit:]

    results = []

    for e_id in reversed(email_ids):
        _, msg_data = mail.fetch(e_id, "(BODY.PEEK[])")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                subject = msg.get("Subject", "")
                from_raw = msg.get("From", "")
                sender_name, sender_email = parseaddr(from_raw)

                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode(errors="ignore")
                                break
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode(errors="ignore")

                results.append({
                    "id": e_id.decode(),
                    "from": from_raw,
                    "sender_email": sender_email,
                    "subject": subject,
                    "body": body
                })

    mail.logout()
    return results