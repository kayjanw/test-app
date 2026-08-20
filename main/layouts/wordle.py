from dash import dcc, html
from dash_iconify import DashIconify

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
                            html.Div(
                                create_grid(),
                                id="wordle-grid",
                                className="justify-space-around",
                            ),
                            html.Div(
                                [
                                    dcc.Input(
                                        id="wordle-guess",
                                        type="text",
                                        maxLength=5,
                                        placeholder="Enter 5 letters",
                                    ),
                                    html.Button(
                                        "Submit",
                                        id="button-wordle-submit",
                                        className="button-outline-wordle",
                                    ),
                                    html.Button(
                                        html.Span(
                                            DashIconify(
                                                icon="material-symbols:replay", width=20
                                            ),
                                            title="Replay",
                                        ),
                                        id="button-wordle-icon-redo",
                                    ),
                                    html.Button(
                                        html.Span(
                                            DashIconify(
                                                icon="tabler:switch-3", width=20
                                            ),
                                            title="Switch difficulty",
                                        ),
                                        id="button-wordle-icon-switch",
                                    ),
                                    dcc.Input(
                                        id="nletters-wordle",
                                        type="number",
                                        value=5,
                                        min=5,
                                        max=6,
                                        style={"display": "none"},
                                    ),
                                ],
                                className="custom-div-flex-only custom-div-space-above justify-space-around",
                            ),
                            html.Div(id="wordle-output"),
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
