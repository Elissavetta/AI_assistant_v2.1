from .basic_commands.start import StartCommand
from .basic_commands.help import HelpCommand
from .ai_handler import AIHandler
from .model_commands import ModelCommands
from telegram.ext import MessageHandler, filters


def get_all_handlers(ai_client, ai_service, video_service):
    help_cmd = HelpCommand()
    ai_handler = AIHandler(ai_client, ai_service, video_service)
    model_commands = ModelCommands(ai_service)
    start = StartCommand(ai_handler, model_commands, help_cmd)

    handlers_list = [
        ("start", start.start_command),
        ("help", help_cmd.help_command),
        ("model", model_commands.model_info),
        ("deepseek", model_commands.set_model),
        ("qwen", model_commands.set_model),
        ("gpt", model_commands.set_model),
        ("sonar", model_commands.set_model),
        ("veo", model_commands.set_model),
        MessageHandler(filters.TEXT & ~filters.COMMAND, start.handle_reply_buttons),
        MessageHandler(filters.VOICE, ai_handler.handle_voice),
    ]

    return handlers_list
