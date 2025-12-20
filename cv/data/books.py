from typing import List, Tuple

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


bookshelf_leisure = [
    Book(
        "The Little Prince",
        "The Little Prince",
        "Antoine de Saint-Exupery",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-18-56.png",
        "Adventure",
    ),
    Book(
        "The Girl Who Saved the King of Sweden",
        "The Girl Who Saved the King of Sweden",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-19-09.png",
        "Adventure, Satirical",
    ),
    Book(
        "The Hundred-Year-Old Man Who Climbed Out the Window and Disappeared",
        "The Hundred-Year-Old Man Who ...",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/719zo5utsfl._ac_uf10001000_ql80_.jpg",
        "Adventure, Satirical",
    ),
    Book(
        "Hitman Anders and the Meaning of It All",
        "Hitman Anders and the ...",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-19-34-1.png",
        "Adventure, Satirical",
    ),
    Book(
        "Before the Coffee Gets Cold",
        "Before the Coffee Gets Cold",
        "Toshikazu Kawaguchi",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-19-45-1.png",
        "Touching",
    ),
    Book(
        "Strange Pictures",
        "Strange Pictures",
        "Uketsu",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-20-14-1.png",
        "Mystery",
    ),
    Book(
        "Strange Houses",
        "Strange Houses",
        "Uketsu",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-20-23.png",
        "Mystery",
    ),
    Book(
        "Hidden Pictures",
        "Hidden Pictures",
        "Jason Rekulak",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-20-33-1.png",
        "Mystery",
    ),
    Book(
        "The Boring Book",
        "The Boring Book",
        "Shinsuke Yoshitake",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-1.jpg",
        "Fun",
    ),
    Book(
        "Butter",
        "Butter",
        "Asako Yuzuki",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-02-02-36.png",
        "Literary Fiction",
    ),
    Book(
        "The Accidental Further Adventures of the Hundred-Year-Old Man",
        "The Accidental Further Adventures ...",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-02-02-15.png",
    ),
    Book(
        "Last Night at the Telegraph Club",
        "Last Night at the Telegraph Club",
        "Malinda Lo",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/last-night-at-the-telegraph-club.png",
    ),
]
bookshelf_puzzle = [
    Book(
        "Think Twice",
        "Think Twice",
        "Alex Bellos",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-1-1.jpg",
        "Fun",
    ),
    Book(
        "Think Again!",
        "Think Again!",
        "John Pinkney",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/screenshot-2025-11-13-at-2.32.04-pm.png",
    ),
    Book(
        "KGB Killer Puzzzles Dossier",
        "KGB Killer Puzzzles Dossier",
        "Dmitry Raskolnikov",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/kgb-killer-puzzles.jpg",
    ),
]
bookshelf_self = [
    Book(
        "The Art of Thinking Clearly",
        "The Art of Thinking Clearly",
        "Rolf Dobelli",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-41-24.png",
        rating_review(5, "Must read", carousel=use_carousel),
    ),
    Book(
        "Difficult Conversations",
        "Difficult Conversations",
        "Douglas Stone",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-41-37.png",
        rating_review(5, "Learnt a lot", carousel=use_carousel),
    ),
    Book(
        "Crucial Conversations: Tools for Talking When Stakes are High",
        "Crucial Conversations",
        "Kerry Patterson, Joseph Grenny, Al Switzler, Ron McMillan",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-41-46.png",
        rating_review(4.33, "Not very structured", carousel=use_carousel),
    ),
    Book(
        "Life Coaching: Change Your Life in 7 Days",
        "Life Coaching",
        "Eileen Mulligan",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-42-14.png",
        rating_review(3, "Not comprehensive", carousel=use_carousel),
    ),
    Book(
        "Rules of Thinking",
        "Rules of Thinking",
        "Richard Templar",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-42-30.png",
        rating_review(3.33, "Interesting tips", carousel=use_carousel),
    ),
    Book(
        "Ikigai",
        "Ikigai",
        "Francesc Miralles, Hector Garcia",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-19-54.png",
        rating_review(3.33, "Inspiring", carousel=use_carousel),
    ),
    Book(
        "Ichigo Ichie",
        "Ichigo Ichie",
        "Francesc Miralles, Hector Garcia",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-20-04.png",
        rating_review(3.33, "Transformative", carousel=use_carousel),
    ),
    Book(
        "The 48 Laws of Power",
        "The 48 Laws of Power",
        "Robert Greene",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image.png",
        rating_review(3, "Nasty..", carousel=use_carousel),
    ),
    Book(
        "How To Break Up With Your Phone",
        "How To Break Up With Your Phone",
        "Catherine Price",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-3.jpg",
    ),
]
bookshelf_leadership = [
    Book(
        "The 21 Indispensable Qualities of a Leader",
        "The 21 Indispensable ...",
        "John C. Maxwell",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-41-57-1.png",
        rating_review(4.33, "Informative", carousel=use_carousel),
    ),
    Book(
        "The Manager's Path: A Guide for Tech Leaders Navigating Growth and Change",
        "The Manager's Path",
        "Camille Fournier",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-01-22-39-53.png",
        rating_review(5, "Insightful", carousel=use_carousel),
    ),
    Book(
        "Staff Engineer",
        "Staff Engineer",
        "Will Larson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/photo-2025-08-20-22-18-00.jpg",
        rating_review(5, "Practical", carousel=use_carousel),
    ),
    Book(
        "Engineering Management for the Rest of Us",
        "Engineering Management",
        "Sarah Drasner",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/photo-2025-08-20-22-18-04.jpg",
        rating_review(4.33, "Helpful", carousel=use_carousel),
    ),
    Book(
        "The Five Dysfunctions of a Team",
        "The Five Dysfunctions of a Team",
        "Patrick Lencioni",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/the-five-dysfunctions-of-a-team.jpg",
        rating_review(5, "Engaging and insightful", carousel=use_carousel),
    ),
]
bookshelf_finance = [
    Book(
        "Getting Started In Technical Analysis",
        "Getting Started In Technical Analysis",
        "Jack D. Schwager",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/715khkxn-ll.jpg?w=678",
        rating_review(3.33, "A little dry", carousel=use_carousel),
    ),
]
bookshelf_technical = [
    Book(
        "Software Teaming: A Mob Programming, Whole-Team Approach",
        "Software Teaming",
        "Woody Zuill, Kevin Meadows",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/71zbcvmyuzl._uf10001000_ql80_.jpg",
        rating_review(5, "Practical", carousel=use_carousel),
    ),
    Book(
        "Head First Software Architecture",
        "Head First Software Architecture",
        "Mark Richards, Neal Ford, Raju Gandhi",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/81drluswxkl-1.jpg?w=886",
        rating_review(4, "Easy to digest", carousel=use_carousel),
    ),
    Book(
        "The Pragmatic Programmer",
        "The Pragmatic Programmer",
        "David Thomas, Andrew Hunt",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-01-22-38-40.png",
        rating_review(5, "Awesome tips and reminder", carousel=use_carousel),
    ),
    Book(
        "Refactoring, Second Edition",
        "Refactoring, Second Edition",
        "Martin Fowler",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-01-22-40-17.png",
        rating_review(3, "Straightforward", carousel=use_carousel),
    ),
    Book(
        "Software Engineering at Google",
        "Software Engineering at Google",
        "Titus Winters, Tom Manshreck, Hyrum Wright",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-02-02-26.png",
        rating_review(3, "Long-winded", carousel=use_carousel),
    ),
    Book(
        "Why Programs Fail, A Guide to Systematic Debugging",
        "Why Programs Fail",
        "Andreas Zeller",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-03-01-07-53.png",
        rating_review(3, "Long-winded", carousel=use_carousel),
    ),
    Book(
        "Storytelling with Data",
        "Storytelling with Data",
        "Cole Nussbaumer Knaflic",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2.jpg",
        rating_review(4, "Easy to follow", carousel=use_carousel),
    ),
    Book(
        "Designing Data-Intensive Applications",
        "Designing Data-Intensive ...",
        "Martin Kleppmann, Chris Riccomini",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/download.png",
    ),
]


books_data: List[Tuple[List[Book], str]] = [
    (bookshelf_leisure, "Leisure"),
    (bookshelf_puzzle, "Puzzle"),
    (bookshelf_self, "Self-Improvement"),
    (bookshelf_leadership, "Leadership"),
    (bookshelf_finance, "Finance"),
    (bookshelf_technical, "Technical"),
]
# Split into read and reading
book_data = [
    ([book for book in books if book.review], theme) for books, theme in books_data
]
book_reading_data = [
    ([book for book in books if not book.review], theme) for books, theme in books_data
]

# Remove empty themes
book_data = [x for x in book_data if x[0]]
book_reading_data = [x for x in book_reading_data if x[0]]
