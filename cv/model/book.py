from cv.model.base_item import BaseItem
from cv.model.review import Review


class Book(BaseItem):
    def __init__(
        self,
        title: str,
        authors: str,
        image_url: str,
        review: Review = Review(""),
    ):
        super().__init__(title, image_url, review)
        self.authors = authors

    def __lt__(self, other: "Book"):
        return self.review < other.review
