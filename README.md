# AI Reservation Assistant

## Overview

This project implements an AI-assisted tool to support restaurant staff in processing reservation emails.

The system extracts key booking information from incoming emails and generates suggested replies.  
Staff remain responsible for checking availability and recording reservations in the existing reservation book.

The goal is to reduce manual effort while preserving the current workflow.

---

## Problem

Handling reservation emails manually requires:
- reading and interpreting each message
- extracting relevant details (date, time, number of guests, customer data)
- checking availability
- composing a response

This process is time-consuming and prone to errors.

---

## Solution

The application assists staff by:
- extracting reservation details from emails
- presenting the information in a structured format
- generating predefined reply options

The final decision remains with the staff member, who verifies availability and sends the response.

---

## Features (MVP)

- Email retrieval via IMAP  
- Extraction of reservation data:
  - date
  - time
  - number of guests
  - customer name
  - phone (if available)
- Generation of reply options:
  - confirmation
  - no availability / alternative
- Editable responses
- Email sending via SMTP
- Simple web interface
- Local execution

---

## Workflow

1. Reservation emails are forwarded to a system mailbox  
2. The application retrieves new messages  
3. Booking details are extracted using an AI model  
4. The request is displayed in the interface  
5. Staff check availability in the reservation book  
6. Staff select a response  
7. The system sends the email  

---

## Architecture

- Backend: Python (FastAPI)  
- Frontend: HTML / CSS / JavaScript  
- AI processing: OpenAI API  
- Email handling: IMAP (receive), SMTP (send)  
- Storage: SQLite (optional)  
- Runtime: local application  

---

## Design Decisions

- The reservation book remains the primary system  
- The application does not perform automatic booking confirmation  
- User interaction is required before sending any response  
- The system is designed for local use to reduce deployment complexity  

---

## Documentation

Detailed documentation is available in the project Wiki:

[wiki](https://github.com/thePolly/restaurant-reservation-assistant-ai/wiki)

---

## Running the Application

1. Start the application using the provided launcher  
2. The interface opens in the browser  
3. Begin processing incoming reservation emails  

---

## Future Work

- Direct integration with the primary mailbox  
- Improved handling of ambiguous or incomplete requests  
- Reservation conflict detection  
- Extended user interface  

---
