import dash_html_components as html
import dash_table
import numpy as np
import plotly.graph_objects as go

from components.helper import table_css


def remove_string_values(df, col):
    # Handle string values
    if isinstance(col, str):
        df[col].replace(regex=True, to_replace=r'[^0-9.]', value=np.nan, inplace=True)
    elif isinstance(col, list):
        for c in col:
            df[c].replace(regex=True, to_replace=r'[^0-9.]', value=np.nan, inplace=True)
    return df


def remove_null(df, col):
    # Handle string values
    if isinstance(col, str):
        df.dropna(subset=[col], inplace=True)
    elif isinstance(col, list):
        df.dropna(subset=col, inplace=True)
    return df


def convert_to_float(df, col, col_max):
    # Convert to float, normalize if necessary
    if col_max is not None and col_max is not '':
        df[col] = df[col].astype(float) / col_max * 100
        df[col] = np.round(df[col], 2)
    else:
        df[col] = df[col].astype(float)
    return df


def compute_change(df, x_col, x_max, y_col, y_max):
    df = df.copy()
    df = remove_string_values(df, [x_col, y_col])
    df = remove_null(df, [x_col, y_col])
    df = convert_to_float(df, x_col, x_max)
    df = convert_to_float(df, y_col, y_max)
    df['Change'] = df[y_col] - df[x_col]
    return df


def get_summary_statistics(df, x_col, y_col):
    param_name = ['Number of values', 'Mean', 'Std. Dev', 'Min, 0%', '25%', 'Median, 50%', '75%', 'Max, 100%']
    return dash_table.DataTable(
        columns=[
            {'name': 'Parameter', 'id': 'Parameter'},
            {'name': x_col, 'id': x_col},
            {'name': y_col, 'id': y_col}
        ],
        data=[{
            'Parameter': param_name[idx],
            x_col: np.round(df[x_col].describe()[idx], 2),
            y_col: np.round(df[y_col].describe()[idx], 2)
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
    x_min, x_max = df[x_col].min(), df[x_col].max()
    y_min, y_max = df[y_col].min(), df[y_col].max()
    x_min_limit, x_max_limit = min(0, x_min - 5), max(100, x_max + 5)
    y_min_limit, y_max_limit = min(0, y_min - 5), max(100, y_max + 5)
    trace = go.Violin(
        x=df[x_col],
        y=df[y_col],
        marker={'color': '#202029'},
        text=['<br>'.join([f'{df.columns[idx]}: {x[idx]}' for idx in range(len(df.columns))]) for x in df.values],
        hoverinfo='text',
        jitter=1,
        points='all',
        line_color='#FFFFFF',
    )
    line = go.Scatter(
        x=[min(x_min, y_min), max(x_max, y_max)],
        y=[min(x_min, y_min), max(x_max, y_max)],
        mode='lines',
        hoverinfo='skip'
    )
    hist_x = go.Histogram(
        x=df[x_col],
        name=x_col+' distribution',
        nbinsx=10,
        yaxis='y2',
        marker={'color': '#202029'},
        hovertemplate='Range: %{x}<br>Total: %{y}<extra></extra>'
    )
    hist_y = go.Histogram(
        y=df[y_col],
        name=y_col+' distribution',
        nbinsy=10,
        xaxis='x2',
        marker={'color': '#202029'},
        hovertemplate='Range: %{y}<br>Total: %{x}<extra></extra>',
        orientation='h'
    )
    layout = dict(
        title='Scatterplot + Histogram of results',
        xaxis=dict(title=x_col, domain=[0, 0.85], range=[x_min_limit, x_max_limit]),
        yaxis=dict(title=y_col, domain=[0, 0.85], range=[y_min_limit, y_max_limit]),
        xaxis2=dict(domain=[0.85, 1]),
        yaxis2=dict(domain=[0.85, 1]),
        hovermode='closest',
        showlegend=False,
        font=dict(
            family='Source Sans Pro',
        )
    )
    return dict(data=[trace, line, hist_x, hist_y], layout=layout)


def get_changes_table():
    style_header, style_cell, style_table, css = table_css()
    return dash_table.DataTable(
        id='table-changes',
        columns=[
            dict(name='Columns to compare', id='column', presentation='dropdown'),
            dict(name='Maximum possible value (integer value, optional)', id='max', type='numeric', on_change={'failure': 'default'}),
        ],
        data=[dict(column='', max='') for i in range(4)],
        editable=True,
        style_as_list_view=True,
        style_header=style_header,
        style_cell=style_cell,
        css=css
    )


def compute_changes(df, col_identifier, list_of_tuples):
    df = df.copy()
    for col, col_max in list_of_tuples:
        df = remove_string_values(df, col)
        df = remove_null(df, col)
        df = convert_to_float(df, col, col_max)
    df = remove_null(df, col_identifier)
    return df


def transpose_dataframe(df, col_identifier, list_of_tuples):
    cols = [row[0] for row in list_of_tuples]
    df2 = df[cols].transpose()
    if col_identifier is not '' and col_identifier is not None:
        df2.columns = df[col_identifier]
    return df2


def get_line_plot(df2):
    trace = []
    instructions = [
        'Hover over line to see more information',
        html.Br(),
        'Single click on legend to hide entry',
        html.Br(),
        'Double click on legend to highlight entry'
    ]
    if df2.columns.nunique() < len(df2.columns):
        df2.columns = range(len(df2.columns))
        instructions.append(html.Br())
        instructions.append('Note: Column identifier do not have unique entries, replaced legend with running numbers')
    for col in df2.columns:
        trace.append(
            go.Scatter(
                x=list(df2.index),
                y=df2[col],
                name=col,
                mode='lines',
                line=dict(color='#202029'),
                text=[f'{col}<br><br>'+'<br>'.join([f'{df2.index[idx]}: {x}' for idx, x in
                                   enumerate(df2[col].values)])] * len(df2.index),
                hoverinfo='text',
            )
        )
    layout = dict(
        title='Line plot of results',
        hovermode='closest',
        hoverdistance=-1,
        xaxis=dict(
            type='category'
        ),
        font=dict(
            family='Source Sans Pro',
            size=16
        )
    )
    return instructions, dict(data=trace, layout=layout)


def get_parallel_coord(df, col_identifier, list_of_tuples):
    cols = [row[0] for row in list_of_tuples]
    trace = go.Parcoords(
        line_color='#202029',
        customdata=df[col_identifier],  # cannot seem to support hover information
        dimensions=[
            dict(
                label=col,
                values=df[col],
                range=[np.round(df[col].min()-5, -1), np.round(df[col].max()+5, -1)],
                tickvals=np.arange(np.round(df[col].min()-5, -1), np.round(df[col].max()+5, -1)+1, 10)
            )
            for col in cols
        ] + [
            dict(
                label=col_identifier,
                values=list(range(len(df))),
                range=[0, len(df)],
                tickvals=list(range(len(df))),
                ticktext=df[col_identifier]
            )
        ],
    )
    layout = dict(
        title='Parallel Coordinate plot of results',
        showlegend=True,
        font=dict(
            family='Source Sans Pro',
            size=16,
        )
    )
    instructions = [
        'Drag along vertical axis line to select a subset of data (i.e. constrained selection), slide the constrained '
        'selection to toggle the selected range',
        html.Br(),
        'Click anywhere along the vertical axis line to remove constrained selection',
        html.Br(),
        'Slide the axis label to toggle the width between vertical axis lines or even change the axis order'
    ]
    return instructions, dict(data=[trace], layout=layout)
