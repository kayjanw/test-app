import dash_mantine_components as dmc
from dash.dependencies import Input, Output

from common.components.helper import print_callback
from cv.data.shows import shows_data
from cv.layouts.shows import show_splash


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
                show_splash(show[0], n_cols=n_cols),
                value=show[1],
            )
            for show in shows_data
        ]
