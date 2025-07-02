from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.layouts.helper import accordian
from cv.layouts.teaching_data import (  # teaching_content_details,
    cristofori_details,
    dajin_details,
    ga_details,
    hei_details,
    nus_details,
    tutor_details,
    writing_details,
)


def teaching_tab(app):
    return html.Div(
        [
            content_header(
                "Teaching & Writing",
                [
                    DashIconify(icon="openmoji:beating-heart", height=40),
                    "Teaching is my way of learning twice",
                ],
            ),
            html.Div(
                accordian(
                    [
                        hei_details,
                        writing_details,
                        ga_details,
                        nus_details,
                        cristofori_details,
                        dajin_details,
                        tutor_details,
                    ]
                ),
                className="custom-div-instruction custom-div-left",
            ),
            # html.Div(
            #     teaching_content_details,
            #     className="custom-div-instruction custom-div-left",
            # ),
        ]
    )
