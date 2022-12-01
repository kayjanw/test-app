from dash import dcc, html

from components import TradeSocket
from layouts.main import content_header, style_dropdown, style_input, style_p


def trade_tab():
    trade = TradeSocket()
    indicators = ["SMA10", "SMA50", "BOLL(Close,20)", "RSI(Close,14)", "MACD"]
    # indicators_desc = [
    #     "Simple Moving Average for past 10 values, Lagging Indicator, highlights direction of trend",
    #     "Simple Moving Average for past 50 values, Lagging Indicator, highlights direction of trend",
    #     "Bollinger Bands for 20 periods, Momentum Indicator, measures volatility of market",
    #     "Relative Strength Index, Momentum Indicator, measures magnitude of price changes",
    #     "Moving Average Convergence Divergence, Momentum Indicator, measures change between fast and slow EMA",
    # ]
    return html.Div(
        [
            content_header(
                "Live Trading", "Candlestick + Technical Indicators + Forecast"
            ),
            html.Div(
                [
                    html.P(
                        "Users can select their preferred trade and view a candlestick chart, with statistical indicators "
                        "and forecasts! Candlestick chart refreshes every 1 second."
                    ),
                    html.Br(),
                    html.P("Step 1: Select preferred symbol"),
                    html.P(
                        "Step 2: (Optional) Select preferred frequency of candlestick, number of candles to plot, "
                        "and whether to show technical indicators or forecasts"
                    ),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P("Symbol:", style=style_p),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-trade-symbol",
                                                options=[
                                                    {"label": s, "value": s}
                                                    for s in trade.get_symbol_names()
                                                ],
                                                value=trade.get_symbol_names()[0],
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style=style_input,
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Frequency:", style=style_p),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-trade-frequency",
                                                options=[
                                                    {"label": t, "value": t}
                                                    for t in trade.TIMEFRAME_DICT.keys()
                                                ],
                                                value=list(trade.TIMEFRAME_DICT.keys())[
                                                    0
                                                ],
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style=style_input,
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Number of Candles:", style=style_p),
                                    dcc.Input(
                                        id="input-trade-candle",
                                        type="number",
                                        value=50,
                                        min=1,
                                        max=300,
                                        style=style_input,
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Technical Indicators:", style=style_p),
                                    dcc.Checklist(
                                        id="checkbox-trade-ind",
                                        options=[
                                            {"label": ind, "value": ind}
                                            for idx, ind in enumerate(indicators)
                                        ],
                                        value=indicators[:2],
                                    ),
                                    # ] + [
                                    #     dbc.Tooltip(
                                    #         indicators_desc[idx],
                                    #         target=indicators[idx],
                                    #         placement="right",
                                    #         className="tooltip"
                                    #     )
                                    #     for idx in range(len(indicators))
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Forecast:", style=style_p),
                                    dcc.Checklist(
                                        id="radio-trade-forecast",
                                        options=[
                                            {
                                                "label": "Forecast (EWM(0.8))",
                                                "value": "EMA(0.8)",
                                            }
                                        ],
                                        value=[],
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            html.P(id="trade-result"),
                        ],
                        className="custom-div-smaller custom-div-left custom-div-dark",
                    ),
                    html.Div(
                        [
                            dcc.Interval(id="interval-trade", interval=2000),
                            dcc.Graph(id="graph-trade", style={"height": "70vh"}),
                        ],
                        className="custom-div-large custom-div-center",
                    ),
                ],
                className="custom-container custom-div-space-above",
            ),
        ]
    )
