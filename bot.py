import asyncio
import logging
from aiogram import Dispatcher
from handlers import authors, common, predict, rate
from main.botdef import bot


# Запуск процесса поллинга новых апдейтов
async def main():
    logging.basicConfig(filename="bot.log", encoding="utf-8", level=logging.INFO)
    # logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    dp.include_routers(predict.router, authors.router, rate.router, common.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
