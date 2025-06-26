import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID"))
