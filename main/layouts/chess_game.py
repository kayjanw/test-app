from dash import dcc, html

from common.components.helper import encode_dict
from common.layouts.main import content_header
from main.components.chess_game import ChessGame
from main.layouts.main import style_hidden


def chess_tab(app):
    chess_game = ChessGame()

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
                                html.Span(
                                    html.Img(src=app.get_asset_url("undo.svg")),
                                    title="Undo",
                                ),
                                id="chess-undo",
                                className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("new.svg")),
                                    title="New game",
                                ),
                                id="chess-new-game",
                                className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
                            html.Form(
                                [
                                    dcc.Input(
                                        value=encode_dict(
                                            chess_game.convert_to_save_format()
                                        ),
                                        name="result",
                                        type="text",
                                        style=style_hidden,
                                        id="input-chess",
                                    ),
                                    html.Button(
                                        html.Span(
                                            html.Img(
                                                src=app.get_asset_url("download.svg")
                                            ),
                                            title="Save game",
                                        ),
                                        type="submit",
                                        id="button-chess-download-ok",
                                        className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                                    ),
                                ],
                                method="POST",
                                action="/download_chess/",
                                style={"display": "inline-block"},
                            ),
                            html.A(
                                [
                                    dcc.Upload(
                                        [
                                            html.Span(
                                                html.Img(
                                                    src=app.get_asset_url("upload.svg")
                                                ),
                                                title="Upload game",
                                            ),
                                        ],
                                        id="uploadchess-button",
                                        multiple=False,
                                    )
                                ],
                                className="custom-div-center div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
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
                data=chess_game.state,
            ),
        ]
    )
