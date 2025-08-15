import numpy as np
from _plotly_utils.colors import n_colors
from dash import dcc, html
from dash_iconify import DashIconify
from plotly import graph_objects as go


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
        title="a r t. p n g",
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


def pixel_art():
    colour_range = [
        "deep-red",
        "red",
        "deep-orange",
        "orange",
        "deep-yellow",
        "yellow",
        "green",
        "deep-green",
        "blue",
        "deep-blue",
        "purple",
        "deep-purple",
    ]
    np.random.seed(1)
    num_colours = list(map(int, np.random.random(len(colour_range)) * 22))
    art = []
    for idx, colour in enumerate(colour_range):
        art.extend(
            [
                DashIconify(
                    icon=f"openmoji:{colour}-flag",
                    height=40,
                    style={"margin": 0, "padding": 0},
                )
                for _ in range(num_colours[idx] + 3)
            ]
        )
        art.append(html.Br())
    return art
