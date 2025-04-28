import telegram

class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=bot_token)

    def send_message(self, message: str):
        """Sends a message to the configured Telegram chat."""
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
            print(f"Telegram message sent: {message}")
        except Exception as e:
            print(f"Error sending Telegram message: {e}")

    def send_signal_notification(self, signal_details: dict):
        """Sends a formatted notification for a trading signal."""
        message = f"📈 New Trading Signal!\n\n" \
                  f"Score: {signal_details.get('score', 'N/A')}\n" \
                  f"Trend: {signal_details.get('trend_status', 'N/A')}\n" \
                  f"Signal Type: {signal_details.get('signal_type', 'N/A')}\n" \
                  f"Details: {signal_details.get('details', 'N/A')}"
        self.send_message(message)

    def send_trade_notification(self, trade_details: dict):
        """Sends a formatted notification for a trade execution or adjustment."""
        message = f"📊 Trade Update!\n\n" \
                  f"Action: {trade_details.get('action', 'N/A')}\n" \
                  f"Symbol: {trade_details.get('symbol', 'N/A')}\n" \
                  f"Price: {trade_details.get('price', 'N/A')}\n" \
                  f"Profit/Loss: {trade_details.get('profit', 'N/A')}\n" \
                  f"Notes: {trade_details.get('notes', 'N/A')}"
        self.send_message(message)
