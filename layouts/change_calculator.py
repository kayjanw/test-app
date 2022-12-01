from dash import html, dcc, dash_table

from components.helper import dcc_loading, table_css
from layouts.main import content_header, style_dropdown, style_hidden, style_input


def change_tab(app):
    return html.Div(
        [
            content_header("Change Calculator", "Compare changes over two periods"),
            html.Div(
                [
                    html.P(
                        "Users can view summary statistics and plot a scatterplot with marginal histograms of past "
                        "values (x axis) against present values (y axis). Users also have the option to download "
                        "processed results with change value into an excel file"
                    ),
                    html.Br(),
                    html.P("Step 1: Upload a file (.csv, .xls, .xlsx with multiple worksheets supported), "
                           "sample of file will be displayed once upload is successful"),
                    html.P("Step 2: Specify columns for past values (x axis) and present values (y axis)"),
                    html.P("Step 3: Specify maximum possible value for each column to normalize column values "
                           "(optional)"),
                    html.P('Step 4: Click "OK" button to generate results!'),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Upload(
                                [
                                    html.Img(src=app.get_asset_url("upload.svg")),
                                    html.Span("Drag and drop file here, or click to upload"),
                                ],
                                id="upload-change",
                                multiple=False,
                                className="div-with-image div-with-image-left small-image image-dark-bg",
                            ),
                            html.Div(
                                [
                                    html.P("Select worksheet:"),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-change-worksheet",
                                                placeholder="Select worksheet",
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style={"width": "40%"},
                                    ),
                                ],
                                id="change-select-worksheet",
                                className="custom-div-flex",
                                style=style_hidden,
                            ),
                            html.Div(
                                id="change-sample-data",
                                className="custom-div-small-space-below",
                            ),
                            html.Div(
                                [
                                    html.P("Select x-axis:"),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-change-x",
                                                placeholder="Select column",
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style=style_input,
                                    ),
                                    html.P("out of"),
                                    dcc.Input(id="input-change-x", type="number", min=1, style={"width": "20%"}),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Select y-axis:"),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-change-y",
                                                placeholder="Select column",
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style=style_input,
                                    ),
                                    html.P("out of"),
                                    dcc.Input(id="input-change-y", type="number", min=1, style={"width": "20%"}),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Button("OK", id="button-change-ok"),
                            dcc.Store(id="intermediate-change-result", storage_type="memory"),
                            dcc_loading(html.P(id="change-result-error"), dark_bg=True),
                        ],
                        className="custom-div-small-medium custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
            html.Div(
                [
                    html.Div(
                        id="change-result",
                        className="custom-div-small custom-div-space-below custom-div-left custom-div-white image-dark-bg"
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src=app.get_asset_url("info.svg")),
                                    html.Span(
                                        "Mouseover for information, highlight to zoom, double click to reset view"),
                                    html.Span(dcc.Graph(id="graph-change-result"), className="custom-div-large-full"),
                                ],
                                className="custom-div-full custom-div-center div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.P("Footnote:"),
                                    html.P(
                                        "1. Computation ignores rows where either x or y value is not in numerical "
                                        "format"),
                                    html.P(
                                        "2. Points will be very close to each other (but not overlapping) if two rows "
                                        "have identical x and y values, it is recommended to zoom or download the "
                                        "results file"),
                                    html.P("3. Interpreting the scatterplot above:"),
                                    html.P("• Points above the line represent positive change",
                                           style={"margin-left": "10px"}),
                                    html.P("• Distance from the line represent magnitude of change",
                                           style={"margin-left": "10px"}),
                                    html.P("4. Interpreting the histogram above:"),
                                    html.P("• Histogram shows the distribution of values for x and y axis respectively",
                                           style={"margin-left": "10px"}),
                                    html.P("5. Interpreting the summary statistics on the left:"),
                                    html.P(
                                        "• If median is higher than mean: data is skewed to the left; there is a long "
                                        "tail of low scores pulling the mean down", style={"margin-left": "10px"}),
                                ],
                            ),
                        ],
                        className="custom-div-large custom-div-left custom-div-white"
                    ),
                ],
                id="div-change-result",
                className="custom-container custom-div-space-below",
                style=style_hidden,
            ),
        ]
    )


def get_changes_table():
    """Return the table used to compare changes across multiple periods

    Returns:
        (dash_table.DataTable)
    """
    style_header, style_cell, style_table, css = table_css()
    return dash_table.DataTable(
        id="table-changes",
        columns=[
            dict(name="Columns to compare", id="column", presentation="dropdown"),
            dict(name="Maximum possible value (integer value, optional)", id="max", type="numeric",
                 on_change={"failure": "default"}),
        ],
        data=[dict(column="", max="") for i in range(4)],
        editable=True,
        style_as_list_view=True,
        style_header=style_header,
        style_cell=style_cell,
        style_table=style_table,
        css=css,
    )


def changes_tab(app):
    return html.Div(
        [
            content_header("Change Calculator 2", "Compare changes over multiple periods"),
            html.Div([
                html.P("Users can view summary statistics in table and box plot, and changes over time on a line plot. "
                       "Just minor changes from the other change tab (haha)"),
                html.Br(),
                html.P("Step 1: Upload a file (.csv, .xls, .xlsx with multiple worksheets supported), "
                       "sample of file will be displayed once upload is successful"),
                html.P("Step 2: Specify column identifier in dropdown option, and columns to compare in the table"),
                html.P(
                    "Step 3: Specify maximum possible value for each column to normalize the column values "
                    "(optional)"),
                html.P('Step 4: Click "OK" button to generate results!'),
                html.Br(),
                html.P("Footnote:"),
                html.P("1. Computation ignores rows where any column comparison values are not in numerical format"),
                html.P("2. Computation ignores rows where column identifier values are empty"),
                html.P(
                    "3. Ensure all column identifier values are unique, if not it will be replaced with running "
                    "numbers"),
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
                                    html.Span("Drag and drop file here, or click to upload"),
                                ],
                                id="upload-changes",
                                multiple=False,
                                className="div-with-image div-with-image-left small-image image-dark-bg",
                            ),
                            html.Div(
                                [
                                    html.P("Select worksheet:"),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-changes-worksheet",
                                                placeholder="Select worksheet",
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style={"width": "40%"},
                                    ),
                                ],
                                id="changes-select-worksheet",
                                className="custom-div-flex",
                                style=style_hidden,
                            ),
                            html.Div(
                                id="changes-sample-data",
                                className="custom-div-small-space-below"
                            ),
                            dcc.Store(id="intermediate-changes-result", storage_type="memory"),
                            html.Div(
                                [
                                    html.P("Column identifier (i.e. Name):"),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-changes-identifier",
                                                placeholder="Select column",
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style=style_input,
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            get_changes_table(),
                            html.Button("Add rows", id="button-changes-add"),
                            html.Button("OK", id="button-changes-ok"),
                            dcc_loading([html.P(id="changes-result-error")], dark_bg=True),
                        ],
                        className="custom-div-small-medium custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P(id="changes-result", className="custom-div-small custom-div-left custom-div-white"),
                            html.Div(
                                [
                                    html.P(
                                        [
                                            html.Img(src=app.get_asset_url("info.svg")),
                                            html.Span(
                                                "Hover over box to see more information"
                                            ),
                                            html.Span(
                                                "Single click on legend to "
                                                "hide entry, double click on legend to highlight entry"
                                            ),
                                        ],
                                        className="div-with-image div-with-image-left small-image image-dark-bg"
                                    ),
                                    dcc.Graph(id="graph-changes-boxplot")
                                ],
                                className="custom-div-large custom-div-center custom-div-white",
                            ),
                        ],
                        className="custom-container custom-div-center custom-div-dark"
                    ),
                    html.P(
                        id="graph-changes-result",
                        className="custom-div-full custom-div-space-above custom-div-center "
                                  "div-with-image div-with-image-left small-image",
                    ),
                ],
                id="div-changes-result",
                className="custom-container custom-div-space-below",
                style=style_hidden,
            ),
        ]
    )
