from dash import dcc, html

from common.components.helper import colour_palette, dcc_loading
from common.components.landing_page import violin_plot
from common.layouts.main import banner, content_header, sidebar_header

style_dropdown = {"width": "100%", "color": "black"}
style_p = {"width": "40%"}
style_input = {"width": "35%"}
style_checklist = {"width": "100%"}
style_wnrs_text = {}
style_contact_textarea = {"width": "70%", "margin-bottom": "5px"}
style_hidden = {"display": "none"}


def app_1() -> html.Div:
    return html.Div(
        [
            # Top contents
            html.Div(banner(), id="banner"),
            # Left contents
            html.Div([sidebar_header(), sidebar_dropdown()], id="sidebar"),
            # Right contents
            html.Div(dcc_loading(violin_plot(), dark_bg=False), id="tab-content"),
        ]
    )


def app_2(pathname) -> html.Div:
    return html.Div(
        [
            # Top contents
            html.Div(banner(), id="banner"),
            # Left contents
            html.Div([sidebar_header(), dcc.Tabs(id="tabs-parent")], id="sidebar"),
            # Right contents
            html.Div(
                [
                    content_header("Nice try", "Sadly this page does not exist"),
                    html.Div(
                        [
                            html.P(
                                [
                                    f"What were you hoping for in {pathname} page?",
                                    html.Br(),
                                    "Click ",
                                    html.A("here", href="/"),
                                    " to return to home page",
                                ]
                            ),
                        ],
                        className="custom-div-instruction",
                    ),
                ],
                id="tab-content",
            ),
        ]
    )


def app_event() -> html.Div:
    return html.Div(
        [
            # Top contents
            html.Div(banner(), id="banner"),
            # Left contents
            html.Div(
                [sidebar_header(), sidebar_dropdown_event()],
                id="sidebar",
            ),
            # Right contents
            html.Div(dcc_loading(violin_plot(), dark_bg=False), id="tab-content"),
        ]
    )


def sidebar_dropdown():
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
                        value="tab-aboutme",
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
                        label="Data Analytics",
                        value="",
                        className="custom-tab-disabled",
                        disabled=True,
                    ),
                    dcc.Tab(
                        label="Change Calculator",
                        value="tab-change",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Change Calculator 2",
                        value="tab-change2",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Chat Analyzer",
                        value="tab-chat",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Optimization",
                        value="",
                        className="custom-tab-disabled",
                        disabled=True,
                    ),
                    dcc.Tab(
                        label="Trip Planner",
                        value="tab-trip",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Prediction",
                        value="",
                        className="custom-tab-disabled",
                        disabled=True,
                    ),
                    dcc.Tab(
                        label="MBTI Personality Test",
                        value="tab-mbti",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Live Trading",
                        value="tab-trade",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Fun Things",
                        value="",
                        className="custom-tab-disabled",
                        disabled=True,
                    ),
                    dcc.Tab(
                        label="Event Planner",
                        value="tab-event",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Random Generator",
                        value="tab-rng",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="We're Not Really Strangers",
                        value="tab-wnrs",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Chess",
                        value="tab-chess",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Wordle",
                        value="tab-wordle",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Poker",
                        value="tab-poker",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    # dcc.Tab(
                    #     label="Go to events!",
                    #     value="tab-others",
                    #     className="custom-tab",
                    # ),
                    dcc.Tab(
                        label="Contact Me",
                        value="tab-contact",
                        className="custom-tab p-bold",
                        selected_className="custom-tab-selected",
                    ),
                    # dcc.Tab(label='Image Editing', value='tab-image', className='custom-tab', selected_className='custom-tab-selected')
                ],
                colors={"background": colour_palette["deep_blue"]},
                persistence=True,
                persistence_type="memory",
            ),
        ]
    )


def sidebar_dropdown_event():
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
                        value="tab-aboutme",
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
                        label="Fun Things",
                        value="",
                        className="custom-tab-disabled",
                        disabled=True,
                    ),
                    dcc.Tab(
                        label="Event Planner",
                        value="tab-event",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="Random Generator",
                        value="tab-rng",
                        className="custom-tab-sub",
                        selected_className="custom-tab-selected",
                    ),
                    dcc.Tab(
                        label="We're Not Really Strangers",
                        value="tab-wnrs",
                        className="custom-tab-sub",
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
