# Trading Pair
TRADING_PAIR = "ETH_USDT"

# Timeframe for K-lines
KLINE_INTERVAL = "1m"
KLINE_LIMIT = 100 # Number of recent k-lines to fetch

# Vegas Tunnel EMA periods
VEGAS_EMA_SHORT = 85
VEGAS_EMA_MEDIUM = 144
VEGAS_EMA_LONG = 169

# MACD parameters
MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9

# RSI parameters
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# ATR parameters
ATR_PERIOD = 14
ATR_MULTIPLIER = 2.0

# Signal Scoring thresholds
SIGNAL_SCORE_STRONG = 8
SIGNAL_SCORE_MEDIUM = 6
SIGNAL_SCORE_NEUTRAL = 4

# Trailing Stop Loss and Take Profit
INITIAL_STOP_LOSS_USD = 10.0
INITIAL_TAKE_PROFIT_USD = 10.0
TRAILING_TRIGGER_USD = 5.0

# Database
DATABASE_FILE = "sql_app.db"

# Telegram
TELEGRAM_SIGNAL_NOTIFICATION_PREFIX = "📈 New Trading Signal!"
TELEGRAM_TRADE_NOTIFICATION_PREFIX = "📊 Trade Update!"

# Scheduled Task
SIGNAL_REFRESH_INTERVAL_SECONDS = 60 # Refresh signals every minute
