from services.data_extractor import extract_reservation_data

from services.reply_templates import confirmation_reply_de, alternative_reply_de

from services.pii_masker import mask_pii, unmask_pii

from services.ai_engine import extract_data

text = """

Hello, 
I want to do a reservation for 2 people on the 15th of September at 7pm.
My email is john.smith@gmail.com.
Freundliche Grüsse
John Smith
+41 79 123 45 67.
"""


def handle_customer_request(user_input: str):
    # 1. Маскируем (защищаем данные)
    # Здесь используется твоя логика с сохранением имени для определения пола
    masked_text, mapping = mask_pii(user_input)
    
    # 2. Отправляем замаскированный текст в OpenRouter
    # ИИ увидит: "John [LASTNAME_xxx] wants a table for 2..."
    extracted_data = extract_data(masked_text)
    
    # 3. Возвращаем результат
    return {
        "structured_data": extracted_data, # Объект Pydantic
        "mapping": mapping,                # Ключи для размаскировки в будущем
        "masked_text": masked_text         # На всякий случай
    }

# ПРИМЕР ЗАПУСКА:
raw_input = "Hello, I am Anna Smith. Table for 3 on Friday at 8pm. No dogs please."
final_result = handle_customer_request(raw_input)

print(f"Тип запроса: {final_result['structured_data'].request_type}")
print(f"Пол (по имени): {'Female' if 'Anna' in final_result['masked_text'] else 'Unknown'}")