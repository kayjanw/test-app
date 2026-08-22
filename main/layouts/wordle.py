import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from main.components.wordle import Wordle, create_grid

replay_symbol = html.Span(
    DashIconify(icon="material-symbols:replay", width=20),
    title="Replay",
)
switch_symbol = html.Span(
    DashIconify(icon="tabler:switch-3", width=20),
    title="Switch difficulty",
)


def modal_help():
    return [
        html.P(
            "How to Play (1 player)",
            className="p-short p-bold neucha-font",
        ),
        html.P(
            [
                "Guess the ",
                html.Span("WORDLE", className="p-short p-bold"),
                " in six tries. Each guess must be a valid five-letter "
                "word. Hit enter or press the button to submit your guess. After each "
                "guess, the colour of the tiles will change to show how close your guess was "
                "to the word.",
                html.Br(),
                html.Br(),
                "Select ",
                replay_symbol,
                " to restart game or ",
                switch_symbol,
                " to toggle between a five-letter or six-letter word.",
            ],
        ),
        html.Br(),
        html.P(
            "Tile Colour Meaning",
            style={"margin-top": "20px"},
            className="p-short p-bold neucha-font",
        ),
        html.P(
            [
                "Green: The letter is in the word and in the correct position",
                html.Br(),
                "Yellow: The letter is in the word but in the wrong position",
                html.Br(),
                "Gray: The letter is not in the hidden word",
            ],
        ),
        html.Br(),
        html.P(
            html.P("Have fun!", className="rainbow"),
            style={"margin-top": "20px"},
            className="custom-div-center p-short p-bold",
        ),
        html.Br(),
    ]


def wordle_tab(app):
    wordle_game = Wordle()
    return html.Div(
        [
            content_header(
                [
                    "Wordle",
                    html.Button(
                        html.Span(
                            html.Img(src=app.get_asset_url("help.png")),
                            title="How to play",
                        ),
                        id={"type": "button-modal-wordle", "index": "modal-help"},
                        className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                    ),
                ],
                "",
            ),
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
                                        replay_symbol, id="button-wordle-icon-redo"
                                    ),
                                    html.Button(
                                        switch_symbol, id="button-wordle-icon-switch"
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
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Instructions")),
                    dbc.ModalBody(
                        modal_help(),
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id={
                                "type": "button-close-modal-wordle",
                                "index": "modal-help",
                            },
                        )
                    ),
                ],
                id={"type": "modal-wordle", "index": "modal-help"},
                is_open=False,
                centered=True,
                size="lg",
            ),
        ]
    )
