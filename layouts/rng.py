import dash_daq as daq
from dash import dcc, html
from mergedeep import merge

from components.helper import dcc_loading, flex_style
from layouts.main import content_header, style_hidden


def rng_tab():
    return html.Div(
        [
            content_header("Random Generator", "Generate random selection or groups"),
            html.Div(
                [
                    html.P(
                        "Users can perform random selection of items or grouping of items"
                    ),
                    html.Br(),
                    html.P("Step 1: Fill in the text box with items"),
                    html.P("Step 2: Specify type of task accordingly"),
                    html.P('Step 3: Click "OK" button to generate results!'),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Item List:", className="p-bold"),
                            dcc.Textarea(
                                id="input-rng",
                                value="Item A\nItem B\nItem C\nItem D",
                                placeholder="Insert item here",
                            ),
                            html.P(
                                ["Task:"],
                                className="p-bold",
                                style={
                                    "margin-top": "20px",
                                    "margin-bottom": 0,
                                },
                            ),
                            html.Div(
                                [
                                    html.P("Select N items", className="p-short"),
                                    daq.ToggleSwitch(
                                        id="toggle-rng",
                                        value=False,
                                        color="rgb(190, 155, 137)",
                                        className="custom-div-inline custom-margin-left custom-margin-right",
                                    ),
                                    html.P("Split into N groups", className="p-short"),
                                ]
                            ),
                            html.Div(
                                [
                                    html.P("Number of items:"),
                                    dcc.Input(
                                        id="input-rng-item",
                                        type="number",
                                        value=1,
                                        min=1,
                                        style={
                                            "width": "40%",
                                        },
                                    ),
                                ],
                                id="div-rng-item",
                                className="custom-div-flex custom-margin-top",
                                style=merge(
                                    {
                                        "display": "none",
                                        "margin": 0,
                                    },
                                    flex_style,
                                ),
                            ),
                            html.Div(
                                [
                                    html.P("Number of groups:"),
                                    dcc.Input(
                                        id="input-rng-group",
                                        type="number",
                                        value=2,
                                        min=2,
                                        style={
                                            "width": "40%",
                                        },
                                    ),
                                ],
                                id="div-rng-group",
                                className="custom-div-flex custom-margin-top",
                                style={
                                    "display": "none",
                                    "margin": 0,
                                },
                            ),
                            html.Button("OK", id="button-rng-ok"),
                            dcc_loading(
                                [html.P(id="rng-result-error", className="color-red")],
                                dark_bg=True,
                            ),
                        ],
                        className="custom-div-small-medium custom-div-space-below custom-div-left custom-div-dark",
                    ),
                    # Result
                    html.Div(
                        id="div-rng-result",
                        style=style_hidden,
                        className="custom-div-small-medium custom-div-space-below custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above",
            ),
        ]
    )
