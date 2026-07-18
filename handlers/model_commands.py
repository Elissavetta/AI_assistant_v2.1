from telegram import Update
from telegram.ext import ContextTypes
from services.ai_service import AIService
from config import Config


class ModelCommands:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def model_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        current_model = context.user_data.get("current_model", Config.DEFAULT_MODEL)
        available_models = self.ai_service.get_available_models()

        message = f"<b>Текущая модель:</b> {available_models[current_model]}\n\n"
        message += "<b>Доступные модели:</b>\n"

        for model_key, model_description in available_models.items():
            indicator = "●" if model_key == current_model else "○"
            message += f"{indicator} /{model_key} - {model_description}\n"

        message += "\n<i>Используй команды выше для смены модели</i>"

        await update.message.reply_text(message, parse_mode="HTML")

    async def set_model(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, model_key: str = None
    ):
        if model_key is None:
            model_key = update.message.text.lstrip("/")

        if self.ai_service.is_valid_model(model_key):
            context.user_data["current_model"] = model_key
            available_models = self.ai_service.get_available_models()
            await update.message.reply_text(
                f"Модель изменена на: <b>{available_models[model_key]}</b>",
                parse_mode="HTML",
            )
        else:
            await update.message.reply_text(
                "Неизвестная модель. Используй /model для списка доступных моделей."
            )
