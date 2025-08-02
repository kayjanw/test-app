from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.industry import industry_accordian_data  # industry_content_data
from cv.layouts.helper import accordian
from cv.model.accordian_row import convert_to_accordian


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
                    convert_to_accordian(industry_accordian_data),
                    value=["industry-sqp"],
                ),
                className="custom-div-instruction custom-div-left",
            ),
            # *industry_content_data,
        ]
    )
