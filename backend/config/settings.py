import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings:
    GATEIO_API_KEY: Optional[str] = os.getenv("GATEIO_API_KEY")
    GATEIO_SECRET_KEY: Optional[str] = os.getenv("GATEIO_SECRET_KEY")
    GATEIO_ORDER_API_KEY: Optional[str] = os.getenv("GATEIO_ORDER_API_KEY")
    GATEIO_ORDER_SECRET_KEY: Optional[str] = os.getenv("GATEIO_ORDER_SECRET_KEY")
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

settings = Settings()
