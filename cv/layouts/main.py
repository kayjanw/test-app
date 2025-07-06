from dash import dcc, html

from common.components.helper import colour_palette, dcc_loading
from common.components.landing_page import violin_plot
from common.layouts.main import banner, sidebar_header


def app_cv() -> html.Div:
    return html.Div(
        [
            # Top contents
            html.Div(banner(), id="banner"),
            # Left contents
            html.Div(
                [sidebar_header(), sidebar_dropdown_cv()],
                id="sidebar",
            ),
            # Right contents
            html.Div(dcc_loading(violin_plot(), dark_bg=False), id="tab-content"),
        ]
    )


def sidebar_dropdown_cv():
    return html.Div(
        [
            dcc.Tabs(
                id="tabs-parent",
                value=None,
                vertical=True,
                parent_className="custom-tabs-parent",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        label="About Me",
                        value="tab-cv-aboutme",
                        className="custom-tab p-bold",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Articles",
                        value="tab-articles",
                        className="custom-tab p-bold",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Work",
                        value="",
                        className="custom-tab-disabled",
                        disabled=True,
                    ),
                    dcc.Tab(
                        label="Industry",
                        value="tab-cv-industry",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Teaching",
                        value="tab-cv-teaching",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Education",
                        value="tab-cv-education",
                        className="custom-tab p-bold",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Certifications",
                        value="tab-cv-certifications",
                        className="custom-tab p-bold",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Bookshelf",
                        value="tab-cv-books",
                        className="custom-tab p-bold",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Contact Me",
                        value="tab-contact",
                        className="custom-tab p-bold",
                        selected_className="custom-tab-selected",
                    ),
                ],
                colors={"background": colour_palette["deep_blue"]},
                persistence=True,
                persistence_type="memory",
            )
        ]
    )
