import re
import uuid
from typing import Dict, Tuple, Any

import spacy


try:
    nlp = spacy.load("xx_ent_wiki_sm")
except OSError:
    raise RuntimeError(
        "spaCy model not found. Run: python -m spacy download xx_ent_wiki_sm"
    )


PHONE_PATTERN = re.compile(r"(?<!\w)(\+?\d[\d\s().-]{7,}\d)(?!\w)")
EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")


def _make_token(label: str) -> str:
    return f"[{label}_{uuid.uuid4().hex[:8]}]"


def mask_pii(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Masks PII and returns:
    1. masked text
    2. mapping for later unmasking

    Example:
    "John Smith, +41 79 123 45 67"
    -> "[PERSON_xxxxxxxx], [PHONE_yyyyyyyy]"
    """

    mapping: Dict[str, str] = {}

    # 1. Mask emails first
    def replace_email(match: re.Match) -> str:
        original = match.group(0)
        token = _make_token("EMAIL")
        mapping[token] = original
        return token

    masked_text = EMAIL_PATTERN.sub(replace_email, text)

    # 2. Mask phone numbers
    def replace_phone(match: re.Match) -> str:
        original = match.group(0)
        token = _make_token("PHONE")
        mapping[token] = original
        return token

    masked_text = PHONE_PATTERN.sub(replace_phone, masked_text)

    print("After masking phone and email:", masked_text)
    # 3. Mask person names with spaCy

    doc = nlp(masked_text)

    entities = [
        ent
        for ent in doc.ents
        if ent.label_ in ("PER", "PERSON")
    ]

    # Идем с конца текста к началу, чтобы индексы не поехали
    for ent in sorted(entities, key=lambda e: e.start_char, reverse=True):
        full_name = masked_text[ent.start_char:ent.end_char]
        parts = full_name.split()

        if len(parts) > 1:
            # Если слов больше одного (например, "John Smith")
            first_name = parts[0]           # Оставляем "John"
            last_name = " ".join(parts[1:]) # Берем всё остальное ("Smith")
            
            token = _make_token("LASTNAME")
            mapping[token] = last_name
            
            # В тексте будет: "John [LASTNAME_xxxx]"
            replacement = f"{first_name} {token}"
        else:
            # Если только одно слово, маскируем его целиком
            token = _make_token("PERSON")
            mapping[token] = full_name
            replacement = token

        # Заменяем имя в тексте
        masked_text = (
            masked_text[:ent.start_char]
            + replacement
            + masked_text[ent.end_char:]
        )


    print("After masking phone and email and name:", masked_text)
    return masked_text, mapping


def unmask_pii(masked_text: str, mapping: Dict[str, str]) -> str:
    """
    Restores masked PII using the saved mapping.
    """

    restored_text = masked_text

    for token, original in mapping.items():
        restored_text = restored_text.replace(token, original)

    return restored_text


def mask_pii_payload(text: str) -> Dict[str, Any]:
    """
    Useful for API responses.
    """

    masked_text, mapping = mask_pii(text)

    return {
        "masked_text": masked_text,
        "mapping": mapping,
    }


def unmask_pii_payload(masked_text: str, mapping: Dict[str, str]) -> Dict[str, str]:
    """
    Useful for API responses.
    """

    return {
        "unmasked_text": unmask_pii(masked_text, mapping)
    }