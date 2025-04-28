import pandas as pd

class VegasTunnel:
    def __init__(self, ema_short=85, ema_medium=144, ema_long=169):
        self.ema_short = ema_short
        self.ema_medium = ema_medium
        self.ema_long = ema_long

    def calculate_emas(self, data: pd.DataFrame):
        """Calculates the Vegas Tunnel EMAs."""
        data[f'EMA_{self.ema_short}'] = data['close'].ewm(span=self.ema_short, adjust=False).mean()
        data[f'EMA_{self.ema_medium}'] = data['close'].ewm(span=self.ema_medium, adjust=False).mean()
        data[f'EMA_{self.ema_long}'] = data['close'].ewm(span=self.ema_long, adjust=False).mean()
        return data

    def identify_trend(self, data: pd.DataFrame):
        """Identifies the trend based on Vegas Tunnel."""
        if data[f'EMA_{self.ema_short}'].iloc[-1] > data[f'EMA_{self.ema_medium}'].iloc[-1] > data[f'EMA_{self.ema_long}'].iloc[-1]:
            return "uptrend"
        elif data[f'EMA_{self.ema_short}'].iloc[-1] < data[f'EMA_{self.ema_medium}'].iloc[-1] < data[f'EMA_{self.ema_long}'].iloc[-1]:
            return "downtrend"
        elif (data[f'EMA_{self.ema_short}'].iloc[-1] > data[f'EMA_{self.ema_medium}'].iloc[-1] and
              data[f'EMA_{self.ema_medium}'].iloc[-1] < data[f'EMA_{self.ema_long}'].iloc[-1]):
            return "potential_downtrend_reversal" # Example of other conditions
        elif (data[f'EMA_{self.ema_short}'].iloc[-1] < data[f'EMA_{self.ema_medium}'].iloc[-1] and
              data[f'EMA_{self.ema_medium}'].iloc[-1] > data[f'EMA_{self.ema_long}'].iloc[-1]):
            return "potential_uptrend_reversal" # Example of other conditions
        else:
            return "sideways"
