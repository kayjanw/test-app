from typing import List, Union

import dash
from dash import ctx, dcc, html
from dash.dependencies import Input, Output, State

from components.helper import (
    dcc_loading,
    print_callback,
    return_message,
    send_email,
    valid_email,
    violin_plot,
)
from layouts import (
    about_me_tab,
    app_1,
    app_2,
    app_event,
    articles_tab,
    change_tab,
    changes_tab,
    chat_tab,
    contact_tab,
    event_tab,
    image_edit_tab,
    mbti_tab,
    rng_tab,
    trade_tab,
    trip_tab,
    wnrs_tab,
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
    ) -> str:
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
        Output("image-canvas", "image_content"),
        [Input("upload-image", "contents")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_canvas_image(contents) -> str:
        """Update canvas with loaded image

        Args:
            contents: contents of data uploaded, triggers callback

        Returns:
            contents of data uploaded
        """
        if dash.callback_context.triggered:
            contents_type, _ = contents.split(";")
            if "image" in contents_type:
                return contents

    @app.callback(
        Output("image-canvas", "json_objects"),
        [Input("button-canvas-clear", "n_clicks")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def clear_canvas(n_clicks) -> str:
        """Clear canvas to blank state

        Args:
            n_clicks: trigger on button click

        Returns:
            (str)
        """
        strings = ['{"objects":[ ]}', '{"objects":[]}']
        if n_clicks:
            return strings[n_clicks % 2]
        return strings[0]

    @app.callback(
        Output("knob-canvas", "value"),
        [
            Input("button-image-minus", "n_clicks"),
            Input("button-image-plus", "n_clicks"),
        ],
        [State("knob-canvas", "value")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_canvas_brush_size(trigger_minus, trigger_plus, value) -> int:
        """Update canvas brush size (line width)

        Args:
            trigger_minus: trigger from button click
            trigger_plus: trigger from button click
            value: value of brush size

        Returns:
            updated value of brush size
        """
        if ctx.triggered_id == "button-image-minus":
            value -= 1
        elif ctx.triggered_id == "button-image-plus":
            value += 1
        return value

    @app.callback(
        Output("image-canvas", "lineWidth"),
        [Input("knob-canvas", "value")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_canvas_brush(value) -> int:
        """Update canvas brush size (line width)

        Args:
            value: input value of brush size

        Returns:
            updated value of brush size
        """
        return value

    @app.callback(
        Output("image-canvas", "lineColor"),
        [Input("image-color-picker", "value")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_canvas_color(value) -> str:
        """Update canvas brush colour (line colour)

        Args:
            value: input value of brush colour

        Returns:
            updated value of brush colour
        """
        if isinstance(value, dict):
            return value["hex"]
        else:
            return value

    # @app.callback(Output('image-result', 'children'),
    #               [Input('image-canvas', 'json_data')],
    #               prevent_initial_call=True,
    #               )
    # def update_canvas_result(string):
    #     """Update canvas result
    #
    #     Args:
    #         string: json data of canvas
    #
    #     Returns:
    #         (list)
    #     """
    #     import numpy as np
    #     from skimage import color, io, filters, measure
    #     from dash_canvas.utils.parse_json import parse_jsonstring
    #     from dash_canvas.utils import array_to_data_url
    #     from dash_canvas.utils.image_processing_utils import modify_segmentation
    #
    #     filename = 'http://www.image.png'
    #     img = io.imread(filename, as_gray=True)
    #     height, width = img.shape
    #     mask = img > 1.2 * filters.threshold_otsu(img)
    #     labs = measure.label(mask)
    #
    #     mask = parse_jsonstring(string, shape=(height, width))
    #     mode = 'merge'  # 'split'
    #     new_labels = modify_segmentation(labs, mask, img=img, mode=mode)
    #     new_labels = np.array(new_labels)
    #     color_labels = color.label2rgb(new_labels)
    #     uri = array_to_data_url(new_labels, dtype=np.uint8)
    #     return uri

    # @app.callback(Output('placeholder', 'children'),
    #               [Input('button_music', 'n_clicks')],
    #               prevent_initial_call=True,
    #               )
    # @print_callback(print_function)
    # def update_keyboard(trigger):
    #     if trigger:
    #         import base64
    #         sound_filename = 'assets/Music_Note/sample_sound.wav'  # replace with your own .mp3 file
    #         # sound_filename = 'assets/Music_Note/C.wav'  # replace with your own .mp3 file
    #         encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())
    #         return html.Audio(src=f'data:audio/wav;base64,{encoded_sound.decode()}', controls=False)

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
            } else if (tab_value === 'tab-contact') {
                document.title = 'Contact Me'
            } else if (tab_value === 'tab-image') {
                document.title = 'Image Editing'
            }
        }
        """,
        Output("blank-output", "children"),
        [Input("tabs-parent", "value")],
    )
