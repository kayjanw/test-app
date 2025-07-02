import dash_mantine_components as dmc
from dash import html

from common.layouts.main import content_header
from main.layouts.about_me import about_me_component, about_me_links


def about_me_cv_tab(app):
    return html.Div(
        [
            content_header("About me"),
            html.Div(
                [
                    html.P(
                        dmc.Highlight(
                            "A highly motivated and growth-driven individual with strong interest in coding and people "
                            "management. Possesses strong analytical, reasoning and problem-solving skills. A forward "
                            "looking individual with outstanding communication, teamwork and ability to navigate in a "
                            "global environment.",
                            highlight=["growth-driven", "problem-solving skills"],
                            style={"fontSize": "inherit"},
                        ),
                    ),
                    about_me_component(
                        "code-editor",
                        "Languages",
                        "Python, Pyspark, SQL, KDB+/Q",
                    ),
                    about_me_component(
                        "wrench",
                        "Frameworks and Tools",
                        "Airflow, Kedro, MLflow, Docker, Jenkins, Kubernetes, OpenShift",
                    ),
                    about_me_component(
                        "bar-chart",
                        "Visualisation and Modeling",
                        "AMPL, ExtendSim, Tableau, QGIS",
                    ),
                    about_me_component(
                        "interview",
                        "Spoken Languages",
                        "English (native), Chinese (native), Cantonese (fluent)",
                    ),
                    html.Br(),
                    html.Br(),
                    html.P(
                        [
                            "This website is made with Python Dash, deployed using Gunicorn with Docker and hosted on "
                            "Fly.io.",
                        ]
                    ),
                    html.P(
                        [
                            "Easter egg: Try removing the '/cv' extension in the url!",
                        ]
                    ),
                    html.P(
                        [
                            about_me_links(
                                "linkedin",
                                "LinkedIn",
                                "https://www.linkedin.com/in/kayjan/",
                            ),
                            " / ",
                            about_me_links(
                                "github", "GitHub", "https://www.github.com/kayjan/"
                            ),
                            " / ",
                            about_me_links(
                                "woman-student",
                                "Google Scholar",
                                "https://scholar.google.com/citations?user=ClCErYgAAAAJ/",
                            ),
                            " / ",
                            about_me_links(
                                "newspaper",
                                "Medium Articles",
                                "https://kayjanwong.medium.com/",
                            ),
                            " / ",
                            about_me_links(
                                "package",
                                "bigtree Python Package",
                                "https://bigtree.readthedocs.io/",
                            ),
                            " / ",
                            about_me_links(
                                "robot",
                                "PickMe Telegram Bot",
                                "https://t.me/pickme_bot",
                            ),
                        ]
                    ),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ],
        className="div-with-image div-with-image-left medium-image",
    )
