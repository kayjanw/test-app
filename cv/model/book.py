from cv.model.review import Review, is_numeric_rating


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
        if is_numeric_rating(self.review.rating) and is_numeric_rating(
            other.review.rating
        ):
            return self.review.rating > other.review.rating
        return self.review.genre_or_review < other.review.genre_or_review
