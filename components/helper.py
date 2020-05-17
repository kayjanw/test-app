import numpy as np
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
