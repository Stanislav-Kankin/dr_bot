import asyncio
import logging
from aiogram import Bot, Dispatcher

from config_data.config import BOT_TOKEN
from database.database import create_db
from handlers import user_handlers, other_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

async def main():
    # Создание базы данных
    await create_db()
    
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Регистрация роутеров
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())