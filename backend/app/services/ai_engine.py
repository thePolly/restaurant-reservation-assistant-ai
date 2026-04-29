import os
import json
from dotenv import load_dotenv
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

api_key = os.getenv("OPEN_ROUTER_API_KEY")

if not api_key:
    raise ValueError("OPEN_ROUTER_API_KEY is missing. Check your .env file.")


class ExtractionSchema(BaseModel):
    request_type: Literal["general", "reservation"]
    date: Optional[str] = None
    time_category: Optional[Literal["breakfast", "lunch", "dinner"]] = None
    people_count: Optional[int] = None
    special_requests: List[str] = Field(default_factory=list)
    location_preference: Optional[
        Literal["terrace", "saal", "taverne", "small_room"]
    ] = None


def create_llm(model: str) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model=model,
        temperature=0,
        timeout=30,
        max_retries=1,
        default_headers={
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "restaurant-reservation-assistant-ai",
        },
    )


llm = create_llm("openai/gpt-4o-mini")


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a restaurant reservation assistant.

Extract data from the email.

Return ONLY valid JSON.
No markdown.
No explanations.

JSON schema:
{{
  "request_type": "general" or "reservation",
  "date": string or null,
  "time_category": "breakfast" or "lunch" or "dinner" or null,
  "people_count": number or null,
  "special_requests": list of strings,
  "location_preference": "terrace" or "saal" or "taverne" or "small_room" or null
}}
"""
    ),
    ("user", "{text}")
])


def clean_json_response(content: str) -> str:
    return (
        content.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )


def extract_data(masked_text: str) -> ExtractionSchema:

    try:
        chain = prompt | llm
        response = chain.invoke({"text": masked_text})
        cleaned_content = clean_json_response(response.content)
        raw_data = json.loads(cleaned_content)
        return ExtractionSchema(**raw_data)

    except Exception as e:
        raise RuntimeError(f"Extraction failed: {e}")


if __name__ == "__main__":
    masked_text = """
Hello, I want to do a reservation for 2 people on the 15th of September at 7pm.
My email is [EMAIL_123].
John [LASTNAME_456]
"""

    result = extract_data(masked_text)
    print(result.model_dump_json(indent=2))