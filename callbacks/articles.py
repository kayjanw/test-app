from dash.dependencies import ALL, MATCH, Input, Output, State

from components.helper import hide_style, print_callback


def register_callbacks_articles(app, print_function):
    @app.callback(
        Output({"type": "button-article", "id": MATCH}, "style"),
        [
            Input({"type": "button-article", "id": MATCH}, "n_clicks"),
        ],
        [
            State({"type": "button-article", "id": MATCH}, "style"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_button_colour(trigger, button_style):
        """Update button colour on button click

        Args:
            trigger: trigger on button click
            button_style (dict): current style of buttons

        Returns:
            (dict)
        """
        empty_button_style = {
            "color": "black",
            "background-color": "white",
            "border": "1px solid black",
        }
        if not trigger % 2:
            if "background-color" in button_style:
                del button_style["color"]
                del button_style["background-color"]
                del button_style["border"]
        else:
            button_style.update(empty_button_style)
        return button_style

    @app.callback(
        Output({"type": "card-article", "id": ALL, "idx": ALL}, "style"),
        [
            Input({"type": "button-article", "id": ALL}, "style"),
        ],
        [
            State({"type": "button-article", "id": ALL}, "id"),
            State({"type": "card-article", "id": ALL, "idx": ALL}, "id"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_article_visibility(button_styles, button_ids, card_ids):
        """Update article visibility on button click

        Args:
            button_styles (dict): current style of buttons
            button_ids (list): current id of buttons
            card_ids (list): current id of cards

        Returns:
            (dict, dict)
        """
        invisible_styles = []
        for _button_id, _style in zip(button_ids, button_styles):
            if "background-color" in _style:
                invisible_styles.append(_button_id["id"])

        card_styles = []
        for card_id in card_ids:
            if card_id["id"] in invisible_styles:
                card_styles.append(hide_style)
            else:
                card_styles.append(None)
        return card_styles
