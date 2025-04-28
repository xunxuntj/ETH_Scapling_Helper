import gate_api
import os
from dotenv import load_dotenv

load_dotenv()

class GateioClient:
    def __init__(self):
        self.api_key = os.getenv("GATEIO_API_KEY")
        self.secret_key = os.getenv("GATEIO_SECRET_KEY")
        self.order_api_key = os.getenv("GATEIO_ORDER_API_KEY")
        self.order_secret_key = os.getenv("GATEIO_ORDER_SECRET_KEY")

        self.configuration = gate_api.Configuration(
            key=self.api_key,
            secret=self.secret_key
        )
        self.api_client = gate_api.ApiClient(self.configuration)
        self.spot_api = gate_api.SpotApi(self.api_client)
        self.futures_api = gate_api.FuturesApi(self.api_client) # Assuming perpetual futures

    def get_klines(self, currency_pair: str, interval: str = "1m", limit: int = 100):
        """Fetches k-line data for a given currency pair and interval."""
        try:
            # Gate.io futures klines endpoint might be different, need to confirm with SDK docs
            # This is a placeholder using spot klines for now
            klines = self.spot_api.list_candlesticks(currency_pair, interval=interval, limit=limit)
            # TODO: Adapt for futures klines if necessary
            return klines
        except Exception as e:
            print(f"Error fetching klines: {e}")
            return None

    def get_account_balance(self, currency: str = "USDT"):
        """Fetches the account balance for a given currency."""
        try:
            # Gate.io futures account balance endpoint might be different
            # This is a placeholder using spot account for now
            accounts = self.spot_api.list_spot_accounts()
            for account in accounts:
                if account.currency == currency:
                    return float(account.available) # Assuming 'available' is the relevant balance
            # TODO: Adapt for futures account balance if necessary
            return None
        except Exception as e:
            print(f"Error fetching account balance: {e}")
            return None

    # TODO: Add methods for placing and canceling orders using order API keys
