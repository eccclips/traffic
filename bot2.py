import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from config2 import TOKEN, CHANNELS

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция проверки подписки
async def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel["name"], user_id=user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                return False  # Пользователь не подписан на канал
        except Exception as e:
            logging.error(f"Ошибка проверки подписки на {channel['name']}: {e}")
            return False  # Ошибка доступа (например, приватный канал без админа бота)
    return True

async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Подписаться на {channel['name']}", url=channel["link"])
         for channel in CHANNELS]
    ])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="✅ Я подписался!", callback_data="check_sub")])

    await message.answer("Чтобы продолжить, подпишитесь на каналы:", reply_markup=keyboard)

async def check_subscription_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await check_subscription(user_id):
        await callback.answer("✅ Вы подписаны на все каналы!")
        await bot.send_message(user_id, "🎉 Спасибо за подписку! Теперь у вас есть доступ.")
    else:
        await callback.answer("❌ Вы не подписаны на все каналы. Подпишитесь и попробуйте снова!", show_alert=True)

def register_handlers():
    dp.message.register(start, Command("start"))
    dp.callback_query.register(check_subscription_callback, F.data == "check_sub")

async def main():
    register_handlers()  # Регистрируем хендлеры
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())