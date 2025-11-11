from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import datetime


class StartCommand:

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.effective_user.first_name
        greeting = await self.get_time_greeting()

        # Создаем reply-клавиатуру с кнопками
        keyboard = [
            ["🧠Текущая AI модель", "⚙️ Сменить модель"],
            ["📌 Заметки", "✅ Календарь"],
            ["❓ Помощь"]
        ]
        
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="Выбери действие или напиши сообщение..."
        )

        await update.message.reply_text(
            f"""
{greeting}, {user_name}!

Я готова помочь с решением различных задач. Здесь ты можешь получить информацию, ответы на вопросы или оперативную помощь. 
Чтобы начать, просто напиши, что тебя интересует, или воспользуйся меню команд.
""".strip(),
            parse_mode='HTML',
            reply_markup=reply_markup
        )

    # Обработчик нажатий на reply-кнопки
    async def handle_reply_buttons(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        
        # Обработка кнопок
        if text == "❓ Помощь":
            await self.call_help_command(update, context)
        elif text == "🧠Текущая AI модель":
            await self.call_model_command(update, context)
        elif text == "⚙️ Сменить модель":
            await self.show_model_switch_keyboard(update, context)
        elif text == "📌 Заметки":
            await update.message.reply_text("📌 Раздел заметок в разработке...")
        elif text == "✅ Календарь":
            await update.message.reply_text("✅ Раздел календаря в разработке...")
        elif text in ["ChatGPT-5", "DeepSeek V3", "QWEN Coder", "Sonar"]:
            await self.handle_model_selection(update, context, text)
        elif text == "🔙 Назад":
            await self.start_command(update, context)
        else:
            # Если текст не соответствует кнопкам, передаем в AI обработчик
            # Для этого нужно получить доступ к ai_handler через контекст
            if 'ai_handler' in context.bot_data:
                await context.bot_data['ai_handler'].handle_message(update, context)

    async def show_model_switch_keyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показывает клавиатуру для смены модели"""
        model_keyboard = [
            ["ChatGPT-5", "DeepSeek V3"],
            ["QWEN Coder", "Sonar"],
            ["🔙 Назад"]
        ]
        
        reply_markup = ReplyKeyboardMarkup(
            model_keyboard,
            resize_keyboard=True,
            input_field_placeholder="Выбери модель AI..."
        )
        
        await update.message.reply_text(
            "⚙️ <b>Выбери AI модель:</b>",
            parse_mode='HTML',
            reply_markup=reply_markup
        )

    async def handle_model_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, model_text: str):
        """Обрабатывает выбор модели AI"""
        model_mapping = {
            "ChatGPT-5": self.call_gpt_command,
            "DeepSeek V3": self.call_deepseek_command,
            "QWEN Coder": self.call_qwen_command,
            "Sonar": self.call_sonar_command
        }
        
        handler = model_mapping.get(model_text)
        if handler:
            await handler(update, context)
        else:
            await update.message.reply_text("Модель не найдена")

    # Методы для вызова существующих команд
    async def call_help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вызывает команду /help"""
        from .help import HelpCommand
        help_cmd = HelpCommand()
        await help_cmd.help_command(update, context)

    async def call_model_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вызывает команду /model"""
        from ..model_commands import ModelCommands
        # Получаем ai_service из контекста бота
        ai_service = context.bot_data.get('ai_service')
        if ai_service:
            model_cmd = ModelCommands(ai_service)
            await model_cmd.model_info(update, context)
        else:
            await update.message.reply_text("Ошибка: сервис AI не доступен")

    async def call_gpt_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вызывает команду /gpt"""
        from ..model_commands import ModelCommands
        ai_service = context.bot_data.get('ai_service')
        if ai_service:
            model_cmd = ModelCommands(ai_service)
            await model_cmd.set_model_gpt(update, context)

    async def call_deepseek_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вызывает команду /deepseek"""
        from ..model_commands import ModelCommands
        ai_service = context.bot_data.get('ai_service')
        if ai_service:
            model_cmd = ModelCommands(ai_service)
            await model_cmd.set_model_deepseek(update, context)

    async def call_qwen_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вызывает команду /qwen"""
        from ..model_commands import ModelCommands
        ai_service = context.bot_data.get('ai_service')
        if ai_service:
            model_cmd = ModelCommands(ai_service)
            await model_cmd.set_model_qwen(update, context)

    async def call_sonar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вызывает команду /sonar"""
        from ..model_commands import ModelCommands
        ai_service = context.bot_data.get('ai_service')
        if ai_service:
            model_cmd = ModelCommands(ai_service)
            await model_cmd.set_model_sonar(update, context)
    
    async def get_time_greeting(self):
        current_hour = datetime.datetime.now().hour
        
        if 5 <= current_hour < 12:
            return "Доброе утро"
        elif 12 <= current_hour < 17:
            return "Добрый день"
        elif 17 <= current_hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"