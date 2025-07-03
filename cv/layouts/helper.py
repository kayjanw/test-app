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


def create_scrollable_area(data: List[List[str]], columns: List[str], **kwargs):
    table_kwargs = dict(
        withTableBorder=False,
        withColumnBorders=False,
        withRowBorders=False,
        highlightOnHover=True,
        horizontalSpacing="xs",
        verticalSpacing="xs",
    )
    table_kwargs = {**table_kwargs, **kwargs}

    return dmc.TableScrollContainer(
        dmc.Table(children=create_course_table(data, columns), **table_kwargs),
        maxHeight=400,
        minWidth=600,
        type="scrollarea",
    )


def create_course_table(data: List[List[str]], columns: List[str]):
    return [
        html.Thead(html.Tr([html.Th(col) for col in columns])),
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(_data[0]),
                        html.Td(_data[1]),
                    ]
                    + (
                        [
                            html.Td(
                                html.A(
                                    dmc.Button("Details", size="md"),
                                    href=_data[2],
                                    target="_blank",
                                )
                            )
                            if _data[2].startswith("http")
                            else html.Td(_data[2])
                        ]
                        if len(columns) == 3
                        else []
                    )
                )
                for _data in data
            ]
        ),
    ]
