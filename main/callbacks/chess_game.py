import json
from typing import Union

import chess
from dash import ctx
from dash.dependencies import ALL, Input, Output, State

from common.components.helper import parse_data, print_callback, return_message
from main.components.chess_game import ChessGame


def register_callbacks_chess(app, print_function):
    @app.callback(
        [
            Output("chess-state", "data"),
            Output("input-chess", "value"),
            Output("chess-status", "children"),
            Output("chess-switch", "checked"),
        ],
        Input({"type": "chess-square", "square": ALL}, "n_clicks"),
        Input("chess-new-game", "n_clicks"),
        Input("chess-undo", "n_clicks"),
        Input("chess-switch", "checked"),
        Input("uploadchess-button", "contents"),
        State("uploadchess-button", "filename"),
        State({"type": "chess-square", "square": ALL}, "id"),
        State("chess-state", "data"),
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def handle_move(
        square_clicks,
        new_game_clicks,
        undo_clicks,
        computer_toggle: bool,
        contents: str,
        filename: str,
        square_ids: list[dict[str, Union[str, int]]],
        state: dict,
    ):
        """Board is always reconstructed from the FEN stored in dcc.Store. There are 5 triggers

        - Click on board
        - New game
        - Undo
        - Toggle play with computer
        - Upload
        """
        if ctx.triggered_id in ["chess-new-game", "chess-switch"]:
            state = None

        if ctx.triggered_id == "uploadchess-button":
            if "json" not in filename:
                error_message = return_message["file_not_uploaded_json"]
                return (
                    {"error": error_message},
                    "",
                    error_message,
                    computer_toggle,
                )
            try:
                data = parse_data(contents, filename)
                data = json.loads(data.decode("utf-8"))
                chess_game = ChessGame.from_moves(
                    data["moves"].split(","), data["computer"]
                )
            except (KeyError, chess.InvalidMoveError):
                error_message = return_message["wrong_format_json"]
                return (
                    {"error": error_message},
                    "",
                    error_message,
                    computer_toggle,
                )
        else:
            # Game in error state
            if state and "error" in state:
                return state, ""
            chess_game = ChessGame.from_state(state, computer=computer_toggle)

        if ctx.triggered_id == "chess-undo":
            chess_game.undo()
        if isinstance(ctx.triggered_id, dict):
            clicked_square = ctx.triggered_id["square"]
            chess_game.move(clicked_square)
        return (
            chess_game.state,
            chess_game.convert_to_save_format(),
            chess_game.status,
            chess_game.computer_playing,
        )

    @app.callback(
        Output("chess-container", "children"),
        Output("chess-history", "children"),
        Input("chess-state", "data"),
    )
    @print_callback(print_function)
    def update_display(state):
        """Update display of UI components

        Args:
            state: updated state of chess game

        Returns:
            board display, history record, status of game
        """
        if "error" in state:
            state = None

        chess_game = ChessGame(state)
        board_component = chess_game.render(
            selected_square=chess_game.state.get("selected_square")
        )
        history_component = chess_game.history_to_components(
            chess_game.state.get("history", [])
        )
        return board_component, history_component
