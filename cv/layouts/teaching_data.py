import dash_mantine_components as dmc
from dash import html

from cv.layouts.helper import bullet_point

hei_details = [
    "Instructor, Heicoders Academy",
    "Jun 2022 - Present",
    "tabler:code",
    [
        bullet_point(
            "✔️",
            html.P("Responsible for instructing AI200 Applied Machine Learning course"),
        )
    ],
    "teaching-hei",
]

writing_details = [
    "Content Writer, Various Publishers",
    "Jan 2022 - Present",
    "tabler:pencil",
    [
        bullet_point(
            "🎖",
            dmc.Highlight(
                "Key accomplishments include having multiple articles of over 100K views",
                highlight="100K views",
                style={"fontSize": "inherit"},
            ),
        ),
        bullet_point(
            "✔️", html.P("Published on Towards Data Science, Python in Plain English")
        ),
    ],
    "teaching-writing",
]

ga_details = [
    "Instructor Assistant, General Assembly",
    "Dec 2023 - Jun 2024",
    "tabler:code",
    [
        bullet_point(
            "✔️",
            html.P(
                "Responsible for grading assignments for Software Engineering Immersive Flex (SEIF) course"
            ),
        )
    ],
    "teaching-ga",
]

nus_details = [
    "Assistant Lecturer, National University of Singapore (NUS), School of Computing",
    "Jan 2021 - Oct 2023",
    "tabler:code",
    [
        bullet_point(
            "✔️",
            html.P(
                "Equipped over 300 NUS Executive and Administrative staff with working knowledge of AI and experience "
                "in structuring projects with CRISP-DM framework"
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Conducted teaching sessions in flipped classroom model and project grading"
            ),
        ),
    ],
    "teaching-nus",
]

cristofori_details = [
    "Music Teacher, Cristofori",
    "Dec 2017 - Jul 2018",
    "tabler:music",
    [
        bullet_point(
            "✔️",
            html.P(
                "Conduct electronic keyboard lessons for under-privileged children at Providence Care Centre"
            ),
        )
    ],
    "teaching-cristofori",
]

dajin_details = [
    "Daycare Tutor, Dajin Daycare",
    "Dec 2014 - Apr 2015",
    "tabler:math",
    [
        bullet_point(
            "✔️",
            html.P(
                "Nurtured primary school children, up to a class of 20 students, and taught the students English, "
                "Mathematics, Science and Mother Tongue (Mandarin) with 100% passing rate"
            ),
        ),
        bullet_point(
            "✔️",
            html.P(
                "Tutored the weaker students personally after daycare working hours to help the students understand "
                "the main concepts and catch up with the rest of the class"
            ),
        ),
    ],
    "teaching-dajin",
]

tutor_details = [
    "Private Tutor",
    "Dec 2014 - Oct 2015",
    "tabler:math",
    [
        bullet_point(
            "✔️",
            html.P(
                "Provide one-to-one private tuition for Junior College Mathematics and Primary School English, "
                "Mathematics and Science"
            ),
        )
    ],
    "teaching-tutor",
]

teaching_content_details = [
    html.Div(
        [
            html.H5("Instructor, Heicoders Academy"),
            html.H6("Jun 2022 - Present"),
            html.Br(),
            html.P(
                (
                    "✔️ Responsible for instructing AI200 Applied Machine Learning course"
                ),
                className="p-indent",
            ),
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    ),
    html.Div(
        [
            html.H5("Content Writer, Various Publishers"),
            html.H6("Jan 2022 - Present"),
            html.Br(),
            html.P(
                dmc.Highlight(
                    "🎖️ Key accomplishments include having multiple articles of over 100K views",
                    highlight="100K views",
                    style={"fontSize": "inherit"},
                ),
                className="p-indent",
            ),
            html.P(
                "✔️ Published on Towards Data Science, Python in Plain English",
                className="p-indent",
            ),
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    ),
    html.Div(
        [
            html.H5("Instructor Assistant, General Assembly"),
            html.H6("Dec 2023 - Jun 2024"),
            html.Br(),
            html.P(
                "✔️ Responsible for grading assignments for Software Engineering Immersive Flex (SEIF) course",
                className="p-indent",
            ),
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    ),
    html.Div(
        [
            html.H5(
                "Assistant Lecturer, National University of Singapore (NUS), School of Computing"
            ),
            html.H6("Jan 2021 - Oct 2023"),
            html.Br(),
            html.P(
                "✔️ Equipped over 300 NUS Executive and Administrative staff with working knowledge of AI and "
                "experience in structuring projects with CRISP-DM framework",
                className="p-indent",
            ),
            html.P(
                "✔️ Conducted teaching sessions in flipped classroom model and project grading",
                className="p-indent",
            ),
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    ),
    html.Div(
        [
            html.H5("Music Teacher, Cristofori"),
            html.H6("Dec 2017 - Jul 2018"),
            html.Br(),
            html.P(
                "✔️ Conduct electronic keyboard lessons for under-privileged children at Providence Care Centre",
                className="p-indent",
            ),
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    ),
    html.Div(
        [
            html.H5("Daycare Tutor, Dajin Daycare"),
            html.H6("Dec 2014 - Apr 2015"),
            html.Br(),
            html.P(
                "✔️ Nurtured primary school children, up to a class of 20 students, and taught the students English, "
                "Mathematics, Science and Mother Tongue (Mandarin) with 100% passing rate",
                className="p-indent",
            ),
            html.P(
                "✔️ Tutored the weaker students personally after daycare working hours to help the students understand "
                "the main concepts and catch up with the rest of the class",
                className="p-indent",
            ),
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    ),
    html.Div(
        [
            html.H5("Private Tutor"),
            html.H6("Dec 2014 - Oct 2015"),
            html.Br(),
            html.P(
                (
                    "✔️ Provide one-to-one private tuition for Junior College Mathematics and Primary School English, "
                    "Mathematics and Science"
                ),
                className="p-indent",
            ),
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    ),
]
