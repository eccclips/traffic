import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters  # Обновленный импорт для Filters

# Импортируем настройки из config1.py
from config1 import BOT_TOKEN, MY_CHANNELS, SOURCE_CHANNELS, CHANNEL_MAPPING

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    """Отправляет приветственное сообщение."""
    await update.message.reply_text('Hello! This bot is monitoring channels.')


async def forward_message(update: Update, context: CallbackContext):
    """Обрабатывает новые сообщения в каналах и пересылает их в соответствующие ваши каналы."""
    source_channel = update.channel_post.chat.username
    logger.info(f"Received a post from channel: {source_channel}")

    if source_channel in SOURCE_CHANNELS:
        target_channel = CHANNEL_MAPPING.get(source_channel)

        if target_channel:
            # Пересылаем сообщение без указания источника
            await context.bot.forward_message(
                chat_id=target_channel,
                from_chat_id=update.channel_post.chat.id,
                message_id=update.channel_post.message_id
            )
            logger.info(f"Message forwarded to: {target_channel}")
        else:
            logger.warning(f"No target channel found for {source_channel}")
    else:
        logger.warning(f"Message from {source_channel} not in SOURCE_CHANNELS.")


def main():
    """Основной цикл работы бота."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, forward_message))

    application.run_polling()
    logger.info("Bot started")


if __name__ == '__main__':
    main()