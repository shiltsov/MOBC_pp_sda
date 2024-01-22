import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import authors, common, predict, rate
from main.botdef import bot 

# Запуск процесса поллинга новых апдейтов
async def main():
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    dp.include_routers(common.router, predict.router, authors.router, rate.router)   
        
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())