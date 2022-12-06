import dash_leaflet as dl
from dash import dash_table, dcc, html

from components.helper import dcc_loading, table_css
from layouts.main import content_header


def trip_tab(app):
    return html.Div(
        [
            content_header("Trip Planner", "Optimize your route"),
            html.Div(
                [
                    html.P(
                        "Users can fill in multiple destinations and an optimal route based on distance will be "
                        "calculated, starting and ending from the first destination specified. "
                        "This is also known as the Travelling Salesman Problem"
                    ),
                    html.Br(),
                    html.P("Step 1: Fill in landmark name (optional)"),
                    html.P("Step 2: Click point on map corresponding to landmark name"),
                    html.P(
                        "Step 3: Repeat steps 1 and 2 until all destinations have been entered"
                    ),
                    html.P(
                        "Step 4: Name of landmark can be altered in the table. Try not to use the same landmark name"
                    ),
                    html.P(
                        'Step 5: Click "OK" button to generate shortest and fastest route!'
                    ),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P("Name of landmark:"),
                                    dcc.Input(
                                        id="input-trip-landmark",
                                        type="text",
                                        placeholder="i.e. Home, Work",
                                        style={"width": "50%"},
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            get_trip_table(),
                            html.Button(
                                "Remove last landmark", id="button-trip-remove"
                            ),
                            html.Button("Reset all landmarks", id="button-trip-reset"),
                            html.Br(),
                            html.Button("OK", id="button-trip-ok"),
                            dcc_loading(html.Div(id="trip-result"), dark_bg=True),
                        ],
                        className="custom-div-small custom-div-space-below custom-div-left custom-div-dark",
                    ),
                    html.Div(
                        [
                            html.P(
                                [
                                    html.Img(src=app.get_asset_url("info.svg")),
                                    html.Span("Scroll to zoom, drag to move"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            dl.Map(
                                id="map-trip",
                                style={
                                    "height": "400px",
                                },
                                center=[1.3521, 103.8198],
                                zoom=11,
                                children=[dl.TileLayer()],
                            ),
                        ],
                        className="custom-div-large custom-div-center",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
        ]
    )


def get_trip_table():
    """Return the table that displays landmarks information

    Returns:
        (dash_table.DataTable)
    """
    style_header, style_cell, style_table, css = table_css()
    return dash_table.DataTable(
        id="table-trip-landmark",
        columns=[
            dict(name="Landmark", id="Landmark", editable=True),
            dict(name="Street", id="Street"),
            dict(name="lat", id="lat"),
            dict(name="lon", id="lon"),
        ],
        data=[],
        style_as_list_view=True,
        style_header=style_header,
        style_cell_conditional=[
            {"if": {"column_id": c}, "display": "none"} for c in ["lat", "lon"]
        ],
        style_cell=style_cell,
        css=css,
    )
