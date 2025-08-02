from typing import List, Optional, Union

import dash_mantine_components as dmc
from dash import html

from cv.layouts.helper import highlight_text


class Cert:
    def __init__(
        self,
        title: str,
        organization: str,
        link_or_date: str,
        highlight: Optional[Union[str, List[str]]] = None,
    ):
        self._title = title
        self.organization = organization
        self.link_or_date = link_or_date
        self.highlight = highlight

    @property
    def title(self) -> Union[str, dmc.Highlight]:
        return highlight_text(self._title, self.highlight)

    @property
    def link(self):
        if self.link_or_date.startswith("http"):
            return self.link_or_date

    @property
    def link_button(self):
        if self.link:
            return html.A(
                dmc.Button("Details", size="md"),
                href=self.link,
                target="_blank",
            )

    @property
    def date(self):
        if not self.link_or_date.startswith("http"):
            return self.link_or_date
