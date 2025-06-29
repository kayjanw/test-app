from dash import html
from dash_iconify import DashIconify

from layouts.main_components import content_header


def education_tab(app):
    return html.Div(
        [
            content_header(
                "Education",
                [
                    DashIconify(icon="openmoji:school", height=40),
                    "Learning never stops",
                ],
            ),
            html.Div(
                [
                    html.H5("National University of Singapore (NUS)"),
                    html.H6("Master of Computing, Computer Science"),
                    html.P("GPA: 4.85 / 5.00, 4 out of 10 modules with A+"),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.H5("Singapore University of Technology and Design (SUTD)"),
                    html.H6(
                        "Bachelor of Engineering, Engineering Systems and Design (Financial Services)"
                    ),
                    html.P("Summa Cum Laude (Highest Distinction)"),
                    html.P(
                        ("✔️ Asian Leadership Programme Scholarship"),
                        className="p-indent",
                    ),
                    html.P(
                        ("✔️ Honours List for Freshmore Terms"),
                        className="p-indent",
                    ),
                    html.P(
                        (
                            "✔️ Top performing student for Financial Services focus track"
                        ),
                        className="p-indent",
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
