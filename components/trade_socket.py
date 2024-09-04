import datetime
import json
from typing import Any, Dict, List, Optional

import dateutil.parser
import pandas as pd
import requests
import websocket

from components.trade import Trade


class TradeSocket:
    """The TradeSocket object contains functions used for Trade tab"""

    def __init__(self):
        """Initialize class attributes"""
        # Parameters
        self.socket = "wss://ws-feed.pro.coinbase.com"
        self.api_url = "https://api.pro.coinbase.com"
        self.TIMEFRAME_DICT = {
            "1 min": (60, "1T"),
            "5 min": (300, "5T"),
            "15 min": (900, "15T"),
            "1 hour": (3600, "1H"),
            "1 day": (86400, "1D"),
        }
        self.date_col = "Datetime"

        # Variables
        self.df_tick = pd.DataFrame()

    @staticmethod
    def get_symbol_names() -> List[str]:
        """Get symbol names"""
        symbol_names = [
            "BTC-USD",
            # "ETH-BTC",
            # "ETH-EUR",
            "ETH-USD",
        ]
        return symbol_names

    def get_historical_data(
        self, ticker: str, granularity: str, end: Optional[str] = None
    ) -> pd.DataFrame:
        """Get historical data of stock symbol

        Args:
            ticker: symbol to display
            granularity: granularity of candlestick chart
            end: end datetime of historical data
        """
        _request = (
            self.api_url
            + f"/products/{ticker}/candles?end={end}&granularity={self.TIMEFRAME_DICT[granularity][0]}"
        )
        resp = requests.get(_request)
        assert (
            resp.status_code == 200
        ), f"Request has error of status code {resp.status_code}"
        df_historical = pd.DataFrame(
            resp.json(), columns=["Epoch", "Low", "High", "Open", "Close", "Volume"]
        )
        df_historical = df_historical.sort_values("Epoch")
        df_historical[self.date_col] = pd.to_datetime(df_historical["Epoch"], unit="s")
        return df_historical[[self.date_col, "Open", "High", "Low", "Close"]]

    def on_open(self, ws, symbol: str):
        """Websocket callback object, called when opening websocket

        Args:
            ws (WebSocketApp): websocket object
            symbol: symbol to display
        """
        subscribe_msg = {
            "type": "subscribe",
            "channels": [{"name": "matches", "product_ids": [symbol]}],
        }
        ws.send(json.dumps(subscribe_msg))

    def on_message(self, ws, message: str, granularity: str):
        """Websocket callback object, called when received data

        Args:
            ws (WebSocketApp): websocket class object
            message: utf-8 data received from server
            granularity: granularity of candlestick chart

        Returns:
            (pd.DataFrame)
        """
        current_tick = json.loads(message)

        # Create DataFrame
        tick_time_ds = dateutil.parser.parse(current_tick["time"])
        tick_time_string = tick_time_ds.strftime("%Y-%m-%d %H:%M:%S")
        df_tick = pd.DataFrame(
            columns=["Datetime", "market", "price"],
            data=[
                [
                    tick_time_string,
                    current_tick["product_id"],
                    current_tick["price"],
                ]
            ],
        )
        df_tick[self.date_col] = df_tick["Datetime"].astype("datetime64[ns]")
        df_tick["price"] = df_tick["price"].astype("float64")

        # Get latest tick
        self.df_tick = df_tick.copy()
        self.df_tick[self.date_col] = self.df_tick[self.date_col].dt.floor(
            freq=self.TIMEFRAME_DICT[granularity][1]
        )
        ws.close()

    def run_socket(self, ticker: str, granularity: str):
        """Connect to web socket

        Args:
            ticker: symbol to display
            granularity: granularity of candlestick chart
        """
        ws = websocket.WebSocketApp(
            self.socket,
            on_open=lambda ws: self.on_open(ws, ticker),
            on_message=lambda ws, msg: self.on_message(ws, msg, granularity),
        )
        ws.run_forever()

    def get_rates_data(
        self, symbol: str, granularity: str, n_points: int
    ) -> pd.DataFrame:
        """Compute rate data (time, open, high, low, close)

        Args:
            symbol: symbol to display
            granularity: granularity of candlestick chart
            n_points: number of points on candlestick
        """
        historical_only = False

        if historical_only:
            # Get data
            end = datetime.datetime.now().isoformat()
            df_historical = self.get_historical_data(symbol, granularity, end=end)
        else:
            # Get data
            self.run_socket(symbol, granularity)
            end = self.df_tick[self.date_col].max().isoformat()
            df_historical = self.get_historical_data(symbol, granularity, end=end)

            if self.df_tick[self.date_col][0] in set(df_historical[self.date_col]):
                df_new = df_historical[
                    (
                        df_historical[self.date_col]
                        == self.df_tick[self.date_col].values[0]
                    )
                ]
                # Replace close
                df_historical.at[df_new.index.values[0], "Close"] = self.df_tick[
                    "price"
                ].values[0]
                # Replace high
                if self.df_tick["price"].values[0] > df_new["High"].values[0]:
                    df_historical.at[df_new.index.values[0], "High"] = self.df_tick[
                        "price"
                    ].values[0]
                # Replace low
                if float(self.df_tick["price"].values[0]) < float(
                    df_new["Low"].values[0]
                ):
                    df_historical.at[df_new.index.values[0], "Low"] = self.df_tick[
                        "price"
                    ].values[0]
            else:
                df_new = pd.DataFrame(
                    columns=df_historical.columns,
                    data=[
                        [
                            self.df_tick[self.date_col].values[0],
                            self.df_tick["price"].values[0],
                            self.df_tick["price"].values[0],
                            self.df_tick["price"].values[0],
                            self.df_tick["price"].values[0],
                        ]
                    ],
                )
                df_historical = pd.concat([df_historical, df_new])

        # Adjust to SG time
        df_historical[self.date_col] = df_historical[
            self.date_col
        ] + datetime.timedelta(hours=8)
        return df_historical

    @staticmethod
    def get_candlestick_chart(
        symbol: str,
        n_points: int,
        rates_df: pd.DataFrame,
        indicators_ind: List[str],
        forecast_methods: List[str],
    ) -> Dict[str, Any]:
        """Get figure for plot

        Adds plotly.graph_objects charts for candlestick plot, visualizing trade movement

        Args:
            symbol: symbol to plot for
            n_points: number of points on candlestick
            rates_df: rate data (time, open, high, low, close, tick volume, spread)
            indicators_ind: list of indicators to plot
            forecast_methods: list of forecasting methods

        Returns:
            graphical result of trade
        """
        return Trade().get_candlestick_chart(
            symbol=symbol,
            n_points=n_points,
            rates_df=rates_df,
            indicators_ind=indicators_ind,
            forecast_methods=forecast_methods,
        )
