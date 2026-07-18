from dotenv import load_dotenv
from config import Config
from handlers import get_all_handlers
from telegram.ext import Application, CommandHandler
from openai import AsyncOpenAI
from services.ai_service import AIService
from services.video_service import VideoService
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class AIAssistant:
    def __init__(self):
        Config.validate()

        self.ai_client = AsyncOpenAI(
            api_key=Config.AITUNNEL_API_KEY,
            base_url=Config.AI_BASE_URL,
        )

        self.ai_service = AIService(self.ai_client)
        self.video_service = VideoService(Config.AITUNNEL_API_KEY, Config.AI_BASE_URL)

        self.application = (
            Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        )
        self.setup_handlers()

    def setup_handlers(self):
        handlers = get_all_handlers(self.ai_client, self.ai_service, self.video_service)

        for handler in handlers:
            if isinstance(handler, tuple):
                command_name, handler_func = handler
                self.application.add_handler(CommandHandler(command_name, handler_func))
            else:
                self.application.add_handler(handler)

    def run(self):
        print("Running...")
        print("To stop: ctrl+C")
        self.application.run_polling()


if __name__ == "__main__":
    bot = AIAssistant()
    bot.run()
