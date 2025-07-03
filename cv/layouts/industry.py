from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.industry import industry_data  # industry_content_data
from cv.layouts.helper import accordian


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
                    industry_data,
                    value=["industry-sqp"],
                ),
                className="custom-div-instruction custom-div-left",
            ),
            # *industry_content_data,
        ]
    )
