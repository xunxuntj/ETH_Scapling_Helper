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
        # Use the correct futures API method
        try:
            klines = self.futures_api.list_futures_candlesticks(contract=currency_pair, interval=interval, limit=limit)
            return klines # Return the result directly
        except Exception as e:
            raise Exception(f"Error fetching klines: {e}") # Raise an exception


    def get_account_balance(self, currency: str = "USDT"):
        """Fetches the account balance for a given currency."""
        # Use the correct futures API method
        try:
            accounts = self.futures_api.list_futures_accounts()
            for account in accounts:
                if account.currency == currency:
                    return float(account.available)  # Assuming 'available' is the relevant balance
            raise Exception(f"Currency {currency} not found in futures accounts")
        except Exception as e:
            print(f"Error fetching account balance: {e}")
            return 0.0

    def get_open_positions(self, currency_pair: str):
        """Fetches open positions for a given currency pair."""
        try:
            # Assuming Gate.io futures API has a method to list positions
            # Need to confirm the exact method and parameters from SDK docs
            positions = self.futures_api.list_futures_positions(contract=currency_pair, currency_pair=currency_pair) # Placeholder method and parameter
        except Exception as e:
            print(f"Error fetching open positions: {e}")
            return None
        return positions

    def amend_order(self, contract: str, order_id: str, new_stop_loss: float = None, new_take_profit: float = None):
        """Amends an existing order to update stop loss and/or take profit."""
        order_configuration = gate_api.Configuration(
            key=self.order_api_key,
            secret=self.order_secret_key
        )
        order_api_client = gate_api.ApiClient(order_configuration)
        futures_api = gate_api.FuturesApi(order_api_client)
        
        update_params = {}
        if new_stop_loss is not None:
            update_params["text"] = f"stop_loss:{new_stop_loss}"
        if new_take_profit is not None:
            update_params["text"] = f"take_profit:{new_take_profit}"

        if len(update_params) == 0:
            return None
        
        try:
            # Assuming Gate.io spot API has an amend_order method
            amended_order = futures_api.update_futures_order(order_id=order_id, contract=contract, text=update_params["text"])
            print(f"Order amended: {amended_order}")
            return amended_order
        except Exception as e:
            print(f"Error amending order: {e}")
            return None
        
    def place_order(self, currency_pair: str, side: str, amount: float, price: float = None):
        """Places a futures order."""
        order_configuration = gate_api.Configuration(
            key=self.order_api_key,
            secret=self.order_secret_key
        )
        order_api_client = gate_api.ApiClient(order_configuration)
        futures_api = gate_api.FuturesApi(order_api_client)
        
        order = gate_api.FuturesOrder(
            contract=currency_pair,
            side=side,
            size=amount,
            price=price if price is not None else None,
            tif="ioc"
        )

        try:
            # Assuming Gate.io spot API has a create_order method
            # Need to confirm the exact method and parameters from SDK docs
            created_order = futures_api.create_futures_order(order) # Placeholder method
            print(f"Order placed: {created_order}")
            return created_order
        except Exception as e:
            print(f"Error placing order: {e}")
            return None

    def cancel_order(self, currency_pair: str, order_id: str):
        """Cancels a futures order."""
        order_configuration = gate_api.Configuration(
            key=self.order_api_key,
            secret=self.order_secret_key
        )
        order_api_client = gate_api.ApiClient(order_configuration)
        futures_api = gate_api.FuturesApi(order_api_client)
        try:
            canceled_order = futures_api.cancel_futures_order(order_id=order_id, contract=currency_pair)
            print(f"Order canceled: {canceled_order}")
            return canceled_order
        except Exception as e:
            print(f"Error canceling order: {e}")
            return None
