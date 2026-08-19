from dash import dcc, html

from common.layouts.main import content_header
from main.components import Wordle
from main.model.wordle import N_GUESSES, N_LETTERS


def create_grid():
    grid = []
    for r in range(N_GUESSES):
        row = []
        for c in range(N_LETTERS):
            row.append(html.Div("", id=f"tile-{r}-{c}", className="wordle-tile"))
        grid.append(html.Div(row, className="wordle-row"))
    return html.Div(grid, className="wordle-grid")


def wordle_tab(app):
    wordle_game = Wordle(n_letters=N_LETTERS)
    return html.Div(
        [
            content_header(["Wordle"], ""),
            html.Div(
                [
                    html.Div(
                        [
                            create_grid(),
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
