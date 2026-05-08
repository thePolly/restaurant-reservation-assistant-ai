# Reply Generation API Documentation

## Overview
The backend provides three REST endpoints for generating reply messages to reservation requests. These endpoints use pre-defined templates and populate them with reservation details provided by the frontend.

## Endpoints

### 1. Generate Reply (Generic)
**POST** `/replies/generate`

Generate a reply based on specified type (accept or alternative).

**Request Body:**
```json
{
  "salutation": "Herr",
  "last_name": "Müller",
  "date": "15. September 2025",
  "time": "19:00",
  "guests": 4,
  "reply_type": "accept"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Reply generated successfully as accept",
  "reply_text": "Guten Tag, Herr Müller,\n\nVielen Dank für Ihre Anfrage. Wir bestätigen Ihre Reservierung am 15. September 2025 um 19:00 Uhr für 4 Personen.\n\nWir freuen uns, Sie bei uns begrüssen zu dürfen.\n\nFreundliche Grüsse\nIhr Restaurant Team"
}
```

---

### 2. Generate Accept Reply
**POST** `/replies/accept`

Generate an acceptance reply confirming the reservation.

**Request Body:**
```json
{
  "salutation": "Frau",
  "last_name": "Schmidt",
  "date": "20. September 2025",
  "time": "18:30",
  "guests": 2,
  "reply_type": "accept"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Acceptance reply generated successfully",
  "reply_text": "Guten Tag, Frau Schmidt,\n\nVielen Dank für Ihre Anfrage. Wir bestätigen Ihre Reservierung am 20. September 2025 um 18:30 Uhr für 2 Personen.\n\nWir freuen uns, Sie bei uns begrüssen zu dürfen.\n\nFreundliche Grüsse\nIhr Restaurant Team"
}
```

---

### 3. Generate Alternative Reply
**POST** `/replies/alternative`

Generate a rejection reply informing of no availability at requested time.

**Request Body:**
```json
{
  "salutation": "Herr",
  "last_name": "Weber",
  "date": "22. September 2025",
  "time": "20:00",
  "guests": 6,
  "reply_type": "alternative"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Alternative reply generated successfully",
  "reply_text": "Guten Tag, Herr Weber,\n\nVielen Dank für Ihre Anfrage. Leider haben wir am 22. September 2025 um 20:00 Uhr keine Verfügbarkeit mehr.\n\nFreundliche Grüsse\nIhr Restaurant Team"
}
```

---

## Request Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| salutation | string | "Herr" or "Frau" | Yes |
| last_name | string | Guest's last name | Yes |
| date | string | Reservation date (e.g., "15. September 2025") | Yes |
| time | string | Reservation time (e.g., "19:00") | Yes |
| guests | integer | Number of guests | Yes (accept only) |
| reply_type | string | "accept" or "alternative" | Yes (generate endpoint only) |

---

## Response Structure

All endpoints return a `ReplyGenerationResponse` object:

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the reply was generated successfully |
| message | string | Status message or error description |
| reply_text | string \| null | The generated reply text (null on error) |

---

## Frontend Integration Example

### Step 1: Collect reservation details from email
Extract or display the following from the reservation email:
- Guest name (salutation & last name)
- Requested date
- Requested time
- Number of guests

### Step 2: When user clicks "Accept" button
```javascript
const replyData = {
  salutation: "Herr",        // from email parsing
  last_name: "Müller",       // from email parsing
  date: "15. September 2025", // from email
  time: "19:00",              // from email
  guests: 4,                  // from email
  reply_type: "accept"
};

const response = await fetch("http://localhost:8000/replies/accept", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(replyData)
});

const result = await response.json();
// Display result.reply_text in modal field
```

### Step 3: When user clicks "Alternative" button
```javascript
const replyData = {
  salutation: "Herr",
  last_name: "Müller",
  date: "15. September 2025",
  time: "19:00",
  reply_type: "alternative"
};

const response = await fetch("http://localhost:8000/replies/alternative", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(replyData)
});

const result = await response.json();
// Display result.reply_text in modal field
```

### Step 4: Display in Modal
- Show `result.reply_text` in a text field that user can edit before sending
- Allow user to copy or send the reply directly

---

## Error Handling

If `success` is `false`, check the `message` field for error details:

```javascript
if (!result.success) {
  console.error("Error generating reply:", result.message);
  // Display error to user
}
```

## Notes

- All replies are generated in German based on the available templates
- The reply text contains newline characters (`\n`) for formatting
- Frontend should display replies with preserved line breaks (use `<pre>` or `white-space: pre-wrap` in CSS)
- Users can edit the generated text before sending if needed
