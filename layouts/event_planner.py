from dash import html, dcc

from components.helper import result_download_text, dcc_loading
from layouts.main import content_header, style_checklist, style_hidden


def event_tab(app):
    return html.Div(
        [
            content_header("Event Planner", "Generate random matches and groups"),
            html.Div(
                [
                    html.P(
                        "Users can perform random matching of people with customized criterias and/or split "
                        "participants into groups. Criteria can be customized to be individual-level or group-level "
                        "and results can be toggled to show/hide from web-page or emailed to participants separately. "
                        "Usage include"
                    ),
                    html.P(
                        [
                            "• ",
                            html.P("Team Activity", className="p-short p-bold"),
                            ": Split team into multiple groups and specify criteria for activity such as location!"
                        ],
                        style={
                            "padding-left": "20px"
                        }
                    ),
                    html.P(
                        [
                            "• ",
                            html.P("Secret Santa", className="p-short p-bold"),
                            ": Organize gift exchange and specify criteria for gift such as colour or texture of gift!"
                        ],
                        style={
                            "padding-left": "20px"
                        }
                    ),
                    html.Br(),
                    html.P(
                        [
                            "Step 1: Download demo worksheet ",
                            result_download_text("here"),
                            " and fill in the values. Do not change items in ",
                            html.P("red", style={"color": "red"}, className="p-short p-bold")
                        ]
                    ),
                    html.P(
                        "Step 2: Upload completed worksheet, a message will appear to indicate if file is uploaded "
                        "successfully"),
                    html.P(
                        "Step 3: Specify number of groups to split participants into and other options accordingly"
                    ),
                    html.P('Step 4: Click "OK" button to generate results!'),
                ],
                className="custom-div-instruction custom-div-left"
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Upload(
                                [
                                    html.Img(src=app.get_asset_url("upload.svg")),
                                    html.Span(
                                        "Drag and drop file here, or click to upload"
                                    ),
                                ],
                                id="upload-event",
                                multiple=False,
                                className="div-with-image div-with-image-left small-image image-dark-bg",
                            ),
                            html.P(id="text-event-confirm"),
                            html.Div(
                                [
                                    html.P("Select number of groups:"),
                                    html.P(
                                        [
                                            dcc.Input(
                                                id="input-event-group",
                                                type="number",
                                                value=1,
                                                min=1,
                                                style=style_checklist,
                                            ),
                                        ]
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P(
                                        [
                                            dcc.Checklist(
                                                id="checklist-event-pair",
                                                options=[
                                                    {
                                                        "label": "Pair participants up (i.e. for gift exchange)",
                                                        "value": "pair",
                                                    }
                                                ],
                                                value=["pair"],
                                                style=style_checklist,
                                            )
                                        ]
                                    ),
                                    html.P(
                                        [
                                            "Criteria should unique to",
                                            dcc.RadioItems(
                                                id="radio-event-criteria",
                                                options=[
                                                    {
                                                        "label": "individual",
                                                        "value": "individual",
                                                    },
                                                    {
                                                        "label": "group",
                                                        "value": "group",
                                                    }
                                                ],
                                                value="individual",
                                                style={
                                                    "display": "flex"
                                                }
                                            )
                                        ],
                                        className="custom-div-flex"
                                    ),
                                    html.P(
                                        [
                                            dcc.Checklist(
                                                id="checklist-event-email",
                                                options=[
                                                    {
                                                        "label": "Email individual results to recipients separately",
                                                        "value": "email",
                                                    }
                                                ],
                                                style=style_checklist,
                                            )
                                        ]
                                    ),
                                    html.P(
                                        [
                                            dcc.Checklist(
                                                id="checklist-event-display",
                                                options=[
                                                    {
                                                        "label": "Hide results",
                                                        "value": "hide",
                                                    }
                                                ],
                                                style=style_checklist,
                                            )
                                        ]
                                    )
                                ]
                            ),
                            html.Br(),
                            html.Button("OK", id="button-event-ok"),
                            dcc.Store(
                                id="intermediate-event-result", storage_type="memory"
                            ),
                            dcc_loading([html.P(id="event-result-error")], dark_bg=True),
                        ],
                        className="custom-div-small-medium custom-div-space-below custom-div-left custom-div-dark"
                    ),
                    html.Div(
                        id="div-event-result",
                        style=style_hidden,
                        className="custom-div-small-medium custom-div-space-below custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above",
            ),
        ]
    )
