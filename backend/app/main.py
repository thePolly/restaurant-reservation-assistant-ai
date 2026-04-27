from services.reply_templates import confirmation_reply_de

data = {

    "salutation": "Herr",
    "last_name": "Müller",
    "date": "27.04.2026",
    "time": "19:00",
    "guests": 4

}

print(confirmation_reply_de(data))