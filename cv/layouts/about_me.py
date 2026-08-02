import dash_mantine_components as dmc
from dash import html

from common.layouts.about_me import about_me_component, about_me_links
from common.layouts.main import content_header


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
                        "Python, Pyspark, SQL, Bash, KDB+/Q",
                    ),
                    about_me_component(
                        "wrench",
                        "Frameworks and Tools",
                        "Airflow, Docker, Jenkins, Kedro, Kubernetes, MLflow, OpenShift, Prefect",
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
                                "openmoji:linkedin",
                                "LinkedIn",
                                "https://www.linkedin.com/in/kayjan/",
                            ),
                            about_me_links(
                                "openmoji:github",
                                "GitHub",
                                "https://www.github.com/kayjan/",
                            ),
                            about_me_links(
                                "academicons:google-scholar-square",
                                "Google Scholar",
                                "https://scholar.google.com/citations?user=ClCErYgAAAAJ/",
                            ),
                            about_me_links(
                                "lineicons:medium",
                                "Medium",
                                "https://kayjanwong.medium.com/",
                            ),
                            about_me_links(
                                "material-icon-theme:python",
                                "bigtree Python Package",
                                "https://bigtree.readthedocs.io/",
                            ),
                            about_me_links(
                                "logos:telegram",
                                "PickMe Telegram Bot",
                                "https://t.me/pickme_bot",
                                size=35,
                            ),
                        ]
                    ),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ],
    )
