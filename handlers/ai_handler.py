from telegram import Update
from telegram.error import TimedOut
from telegram.ext import ContextTypes
import logging
from services.voice_service import VoiceService
from services.video_service import VideoService
from config import Config


class AIHandler:
    def __init__(self, ai_client, ai_service, video_service: VideoService):
        self.ai_client = ai_client
        self.ai_service = ai_service
        self.video_service = video_service
        self.voice_service = VoiceService(ai_client)
        self.logger = logging.getLogger(__name__)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message:
            return

        message_text = update.message.text or update.message.caption

        if not message_text:
            return

        if message_text.startswith("/"):
            return

        current_model = context.user_data.get("current_model", Config.DEFAULT_MODEL)

        if current_model == "veo":
            await self._handle_video(update, message_text)
            return

        thinking_message = await update.message.reply_text("Думаю...")

        try:
            response = await self.ai_service.get_ai_response(
                message_text, current_model
            )
            await thinking_message.delete()
            await update.message.reply_text(response)

        except Exception as e:
            await thinking_message.delete()
            self.logger.error(f"Ошибка AI обработки: {e}")
            await update.message.reply_text("Произошла ошибка при обработке запроса")

    async def _handle_video(self, update: Update, prompt: str):
        status_message = await update.message.reply_text("Генерирую видео...")

        try:
            video_bytes = await self.video_service.generate_video(prompt)
        except Exception as e:
            await status_message.delete()
            self.logger.error(
                f"Ошибка генерации видео: {e}", exc_info=True
            )
            error_text = str(e) or "Неизвестная ошибка"
            await update.message.reply_text(
                f"Произошла ошибка при генерации видео: {error_text}"
            )
            return

        await status_message.delete()

        try:
            await update.message.reply_video(
                video_bytes,
                filename="video.mp4",
                write_timeout=300,
                read_timeout=300,
            )
        except TimedOut:
            self.logger.error("Таймаут при отправке видео в Telegram")
            await update.message.reply_text(
                "Видео слишком долго загружалось в Telegram. Попробуйте ещё раз."
            )
        except Exception as e:
            self.logger.error(
                f"Ошибка отправки видео: {e}", exc_info=True
            )
            await update.message.reply_text(
                f"Произошла ошибка при отправке видео: {e}"
            )

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.voice:
            return

        thinking_message = await update.message.reply_text(
            "Обрабатываю голосовое сообщение..."
        )

        try:
            voice_file = await update.message.voice.get_file()
            audio_url = voice_file.file_path

            transcribed_text = await self.voice_service.speech_to_text(audio_url)

            if transcribed_text:
                await thinking_message.edit_text(
                    f"Распознано: {transcribed_text}\n\nДумаю..."
                )

                current_model = context.user_data.get(
                    "current_model", Config.DEFAULT_MODEL
                )
                response = await self.ai_service.get_ai_response(
                    transcribed_text, current_model
                )

                await thinking_message.delete()
                await update.message.reply_text(response)
            else:
                await thinking_message.edit_text("Не удалось распознать речь")

        except Exception as e:
            await thinking_message.delete()
            self.logger.error(f"Ошибка обработки голосового сообщения: {e}")
            await update.message.reply_text(
                "Произошла ошибка при обработке голосового сообщения"
            )
