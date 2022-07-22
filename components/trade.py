try:
    import MetaTrader5 as mt5
    USE_MT5 = True
except ImportError:
    USE_MT5 = False

try:
    import yfinance as yf
except ImportError:
    pass

import datetime
import pandas as pd
import plotly.graph_objects as go

from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots


GRANULARITY = 4


def sma(data, window):
    """
    Calculates Simple Moving Average (SMA)

    SMA is a lagging indicator that smooths out price action and highlights direction of trend

    Args:
        data (pandas Series): input pandas Series
        window (int): number of historical periods to calculate SMA

    Returns:
        (pandas Series)
    """
    _sma = data.rolling(window).mean()
    return round(_sma, GRANULARITY)


def bol(data_close, data_low, data_high, periods=20, num_std=2):
    """
    Calculates Bollinger Bands (BOL)

    BOL measures volatility of market and overbought and oversold conditions and made up of SMA and upper and lower
    band. The closer the price is to the upper band, the closer to overbought conditions, vice versa. If bands are
    very close (low volatility), this can be indication of potential future volatility, vice versa

    Args:
        data_close (pandas Series): input pandas Series for closing price
        data_low (pandas Series): input pandas Series for low price
        data_high (pandas Series): input pandas Series for high price
        periods (int): number of periods to smooth, defaults to 20
        num_std (int): number of standard deviation, defaults to 2

    Returns:
        (pandas Series)
    """
    typical_price = (data_close + data_low + data_high) / 3
    typical_price_std = typical_price.rolling(periods).std(ddof=0)
    typical_price_ma = typical_price.rolling(periods).mean()
    bol_upper = typical_price_ma + num_std * typical_price_std
    bol_lower = typical_price_ma - num_std * typical_price_std
    return round(bol_lower, GRANULARITY), round(bol_upper, GRANULARITY)


def rsi(data, periods=14, ema=True):
    """
    Calculates Relative Strength Index (RSI)

    RSI is a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or
    oversold conditions in the price of an asset. RSI measures price change in relation to recent price highs and lows

    Args:
        data (pandas Series): input pandas Series
        periods (int): number of periods to calculate RSI, defaults to 14
        ema (bool): indicator to use exponential moving average, defaults to True

    Returns:
        (pandas Series)
    """
    close_delta = data.diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema:
        # Use exponential moving average
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=periods).mean()
        ma_down = down.rolling(window=periods).mean()

    _rsi = ma_up / ma_down
    _rsi = 100 - (100 / (1 + _rsi))
    return round(_rsi, GRANULARITY)


def macd(data, fast=12, slow=26, signal=9):
    """
    Calculates Moving Average Convergence Divergence (MACD)

    MACD is a momentum indicator that signal shifts in market momentum and signal potential breakouts.
    MACD measures the relationship between fast and slow EMA (typically 12-day and 26-day respectively).
    Signal/Trigger measures EMA of period shorter than shortest period used in calculating MACD (typically 9-day).
    Difference between MACD and Trigger represent current selling pressures, positive represent bullish trend
    whereas negative indicate bearish one

    Args:
        data (pandas Series): input pandas Series
        fast (int): number of period to calculate fast EMA, defaults to 12
        slow (int): number of periods to calculate slow EMA, defaults to 26
        signal (int): number of periods to calculate signal, defaults to 9

    Returns:
        (pandas Series, pandas Series, pandas Series): MACD, MACD SIGNAL, MACD - Signal
    """
    # Get the fast (12-day) EMA of the closing price
    k = data.ewm(span=fast, adjust=False, min_periods=12).mean()

    # Get the slow (26-day) EMA of the closing price
    d = data.ewm(span=slow, adjust=False, min_periods=26).mean()

    # Subtract the slow EMA from the fast EMA to get the MACD
    _macd = k - d

    # Get the signal (9-Day) EMA of the MACD for the Trigger line
    _macd_s = _macd.ewm(span=signal, adjust=False, min_periods=9).mean()

    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    _macd_h = _macd - _macd_s
    return round(_macd, GRANULARITY), round(_macd_s, GRANULARITY), round(_macd_h, GRANULARITY)


def forecast_ewm(data, alpha=0.8):
    """
    Forecasting with Exponential Weighted Moving Average

    Args:
        data (pandas Series): input pandas Series
        alpha (float): weight given to preceding EMA value

    Returns:
        float
    """
    pred = data[:-1].ewm(alpha=alpha).mean().values[-1]
    return round(pred, GRANULARITY)


class Trade:
    """The Trade object contains functions used for Trade tab"""
    def __init__(self, use_mt5=USE_MT5):
        """Initialize class attributes

        Args:
            use_mt5 (bool): whether to use MetaTrader5, defaults to False
        """
        self.use_mt5 = use_mt5
        self.col_names = []
        self.TIMEFRAME_DICT = {
            "1 min": "1m",
            "5 min": "5m",
            "15 min": "15m",
            "30 min": "30m",
            "1 hour": "60m",
            "1 day": "1d",
            "1 week": "1wk",
            "1 month": "1mo",
        }
        if use_mt5:
            # Connect to MetaTrader5 Platform
            assert mt5.initialize("data/MetaTrader5/terminal64.exe", portable=True), "Cannot initialize MetaTrader5"

            self.TIMEFRAME_DICT = {
                "1 min": mt5.TIMEFRAME_M1,
                "5 min": mt5.TIMEFRAME_M5,
                "15 min": mt5.TIMEFRAME_M15,
                "30 min": mt5.TIMEFRAME_M30,
                "1 hour": mt5.TIMEFRAME_H1,
                "4 hours": mt5.TIMEFRAME_H4,
                "1 day": mt5.TIMEFRAME_D1,
                "1 week": mt5.TIMEFRAME_W1,
                "1 month": mt5.TIMEFRAME_MN1,
            }

    def get_symbol_names(self):
        """Get symbol names

        Returns:
            list
        """
        symbol_names = []
        if self.use_mt5:
            symbols = mt5.symbols_get()
            symbol_names = [symbol._asdict()["name"] for symbol in symbols]
        return symbol_names

    def get_rates_data(self, symbol, timeframe, n_points):
        """Compute rate data (time, open, high, low, close, tick volume, spread)

        Args:
            symbol (str): symbol to plot for
            timeframe (str): frequency of candlestick
            n_points (int): number of points on candlestick

        Returns:
            pandas DataFrame: result of rate data
        """
        frequency = self.TIMEFRAME_DICT[timeframe]

        if self.use_mt5:
            # n_points to be minimum of 100 to calculate technical indicators
            n_candles = max(n_points, 100)
            rates_arr = mt5.copy_rates_from_pos(symbol, frequency, 0, n_candles)

            # Time, Open, High, Low, Close, Tick volume, Spread, Real volume
            col_names = [col.replace("_", " ").capitalize() for col in rates_arr.dtype.fields.keys()]
            rates_df = pd.DataFrame(rates_arr)
            rates_df.columns = col_names
            rates_df[col_names[0]] = pd.to_datetime(rates_df[col_names[0]], unit="s")
        else:
            start_dt = (datetime.datetime.now() - relativedelta(years=1)).strptime("%Y-%m-%d")
            rates_df = yf.Ticker(symbol).history(start=start_dt, interval=frequency).reset_index(drop=True)
            # Datetime, Open, High, Low, Close, Volume, Dividend, Stock Splits
            col_names = rates_df.columns

        self.col_names = col_names
        return rates_df

    @staticmethod
    def get_candlestick_chart(symbol, n_points, rates_df, indicators_ind, forecast_methods):
        """Get figure for plot

        Adds plotly.graph_objects charts for candlestick plot, visualizing trade movement

        Args:
            symbol (str): symbol to plot for
            n_points (int): number of points on candlestick
            rates_df (pandas DataFrame): rate data (time, open, high, low, close, tick volume, spread)
            indicators_ind (list): list of indicators to plot
            forecast_methods (list): list of forecasting methods

        Returns:
            dict: graphical result of trade
        """
        assert len(rates_df.columns), "Rate data is not initialized"
        col_time, col_open, col_high, col_low, col_close = rates_df.columns[:5]

        # Candlestick
        data_top = []
        rates_df_points = rates_df.copy()[-n_points:]
        data_top.append(
            go.Candlestick(
                x=rates_df_points[col_time],
                open=rates_df_points[col_open],
                high=rates_df_points[col_high],
                low=rates_df_points[col_low],
                close=rates_df_points[col_close],
                name="Candlestick",
                text=["<br>".join([
                    f"{rates_df_points.columns[idx]}: {x[idx]}"
                    for idx in range(len(rates_df_points.columns))]) for x in rates_df_points.values],
                hoverinfo="text",
            )
        )

        # Forecast
        for ind in forecast_methods:
            if ind == "EMA(0.8)":
                ind_col = "Forecast EMA(0.8)"
                pred = forecast_ewm(rates_df[col_close], alpha=0.8)
                rates_df[ind_col] = [None] * (len(rates_df) - 1) + [pred]
                rates_df_points = rates_df.copy()[-n_points:]
                data_top.append(
                    go.Scatter(
                        x=rates_df_points[col_time],
                        y=rates_df_points[ind_col],
                        name=ind_col,
                        mode="markers",
                        marker={
                            "color": "black"
                        },
                        hovertemplate="%{y}",
                    )
                )

        # Compute technical indicator
        ind_df = rates_df.copy()[[col_time]]
        data_middle = []
        data_bottom = []
        for ind in indicators_ind:
            if ind == "SMA10":
                ind_df[ind] = sma(rates_df[col_close], 10)
                ind_df_points = ind_df[-n_points:]
                data_top.append(
                    go.Scatter(
                        x=ind_df_points[col_time],
                        y=ind_df_points[ind],
                        name=ind,
                        mode="lines",
                        hovertemplate="%{y}",
                    )
                )

            elif ind == "SMA50":
                ind_df[ind] = sma(rates_df[col_close], 50)
                ind_df_points = ind_df[-n_points:]
                data_top.append(
                    go.Scatter(
                        x=ind_df_points[col_time],
                        y=ind_df_points[ind],
                        name=ind,
                        mode="lines",
                        hovertemplate="%{y}",
                    )
                )

            elif ind == "BOLL(Close,20)":
                ind_df["BOLU"], ind_df["BOLD"] = bol(
                    rates_df[col_close], rates_df[col_low], rates_df[col_high]
                )
                ind_df_points = ind_df[-n_points:]
                data_top.append(
                    go.Scatter(
                        x=ind_df_points[col_time],
                        y=ind_df_points["BOLD"],
                        name="BOLL(Close,20)",
                        line=dict(color="rgba(255, 165, 0, 0)"),
                        hovertemplate="%{y}",
                        showlegend=False,
                    )
                )
                data_top.append(
                    go.Scatter(
                        x=ind_df_points[col_time],
                        y=ind_df_points["BOLU"],
                        name="BOLL(Close,20)",
                        line=dict(color="rgba(255, 165, 0, 0)"),
                        hovertemplate="%{y}",
                        fill="tonexty",
                        fillcolor="rgba(255, 165, 0, 0.5)"
                    )
                )

            elif ind == "RSI(Close,14)":
                ind_df[ind] = rsi(rates_df[col_close])
                ind_df_points = ind_df[-n_points:]
                data_middle.append(
                    go.Scatter(
                        x=ind_df_points[col_time],
                        y=ind_df_points[ind],
                        name=ind,
                        mode="lines",
                    )
                )

            elif ind == "MACD":
                ind_df["MACD(12,26)"], ind_df["MACD SIGNAL(9)"], ind_df["MACD - Signal"] = macd(rates_df[col_close])
                ind_df_points = ind_df[-n_points:]
                data_bottom.append(
                    go.Scatter(
                        x=ind_df_points[col_time],
                        y=ind_df_points["MACD(12,26)"],
                        name="MACD(12,26)",
                        mode="lines",
                        line=dict(color="rgba(63, 195, 128, 1)"),
                    )
                )
                data_bottom.append(
                    go.Scatter(
                        x=ind_df_points[col_time],
                        y=ind_df_points["MACD SIGNAL(9)"],
                        name="MACD SIGNAL(9)",
                        mode="lines",
                        line=dict(color="rgba(255, 100, 91, 1)"),
                    )
                )
                data_bottom.append(
                    go.Bar(
                        x=ind_df_points[col_time],
                        y=ind_df_points["MACD - Signal"],
                        name="MACD - Signal",
                        marker=dict(
                            color=[
                                "rgba(63, 195, 128, 1)" if x > 0 else "rgba(255, 100, 91, 1)" for x in
                                ind_df_points["MACD - Signal"]]
                        ),
                    )
                )

        layout_visible_grid = {"gridwidth": 1, "gridcolor": "lightgrey"}
        layout_visible_false = {"rangeslider_visible": False}
        layout_visible_true = {"rangeslider_visible": True}
        layout = {
            "title": f"{symbol} Rates",
            "hovermode": "x",
            "legend": {"traceorder": "normal"},
            "plot_bgcolor": "white",
            "xaxis": layout_visible_grid,
            "yaxis": layout_visible_grid,
        }

        if len(data_middle) and len(data_bottom):
            fig = make_subplots(
                rows=3,
                shared_xaxes=True,
            )
            for data in data_top:
                fig.add_trace(data, row=1, col=1)
            for data in data_middle:
                fig.add_trace(data, row=2, col=1)
            for data in data_bottom:
                fig.add_trace(data, row=3, col=1)
            fig.update_layout(layout)
            fig.update_layout(
                {
                    "xaxis": layout_visible_false,
                    "yaxis": {"domain": [0.3, 1]},
                    "xaxis2": {**layout_visible_false, **layout_visible_grid},
                    "yaxis2": {**{"domain": [0.15, 0.3]}, **layout_visible_grid},
                    "xaxis3": {**layout_visible_true, **layout_visible_grid},
                    "yaxis3": {**{"domain": [0, 0.15]}, **layout_visible_grid},
                }
            )
        elif len(data_middle) or len(data_bottom):
            fig = make_subplots(
                rows=2,
                shared_xaxes=True,
            )
            for data in data_top:
                fig.add_trace(data, row=1, col=1)
            for data in data_middle:
                fig.add_trace(data, row=2, col=1)
            for data in data_bottom:
                fig.add_trace(data, row=2, col=1)
            fig.update_layout(layout)
            fig.update_layout(
                {
                    "xaxis": layout_visible_false,
                    "yaxis": {"domain": [0.3, 1]},
                    "xaxis2": {**layout_visible_true, **layout_visible_grid},
                    "yaxis2": {**{"domain": [0, 0.3]}, **layout_visible_grid},
                }
            )
        else:
            fig = dict(data=data_top, layout=layout)

        return fig
