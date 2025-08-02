from typing import Optional, Union

from dash import html


class Book:
    def __init__(
        self,
        title: str,
        title_short: str,
        authors: str,
        image_url: str,
        review: Optional[Union[str, html.Div]] = None,
    ):
        self.title = title
        self.title_short = title_short
        self.authors = authors
        self.image_url = image_url
        self.review = review

    @property
    def review_table(self) -> Union[html.Div, html.Span]:
        if isinstance(self.review, str):
            return html.Span(self.review, className="span-book")
        return self.review
