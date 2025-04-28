from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import time
import asyncio
import pandas as pd

from .database import models, db
from .signal_engine.vegas_tunnel import VegasTunnel
from .signal_engine.macd_rsi_logic import MacdRsiLogic
from .signal_engine.fib_support import FibSupport
from .signal_engine.atr_trailing import AtrTrailing
from .signal_engine.candle_patterns import CandlePatterns
from .signal_engine.scoring_system import ScoringSystem
from .trading_assistant.trailing_manager import TrailingManager
from .trading_assistant.telegram_notifier import TelegramNotifier
from .gateio_client.api_client import GateioClient
from .config.settings import settings
from .config.constants import *

app = FastAPI()

# Initialize database
models.Base.metadata.create_all(bind=db.engine)

# Initialize components
gateio_client = GateioClient()
vegas_tunnel = VegasTunnel(VEGAS_EMA_SHORT, VEGAS_EMA_MEDIUM, VEGAS_EMA_LONG)
macd_rsi_logic = MacdRsiLogic()
fib_support = FibSupport()
atr_trailing = AtrTrailing() # ATR_PERIOD is for calculation, not trailing levels
candle_patterns = CandlePatterns()
scoring_system = ScoringSystem()
trailing_manager = TrailingManager(INITIAL_STOP_LOSS_USD, INITIAL_TAKE_PROFIT_USD, TRAILING_TRIGGER_USD)
# Handle potential None values for Telegram credentials
telegram_bot_token = settings.TELEGRAM_BOT_TOKEN if settings.TELEGRAM_BOT_TOKEN else "" # TODO: Add proper error handling if None
telegram_chat_id = settings.TELEGRAM_CHAT_ID if settings.TELEGRAM_CHAT_ID else "" # TODO: Add proper error handling if None
telegram_notifier = TelegramNotifier(telegram_bot_token, telegram_chat_id)

async def run_trading_logic():
    """Scheduled task to run trading signal and management logic."""
    while True:
        print("Running trading logic...")
        
        # 1. Fetch k-line data
        klines_data = gateio_client.get_klines(TRADING_PAIR, KLINE_INTERVAL, KLINE_LIMIT)
        if not klines_data:
            print("Failed to fetch k-line data. Skipping this cycle.")
            await asyncio.sleep(SIGNAL_REFRESH_INTERVAL_SECONDS)
            continue

        # Convert klines data to pandas DataFrame
        # Assuming klines_data is a list of lists/tuples in the format [timestamp, open, high, low, close, volume]
        df = pd.DataFrame(klines_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s') # Convert timestamp to datetime
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float) # Convert price/volume to float

        # 2. Calculate indicators
        df = vegas_tunnel.calculate_emas(df)
        df = macd_rsi_logic.calculate_indicators(df)
        # Integrate FibSupport and AtrTrailing calculations
        df = atr_trailing.calculate_atr(df, ATR_PERIOD)
        current_atr_value = df['ATR_14'].iloc[-1] if 'ATR_14' in df.columns else 0.0 # Get the latest ATR value

        # Calculate FibSupport and CandlePatterns
        fib_levels = fib_support.find_levels(df)
        current_price = df['close'].iloc[-1]
        fib_levels_near = fib_support.check_price_near_level(current_price, fib_levels)
        candle_patterns_detected = candle_patterns.identify_patterns(df)

        # TODO: Pass large timeframe trend to scoring system
        large_timeframe_trend = "sideways" # Placeholder

        # 3. Calculate signal score
        # Extract necessary data from df for scoring
        current_trend_status = vegas_tunnel.identify_trend(df)
        current_macd_rsi_signals = macd_rsi_logic.check_signals(df)

        signal_score = scoring_system.calculate_score(
            current_trend_status,
            current_macd_rsi_signals,
            fib_levels_near,
            candle_patterns_detected,
            large_timeframe_trend,
            current_atr_value # Pass ATR value
        )

        # 4. Generate and log signals
        signal_details = {
            "score": signal_score,
            "details": scoring_system.interpret_score(signal_score),
            "trend_direction": current_trend_status,
            # TODO: Add other relevant signal details from indicators and patterns
            "signal_type": "BUY" if signal_score >= SIGNAL_SCORE_STRONG and current_trend_status == "uptrend" else "SELL" if signal_score >= SIGNAL_SCORE_STRONG and current_trend_status == "downtrend" else "NEUTRAL" # Basic signal type
        }

        # Log signal to the database
        db_signal = models.Signal(
            score=signal_details['score'],
            details=signal_details['details'],
            trend_direction=signal_details['trend_direction'],
            # TODO: Map other signal details to model fields
            signal_type=signal_details['signal_type']
        )
        
        # Add session and commit to database
        db_session = next(db.get_db()) # Get a database session
        try:
            db_session.add(db_signal)
            db_session.commit()
            db_session.refresh(db_signal) # Refresh to get the assigned ID
            print(f"Signal logged to database with ID: {db_signal.id}")
        except Exception as e:
            db_session.rollback()
            print(f"Error logging signal to database: {e}")
        finally:
            db_session.close()

        print(f"Generated Signal: {signal_details}")

        # 5. Check for open positions
        # TODO: Implement get_open_positions in GateioClient (needs order API keys)
        open_positions = gateio_client.get_open_positions(TRADING_PAIR) # Placeholder call

        # 6. Calculate and adjust trailing stop loss/take profit
        if open_positions:
            print(f"Checking {len(open_positions)} open positions for adjustments...")
            for position in open_positions:
                # TODO: Extract necessary data from position object (open_price, current_stop_loss, current_take_profit, etc.)
                # Assuming position is a dict-like object with relevant keys
                trade_data = {
                    'open_price': float(position.get('entry_price', 0.0)), # Placeholder key
                    'current_stop_loss': float(position.get('stop_loss', None)) if position.get('stop_loss') is not None else None, # Placeholder key
                    'current_take_profit': float(position.get('take_profit', None)) if position.get('take_profit') is not None else None, # Placeholder key
                    'initial_stop_loss': INITIAL_STOP_LOSS_USD, # Assuming initial values are stored or accessible
                    'initial_take_profit': INITIAL_TAKE_PROFIT_USD, # Assuming initial values are stored or accessible
                    'position_direction': position.get('side') # Assuming 'side' indicates 'long' or 'short'
                }
                current_price = df['close'].iloc[-1] # Use the latest close price
                # TODO: Get ATR value for the current timeframe (maybe from the calculated df)
                current_atr_for_trailing = df['ATR_14'].iloc[-1] if 'ATR_14' in df.columns else 0.0 # Using the calculated ATR

                needs_adjustment, new_stop_loss, new_take_profit = trailing_manager.check_for_adjustment(
                    trade_data,
                    current_price,
                    0.0 # Placeholder for ATR value
                )

                if needs_adjustment:
                    print(f"Adjustment needed for position: {position}. New SL: {new_stop_loss}, New TP: {new_take_profit}")
                    # Implement logic to update stop loss/take profit on GateIO (placeholder)
                    # TODO: Implement amend_order in GateioClient (needs order API keys)
                    # Assuming position object contains order ID or similar identifier
                    # gateio_client.amend_order(position.get('order_id'), new_stop_loss, new_take_profit) # Placeholder call

                    # Log the adjustment to the database (placeholder)
                    # TODO: Log the stop loss/take profit adjustment in the database (e.g., in the Trade table or a separate adjustments table)


        # 7. Log trades and capital snapshots
        # Implement logic to log trade executions and closures when they occur (placeholder)
        # TODO: Integrate actual trade execution/closure logging when order management is implemented

        # Implement logic to periodically log capital snapshots (placeholder)
        # TODO: Fetch actual capital from GateIO and log to database periodically
        # Example: Log capital snapshot every hour or day

        # 8. Send notifications
        # Use TelegramNotifier to send signal and trade notifications
        # Implement logic to trigger notifications based on signal generation and trade events (placeholder)
        # Example: Send signal notification if a strong signal is generated
        if signal_score >= SIGNAL_SCORE_STRONG:
             telegram_notifier.send_signal_notification(signal_details)
        # Example: Send trade notification when a trade is opened or closed
        # TODO: Call telegram_notifier.send_trade_notification() when trades are executed or closed


        await asyncio.sleep(SIGNAL_REFRESH_INTERVAL_SECONDS)

@app.on_event("startup")
async def startup_event():
    """Starts the background trading logic task."""
    asyncio.create_task(run_trading_logic())

@app.get("/")
def read_root():
    return {"message": "ETH Scalping Assistant Backend"}

# TODO: Add API endpoints for frontend to interact with (e.g., get signals, get trades, manual trade management)
