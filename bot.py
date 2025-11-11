from dotenv import load_dotenv
from config import Config
from handlers import get_all_handlers
from telegram.ext import Application, CommandHandler
from openai import OpenAI
from services.ai_service import AIService  # Добавляем импорт

class AIAssistant:
    def __init__(self):
        Config.validate()
        
        self.ai_client = OpenAI(
            api_key=Config.AITUNNEL_API_KEY,
            base_url=Config.AI_BASE_URL,
        )
        
        # Создаем AI service
        self.ai_service = AIService(self.ai_client)
        
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        # Передаем и ai_client и ai_service
        handlers = get_all_handlers(self.ai_client, self.ai_service)
        
        # Сохраняем ai_handler в bot_data для доступа из других обработчиков
        self.application.bot_data['ai_service'] = self.ai_service
        self.application.bot_data['ai_handler'] = None
        
        for handler in handlers:
            if isinstance(handler, tuple):
                command_name, handler_func = handler
                self.application.add_handler(CommandHandler(command_name, handler_func))
            else:
                self.application.add_handler(handler)
                # Сохраняем ссылку на ai_handler
                if hasattr(handler, 'callback') and 'ai_handler' in str(handler.callback):
                    self.application.bot_data['ai_handler'] = handler.callback

    def run(self):
        print("Running...")
        print("To stop: ctrl+C")
        self.application.run_polling()

if __name__ == "__main__":
    bot = AIAssistant()
    bot.run()