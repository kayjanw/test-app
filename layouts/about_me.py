from dash import html

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
                            html.Img(src=app.get_asset_url("data-analytics.svg")),
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
                            html.Img(src=app.get_asset_url("optimization.svg")),
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
                            html.Img(src=app.get_asset_url("prediction.svg")),
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
                            html.Img(src=app.get_asset_url("event.png")),
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
                        [
                            "Check out my ",
                            html.A(
                                "linkedin",
                                href="https://www.linkedin.com/in/kayjan/",
                                target="_blank",
                            ),
                            " / ",
                            html.A(
                                "formal website",
                                href="http://kayjan.github.io/",
                                target="_blank",
                            ),
                            " / ",
                            html.A(
                                "Medium articles",
                                href="https://kayjanwong.medium.com/",
                                target="_blank",
                            ),
                            " / ",
                            html.A(
                                "bigtree Python Package",
                                href="https://bigtree.readthedocs.io/",
                                target="_blank",
                            ),
                            ".",
                        ]
                    ),
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
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ],
        className="div-with-image div-with-image-left medium-image",
    )
