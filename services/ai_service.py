import logging
from config import Config


class AIService:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.logger = logging.getLogger(__name__)

    def is_valid_model(self, model_key: str) -> bool:
        return model_key in Config.MODEL_MAPPING

    def get_real_model_name(self, model_key: str) -> str | None:
        return Config.MODEL_MAPPING.get(model_key)

    def get_available_models(self) -> dict:
        return Config.MODEL_DESCRIPTIONS

    async def get_ai_response(self, user_message: str, model_key: str) -> str:
        real_model_name = self.get_real_model_name(model_key)
        if not real_model_name:
            return "Модель не найдена."

        try:
            completion = await self.ai_client.chat.completions.create(
                model=real_model_name,
                messages=[
                    {
                        "role": "system",
                        "content": """Ты — дружелюбный ИИ-ассистент в Telegram. Тон: вежливо-деловой, помогающий. Структурируй ответы (списки, абзацы, эмодзи), используй вежливые формы, но обращайся на "Ты". Показывай эмпатию и проактивность в помощи ("Конечно, я помогу", "Хороший вопрос!") . Используй форматирование в Telegram. Приводи в скобках примеры для лучшего понимания. В конце  ответа добавляй интересный факт по теме вопроса.""",
                    },
                    {"role": "user", "content": user_message},
                ],
                max_tokens=1000,
                temperature=0.7,
            )

            response = completion.choices[0].message.content
            return self._chunk_response(response)

        except Exception as e:
            self.logger.error(f"Ошибка API AITUNNEL ({real_model_name}): {e}")
            return "Извини, в настоящее время сервис недоступен. Попробуй позже."

    @staticmethod
    def _chunk_response(text: str, max_length: int = 4000) -> str:
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."
