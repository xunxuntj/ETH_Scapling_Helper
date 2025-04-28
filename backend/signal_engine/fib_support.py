import pandas as pd

class FibSupport:
    def find_levels(self, data: pd.DataFrame):
        """Finds potential Fibonacci support and resistance levels."""
        # TODO: Implement a more sophisticated method to identify significant swing highs and lows
        # to accurately draw Fibonacci retracement and extension levels.
        # This is a simplified example.

        highest_high = data['high'].max()
        lowest_low = data['low'].min()
        diff = highest_high - lowest_low

        levels = {
            "0%": highest_high,
            "23.6%": highest_high - 0.236 * diff,
            "38.2%": highest_high - 0.382 * diff,
            "50%": highest_high - 0.5 * diff,
            "61.8%": highest_high - 0.618 * diff,
            "78.6%": highest_high - 0.786 * diff,
            "100%": lowest_low,
        }
        return levels

    def check_price_near_level(self, current_price: float, levels: dict, tolerance: float = 0.005):
        """Checks if the current price is near a Fibonacci level within a tolerance."""
        near_levels = []
        for level_name, level_price in levels.items():
            if abs(current_price - level_price) / level_price <= tolerance:
                near_levels.append(level_name)
        return near_levels
