from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- 1. Добавляем импорт
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.pii_masker import mask_pii
from app.services.ai_engine import extract_data, ExtractionSchema
from app.services.email_sender import send_email_reply
from app.services.general_reply_generator import generate_general_email_reply
from app.services.reply_generator import (
    generate_acceptance_reply,
    generate_alternative_reply,
    generate_reservation_reply,
    generate_reply_from_extracted_data
)

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

app = FastAPI()

# --- 2. ДОБАВЛЯЕМ НАСТРОЙКИ CORS (БЕЗ ЭТОГО REACT НЕ УВИДИТ ДАННЫЕ) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы с любого адреса (для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешает любые заголовки
)
# -----------------------------------------------------------------------

class IncomingEmail(BaseModel):
    id: int
    sender: str
    subject: str
    body: str

class ProcessedEmail(BaseModel):
    id: int
    sender: str
    sender_email: str
    masked_body: str
    extracted_data: ExtractionSchema

class SendReplyRequest(BaseModel):
    to_email: str
    subject: str
    body: str

class GeneralReplyRequest(BaseModel):
    masked_body: str

class ReplyGenerationRequest(BaseModel):
    """Request model for generating reservation replies"""
    salutation: str  # e.g., "Herr", "Frau"
    last_name: str
    date: str  # e.g., "15. September 2025"
    time: str  # e.g., "19:00"
    guests: int
    reply_type: str  # "accept" or "alternative"


class ReplyGenerationResponse(BaseModel):
    """Response model for generated replies"""
    success: bool
    message: str
    reply_text: Optional[str] = None


class SimpleReplyGenerationRequest(BaseModel):
    """Request model for generating replies from extracted email data (minimal frontend logic)"""
    name: Optional[str] = None
    date: Optional[str] = None
    time_category: Optional[str] = None  # "breakfast", "lunch", "dinner"
    people_count: Optional[int] = None
    action: str  # "accept" or "alternative"

MOCK_EMAILS = [
    {
        "id": 1,
        "sender": "john.smith@gmail.com",
        "subject": "Reservation request",
        "body": "Hello, I am John Smith. I want to book a table for 2 people on Sept 15 at 7pm. Terrace please."
    },
    {
        "id": 2,
        "sender": "anna.m@web.de",
        "subject": "Question",
        "body": "Hi, do you allow dogs in the taverne? We are 4 people for lunch tomorrow."
    }
]

@app.get("/emails/mock", response_model=List[ProcessedEmail])
async def get_mock_emails():
    emails = fetch_unread_emails(limit=3)

    print(f"Found {len(emails)} emails\n")
    results = []

    for i, email_data in enumerate(emails, start=1):

        extracted = extract_data(email_data["body"])


        results.append({
            "id": i,
            "sender": email_data["from"],
            "sender_email": email_data.get("sender_email", ""),
            "masked_body": email_data["body"],
            "extracted_data": extracted
        })
    return results


# ==================== REPLY GENERATION ENDPOINTS ====================

@app.post("/replies/generate", response_model=ReplyGenerationResponse)
async def generate_reply(request: ReplyGenerationRequest):
    """
    Generate a reply message for a reservation request.
    
    Request body should contain:
    - salutation: "Herr" or "Frau"
    - last_name: Guest's last name
    - date: Reservation date (e.g., "15. September 2025")
    - time: Reservation time (e.g., "19:00")
    - guests: Number of guests
    - reply_type: "accept" or "alternative"
    """
    try:
        data = {
            "salutation": request.salutation,
            "last_name": request.last_name or "Gast",
            "date": request.date,
            "time": request.time,
            "guests": request.guests
        }
        
        reply_text = generate_reservation_reply(data, request.reply_type)
        
        return {
            "success": True,
            "message": f"Reply generated successfully as {request.reply_type}",
            "reply_text": reply_text
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "reply_text": None
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating reply: {str(e)}",
            "reply_text": None
        }

@app.post("/emails/send-reply-reserved")
async def send_reply(request: SendReplyRequest):
    try:
        send_email_reply(
            to_email=request.to_email,
            subject=request.subject,
            body=request.body
        )

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as e:
        return {
            "success": False,

            "message": f"Error sending email: {str(e)}"

        }
    
@app.post("/emails/send-reply")

async def send_reply(request: SendReplyRequest):

    print("\n=============================")
    print("📨 DEMO EMAIL SENT")
    print("TO:", request.to_email)
    print("SUBJECT:", request.subject)
    print("BODY:")
    print(request.body)
    print("==============================\n")
    return {
        "success": True,
        "message": "Demo mode: email logged in backend console"
    }


@app.post("/replies/accept", response_model=ReplyGenerationResponse)
async def generate_accept_reply(request: ReplyGenerationRequest):
    """
    Generate an acceptance reply for a reservation request.
    
    Confirms the reservation with provided details.
    """
    try:
        data = {
            "salutation": request.salutation,
            "last_name": request.last_name,
            "date": request.date,
            "time": request.time,
            "guests": request.guests
        }
        
        reply_text = generate_acceptance_reply(data)
        
        return {
            "success": True,
            "message": "Acceptance reply generated successfully",
            "reply_text": reply_text
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating acceptance reply: {str(e)}",
            "reply_text": None
        }


@app.post("/replies/alternative", response_model=ReplyGenerationResponse)
async def generate_alternative_response(request: ReplyGenerationRequest):
    """
    Generate an alternative/rejection reply for a reservation request.
    
    Informs guest of no availability at requested time.
    """
    try:
        data = {
            "salutation": request.salutation,
            "last_name": request.last_name,
            "date": request.date,
            "time": request.time
        }
        
        reply_text = generate_alternative_reply(data)
        
        return {
            "success": True,
            "message": "Alternative reply generated successfully",
            "reply_text": reply_text
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating alternative reply: {str(e)}",
            "reply_text": None
        }


@app.post("/replies/generate-general", response_model=ReplyGenerationResponse)

async def generate_general_reply(request: GeneralReplyRequest):

    try:

        reply_text = generate_general_email_reply(request.masked_body)

        return {

            "success": True,

            "message": "General reply generated successfully",

            "reply_text": reply_text

        }

    except Exception as e:

        return {

            "success": False,

            "message": f"Error generating general reply: {str(e)}",

            "reply_text": None

        }


# ==================== SIMPLIFIED ENDPOINT (NO FRONTEND LOGIC) ====================

@app.post("/replies/generate-from-email", response_model=ReplyGenerationResponse)
async def generate_reply_from_email(request: SimpleReplyGenerationRequest):
    """
    Generate a reply from extracted email data.
    
    This endpoint handles all business logic - frontend only passes extracted data and action.
    
    Request body:
    {
        "name": "John Smith",
        "date": "15. September 2025",
        "time_category": "dinner",
        "people_count": 4,
        "action": "accept"
    }
    """
    try:
        reply_text = generate_reply_from_extracted_data(
            name=request.name or "Gast",
            date=request.date,
            time_category=request.time_category,
            people_count=request.people_count,
            action=request.action
        )
        
        return {
            "success": True,
            "message": f"Reply generated successfully as {request.action}",
            "reply_text": reply_text
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "reply_text": None
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating reply: {str(e)}",
            "reply_text": None
        }
        

      