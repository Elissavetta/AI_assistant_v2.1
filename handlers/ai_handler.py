from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
import logging
from services.voice_service import VoiceService

class AIHandler:
    def __init__(self, ai_client, ai_service):
        self.ai_client = ai_client
        self.ai_service = ai_service
        self.voice_service = VoiceService(ai_client)
        self.logger = logging.getLogger(__name__)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message:
            return
            
        message_text = update.message.text or update.message.caption
        
        if not message_text:
            return
            
        if message_text.startswith('/'):
            return   

        thinking_message = await update.message.reply_text("Думаю...")

        try:
            response = await self.ai_service.get_ai_response(message_text)            
            await thinking_message.delete()
            await update.message.reply_text(response)
            
        except Exception as e:
            await thinking_message.delete()
            self.logger.error(f"Ошибка AI обработки: {e}")
            await update.message.reply_text("❌ Произошла ошибка при обработке запроса")

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.voice:
            return

        thinking_message = await update.message.reply_text("Обрабатываю голосовое сообщение...")

        try:
            voice_file = await update.message.voice.get_file()
            audio_url = voice_file.file_path
            
            transcribed_text = await self.voice_service.speech_to_text(audio_url)
            
            if transcribed_text:
                await thinking_message.edit_text(f"Распознано: {transcribed_text}\n\nДумаю...")
                
                response = await self.ai_service.get_ai_response(transcribed_text)
                
                await thinking_message.delete()
                await update.message.reply_text(response)
            else:
                await thinking_message.edit_text("❌ Не удалось распознать речь")
                
        except Exception as e:
            await thinking_message.delete()
            self.logger.error(f"Ошибка обработки голосового сообщения: {e}")
            await update.message.reply_text("❌ Произошла ошибка при обработке голосового сообщения")