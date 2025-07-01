from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.layouts.cv_data import (
    books_read_leisure,
    create_scrollable_area,
    professional_certs,
    skill_certs,
)

book_data = [
    (books_read_leisure, "Leisure"),
]


def certifications_tab(app):
    return html.Div(
        [
            content_header(
                "Certifications",
                [
                    DashIconify(icon="openmoji:trophy", height=40),
                    "Certs, skills, and side quests",
                ],
            ),
            html.Div(
                [
                    html.H5("Professional Certificates"),
                    create_scrollable_area(
                        professional_certs,
                        columns=["Course", "Organization", "Date"],
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.H5("Skill Certificates"),
                    create_scrollable_area(
                        skill_certs,
                        columns=["Course", "Organization", "Date"],
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
