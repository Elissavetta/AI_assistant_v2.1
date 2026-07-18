from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from ..ai_handler import AIHandler
from ..model_commands import ModelCommands
from .help import HelpCommand
import datetime

BUTTON_TO_MODEL_KEY = {
    "ChatGPT-5": "gpt",
    "DeepSeek V3": "deepseek",
    "QWEN Coder": "qwen",
    "Sonar": "sonar",
    "Veo 3.1 Lite": "veo",
}


class StartCommand:
    def __init__(
        self,
        ai_handler: AIHandler,
        model_commands: ModelCommands,
        help_command: HelpCommand,
    ):
        self.ai_handler = ai_handler
        self.model_commands = model_commands
        self.help_command = help_command

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.effective_user.first_name
        greeting = self.get_time_greeting()

        keyboard = [
            ["Текущая AI модель"],
            ["Сменить модель"],
            ["Помощь"],
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="Выбери действие или напиши сообщение...",
        )

        await update.message.reply_text(
            f"""
{greeting}, {user_name}!
Чтобы начать, просто напиши, что тебя интересует, или воспользуйся меню команд.
""".strip(),
            parse_mode="HTML",
            reply_markup=reply_markup,
        )

    async def handle_reply_buttons(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        text = update.message.text

        if text == "Помощь":
            await self.help_command.help_command(update, context)
        elif text == "Текущая AI модель":
            await self.model_commands.model_info(update, context)
        elif text == "Сменить модель":
            await self.show_model_switch_keyboard(update, context)
        elif text in BUTTON_TO_MODEL_KEY:
            model_key = BUTTON_TO_MODEL_KEY[text]
            await self.model_commands.set_model(update, context, model_key)
        elif text == "Назад":
            await self.start_command(update, context)
        else:
            await self.ai_handler.handle_message(update, context)

    async def show_model_switch_keyboard(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        model_keyboard = [
            ["ChatGPT-5", "DeepSeek V3"],
            ["QWEN Coder", "Sonar"],
            ["Veo 3.1 Lite"],
            ["Назад"],
        ]

        reply_markup = ReplyKeyboardMarkup(
            model_keyboard,
            resize_keyboard=True,
            input_field_placeholder="Выбери модель AI...",  
        )

        await update.message.reply_text(
            "<b>Выбери AI модель:</b>", parse_mode="HTML", reply_markup=reply_markup
        )

    @staticmethod
    def get_time_greeting():
        current_hour = datetime.datetime.now().hour

        if 5 <= current_hour < 12:
            return "Доброе утро"
        elif 12 <= current_hour < 17:
            return "Добрый день"
        elif 17 <= current_hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"
