import json

import dash
from dash import ALL, MATCH, html
from dash.dependencies import Input, Output, State

from components import WNRS
from components.helper import (
    decode_dict,
    encode_dict,
    hide_button_style,
    hide_style,
    inline_style,
    parse_data,
    print_callback,
    return_message,
    send_email,
    show_button_style,
)


def register_callbacks(app, print_function):
    @app.callback(
        [
            Output("div-wnrs-selection", "style"),
            Output("div-wnrs-instruction", "style"),
            Output("div-wnrs-suggestion", "style"),
            Output("button-wnrs-show-ok", "style"),
            Output("button-wnrs-instruction-ok", "style"),
            Output("button-wnrs-suggestion-ok", "style"),
        ],
        [
            Input("button-wnrs-show-ok", "n_clicks"),
            Input("button-wnrs-instruction-ok", "n_clicks"),
            Input("button-wnrs-suggestion-ok", "n_clicks"),
        ],
        [
            State("div-wnrs-selection", "style"),
            State("div-wnrs-instruction", "style"),
            State("div-wnrs-suggestion", "style"),
            State("button-wnrs-show-ok", "style"),
            State("button-wnrs-instruction-ok", "style"),
            State("button-wnrs-suggestion-ok", "style"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_wnrs_deck_style(
        trigger_selection,
        trigger_instruction,
        trigger_suggestion,
        selection_style,
        instruction_style,
        suggestion_style,
        selection_button_style,
        instruction_button_style,
        suggestion_button_style,
    ):
        """Update style of WNRS card selection and card suggestion (visibility)

        Args:
            trigger_selection: trigger on button click
            trigger_instruction: trigger on button click
            trigger_suggestion: trigger on button click
            selection_style (dict): current style of card selection div
            instruction_style (dict): current style of instruction div
            suggestion_style (dict): current style of card suggestion div
            selection_button_style(dict): current style of card selection button
            instruction_button_style (dict): current style of instruction button
            suggestion_button_style (dict): current style of card suggestion button

        Returns:
            dict: updated style of card selection, instruction and card suggestion div and button
        """
        if dash.callback_context.triggered:
            ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
            if ctx == "button-wnrs-show-ok":
                if selection_style["display"] == "inline-block":
                    selection_style.update(hide_style)
                    selection_button_style.update(hide_button_style)
                else:
                    selection_style.update(inline_style)
                    selection_button_style.update(show_button_style)
                instruction_style.update(hide_style)
                instruction_button_style.update(hide_button_style)
                suggestion_style.update(hide_style)
                suggestion_button_style.update(hide_button_style)
            elif ctx == "button-wnrs-instruction-ok":
                if instruction_style["display"] == "inline-block":
                    instruction_style.update(hide_style)
                    instruction_button_style.update(hide_button_style)
                else:
                    instruction_style.update(inline_style)
                    instruction_button_style.update(show_button_style)
                selection_style.update(hide_style)
                selection_button_style.update(hide_button_style)
                suggestion_style.update(hide_style)
                suggestion_button_style.update(hide_button_style)
            elif ctx == "button-wnrs-suggestion-ok":
                if suggestion_style["display"] == "inline-block":
                    suggestion_style.update(hide_style)
                    suggestion_button_style.update(hide_button_style)
                else:
                    suggestion_style.update(inline_style)
                    suggestion_button_style.update(show_button_style)
                selection_style.update(hide_style)
                selection_button_style.update(hide_button_style)
                instruction_style.update(hide_style)
                instruction_button_style.update(hide_button_style)
        return (
            selection_style,
            instruction_style,
            suggestion_style,
            selection_button_style,
            instruction_button_style,
            suggestion_button_style,
        )

    @app.callback(
        [
            Output("input-wnrs-suggestion", "value"),
            Output("input-wnrs-suggestion2", "value"),
            Output("wnrs-suggestion-reply", "children"),
        ],
        [Input("button-wnrs-send-ok", "n_clicks")],
        [
            State("input-wnrs-suggestion", "value"),
            State("input-wnrs-suggestion2", "value"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_wnrs_suggestion_send_email(trigger, card_prompt, additional_info):
        """Send email for WNRS card suggestion

        Args:
            trigger: trigger on button click
            card_prompt (str): input for card prompt
            additional_info (str): input for additional information

        Returns:
            str: feedback for email sent
        """
        reply = ""
        if dash.callback_context.triggered:
            if card_prompt is None or card_prompt.strip() == "":
                reply = return_message["card_not_filled"]
            else:
                status_code = send_email(f"{card_prompt}\n\n{additional_info}")
                if status_code:
                    card_prompt = ""
                    additional_info = ""
                    reply = return_message["email_sent_suggestion"]
                else:
                    reply = return_message["email_fail"]
        return card_prompt, additional_info, reply

    @app.callback(
        Output({"type": "wnrs-deck-button", "id": MATCH}, "style"),
        [Input({"type": "wnrs-deck-button", "id": MATCH}, "n_clicks")],
        [State({"type": "wnrs-deck-button", "id": MATCH}, "style")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_wnrs_button_style(trigger, current_style):
        """Update style of selected WNRS decks (button colour indication)

        Args:
            trigger: trigger on button click
            current_style (dict): current style of button

        Returns:
            dict: updated style of button
        """
        if dash.callback_context.triggered:
            if current_style is None:
                current_style = dict()
            if (
                "background-color" in current_style
                and current_style["background-color"] == "#BE9B89"
            ):
                current_style["background-color"] = "#F0E3DF"
            else:
                current_style["background-color"] = "#BE9B89"
        return current_style

    @app.callback(
        Output("intermediate-wnrs", "data"),
        [Input({"type": "wnrs-deck-button", "id": ALL}, "style")],
        [Input({"type": "wnrs-deck-button", "id": ALL}, "id")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_wnrs_list_of_decks(styles, ids):
        """Update list of decks selected

        Args:
            args (dict): current style of all buttons

        Returns:
            dict: updated style of all buttons
        """
        data = {}
        list_of_deck = []
        for _style, _id in zip(styles, ids):
            if _style is not None and _style["background-color"] == "#BE9B89":
                list_of_deck.append(_id["id"])
        if len(list_of_deck):
            wnrs_game = WNRS()
            wnrs_game.initialize_game(list_of_deck)
            data = dict(list_of_deck=list_of_deck, wnrs_game_dict=wnrs_game.__dict__)
        return data

    @app.callback(
        [
            Output("input-wnrs", "value"),
            Output("wnrs-prompt", "children"),
            Output("wnrs-reminder-text", "children"),
            Output("wnrs-reminder", "children"),
            Output("wnrs-deck", "children"),
            Output("wnrs-counter", "children"),
            Output("wnrs-card", "style"),
            Output("button-wnrs2-back", "style"),
            Output("button-wnrs2-next", "style"),
        ],
        [
            Input("button-wnrs-back", "n_clicks"),
            Input("button-wnrs-next", "n_clicks"),
            Input("button-wnrs2-back", "n_clicks"),
            Input("button-wnrs2-next", "n_clicks"),
            Input("button-wnrs-shuffle-ok", "n_clicks"),
            Input("intermediate-wnrs", "data"),
            Input("uploadbutton-wnrs", "contents"),
        ],
        [
            State("uploadbutton-wnrs", "filename"),
            State("input-wnrs", "value"),
            State("wnrs-prompt", "children"),
            State("wnrs-card", "style"),
            State("button-wnrs2-back", "style"),
            State("button-wnrs2-next", "style"),
        ],
    )
    @print_callback(print_function)
    def update_wnrs_card(
        trigger_back,
        trigger_next,
        trigger_back2,
        trigger_next2,
        trigger_shuffle,
        data,
        contents,
        filename,
        data2_ser,
        card_prompt,
        current_style,
        button_back,
        button_next,
    ):
        """Update underlying data, card content and style

        Args:
            trigger_back: trigger on button click
            trigger_next: trigger on button click
            trigger_back2: trigger on button click
            trigger_next2: trigger on button click
            trigger_shuffle: trigger on button click
            data (dict): data of WNRS object
            contents (str): contents of data uploaded, triggers callback
            filename (str): filename of data uploaded
            data2_ser (str): serialized data of WNRS object
            card_prompt (str/list): current prompt on card
            current_style (dict): current style of card
            button_back (dict): current opacity for back button
            button_next (dict): current opacity for next button

        Returns:
            str, str, str, dict, str, str, str, dict, dict
        """
        card_prompt, card_deck, card_counter, data_new = (
            [card_prompt, "", ""],
            "",
            "- / -",
            {},
        )
        next_card = 0
        if dash.callback_context.triggered:
            ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
            data2 = decode_dict(data2_ser)
            if ctx == "intermediate-wnrs":
                if "wnrs_game_dict" not in data:
                    card_prompt[0] = html.P(return_message["card_not_select"])
                else:  # dummy callback
                    data_new = data.copy()
            elif ctx == "uploadbutton-wnrs":
                if "json" not in filename:
                    card_prompt[0] = html.P(return_message["file_not_uploaded_json"])
                else:
                    data = parse_data(contents, filename)
                    data = json.loads(data.decode("utf-8"))
                    try:
                        wnrs_game = WNRS()
                        wnrs_game.load_game(
                            data["list_of_deck"], data["pointer"], data["index"]
                        )
                        data_new = dict(
                            list_of_deck=data["list_of_deck"],
                            wnrs_game_dict=wnrs_game.__dict__,
                        )
                    except KeyError:
                        card_prompt[0] = html.P(return_message["wrong_format_json"])
            elif ctx in [
                "button-wnrs-back",
                "button-wnrs2-back",
                "button-wnrs-next",
                "button-wnrs2-next",
            ]:
                data_new = data2.copy()
                if not button_next.get("opacity", True):
                    if ctx.endswith("back"):
                        next_card = -1
                    elif ctx.endswith("next"):
                        next_card = 1
                else:
                    button_back = button_next = dict(opacity=0)
            elif ctx == "button-wnrs-shuffle-ok":
                data_new = data2.copy()
                next_card = 2
        elif data2_ser is None:
            print("Not triggered")
            data_new = data.copy()
        else:  # initial run
            data2 = decode_dict(data2_ser)
            data_new = data2.copy()

        if len(data_new) > 1:
            wnrs_game = WNRS()
            wnrs_game.load_game_from_dict(data_new["wnrs_game_dict"])
            if next_card == 1:
                (
                    card_deck,
                    card_prompt,
                    card_style,
                    card_counter,
                ) = wnrs_game.get_next_card()
            elif next_card == -1:
                (
                    card_deck,
                    card_prompt,
                    card_style,
                    card_counter,
                ) = wnrs_game.get_previous_card()
            elif next_card == 0:
                (
                    card_deck,
                    card_prompt,
                    card_style,
                    card_counter,
                ) = wnrs_game.get_current_card()
            elif next_card == 2:
                (
                    card_deck,
                    card_prompt,
                    card_style,
                    card_counter,
                ) = wnrs_game.shuffle_remaining_cards()
            data_new["wnrs_game_dict"] = wnrs_game.__dict__
            current_style.update(card_style)
        data_new2 = encode_dict(data_new)
        return [
            data_new2,
            *card_prompt,
            card_deck,
            card_counter,
            current_style,
            button_back,
            button_next,
        ]
