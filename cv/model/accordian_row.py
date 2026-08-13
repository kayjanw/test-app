from typing import Dict, List, Optional, Union

import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

from cv.layouts.helper import bullet_point, highlight_text


class AccordianDetails:
    def __init__(
        self, icon: str, detail: str, highlight: Optional[Union[str, List[str]]] = None
    ):
        self.icon = icon
        self.detail = detail
        self.highlight = highlight


class AccordianRow:
    def __init__(
        self,
        title: str,
        subtitle: str,
        icon: str,
        details: Dict[str, List[AccordianDetails]],
        accordian_id: str,
        open: bool = False,
    ):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.details = details
        self.accordian_id = accordian_id
        self.open = open

    @property
    def accordian_details(self):
        return [
            bullet_point(
                detail.icon,
                highlight_text(detail.detail, detail.highlight, wrap_p=True),
            )
            for details in self.details.values()
            for detail in details
        ]


def split_title(title: str):
    if "," in title:
        return title.split(",")[0], ", " + ",".join(title.split(",")[1:])
    return title, ""


def accordian(
    details: List[AccordianRow],
    value: Union[str, List[str]] = [],
) -> dmc.Accordion:
    """Display details in accordian layout

    Args:
        details: details of a single accordian
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
                        children=[
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H5(split_title(detail.title)[0]),
                                            html.H5(
                                                split_title(detail.title)[1],
                                                className="p-normal",
                                            ),
                                        ],
                                        className="custom-div-flex-only",
                                    ),
                                    html.H6(detail.subtitle),
                                ]
                            )
                        ],
                        icon=DashIconify(
                            icon=detail.icon,
                            color="#202029",
                            width=20,
                        ),
                    ),
                    dmc.AccordionPanel(
                        detail.accordian_details, style={"padding": "0px 10px"}
                    ),
                ],
                value=detail.accordian_id,
            )
            for detail in details
        ],
    )


def convert_one_row(accordian_row: AccordianRow):
    return html.Div(
        [
            html.H5(accordian_row.title),
            html.H6(accordian_row.subtitle),
            html.Br(),
            *[
                html.Details(
                    [
                        html.Summary(detail_dept, className="p-summary"),
                        dcc.Markdown(
                            "\n\n".join(
                                f"> {_detail.icon} {_detail.detail}"
                                for _detail in detail_details
                            )
                        ),
                    ],
                    title="Expand for details",
                )
                for detail_dept, detail_details in accordian_row.details.items()
            ],
            html.Br(),
        ],
        className="custom-div-instruction custom-div-left",
    )


def convert_to_list(accordian_data: List[AccordianRow]):
    return [convert_one_row(industry_row) for industry_row in accordian_data]
