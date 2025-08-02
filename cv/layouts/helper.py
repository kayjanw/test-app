from typing import Any, List, Optional, Union

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def rating_review(
    rating: Union[float, int], review: str, carousel: bool = False
) -> dmc.Group:
    """Rating and review for table cell

    Args:
        rating: rating
        review: review details
        carousel: whether display is for carousel card
    """
    if carousel:
        return html.Div(
            [
                dmc.Rating(fractions=3, value=rating, readOnly=True),
                html.Span(review, className="span-book"),
            ]
        )
    return dmc.Group(
        [dmc.Rating(fractions=3, value=rating, readOnly=True), html.Span(review)]
    )


def highlight_text(
    text: str, highlight: Optional[Union[str, List[str]]] = None, wrap_p: bool = False
) -> Union[str, dmc.Highlight]:
    if highlight:
        return dmc.Highlight(text, highlight=highlight, style={"fontSize": "inherit"})
    return html.P(text) if wrap_p else text


def accordian(
    details: List[List[Union[str, List[str]]]],
    value: Union[str, List[str]] = [],
) -> dmc.Accordion:
    """Display details in accordian layout

    Args:
        details: details consisting of
            - title
            - subtitle
            - accordian icon
            - detail
            - accordian id
        value: value(s) of active accordian id

    Returns:
        Accordian item
    """
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
