from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header


def teaching_tab(app):
    return html.Div(
        [
            content_header(
                "Teaching, Writing",
                [
                    DashIconify(icon="openmoji:beating-heart", height=40),
                    "Giving back what I learnt",
                ],
            ),
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
                        (
                            "🎖️ Key accomplishments include having multiple articles of over 100K views"
                        ),
                        className="p-indent",
                    ),
                    html.P(
                        (
                            "✔️ Published on Towards Data Science, Python in Plain English"
                        ),
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
                        (
                            "✔️ Responsible for grading assignments for Software Engineering Immersive Flex (SEIF) "
                            "course"
                        ),
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
                        (
                            "✔️ Equipped over 300 NUS Executive and Administrative staff with working knowledge of AI "
                            "and experience in structuring projects with CRISP-DM framework"
                        ),
                        className="p-indent",
                    ),
                    html.P(
                        (
                            "✔️ Conducted teaching sessions in flipped classroom model and project grading"
                        ),
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
                        (
                            "✔️ Conduct electronic keyboard lessons for under-privileged children at Providence Care "
                            "Centre"
                        ),
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
                        (
                            "✔️ Nurtured primary school children, up to a class of 20 students, and taught the students "
                            "English, Mathematics, Science and Mother Tongue (Mandarin) with 100% passing rate"
                        ),
                        className="p-indent",
                    ),
                    html.P(
                        (
                            "✔️ Tutored the weaker students personally after daycare working hours to help the students "
                            "understand the main concepts and catch up with the rest of the class"
                        ),
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
                            "✔️ Provide one-to-one private tuition for Junior College Mathematics and Primary School English, Mathematics and Science"
                        ),
                        className="p-indent",
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
