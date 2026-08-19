from dash import dcc, html

from common.layouts.main import content_header
from main.components.wordle import Wordle, create_grid


def wordle_tab(app):
    wordle_game = Wordle()
    return html.Div(
        [
            content_header(["Wordle"], ""),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(create_grid(), id="wordle-grid"),
                            html.Div(
                                [
                                    dcc.Input(
                                        id="wordle-guess",
                                        type="text",
                                        maxLength=5,
                                        placeholder="Enter 5 letters",
                                    ),
                                    html.Button("Submit", id="button-wordle"),
                                    html.Div(id="wordle-output"),
                                    dcc.Input(
                                        id="nletters-wordle",
                                        type="number",
                                        value=5,
                                        min=5,
                                        max=6,
                                        style={"display": "none"},
                                    ),
                                ],
                                className="custom-div-space-above",
                            ),
                        ],
                        id="div-wordle",
                        className="custom-div-center",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
                style={
                    "text-align": "center",
                    "margin-bottom": 0,
                },
            ),
            dcc.Store(
                id="wordle-state", storage_type="memory", data=wordle_game.to_store()
            ),
        ]
    )
