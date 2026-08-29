from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from message import router
from configdatastorage import token
from basedatastorage import init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("bottask6.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

async def main():
    init_db()
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.info('🎉Бот запущен админом(консоль), приятного использования!')
        print('=' * 50)
        print('🎉Бот запущен, приятного использования!')
        print('=' * 50)
        asyncio.run(main())   
    except KeyboardInterrupt:
        logging.error("Бот остановлен😴🛑")
        print("\n🛑 Бот остановлен")