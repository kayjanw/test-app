import dash_daq as daq
from dash import dcc, html
from dash_canvas import DashCanvas

from layouts.main import content_header


def image_edit_tab(app):
    return html.Div(
        [
            content_header("Image Editing", "Draw on images"),
            html.Div(
                [
                    html.P(
                        "Users can edit images directly by drawing on them, or just draw on a blank canvas!"
                    ),
                    html.Br(),
                    html.P("Step 1: Upload an image (optional)"),
                    html.P("Step 2: Start drawing!"),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    # Left item
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Upload(
                                        [
                                            html.Img(
                                                src=app.get_asset_url("upload.svg")
                                            ),
                                            html.Span(
                                                "Drag and drop image here, or click to upload"
                                            ),
                                        ],
                                        id="upload-image",
                                        multiple=False,
                                    ),
                                ],
                                id="div-image-input",
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Br(),
                            html.Div(
                                [
                                    DashCanvas(
                                        id="image-canvas",
                                        width=600,
                                        height=400,
                                        goButtonTitle="Save",
                                        hide_buttons=[
                                            "zoom",
                                            "line",
                                            "rectangle",
                                            "select",
                                        ],
                                    ),
                                    html.Button(
                                        "clear",
                                        id="button-canvas-clear",
                                        style={
                                            "float": "right",
                                            "transform": "translateY(-58px)",
                                        },
                                    ),
                                ],
                                id="div-image-output",
                            ),
                        ],
                        className="custom-div-large custom-div-left custom-div-dark",
                    ),
                    # Right item
                    html.Div(
                        [
                            html.P("Brush width"),
                            daq.Knob(id="knob-canvas", min=2, max=40, value=5),
                            html.Button(
                                html.P("-", style={"font-size": "2em"}),
                                id="button-image-minus",
                                style={
                                    "display": "inline-block",
                                    "margin": 0,
                                    "margin-right": "10px",
                                    "transform": "translateY(-50px)",
                                },
                            ),
                            html.Button(
                                html.P("+", style={"font-size": "2em"}),
                                id="button-image-plus",
                                style={
                                    "display": "inline-block",
                                    "margin": 0,
                                    "transform": "translateY(-50px)",
                                },
                            ),
                            html.P("Brush colour"),
                            daq.ColorPicker(
                                id="image-color-picker",
                                label=" ",
                                value=dict(hex="#119DFF"),
                                style={"border": "none", "overflow": "hidden"},
                            ),
                        ],
                        className="custom-div-smaller custom-div-center",
                    ),
                    # Bottom item
                    html.Div(id="image-result"),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
        ]
    )
