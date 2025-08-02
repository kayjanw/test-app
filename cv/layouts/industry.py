from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.industry import industry_data, use_accordian
from cv.layouts.helper import accordian
from cv.model.accordian_row import convert_to_accordian, convert_to_list


def industry_tab(app):
    return html.Div(
        [
            content_header(
                "Quantitative Developer, Data Scientist",
                [
                    DashIconify(icon="openmoji:woman-technologist", height=40),
                    "I love all things math + coding",
                ],
            ),
            html.Div(
                accordian(
                    convert_to_accordian(industry_data),
                    value=["industry-sqp"],
                ),
                className="custom-div-instruction custom-div-left",
            )
            if use_accordian
            else html.Div(
                [convert_to_list(industry_row) for industry_row in industry_data]
            ),
        ]
    )
