from telegram import Update
from telegram.ext import ContextTypes


class HelpCommand:

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text(f"""
<b>Поддерживаемые AI модели:</b>
• ChatGPT-5
• DeepSeek V3  
• QWEN - Coder
• Sonar

<b>Список основных команд:</b>
/help - Вызов справки
/model - Узнать текущую модель AI, которая обрабатывает сообщения

<b>Команды для переключения ИИ модели:</b>
/gpt - Переключить модель AI на ChatGPT-5
/deepseek - Переключить модель AI на DeepSeek V3
/qwen - Переключить модель AI на QWEN
/sonar - Переключить модель AI на Sonar

/ivent - Внести задачу в календарь (команда в статусе: "В разработке")
/note  - Сохранить заметку (команда в статусе: "В разработке")

[AI Assistant Ver 2.1]
""".strip(),
       parse_mode='HTML'
       )

