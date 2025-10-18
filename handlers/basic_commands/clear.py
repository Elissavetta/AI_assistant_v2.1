from telegram import Update
from telegram.ext import ContextTypes
import logging

class ClearCommand:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Простая и надежная очистка чата"""
        try:
            chat_id = update.effective_chat.id
            current_message_id = update.message.message_id
            
            self.logger.info(f"Clear command called in chat {chat_id}, message {current_message_id}")
            
            # Сразу пытаемся удалить команду clear
            try:
                await context.bot.delete_message(chat_id, current_message_id)
                self.logger.info("Clear command message deleted")
            except Exception as e:
                self.logger.warning(f"Could not delete clear command: {e}")
            
            deleted_count = 0
            
            # Пробуем удалить 100 сообщений ПОД текущим сообщением
            for i in range(1, 101):
                try:
                    target_id = current_message_id - i
                    if target_id <= 0:
                        break
                    
                    await context.bot.delete_message(chat_id, target_id)
                    deleted_count += 1
                    self.logger.info(f"Deleted message {target_id}")
                    
                except Exception as e:
                    # Просто продолжаем при любой ошибке
                    continue
            
            # Отправляем результат
            result_msg = await context.bot.send_message(
                chat_id, 
                f"✅ Удалено {deleted_count} сообщений"
            )
            
            # Пытаемся удалить результат через 3 секунды
            try:
                import asyncio
                await asyncio.sleep(3)
                await context.bot.delete_message(chat_id, result_msg.message_id)
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"Clear command failed: {e}")
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")