from .basic_commands.start import StartCommand
from .basic_commands.help import HelpCommand
from .ai_handler import AIHandler
from .model_commands import ModelCommands
from telegram.ext import MessageHandler, filters

def get_all_handlers(ai_client, ai_service):
    start = StartCommand()
    help = HelpCommand()
    ai_handler = AIHandler(ai_client, ai_service)
    model_commands = ModelCommands(ai_service)
    
    handlers_list = [
        ("start", start.start_command),
        ("help", help.help_command), 
        ("model", model_commands.model_info),
        # Простые команды для смены моделей
        ("deepseek", model_commands.set_model_deepseek),
        ("qwen", model_commands.set_model_qwen),
        ("gpt", model_commands.set_model_gpt),
        ("sonar", model_commands.set_model_sonar),
        # Обработчик reply-кнопок (должен быть перед общим MessageHandler)
        MessageHandler(filters.TEXT & ~filters.COMMAND, start.handle_reply_buttons),
        # Общий обработчик сообщений для AI
        MessageHandler(filters.TEXT & ~filters.COMMAND, ai_handler.handle_message),
        MessageHandler(filters.VOICE, ai_handler.handle_voice)
    ]
    
    return handlers_list