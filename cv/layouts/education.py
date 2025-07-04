import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.education import coursera_data, datacamp_data
from cv.layouts.helper import bullet_point, create_scrollable_area


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
                    html.H6(
                        "Master of Computing, Computer Science", className="p-bold"
                    ),
                    html.P("GPA: 4.85 / 5.00, 4 out of 10 modules with A+"),
                    html.Br(),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.H5("Singapore University of Technology and Design (SUTD)"),
                    html.H6(
                        "Bachelor of Engineering, Engineering Systems and Design (Financial Services)",
                        className="p-bold",
                    ),
                    html.P("Summa Cum Laude (Highest Distinction)"),
                    html.Div(
                        [
                            bullet_point(
                                "🎖️️️", "Asian Leadership Programme Scholarship"
                            ),
                            bullet_point("🎖️️️️", "Honours List for Freshmore Terms"),
                            bullet_point(
                                "🎖️️️️",
                                "Top performing student for Financial Services focus track",
                            ),
                            bullet_point(
                                "✔️",
                                "Represented College in CFA Institute Research Challenge (Season 2017-2018)",
                            ),
                        ],
                        className="p-indent",
                    ),
                    html.P("Clubs and Societies"),
                    html.Div(
                        [
                            bullet_point(
                                "🎀",
                                "Vertex Cheerleading, President, Team Manager, and Treasurer | May 2015 - Jun 2017",
                            ),
                            bullet_point(
                                "🎹",
                                "Bands, Performer, Publicity and Decor Executive | May 2015 - Nov 2016",
                            ),
                            bullet_point(
                                "💼",
                                "Startups (Entrepreneurship Club), Public Relations Head | Sep 2016 - Dec 2016",
                            ),
                            bullet_point(
                                "🎪",
                                "Sports Core (Sports Club), Events Executive | Oct 2016 - Mar 2017",
                            ),
                            bullet_point(
                                "🏈",
                                "Touch Rugby, Competitive Member | Jun 2015 - Sep 2018",
                            ),
                            bullet_point(
                                "☄️",
                                "Tchoukball, Competitive Member | Jun 2015 - Nov 2015",
                            ),
                            bullet_point(
                                "🏀",
                                "Basketball, Member | May 2018 - Sep 2018",
                            ),
                        ],
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
