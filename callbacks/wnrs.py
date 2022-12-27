import json

import dash
from dash import ALL, MATCH, ctx, html
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
            Output("button-wnrs-show-ok", "style"),
            Output("button-wnrs-instruction-ok", "style"),
        ],
        [
            Input("button-wnrs-show-ok", "n_clicks"),
            Input("button-wnrs-instruction-ok", "n_clicks"),
        ],
        [
            State("div-wnrs-selection", "style"),
            State("div-wnrs-instruction", "style"),
            State("button-wnrs-show-ok", "style"),
            State("button-wnrs-instruction-ok", "style"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_wnrs_deck_style(
        trigger_selection,
        trigger_instruction,
        selection_style,
        instruction_style,
        selection_button_style,
        instruction_button_style,
    ):
        """Update style of WNRS card selection and card suggestion (visibility)

        Args:
            trigger_selection: trigger on button click
            trigger_instruction: trigger on button click
            selection_style (dict): current style of card selection div
            instruction_style (dict): current style of instruction div
            selection_button_style(dict): current style of card selection button
            instruction_button_style (dict): current style of instruction button

        Returns:
            dict: updated style of card selection, instruction and card suggestion div and button
        """
        if dash.callback_context.triggered:
            if ctx.triggered_id == "button-wnrs-show-ok":
                if selection_style["display"] == "inline-block":
                    selection_style.update(hide_style)
                    selection_button_style.update(hide_button_style)
                else:
                    selection_style.update(inline_style)
                    selection_button_style.update(show_button_style)
                instruction_style.update(hide_style)
                instruction_button_style.update(hide_button_style)
            elif ctx.triggered_id == "button-wnrs-instruction-ok":
                if instruction_style["display"] == "inline-block":
                    instruction_style.update(hide_style)
                    instruction_button_style.update(hide_button_style)
                else:
                    instruction_style.update(inline_style)
                    instruction_button_style.update(show_button_style)
                selection_style.update(hide_style)
                selection_button_style.update(hide_button_style)
        return (
            selection_style,
            instruction_style,
            selection_button_style,
            instruction_button_style,
        )

    @app.callback(
        Output({"type": "modal-wnrs", "index": MATCH}, "is_open"),
        [
            Input({"type": "button-modal-wnrs", "index": MATCH}, "n_clicks"),
            Input({"type": "button-close-modal-wnrs", "index": MATCH}, "n_clicks"),
        ],
        State({"type": "modal-wnrs", "index": MATCH}, "is_open"),
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_modal_display(trigger_open, trigger_close, is_open):
        """Update modal display

        Args:
            trigger_open: trigger on button click
            trigger_close: trigger on button click
            is_open (bool): current state of open

        Returns:
            (bool)
        """
        if trigger_open or trigger_close:
            return not is_open
        return is_open

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
        shaded_colour = "#BE9B89"
        unshaded_colour = "#F0E3DF"
        if dash.callback_context.triggered:
            if current_style is None:
                current_style = dict()
            if (
                "background-color" in current_style
                and current_style["background-color"] == shaded_colour
            ):
                current_style["background-color"] = unshaded_colour
            else:
                current_style["background-color"] = shaded_colour
        return current_style

    @app.callback(
        [Output("intermediate-wnrs", "data"), Output("uploadwnrs-button", "contents")],
        [Input({"type": "wnrs-deck-button", "id": ALL}, "style")],
        [Input({"type": "wnrs-deck-button", "id": ALL}, "id")],
        Input("uploadwnrs-button", "contents"),
        State("uploadwnrs-button", "filename"),
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_wnrs_list_of_decks(styles, ids, contents, filename):
        """Update list of decks selected

        Args:
            styles (dict): current style of all buttons
            ids (dict): current id of all buttons
            contents (str): contents of data uploaded, triggers callback
            filename (str): filename of data uploaded

        Returns:
            dict: updated style of all buttons
        """
        shaded_colour = "#BE9B89"
        data = {}
        list_of_deck = []
        if ctx.triggered_id == "uploadwnrs-button":  # upload past progress
            if "json" not in filename:
                data["error"] = return_message["file_not_uploaded_json"]
            else:
                data = parse_data(contents, filename)
                data = json.loads(data.decode("utf-8"))
                try:
                    wnrs_game = WNRS()
                    wnrs_game.load_game(
                        data["list_of_deck"], data["pointer"], data["index"]
                    )
                    data = dict(
                        playing_cards=wnrs_game.playing_cards,
                        list_of_deck=wnrs_game.list_of_deck,
                        pointer=wnrs_game.pointer,
                        index=wnrs_game.index,
                    )
                except KeyError:
                    data["error"] = return_message["wrong_format_json"]
        else:
            for _style, _id in zip(styles, ids):
                if _style is not None and _style["background-color"] == shaded_colour:
                    list_of_deck.append(_id["id"])
            if len(list_of_deck):
                wnrs_game = WNRS()
                wnrs_game.initialize_game(list_of_deck)
                data = dict(
                    playing_cards=wnrs_game.playing_cards,
                    list_of_deck=wnrs_game.list_of_deck,
                    pointer=wnrs_game.pointer,
                    index=wnrs_game.index,
                )
        return data, ""

    @app.callback(
        [
            Output("input-wnrs", "value"),
            Output("wnrs-prompt", "children"),
            Output("wnrs-reminder-text", "children"),
            Output("wnrs-reminder", "children"),
            Output("wnrs-deck", "children"),
            Output("wnrs-counter", "children"),
            Output("wnrs-card", "style"),
            Output("colorpicker-wnrs-text", "value"),
            Output("colorpicker-wnrs-background", "value"),
            Output("swatches-wnrs-text", "value"),
            Output("swatches-wnrs-background", "value"),
            Output("button-wnrs2-back", "style"),
            Output("button-wnrs2-next", "style"),
            Output("theme-wnrs", "data"),
        ],
        [
            Input("button-wnrs-back", "n_clicks"),
            Input("button-wnrs-next", "n_clicks"),
            Input("button-wnrs2-back", "n_clicks"),
            Input("button-wnrs2-next", "n_clicks"),
            Input("button-wnrs-shuffle-ok", "n_clicks"),
            Input("colorpicker-wnrs-text", "value"),
            Input("colorpicker-wnrs-background", "value"),
            Input("swatches-wnrs-text", "value"),
            Input("swatches-wnrs-background", "value"),
            Input("button-reset-style", "n_clicks"),
            Input("intermediate-wnrs", "data"),
        ],
        [
            State("input-wnrs", "value"),
            State("wnrs-prompt", "children"),
            State("wnrs-card", "style"),
            State("button-wnrs2-back", "style"),
            State("button-wnrs2-next", "style"),
            State("theme-wnrs", "data"),
        ],
    )
    @print_callback(print_function)
    def update_wnrs_card(
        trigger_back,
        trigger_next,
        trigger_back2,
        trigger_next2,
        trigger_shuffle,
        style_text,
        style_background,
        swatch_text,
        swatch_background,
        style_reset,
        data,
        data2_ser,
        card_prompt,
        current_style,
        button_back,
        button_next,
        theme_ind,
    ):
        """Update underlying data, card content and style

        Args:
            trigger_back: trigger on button click
            trigger_next: trigger on button click
            trigger_back2: trigger on button click
            trigger_next2: trigger on button click
            trigger_shuffle: trigger on button click
            style_text (dict): current style of card text
            style_background (dict): current style of card background
            swatch_text (str): input swatch colour of card text
            swatch_background (str): input swatch colour of card background
            style_reset: trigger on button click
            data (dict): data of WNRS object, from store data
            data2_ser (str): serialized data of WNRS object, from saved data
            card_prompt (str/list): current prompt on card
            current_style (dict): current style of card
            button_back (dict): current opacity for back button
            button_next (dict): current opacity for next button
            theme_ind (bool): indicator on whether theme is set or not

        Returns:
            str, list, list, list, list str, dict, dict, dict, dict, dict
        """
        card_prompt, card_deck, card_counter, data_new = (
            [card_prompt, "", ""],
            "",
            "- / -",
            {},
        )
        next_card = 0
        data2 = decode_dict(data2_ser)
        data_new = {}

        if dash.callback_context.triggered:
            ctx_id = ctx.triggered_id
            data2 = decode_dict(data2_ser)

            if "error" in data:
                card_prompt[0] = html.P(data["error"])
                data2 = {"error": data["error"]}
                ctx_id = ""
            if ctx_id == "intermediate-wnrs":  # new decks selected
                if "playing_cards" not in data:
                    card_prompt[0] = html.P(return_message["card_not_select"])
                    data2 = {"error": return_message["card_not_select"]}
                else:
                    data_new = dict(
                        playing_cards=data["playing_cards"],
                        list_of_deck=data["list_of_deck"],
                        pointer=data["pointer"],
                        index=data["index"],
                    )

            elif ctx_id in [
                "button-wnrs-back",
                "button-wnrs2-back",
                "button-wnrs-next",
                "button-wnrs2-next",
            ]:
                if not button_next.get("opacity", True):
                    if ctx_id.endswith("back"):
                        next_card = -1
                    elif ctx_id.endswith("next"):
                        next_card = 1
                else:
                    button_back = button_next = dict(opacity=0)
                if "playing_cards" in data:
                    data_new = dict(
                        playing_cards=data["playing_cards"],
                        list_of_deck=data2["list_of_deck"],
                        pointer=data2["pointer"],
                        index=data2["index"],
                    )

            elif ctx_id == "button-wnrs-shuffle-ok":
                if not button_next.get("opacity", True):
                    next_card = 2
                if "playing_cards" in data:
                    data_new = dict(
                        playing_cards=data["playing_cards"],
                        list_of_deck=data2["list_of_deck"],
                        pointer=data2["pointer"],
                        index=data2["index"],
                    )

            elif ctx_id in [
                "colorpicker-wnrs-text",
                "colorpicker-wnrs-background",
                "swatches-wnrs-text",
                "swatches-wnrs-background",
            ]:
                theme_ind = True
                if ctx_id == "swatches-wnrs-text":
                    style_text["hex"] = swatch_text
                elif ctx_id == "swatches-wnrs-background":
                    style_background["hex"] = swatch_background
                if "playing_cards" in data:
                    data_new = dict(
                        playing_cards=data["playing_cards"],
                        list_of_deck=data2["list_of_deck"],
                        pointer=data2["pointer"],
                        index=data2["index"],
                    )

            elif ctx_id == "button-reset-style":
                if "playing_cards" in data:
                    data_new = dict(
                        playing_cards=data["playing_cards"],
                        list_of_deck=data2["list_of_deck"],
                        pointer=data2["pointer"],
                        index=data2["index"],
                    )
                theme_ind = False

        elif data2_ser is None:
            print("Not triggered")
            data_new = {}

        else:  # initial run
            data_new = dict(
                playing_cards=data["playing_cards"],
                list_of_deck=data2["list_of_deck"],
                pointer=data2["pointer"],
                index=data2["index"],
            )

        if len(data_new) > 1:
            wnrs_game = WNRS()
            wnrs_game.load_game_from_dict(data_new)
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
            current_style.update(card_style)
            data2 = wnrs_game.convert_to_save_format()

        if theme_ind:
            current_style.update(
                {
                    "color": style_text["hex"],
                    "background-color": style_background["hex"],
                }
            )

        return [
            encode_dict(data2),
            *card_prompt,
            card_deck,
            card_counter,
            current_style,
            dict(hex=current_style["color"]),
            dict(hex=current_style["background-color"]),
            "",
            "",
            button_back,
            button_next,
            theme_ind,
        ]
