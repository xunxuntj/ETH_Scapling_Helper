from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
import datetime

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    score = Column(Float)
    details = Column(String)
    trend_direction = Column(String)
    vegas_ema_85 = Column(Float)
    vegas_ema_144 = Column(Float)
    vegas_ema_169 = Column(Float)
    macd_status = Column(String)
    rsi_status = Column(String)
    fib_level = Column(Float, nullable=True) # Assuming a single relevant level can be stored
    candle_pattern = Column(String, nullable=True)
    large_timeframe_trend = Column(String)
    signal_type = Column(String) # "BUY" or "SELL"

    trades = relationship("Trade", back_populates="signal")

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("signals.id"))
    open_time = Column(DateTime, default=datetime.datetime.utcnow)
    close_time = Column(DateTime, nullable=True)
    open_price = Column(Float)
    close_price = Column(Float, nullable=True)
    profit = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    initial_stop_loss = Column(Float, nullable=True)
    initial_take_profit = Column(Float, nullable=True)
    current_stop_loss = Column(Float, nullable=True)
    current_take_profit = Column(Float, nullable=True)
    atr_value = Column(Float, nullable=True)

    signal = relationship("Signal", back_populates="trades")

class FundingPhase(Base):
    __tablename__ = "funding_phases"

    id = Column(Integer, primary_key=True, index=True)
    phase_number = Column(Integer)
    start_capital = Column(Float)
    target_capital = Column(Float)
    suggested_order_amount = Column(String)
    notes = Column(String, nullable=True)

    capital_snapshots = relationship("CapitalSnapshot", back_populates="funding_phase")

class CapitalSnapshot(Base):
    __tablename__ = "capital_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    total_capital = Column(Float)
    funding_phase_id = Column(Integer, ForeignKey("funding_phases.id"))

    funding_phase = relationship("FundingPhase", back_populates="capital_snapshots")
