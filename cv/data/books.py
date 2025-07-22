from cv.layouts.helper import rating_review

books_read_leisure = [
    [
        "The Little Prince",
        "Antoine de Saint-Exupery",
        "Adventure",
    ],
    [
        "The Girl Who Saved the King of Sweden",
        "Jonas Jonasson",
        "Adventure, Satirical",
    ],
    [
        "The Hundred-Year-Old Man Who Climbed Out the Window and Disappeared",
        "Jonas Jonasson",
        "Adventure, Satirical",
    ],
    [
        "Hitman Anders and the Meaning of It All",
        "Jonas Jonasson",
        "Adventure, Satirical",
    ],
    [
        "Before the Coffee Gets Cold",
        "Toshikazu Kawaguchi",
        "Touching",
    ],
    [
        "Ikigai",
        "Francesc Miralles, Hector Garcia",
        "Inspiring",
    ],
    [
        "Ichigo Ichie",
        "Francesc Miralles, Hector Garcia",
        "Transformative",
    ],
    [
        "Strange Pictures",
        "Uketsu",
        "Mystery",
    ],
    [
        "Strange Houses",
        "Uketsu",
        "Mystery",
    ],
    [
        "Hidden Pictures",
        "Jason Rekulak",
        "Mystery",
    ],
]


books_read_self = [
    [
        "The Art of Thinking Clearly",
        "Rolf Dobelli",
        rating_review(5, "Must read"),
    ],
    [
        "Difficult Conversations",
        "Douglas Stone",
        rating_review(5, "Learnt a lot"),
    ],
    [
        "Crucial Conversations: Tools for Talking When Stakes are High",
        "Kerry Patterson, Joseph Grenny, Al Switzler, Ron McMillan",
        rating_review(4.33, "Not very structured"),
    ],
    [
        "The 21 Indispensable Qualities of a Leader",
        "John C. Maxwell",
        rating_review(4.33, "Insightful"),
    ],
    [
        "Life Coaching: Change Your Life in 7 Days",
        "Eileen Mulligan",
        rating_review(3, "Not comprehensive"),
    ],
    ["Rules of Thinking", "Richard Templar", rating_review(3.33, "Interesting tips")],
]
books_read_technical = [
    [
        "Software Teaming: A Mob Programming, Whole-Team Approach",
        "Woody Zuill, Kevin Meadows",
        rating_review(5, "Practical"),
    ],
    [
        "Head First Software Architecture",
        "Mark Richards, Neal Ford, Raju Gandhi",
        rating_review(4, "Easy to digest"),
    ],
    [
        "The Pragmatic Programmer",
        "David Thomas, Andrew Hunt",
        rating_review(5, "Awesome tips and reminder"),
    ],
    [
        "The Manager's Path: A Guide for Tech Leaders Navigating Growth and Change",
        "Camille Fournier",
        rating_review(5, "Insightful"),
    ],
    [
        "Getting Started In Technical Analysis",
        "Jack D. Schwager",
        rating_review(3.33, "A little dry"),
    ],
    [
        "Refactoring, Second Edition",
        "Martin Fowler",
        rating_review(3, "Straightforward"),
    ],
]
books_reading_leisure = [
    [
        "The Accidental Further Adventures of the Hundred-Year-Old Man",
        "Jonas Jonasson",
    ],
    [
        "Butter",
        "Asako Yuzuki",
    ],
]
books_reading_self = []
books_reading_technical = [
    ["Software Engineering at Google", "Titus Winters, Tom Manshreck, Hyrum Wright"]
]


book_data = [
    (books_read_leisure, "Leisure"),
    (books_read_self, "Self-Improvement"),
    (books_read_technical, "Technical"),
]

book_reading_data = [
    (books_reading_leisure, "Leisure"),
    (books_reading_self, "Self-Improvement"),
    (books_reading_technical, "Technical"),
]
