import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.education import coursera_data, datacamp_data
from cv.layouts.helper import create_scrollable_area


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
            html.Div(
                [
                    html.H5("Coursera, Online Courses"),
                    html.H6(
                        [
                            "133 Courses and 20 Specializations done to date. View my profile ",
                            html.A(
                                "here",
                                href="https://www.coursera.org/user/83789311d9e1811d14aa5fe139b5c6c6",
                                target="_blank",
                            ),
                        ]
                    ),
                    dmc.Tabs(
                        children=[
                            dmc.TabsList(
                                [
                                    dmc.TabsTab(
                                        course[1],
                                        value=course[1],
                                    )
                                    for course in coursera_data
                                ]
                            ),
                        ]
                        + [
                            dmc.TabsPanel(
                                html.Div(
                                    create_scrollable_area(
                                        course[0],
                                        columns=["Course", "Organization", "Link"],
                                    )
                                ),
                                value=course[1],
                            )
                            for course in coursera_data
                        ],
                        color="#202029",
                        variant="default",
                        radius="md",
                        orientation="horizontal",
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.H5("DataCamp, Online Courses"),
                    html.H6("29 Courses done to date"),
                    dmc.Tabs(
                        children=[
                            dmc.TabsList(
                                [
                                    dmc.TabsTab(
                                        course[1],
                                        value=course[1],
                                    )
                                    for course in datacamp_data
                                ]
                            ),
                        ]
                        + [
                            dmc.TabsPanel(
                                html.Div(
                                    create_scrollable_area(
                                        course[0],
                                        columns=["Course", "Type", "Link"],
                                    )
                                ),
                                value=course[1],
                            )
                            for course in datacamp_data
                        ],
                        color="#202029",
                        variant="default",
                        radius="md",
                        orientation="horizontal",
                    ),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
