import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.layouts.cv_data import (
    books_read_leisure,
    books_read_self,
    books_read_technical,
    books_reading_leisure,
    books_reading_self,
    books_reading_technical,
    create_scrollable_area,
)

book_data = [
    (books_read_leisure, "Leisure"),
    (books_read_self, "Self-Improvement"),
    (books_read_technical, "Technical"),
]

book_reading_data = [
    (books_reading_leisure, "Leisure"),
    (books_reading_self, "Self-Improvement"),
    (books_reading_technical, "Technical"),
]


def books_tab(app):
    return html.Div(
        [
            content_header(
                "Bookshelf",
                [
                    DashIconify(icon="openmoji:croissant", height=40),
                    "Food for the brain",
                ],
            ),
            html.Div(
                [
                    html.H5("Books Read"),
                    dmc.Tabs(
                        children=[
                            dmc.TabsList(
                                [
                                    dmc.TabsTab(
                                        course[1],
                                        value=course[1],
                                    )
                                    for course in book_data
                                ]
                            ),
                        ]
                        + [
                            dmc.TabsPanel(
                                html.Div(
                                    create_scrollable_area(
                                        course[0],
                                        columns=["Title", "Author", "Review / Notes"],
                                    )
                                ),
                                value=course[1],
                            )
                            for course in book_data
                        ],
                        value=book_data[0][1],
                        color="#202029",
                        variant="default",
                        radius="md",
                        orientation="horizontal",
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.H5("Books Reading"),
                    dmc.Tabs(
                        children=[
                            dmc.TabsList(
                                [
                                    dmc.TabsTab(
                                        course[1],
                                        value=course[1],
                                    )
                                    for course in book_reading_data
                                ]
                            ),
                        ]
                        + [
                            dmc.TabsPanel(
                                html.Div(
                                    create_scrollable_area(
                                        course[0],
                                        columns=["Title", "Author"],
                                    )
                                ),
                                value=course[1],
                            )
                            for course in book_reading_data
                        ],
                        value=book_data[0][1],
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
