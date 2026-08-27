import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message):
    await message.answer("✅ Бот работает! Сессия не нужна.")

async def main():
    logging.info("🚀 Тестовый бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())