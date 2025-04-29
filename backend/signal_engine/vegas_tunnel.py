import pandas as pd
import numpy as np
from typing import Dict, Tuple

class VegasTunnel:
    def __init__(self, ema_short=85, ema_medium=144, ema_long=169):
        self.ema_short = ema_short
        self.ema_medium = ema_medium 
        self.ema_long = ema_long
        self.timeframe_ratios = [1, 4, 16]  # 1m, 4m, 16m timeframes

    def calculate_emas(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculates EMAs for all configured timeframes"""
        for ratio in self.timeframe_ratios:
            span_short = self.ema_short * ratio
            span_medium = self.ema_medium * ratio
            span_long = self.ema_long * ratio
            
            data[f'EMA_{span_short}'] = data['close'].ewm(
                span=span_short, adjust=False).mean()
            data[f'EMA_{span_medium}'] = data['close'].ewm(
                span=span_medium, adjust=False).mean()
            data[f'EMA_{span_long}'] = data['close'].ewm(
                span=span_long, adjust=False).mean()
        return data

    def calculate_trend_strength(self, data: pd.DataFrame) -> float:
        """Calculates trend strength score (0-1) based on EMA alignment"""
        ema_short = data[f'EMA_{self.ema_short}'].iloc[-1]
        ema_medium = data[f'EMA_{self.ema_medium}'].iloc[-1] 
        ema_long = data[f'EMA_{self.ema_long}'].iloc[-1]
        
        if ema_short > ema_medium > ema_long:  # Strong uptrend
            return min(1.0, (ema_short - ema_long) / ema_long * 0.1)
        elif ema_short < ema_medium < ema_long:  # Strong downtrend
            return min(1.0, (ema_long - ema_short) / ema_short * 0.1)
        return 0.0  # Weak or no trend

    def identify_trend(self, data: pd.DataFrame) -> Tuple[str, float]:
        """Identifies trend with strength score"""
        trend = "sideways"
        strength = 0.0
        
        if data[f'EMA_{self.ema_short}'].iloc[-1] > data[f'EMA_{self.ema_medium}'].iloc[-1] > data[f'EMA_{self.ema_long}'].iloc[-1]:
            trend = "uptrend"
            strength = self.calculate_trend_strength(data)
        elif data[f'EMA_{self.ema_short}'].iloc[-1] < data[f'EMA_{self.ema_medium}'].iloc[-1] < data[f'EMA_{self.ema_long}'].iloc[-1]:
            trend = "downtrend" 
            strength = self.calculate_trend_strength(data)
            
        return trend, strength

    def validate_emas(self, data: pd.DataFrame) -> bool:
        """Validates EMA calculations"""
        for ratio in self.timeframe_ratios:
            span_short = self.ema_short * ratio
            if f'EMA_{span_short}' not in data.columns:
                return False
        return True


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
