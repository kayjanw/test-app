from typing import Union

import dash_mantine_components as dmc
from dash import html

from cv.data.books import Book
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
                    className="card-carousel-image",
                ),
                html.Div(
                    [
                        html.Span(_item.title_short),
                        _item.review.div,
                    ],
                    className="card-carousel-children",
                ),
            ],
            shadow="sm",
            padding="md",
            radius="md",
            className="card-carousel",
        )

    if isinstance(item.review.rating, str):
        return wrap_card(_generate_card(item), label=item.review.rating)
    return _generate_card(item)
