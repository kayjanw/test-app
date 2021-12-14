"""This file contains helper functions that are used across multiple tabs
"""

import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import io
import json
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import re
import sendgrid

from functools import reduce
from plotly.colors import n_colors
from sendgrid.helpers.mail import Mail, Email, To, Content


def print_callback(print_function):
    """Decorator function to print callback on backend for debugging purposes

    Args:
        print_function (bool): indicates whether to print callback

    Returns:
        (function)
    """
    def decorator(func):
        def wrapper(*args, **kw):
            if print_function:
                print(f'==== Function called: {func.__name__}')
                print(f"Triggered by {dash.callback_context.triggered[0]['prop_id']}")
            result = func(*args, **kw)
            return result
        return wrapper
    return decorator


def violin_plot():
    """Get data for plot, return plot

    Adds plotly.graph_objects charts for violin plot at initial loading page

    Returns:
        (dcc.Graph)
    """
    np.random.seed(1)
    points = (np.linspace(1, 2, 12)[:, None] * np.random.randn(12, 200) +
              (np.arange(12) + 2 * np.random.random(12))[:, None])
    points2 = np.array(
        [np.concatenate((point, [points.min(), points.max()])) for point in points])
    colors = n_colors('rgb(32, 32, 41)',
                      'rgb(190, 155, 137)', 12, colortype='rgb')
    data = []
    for data_line, color in zip(points2, colors):
        trace = go.Violin(
            x=data_line,
            line_color=color,
            side='positive',
            width=3,
            points=False,
            hoverinfo='skip'
        )
        data.append(trace)
    layout = dict(
        title='u t i l s . p y',
        xaxis={
            'showgrid': False,
            'zeroline': False,
            'visible': False,
            'fixedrange': True,
        },
        yaxis={
            'showgrid': False,
            'zeroline': False,
            'visible': False,
            'fixedrange': True,
        },
        showlegend=False,
        margin=dict(l=0, r=0, t=80, b=0)
    )
    return dcc.Graph(
        figure=dict(data=data, layout=layout),
        id='violin-plot',
        config={
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                                       'autoScale2d', 'resetScale2d', 'toggleSpikelines',
                                       'hoverClosestCartesian', 'hoverCompareCartesian'],
        },
        style={
            'margin-top': '15vh',
            'height': '60vh'
        }
    )


def dcc_loading(children, dark_bg=True):
    """Get default dcc.Loading component

    Args:
        children (list): children of component
        dark_bg (bool): indicates whether loading icon is on dark background

    Returns:
        (dcc.Loading)
    """
    if dark_bg:
        color = 'white'
    else:
        color = '#202029'
    return dcc.Loading(
        children,
        type='circle',
        color=color
    )


def table_css():
    """Gets default dash_table CSS components

    Returns:
        4-element tuple

        - (dict): Style for table header
        - (dict): Style for table cell
        - (dict): Style for table
        - (list): CSS component
    """
    style_header = {
        'fontWeight': 'bold',
        'textAlign': 'left'
    }
    style_cell = {
        'background-color': 'transparent',
        'color': 'white',
        'font-family': 'Source Sans Pro',
        'font-size': 13,
        'textAlign': 'left'
    }
    style_table = {
        'overflowX': 'auto'
    }
    css = [
        {
            'selector': 'tr:hover',
            'rule': 'background-color: black; color: white'
        }, {
            'selector': 'td.cell--selected *, td.focused *',
            'rule': 'background-color: black !important;'
                    'color: white !important;'
                    'text-align: left;'
        }
    ]
    return style_header, style_cell, style_table, css


def get_worksheet(contents):
    """Get worksheet names from an excel file

    Args:
        contents (str): contents of data uploaded

    Returns:
        (list): list of worksheet names
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    xls = pd.ExcelFile(io.BytesIO(decoded))
    return xls.sheet_names


def parse_data(contents, filename, worksheet=None):
    """Reads uploaded data into DataFrame

    Args:
        contents (str): contents of data uploaded
        filename (str): filename of data uploaded
        worksheet (str): worksheet of excel file, if applicable, defaults to None

    Returns:
        (pandas DataFrame)
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = None
    try:
        if 'csv' in filename:
            file = io.StringIO(decoded.decode('utf-8'))
            df = pd.read_csv(file)
        elif 'xls' in filename:
            if worksheet is not None:
                xls = pd.ExcelFile(io.BytesIO(decoded))
                df = pd.read_excel(xls, worksheet)
            else:
                df = pd.read_excel(io.BytesIO(decoded))
        elif 'json' in filename:
            df = decoded
        else:
            raise Exception('File format not supported')
    except Exception as e:
        print(e)
    return df


def generate_datatable(df, max_rows=3):
    """Generate table from pandas DataFrame

    Args:
        df (pandas DataFrame): input DataFrame
        max_rows (int): maximum number of rows to show

    Returns:
        (dash_table.DataTable)
    """
    style_header, style_cell, style_table, css = table_css()
    return dash_table.DataTable(
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records')[:max_rows],
        style_as_list_view=True,
        style_header=style_header,
        style_cell=style_cell,
        style_table=style_table,
        css=css
    )


def get_summary_statistics(df, cols):
    """Generate table of summary statistics for DataFrame for list of columns

    Args:
        df (pandas DataFrame): input DataFrame
        cols (list): column(s) to get summary statistic for

    Returns:
        (dash_table.DataTable)
    """
    param_name = ['Number of values', 'Mean', 'Std. Dev',
                  'Min, 0%', '25%', 'Median, 50%', '75%', 'Max, 100%']
    style_header, style_cell, style_table, css = table_css()
    return dash_table.DataTable(
        columns=[
            {'name': 'Parameter', 'id': 'Parameter'}
        ] + [
            {'name': col, 'id': col} for col in cols
        ],
        data=[reduce(lambda a, b: dict(a, **b), [{
            'Parameter': param_name[idx],
            col: np.round(df[col].describe()[idx], 2)
        } for col in cols]) for idx in range(len(param_name))],
        style_as_list_view=True,
        style_header=style_header,
        style_cell=style_cell,
        style_table=style_table,
        css=css
    )


def encode_df(df):
    """Serializes pandas DataFrame to JSON format

    Args:
        df (pandas DataFrame): input DataFrame

    Returns:
        (str)
    """
    df_ser = df.to_json(orient='split', date_format='iso')
    return df_ser


def decode_df(df_ser):
    """De-serializes JSON format string to pandas DataFrame

    Args:
        df_ser (str): input serialized DataFrame

    Returns:
        (pandas DataFrame)
    """
    df = pd.read_json(df_ser, orient='split')
    df.columns = df.columns.astype(str)
    return df


def encode_dict(d):
    """Serializes dictionary to JSON format

    Args:
        d (dict): input dictionary

    Returns:
        (str)
    """
    return json.dumps(d)


def decode_dict(d_ser):
    """De-serializes JSON format string to dictionary

    Args:
        d_ser (str): input serialized dictionary

    Returns:
        (dict)
    """
    return json.loads(d_ser)


def update_when_upload(contents, worksheet, filename, style, ctx):
    """Reads uploaded data into DataFrame and return dash application objects

    Args:
        contents (str): contents of data uploaded
        worksheet (str): worksheet of excel file, if applicable, defaults to None
        filename (str): filename of data uploaded
        style (dict): current style of worksheet selector dropdown
        ctx (str): dash callback trigger item name

    Returns:
        4-element tuple

        - (list): list of worksheets options
        - (dict): updated style of worksheet selector dropdown
        - (dash_table.DataTable/list): sample of uploaded data
        - (dict): intermediate data stored in dcc.Store
    """
    worksheet_options = []
    sample_table = []
    if dash.callback_context.triggered and contents is not None:
        # Check file type
        if 'xls' not in filename and 'csv' not in filename:
            sample_table = [
                html.P('File type not supported. Please upload another file.')]

        # Get worksheet options
        if 'xls' in filename:
            worksheet_list = get_worksheet(contents)
            if len(worksheet_list) > 1:
                worksheet_options = [{'label': ws, 'value': ws}
                                     for ws in worksheet_list]

        # Update worksheet options display style
        if len(worksheet_options):
            style['display'] = 'flex'
        else:
            style['display'] = 'none'

        # Read uploaded contents
        if 'worksheet' in ctx:
            df = parse_data(contents, filename, worksheet)
        else:
            df = parse_data(contents, filename)

        if type(df) == pd.DataFrame:
            df.columns = df.columns.astype(str)
            sample_table = [
                html.P('Sample of uploaded data:', style={'margin': 0}),
                generate_datatable(df),
                html.P(f'Number of rows: {len(df)}', style={'margin': 0})
            ]
            records = dict(df=encode_df(df))
            return worksheet_options, style, sample_table, records
    return worksheet_options, style, sample_table, {}


def result_download_button(app, df):
    """Download button for processed data or results

    Args:
        app (app): get app properties
        df (pandas DataFrame): input DataFrame, to be downloaded by user

    Returns:
        (html.Form)
    """
    df_ser = encode_df(df)
    return html.Form([
        dcc.Input(
            value=df_ser,
            name='result',
            type='text',
            style={'display': 'none'}),
        html.Button([
            html.Img(src=app.get_asset_url('download.svg')),
            html.Span('Download results')
        ],
            type='submit',
            className='div-with-image div-with-image-left small-image'
        )
    ],
        method='POST',
        action='/download_df/'
    )


def result_download_text(df, input_text):
    """Download text for processed data or results

    Args:
        df (pandas DataFrame): input DataFrame, to be downloaded by user
        input_text (str): text to display

    Returns:
        (html.Form)
    """
    df_ser = encode_df(df)
    return html.Form([
        dcc.Input(
            value=df_ser,
            name='demo',
            type='text',
            style={'display': 'none'}
        ),
        html.Button([
            input_text
        ],
            style={
                'height': '5px',
                'margin': 0,
                'padding': 0,
                'font-size': '1em',
                'font-weight': 'bold',
                'letter-spacing': 'normal',
                'text-transform': 'none'
            },
            type='submit',
        )
    ],
        style={
          'display': 'inline-block'
        },
        method='POST',
        action='/download_demo/'
    )


def valid_email(email):
    """Helper function to validate email address

    Args:
        email (str): email address

    Returns:
        (bool)
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False


def send_email(email_body, subject='Email from Herokuapp', recipient='e0503512@u.nus.edu'):
    """Helper function to send email

    Args:
        email_body (str): email body to be sent

    Returns:
        (bool)
    """
    try:
        SENDGRID_API_KEY = ENV['SENDGRID_API_KEY']
    except NameError:
        try:
            SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
        except KeyError:
            print('No SENDGRID_API_KEY found')
    try:
        my_sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email('kay.jan@hotmail.com')  # verified sender
        to_email = To(recipient)
        subject = subject
        content = Content('text/plain', email_body)
        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()
        response = my_sg.client.mail.send.post(request_body=mail_json)
        if response.status_code == 202:
            return True
        else:
            return False
    except Exception:
        return False
