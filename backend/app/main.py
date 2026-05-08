from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

print("BASE_DIR:", BASE_DIR)
print("ENV_PATH:", ENV_PATH)
print("EXISTS:", ENV_PATH.exists())

# пробуем загрузить
from dotenv import load_dotenv
load_dotenv(ENV_PATH)

print("IMAP:", os.getenv("IMAP_SERVER"))
print("USER:", os.getenv("EMAIL_USER"))

from app.services.message_reader import fetch_unread_emails

def main():

    print("ENV CHECK:")

    print("IMAP:", os.getenv("IMAP_SERVER"))

    print("USER:", os.getenv("EMAIL_USER"))

    print()

    emails = fetch_unread_emails(limit=5)

    print(f"Found {len(emails)} emails\n")

    for i, email_data in enumerate(emails, start=1):

        print(f"--- Email {i} ---")

        print("FROM:", email_data["from"])

        print("SUBJECT:", email_data["subject"])

        print("BODY:", email_data["body"][:200])

        print("-" * 40)

if __name__ == "__main__":

    main()