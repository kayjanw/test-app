from typing import List

from cv.layouts.helper import rating_review
from cv.model.book import Book

use_carousel = True


def convert_to_table(bookshelf: List[Book]):
    return [
        [
            book.title,
            book.authors,
            book.review,
        ]
        for book in bookshelf
    ]


bookshelf_read_leisure = [
    Book(
        "The Little Prince",
        "The Little Prince",
        "Antoine de Saint-Exupery",
        "https://i.ibb.co/SDCjmpxZ/image-2025-08-02-01-18-56.png",
        "Adventure",
    ),
    Book(
        "The Girl Who Saved the King of Sweden",
        "The Girl Who Saved the King of Sweden",
        "Jonas Jonasson",
        "https://i.ibb.co/Z17rGSjj/image-2025-08-02-01-19-09.png",
        "Adventure, Satirical",
    ),
    Book(
        "The Hundred-Year-Old Man Who Climbed Out the Window and Disappeared",
        "The Hundred-Year-Old Man Who ...",
        "Jonas Jonasson",
        "https://i.ibb.co/qLk2QWRW/image-2025-08-02-01-19-21.png",
        "Adventure, Satirical",
    ),
    Book(
        "Hitman Anders and the Meaning of It All",
        "Hitman Anders and the ...",
        "Jonas Jonasson",
        "https://i.ibb.co/VWVDx8cj/image-2025-08-02-01-19-34.png",
        "Adventure, Satirical",
    ),
    Book(
        "Before the Coffee Gets Cold",
        "Before the Coffee Gets Cold",
        "Toshikazu Kawaguchi",
        "https://i.ibb.co/5D9Wsbk/image-2025-08-02-01-19-45.png",
        "Touching",
    ),
    Book(
        "Ikigai",
        "Ikigai",
        "Francesc Miralles, Hector Garcia",
        "https://i.ibb.co/5W0S3bZG/image-2025-08-02-01-19-54.png",
        "Inspiring",
    ),
    Book(
        "Ichigo Ichie",
        "Ichigo Ichie",
        "Francesc Miralles, Hector Garcia",
        "https://i.ibb.co/DgHs9mLG/image-2025-08-02-01-20-04.png",
        "Transformative",
    ),
    Book(
        "Strange Pictures",
        "Strange Pictures",
        "Uketsu",
        "https://i.ibb.co/KcxbSKQ2/image-2025-08-02-01-20-14.png",
        "Mystery",
    ),
    Book(
        "Strange Houses",
        "Strange Houses",
        "Uketsu",
        "https://i.ibb.co/gFzwGWKv/image-2025-08-02-01-20-23.png",
        "Mystery",
    ),
    Book(
        "Hidden Pictures",
        "Hidden Pictures",
        "Jason Rekulak",
        "https://i.ibb.co/8nn5QGYL/image-2025-08-02-01-20-33.png",
        "Mystery",
    ),
]
bookshelf_read_self = [
    Book(
        "The Art of Thinking Clearly",
        "The Art of Thinking Clearly",
        "Rolf Dobelli",
        "https://i.ibb.co/JwxH70Mh/image-2025-08-02-01-41-24.png",
        rating_review(5, "Must read", carousel=use_carousel),
    ),
    Book(
        "Difficult Conversations",
        "Difficult Conversations",
        "Douglas Stone",
        "https://i.ibb.co/67gK4gXJ/image-2025-08-02-01-41-37.png",
        rating_review(5, "Learnt a lot", carousel=use_carousel),
    ),
    Book(
        "Crucial Conversations: Tools for Talking When Stakes are High",
        "Crucial Conversations",
        "Kerry Patterson, Joseph Grenny, Al Switzler, Ron McMillan",
        "https://i.ibb.co/SDVy4ngZ/image-2025-08-02-01-41-46.png",
        rating_review(4.33, "Not very structured", carousel=use_carousel),
    ),
    Book(
        "Life Coaching: Change Your Life in 7 Days",
        "Life Coaching",
        "Eileen Mulligan",
        "https://i.ibb.co/mnnGrbb/image-2025-08-02-01-42-14.png",
        rating_review(3, "Not comprehensive", carousel=use_carousel),
    ),
    Book(
        "Rules of Thinking",
        "Rules of Thinking",
        "Richard Templar",
        "https://i.ibb.co/N6jyVLVF/image-2025-08-02-01-42-30.png",
        rating_review(3.33, "Interesting tips", carousel=use_carousel),
    ),
]
bookshelf_read_leadership = [
    Book(
        "The 21 Indispensable Qualities of a Leader",
        "The 21 Indispensable ...",
        "John C. Maxwell",
        "https://i.ibb.co/dJ5kyJYp/image-2025-08-02-01-41-57.png",
        rating_review(4.33, "Insightful", carousel=use_carousel),
    ),
    Book(
        "The Manager's Path: A Guide for Tech Leaders Navigating Growth and Change",
        "The Manager's Path",
        "Camille Fournier",
        "https://i.ibb.co/S7mHwqdy/image-2025-08-01-22-39-53.png",
        rating_review(5, "Insightful", carousel=use_carousel),
    ),
]
bookshelf_read_finance = [
    Book(
        "Getting Started In Technical Analysis",
        "Getting Started In Technical Analysis",
        "Jack D. Schwager",
        "https://i.ibb.co/BHbYPTQR/image-2025-08-01-22-40-05.png",
        rating_review(3.33, "A little dry", carousel=use_carousel),
    ),
]
bookshelf_read_technical = [
    Book(
        "Software Teaming: A Mob Programming, Whole-Team Approach",
        "Software Teaming",
        "Woody Zuill, Kevin Meadows",
        "https://i.ibb.co/nNkWL4Mf/image-2025-08-01-22-38-52.png",
        rating_review(5, "Practical", carousel=use_carousel),
    ),
    Book(
        "Head First Software Architecture",
        "Head First Software Architecture",
        "Mark Richards, Neal Ford, Raju Gandhi",
        "https://i.ibb.co/yFKs7dVv/image-2025-08-01-22-39-22.png",
        rating_review(4, "Easy to digest", carousel=use_carousel),
    ),
    Book(
        "The Pragmatic Programmer",
        "The Pragmatic Programmer",
        "David Thomas, Andrew Hunt",
        "https://i.ibb.co/Q7405kMZ/image-2025-08-01-22-38-40.png",
        rating_review(5, "Awesome tips and reminder", carousel=use_carousel),
    ),
    Book(
        "Refactoring, Second Edition",
        "Refactoring, Second Edition",
        "Martin Fowler",
        "https://i.ibb.co/XrkQzQc1/image-2025-08-01-22-40-17.png",
        rating_review(3, "Straightforward", carousel=use_carousel),
    ),
    Book(
        "Software Engineering at Google",
        "Software Engineering at Google",
        "Titus Winters, Tom Manshreck, Hyrum Wright",
        "https://i.ibb.co/dsjVRZrL/image-2025-08-02-02-02-26.png",
        rating_review(3, "Long-winded", carousel=use_carousel),
    ),
    Book(
        "Why Programs Fail, A Guide to Systematic Debugging",
        "Why Programs Fail",
        "Andreas Zeller",
        "https://i.ibb.co/cXkK4hh7/image-2025-08-03-01-07-53.png",
        rating_review(3, "Long-winded", carousel=use_carousel),
    ),
]

bookshelf_reading_leisure = [
    Book(
        "The Accidental Further Adventures of the Hundred-Year-Old Man",
        "The Accidental Further Adventures ...",
        "Jonas Jonasson",
        "https://i.ibb.co/ccZWfqgh/image-2025-08-02-02-02-15.png",
    ),
    Book(
        "Butter",
        "Butter",
        "Asako Yuzuki",
        "https://i.ibb.co/7xLWM9cr/image-2025-08-02-02-02-36.png",
    ),
]
bookshelf_reading_self = []
bookshelf_reading_leadership = [
    Book(
        "Engineering Management for the Rest of Us",
        "Engineering Management",
        "Sarah Drasner",
        "https://i.ibb.co/nGDM9y8/photo-2025-08-20-22-18-04.jpg",
    ),
    Book(
        "Staff Engineer",
        "Staff Engineer",
        "Will Larson",
        "https://i.ibb.co/Q7nRHncd/photo-2025-08-20-22-18-00.jpg",
    )
]
bookshelf_reading_finance = []
bookshelf_reading_technical = [
    Book(
        "Designing Data-Intensive Applications",
        "Designing Data-Intensive ...",
        "Martin Kleppmann, Chris Riccomini",
        "https://i.ibb.co/W4MkJxj0/download.png",
    ),
]

book_data = [
    (bookshelf_read_leisure, "Leisure"),
    (bookshelf_read_self, "Self-Improvement"),
    (bookshelf_read_leadership, "Leadership"),
    (bookshelf_read_finance, "Finance"),
    (bookshelf_read_technical, "Technical"),
]
book_reading_data = [
    (bookshelf_reading_leisure, "Leisure"),
    # (bookshelf_reading_self, "Self-Improvement"),
    (bookshelf_reading_leadership, "Leadership"),
    # (bookshelf_reading_finance, "Finance"),
    (bookshelf_reading_technical, "Technical"),
]
