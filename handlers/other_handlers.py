from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def other_messages(message: Message):
    await message.answer("Я понимаю только команду /start")