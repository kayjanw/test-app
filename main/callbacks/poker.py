from dash import ctx, html
from dash.dependencies import Input, Output, State

from common.components.helper import print_callback
from main.components.poker import Poker, render_amount
from main.model.poker import STAGES, ButtonColour


def register_callbacks_poker(app, print_function):
    @app.callback(
        [
            Output("poker-state", "data"),
            Output("poker-stage", "children"),
            Output("poker-pot", "children"),
            Output("poker-call", "children"),
            Output("poker-user-cards", "children"),
            Output("poker-cpu-cards", "children"),
            Output("poker-board-cards", "children"),
            Output("poker-output", "children"),
            Output("poker-user-chips", "children"),
            Output("poker-cpu-chips", "children"),
            # # Button looks
            Output("button-poker-newhandfold", "children"),
            Output("button-poker-checkcall", "children"),
            Output("button-poker-newhandfold", "style"),
            Output("button-poker-checkcall", "style"),
            Output("button-poker-raise", "style"),
            Output("poker-raise", "style"),
        ],
        Input("button-poker-newhandfold", "n_clicks"),
        Input("button-poker-checkcall", "n_clicks"),
        Input("button-poker-raise", "n_clicks"),
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

        if poker_game.player_moved and not poker_game.game_over:
            poker_game.cpu_move()

        if (
            poker_game.stage == STAGES[-1]
            and not poker_game.to_call
            and not poker_game.game_over
        ):
            poker_game.showdown()

        # Button display
        newhandfold_children = "Fold"
        newhandfold_style = {"backgroundColor": ButtonColour.FOLD}
        checkcall_children = "Check"
        checkcall_style = bet_style = raise_style = {"display": "unset"}
        if poker_game.to_call:
            checkcall_children = "Call"
        if poker_game.game_over:
            newhandfold_children = "New Hand"
            newhandfold_style = {"backgroundColor": ButtonColour.NEW_HAND}
            checkcall_style = bet_style = raise_style = {"display": "none"}

        return (
            poker_game.state,
            poker_game.stage,
            render_amount(poker_game.pot),
            render_amount(poker_game.to_call),
            *poker_game.render_cards(),
            [html.P(line) for line in poker_game.result.splitlines()],
            f"{render_amount(poker_game.chips_user)} ({poker_game.hand_user})",
            render_amount(poker_game.chips_cpu),
            newhandfold_children,
            checkcall_children,
            newhandfold_style,
            checkcall_style,
            bet_style,
            raise_style,
        )
