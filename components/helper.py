"""This file contains helper functions that are used across multiple tabs
"""
import base64
import io
import json
import os
import re
from functools import reduce
from typing import Any, Dict, List, Optional

import dash
import matplotlib.pyplot as plt
import msoffcrypto
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sendgrid
from dash import dash_table, dcc, html
from plotly.colors import n_colors
from sendgrid.helpers.mail import Content, Email, Mail, To

colour_palette = {
    "grey": "#57555A",
    "deep_blue": "#202029",
    "dark_pink": "#BE9B89",
    "light_pink": "#F0E3DF",
    "pink_grey": "#D6CAC7",
}

inline_style = {"display": "inline-block"}
flex_style = {"display": "flex"}
hide_style = {"display": "none"}
show_button_style = {"background-color": "#BE9B89"}
hide_button_style = {"background-color": "#F0E3DF"}

return_message = {
    "card_not_filled": "Please fill in a card prompt (required field)",
    "card_not_select": "Please select a deck to start",
    "change_axis": "Please specify columns as axis",
    "change_columns": "Please select different columns for comparison",
    "change_columns_empty": "Please specify columns to compare",
    "change_numeric": "Processed dataframe is empty. Please select numeric columns",
    "file_uploaded": "File uploaded",
    "file_not_uploaded": "Please upload a file",
    "file_not_uploaded_json": "Please upload a JSON file",
    "email_email_valid": "Please fill in a valid email address",
    "email_empty_body": "Please fill in content into email body (required field)",
    "email_empty_email": "Please fill in your email (required field)",
    "email_empty_name": "Please fill in your name (required field)",
    "email_fail": "Email failed to send, please contact kay.jan@hotmail.com directly",
    "email_fail_all": "Some email failed to send to participants, "
    "please contact kay.jan@hotmail.com directly",
    "email_sent_feedback": "Feedback received! Thank you",
    "email_sent_suggestion": "Suggestion received! Thank you",
    "email_sent_all": "Results emailed successfully to all participants!",
    "input_empty": "Please fill in text input",
    "rng_task_empty": "Please select a task",
    "scroll_down": "Please scroll down for results",
    "wrong_format_demo": "File is not in expected format. "
    "Please download the demo worksheet and follow the format "
    "accordingly",
    "wrong_format_json": "Please upload a valid JSON file. Data is not in the correct format",
    "wrong_file_type": "File type not supported. Please upload another file",
}


def print_callback(print_function):
    """Decorator function to print callback on backend for debugging purposes

    Args:
        print_function (bool): indicates whether to print callback

    Returns:
        function
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if print_function:
                print(f"==== Function called: {func.__name__}")
                print(f"Triggered by {dash.callback_context.triggered[0]['prop_id']}")
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def violin_plot() -> dcc.Graph:
    """Get data for plot, return plot

    Adds plotly.graph_objects charts for violin plot at initial loading page
    """
    np.random.seed(1)
    points = (
        np.linspace(1, 2, 12)[:, None] * np.random.randn(12, 200)
        + (np.arange(12) + 2 * np.random.random(12))[:, None]
    )
    points2 = np.array(
        [np.concatenate((point, [points.min(), points.max()])) for point in points]
    )
    colors = n_colors("rgb(32, 32, 41)", "rgb(190, 155, 137)", 12, colortype="rgb")
    data = []
    for data_line, color in zip(points2, colors):
        trace = go.Violin(
            x=data_line,
            line_color=color,
            side="positive",
            width=3,
            points=False,
            hoverinfo="skip",
        )
        data.append(trace)
    layout = dict(
        title="u t i l s . p y",
        xaxis={
            "showgrid": False,
            "zeroline": False,
            "visible": False,
            "fixedrange": True,
        },
        yaxis={
            "showgrid": False,
            "zeroline": False,
            "visible": False,
            "fixedrange": True,
        },
        showlegend=False,
        margin=dict(l=0, r=0, t=80, b=0),
    )
    return dcc.Graph(
        figure=dict(data=data, layout=layout),
        id="violin-plot",
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
    )


def dcc_loading(children, dark_bg: bool = True) -> dcc.Loading:
    """Get default dcc.Loading component

    Args:
        children: children of component
        dark_bg: indicates whether loading icon is on dark background
    """
    if dark_bg:
        color = "white"
    else:
        color = colour_palette["deep_blue"]
    return dcc.Loading(children, type="circle", color=color)


def table_css(dark: bool = True):
    """Gets default dash_table CSS components

    Args:
        dark: if table is loaded in dark background, defaults to True

    Returns:
        4-element tuple

        - (dict): Style for table header
        - (dict): Style for table cell
        - (dict): Style for table
        - (list): CSS component
    """
    if dark:
        background_color = "black"
        color = "white"
    else:
        background_color = "white"
        color = "black"

    style_header = {"fontWeight": "bold", "textAlign": "left"}
    style_cell = {
        "background-color": "transparent",
        "color": color,
        "font-family": "Source Sans Pro",
        "font-size": 13,
        "textAlign": "left",
    }
    style_table = {"overflowX": "auto"}
    css = [
        {
            "selector": "tr:hover",
            "rule": f"background-color: {background_color}; color: {color}",
        },
        {
            "selector": "td.cell--selected *, td.focused *",
            "rule": f"background-color: {background_color} !important;"
            f"color: {color} !important;"
            "text-align: left;",
        },
    ]
    return style_header, style_cell, style_table, css


def get_worksheet(contents: str) -> List[str]:
    """Get worksheet names from an excel file

    Args:
        contents: contents of data uploaded

    Returns:
        list of worksheet names
    """
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    xls = pd.ExcelFile(io.BytesIO(decoded))
    return xls.sheet_names


def parse_data(
    contents: str, filename: str, worksheet: Optional[str] = None, **kwargs
) -> pd.DataFrame:
    """Reads uploaded data into DataFrame

    Args:
        contents: contents of data uploaded
        filename: filename of data uploaded
        worksheet: worksheet of excel file, if applicable, defaults to None
    """
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = None
    try:
        if ".csv" in filename:
            file = io.StringIO(decoded.decode("utf-8"))
            df = pd.read_csv(file, **kwargs)
        elif ".xls" in filename:
            if worksheet is not None:
                xls = pd.ExcelFile(io.BytesIO(decoded), **kwargs)
                df = pd.read_excel(xls, worksheet)
            else:
                df = pd.read_excel(io.BytesIO(decoded), **kwargs)
        elif ".json" in filename:
            df = decoded
        else:
            raise Exception("File format not supported")
    except Exception as e:
        print(e)
    return df


def generate_datatable(
    df: pd.DataFrame, max_rows: int = 3, dark: bool = True
) -> dash_table.DataTable:
    """Generate table from pandas DataFrame

    Args:
        df: input DataFrame
        max_rows: maximum number of rows to show
        dark: if table is loaded in dark background, defaults to True
    """
    style_header, style_cell, style_table, css = table_css(dark=dark)
    return dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records")[:max_rows],
        style_as_list_view=True,
        style_header=style_header,
        style_cell=style_cell,
        style_table=style_table,
        css=css,
        cell_selectable=False,
    )


def get_summary_statistics(
    df: pd.DataFrame, cols: List[str], dark: bool = True
) -> dash_table.DataTable:
    """Generate table of summary statistics for DataFrame for list of columns

    Args:
        df: input DataFrame
        cols: column(s) to get summary statistic for
        dark: if table is loaded in dark background, defaults to True
    """
    param_name = [
        "Number of values",
        "Mean",
        "Std. Dev",
        "Min, 0%",
        "25%",
        "Median, 50%",
        "75%",
        "Max, 100%",
    ]
    style_header, style_cell, style_table, css = table_css(dark=dark)
    return dash_table.DataTable(
        columns=[{"name": "Parameter", "id": "Parameter"}]
        + [{"name": col, "id": col} for col in cols],
        data=[
            reduce(
                lambda a, b: dict(a, **b),
                [
                    {
                        "Parameter": param_name[idx],
                        col: np.round(df[col].describe()[idx], 2),
                    }
                    for col in cols
                ],
            )
            for idx in range(len(param_name))
        ],
        style_as_list_view=True,
        style_header=style_header,
        style_cell=style_cell,
        style_table=style_table,
        css=css,
        cell_selectable=False,
    )


def encode_df(df: pd.DataFrame) -> str:
    """Serializes pandas DataFrame to JSON format

    Args:
        df: input DataFrame
    """
    df_ser = df.to_json(orient="split", date_format="iso")
    return df_ser


def decode_df(df_ser: str) -> pd.DataFrame:
    """De-serializes JSON format string to pandas DataFrame

    Args:
        df_ser: input serialized DataFrame
    """
    df = pd.read_json(df_ser, orient="split")
    df.columns = df.columns.astype(str)
    return df


def encode_dict(d: Dict[str, Any]) -> str:
    """Serializes dictionary to JSON format

    Args:
        d: input dictionary

    """
    return json.dumps(d)


def decode_dict(d_ser: str) -> Dict[str, Any]:
    """De-serializes JSON format string to dictionary

    Args:
        d_ser: input serialized dictionary
    """
    return json.loads(d_ser)


def decrypt_workbook(file_path: str, password: str) -> io.BytesIO:
    """Decrypt file

    Args:
        file_path: file path
        password: file password
    """
    decrypted_workbook = io.BytesIO()
    with open(file_path, "rb") as file:
        office_file = msoffcrypto.OfficeFile(file)
        office_file.load_key(password=password)
        office_file.decrypt(decrypted_workbook)
    return decrypted_workbook


def update_when_upload(
    contents: str,
    worksheet: str,
    sample_data_style: Dict[str, Any],
    filename: str,
    style: Dict[str, Any],
    ctx: str,
    **kwargs,
):
    """Reads uploaded data into DataFrame and return dash application objects

    Args:
        contents: contents of data uploaded
        worksheet: worksheet of excel file, if applicable, defaults to None
        sample_data_style: current style of sample uploaded data
        filename: filename of data uploaded
        style: current style of worksheet selector dropdown
        ctx: dash callback trigger item name

    Returns:
        5-element tuple

        - (list): list of worksheets options
        - (dict): updated style of worksheet selector dropdown
        - (dash_table.DataTable/list): sample of uploaded data
        - (dict): updated style of uploaded data
        - (dict): intermediate data stored in dcc.Store
    """
    worksheet_options = []
    sample_table = []
    if dash.callback_context.triggered and contents is not None:
        if sample_data_style is None:
            sample_data_style = {}

        # Check file type
        if ".xls" not in filename and ".csv" not in filename:
            sample_table = [html.P(return_message["wrong_file_type"])]
            sample_data_style["color"] = "red"

        # Get worksheet options
        if ".xls" in filename:
            worksheet_list = get_worksheet(contents)
            if len(worksheet_list) > 1:
                worksheet_options = [
                    {"label": ws, "value": ws} for ws in worksheet_list
                ]

        # Update worksheet options display style
        if len(worksheet_options):
            style["display"] = "flex"
        else:
            style["display"] = "none"

        # Read uploaded contents
        if "worksheet" in ctx:
            df = parse_data(contents, filename, worksheet, **kwargs)
        else:
            df = parse_data(contents, filename, **kwargs)

        if isinstance(df, pd.DataFrame):
            df.columns = df.columns.astype(str)
            sample_table = [
                html.P("Sample of uploaded data:", style={"margin": 0}),
                generate_datatable(df),
                html.P(f"Number of rows: {len(df)}", style={"margin": 0}),
            ]
            sample_data_style["color"] = "inherit"
            records = dict(df=encode_df(df))
            return worksheet_options, style, sample_table, sample_data_style, records
    return worksheet_options, style, sample_table, sample_data_style, {}


def result_download_button(app, df: pd.DataFrame, dark: bool = True) -> html.Form:
    """Download button for processed data or results

    Args:
        app (app): get app properties
        df: input DataFrame, to be downloaded by user
        dark: if table is loaded in dark background, defaults to True
    """
    if dark:
        class_name = "button-dark image-dark-bg"
    else:
        class_name = ""
    df_ser = encode_df(df)
    return html.Form(
        [
            dcc.Input(
                value=df_ser, name="result", type="text", style={"display": "none"}
            ),
            html.Button(
                [
                    html.Img(src=app.get_asset_url("download.svg")),
                    html.Span("Download results"),
                ],
                type="submit",
                className=f"div-with-image div-with-image-left small-image {class_name}",
            ),
        ],
        method="POST",
        action="/download_df/",
    )


def result_download_text(input_text: str) -> html.Form:
    """Download text for processed data or results

    Args:
        input_text (str): text to display
    """
    return html.Form(
        [
            html.Button(
                [html.Span(input_text)],
                style={
                    "line-height": 1.6,
                    "margin": 0,
                    "padding": 0,
                    "border-radius": 0,
                    "font-size": "1em",
                    "font-weight": "bold",
                    "letter-spacing": "normal",
                    "text-decoration": "underline",
                    "text-transform": "none",
                },
                type="submit",
            )
        ],
        style={"display": "inline-block"},
        method="POST",
        action="/download_demo/",
    )


def valid_email(email: str) -> bool:
    """Helper function to validate email address

    Args:
        email: email address

    Returns:
        indicator if email is valid
    """
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return True
    return False


def send_email(
    email_body: str,
    subject: str = "Email from utils.py Web App",
    recipient: str = "kayjanw@gmail.com",
) -> bool:
    """Helper function to send email

    Args:
        email_body: email body to be sent
        subject: email subject to be sent
        recipient: email recipient to receive email

    Returns:
        indicator if email is sent
    """
    try:
        SENDGRID_API_KEY = ENV["SENDGRID_API_KEY"]
    except NameError:
        try:
            SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
        except KeyError:
            print("No SENDGRID_API_KEY found")
    try:
        my_sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email("kay.jan@hotmail.com")  # verified sender
        to_email = To(recipient)
        subject = subject
        content = Content("text/html", email_body.replace("\n", "<br>"))
        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()
        response = my_sg.client.mail.send.post(request_body=mail_json)
        if response.status_code == 202:
            return True
        else:
            return False
    except Exception:
        return False


def get_excel_from_df(df: pd.DataFrame) -> io.BytesIO:
    """Create excel from DataFrame

    Args:
        df: input DataFrame
    """
    buf = io.BytesIO()
    excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="Sheet1", index=False)
    excel_writer.save()
    excel_data = buf.getvalue()  # noqa: F841
    buf.seek(0)
    return buf


def get_excel_demo() -> io.BytesIO:
    """Create demo excel for Event Planner tab"""
    buf = io.BytesIO()
    excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
    pd.DataFrame().to_excel(excel_writer, sheet_name="Sheet1", index=False)

    # Add items
    worksheet = excel_writer.sheets["Sheet1"]
    workbook = excel_writer.book
    bold_red = workbook.add_format({"bold": True, "font_color": "red"})
    bold = workbook.add_format({"bold": True})
    worksheet.write("A1", "Event:", bold_red)
    worksheet.write("B1", "Secret Santa")
    start_row = 3
    worksheet.write(f"A{start_row}", "Name", bold_red)
    for idx in range(5):
        worksheet.write(f"A{idx + start_row + 1}", f"Person {idx + 1}")
    worksheet.write(f"B{start_row}", "Email (Optional)", bold_red)
    colour_list = ["Red", "Orange", "Yellow", "Green", "Blue", "Black"]
    worksheet.write(f"C{start_row}", "Gift Criteria: Colour", bold)
    for idx in range(len(colour_list)):
        worksheet.write(f"C{idx + start_row + 1}", colour_list[idx])
    colour_texture = ["Shiny", "Round", "Smooth"]
    worksheet.write(f"D{start_row}", "Gift Criteria: Texture", bold)
    for idx in range(len(colour_texture)):
        worksheet.write(f"D{idx + start_row + 1}", colour_texture[idx])

    excel_writer.save()
    excel_data = buf.getvalue()  # noqa: F841
    buf.seek(0)
    return buf


def create_json_from_dict(d: Dict[str, Any]) -> io.BytesIO:
    """Create JSON from dictionary

    Args:
        d: input dictionary
    """
    buf = io.BytesIO(json.dumps(d).encode())
    return buf


def create_fig_from_diagram(
    diagram, id: str, close_all: bool = True, **kwargs
) -> html.Img:
    """Create html.Img from diagram

    Args:
        diagram: input diagram
        id: id of html.Img object
        close_all: whether to close image
    """
    out_img = io.BytesIO()
    diagram.savefig(out_img, format="png", transparent=True)
    if close_all:
        diagram.clf()
        plt.close("all")
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    content = f"data:image/png;base64,{encoded}"
    return html.Img(id=id, src=content, **kwargs)
