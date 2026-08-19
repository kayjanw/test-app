from typing import List, Tuple, Union

import dash
from dash import ctx, dcc, html
from dash.dependencies import Input, Output, State

from common.components.email import send_email, valid_email
from common.components.helper import dcc_loading, print_callback, return_message
from common.components.landing_page import violin_plot
from cv.layouts import (
    about_me_cv_tab,
    app_cv,
    books_tab,
    certifications_tab,
    education_tab,
    hobby_tab,
    industry_tab,
    shows_tab,
    teaching_tab,
)
from main.layouts import (
    about_me_tab,
    app_1,
    app_2,
    app_event,
    articles_tab,
    change_tab,
    changes_tab,
    chat_tab,
    chess_tab,
    contact_tab,
    event_tab,
    image_edit_tab,
    mbti_tab,
    rng_tab,
    trade_tab,
    trip_tab,
    wnrs_tab,
    wordle_tab,
)


def register_callbacks(app, print_function):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    @print_callback(print_function)
    def display_page(pathname: str) -> html.Div:
        """Display page based on URL

        Args:
            pathname: url path

        Returns:
            page display
        """
        if pathname == "/":
            return app_1()
        elif pathname == "/event":
            return app_event()
        elif pathname == "/cv":
            return app_cv()
        else:
            return app_2(pathname)

    @app.callback(
        [
            Output("sidebar", "style"),
            Output("banner", "style"),
            Output("tab-content", "style"),
        ],
        [Input("button-sidebar", "n_clicks"), Input("tabs-parent", "value")],
        [
            State("sidebar", "style"),
            State("banner", "style"),
            State("tab-content", "style"),
        ],
    )
    @print_callback(print_function)
    def display_sidebar_mobile(
        trigger_sidebar, trigger_tab, style_sidebar, style_banner, style_contents
    ):
        """Display sidebar on icon click (mobile device)

        Args:
            trigger_sidebar: trigger on button click on sidebar
            trigger_tab: trigger on tab change
            style_sidebar: current style of sidebar
            style_banner: current style of banner
            style_contents: current style of tab content

        Returns:
        3-element tuple

        - (dict): updated style of sidebar
        - (dict): updated style of banner
        - (dict): updated style of tab content
        """
        if ctx.triggered_id == "button-sidebar":
            if (
                isinstance(style_sidebar, dict)
                and style_sidebar["display"] == "inline-block"
            ):
                # Collapse left sidebar
                style_sidebar["display"] = "none"
                style_banner["margin-left"] = "0"
                style_contents["margin-left"] = "0"
                style_contents["position"] = "absolute"
            else:
                # First assignment, show left sidebar
                style_sidebar = {"display": "inline-block"}
                style_banner = {"margin-left": "85vw"}
                style_contents = {"margin-left": "85vw", "position": "fixed"}
        elif ctx.triggered_id == "tabs-parent":
            if isinstance(style_sidebar, dict):
                # Collapse left sidebar
                style_sidebar = {"display": "none"}
                style_banner = {"margin-left": "0"}
                style_contents = {"margin-left": "0", "position": "absolute"}
        return style_sidebar, style_banner, style_contents

    @app.callback(
        [
            Output("input-contact-name", "value"),
            Output("input-contact-email", "value"),
            Output("input-contact-content", "value"),
            Output("contact-reply", "children"),
        ],
        [Input("button-contact-ok", "n_clicks")],
        [
            State("input-contact-name", "value"),
            State("input-contact-email", "value"),
            State("input-contact-content", "value"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_contact_send_email(
        trigger, contact_name: str, contact_email: str, contact_content: str
    ) -> Tuple[str, str, str, str]:
        """Send email for contact information

        Args:
            trigger: trigger on button click
            contact_name: input for contact name
            contact_email: input for contact email
            contact_content: input for email body

        Returns:
            feedback for email sent
        """
        reply = ""
        if dash.callback_context.triggered:
            if contact_name is None or contact_name.strip() == "":
                reply = return_message["email_empty_name"]
            elif contact_email is None or contact_email.strip() == "":
                reply = return_message["email_empty_email"]
            elif not valid_email(contact_email):
                reply = return_message["email_email_valid"]
            elif contact_content is None or contact_content.strip() == "":
                reply = return_message["email_empty_body"]
            else:
                status_code = send_email(
                    f"Name: {contact_name}\n\nEmail: {contact_email}\n\n{contact_content}"
                )
                if status_code:
                    contact_content = ""
                    reply = return_message["email_sent_feedback"]
                else:
                    reply = return_message["email_fail"]
        return contact_name, contact_email, contact_content, reply

    @app.callback(
        Output("tab-content", "children"),
        [Input("tabs-parent", "value")],
        [State("tabs-parent", "children"), State("tab-content", "children")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_output(
        tab, children: List, current_content: html.Div
    ) -> Union[html.Div, dcc.Location]:
        """Update content when tab changes

        Args:
            tab: trigger on tab change
            children: list of available tab contents
            current_content: current tab content

        Returns:
            content of tab
        """
        available_tabs = [tab]
        if children:
            available_tabs = [
                children[idx]["props"]["value"] for idx in range(len(children))
            ]
        if tab not in available_tabs:
            return dcc_loading(violin_plot(), dark_bg=False)
        if tab == "tab-aboutme":
            return about_me_tab(app)
        elif tab == "tab-articles":
            return articles_tab()
        elif tab == "tab-change":
            return change_tab(app)
        elif tab == "tab-change2":
            return changes_tab(app)
        elif tab == "tab-chat":
            return chat_tab(app)
        elif tab == "tab-trip":
            return trip_tab(app)
        elif tab == "tab-mbti":
            return mbti_tab()
        elif tab == "tab-trade":
            return trade_tab()
        elif tab == "tab-image":
            return image_edit_tab(app)
        elif tab == "tab-contact":
            return contact_tab()
        elif tab == "tab-others":
            return dcc.Location(pathname="/event", id="some_id")
        elif tab == "tab-event":
            return event_tab(app)
        elif tab == "tab-rng":
            return rng_tab()
        elif tab == "tab-wnrs":
            return wnrs_tab(app)
        elif tab == "tab-chess":
            return chess_tab(app)
        elif tab == "tab-wordle":
            return wordle_tab(app)
        # CV
        elif tab == "tab-cv-aboutme":
            return about_me_cv_tab(app)
        elif tab == "tab-cv-industry":
            return industry_tab(app)
        elif tab == "tab-cv-teaching":
            return teaching_tab(app)
        elif tab == "tab-cv-education":
            return education_tab(app)
        elif tab == "tab-cv-certifications":
            return certifications_tab(app)
        elif tab == "tab-cv-books":
            return books_tab(app)
        elif tab == "tab-cv-shows":
            return shows_tab(app)
        elif tab == "tab-cv-hobby":
            return hobby_tab(app)
        else:
            return current_content

    app.clientside_callback(
        """
        function(tab_value) {
            if (tab_value === 'tab-aboutme') {
                document.title = 'About Me'
            } else if (tab_value === 'tab-articles') {
                document.title = 'Articles'
            } else if (tab_value === 'tab-change') {
                document.title = 'Change Calculator'
            } else if (tab_value === 'tab-change2') {
                document.title = 'Change Calculator 2'
            } else if (tab_value === 'tab-chat') {
                document.title = 'Chat Analyzer'
            } else if (tab_value === 'tab-trip') {
                document.title = 'Trip Planner'
            } else if (tab_value === 'tab-mbti') {
                document.title = 'MBTI Personality Test'
            } else if (tab_value === 'tab-trade') {
                document.title = 'Live Trading'
            } else if (tab_value === 'tab-event') {
                document.title = 'Event Planner'
            } else if (tab_value === 'tab-rng') {
                document.title = 'Random Generator'
            } else if (tab_value === 'tab-wnrs') {
                document.title = 'WNRS Card Game'
            } else if (tab_value === 'tab-chess') {
                document.title = 'Chess'
            } else if (tab_value === 'tab-wordle') {
                document.title = 'Wordle'
            } else if (tab_value === 'tab-contact') {
                document.title = 'Contact Me'
            } else if (tab_value === 'tab-image') {
                document.title = 'Image Editing'
            } else if (tab_value === 'tab-cv-aboutme') {
                document.title = 'About Me'
            } else if (tab_value === 'tab-cv-industry') {
                document.title = 'Industry'
            } else if (tab_value === 'tab-cv-teaching') {
                document.title = 'Teaching'
            } else if (tab_value === 'tab-cv-education') {
                document.title = 'Education'
            } else if (tab_value === 'tab-cv-certifications') {
                document.title = 'Certifications'
            } else if (tab_value === 'tab-cv-books') {
                document.title = 'Bookshelf'
            } else if (tab_value === 'tab-cv-shows') {
                document.title = 'Shows'
            } else if (tab_value === 'tab-cv-hobby') {
                document.title = 'Hobbies'
            }
        }
        """,
        Output("blank-output", "children"),
        [Input("tabs-parent", "value")],
    )

    app.clientside_callback(
        """
        function(trigger) {
            if (!window.hasResizeListener) {
                window.hasResizeListener = true;

                // Debounce function to prevent overloading Dash callbacks
                let timeout;
                window.addEventListener('resize', () => {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => {
                        const triggerEl = document.getElementById('resize-trigger');
                        if (triggerEl) triggerEl.click();
                    }, 150); // Fires 150ms after user stops resizing
                });
            }
            return window.innerWidth;
        }
        """,
        Output("resize-trigger", "children"),
        Input("resize-trigger", "n_clicks"),
    )
