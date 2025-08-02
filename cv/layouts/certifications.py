from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.certifications import convert_to_table, professional_certs, skill_certs
from cv.layouts.helper import create_scrollable_area


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
                        convert_to_table(professional_certs),
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
                        convert_to_table(skill_certs),
                        columns=["Course", "Organization", "Date"],
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
