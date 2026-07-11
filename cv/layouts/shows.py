import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.shows import shows_data


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
