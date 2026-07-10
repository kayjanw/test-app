from typing import List

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.shows import shows_data
from cv.layouts.books import card_carousel
from cv.model.show import Show


def show_carousel(shows: List[Show]):
    return dmc.Container(
        children=[
            dmc.Carousel(
                [dmc.CarouselSlide(card_carousel(show)) for show in shows],
                controlSize=45,
                slideSize="18%",
                slideGap="md",
                withIndicators=True,
                emblaOptions={"loop": False, "align": "start", "slidesToScroll": 2},
                height=550,
                classNames={
                    "root": "dmc-root",
                    "controls": "dmc-controls",
                    "control": "dmc-control",
                    "indicator": "dmc-indicator",
                },
            ),
        ],
        className="container-book",
    )


def show_splash(shows: List[Show]):
    return html.Div(
        children=[
            dmc.Card(
                [card_carousel(show) for show in shows],
                className="card-show",
            ),
        ],
        className="container-show",
    )


def shows_tab(app):
    return html.Div(
        [
            content_header(
                "Theatre",
                [
                    DashIconify(icon="openmoji:film-projector", height=40),
                    "Work and Plays",
                ],
            ),
            html.Div(
                [
                    html.H5("Theatre"),
                    dmc.Tabs(
                        children=[
                            dmc.TabsList(
                                [
                                    dmc.TabsTab(
                                        show[1],
                                        value=show[1],
                                    )
                                    for show in shows_data
                                ]
                            ),
                        ]
                        + [
                            dmc.TabsPanel(
                                show_splash(show[0]),
                                value=show[1],
                            )
                            for show in shows_data
                        ],
                        value=shows_data[0][1],
                        color="#202029",
                        variant="default",
                        radius="md",
                        orientation="horizontal",
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
