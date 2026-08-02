from dash import html

from common.layouts.about_me import about_me_component, about_me_links
from common.layouts.main import content_header


def about_me_audio():
    """Audio component for about-me tab (WIP)

    Returns:
        (html.Audio)
    """
    return (
        html.Audio(
            src="https://www.youtube.com/embed/kgx4WGK0oNU",
            autoPlay=True,
        ),
    )


def about_me_tab(app):
    return html.Div(
        [
            content_header("About me"),
            html.Div(
                [
                    html.P(
                        "Just someone who loves coding, and believes coding should make our lives easier."
                    ),
                    about_me_component(
                        "bar-chart",
                        "Data Analytics",
                        "Visualize results graphically using uploaded data",
                    ),
                    about_me_component(
                        "chart-increasing",
                        "Optimization",
                        "Solve computationally expensive math problems",
                    ),
                    about_me_component(
                        "brain",
                        "Prediction",
                        "Use machine learning methods to churn out predictions",
                    ),
                    about_me_component(
                        "party-popper",
                        "Fun Things",
                        "Plan events and play games!",
                    ),
                    html.Br(),
                    html.Br(),
                    html.P(
                        "Feel free to write in for any UI/UX suggestion, functionality idea, "
                        "new use case or bugs encountered!"
                    ),
                    html.P(
                        [
                            "This website is made with Python Dash, deployed using Gunicorn with Docker and hosted on "
                            "GCP/Fly.io, view code documentation on Sphinx ",
                            html.A(
                                "here",
                                href="http://kayjan.readthedocs.io",
                                target="_blank",
                            ),
                            ".",
                        ]
                    ),
                    html.P(
                        [
                            about_me_links(
                                "solar:suitcase-bold",
                                "Formal Website",
                                "https://kayjan.fly.dev/cv",
                                size=35,
                            ),
                            about_me_links(
                                "material-icon-theme:github-sponsors",
                                "Support Me!",
                                "https://buymeacoffee.com/kayjan",
                                size=35,
                            ),
                        ]
                    ),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ],
        className="div-with-image div-with-image-left medium-image",
    )
