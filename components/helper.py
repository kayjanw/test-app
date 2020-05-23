import base64
import io

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
    return dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict('records')[:max_rows],
        style_as_list_view=True,
        style_header={
            'fontWeight': 'bold',
            'textAlign': 'left'
        },
        style_cell={
            'background-color': 'transparent',
            'color': 'white',
            'font-family': 'Source Sans Pro',
            'font-size': 13,
            'textAlign': 'center'
        },
        style_table={
            'overflowX': 'auto'
        },
        css=[{
            'selector': 'tr:hover',
            'rule': 'background-color: black; color: white'
        }, {
            'selector': 'td.cell--selected *, td.focused *',
            'rule': 'background-color: black !important;'
                    'color: white !important;'
                    'text-align: left;'
        }]
    )


def change_download_button(df):
    df = df.to_json(orient='split', date_format='iso')
    return html.Form([
        dcc.Input(
            value=df,
            name='result',
            type='text',
            style={'display': 'none'}),
        html.Button(
            'Download results',
            type='submit'
        )
    ],
        method='POST',
        action='/download_change_df/'
    )