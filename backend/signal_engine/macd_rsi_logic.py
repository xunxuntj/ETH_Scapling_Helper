import pandas as pd
import pandas_ta as ta

class MacdRsiLogic:
    def calculate_indicators(self, data: pd.DataFrame):
        """Calculates MACD and RSI."""
        data.ta.macd(close=data['close'], append=True)
        data.ta.rsi(close=data['close'], append=True)
        return data

    def check_signals(self, data: pd.DataFrame):
        """Checks for MACD and RSI signals (golden cross, death cross, overbought, oversold, divergence)."""
        signals = {}

        # MACD signals
        if data['MACDh_12_26_9'].iloc[-2] <= 0 and data['MACDh_12_26_9'].iloc[-1] > 0:
            signals['macd_golden_cross'] = True
        elif data['MACDh_12_26_9'].iloc[-2] >= 0 and data['MACDh_12_26_9'].iloc[-1] < 0:
            signals['macd_death_cross'] = True

        # RSI signals
        if data['RSI_14'].iloc[-1] > 70:
            signals['rsi_overbought'] = True
        elif data['RSI_14'].iloc[-1] < 30:
            signals['rsi_oversold'] = True

        # Implement RSI divergence detection (simplified)
        # Bullish divergence: Lower low in price, higher low in RSI
        if len(data) >= 2 and data['close'].iloc[-1] < data['close'].iloc[-2] and data['RSI_14'].iloc[-1] > data['RSI_14'].iloc[-2]:
             signals['rsi_bullish_divergence'] = True
        # Bearish divergence: Higher high in price, lower high in RSI
        if len(data) >= 2 and data['close'].iloc[-1] > data['close'].iloc[-2] and data['RSI_14'].iloc[-1] < data['RSI_14'].iloc[-2]:
             signals['rsi_bearish_divergence'] = True

        return signals
