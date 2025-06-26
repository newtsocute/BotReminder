from aiogram import Dispatcher
from .reminder import reminder_router
from .tracker import tracker_router


def register_routers(dp: Dispatcher):
    dp.include_router(reminder_router)
    dp.include_router(tracker_router)

