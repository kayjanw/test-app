from dash import html
from dash_iconify import DashIconify

from layouts.main import content_header


def about_me_tab(app):
    return html.Div(
        [
            content_header("About me"),
            html.Div(
                [
                    html.P(
                        "Just someone who loves coding, and believes coding should make our lives easier."
                    ),
                    html.Div(
                        [
                            DashIconify(icon="openmoji:bar-chart", height=40),
                            html.P("Data Analytics", className="p-short p-bold"),
                            html.P(
                                ": Using uploaded data, visualize results graphically",
                                className="p-short",
                            ),
                        ],
                        className="custom-div-small-space-below",
                    ),
                    html.Div(
                        [
                            DashIconify(icon="openmoji:chart-increasing", height=40),
                            html.P("Optimization", className="p-short p-bold"),
                            html.P(
                                ": Solve computationally expensive math problems",
                                className="p-short",
                            ),
                        ],
                        className="custom-div-small-space-below",
                    ),
                    html.Div(
                        [
                            DashIconify(icon="openmoji:brain", height=40),
                            html.P("Prediction", className="p-short p-bold"),
                            html.P(
                                ": Use machine learning methods to churn out predictions",
                                className="p-short",
                            ),
                        ],
                        className="custom-div-small-space-below",
                    ),
                    html.Div(
                        [
                            DashIconify(icon="openmoji:party-popper", height=40),
                            html.P("Fun Things", className="p-short p-bold"),
                            html.P(
                                ": Plan events and play games!", className="p-short"
                            ),
                        ],
                        className="custom-div-small-space-below",
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
                            html.Span(
                                html.A(
                                    [
                                        DashIconify(
                                            icon="openmoji:linkedin", height=40
                                        ),
                                        "LinkedIn",
                                    ],
                                    href="https://www.linkedin.com/in/kayjan/",
                                    target="_blank",
                                ),
                                title="LinkedIn",
                            ),
                            " / ",
                            html.Span(
                                html.A(
                                    [
                                        DashIconify(icon="openmoji:github", height=40),
                                        "GitHub",
                                    ],
                                    href="https://www.github.com/kayjan/",
                                    target="_blank",
                                ),
                                title="GitHub",
                            ),
                            " / ",
                            html.Span(
                                html.A(
                                    [
                                        DashIconify(icon="openmoji:chrome", height=40),
                                        "Formal Website",
                                    ],
                                    href="http://kayjan.github.io/",
                                    target="_blank",
                                ),
                                title="Formal Website",
                            ),
                            " / ",
                            html.Span(
                                html.A(
                                    [
                                        DashIconify(
                                            icon="openmoji:newspaper", height=40
                                        ),
                                        "Medium Articles",
                                    ],
                                    href="https://kayjanwong.medium.com/",
                                    target="_blank",
                                ),
                                title="Medium Articles",
                            ),
                            " / ",
                            html.Span(
                                html.A(
                                    [
                                        DashIconify(icon="openmoji:package", height=40),
                                        "bigtree Python Package",
                                    ],
                                    href="https://bigtree.readthedocs.io/",
                                    target="_blank",
                                ),
                                title="bigtree Python Package",
                            ),
                        ]
                    ),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ],
        className="div-with-image div-with-image-left medium-image",
    )
