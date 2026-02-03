from typing import Union

import dash_mantine_components as dmc
from dash import html

use_carousel = True


class Review:
    def __init__(self, genre_or_review: str, rating: Union[None, float, int] = None):
        self.genre_or_review = genre_or_review
        self.rating = rating

    @property
    def div(self) -> Union[html.Span, html.Div, dmc.Group]:
        if use_carousel:
            if self.rating is None:
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


class Book:
    def __init__(
        self,
        title: str,
        title_short: str,
        authors: str,
        image_url: str,
        review: Review = Review(""),
    ):
        self.title = title
        self.title_short = title_short
        self.authors = authors
        self.image_url = image_url
        self.review = review

    def __lt__(self, other: "Book"):
        # Sort based on rating (descending order) or genre_or_review (ascending order)
        if self.review.rating is not None and other.review.rating is not None:
            return self.review.rating > other.review.rating
        return self.review.genre_or_review < other.review.genre_or_review
