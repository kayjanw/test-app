from typing import Any, Dict, List, Optional, Union

from dash import html

from cv.layouts.helper import highlight_text


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
    ):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.details = details
        self.accordian_id = accordian_id

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


def convert_to_accordian(accordian_data: List[AccordianRow]):
    return [
        [
            accordian_row.title,
            accordian_row.subtitle,
            accordian_row.icon,
            accordian_row.accordian_details,
            accordian_row.accordian_id,
        ]
        for accordian_row in accordian_data
    ]
