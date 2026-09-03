import random
import time

from dash import MATCH, ctx, html
from dash.dependencies import Input, Output, State

from common.components.helper import print_callback
from main.components.poker import Poker, render_amount
from main.model.poker.poker import STAGES, ButtonColour


def register_callbacks_poker(app, print_function):
    @app.callback(
        Output({"type": "modal-poker", "index": MATCH}, "is_open"),
        [
            Input({"type": "button-modal-poker", "index": MATCH}, "n_clicks"),
            Input({"type": "button-close-modal-poker", "index": MATCH}, "n_clicks"),
        ],
        State({"type": "modal-poker", "index": MATCH}, "is_open"),
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_modal_display(trigger_open, trigger_close, is_open: bool) -> bool:
        """Update modal display

        Args:
            trigger_open: trigger on button click
            trigger_close: trigger on button click
            is_open: current state of open

        Returns:
            indicator whether modal is open or not
        """
        if trigger_open or trigger_close:
            return not is_open
        return is_open

    @app.callback(
        [
            Output("poker-state", "data", allow_duplicate=True),
            Output("poker-move", "data", allow_duplicate=True),
            Output("poker-output", "children", allow_duplicate=True),
            Output("poker-pot", "children", allow_duplicate=True),
            Output("poker-call", "children", allow_duplicate=True),
            Output("poker-user-chips", "children", allow_duplicate=True),
            Output("button-poker-newhandfold", "style", allow_duplicate=True),
            Output("button-poker-checkcall", "style", allow_duplicate=True),
            Output("button-poker-betraise", "style", allow_duplicate=True),
            Output("poker-raise", "style", allow_duplicate=True),
        ],
        Input("button-poker-newhandfold", "n_clicks"),
        Input("button-poker-checkcall", "n_clicks"),
        Input("button-poker-betraise", "n_clicks"),
        [
            State("poker-state", "data"),
            State("poker-raise", "value"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_game(
        newhand_nclicks,
        checkcall_nclicks,
        raise_nclicks,
        state: dict,
        amount: int,
    ):
        """Update poker game"""
        triggered_id = ctx.triggered_id
        poker_game = Poker.from_state(state)

        if triggered_id == "button-poker-newhandfold":
            if poker_game.game_over or state["stage"] in STAGES[0]:
                poker_game.new_game()
            else:
                poker_game.fold()
        elif triggered_id == "button-poker-checkcall":
            poker_game.check_or_call()
        else:
            poker_game.bet_or_raise(amount)

        poker_move = ""
        if poker_game.player_moved and not poker_game.game_over:
            poker_move = "move"

        newhandfold_style = checkcall_style = bet_style = raise_style = {
            "display": "none"
        }
        return (
            poker_game.state,
            poker_move,
            [html.P(line) for line in poker_game.result.splitlines()],
            render_amount(poker_game.pot),
            render_amount(poker_game.to_call),
            f"{render_amount(poker_game.chips_user)} ({poker_game.hand_user})",
            newhandfold_style,
            checkcall_style,
            bet_style,
            raise_style,
        )

    @app.callback(
        [
            Output("poker-state", "data"),
            Output("poker-move", "data"),
            Output("poker-output", "children"),
            Output("poker-stage", "children"),
            Output("poker-pot", "children"),
            Output("poker-call", "children"),
            Output("poker-user-cards", "children"),
            Output("poker-cpu-cards", "children"),
            Output("poker-board-cards", "children"),
            Output("poker-user-chips", "children"),
            Output("poker-cpu-chips", "children"),
            Output("poker-user-profile", "children"),
            # Button looks
            Output("button-poker-newhandfold", "children"),
            Output("button-poker-checkcall", "children"),
            Output("button-poker-betraise", "children"),
            Output("button-poker-newhandfold", "style"),
            Output("button-poker-checkcall", "style"),
            Output("button-poker-betraise", "style"),
            Output("poker-raise", "style"),
        ],
        Input("poker-move", "data"),
        [
            State("poker-state", "data"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_game_after_computer(
        poker_move,
        state,
    ):
        poker_game = Poker.from_state(state)

        if poker_game.player_moved and not poker_game.game_over:
            time.sleep(random.random())
            poker_game.cpu_move()

        if (
            poker_game.stage == STAGES[-1]
            and not poker_game.to_call
            and not poker_game.game_over
        ):
            poker_game.showdown()
        user_profile = (
            poker_game.profile_user.profile_type if poker_game.total_hands >= 10 else ""
        )
        # print(poker_game.profile_user.__dict__)

        # Button display
        newhandfold_children = "Fold"
        newhandfold_style = {"backgroundColor": ButtonColour.FOLD}
        checkcall_children = "Check"
        checkcall_style = bet_style = raise_style = {"display": "unset"}
        betraise_children = "Raise"
        if poker_game.to_call:
            checkcall_children = "Call"
        if poker_game.is_user_bet:
            betraise_children = "Bet"
        if poker_game.game_over:
            newhandfold_children = "New Hand"
            newhandfold_style = {"backgroundColor": ButtonColour.NEW_HAND}
            checkcall_style = bet_style = raise_style = {"display": "none"}

        return (
            poker_game.state,
            "",
            [html.P(line) for line in poker_game.result.splitlines()],
            poker_game.stage,
            render_amount(poker_game.pot),
            render_amount(poker_game.to_call),
            *poker_game.render_cards(),
            f"{render_amount(poker_game.chips_user)} ({poker_game.hand_user})",
            render_amount(poker_game.chips_cpu),
            [html.P(line, className="p-tight") for line in user_profile.splitlines()],
            newhandfold_children,
            checkcall_children,
            betraise_children,
            newhandfold_style,
            checkcall_style,
            bet_style,
            raise_style,
        )
