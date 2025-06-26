import asyncio
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from config import Config

from .utils import generate_mentions
from .db import save_user


reminder_router = Router()
MSK = ZoneInfo("Europe/Moscow")

@reminder_router.message(Command("n"))
async def remind_handler(message: Message, bot: Bot):
    if message.chat.id != Config.ALLOWED_CHAT_ID:
        await message.answer("⛔Я работаю только определенном чате.")
        return

    # Сохраняем пользователя
    save_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )

    text = message.text[len("/n "):].strip()
    match_relative = re.search(r"(.+?) через (\d+)([mh])", text, re.IGNORECASE)
    match_absolute = re.search(r"(.+?) (\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2})", text)

    if match_relative:
        reminder_text, amount, unit = match_relative.groups()
        delay = int(amount) * 60 if unit.lower() == "m" else int(amount) * 3600
        remind_time = datetime.now(MSK) + timedelta(seconds=delay)

    elif match_absolute:
        reminder_text, date_str, time_str = match_absolute.groups()
        try:
            remind_time = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M").replace(tzinfo=MSK)
        except ValueError:
            await message.answer("Неверный формат даты.")
            return
    else:
        await message.answer("Формат:\n/n текст через 10m\nили\n/n текст 01.06.2025 12:00")
        return

    user = message.from_user.mention_html()
    chat_id = message.chat.id
    await message.answer(f"🔔 Напоминание установлено на {remind_time.strftime('%d.%m.%Y %H:%M')} (МСК)")

    async def wait_and_remind():
        delay = (remind_time - datetime.now(MSK)).total_seconds()
        if delay > 0:
            await asyncio.sleep(delay)
        mentions = generate_mentions()
        await bot.send_message(chat_id, f"🔔 {user} напомнил: <b>{reminder_text}</b>\n{mentions}")

    asyncio.create_task(wait_and_remind())

