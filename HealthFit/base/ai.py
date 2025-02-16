# # import os
# # import google.generativeai as genai
# #
# # # Установите API ключ
# # genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
# # genai.configure(api_key='AIzaSyA56tUTFKLGnE0RGla75u5Twc1Tvl-njWk')
# # # Инициализация модели
# # model = genai.GenerativeModel('gemini-pro')
#
# # generativeai_utils.py
# import google.generativeai as genai
# import json
# import os
#
# def initialize_generativeai(api_key: str):
#     """Инициализация Google Generative AI."""
#     genai.configure(api_key='AIzaSyA56tUTFKLGnE0RGla75u5Twc1Tvl-njWk')
#
# def generate_workout_plan(prompt: str) -> dict:
#     """Генерация плана тренировки с использованием Google Generative AI."""
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(prompt)
#
#     # Очищаем ответ от возможных маркеров кода и лишних символов
#     cleaned_response = response.text.strip()
#     if cleaned_response.startswith('```json'):
#         cleaned_response = cleaned_response[7:]
#     if cleaned_response.endswith('```'):
#         cleaned_response = cleaned_response[:-3]
#     cleaned_response = cleaned_response.strip()
#
#     return json.loads(cleaned_response)