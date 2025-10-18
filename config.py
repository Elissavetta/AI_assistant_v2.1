import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    AITUNNEL_API_KEY = os.getenv('AITUNNEL_API_KEY')
    AI_BASE_URL = "https://api.aitunnel.ru/v1/"
    
    # Маппинг: простые команды -> реальные имена моделей AITUNNEL
    MODEL_MAPPING = {
        "deepseek": "deepseek-v3.2-exp",
        "qwen": "qwen3-coder", 
        "gpt": "gpt-5-mini",
        "sonar": "sonar"
    }
    
    # Описания для пользователей
    MODEL_DESCRIPTIONS = {
        "deepseek": "DeepSeek Chat (умный и сбалансированный)",
        "qwen": "QWEN Coder (для программирования)",
        "gpt": "GPT-5 Mini (быстрый и экономный)",
        "sonar": "Sonar (ищет актуальную информацию в сети)"
    }
    
    # Модель по умолчанию
    DEFAULT_MODEL = "deepseek"

    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("❌ Токен бота не найден! Проверь файл .env")
        if not cls.AITUNNEL_API_KEY:
            raise ValueError("❌ AITUNNEL API ключ не найден! Проверь файл .env")