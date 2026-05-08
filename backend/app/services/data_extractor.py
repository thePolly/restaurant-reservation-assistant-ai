import re


def extract_guests(email_text: str):
    patterns = [
        r"für\s+(\d+)\s+(personen|person|gäste|gästen)",
        r"(\d+)\s+(personen|person|gäste|gästen)",
        r"table\s+for\s+(\d+)",
        r"for\s+(\d+)\s+people",
    ]

    text = email_text.lower()

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))

    return None


def extract_time(email_text: str):
    patterns = [
        r"um\s+(\d{1,2})[:.](\d{2})",
        r"um\s+(\d{1,2})\s*uhr",
        r"at\s+(\d{1,2})[:.](\d{2})",
    ]

    text = email_text.lower()

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            if len(match.groups()) == 2:
                return f"{match.group(1).zfill(2)}:{match.group(2)}"
            return f"{match.group(1).zfill(2)}:00"

    return None


def extract_last_name(email_text: str):
    patterns = [
        r"name[:\s]+([A-ZÄÖÜ][a-zäöüß]+)",
        r"Grüsse\s+([A-ZÄÖÜ][a-zäöüß]+)",
        r"freundliche grüsse\s+([A-ZÄÖÜ][a-zäöüß]+)",
        r"freundliche grüße\s+([A-ZÄÖÜ][a-zäöüß]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, email_text)
        if match:
            return match.group(1)

    return None


def extract_phone(email_text: str):
    pattern = r"(\+?\d[\d\s]{7,}\d)"
    match = re.search(pattern, email_text)

    if match:
        return match.group(1).strip()

    return None


def extract_salutation(email_text: str):
    text = email_text.lower()

    if "frau" in text:
        return "Frau"

    if "herr" in text:
        return "Herr"

    return None


def extract_reservation_data(email_text: str):
    data = {
        "salutation": extract_salutation(email_text),
        "last_name": extract_last_name(email_text),
        "phone": extract_phone(email_text),
        "date": None,  # later: AI or date parser
        "time": extract_time(email_text),
        "guests": extract_guests(email_text),
        "special_requests": None,
    }

    missing_fields = [
        field for field in ["last_name", "date", "time", "guests"]
        if data[field] is None
    ]

    data["needs_ai"] = len(missing_fields) > 0
    data["missing_fields"] = missing_fields

    return data