import datetime as dt

from cv.model.review import Review


class Show:
    def __init__(
        self,
        title: str,
        title_short: str,
        image_url: str,
        production: str,
        date: str | dt.datetime,
        location: str,
        seat: str = "",
        review: Review = Review(""),
    ):
        self.title = title
        self.title_short = title_short
        self.image_url = image_url
        self.production = production
        self.date = date
        self.location = location
        self.seat = seat
        self.review = review

    def __lt__(self, other: "Show") -> bool:
        return self.review.rating > other.review.rating
