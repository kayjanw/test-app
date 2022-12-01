from dash import html

from layouts.main import content_header


def sample_tab():
    return html.Div(
        [
            content_header("Header", "Subheader"),
            html.Div([
                html.P("Description"),
                html.Br(),
                html.P("Step 1: "),
                html.P("Step 2: "),
            ],
                className="custom-div-instruction custom-div-left"
            ),
            html.Div(
                [
                    # html.P('Left component',),
                ],
                className="custom-div-instruction2 custom-div-left custom-div-dark"
            ),
            html.Div(
                [
                    # Left item
                    html.Div(
                        [
                            # html.P('Left component',),
                        ],
                        className="custom-div-small custom-div-left custom-div-dark",
                    ),
                    # Right item
                    html.Div(
                        [
                            # html.P('Right component')
                        ],
                        className="custom-div-large custom-div-center",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
        ]
    )
