import os
import smtplib
from email.message import EmailMessage



def send_email_reply(to_email: str, subject: str, body: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    print("SMTP_SERVER:", repr(smtp_server))

    print("SMTP_PORT:", repr(smtp_port))

    print("EMAIL_USER:", repr(email_user))

    if not smtp_server or not email_user or not email_password:
        raise ValueError("SMTP settings are missing")

    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=20) as server:
        server.login(email_user, email_password)
        server.send_message(msg)


    return True