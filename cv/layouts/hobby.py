import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash_iconify import DashIconify

from common.layouts.main import content_header
from cv.data.hobby import hobbies


def get_hobby_plot(hobby_data: pd.DataFrame):
    x_max, y_max = 10, 10
    fig = go.Figure()

    for _type in hobby_data["type"].unique():
        hobby_data_type = hobby_data[hobby_data["type"] == _type]
        opacities = [frequency.value for frequency in hobby_data_type["frequency"]]
        fig.add_trace(
            go.Scatter(
                x=hobby_data_type["enjoyment"],
                y=hobby_data_type["proficiency"],
                hoverinfo="text",
                hovertext=[
                    frequency.name.capitalize()
                    for frequency in hobby_data_type["frequency"]
                ],
                mode="markers+text",
                text=hobby_data_type["name"],
                textposition="top center",
                name=_type.name.capitalize(),
                marker=dict(size=12, color=_type.value, opacity=opacities),
                showlegend=False,
                legendgroup=_type.name.capitalize(),
            )
        )

        # Dummy plot to show marker with full opacity
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                name=_type.name.capitalize(),
                marker=dict(size=12, color=_type.value, opacity=1.0),
                legendgroup=_type.name.capitalize(),  # legend links to data
            )
        )

    # Quadrant
    line_kwargs = dict(
        type="line", opacity=0.7, line=dict(color="gray", width=2, dash="dash")
    )
    fig.add_shape(x0=x_max // 2, y0=0, x1=x_max // 2, y1=y_max, **line_kwargs)
    fig.add_shape(x0=0, y0=y_max // 2, x1=x_max, y1=y_max // 2, **line_kwargs)

    rect_kwargs = dict(
        type="rect", xref="x", yref="y", opacity=0.2, layer="below", line_width=0
    )
    fig.add_shape(x0=5, y0=5, x1=10, y1=10, fillcolor="rgb(214,39,40)", **rect_kwargs)
    fig.add_shape(x0=0, y0=5, x1=5, y1=10, fillcolor="rgb(166,216,84)", **rect_kwargs)
    fig.add_shape(x0=5, y0=0, x1=10, y1=5, fillcolor="rgb(255,217,47)", **rect_kwargs)
    fig.add_shape(x0=0, y0=0, x1=5, y1=5, fillcolor="rgb(140,86,75)", **rect_kwargs)

    annotation_kwargs = dict(showarrow=False, font=dict(size=12, color="black"))
    fig.add_annotation(x=7.5, y=9.5, text="<b>Passion</b>", **annotation_kwargs)
    fig.add_annotation(x=2.5, y=9.5, text="<b>Enriching</b>", **annotation_kwargs)
    fig.add_annotation(x=7.5, y=0.5, text="<b>Growth</b>", **annotation_kwargs)
    fig.add_annotation(x=2.5, y=0.5, text="<b>Low Priority</b>", **annotation_kwargs)

    axis_kwargs = dict(
        range=[0, 10], showticklabels=False, showgrid=False, fixedrange=True
    )
    fig.update_layout(
        xaxis=dict(title="Enjoyment", **axis_kwargs),
        yaxis=dict(title="Proficiency", **axis_kwargs),
        plot_bgcolor="white",
        margin=dict(t=10, b=10, r=5, l=5),
        legend=dict(x=0.5, y=1, xanchor="center", yanchor="bottom", orientation="h"),
    )
    return fig


def hobby_tab(app):
    return html.Div(
        [
            content_header(
                "Hobbies",
                [
                    DashIconify(icon="openmoji:sunglasses", height=40),
                    "All fun and play",
                ],
            ),
            html.Div(
                [
                    dcc.Graph(
                        figure=get_hobby_plot(pd.DataFrame(hobbies)),
                        config={
                            "scrollZoom": False,
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
                    ),
                ],
                className="custom-div-instruction custom-div-left",
                style={"min-width": "800px"},
            ),
        ]
    )
