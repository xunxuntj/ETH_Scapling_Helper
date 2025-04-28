import pandas as pd
import pandas_ta as ta

class AtrTrailing:
    def calculate_atr(self, data: pd.DataFrame, length: int = 14):
        """Calculates Average True Range (ATR)."""
        data.ta.atr(length=length, append=True)
        return data

    def calculate_trailing_levels(self, current_price: float, atr_value: float, position_direction: str, multiplier: float = 2.0):
        """Calculates dynamic trailing stop loss and take profit levels based on ATR."""
        # This is a basic example. More sophisticated trailing stops exist.
        # TODO: Refine trailing logic based on specific strategy rules (e.g., parabolic SAR, fixed percentage)

        if position_direction == "long":
            stop_loss = current_price - atr_value * multiplier
            take_profit = current_price + atr_value * multiplier # Basic take profit for now
        elif position_direction == "short":
            stop_loss = current_price + atr_value * multiplier
            take_profit = current_price - atr_value * multiplier # Basic take profit for now
        else:
            return None, None # Should not happen in a typical trading scenario

        return stop_loss, take_profit
