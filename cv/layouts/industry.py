from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.layouts.helper import accordian
from cv.layouts.industry_data import (  # industry_content_details,
    db_details,
    dbs_details,
    gic_details,
    kpmg_details,
    squarepoint_details,
)


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
                    [
                        squarepoint_details,
                        gic_details,
                        dbs_details,
                        kpmg_details,
                        db_details,
                    ],
                    value=["industry-sqp"],
                ),
                className="custom-div-instruction custom-div-left",
            ),
            # *industry_content_details,
        ]
    )
