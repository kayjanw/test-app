import dash_table
import numpy as np
import plotly.graph_objects as go


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
        autosize=False,
        xaxis=dict(title=x_col, domain=[0, 0.85], range=[x_min_limit, x_max_limit]),
        yaxis=dict(title=y_col, domain=[0, 0.85], range=[y_min_limit, y_max_limit]),
        xaxis2=dict(domain=[0.85, 1]),
        yaxis2=dict(domain=[0.85, 1]),
        hovermode='closest',
        showlegend=False,
        font=dict(
            family="Source Sans Pro",
        )
    )
    return dict(data=[trace, line, hist_x, hist_y], layout=layout)
