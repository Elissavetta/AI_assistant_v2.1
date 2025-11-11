from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
import asyncio

class ClearCommand:
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        
        # Проверка прав в группах
        if chat.type != ChatType.PRIVATE:
            bot_member = await chat.get_member(context.bot.id)
            if not bot_member.can_delete_messages:
                await update.message.reply_text("❌ Нет прав для удаления сообщений")
                return
        
        chat_id = chat.id
        current_id = update.message.message_id
        
        # Сразу отправляем сообщение
        result_msg = await context.bot.send_message(chat_id, "🔄 Очищаю чат...")
        
        deleted_count = 0
        
        # Удаляем команду clear
        try:
            await context.bot.delete_message(chat_id, current_id)
            deleted_count += 1
        except:
            pass
        
        # Удаляем 100 сообщений быстрым перебором
        for i in range(1, 101):
            try:
                target_id = current_id - i
                # Быстрое удаление без задержек
                await context.bot.delete_message(chat_id, target_id)
                deleted_count += 1
            except:
                # Мгновенно переходим к следующему сообщению
                pass
        
        # Мгновенно обновляем результат
        await result_msg.edit_text(f"✅ Удалено {deleted_count} сообщений")
        
        # Удаляем подтверждение через 3 секунды
        await asyncio.sleep(3)
        await result_msg.delete()