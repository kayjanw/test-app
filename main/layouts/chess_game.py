from dash import dcc, html

from common.layouts.main import content_header
from main.components.chess_game import ChessGame


def chess_tab(app):
    return html.Div(
        [
            content_header("Chess", "Not checkers"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(id="chess-container"),
                        ],
                        style={
                            "flex": "1",
                            "display": "flex",
                            "justifyContent": "center",
                        },
                    ),
                    html.Div(
                        [
                            html.Div(
                                id="chess-status",
                                style={
                                    "textAlign": "center",
                                    "fontSize": "20px",
                                    "marginBottom": "16px",
                                },
                            ),
                            html.Div(
                                id="chess-history",
                                style={
                                    "maxHeight": "500px",
                                    "overflowY": "auto",
                                    "border": "1px solid #ddd",
                                    "padding": "12px",
                                },
                            ),
                            html.Br(),
                            html.Button(
                                "New Game",
                                id="chess-new-game",
                                n_clicks=0,
                            ),
                            # TODO: introduce save game, load game, undo
                        ],
                        style={
                            "width": "250px",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "32px",
                    "maxWidth": "1100px",
                    "margin": "auto",
                    "alignItems": "flex-start",
                },
            ),
            dcc.Store(
                id="chess-state",
                storage_type="memory",
                data=ChessGame().get_initial_state(),
            ),
        ]
    )
