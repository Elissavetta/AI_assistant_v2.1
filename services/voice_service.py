import logging
import requests

class VoiceService:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.logger = logging.getLogger(__name__)

    async def speech_to_text(self, audio_url: str) -> str:
        """Конвертирует голосовое сообщение в текст с помощью Whisper"""
        try:
            # Скачиваем аудио файл
            response = requests.get(audio_url)
            audio_file = ("audio.ogg", response.content, "audio/ogg")
            
            # Отправляем в Whisper для транскрибации
            transcription = self.ai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ru"
            )
            
            return transcription.text
            
        except Exception as e:
            self.logger.error(f"Ошибка Whisper API: {e}")
            return None