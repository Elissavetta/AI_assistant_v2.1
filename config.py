import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    AITUNNEL_API_KEY = os.getenv("AITUNNEL_API_KEY")
    AI_BASE_URL = os.getenv("AI_BASE_URL")

    # Маппинг: простые команды -> реальные имена моделей AITUNNEL
    MODEL_MAPPING = {
        "deepseek": "deepseek-v3.2-exp",
        "qwen": "qwen3-coder",
        "gpt": "gpt-5-mini",
        "sonar": "sonar",
        "veo": "veo-3.1-lite",
    }

    # Описания для пользователей
    MODEL_DESCRIPTIONS = {
        "deepseek": "DeepSeek Chat",
        "qwen": "QWEN Coder",
        "gpt": "GPT-5 Mini",
        "sonar": "Sonar",
        "veo": "Veo 3.1 Lite",
    }

    # Модель по умолчанию
    DEFAULT_MODEL = "deepseek"

    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("Токен бота не найден! Проверь файл .env")
        if not cls.AITUNNEL_API_KEY:
            raise ValueError("AITUNNEL API ключ не найден! Проверь файл .env")
