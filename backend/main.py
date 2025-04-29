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
telegram_chat_id = settings.TELEGRAM_CHAT_ID if settings.TELEGRAM_CHAT_ID else ""  # TODO: Add proper error handling if None
if not telegram_bot_token or not telegram_chat_id:  
    raise ValueError("Telegram bot token or chat ID not set. Please configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in your settings.")

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
            
        # 1.1 Fetch large time frame k-line data
        klines_data_large_tf = gateio_client.get_klines(TRADING_PAIR, "4h", 100)
        if not klines_data_large_tf:
            print("Failed to fetch large time frame k-line data. Skipping this cycle.")
            await asyncio.sleep(SIGNAL_REFRESH_INTERVAL_SECONDS)
            continue
        
        df_large_tf = pd.DataFrame(klines_data_large_tf, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df_large_tf[['open', 'high', 'low', 'close', 'volume']] = df_large_tf[['open', 'high', 'low', 'close', 'volume']].astype(float)
        if not klines_data_large_tf:
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

        large_timeframe_trend = vegas_tunnel.calculate_large_timeframe_trend(df_large_tf)

        # 3. Calculate signal score
        # Extract necessary data from df for scoring
        current_trend_status = vegas_tunnel.identify_trend(df)
        current_macd_rsi_signals = macd_rsi_logic.check_signals(df)

        signal_score = scoring_system.calculate_score(
            current_trend_status,
            current_macd_rsi_signals,
            fib_levels_near,
            candle_patterns_detected,
            large_timeframe_trend, #type: ignore
            current_atr_value # Pass ATR value
        )

        # 4. Generate and log signals
        signal_details = {
            "score": signal_score,
            "details": scoring_system.interpret_score(signal_score), # type: ignore
            "trend_direction": current_trend_status,
            "trend_status": current_trend_status,
            "macd_status": current_macd_rsi_signals.get('macd_status'), # type: ignore
            "rsi_status": current_macd_rsi_signals.get('rsi_status'), # type: ignore
            "fib_levels_status": fib_levels_near,
            "candle_patterns_status": candle_patterns_detected,
            "signal_type": "BUY" if signal_score >= SIGNAL_SCORE_STRONG and current_trend_status == "uptrend" else "SELL" if signal_score >= SIGNAL_SCORE_STRONG and current_trend_status == "downtrend" else "NEUTRAL" # Basic signal type
        }

        pass # Placeholder

        # Log signal to the database
        db_signal = models.Signal(
            score=signal_details['score'],
            details=signal_details['details'],
            trend_direction=signal_details['trend_direction'],
            fib_levels_status=signal_details['fib_levels_status'],
            candle_patterns_status=signal_details['candle_patterns_status'],
            signal_type=signal_details['signal_type'],
        )  
        pass # Placeholder
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
        try:
            open_positions = gateio_client.get_open_positions(TRADING_PAIR) # Placeholder call
        except Exception as e:
            print(f"Error fetching open positions: {e}")
            open_positions = None

        # 6. Calculate and adjust trailing stop loss/take profit
        if open_positions:
            print(f"Checking {len(open_positions)} open positions for adjustments...")
            for position in open_positions:
                # TODO: Extract necessary data from position object (open_price, current_stop_loss, current_take_profit, etc.)
                # Assuming position is a dict-like object with relevant keys
                position_size = float(position.get('size', 1.0)) # Get position size, default to 1.0
                is_long = position.get('side') == 'long'
                trade_data = {
                    'open_price': float(position.get('entry_price', 0.0)),
                    'current_stop_loss': float(position.get('liq_price', None)) if not is_long else None,
                    'current_take_profit': None if is_long else float(position.get('liq_price', None)),
                    'initial_stop_loss': INITIAL_STOP_LOSS_USD, # Assuming initial values are stored or accessible
                    'initial_take_profit': INITIAL_TAKE_PROFIT_USD, # Assuming initial values are stored or accessible
                    'position_direction': position.get('side')
                }
                current_price = df['close'].iloc[-1] # Use the latest close price
                current_atr_for_trailing = df['ATR_14'].iloc[-1] if 'ATR_14' in df.columns else 0.0 # Using the calculated ATR

                needs_adjustment, new_stop_loss, new_take_profit = trailing_manager.check_for_adjustment(
                    trade_data,
                    current_price,
                    current_atr_for_trailing,
                    position_size
                )

                if needs_adjustment:
                    print(f"Adjustment needed for position: {position}. New SL: {new_stop_loss}, New TP: {new_take_profit}")
                    gateio_client.amend_order(TRADING_PAIR, position.get('id'), new_stop_loss, new_take_profit)
                # Log the adjustment to the database (placeholder)
                    # TODO: Log the stop loss/take profit adjustment in the database (e.g., in the Trade table or a separate adjustments table)

        # 7. Log trades and capital snapshots
        # Implement logic to log trade executions and closures when they occur (placeholder)
        # TODO: Integrate actual trade execution/closure logging when order management is implemented
        # Example placeholder:
        trade_executed = False
        trade_closed = False
        if trade_executed:
            db_trade = models.Trade(  # type: ignore
                open_price=current_price,
                close_price=current_price,
                profit=0.0,
                signal_id=db_signal.id
            ) # Create Trade object
            db_session = next(db.get_db())
            try:
                db_session.add(db_trade)
                telegram_notifier.send_trade_notification({"action": "Opened", "symbol": TRADING_PAIR, "price": current_price, "notes": "Trade opened based on signal"})
                db_session.commit()
                db_session.refresh(db_trade)
            finally:
                db_session.close()
            pass # Placeholder
            pass # Placeholder

        if trade_closed:
            try:
                telegram_notifier.send_trade_notification({"action": "Closed", "symbol": TRADING_PAIR, "price": current_price, "profit": 0.0, "notes": "Trade closed"})
            except Exception as e:
                print(f"Error sending trade notification: {e}")
        




        try:
            current_capital = gateio_client.get_account_balance("USDT") # Fetch capital
            if current_capital is not None:
                db_capital_snapshot = models.CapitalSnapshot(total_capital=current_capital, funding_phase_id=None) # TODO: Determine funding phase ID
                db_session = next(db.get_db())
                try:
                    db_session.add(db_capital_snapshot)
                    db_session.commit()
                    db_session.refresh(db_capital_snapshot)
                finally:
                    db_session.close()
        except Exception as e:
            print(f"Error fetching capital from GateIO: {e}")


        # 8. Send notifications
        # Use TelegramNotifier to send signal and trade notifications
        # Implement logic to trigger notifications based on signal generation and trade events (placeholder)
        # Example: Send signal notification if a strong signal is generated
        if signal_score >= SIGNAL_SCORE_STRONG:
            try:
                telegram_notifier.send_signal_notification(signal_details)
            except Exception as e:
                print(f"Error sending signal notification: {e}")
        pass # Placeholder


        await asyncio.sleep(SIGNAL_REFRESH_INTERVAL_SECONDS)

@app.on_event("startup")
async def startup_event():
    """Starts the background trading logic task."""
    asyncio.create_task(run_trading_logic())

@app.get("/")
def read_root():
    return {"message": "ETH Scalping Assistant Backend"}

@app.get("/signals")
def get_signals():
    # TODO: Implement logic to fetch signals from the database
    # Placeholder
    db_session = next(db.get_db())
    try:
        signals = db_session.query(models.Signal).order_by(models.Signal.id.desc()).limit(10).all()
        signal_list = [{"score": signal.score, "details": signal.details, "trend_direction": signal.trend_direction, "signal_type": signal.signal_type} for signal in signals]
        return signal_list
    except Exception as e:
        print(f"Error fetching signals from database: {e}")
        return {"message": "Error fetching signals"}
    finally:
        db_session.close()
    pass # Placeholder