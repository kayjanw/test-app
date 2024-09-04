from typing import List

from dash.dependencies import Input, Output, State

from components import TradeSocket
from components.helper import print_callback


def register_callbacks(app, print_function):
    @app.callback(
        [Output("trade-result", "children"), Output("graph-trade", "figure")],
        Input("interval-trade", "n_intervals"),
        [
            State("dropdown-trade-symbol", "value"),
            State("dropdown-trade-frequency", "value"),
            State("input-trade-candle", "value"),
            State("checkbox-trade-ind", "value"),
            State("radio-trade-forecast", "value"),
        ],
    )
    @print_callback(print_function)
    def update_trade_graph(
        trigger,
        symbol: str,
        frequency: str,
        n_candle: int,
        indicators_ind: List[str],
        forecast_methods: List[str],
    ):
        """Update trade candlestick chart

        Args:
            trigger: triggers callback
            symbol: symbol to plot for
            frequency: frequency of candlestick
            n_candle: number of points on candlestick
            indicators_ind: list of indicators to plot
            forecast_methods: list of forecasting methods

        Returns:
            (dict): graphical result of trade
        """
        error_message = ""
        fig = {}
        if symbol and frequency and n_candle:
            try:
                trade = TradeSocket()
                rates_data = trade.get_rates_data(symbol, frequency, n_candle)
                fig = trade.get_candlestick_chart(
                    symbol, n_candle, rates_data, indicators_ind, forecast_methods
                )
            except Exception as e:
                error_message = f"Error: {e}"
        return error_message, fig
