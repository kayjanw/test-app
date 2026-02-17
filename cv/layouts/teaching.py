from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.teaching import teaching_accordian_data, teaching_data, use_accordian
from cv.model.accordian_row import accordian


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
                accordian(teaching_accordian_data),
                className="custom-div-instruction custom-div-left",
            )
            if use_accordian
            else html.Div(
                teaching_data,
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
