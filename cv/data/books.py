from typing import List, Tuple

from cv.model.book import Book, Review

rating_system = {
    5: "Must read",
    4.5: "Must read, but not as good",
    4: "Good to read",
    3.5: "Can read if you want",
    3: "Do not bother",
    2: "It is bad",
}


def convert_to_table(bookshelf: List[Book]):
    return [
        [
            book.title,
            book.authors,
            book.review.div,
        ]
        for book in bookshelf
    ]


bookshelf_leisure = [
    Book(
        "The Little Prince",
        "Antoine de Saint-Exupery",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-18-56.png",
        Review("Children's Fiction"),
    ),
    Book(
        "The Girl Who Saved the King of Sweden",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-19-09.png",
        Review("Humorous Fiction"),
    ),
    Book(
        "The Hundred-Year-Old Man Who Climbed Out the Window and Disappeared",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/719zo5utsfl._ac_uf10001000_ql80_.jpg",
        Review("Humorous Fiction"),
    ),
    Book(
        "Hitman Anders and the Meaning of It All",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-19-34-1.png",
        Review("Humorous Fiction"),
    ),
    # 2025
    Book(
        "Before the Coffee Gets Cold",
        "Toshikazu Kawaguchi",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-19-45-1.png",
        Review("Time Travel Fiction"),
    ),
    Book(
        "Strange Pictures",
        "Uketsu",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-20-14-1.png",
        Review("Mystery", "👑"),
    ),
    Book(
        "Strange Houses",
        "Uketsu",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-20-23.png",
        Review("Mystery"),
    ),
    Book(
        "Hidden Pictures",
        "Jason Rekulak",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-20-33-1.png",
        Review("Mystery"),
    ),
    Book(
        "The Boring Book",
        "Shinsuke Yoshitake",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-1.jpg",
        Review("Children's Fiction"),
    ),
    Book(
        "Butter",
        "Asako Yuzuki",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-02-02-36.png",
        Review("Literary Fiction"),
    ),
    Book(
        "Last Night at the Telegraph Club",
        "Malinda Lo",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/last-night-at-the-telegraph-club.png",
        Review("Romance"),
    ),
    # 2026
    Book(
        "Foundryside",
        "Robert Jackson Bennett",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/foundryside.jpg",
        Review("Science Fiction"),
    ),
    Book(
        "The Accidental Further Adventures of the Hundred-Year-Old Man",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-02-02-15.png",
        Review("Humorous Fiction"),
    ),
    Book(
        "Strange Buildings",
        "Uketsu",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/img_2480.jpeg",
        Review("Mystery"),
    ),
    Book(
        "Welcome to the Hyunam-Dong Bookshop",
        "Hwang Bo-Reum",
        "https://kayjanw.wordpress.com/wp-content/uploads/2026/02/welcome-to-the-hyunam-dong-bookshop.jpg",
        Review("Cozy Fiction"),
    ),
    Book(
        "Vegetarian",
        "Han Kang",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/vegetarian.jpg",
        Review("Literary Fiction"),
    ),
    Book(
        "How to Solve Your Own Murder",
        "Kristen Perrin",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/how-to-solve-your-own-murder.jpg?w=678",
        Review("Mystery", "👍"),
    ),
    Book(
        "A Short Stay in Hell",
        "Steven L. Peck",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/a-short-stay-in-hell.jpg",
        Review("Philosophical Horror", "👑"),
    ),
    Book(
        "Small Boat",
        "Vincent Delecroix",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/img_2479.jpeg",
        Review("Psychological Fiction"),
    ),
    Book(
        "The Waiter",
        "Kwan Ann Tan",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/img_2578.jpeg",
        Review("Interactive Fiction"),
    ),
    Book(
        "Never Lie",
        "Freida McFadden",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/never-lie.jpg",
        Review("Suspense"),
    ),
    Book(
        "Julie Chan is Dead",
        "Liann Zhang",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/julie-chan-is-dead.jpg",
        Review("Suspense"),
    ),
    Book(
        "There Are Rivers In The Sky",
        "Elif Shafak",
        "https://kayjanw.wordpress.com/wp-content/uploads/2026/06/img_3256.jpeg",
    ),
    Book(
        "Sweet Sweet Revenge Ltd.",
        "Jonas Jonasson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/sweet-sweet-revenge.jpg?w=670",
    ),
]
bookshelf_puzzle = [
    # 2025
    Book(
        "Think Twice",
        "Alex Bellos",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-1-1.jpg",
        Review("Fun"),
    ),
    Book(
        "Think Again!",
        "John Pinkney",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/screenshot-2025-11-13-at-2.32.04-pm.png",
    ),
    # 2026
    Book(
        "KGB Killer Puzzzles Dossier",
        "Dmitry Raskolnikov",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/kgb-killer-puzzles.jpg",
    ),
    Book(
        "Logical Brain Games",
        "Dr Gareth Moore",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image.jpeg",
    ),
]
bookshelf_self = [
    Book(
        "The Art of Thinking Clearly",
        "Rolf Dobelli",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-41-24.png",
        Review("Must read", 5),
    ),
    Book(
        "Difficult Conversations",
        "Douglas Stone",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-41-37.png",
        Review("Learnt a lot", 5),
    ),
    Book(
        "Crucial Conversations",
        "Kerry Patterson, Joseph Grenny, Al Switzler, Ron McMillan",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-41-46.png",
        Review("Not very structured", 4.33),
    ),
    Book(
        "Life Coaching: Change Your Life in 7 Days",
        "Eileen Mulligan",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-42-14.png",
        Review("Not comprehensive", 3),
    ),
    Book(
        "Rules of Thinking",
        "Richard Templar",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-42-30.png",
        Review("Interesting tips", 3.33),
    ),
    # 2025
    Book(
        "Ikigai",
        "Francesc Miralles, Hector Garcia",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-19-54.png",
        Review("Inspiring", 3),
    ),
    Book(
        "Ichigo Ichie",
        "Francesc Miralles, Hector Garcia",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-20-04.png",
        Review("Transformative", 3),
    ),
    Book(
        "The 48 Laws of Power",
        "Robert Greene",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image.png",
        Review("Nasty..", 2),
    ),
    Book(
        "How To Break Up With Your Phone",
        "Catherine Price",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-3.jpg",
        Review("Good tips", 3.33),
    ),
    # 2026
    Book(
        "The Sleep Fix",
        "Diane Macedo",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/the-sleep-fix.jpg",
        Review("Good to know", 4),
    ),
    Book(
        "Having People Over",
        "Chelsea Fagan",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/having-people-over.jpg",
        Review("Quick read", 4),
    ),
    Book(
        "Poisonous People",
        "Leanne ten Brinke",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-1.png",
        Review("Not useful", 2.33),
    ),
]
bookshelf_leadership = [
    Book(
        "The 21 Indispensable Qualities of a Leader",
        "John C. Maxwell",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-01-41-57-1.png",
        Review("Informative", 4.33),
    ),
    # 2024
    Book(
        "The Manager's Path",
        "Camille Fournier",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-01-22-39-53.png",
        Review("Insightful", 5),
    ),
    Book(
        "Staff Engineer",
        "Will Larson",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/photo-2025-08-20-22-18-00.jpg",
        Review("Practical", 5),
    ),
    Book(
        "Engineering Management for the Rest of Us",
        "Sarah Drasner",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/photo-2025-08-20-22-18-04.jpg",
        Review("Helpful", 4.33),
    ),
    # 2025
    Book(
        "The Five Dysfunctions of a Team",
        "Patrick Lencioni",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/the-five-dysfunctions-of-a-team.jpg",
        Review("Engaging and insightful", 5),
    ),
    Book(
        "The First 90 Days",
        "Michael D. Watkins",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/the-first-90-days.jpg",
        Review("Not very generic", 3.33),
    ),
]
bookshelf_finance = [
    Book(
        "Getting Started In Technical Analysis",
        "Jack D. Schwager",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/715khkxn-ll.jpg?w=678",
        Review("A little dry", 3.33),
    ),
]
bookshelf_technical = [
    # 2024
    Book(
        "Software Teaming: A Mob Programming, Whole-Team Approach",
        "Woody Zuill, Kevin Meadows",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/71zbcvmyuzl._uf10001000_ql80_.jpg",
        Review("Practical", 5),
    ),
    Book(
        "Head First Software Architecture",
        "Mark Richards, Neal Ford, Raju Gandhi",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/81drluswxkl-1.jpg?w=886",
        Review("Easy to digest", 4),
    ),
    Book(
        "The Pragmatic Programmer",
        "David Thomas, Andrew Hunt",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-01-22-38-40.png",
        Review("Awesome tips and reminder", 5),
    ),
    Book(
        "Refactoring, Second Edition",
        "Martin Fowler",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-01-22-40-17.png",
        Review("Straightforward", 3),
    ),
    Book(
        "Software Engineering at Google",
        "Titus Winters, Tom Manshreck, Hyrum Wright",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-02-02-02-26.png",
        Review("Long-winded", 3),
    ),
    Book(
        "Why Programs Fail, A Guide to Systematic Debugging",
        "Andreas Zeller",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2025-08-03-01-07-53.png",
        Review("Long-winded", 3),
    ),
    Book(
        "Storytelling with Data",
        "Cole Nussbaumer Knaflic",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/image-2.jpg",
        Review("Easy to follow", 4),
    ),
    Book(
        "Designing Data-Intensive Applications",
        "Martin Kleppmann, Chris Riccomini",
        "https://kayjanw.wordpress.com/wp-content/uploads/2022/11/download.png",
        Review("Detailed", 4),
    ),
    # 2026
]


books_data: List[Tuple[List[Book], str]] = [
    (sorted(bookshelf_leisure), "Leisure"),
    (sorted(bookshelf_puzzle), "Puzzle"),
    (sorted(bookshelf_self), "Self-Improvement"),
    (sorted(bookshelf_leadership), "Leadership"),
    (sorted(bookshelf_finance), "Finance"),
    (sorted(bookshelf_technical), "Technical"),
]
# Split into read and reading
book_data = [
    ([book for book in books if book.review.genre_or_review], theme)
    for books, theme in books_data
]
book_reading_data = [
    ([book for book in books if not book.review.genre_or_review], theme)
    for books, theme in books_data
]

# Remove empty themes
book_data = [x for x in book_data if x[0]]
book_reading_data = [x for x in book_reading_data if x[0]]
