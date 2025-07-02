from typing import Any, List, Union

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def bullet_point(icon: str, text: Any):
    return html.Div(
        [
            html.Span(icon, style={"marginRight": "0.5em"}),
            html.Span(text, style={"flex": 1}),
        ],
        style={"display": "flex", "alignItems": "flex-start", "marginBottom": "0.2em"},
    )


def accordian(
    details: List[List[Union[str, List[str]]]],
    value: Union[str, List[str]] = [],
):
    return dmc.Accordion(
        chevron=DashIconify(icon="ant-design:down-outlined"),
        chevronPosition="right",
        variant="separated",
        radius=15,
        multiple=True,
        value=value,
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(
                        children=[html.Div([html.H5(detail[0]), html.H6(detail[1])])],
                        icon=DashIconify(
                            icon=detail[2],
                            color="#202029",
                            width=20,
                        ),
                    ),
                    dmc.AccordionPanel(detail[3], style={"padding": "0px 10px"}),
                ],
                value=detail[4],
            )
            for detail in details
        ],
    )
