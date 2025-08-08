from typing import List

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.books import (
    Book,
    book_data,
    book_reading_data,
    convert_to_table,
    use_carousel,
)
from cv.layouts.helper import create_scrollable_area


def book_carousel(books: List[Book]):
    return dmc.Container(
        children=[
            dmc.Carousel(
                [
                    dmc.CarouselSlide(
                        dmc.Card(
                            children=[
                                html.Img(
                                    src=book.image_url,
                                    height=200,
                                    style={"minWidth": "150px"},
                                ),
                                html.Div(
                                    [
                                        html.Span(book.title_short),
                                        book.review_table,
                                    ],
                                    className="card-book-children",
                                ),
                            ],
                            shadow="sm",
                            padding="md",
                            radius="md",
                            className="card-book",
                        )
                    )
                    for book in books
                ],
                controlSize=45,
                slideSize="18%",
                slideGap="md",
                withIndicators=True,
                emblaOptions={"loop": False, "align": "start"},
                height=550,
            ),
        ],
        className="container-book",
    )


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
                                        book[1],
                                        value=book[1],
                                    )
                                    for book in book_data
                                ]
                            ),
                        ]
                        + [
                            dmc.TabsPanel(
                                book_carousel(book[0])
                                if use_carousel
                                else create_scrollable_area(
                                    convert_to_table(book[0]),
                                    columns=["Title", "Author", "Review / Notes"],
                                ),
                                value=book[1],
                            )
                            for book in book_data
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
                                        book[1],
                                        value=book[1],
                                    )
                                    for book in book_reading_data
                                ]
                            ),
                        ]
                        + [
                            dmc.TabsPanel(
                                book_carousel(book[0])
                                if use_carousel
                                else create_scrollable_area(
                                    convert_to_table(book[0]),
                                    columns=["Title", "Author"],
                                ),
                                value=book[1],
                            )
                            for book in book_reading_data
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
