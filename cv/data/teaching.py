from dash import html

from cv.model.accordian_row import AccordianDetails, AccordianRow

use_accordian = True

hei_details = AccordianRow(
    "Instructor, Heicoders Academy",
    "Jun 2022 - Present",
    "tabler:code",
    {
        "Teaching": [
            AccordianDetails(
                "✔️",
                "Responsible for instructing AI200 Applied Machine Learning course",
            )
        ],
    },
    "teaching-hei",
)

writing_details = AccordianRow(
    "Content Writer, Various Publishers",
    "Jan 2022 - Present",
    "tabler:pencil",
    {
        "Writing": [
            AccordianDetails(
                "🎖",
                "Key accomplishments include having multiple articles of over 100K views",
                highlight="100K views",
            ),
            AccordianDetails(
                "✔️", "Published on Towards Data Science, Python in Plain English"
            ),
        ],
    },
    "teaching-writing",
)

ga_details = AccordianRow(
    "Instructor Assistant, General Assembly",
    "Dec 2023 - Jun 2024",
    "tabler:code",
    {
        "Teaching": [
            AccordianDetails(
                "✔️",
                "Responsible for grading assignments for Software Engineering Immersive Flex (SEIF) course",
            )
        ]
    },
    "teaching-ga",
)

nus_details = AccordianRow(
    "Assistant Lecturer, National University of Singapore (NUS), School of Computing",
    "Jan 2021 - Oct 2023",
    "tabler:code",
    {
        "Teaching": [
            AccordianDetails(
                "✔️",
                "Equipped over 300 NUS Executive and Administrative staff with working knowledge of AI and experience "
                "in structuring projects with CRISP-DM framework",
            ),
            AccordianDetails(
                "✔️",
                "Conducted teaching sessions in flipped classroom model and project grading",
            ),
        ],
    },
    "teaching-nus",
)

cristofori_details = AccordianRow(
    "Music Teacher, Cristofori",
    "Dec 2017 - Jul 2018",
    "tabler:music",
    {
        "Teaching": [
            AccordianDetails(
                "✔️",
                "Conduct electronic keyboard lessons for under-privileged children at Providence Care Centre",
            )
        ],
    },
    "teaching-cristofori",
)

dajin_details = AccordianRow(
    "Daycare Tutor, Dajin Daycare",
    "Dec 2014 - Apr 2015",
    "tabler:math",
    {
        "Teaching": [
            AccordianDetails(
                "✔️",
                "Nurtured primary school children, up to a class of 20 students, and taught the students English, "
                "Mathematics, Science and Mother Tongue (Mandarin) with 100% passing rate",
            ),
            AccordianDetails(
                "✔️",
                "Tutored the weaker students personally after daycare working hours to help the students understand "
                "the main concepts and catch up with the rest of the class",
            ),
        ],
    },
    "teaching-dajin",
)

tutor_details = AccordianRow(
    "Private Tutor",
    "Dec 2014 - Oct 2015",
    "tabler:math",
    {
        "Teaching": [
            AccordianDetails(
                "✔️",
                "Provide one-to-one private tuition for Junior College Mathematics and Primary School English, "
                "Mathematics and Science",
            )
        ],
    },
    "teaching-tutor",
)

teaching_accordian_data = [
    hei_details,
    writing_details,
    ga_details,
    nus_details,
    cristofori_details,
    dajin_details,
    tutor_details,
]


teaching_data = [
    html.Div(
        [
            html.H5(_teaching_data.title),
            html.H6(_teaching_data.subtitle),
            html.Br(),
            *[
                html.P(
                    f"{detail.icon} {detail.detail}",
                    className="p-indent",
                )
                for details in _teaching_data.details.values()
                for detail in details
            ],
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    )
    for _teaching_data in teaching_accordian_data
]
