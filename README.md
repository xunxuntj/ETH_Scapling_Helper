# ETH Scalping Assistant

## 📈 Project Overview

This project is a professional ETH perpetual futures scalping assistant designed to improve trading win rates and profitability through systematic scoring signals, stable trend identification, and program-assisted dynamic take profit and stop loss.

## 🛠 Trading Strategy

The trading strategy is structured as follows:

1.  **Trend Confirmation:**
    *   Vegas Tunnel (EMA85 / EMA144 / EMA169)
    *   MACD Golden Cross/Dead Cross confirmation
    *   EMA Double Cross confirmation
    *   RSI divergence as an auxiliary indicator

2.  **Entry Logic:**
    *   Candlestick patterns (engulfing patterns, hammer lines, etc.)
    *   Fibonacci support/resistance level confirmation
    *   Adherence to the 4x trend principle (small cycle conforms to large cycle direction)

3.  **Scoring System:**
    *   Multiple indicators are scored and standardized to a range of 0-10.
    *   A clear opening signal is given only when the score is above 7.
    *   Considers both trend strength and short-term volatility.

4.  **Take Profit and Stop Loss Rules:**
    *   Initial take profit is fixed (e.g., +10U), and stop loss is fixed (e.g., -10U).
    *   Dynamic take profit range is calculated using ATR.
    *   After the profit exceeds a certain threshold, the take profit and stop loss are automatically adjusted upwards.
    *   Losing trades are manually managed or stopped out.

5.  **Position Holding Time and Rhythm:**
    *   The target holding time for a single trade is 2-4 hours.
    *   5-8 trades per day are recommended.
    *   Take profit and stop loss are set after opening a position, eliminating the need for constant monitoring.

6.  **Capital Management Phase Division:**
    *   The initial capital is 2000USDT, and the single opening amount is dynamically adjusted as the phase rolls over.
    *   After a profit, the single opening capital can be adjusted or part of the profit can be withdrawn to protect the principal.

7.  **Notifications and Logs:**
    *   Telegram notifications are pushed only when there are \[Open Position Signals] and \[Close Position Signals].
    *   All scoring and indicator calculation results are recorded in the database for transaction review and system optimization.

## 💻 Technology Stack

*   **Backend API:** FastAPI (Python)
*   **Frontend Interface:** Next.js + Tailwind CSS
*   **Data Storage:** SQLite simple database (can be upgraded later)
*   **Market and Position Data:** Called using GateIO official Python SDK
*   **Scheduled Task Management:** The backend refreshes signals and position information every minute
*   **Dynamic Take Profit and Stop Loss Module:** The program automatically adjusts the take profit and stop loss prices every minute according to the floating profit, or is manually managed by the user
*   **Telegram Integration:** Push signal reminders via Telegram Bot
*   **Log Management:** Each signal generation, position adjustment, and price change is recorded in the database
*   **Historical Data Management:** Store historical signals and transaction execution, which can be used for retrospective analysis and model optimization
*   **Deployment Platform:** Render Serverless (backend independent service + frontend independent deployment)
*   **Security Management:** .env environment variable management API KEY, front and back end separation

## 🗂 Project Directory Structure

```
ETH-Scalping-Assistant/
│
├── backend/
│   ├── main.py                   # FastAPI main entry
│   ├── signal_engine/             # Signal calculation module
│   │   ├── vegas_tunnel.py        # Vegas tunnel trend judgment
│   │   ├── macd_rsi_logic.py      # MACD and RSI judgment
│   │   ├── fib_support.py         # Fibonacci support resistance level
│   │   ├── atr_trailing.py        # ATR dynamic take profit and stop loss
│   │   ├── candle_patterns.py     # K-line pattern recognition
│   │   └── scoring_system.py      # Signal scoring system
│   │   └── __init__.py
│   ├── trading_assistant/         # Position dynamic management module
│   │   ├── trailing_manager.py    # Automatic take profit and stop loss rolling adjustment
│   │   └── telegram_notifier.py   # Telegram push module
│   ├── database/
│   │   ├── db.py                  # SQLite database connection
│   │   ├── models.py              # Data model
│   │   └── migrations/
│   ├── gateio_client/
│   │   ├── api_client.py          # Gate official API encapsulation
│   │   └── __init__.py
│   ├── config/
│   │   ├── settings.py            # Configuration read
│   │   └── constants.py           # Project constant definition
│   └── requirements.txt           # Back-end dependencies
│
├── frontend/
│   ├── pages/
│   │   ├── index.tsx              # Dashboard main page
│   │   └── api/                   # Front-end API interface
│   ├── components/                # General component
│   ├── styles/                    # Global style
│   ├── public/                    # Static resources
│   └── package.json               # Front-end dependencies
│
├── scripts/
│   ├── deploy_render.sh           # Quick deployment script
│   └── init_db.py                 # Initialize the database
│
├── .env.example                    # Environment variable example
├── README.md                       # Project description
└── LICENSE
```

## 🛎️ Additional Instructions

*   **Scoring System Reference**: The multi-empty signal scoring system of the initial version of Dashboard can be appropriately simplified (without pursuing extreme complexity, but requiring stability and clear logic).
*   **Cycle Control for Positions**: The goal is 2-4 hours to maintain reasonable fluctuation response space and avoid mistakes caused by extremely frequent transactions.
*   **Dynamic Take Profit and Stop Loss Control Switch**: Add a switch button to the front-end Dashboard to allow users to decide whether to automatically adjust by the program or only prompt for manual adjustment.
*   **Historical Data Retrospective**: Each signal must be stored (scoring details, trend indicators, opening and closing prices, etc.) to facilitate future retrospective evaluation of system effectiveness.
*   **API Call Frequency Optimization**: Avoid excessively frequent API brushing while ensuring timely strategy response.
*   **Exception Handling Mechanism**: Such as API exceptions and market data exceptions, fault tolerance and retry can be performed to ensure stable system operation.



The remaining TODOs in the project files are:

backend/main.py
Add other relevant signal details from indicators and patterns
Map other signal details to model fields
Integrate actual trade execution/closure logging when order management is implemented
Fetch actual capital from GateIO and log to database periodically
Call telegram_notifier.send_trade_notification() when trades are executed or closed

backend/gateio_client/api_client.py

Adapt for futures klines if necessary
Adapt for futures account balance if necessary
Construct the amend order parameters based on GateIO API requirements
Add other necessary order parameters (e.g., time_in_force, order_type)
Add methods for placing and canceling orders using order API keys

backend/signal_engine/scoring_system.py
Define a proper threshold for high ATR (e.g., relative to average price or historical ATR)

backend/signal_engine/fib_support.py
Implement a more sophisticated method to identify significant swing highs and lows

backend/signal_engine/atr_trailing.py
Refine trailing logic based on specific strategy rules (e.g., parabolic SAR, fixed percentage)