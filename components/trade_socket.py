import datetime
import dateutil.parser
import json
import pandas as pd
import requests
import websocket

from components.trade import Trade


class TradeSocket:
    """The TradeSocket object contains functions used for Trade tab"""

    def __init__(self, ticker="BTC-USD", granularity="15 min"):
        """Initialize class attributes

        Args:
            ticker (str): ticker to display
            granularity (str): granularity of candlestick charts
        """
        # Parameters
        self.ticker = ticker
        self.granularity = granularity
        self.socket = "wss://ws-feed.pro.coinbase.com"
        self.api_url = "https://api.pro.coinbase.com"
        self.TIMEFRAME_DICT = {
            "1 min": (60, "1T"),
            "5 min": (300, "5T"),
            "15 min": (900, "15T"),
            "30 min": (1800, "30T"),
            "1 hour": (3600, "1H"),
            "4 hours": (14400, "4H"),
            "1 day": (86400, "1D"),
        }
        # Variables
        self.tick_df = pd.DataFrame()

    @staticmethod
    def get_symbol_names():
        """Get symbol names

        Returns:
            (list)
        """
        symbol_names = [
            "BTC-USD",
            "ETH-BTC",
            "ETH-EUR",
            "ETH-USD",
        ]
        return symbol_names

    def get_historical_data(self):
        """Get historical data of stock ticker

        Returns:
            (pd.DataFrame)
        """
        _request = (
            self.api_url
            + f"/products/{self.ticker}/candles?granularity={self.TIMEFRAME_DICT[self.granularity][0]}"
        )
        resp = requests.get(_request)
        assert (
            resp.status_code == 200
        ), f"Request has error of status code {resp.status_code}"
        df_historical = pd.DataFrame(
            resp.json(), columns=["Epoch", "Low", "High", "Open", "Close", "Volume"]
        )
        df_historical = df_historical.sort_values("Epoch")
        df_historical["Datetime"] = pd.to_datetime(
            df_historical["Epoch"], unit="s"
        ) + datetime.timedelta(hours=8)
        return df_historical[["Datetime", "Open", "High", "Low", "Close"]]

    def on_open(self, ws):
        """Websocket callback object, called when opening websocket

        Args:
            ws (WebSocketApp): websocket object
        """
        print("Connection opened")
        subscribe_msg = {
            "type": "subscribe",
            "channels": [{"name": "matches", "product_ids": [self.ticker]}],
        }
        ws.send(json.dumps(subscribe_msg))

    def on_message(self, ws, message):
        """Websocket callback object, called when received data

        Args:
            ws (WebSocketApp): websocket class object
            message (str): utf-8 data received from server

        Returns:
            (pd.DataFrame)
        """
        current_tick = json.loads(message)
        # Create DataFrame
        current_time_ds = dateutil.parser.parse(
            current_tick["time"]
        ) + datetime.timedelta(hours=8)
        current_time_string = current_time_ds.strftime("%Y-%m-%d %H:%M:%S")
        df_current_tick = pd.DataFrame(
            columns=["Datetime", "market", "price"],
            data=[
                [
                    current_time_string,
                    current_tick["product_id"],
                    current_tick["price"],
                ]
            ],
        )
        df_current_tick["Datetime"] = df_current_tick["Datetime"].astype(
            "datetime64[ns]"
        )
        df_current_tick["price"] = df_current_tick["price"].astype("float64")
        if len(self.tick_df):
            ws.close()
            self.tick_df = self.tick_df.concat(df_current_tick)
        else:
            self.tick_df = df_current_tick.copy()
        self.tick_df["Datetime"] = self.tick_df["Datetime"].dt.floor(
            freq=self.TIMEFRAME_DICT[self.granularity][1]
        )

    def run_socket(self):
        ws = websocket.WebSocketApp(
            self.socket,
            on_open=lambda ws: self.on_open(ws),
            on_message=lambda ws, msg: self.on_message(ws, msg),
        )
        ws.run_forever()

    def get_rates_data(self):
        """Compute rate data (time, open, high, low, close)

        Returns:
            (pandas DataFrame)
        """
        df_historical = self.get_historical_data()
        self.run_socket()
        if self.tick_df["Datetime"][0] in set(df_historical["Datetime"]):
            df_new_candle = df_historical[
                (df_historical["Datetime"] == self.tick_df["Datetime"].values[0])
            ]
            # Replace close
            df_historical.at[df_new_candle.index.values[0], "Close"] = self.tick_df[
                "price"
            ].values[0]
            # Replace high
            if self.tick_df["price"].values[0] > df_new_candle["High"].values[0]:
                df_historical.at[df_new_candle.index.values[0], "High"] = self.tick_df[
                    "price"
                ].values[0]
            # Replace low
            if float(self.tick_df["price"].values[0]) < float(
                df_new_candle["Low"].values[0]
            ):
                df_historical.at[df_new_candle.index.values[0], "Low"] = self.tick_df[
                    "price"
                ].values[0]
        else:
            df_new_candle = pd.DataFrame(
                columns=df_historical.columns,
                data=[
                    [
                        self.tick_df["Datetime"].values[0],
                        self.tick_df["price"].values[0],
                        self.tick_df["price"].values[0],
                        self.tick_df["price"].values[0],
                        self.tick_df["price"].values[0],
                    ]
                ],
            )
            df_historical = df_historical.concat(df_new_candle)
        return df_historical

    def get_candlestick_chart(self, indicators_ind, forecast_methods):
        """Get figure for plot

        Adds plotly.graph_objects charts for candlestick plot, visualizing trade movement

        Args:
            indicators_ind (list): list of indicators to plot
            forecast_methods (list): list of forecasting methods

        Returns:
            (dict): graphical result of trade
        """
        rates_df = self.get_rates_data()
        return Trade().get_candlestick_chart(
            symbol=self.ticker,
            n_points=len(rates_df),
            rates_df=rates_df,
            indicators_ind=indicators_ind,
            forecast_methods=forecast_methods,
        )
