from aiogram import Router
from aiogram.types import Message
from .db import save_user

tracker_router = Router()

@tracker_router.message()
async def track_user(message: Message):
    save_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )
