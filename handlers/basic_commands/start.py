from telegram import Update
from telegram.ext import ContextTypes
import datetime


class StartCommand:

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.effective_user.first_name
        greeting =  await self.get_time_greeting()

        await update.message.reply_text(f"""
{greeting}, {user_name}!
Я твой личный AI асcистент, с помощью меня ты можешь взаимодействаовать с выбранной моделью AI прямо из чата
Для вызова справки используй команду /help     
""".strip(),
   parse_mode='HTML'
        )

    
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



