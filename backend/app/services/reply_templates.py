
def confirmation_reply_de(data):

    return (

        f"Guten Tag, {data['salutation']} {data['last_name']},\n\n"
        f"Vielen Dank für Ihre Anfrage. "
        f"Wir bestätigen Ihre Reservierung am {data['date']} um {data['time']} Uhr "
        f"für {data['guests']} Personen.\n\n"
        f"Wir freuen uns, Sie bei uns begrüssen zu dürfen.\n\n"
        f"Freundliche Grüsse\n"
        f"Ihr Restaurant Team"

    )

def alternative_reply_de(data):

    return (

        f"Guten Tag, {data['salutation']} {data['last_name']},\n\n"
        f"Vielen Dank für Ihre Anfrage. "
        f"Leider haben wir am {data['date']} um {data['time']} Uhr "
        f"für {data['guests']} Personen keine Verfügbarkeit mehr.\n\n"
        f"Gerne können wir Ihnen eine alternative Zeit oder ein anderes Datum anbieten.\n\n"
        f"Freundliche Grüsse\n"
        f"Ihr Restaurant Team"

    )