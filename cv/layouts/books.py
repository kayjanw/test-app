from typing import List, Union

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.books import Book, book_data, book_reading_data, convert_to_table
from cv.layouts.helper import create_scrollable_area
from cv.model.review import use_carousel
from cv.model.show import Show


def card_carousel(item: Union[Book, Show]) -> Union[dmc.Indicator, dmc.Card]:
    def wrap_card(_card: dmc.Card, label: str) -> dmc.Indicator:
        return dmc.Indicator(
            _card,
            position="top-end",
            inline=True,
            color="rgba(0,0,0,0)",
            size=24,
            label=dmc.Text(label, size="3em", className="crown-pulse"),
            offset=0,
            styles={
                "indicator": {
                    "transform": "translate(0%, 50%)",
                }
            },
        )

    def _generate_card(_item: Union[Book, Show]) -> dmc.Card:
        return dmc.Card(
            children=[
                html.Img(
                    src=_item.image_url,
                    className="card-book-image",
                ),
                html.Div(
                    [
                        html.Span(_item.title_short),
                        _item.review.div,
                    ],
                    className="card-book-children",
                ),
            ],
            shadow="sm",
            padding="md",
            radius="md",
            className="card-book",
        )

    if isinstance(item.review.rating, str):
        return wrap_card(_generate_card(item), label=item.review.rating)
    return _generate_card(item)


def book_carousel(books: List[Book]):
    return dmc.Container(
        children=[
            dmc.Carousel(
                [dmc.CarouselSlide(card_carousel(book)) for book in books],
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
                        value=book_reading_data[0][1],
                        color="#202029",
                        variant="default",
                        radius="md",
                        orientation="horizontal",
                    ),
                    html.Br(),
                ]
                if book_reading_data
                else [],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
