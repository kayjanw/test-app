import dash
from dash.dependencies import Input, Output, State

from components import RandomGenerator
from components.helper import flex_style, hide_style, print_callback, return_message


def register_callbacks(app, print_function):
    @app.callback(
        [
            Output("div-rng-item", "style"),
            Output("div-rng-group", "style"),
        ],
        [
            Input("toggle-rng", "value"),
        ],
        [
            State("div-rng-item", "style"),
            State("div-rng-group", "style"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_rng_button_style(
        trigger_toggle,
        item_style,
        group_style,
    ):
        """Update style of random generator button

        Args:
            trigger_toggle: trigger on toggle click
            item_style (dict): current style of item div
            group_style (dict): current style of group div

        Returns:
            dict: updated style of item and group button
        """
        if dash.callback_context.triggered:
            if trigger_toggle:
                item_style.update(hide_style)
                group_style.update(flex_style)
            else:
                item_style.update(flex_style)
                group_style.update(hide_style)
        return item_style, group_style

    @app.callback(
        [
            Output("rng-result-error", "children"),
            Output("div-rng-result", "style"),
            Output("div-rng-result", "children"),
        ],
        [Input("button-rng-ok", "n_clicks")],
        [
            State("input-rng", "value"),
            State("input-rng-item", "value"),
            State("input-rng-group", "value"),
            State("div-rng-item", "style"),
            State("div-rng-group", "style"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_rng_result(trigger, text, n_items, n_groups, item_style, group_style):
        """Update and display random generator results

        Args:
            trigger: trigger on button click
            text (str): input text
            n_items (int): number of items
            n_groups (int): number of groups
            item_style (dict): current style of item div
            group_style (dict): current style of group div

        Returns:
            3-element tuple

            - list: div result of random generator error (if any)
            - dict: updated style of random generator div
            - list: div result of random generator
        """
        result_error = []
        style = hide_style
        result = []
        if trigger:
            task = None
            if item_style["display"] == "flex":
                task = "item"
            elif group_style["display"] == "flex":
                task = "group"
            if text and task:
                result_error, result, style = RandomGenerator().process_result(
                    text, n_items, n_groups, task, style
                )
            elif not text:
                result_error = [return_message["input_empty"]]
            elif not task:
                result_error = [return_message["rng_task_empty"]]
        return result_error, style, result
