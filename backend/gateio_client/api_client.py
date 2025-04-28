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

    def get_open_positions(self, currency_pair: str):
        """Fetches open positions for a given currency pair."""
        try:
            # Assuming Gate.io futures API has a method to list positions
            # Need to confirm the exact method and parameters from SDK docs
            positions = self.futures_api.list_futures_positions(contract=currency_pair) # Placeholder method and parameter
            return positions
        except Exception as e:
            print(f"Error fetching open positions: {e}")
            return None

    def place_order(self, currency_pair: str, side: str, amount: float, price: float = None):
        """Places a spot order."""
        # TODO: Adapt for futures orders if necessary
        # Need to use the order API keys for trading operations
        order_configuration = gate_api.Configuration(
            key=self.order_api_key,
            secret=self.order_secret_key
        )
        order_api_client = gate_api.ApiClient(order_configuration)
        spot_api = gate_api.SpotApi(order_api_client)

        order = gate_api.Order(
            currency_pair=currency_pair,
            side=side, # "buy" or "sell"
            amount=str(amount),
            price=str(price) if price is not None else "", # Pass empty string instead of None for price
            # TODO: Add other necessary order parameters (e.g., time_in_force, order_type)
            # TODO: Handle market orders where price is not provided
        )

        try:
            # Assuming Gate.io spot API has a create_order method
            # Need to confirm the exact method and parameters from SDK docs
            created_order = spot_api.create_order(order) # Placeholder method
            print(f"Order placed: {created_order}")
            return created_order
        except Exception as e:
            print(f"Error placing order: {e}")
            return None

    def cancel_order(self, currency_pair: str, order_id: str):
        """Cancels a spot order."""
        # TODO: Adapt for futures orders if necessary
        # Need to use the order API keys for trading operations
        order_configuration = gate_api.Configuration(
            key=self.order_api_key,
            secret=self.order_secret_key
        )
        order_api_client = gate_api.ApiClient(order_configuration)
        spot_api = gate_api.SpotApi(order_api_client)

        try:
            # Assuming Gate.io spot API has a cancel_order method
            # Need to confirm the exact method and parameters from SDK docs
            canceled_order = spot_api.cancel_order(order_id, currency_pair) # Placeholder method
            print(f"Order canceled: {canceled_order}")
            return canceled_order
        except Exception as e:
            print(f"Error canceling order: {e}")
            return None

    # TODO: Add methods for placing and canceling orders using order API keys
    # The above methods are placeholders and need to be adapted for futures trading and confirmed with SDK docs.
