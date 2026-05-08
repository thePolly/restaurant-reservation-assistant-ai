"""
Service for generating reply messages for reservation requests.
Uses templates from reply_templates.py to generate pre-filled responses.
"""

from app.services import reply_templates
from typing import Dict, Any, Optional


def generate_acceptance_reply(data: Dict[str, Any]) -> str:
    """
    Generate an acceptance reply for a reservation request.
    
    Args:
        data: Dictionary with keys:
            - salutation: Salutation (e.g., "Herr", "Frau")
            - last_name: Last name of the guest
            - date: Reservation date (e.g., "15. September 2025")
            - time: Reservation time (e.g., "19:00")
            - guests: Number of guests
    
    Returns:
        Generated acceptance message
    """
    return reply_templates.confirmation_reply_de(data)


def generate_alternative_reply(data: Dict[str, Any]) -> str:
    """
    Generate an alternative/rejection reply for a reservation request.
    Suggests no availability at requested time.
    
    Args:
        data: Dictionary with keys:
            - salutation: Salutation (e.g., "Herr", "Frau")
            - last_name: Last name of the guest
            - date: Reservation date (e.g., "15. September 2025")
            - time: Reservation time (e.g., "19:00")
    
    Returns:
        Generated alternative message
    """
    return reply_templates.alternative_reply_de(data)


def generate_reservation_reply(data: Dict[str, Any], reply_type: str) -> str:
    """
    Generate a reservation reply based on type.
    
    Args:
        data: Dictionary with reservation details
        reply_type: Type of reply - "accept" or "alternative"
    
    Returns:
        Generated message
    
    Raises:
        ValueError: If reply_type is not recognized
    """
    if reply_type == "accept":
        return generate_acceptance_reply(data)
    elif reply_type == "alternative":
        return generate_alternative_reply(data)
    else:
        raise ValueError(f"Unknown reply type: {reply_type}. Use 'accept' or 'alternative'")


def generate_reply_from_extracted_data(
    name: Optional[str],
    date: Optional[str],
    time_category: Optional[str],
    people_count: Optional[int],
    action: str,
) -> str:
    """
    Generate a reply directly from extracted email data (no frontend logic needed).
    
    Args:
        name: Guest's name (e.g., "John Smith" or "Müller")
        date: Reservation date (e.g., "15. September 2025")
        time_category: Time category ("breakfast", "lunch", "dinner")
        people_count: Number of guests
        action: Reply type - "accept" or "alternative"
    
    Returns:
        Generated reply message
    
    Raises:
        ValueError: If critical data is missing or action is invalid
    """
    if not name:
        raise ValueError("Guest name is required")
    
    if action not in ("accept", "alternative"):
        raise ValueError(f"Invalid action: {action}. Use 'accept' or 'alternative'")
    
    # Extract last name (if "First Last", use Last; otherwise use the name as is)
    name_parts = name.strip().split()
    last_name = name_parts[-1] if name_parts else "Guest"
    
    # Default salutation based on name analysis (simplified - could be enhanced)
    salutation = "Herr"
    
    # Format date (use as-is if provided, otherwise use placeholder)
    formatted_date = date or "TBD"
    
    # Map time category to time
    time_map = {
        "breakfast": "08:00",
        "lunch": "12:00",
        "dinner": "19:00",
    }
    formatted_time = time_map.get(time_category, "19:00")
    
    # Use guests count or default to 2
    guests = people_count or 2
    
    # Prepare data dict for template
    template_data = {
        "salutation": salutation,
        "last_name": last_name,
        "date": formatted_date,
        "time": formatted_time,
        "guests": guests
    }
    
    # Generate reply based on action
    return generate_reservation_reply(template_data, action)
