import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import start, stocks
from database import init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(stocks.router)

async def main():
    init_db()

    try:
        async with aiohttp.ClientSession() as session:
            bot.my_session = session

            logging.info("🚀 Бот запущен!")
            await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка в main: {e}")
        raise
    finally:
        logging.info("🔒 Бот завершил работу")
        

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен вручную")
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
