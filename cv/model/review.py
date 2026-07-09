from typing import Union

import dash_mantine_components as dmc
from dash import html

use_carousel = True


def is_numeric_rating(rating: Union[None, float, int, str]):
    return isinstance(rating, int) or isinstance(rating, float)


class Review:
    def __init__(
        self, genre_or_review: str, rating: Union[None, float, int, str] = None
    ):
        self.genre_or_review = genre_or_review
        self.rating = rating

    @property
    def div(self) -> Union[html.Span, html.Div, dmc.Group]:
        if use_carousel:
            if not is_numeric_rating(self.rating):
                return html.Span(self.genre_or_review, className="span-book")
            return html.Div(
                [
                    dmc.Rating(fractions=3, value=self.rating, readOnly=True),
                    html.Span(self.genre_or_review, className="span-book"),
                ]
            )
        return dmc.Group(
            [
                dmc.Rating(fractions=3, value=self.rating, readOnly=True),
                html.Span(self.genre_or_review),
            ]
        )
