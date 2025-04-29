from database.db import create_connection, save_history, get_history
from datetime import datetime

class TradingLogic:
    def __init__(self):
        self.conn = create_connection("trading_history.db")
        if self.conn:
            create_tables(self.conn)

    def save_trade(self, price, volume, signal_type, signal_strength):
        """Save trade to database"""
        trade_data = {
            "timestamp": datetime.now().timestamp(),
            "price": price,
            "volume": volume,
            "signal_type": signal_type,
            "signal_strength": signal_strength
        }
        save_history(self.conn, trade_data)

    def get_recent_trades(self, limit=100):
        """Get recent trades from database"""
        return get_history(self.conn, limit)
