from typing import Any, List, Optional, Union

import dash_mantine_components as dmc
from dash import html


def bullet_point(icon: str, text: Any) -> html.Div:
    """Bullet point for accordian details

    Args:
        icon: icon for bullet point
        text: bullet point text
    """
    return html.Div(
        [
            html.Span(icon, style={"marginRight": "0.5em"}),
            html.Span(text, style={"flex": 1}),
        ],
        style={"display": "flex", "alignItems": "flex-start", "marginBottom": "0.2em"},
    )


def highlight_text(
    text: str, highlight: Optional[Union[str, List[str]]] = None, wrap_p: bool = False
) -> Union[str, dmc.Highlight]:
    if highlight:
        return dmc.Highlight(text, highlight=highlight, style={"fontSize": "inherit"})
    return html.P(text) if wrap_p else text


def create_scrollable_area(
    data: List[List[str]], columns: List[str], **kwargs
) -> dmc.TableScrollContainer:
    """Create scrollable table

    Args:
        data: data to show, each entry is a row
        columns: column names of table
        **kwargs: any table kwargs

    Returns:
        Scrollable table
    """
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


def create_course_table(data: List[List[str]], columns: List[str]) -> List[Any]:
    """Create a table

    Args:
        data: data to show, each entry is a row
        columns: column names of table

    Returns:
        Table data
    """
    return [
        html.Thead(html.Tr([html.Th(col) for col in columns])),
        html.Tbody(
            [
                html.Tr([html.Td(data_cell) for data_cell in data_row])
                for data_row in data
            ]
        ),
    ]
