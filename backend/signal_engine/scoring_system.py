class ScoringSystem:
    def calculate_score(self, trend_status: str, macd_rsi_signals: dict, fib_levels_near: list, candle_patterns: dict, large_timeframe_trend: str, atr_value: float):
        """Calculates a signal score based on various factors."""
        score = 0

        # Trend direction confirmation
        if trend_status == "uptrend":
            score += 2
        elif trend_status == "downtrend":
            score += 2

        # Short-term momentum (MACD)
        if macd_rsi_signals.get('macd_golden_cross'):
            score += 1.5
        elif macd_rsi_signals.get('macd_death_cross'):
            score += 1.5

        # RSI signals
        if macd_rsi_signals.get('rsi_overbought') or macd_rsi_signals.get('rsi_oversold'):
             # Basic scoring for overbought/oversold, will need refinement based on strategy
            score += 0.5 # Reduced score for just overbought/oversold without divergence
        # Add scoring for RSI divergence
        if macd_rsi_signals.get('rsi_bullish_divergence'):
            score += 1.0 # Example score for bullish divergence
        elif macd_rsi_signals.get('rsi_bearish_divergence'):
            score += 1.0 # Example score for bearish divergence


        # Fibonacci support/resistance
        if fib_levels_near:
            score += 2

        # Candle patterns
        if candle_patterns:
            score += 1.5

        # Large timeframe support
        if (trend_status == "uptrend" and large_timeframe_trend == "uptrend") or \
           (trend_status == "downtrend" and large_timeframe_trend == "downtrend"):
            score += 2

        # Deductions for conflicting signals or extreme volatility
        # Implement logic for deducting points based on conflicting signals or high ATR (simplified)
        # Deduct if MACD and Vegas Tunnel trends conflict
        if (trend_status == "uptrend" and macd_rsi_signals.get('macd_death_cross')) or \
           (trend_status == "downtrend" and macd_rsi_signals.get('macd_golden_cross')):
            score -= 1.0 # Example deduction

        # Deduct if RSI is overbought in uptrend or oversold in downtrend (potential reversal)
        if (trend_status == "uptrend" and macd_rsi_signals.get('rsi_overbought')) or \
           (trend_status == "downtrend" and macd_rsi_signals.get('rsi_oversold')):
            score -= 0.5 # Example deduction

        # TODO: Add deduction based on high ATR (requires ATR value as input)

        # Ensure score is within 0-10 range
        score = max(0, min(10, score))

        return score

    def interpret_score(self, score: float):
        """Interprets the score to provide action advice."""
        if score >= 8:
            return "极强信号 - 积极执行开仓"
        elif score >= 6:
            return "中等偏强 - 可谨慎开仓，小仓位试探"
        elif score >= 4:
            return "中性观望 - 暂不进场，等待确认"
        else:
            return "极弱或无方向 - 严禁进场"
