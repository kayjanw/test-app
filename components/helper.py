import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import io
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from functools import reduce
from plotly.colors import n_colors


def violin_plot():
    """Get data for plot

    Adds plotly.graph_objects charts for violin plot at initial loading page

    Returns:
        (dict)
    """
    np.random.seed(1)
    points = (np.linspace(1, 2, 12)[:, None] * np.random.randn(12, 200) +
              (np.arange(12) + 2 * np.random.random(12))[:, None])
    points2 = np.array([np.concatenate((point, [points.min(), points.max()])) for point in points])
    colors = n_colors('rgb(32, 32, 41)', 'rgb(190, 155, 137)', 12, colortype='rgb')
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
    return dict(data=data, layout=layout)


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
            result = func(*args, **kw)
            return result
        return wrapper
    return decorator


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
        columns=[{"name": col, "id": col} for col in df.columns],
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
    param_name = ['Number of values', 'Mean', 'Std. Dev', 'Min, 0%', '25%', 'Median, 50%', '75%', 'Max, 100%']
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
        # Get worksheet options
        if 'xls' in filename:
            worksheet_list = get_worksheet(contents)
            if len(worksheet_list) > 1:
                worksheet_options = [{'label': ws, 'value': ws} for ws in worksheet_list]

        # Update worksheet options display style
        if len(worksheet_options):
            style['display'] = 'inline-block'
        else:
            style['display'] = 'none'

        # Read uploaded contents
        if ctx == 'dropdown-changes-worksheet':
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


def result_download_button(df):
    """Download button for processed data or results

    Args:
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
        html.Button(
            'Download results',
            type='submit'
        )
    ],
        method='POST',
        action='/download_df/'
    )
