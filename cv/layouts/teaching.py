from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.teaching import teaching_data  # teaching_content_data
from cv.layouts.helper import accordian


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
                accordian(teaching_data),
                className="custom-div-instruction custom-div-left",
            ),
            # html.Div(
            #     teaching_content_data,
            #     className="custom-div-instruction custom-div-left",
            # ),
        ]
    )
