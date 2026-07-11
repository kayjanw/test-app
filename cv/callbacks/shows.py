import dash_mantine_components as dmc
from dash import html
from dash.dependencies import Input, Output

from common.components.helper import print_callback
from cv.data.shows import shows_data
from cv.model.show import Show


def divide_cols(shows: list[Show], n_cols: int):
    shows_cols = [shows[i::n_cols] for i in range(n_cols)]
    return dmc.Group(
        [html.Div([show.div for show in shows_col]) for shows_col in shows_cols],
        align="flex-start",
        grow=True,
    )


def register_callbacks_shows(app, print_function):
    @app.callback(Output("shows-tab", "children"), Input("resize-trigger", "children"))
    @print_callback(print_function)
    def display_width(width):
        n_cols = 3
        if width <= 1100:
            n_cols = 1
        elif width <= 1400:
            n_cols = 2

        return [
            dmc.TabsList(
                [
                    dmc.TabsTab(
                        show[1],
                        value=show[1],
                    )
                    for show in shows_data
                ]
            ),
        ] + [
            dmc.TabsPanel(
                [
                    dmc.Card(
                        divide_cols(show[0], n_cols),
                        className="card-show",
                    ),
                ],
                value=show[1],
            )
            for show in shows_data
        ]
