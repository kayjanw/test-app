import datetime as dt

from cv.model.base_item import BaseItem
from cv.model.review import Review


class Show(BaseItem):
    def __init__(
        self,
        title: str,
        image_url: str,
        production: str,
        date: str | dt.datetime,
        location: str,
        seat: str = "",
        review: Review = Review(""),
    ):
        super().__init__(title, image_url, review)
        self.production = production
        self.date = date
        self.location = location
        self.seat = seat
