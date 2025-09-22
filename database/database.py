import aiosqlite
import os

DB_PATH = 'database/users.db'

async def create_db():
    """Создание базы данных"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')
        await db.commit()

async def check_user(user_id: int) -> bool:
    """Проверка, проходил ли пользователь викторину"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            'SELECT completed FROM users WHERE user_id = ?', 
            (user_id,)
        )
        result = await cursor.fetchone()
        return result is not None and result[0]

async def add_user(user_id: int):
    """Добавление пользователя в базу после завершения"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            'INSERT OR REPLACE INTO users (user_id, completed) VALUES (?, ?)',
            (user_id, True)
        )
        await db.commit()