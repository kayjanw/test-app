import base64
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from plotly.colors import n_colors


def violin_plot():
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
    def decorator(func):
        def wrapper(*args, **kw):
            if print_function:
                print(f'==== Function called: {func.__name__}')
            result = func(*args, **kw)
            return result
        return wrapper
    return decorator


def table_css():
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
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    xls = pd.ExcelFile(io.BytesIO(decoded))
    return xls.sheet_names


def parse_data(contents, filename, worksheet=None):
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


def encode_df(df):
    df_ser = df.to_json(orient='split', date_format='iso')
    return df_ser


def decode_df(df_ser):
    df = pd.read_json(df_ser, orient='split')
    df.columns = df.columns.astype(str)
    return df


def update_when_upload(contents, worksheet, filename, style, ctx):
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


def change_download_button(df):
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
