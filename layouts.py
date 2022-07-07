import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_leaflet as dl
import datetime

from dash import dash_table, dcc, html
from dash_canvas import DashCanvas

from components.helper import (
    colour_palette,
    violin_plot,
    dcc_loading,
    table_css,
    encode_dict,
    result_download_text,
)
from components.trade import Trade
from components.wnrs import WNRS
from version import __version__


style_dropdown = {"width": "100%", "color": "black"}
style_p = {"width": "40%"}
style_input = {"width": "35%"}
style_checklist = {"width": "100%"}
style_wnrs_text = {"margin-top": "20px"}
style_contact_textarea = {"width": "70%", "margin-bottom": "5px"}
style_hidden = {"display": "none"}


def main_layout():
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content"),
            html.Div(id="blank-output"),
            html.P(
                [
                    "If you like this, ",
                    html.A("buy me a coffee ☕ ", href="https://www.buymeacoffee.com/kayjan", target="_blank"),
                    "! ",
                    html.H6(f"(v{__version__})"),
                ],
                className="footer"),
        ]
    )


def banner():
    return html.Div(
        [
            html.Button("☰", id="button-sidebar"),
            html.Div(html.H1(dcc.Link("KJ Wong", href="/")))
        ]
    )


def sidebar_header():
    return html.Div(html.H1(dcc.Link("KJ Wong", href="/")))


def sidebar_dropdown():
    return html.Div(
        [
            dcc.Tabs(
                id="tabs-parent",
                value=None,
                vertical=True,
                parent_className="custom-tabs-parent",
                className="custom-tabs",
                children=[
                    dcc.Tab(label="About Me", value="tab-aboutme", className="custom-tab", selected_className="custom-tab-selected"),
                    dcc.Tab(label="Data Analytics", value="", className="custom-tab-disabled", disabled=True),
                    dcc.Tab(label="Change Calculator", value="tab-change", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    dcc.Tab(label="Change Calculator 2", value="tab-change2", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    dcc.Tab(label="Chat Analyzer", value="tab-chat", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    dcc.Tab(label="Optimization", value="", className="custom-tab-disabled",disabled=True),
                    dcc.Tab(label="Trip Planner", value="tab-trip", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    dcc.Tab(label="Prediction", value="", className="custom-tab-disabled", disabled=True),
                    dcc.Tab(label="MBTI Personality Test", value="tab-mbti", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    # dcc.Tab(label="Live Trading", value="tab-trade", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    dcc.Tab(label="Go to events!", value="tab-others", className="custom-tab"),
                    dcc.Tab(label="Contact Me", value="tab-contact", className="custom-tab", selected_className="custom-tab-selected"),
                    # dcc.Tab(label='Image Editing', value='tab-image', className='custom-tab', selected_className='custom-tab-selected')
                ],
                colors={"background": colour_palette["deep_blue"]},
                persistence=True,
                persistence_type="memory",
            )
        ]
    )


def sidebar_dropdown_event():
    return html.Div(
        [
            dcc.Tabs(
                id="tabs-parent",
                value=None,
                vertical=True,
                parent_className="custom-tabs-parent",
                className="custom-tabs",
                children=[
                    dcc.Tab(label="About Me", value="tab-aboutme", className="custom-tab", selected_className="custom-tab-selected"),
                    dcc.Tab(label="Fun Things", value="", className="custom-tab-disabled", disabled=True),
                    dcc.Tab(label="Event Planner", value="tab-event", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    dcc.Tab(label="Random Generator", value="tab-rng", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    dcc.Tab(label="We're Not Really Strangers", value="tab-wnrs", className="custom-tab-sub", selected_className="custom-tab-selected"),
                    dcc.Tab( label="Contact Me", value="tab-contact", className="custom-tab", selected_className="custom-tab-selected"),
                ],
                colors={"background": colour_palette["deep_blue"]},
                persistence=True,
                persistence_type="memory",
            )
        ]
    )


def app_1():
    return html.Div(
        [
            # Top contents
            html.Div(banner(), id="banner"),
            # Left contents
            html.Div(
                [
                    sidebar_header(),
                    sidebar_dropdown()
                ],
                id="sidebar"
            ),
            # Right contents
            html.Div(dcc_loading(violin_plot(), dark_bg=False), id="tab-content"),
        ]
    )


def app_2(pathname):
    return html.Div(
        [
            # Top contents
            html.Div(banner(), id="banner"),
            # Left contents
            html.Div(
                [
                    sidebar_header(),
                    dcc.Tabs(id="tabs-parent")
                ],
                id="sidebar"
            ),
            # Right contents
            html.Div(
                [
                    content_header("Nice try", "Sadly this page does not exist"),
                    html.Div([
                        html.P(
                            [
                                f"What were you hoping for in {pathname} page?",
                                html.Br(),
                                "Click ",
                                html.A("here", href="/"),
                                " to return to home page",
                            ]
                        ),
                    ],
                        className="custom-div-instruction"
                    )
                ],
                id="tab-content")
        ]
    )


def app_event():
    return html.Div(
        [
            # Top contents
            html.Div(banner(), id="banner"),
            # Left contents
            html.Div(
                [
                    sidebar_header(),
                    sidebar_dropdown_event()
                ],
                id="sidebar",
            ),
            # Right contents
            html.Div(dcc_loading(violin_plot(), dark_bg=False), id="tab-content"),
        ]
    )


def content_header(title, subtitle=None):
    return html.Div(
        [
            html.H2(title, className="content-header"),
            html.H3(subtitle),
            html.H4("————————"),
        ]
    )


def about_me_tab(app):
    return html.Div(
        [
            content_header("About me"),
            html.Div([
                html.P("Just someone who loves coding, and believes coding should make our lives easier."),
                html.Div(
                    [
                        html.Img(src=app.get_asset_url("data-analytics.svg")),
                        html.P("Data Analytics", className="p-short p-bold"),
                        html.P(": Using uploaded data, visualize results graphically", className="p-short"),
                    ],
                    className="custom-div-small-space-below",
                ),
                html.Div(
                    [
                        html.Img(src=app.get_asset_url("optimization.svg")),
                        html.P("Optimization", className="p-short p-bold"),
                        html.P(": Solve computationally expensive math problems", className="p-short"),
                    ],
                    className="custom-div-small-space-below",
                ),
                html.Div(
                    [
                        html.Img(src=app.get_asset_url("prediction.svg")),
                        html.P("Prediction", className="p-short p-bold"),
                        html.P(": Use machine learning methods to churn out predictions", className="p-short"),
                    ],
                    className="custom-div-small-space-below",
                ),
                html.Br(),
                html.Br(),
                html.P(
                    [
                        "Check out my ",
                        html.A("linkedin", href="https://www.linkedin.com/in/kayjan/", target="_blank"),
                        " / ",
                        html.A("formal website", href="http://kayjan.github.io/", target="_blank"),
                        " / ",
                        html.A("Medium articles", href="https://kayjanwong.medium.com/", target="_blank"),
                        ".",
                    ]
                ),
                html.P(
                    "Feel free to write in for any UI/UX suggestion, functionality idea, new use case or bugs "
                    "encountered!"
                ),
                html.P(
                    [
                        "This website is made with Dash, deployed using Gunicorn with Docker and hosted on Heroku, "
                        "view code documentation on Sphinx ",
                        html.A("here", href="http://kayjan.readthedocs.io", target="_blank"),
                    ]
                )
            ],
                className="custom-div-instruction custom-div-left"
            )
        ],
        className="div-with-image div-with-image-left medium-image",
    )


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
                        className="custom-div-small custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above",
            ),
            html.Div(
                [
                    html.Div(
                        id="change-result",
                        className="custom-div-small custom-div-left custom-div-white image-dark-bg"
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src=app.get_asset_url("info.svg")),
                                    html.Span(
                                        "Mouseover for information, highlight to zoom, double click to reset view"),
                                    html.Span(dcc.Graph(id="graph-change-result"), style={"width": "80%"}),
                                ],
                                className="custom-div-center div-with-image div-with-image-left small-image",
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
                                className="custom-div-space-left",
                            ),
                        ],
                        className="custom-div-large custom-div-left custom-div-white"
                    ),
                ],
                id="div-change-result",
                className="custom-container custom-div-space-above custom-div-space-below",
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
                        className="custom-div-small custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above",
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
                                                "Hover over box to see more information, Single click on legend to "
                                                "hide entry, Double click on legend to highlight entry"
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
                className="custom-container custom-div-space-above custom-div-space-below",
                style=style_hidden,
            ),
        ]
    )


def chat_tab(app):
    return html.Div(
        [
            content_header("Chat Analyzer", "View your messaging pattern"),
            html.Div([
                html.P(
                    "Users can find out their telegram messaging statistics and generate word cloud based on their "
                    "Telegram chat data. Confidentiality is guaranteed as long as this webpage is loaded on HTTPS"
                ),
                html.Br(),
                html.P("Step 1: Export chat data in JSON format using Telegram Desktop"),
                html.P("Step 2: Upload exported telegram file (.json format), a message will appear to indicate if "
                       "file is uploaded successfully"),
                html.P('Step 3: Click "OK" button to generate results!')
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
                                id="upload-chat",
                                multiple=False,
                                className="div-with-image div-with-image-left small-image image-dark-bg",
                            ),
                            html.P([html.P(id="text-chat-confirm")], id="text-chat-loading"),
                            html.Button("OK", id="button-chat-ok"),
                            dcc_loading([html.P(id="chat-result-error")], dark_bg=True),
                            dcc.Store(id="intermediate-chat-result", storage_type="memory"),
                        ],
                        className="custom-div-small custom-div-left custom-div-dark"
                    ),
                ],
                className="custom-container custom-div-space-above",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P(id="chat-result", className="custom-div-small custom-div-left custom-div-white"),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Img(src=app.get_asset_url("info.svg")),
                                            html.Span(
                                                "Mouseover for information, highlight to zoom, double click to reset "
                                                "view"),
                                            dcc.Graph(id="graph-chat-result-day"),
                                        ],
                                        className="div-with-image div-with-image-left small-image",
                                    ),
                                ],
                                className="custom-div-large custom-div-center",
                            ),
                        ],
                        className="custom-container custom-div-center"
                    ),
                    html.Div(
                        [
                            html.Div(id="chat-result-wordcloud"),
                            dcc.Graph(id="graph-chat-result-hour"),
                        ],
                        className="custom-div-center custom-div-white",
                        style={
                            "display": "block"
                        }
                    ),
                ],
                id="div-chat-result",
                className="custom-container custom-div-space-above custom-div-space-below",
                style=style_hidden,
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


def trip_tab(app):
    return html.Div(
        [
            content_header("Trip Planner", "Optimize your route"),
            html.Div([
                html.P(
                    "Users can fill in multiple destinations and an optimal route based on distance will be "
                    "calculated, starting and ending from the first destination specified. This is also known as the "
                    "Travelling Salesman Problem"
                ),
                html.Br(),
                html.P("Step 1: Fill in landmark name (optional)"),
                html.P("Step 2: Click point on map corresponding to landmark name"),
                html.P("Step 3: Repeat steps 1 and 2 until all destinations have been entered"),
                html.P("Step 4: Name of landmark can be altered in the table. Try not to use the same landmark name"),
                html.P('Step 5: Click "OK" button to generate shortest and fastest route!'),
            ],
                className="custom-div-instruction custom-div-left"
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
                            html.Button("Remove last landmark", id="button-trip-remove"),
                            html.Button("Reset all landmarks", id="button-trip-reset"),
                            html.Br(),
                            html.Button("OK", id="button-trip-ok"),
                            dcc_loading(html.Div(id="trip-result"), dark_bg=True),
                        ],
                        className="custom-div-small custom-div-left custom-div-dark",
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


def mbti_tab():
    return html.Div(
        [
            content_header("MBTI Personality Test", "Predict MBTI with writing style"),
            html.Div([
                html.P(
                    "Users can find out their MBTI personality based on comparing their writing content, specifically "
                    "their choice and phrasing of words, to other users in an existing database of over 8000 people"
                ),
                html.Details(
                    [
                        html.Summary(
                            "Click here for more details about the data, processing and modelling steps"
                        ),
                        dcc.Markdown(
                            """
                    ###### Input Distribution
                    > Input data is taken from [Kaggle](https://www.kaggle.com/datasnaek/mbti-type/) and 
                    has distribution
                    > - 77% introvert (vs. 23% extrovert)
                    > - 86% intuition (vs. 14% sensing)
                    > - 54% feeling (vs. 46% thinking)
                    > - 60% perceiving (vs. 40% judging)
            
                    ###### Processing
                    > Processing of training data involves
                    > - Making the words lowercase (so don't worry about your casing)
                    > - Removing URLs `http://` and usernames `@username`
                    > - Removing digits and punctuations
                    > - Remove any mention of MBTI types or the word `mbti`
                    > - Lemmatization of words
            
                    ###### Modelling (v1)
                    > After processing the text, input data is split into 80% training and 20% testing data in a stratified 
                    fashion
            
                    > Training data has a vocabulary size of **1710 words/bi-grams/tri-grams**
            
                    > The model used is LightGBM model and 4 different models are trained for each personality trait
            
                    > Grid search is used to tune each model's hyperparameters based on best *balanced accuracy* score, and
                    > is used with stratified cross validation to handle imbalanced data
            
                    > Each model, after hyperparameter tuning, is then scored on the held out testing data
            
                    ###### Modelling (v2)
                    > After processing the text, input data is split into 80% training and 20% testing data in a stratified 
                    fashion
            
                    > Training data has a vocabulary size of **1600 words** with word embedding dimension of 64
            
                    > The model used is tensorflow neural network model and 4 different models are trained for each
                    > personality trait
            
                    > Each model, after training for several epochs, is then scored on the held out testing data
            
                    ###### Results
                    > To interpret the results, accuracy is probability of being correct,
                    > and balanced accuracy is raw accuracy where each sample is weighted according to the inverse 
                    > prevalence of its true class, which avoids inflated performance estimates on imbalanced data
                    > * i.e. 70% accuracy means model is correct 70% of the time
                    > * i.e. If model is able to correctly classify actual majority case 70% of the time, and
                    > correctly classify actual minority case 30% of the time, it achieves a balanced accuracy of 50%
            
                    > The results are
                    > * Introversion-Extroversion Model has Accuracy: 64.1% and Balanced Accuracy: 63.4%
                    > * Intuition-Sensing Model has Accuracy: 68.1% and Balanced Accuracy: 64.1%
                    > * Thinking-Feeling Model has Accuracy: 75.6% and Balanced Accuracy: 75.7%
                    > * Judging-Perceiving Model has Accuracy: 65.1% and Balanced Accuracy: 64.2%
                    > * Please do not take the results too seriously
                    """
                        ),
                    ],
                    title="Expand for details",
                ),
                html.Br(),
                html.P(
                    "Step 1: Fill in the text box with any content (i.e. something you would tweet / short summary of "
                    "yourself)"
                ),
                html.P('Step 2: Click "OK" button to generate results!'),
            ],
                className="custom-div-instruction custom-div-left"
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Textarea(
                                id="input-mbti",
                                value="",
                                placeholder="Put in your text here, preferably more than 50 words and try not to use "
                                            "words that are too common or too complex!",
                            ),
                            html.Div([html.P(id="text-mbti-words")], style={"float": "right"}),
                            html.Button("OK", id="button-mbti-ok"),
                        ],
                        className="custom-div-small-medium custom-div-left custom-div-dark",
                    ),
                    html.Div(
                        [
                            html.Div(id="mbti-results", className="custom-div-center"),
                            dcc_loading(
                                [
                                    dcc.Graph(
                                        id="graph-mbti",
                                        config={
                                            "modeBarButtonsToRemove": [
                                                "zoom2d",
                                                "pan2d",
                                                "select2d",
                                                "lasso2d",
                                                "zoomIn2d",
                                                "zoomOut2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                                "toggleSpikelines",
                                                "hoverClosestCartesian",
                                                "hoverCompareCartesian",
                                            ],
                                        },
                                        style={"display": "none", "height": "100%"},
                                    )
                                ],
                                dark_bg=False
                            ),
                        ],
                        className="custom-div-center custom-div-half",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
        ]
    )


def trade_tab():
    trade = Trade()
    indicators = ["SMA10", "SMA50", "BOLL(Close,20)", "RSI(Close,14)", "MACD"]
    indicators_desc = [
        "Simple Moving Average for past 10 values, Lagging Indicator, highlights direction of trend",
        "Simple Moving Average for past 50 values, Lagging Indicator, highlights direction of trend",
        "Bollinger Bands for 20 periods, Momentum Indicator, measures volatility of market",
        "Relative Strength Index, Momentum Indicator, measures magnitude of price changes",
        "Moving Average Convergence Divergence, Momentum Indicator, measures change between fast and slow EMA"
    ]
    return html.Div(
        [
            content_header("Live Trading", "Candlestick + Technical Indicators + Forecast"),
            html.Div([
                html.P(
                    "Users can select their preferred trade and view a candlestick chart, with statistical indicators "
                    "and forecasts! Candlestick chart refreshes every 1 second."),
                html.Br(),
                html.P("Step 1: Select preferred symbol"),
                html.P("Step 2: (Optional) Select preferred frequency of candlestick, number of candles to plot, "
                       "and whether to show technical indicators or forecasts"),
            ],
                className="custom-div-instruction custom-div-left"
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P("Symbol:", style=style_p),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-trade-symbol",
                                                options=[{"label": s, "value": s} for s in trade.get_symbol_names()],
                                                value=trade.get_symbol_names()[0],
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style=style_input,
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Frequency:", style=style_p),
                                    html.P(
                                        [
                                            dcc.Dropdown(
                                                id="dropdown-trade-frequency",
                                                options=[{"label": t, "value": t} for t in trade.TIMEFRAME_DICT.keys()],
                                                value=list(trade.TIMEFRAME_DICT.keys())[0],
                                                clearable=False,
                                                style=style_dropdown,
                                            ),
                                        ],
                                        style=style_input,
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Number of Candles:", style=style_p),
                                    dbc.Input(id="input-trade-candle", type="number", value=50, style=style_input),
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Technical Indicators:", style=style_p),
                                    dcc.Checklist(
                                        id="checkbox-trade-ind",
                                        options=[
                                            {"label": ind, "value": ind}
                                            for idx, ind in enumerate(indicators)
                                        ],
                                        value=[],
                                    ),
                                # ] + [
                                #     dbc.Tooltip(
                                #         indicators_desc[idx],
                                #         target=indicators[idx],
                                #         placement="right",
                                #         className="tooltip"
                                #     )
                                #     for idx in range(len(indicators))
                                ],
                                className="custom-div-flex",
                            ),
                            html.Div(
                                [
                                    html.P("Forecast:", style=style_p),
                                    dcc.Checklist(
                                        id="radio-trade-forecast",
                                        options=[{"label": "Forecast (EWM(0.8))", "value": "EMA(0.8)"}],
                                        value=[],
                                    ),
                                ],
                                className="custom-div-flex",
                            ),
                            html.P(id="trade-result"),
                        ],
                        className="custom-div-smaller custom-div-left custom-div-dark",
                    ),
                    html.Div(
                        [
                            dcc.Interval(id='interval-trade', interval=1000),
                            dcc.Graph(
                                id="graph-trade",
                                style={"height": "70vh"}
                            ),
                        ],
                        className="custom-div-large-full custom-div-center",
                    ),
                ],
                className="custom-container custom-div-space-above"
            ),
        ]
    )


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
                        className="custom-div-small-medium custom-div-left custom-div-dark"
                    ),
                    html.Div(
                        id="div-event-result",
                        style=style_hidden,
                        className="custom-div-small-medium custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
        ]
    )


def rng_tab():
    return html.Div(
        [
            content_header("Random Generator", "Generate random selection or groups"),
            html.Div(
                [
                    html.P("Users can perform random selection of items or grouping of items"),
                    html.Br(),
                    html.P("Step 1: Fill in the text box with items"),
                    html.P("Step 2: Specify type of task accordingly"),
                    html.P('Step 3: Click "OK" button to generate results!'),
                ],
                className="custom-div-instruction custom-div-left"
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Item List:", className="p-bold"),
                            dcc.Textarea(
                                id="input-rng",
                                value="",
                                placeholder="Item A\nItem B\nItem C\nItem D",
                            ),
                            html.P(
                                [
                                    "Task:"
                                ],
                                className="p-bold",
                                style={
                                    "margin-top": "20px",
                                    "margin-bottom": 0,
                                }
                            ),
                            html.Div(
                                [
                                    html.Button("Select N items", id="button-rng-item-ok"),
                                    html.Div([
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
                                        className="custom-div-flex",
                                        style={
                                            "display": "none",
                                            "margin": 0,
                                        }
                                    ),
                                ],
                                className="custom-div-flex",
                                style={
                                    "margin-bottom": 0
                                }
                            ),
                            html.Div(
                                [
                                    html.Button("Split into N groups", id="button-rng-group-ok"),
                                    html.Div([
                                        html.P("Number of groups:"),
                                        dcc.Input(
                                            id="input-rng-group",
                                            type="number",
                                            value=2,
                                            min=2,
                                            style={
                                                "width": "40%",
                                            },
                                        )
                                    ],
                                        id="div-rng-group",
                                        className="custom-div-flex",
                                        style={
                                            "display": "none",
                                            "margin": 0,
                                        }
                                    )
                                ],
                                className="custom-div-flex",
                                style={
                                    "margin-bottom": 0
                                }
                            ),
                            html.Br(),
                            html.Button("OK", id="button-rng-ok"),
                            dcc_loading([html.P(id="rng-result-error")], dark_bg=True),
                        ],
                        className="custom-div-small-medium custom-div-left custom-div-dark",
                    ),
                    html.Div(
                        id="div-rng-result",
                        style=style_hidden,
                        className="custom-div-small-medium custom-div-left custom-div-dark",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
            ),
        ]
    )


def wnrs_tab(app):
    wnrs_game = WNRS()
    list_of_deck = ["Main Deck 1"]
    wnrs_game.initialize_game(list_of_deck)
    wnrs_information = wnrs_game.get_information()
    data_default = dict(list_of_deck=list_of_deck, wnrs_game_dict=wnrs_game.__dict__)
    return html.Div(
        [
            content_header("We're Not Really Strangers", ""),
            html.Button(
                "Select deck",
                id="button-wnrs-show-ok",
                title="Show/hide deck selection",
            ),
            html.A(
                [
                    dcc.Upload(
                        [
                            html.Span("Upload past progress", title="Upload past progress")
                        ],
                        id="uploadbutton-wnrs",
                        multiple=False,
                    )
                ]
            ),
            html.Button(" + Instructions", id="button-wnrs-instruction-ok", title="How to play"),
            html.Button(" + Suggest prompts", id="button-wnrs-suggestion-ok", title="Send in your card prompt ideas",),
            html.Br(),
            html.Div(
                [
                    html.P("How to Play (2-6 players)", className="p-short p-bold"),
                    html.P("The game is played on a single device. Sit in a circle with device in middle of all "
                           "players. Select the decks you want to play with and the levels. Players take turn to "
                           "answer questions shown on the screen and tap on the right side of card to proceed to next "
                           "question."),
                    html.P("Wildcards", style={"margin-top": "20px"}, className="p-short p-bold"),
                    html.P("If you're presented with a wildcard you must complete the instructions otherwise stated. "
                           "These cards can appear at any moment during the game!"),
                    html.P("Save your progress!", style={"margin-top": "20px"}, className="p-short p-bold"),
                    html.P("Couldn't manage to go through all the cards in one session? Save your progress by clicking "
                           "on the 'Save progress' button at the bottom of the page and load the game next time to "
                           "pick up exactly where you left off."),
                    html.P("Have fun!", style={"margin-top": "20px"}, className="p-short p-bold"),
                ],
                id="div-wnrs-instruction",
                className="custom-div-dark image-dark-bg",
                style={"display": "none", "width": "90%", "margin-top": "20px"},
            ),
            html.Div(
                [
                    html.P(
                        "You can contribute too! Suggest prompts that you would like to see in the game",
                    ),
                    dcc.Input(
                        id="input-wnrs-suggestion",
                        type="text",
                        placeholder="Your prompt(s)",
                        style={"width": "70%", "margin-bottom": "3px"},
                    ),
                    dcc.Textarea(
                        id="input-wnrs-suggestion2",
                        value="",
                        placeholder="(Optional) Additional comments or feedback, include your contact details if you "
                                    "expect a reply!",
                        style={"width": "70%"},
                    ),
                    html.Br(),
                    html.Button("Send", id="button-wnrs-send-ok"),
                    html.P(id="wnrs-suggestion-reply"),
                ],
                id="div-wnrs-suggestion",
                className="custom-div-dark image-dark-bg",
                style={"display": "none", "width": "90%", "margin-top": "20px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Main Deck"),
                            html.Div(
                                [
                                    html.Span("Main Deck", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="main-deck-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Main Deck"]["Main Deck"]["description"],
                                        placement="right",
                                        target="main-deck-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button(
                                        "Level 1", id="Main Deck 1",
                                        style={"background-color": colour_palette["dark_pink"]}),
                                    dbc.Button("Level 2", id="Main Deck 2"),
                                    dbc.Button("Level 3", id="Main Deck 3"),
                                    dbc.Button("Final Card", id="Main Deck Final"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.P("Crossover", style=style_wnrs_text),
                            html.Div(
                                [
                                    html.Span("Bumble x BFF Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="bumble-bff-help",),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"]["Bumble x BFF Edition"]["description"],
                                        placement="right",
                                        target="bumble-bff-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Bumble x BFF Edition 1"),
                                    dbc.Button("Level 2", id="Bumble x BFF Edition 2"),
                                    dbc.Button("Level 3", id="Bumble x BFF Edition 3"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Bumble Bizz Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="bumble-bizz-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"]["Bumble Bizz Edition"]["description"],
                                        placement="right",
                                        target="bumble-bizz-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Bumble Bizz Edition 1"),
                                    dbc.Button("Level 2", id="Bumble Bizz Edition 2"),
                                    dbc.Button("Level 3", id="Bumble Bizz Edition 3"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Bumble Date Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="bumble-date-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"]["Bumble Date Edition"]["description"],
                                        placement="right",
                                        target="bumble-date-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Bumble Date Edition 1"),
                                    dbc.Button("Level 2", id="Bumble Date Edition 2"),
                                    dbc.Button("Level 3", id="Bumble Date Edition 3"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(["Cann Edition", html.Sup("Drinking", className="blinker")],
                                              className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="cann-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"]["Cann Edition"]["description"],
                                        placement="right",
                                        target="cann-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Cann Edition 1"),
                                    dbc.Button("Level 2", id="Cann Edition 2"),
                                    dbc.Button("Level 3", id="Cann Edition 3"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(["Valentino Edition", html.Sup("Reflection", className="blinker")],
                                              className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="valentino-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"]["Valentino Edition"]["description"],
                                        placement="right",
                                        target="valentino-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Valentino Edition 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.P("Expansion", style=style_wnrs_text),
                            html.Div(
                                [
                                    html.Span("Honest Dating Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="dating-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Expansion"]["Honest Dating Edition"]["description"],
                                        placement="right",
                                        target="dating-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Honest Dating Edition 1"),
                                    dbc.Button("Level 2", id="Honest Dating Edition 2"),
                                    dbc.Button("Level 3", id="Honest Dating Edition 3"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Inner Circle Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="inner-circle-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Expansion"]["Inner Circle Edition"]["description"],
                                        placement="right",
                                        target="inner-circle-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Inner Circle Edition 1"),
                                    dbc.Button("Level 2", id="Inner Circle Edition 2"),
                                    dbc.Button("Level 3", id="Inner Circle Edition 3"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Own It Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="own-it-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Expansion"]["Own It Edition"]["description"],
                                        placement="right",
                                        target="own-it-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Own It Edition 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Relationship Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="relationship-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Expansion"]["Relationship Edition"]["description"],
                                        placement="right",
                                        target="relationship-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Relationship Edition 1"),
                                    dbc.Button("Level 2", id="Relationship Edition 2"),
                                    dbc.Button("Level 3", id="Relationship Edition 3"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.P("Online", style=style_wnrs_text),
                            html.Div(
                                [
                                    html.Span("Race and Privilege Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="race-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Online"]["Race and Privilege Edition"]["description"],
                                        placement="right",
                                        target="race-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Race and Privilege Edition 1"),
                                    dbc.Button("Level 2", id="Race and Privilege Edition 2"),
                                    dbc.Button("Level 3", id="Race and Privilege Edition 3"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Quarantine Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="quarantine-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Online"]["Quarantine Edition"]["description"],
                                        placement="right",
                                        target="quarantine-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Quarantine Edition 1"),
                                    dbc.Button("Level 2", id="Quarantine Edition 2"),
                                    dbc.Button("Level 3", id="Quarantine Edition 3"),
                                    dbc.Button("Final Card", id="Quarantine Edition Final"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Voting Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="voting-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Online"]["Voting Edition"]["description"],
                                        placement="right",
                                        target="voting-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Voting Edition 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.P("Single-Player", style=style_wnrs_text),
                            html.Div(
                                [
                                    html.Span("Breakup Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="breakup-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"]["Breakup Edition"]["description"],
                                        placement="right",
                                        target="breakup-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Breakup Edition 1"),
                                    dbc.Button("Final Card", id="Breakup Edition Final"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(["Existential Crisis Edition", html.Sup("Mine", className="blinker")],
                                              className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="crisis-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"]["Existential Crisis Edition"]["description"],
                                        placement="right",
                                        target="crisis-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Existential Crisis Edition 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Forgiveness Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="forgiveness-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"]["Forgiveness Edition"]["description"],
                                        placement="right",
                                        target="forgiveness-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Forgiveness Edition 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Healing Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="healing-help",),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"]["Healing Edition"]["description"],
                                        placement="right",
                                        target="healing-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Healing Edition 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Self-Love Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="love-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"]["Self-Love Edition"]["description"],
                                        placement="right",
                                        target="love-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Self-Love Edition 1"),
                                    dbc.Button("Final Card", id="Self-Love Edition Final"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Self-Reflection Edition", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="reflection-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"]["Self-Reflection Edition"]["description"],
                                        placement="right",
                                        target="reflection-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Self-Reflection Edition 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.P(
                                [
                                    "Gotmann Card Deck",
                                    html.Sup("improve relationship", className="blinker")
                                ],
                                style=style_wnrs_text,
                            ),
                            html.Div(
                                [
                                    html.Span("Love Maps", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="love-maps-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Gotmann"]["Love Maps"]["description"],
                                        placement="right",
                                        target="love-maps-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Love Maps 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Open Ended Questions", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="open-ended-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Gotmann"]["Open Ended Questions"]["description"],
                                        placement="right",
                                        target="open-ended-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Open Ended Questions 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Rituals of Connection", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="rituals-help"),
                                    dbc.Tooltip(
                                        wnrs_information["Gotmann"]["Rituals of Connection"]["description"],
                                        placement="right",
                                        target="rituals-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Rituals of Connection 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Opportunity", className="span-short"),
                                    html.Img(src=app.get_asset_url("info.svg"), id="opportunity-help",),
                                    dbc.Tooltip(
                                        wnrs_information["Gotmann"]["Opportunity"]["description"],
                                        placement="right",
                                        target="opportunity-help",
                                        className="tooltip",
                                    ),
                                    dbc.Button("Level 1", id="Opportunity 1"),
                                ],
                                className="div-with-image div-with-image-left small-image",
                            ),
                        ]
                    ),
                ],
                id="div-wnrs-selection",
                className="custom-div-dark image-dark-bg",
                style={"display": "none", "width": "90%", "margin-top": "20px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.P(id="wnrs-prompt"),
                                            html.P(id="wnrs-reminder-text"),
                                            html.P(id="wnrs-reminder"),
                                            html.P(
                                                [
                                                    "We're Not Really Strangers", html.Br(), html.Br()
                                                ],
                                                id="wnrs-deck"),
                                        ],
                                        style={
                                            "position": "relative",
                                            "height": "100%",
                                            "text-transform": "uppercase",
                                        },
                                    )
                                ],
                                id="wnrs-card",
                            ),
                            html.Button(id="button-wnrs2-back"),
                            html.Button(id="button-wnrs2-next"),
                            html.Span("Press here for previous card", id="wnrs-text-back"),
                            html.Span("Press here for next card", id="wnrs-text-next"),
                        ],
                        id="div-wnrs",
                        className="custom-div-center div-with-invisible-button",
                    ),
                    html.Div(
                        [
                            html.P(id="wnrs-counter"),
                            html.Button("Previous", id="button-wnrs-back", style=style_hidden),
                            html.Button("Next", id="button-wnrs-next", style=style_hidden),
                            html.Button("Shuffle Remaining Cards", id="button-wnrs-shuffle-ok"),
                            html.Form(
                                [
                                    dcc.Input(
                                        value=encode_dict(data_default),
                                        name="result",
                                        type="text",
                                        style=style_hidden,
                                        id="input-wnrs",
                                    ),
                                    html.Button(
                                        [
                                            html.Img(src=app.get_asset_url("download.svg")),
                                            html.Span("Save Progress"),
                                        ],
                                        type="submit",
                                        id="button-wnrs-download-ok",
                                        className="div-with-image div-with-image-left small-image",
                                    ),
                                ],
                                method="POST",
                                action="/download_dict/",
                                style={"display": "inline-block"},
                            ),
                        ]
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
                style={
                    "text-align": "center",
                    "margin-bottom": 0,
                },
            ),
            dcc.Store(id="intermediate-wnrs", storage_type="memory", data=data_default),
        ]
    )


def contact_tab():
    return html.Div(
        [
            content_header("Contact Me"),
            html.Div([
                html.P("If you have any questions, feedback or suggestions, please feel free to drop me an email."),
                dcc.Input(
                    id="input-contact-name",
                    type="text",
                    placeholder="Name",
                    style=style_contact_textarea,
                ),
                dcc.Input(
                    id="input-contact-email",
                    type="text",
                    placeholder="Email Address",
                    style=style_contact_textarea,
                ),
                dcc.Textarea(
                    id="input-contact-content",
                    value="",
                    placeholder="Email body",
                    style=style_contact_textarea,
                ),
                html.Br(),
                html.Button("Send", id="button-contact-ok"),
                html.P(id="contact-reply"),
            ],
                className="custom-div-instruction custom-div-left"
            )
        ]
    )


def image_edit_tab(app):
    return html.Div(
        [
            content_header("Image Editing", "Draw on images"),
            html.Div([
                html.P("Users can edit images directly by drawing on them, or just draw on a blank canvas!"),
                html.Br(),
                html.P("Step 1: Upload an image (optional)"),
                html.P("Step 2: Start drawing!"),
            ],
                className="custom-div-instruction custom-div-left"
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
                        className="custom-div-large-full custom-div-left custom-div-dark",
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


def keyboard_tab():
    return html.Div(
        [
            content_header("Keyboard", "Play music on the flyyyyy"),
            html.Div([
                html.P("Ideally, users can play the keyboard here. Im still figuring out how to make it work."),
            ],
                className="custom-div-instruction custom-div-left"
            ),
            # html.Button('C note', id='button_music')
        ]
    )


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
