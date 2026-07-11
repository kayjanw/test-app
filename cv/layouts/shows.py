from typing import List

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.shows import shows_data
from cv.model.show import Show


def divide_cols(shows: list[Show], n_cols: int):
    shows_cols = [shows[i::n_cols] for i in range(n_cols)]
    return dmc.Group(
        [html.Div([show.div for show in shows_col]) for shows_col in shows_cols],
        align="flex-start",
        grow=True,
    )


def show_splash(shows: List[Show], n_cols: int):
    return html.Div(
        children=[
            dmc.Card(
                divide_cols(shows, n_cols),
                # [show.div for show in shows],
                className="card-show",
            ),
        ],
        className="container-show",
    )


def shows_tab(app):
    return html.Div(
        [
            content_header(
                "Shows",
                [
                    DashIconify(icon="openmoji:film-projector", height=40),
                    "No work and all plays",
                ],
            ),
            html.Div(
                [
                    dmc.Tabs(
                        children=[],
                        value=shows_data[0][1],
                        color="#202029",
                        variant="default",
                        radius="md",
                        orientation="horizontal",
                        id="shows-tab",
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
