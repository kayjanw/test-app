from typing import List

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.layouts.achievements_data import coursera_ai, coursera_big_data, coursera_coding

table_kwargs = dict(
    withTableBorder=False,
    withColumnBorders=False,
    withRowBorders=False,
    highlightOnHover=True,
    horizontalSpacing="xs",
    verticalSpacing="xs",
    striped=False,
)


def create_scrollable_area(data: List[List[str]]):
    return dmc.TableScrollContainer(
        dmc.Table(children=create_coursera_table(data), **table_kwargs),
        maxHeight=400,
        minWidth=600,
        type="scrollarea",
    )


def create_coursera_table(data: List[List[str]]):
    return [
        html.Thead(
            html.Tr(
                [
                    html.Th("Course"),
                    html.Th("Organization"),
                    html.Th("Link"),
                ]
            )
        ),
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(course),
                        html.Td(organization),
                        html.Td(
                            html.A(
                                dmc.Button("Details", size="md"),
                                href=link,
                                target="_blank",
                            )
                        ),
                    ]
                )
                for course, organization, link in data
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
                                        "Artificial Intelligence",
                                        value="ai",
                                    ),
                                    dmc.TabsTab("Big Data", value="big_data"),
                                    dmc.TabsTab(
                                        "Coding Best Practices",
                                        value="coding",
                                    ),
                                    dmc.TabsTab("Data Science", value="Data Science"),
                                    dmc.TabsTab("Finance", value="Finance"),
                                    dmc.TabsTab(
                                        "Software Engineering",
                                        value="Software Engineering",
                                    ),
                                    dmc.TabsTab("Others", value="Others"),
                                ]
                            ),
                            dmc.TabsPanel(
                                html.Div(
                                    [
                                        html.Br(),
                                        create_scrollable_area(coursera_ai),
                                    ]
                                ),
                                value="ai",
                            ),
                            dmc.TabsPanel(
                                html.Div(
                                    [
                                        html.Br(),
                                        create_scrollable_area(coursera_big_data),
                                    ]
                                ),
                                value="big_data",
                            ),
                            dmc.TabsPanel(
                                html.Div(
                                    [
                                        html.Br(),
                                        create_scrollable_area(coursera_coding),
                                    ]
                                ),
                                value="coding",
                            ),
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
