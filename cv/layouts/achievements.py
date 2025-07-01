from typing import List

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.layouts.achievements_data import (
    coursera_ai,
    coursera_big_data,
    coursera_coding,
    coursera_ds,
    coursera_finance,
    coursera_others,
    coursera_se,
    datacamp_ds,
)

coursera_data = [
    (coursera_ai, "Artificial Intelligence"),
    (coursera_big_data, "Big Data"),
    (coursera_coding, "Coding Best Practices"),
    (coursera_ds, "Data Science"),
    (coursera_finance, "Finance"),
    (coursera_se, "Software Engineering"),
    (coursera_others, "Others"),
]

datacamp_data = [
    (datacamp_ds, "Data Science"),
]


def create_scrollable_area(data: List[List[str]], columns: List[str]):
    table_kwargs = dict(
        withTableBorder=False,
        withColumnBorders=False,
        withRowBorders=False,
        highlightOnHover=True,
        horizontalSpacing="xs",
        verticalSpacing="xs",
        striped=False,
    )
    return dmc.TableScrollContainer(
        dmc.Table(children=create_course_table(data, columns), **table_kwargs),
        maxHeight=400,
        minWidth=600,
        type="scrollarea",
    )


def create_course_table(data: List[List[str]], columns: List[str]):
    return [
        html.Thead(html.Tr([html.Th(col) for col in columns])),
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(course),
                        html.Td(details),
                        html.Td(
                            html.A(
                                dmc.Button("Details", size="md"),
                                href=link,
                                target="_blank",
                            )
                        ),
                    ]
                )
                for course, details, link in data
            ]
        ),
    ]


def achievement_tab(app):
    return html.Div(
        [
            content_header(
                "Achievements",
                [
                    DashIconify(icon="openmoji:trophy", height=40),
                    "Awards, Hobbies, Interests",
                ],
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
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    dmc.Tabs(
                        id="achievements-tab",
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
                ]
            ),
            html.Div(
                [
                    html.H5("DataCamp, Online Courses"),
                    html.H6("29 Courses done to date"),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    dmc.Tabs(
                        id="achievements-tab",
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
                ]
            ),
        ]
    )
