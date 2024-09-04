from dash import dcc, html
from dash_iconify import DashIconify

from components.helper import dcc_loading
from layouts.main import content_header, style_dropdown, style_hidden, style_input

dropdown_theme = dcc.Dropdown(
    id="dropdown-chat-template",
    placeholder="Toggle theme for plots",
    clearable=False,
    style=style_dropdown,
    value="presentation",
    options=[
        "ggplot2",
        "seaborn",
        "simple_white",
        "plotly",
        "plotly_white",
        "presentation",
        "xgridoff",
        "ygridoff",
        "gridon",
        "none",
    ],
)


def chat_tab(app):
    return html.Div(
        [
            content_header(
                "Chat Analyzer",
                [
                    DashIconify(icon="openmoji:chats", height=40),
                    "View your messaging pattern",
                ],
            ),
            html.Div(
                [
                    html.P(
                        "Users can find out their telegram messaging statistics and generate word cloud based on their "
                        "Telegram chat data. Confidentiality is guaranteed as long as this webpage is loaded on HTTPS"
                    ),
                    html.Br(),
                    html.P(
                        "Step 1: Export chat data in JSON format using Telegram Desktop"
                    ),
                    html.P(
                        "Step 2: Upload exported telegram file (.json format), a message will appear to indicate if "
                        "file is uploaded successfully"
                    ),
                    html.P('Step 3: Click "OK" button to generate results!'),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Upload(
                                [
                                    html.Img(src=app.get_asset_url("upload.svg")),
                                    html.Span(
                                        "Drag and drop file here, or click to upload"
                                    ),
                                ],
                                id="upload-chat",
                                multiple=False,
                                className="div-with-image div-with-image-left small-image image-dark-bg",
                            ),
                            html.P(
                                [html.P(id="text-chat-confirm")], id="text-chat-loading"
                            ),
                            html.Button("OK", id="button-chat-ok"),
                            dcc_loading(
                                [html.P(id="chat-result-error", className="color-red")],
                                dark_bg=True,
                            ),
                            dcc.Store(
                                id="intermediate-chat-result", storage_type="memory"
                            ),
                        ],
                        className="custom-div-small-medium custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
            # Result
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.P("Toggle theme for plots:"),
                                            html.P([dropdown_theme], style=style_input),
                                        ],
                                        className="custom-div-flex",
                                    ),
                                    html.Br(),
                                    html.P(
                                        id="chat-result",
                                    ),
                                ],
                                className="custom-div-small custom-div-left custom-div-white",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Img(src=app.get_asset_url("info.svg")),
                                            html.Span(
                                                "Mouseover for information, highlight to zoom, double click to reset "
                                                "view"
                                            ),
                                            dcc.Graph(id="graph-chat-result-day"),
                                        ],
                                        className="div-with-image div-with-image-left small-image",
                                    ),
                                ],
                                className="custom-div-large custom-div-center",
                            ),
                        ],
                        className="custom-container custom-div-center",
                    ),
                    html.Div(
                        [
                            html.Div(
                                id="chat-result-wordcloud", className="custom-div-full"
                            ),
                            dcc.Graph(id="graph-chat-result-hour"),
                        ],
                        className="custom-div-center custom-div-white",
                        style={"display": "block"},
                    ),
                ],
                id="div-chat-result",
                className="custom-container custom-div-space-below",
                style=style_hidden,
            ),
        ]
    )
