import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings:
    GATE_IO_READ_ONLY_KEY: Optional[str] = os.getenv("GATE_IO_READ_ONLY_KEY")
    GATE_IO_READ_ONLY_SECRET: Optional[str] = os.getenv("GATE_IO_READ_ONLY_SECRET")
    GATE_IO_TRADE_KEY: Optional[str] = os.getenv("GATE_IO_TRADE_KEY") 
    GATE_IO_TRADE_SECRET: Optional[str] = os.getenv("GATE_IO_TRADE_SECRET")
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

settings = Settings()
