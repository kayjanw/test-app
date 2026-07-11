from typing import Union

import dash_mantine_components as dmc
from dash import html

from cv.model.review import Review


class BaseItem:
    def __init__(
        self,
        title: str,
        image_url: str,
        review: Review = Review(""),
    ):
        self.title = title
        self.image_url = image_url
        self.review = review

    @property
    def div(self) -> Union[dmc.Indicator, dmc.Card]:
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

        def _generate_card(_item: BaseItem) -> dmc.Card:
            return dmc.Card(
                children=[
                    html.Img(
                        src=_item.image_url,
                        className="card-carousel-image",
                    ),
                    html.Div(
                        [
                            html.Span(_item.title, className="card-carousel-title"),
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

        if isinstance(self.review.rating, str):
            return wrap_card(_generate_card(self), label=self.review.rating)
        return _generate_card(self)
