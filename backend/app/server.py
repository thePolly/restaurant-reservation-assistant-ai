from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- 1. Добавляем импорт
from pydantic import BaseModel
from typing import List, Dict, Optional

from services.pii_masker import mask_pii
from services.ai_engine import extract_data, ExtractionSchema

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
    masked_body: str
    extracted_data: ExtractionSchema

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
    results = []
    for email in MOCK_EMAILS:
        masked_text, mapping = mask_pii(email["body"])
        extracted = extract_data(masked_text)
        
        results.append({
            "id": email["id"],
            "sender": email["sender"],
            "masked_body": email["body"],
            "extracted_data": extracted
        })
    return results