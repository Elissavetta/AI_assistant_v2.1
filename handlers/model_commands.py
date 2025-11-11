from telegram import Update
from telegram.ext import ContextTypes
from services.ai_service import AIService

class ModelCommands:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def model_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показывает текущую модель и доступные модели"""
        current_model = self.ai_service.get_current_model()
        available_models = self.ai_service.get_available_models()
        
        message = f"<b>Текущая модель:</b> {available_models[current_model]}\n\n"
        message += "<b>Доступные модели:</b>\n"
        
        for model_key, model_description in available_models.items():
            indicator = "●" if model_key == current_model else "○"
            message += f"{indicator} /{model_key} - {model_description}\n"
        
        message += "\n<i>💡Используй команды выше для смены модели</i>"
        
        await update.message.reply_text(message, parse_mode='HTML')

    async def set_model_deepseek(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает модель DeepSeek"""
        await self._set_model(update, "deepseek")

    async def set_model_qwen(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает модель QWEN"""
        await self._set_model(update, "qwen")

    async def set_model_gpt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает модель GPT"""
        await self._set_model(update, "gpt")

    async def set_model_sonar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает модель Sonar"""
        await self._set_model(update, "sonar")

    async def _set_model(self, update: Update, model_key: str):
        """Внутренний метод для смены модели"""
        if self.ai_service.set_model(model_key):
            available_models = self.ai_service.get_available_models()
            await update.message.reply_text(
                f"✅ Модель изменена на: <b>{available_models[model_key]}</b>",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(
                "❌ Неизвестная модель. Используй /model для списка доступных моделей."
            )