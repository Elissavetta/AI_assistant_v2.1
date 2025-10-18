import logging
from config import Config

class AIService:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.logger = logging.getLogger(__name__)
        self.current_model = Config.DEFAULT_MODEL  # Храним простые имена

    def set_model(self, model_key: str) -> bool:
        """Устанавливает модель для AI по простому имени"""
        if model_key in Config.MODEL_MAPPING:
            self.current_model = model_key
            return True
        return False

    def get_current_model(self) -> str:
        """Возвращает текущую модель (простое имя)"""
        return self.current_model

    def get_current_model_real_name(self) -> str:
        """Возвращает реальное имя текущей модели для API"""
        return Config.MODEL_MAPPING[self.current_model]

    def get_available_models(self) -> dict:
        """Возвращает доступные модели с описаниями"""
        return Config.MODEL_DESCRIPTIONS

    async def get_ai_response(self, user_message: str) -> str:
        """Получает ответ от AI модели"""
        real_model_name = self.get_current_model_real_name()
        
        try:
            completion = self.ai_client.chat.completions.create(
                model=real_model_name,  # Используем реальное имя для API
                messages=[
                    {"role": "system", "content": "Ты умный ИИ ассистент. Формат ответа - сообщение в Телеграмм. Можешь использовать эмоджи если они уместны.Стиль общения нейтральный. В конце обязательно напиши какой-то интересный факт связанный с темой на которую был задан вопрос"},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Ошибка API AITUNNEL ({real_model_name}): {e}")
            return "❌ Извините, в настоящее время сервис недоступен. Попробуйте позже."