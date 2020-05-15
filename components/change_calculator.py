import base64
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import io
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            file = io.StringIO(decoded.decode('utf-8'))
            df = pd.read_csv(file)
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
    return df


def compute_change(df, x_col, x_max, y_col, y_max):
    # Handle string values
    df[x_col].replace(regex=True, to_replace=r'[^0-9.]', value=np.nan, inplace=True)
    df[y_col].replace(regex=True, to_replace=r'[^0-9.]', value=np.nan, inplace=True)
    df.dropna(subset=[x_col, y_col], inplace=True)

    # Convert to float, normalize if necessary
    if x_max is None:
        df[x_col] = df[x_col].astype(float)
    else:
        df[x_col] = df[x_col].astype(float) / x_max * 100
        df[x_col] = np.round(df[x_col], 2)
    if y_max is None:
        df[y_col] = df[y_col].astype(float)
    else:
        df[y_col] = df[y_col].astype(float) / y_max * 100
        df[y_col] = np.round(df[y_col], 2)
    df['Change'] = df[y_col] - df[x_col]
    return df


def get_summary_statistics(df, x_col, y_col):
    param_name = ['Number of values', 'Mean', 'Std. Dev', 'Min, 0%', '25%', 'Median, 50%', '75%', 'Max, 100%']
    return dash_table.DataTable(
        columns=[
            {'name': 'Parameter', 'id': 'Parameter'},
            {'name': 'X-axis', 'id': "X-axis"},
            {'name': 'Y-axis', 'id': "Y-axis"}
        ],
        data=[{
            'Parameter': param_name[idx],
            'X-axis': np.round(df[x_col].describe()[idx], 2),
            'Y-axis': np.round(df[y_col].describe()[idx], 2)
        } for idx in range(len(param_name))
        ],
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
            'textAlign': 'left'
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


def get_scatter_plot(df, x_col, y_col):
    trace = go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='markers',
        marker={'color': '#202029'},
        text=['<br>'.join([f'{df.columns[idx]}: {x[idx]}' for idx in range(len(df.columns))]) for x in df.values],
        hoverinfo='text'
    )
    line = go.Scatter(
        x=[min(df[x_col].min(), df[y_col].min()), max(df[x_col].max(), df[y_col].max())],
        y=[min(df[x_col].min(), df[y_col].min()), max(df[x_col].max(), df[y_col].max())],
        mode='lines',
        hoverinfo='skip'
    )
    layout = dict(
        title='Scatterplot of results',
        xaxis={'title': x_col},
        yaxis={'title': y_col},
        hovermode='closest',
        showlegend=False
    )
    return dict(data=[trace, line], layout=layout)


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
