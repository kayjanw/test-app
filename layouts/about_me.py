from dash import html
from dash_iconify import DashIconify

from layouts.main import content_header


def about_me_component(icon_name: str, component_name: str, component_description: str):
    """Component for about-me tab

    Args:
        icon_name (str): component icon
        component_name (str): component title
        component_description (str): component description

    Returns:
        (html.Div)
    """
    return html.Div(
        [
            DashIconify(icon=f"openmoji:{icon_name}", height=40),
            html.P(component_name, className="p-short p-bold"),
            html.P(f": {component_description}", className="p-short"),
        ],
        className="custom-div-small-space-below",
    )


def about_me_links(icon_name: str, link_title: str, link_url: str):
    """Link component for about-me tab

    Args:
        icon_name (str): link icon
        link_title (str): link title
        link_url (str): link URL

    Returns:
        (html.Span)
    """
    return html.Span(
        html.A(
            [
                DashIconify(icon=f"openmoji:{icon_name}", height=40),
                link_title,
            ],
            href=link_url,
            target="_blank",
        ),
        title=link_title,
    )


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
                                "chrome", "Formal Website", "http://kayjan.github.io/"
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
