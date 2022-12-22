import traceback

from dash.dependencies import Input, Output, State

from components import MBTI
from components.helper import print_callback


def register_callbacks(app, print_function):
    @app.callback(
        Output("text-mbti-words", "children"),
        [Input("input-mbti", "value")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_mbti_words(input_text):
        """Update number of input words in vocabulary

        Args:
            input_text (str): input text

        Returns:
            (str)
        """
        try:
            n_words = MBTI().get_num_words(input_text)
            return f"{n_words} word(s) in vocabulary"
        except Exception as e:
            return f"Error loading number of word(s), error message: {e}"

    @app.callback(
        [
            Output("graph-mbti", "figure"),
            Output("graph-mbti", "style"),
            Output("mbti-results", "children"),
            Output("mbti-result-error", "children"),
        ],
        [Input("button-mbti-ok", "n_clicks")],
        [State("input-mbti", "value"), State("graph-mbti", "style")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_mbti_result(trigger, input_text, style):
        """Update results of mbti personality results and graph

        Args:
            trigger: trigger on button click
            input_text (str): input text
            style (dict): style of graphical result of mbti model

        Returns:
            3-element tuple

            - (dict): graphical result of mbti model
            - (dict): updated style of graphical result of mbti model
            - (list): result of mbti model
        """
        plot = {}
        style["display"] = "none"
        personality_details = []
        error = ""
        if trigger:
            try:
                personality, predictions = MBTI().test_pipeline(input_text)
                plot = MBTI().get_bar_plot(predictions)
                personality_details = MBTI().get_personality_details(personality)
                style["display"] = "block"
                style["height"] = 400
            except Exception as e:
                error = str(e)
                print(traceback.print_exc())
        return plot, style, personality_details, error
