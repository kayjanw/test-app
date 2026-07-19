import json
from typing import Union

import chess
from dash import ctx
from dash.dependencies import ALL, Input, Output, State

from common.components.helper import parse_data, print_callback, return_message
from main.components.chess_game import CONFIG, ChessGame


def register_callbacks_chess(app, print_function):
    @app.callback(
        [Output("chess-state", "data"), Output("input-chess", "value")],
        Input({"type": "chess-square", "square": ALL}, "n_clicks"),
        Input("chess-new-game", "n_clicks"),
        Input("chess-undo", "n_clicks"),
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
        contents: str,
        filename: str,
        square_ids: list[dict[str, Union[str, int]]],
        state: dict,
    ):
        """Board is always reconstructed from the FEN stored in dcc.Store"""
        if ctx.triggered_id == "chess-new-game":
            state = None
        if ctx.triggered_id == "uploadchess-button":
            if "json" not in filename:
                return {"error": return_message["file_not_uploaded_json"]}, ""
            try:
                data = parse_data(contents, filename)
                data = json.loads(data.decode("utf-8"))
                chess_game = ChessGame.from_moves(data["moves"].split(","))
            except (KeyError, chess.InvalidMoveError):
                return {"error": return_message["wrong_format_json"]}, ""
        else:
            # Game in error state
            if state and "error" in state:
                return state, ""
            chess_game = ChessGame(state)

        if ctx.triggered_id == "chess-undo":
            chess_game.undo()
        if isinstance(ctx.triggered_id, dict):
            clicked_square = ctx.triggered_id["square"]
            chess_game.move(clicked_square)
        return chess_game.state, chess_game.convert_to_save_format()

    @app.callback(
        Output("chess-container", "children"),
        Output("chess-history", "children"),
        Output("chess-status", "children"),
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
        error_status = ""
        if "error" in state:
            error_status = state["error"]
            state = None

        chess_game = ChessGame(state)
        board = chess_game.board
        board_component = chess_game.render(
            selected_square=chess_game.state.get("selected_square")
        )
        history_component = chess_game.history_to_components(
            chess_game.state.get("history", [])
        )

        if board.is_checkmate():
            winner = "Black" if board.turn == chess.WHITE else "White"
            status = f"Checkmate — {winner} wins"
        elif board.is_stalemate():
            status = "Stalemate"
        elif board.is_check():
            side = "White" if board.turn == chess.WHITE else "Black"
            status = f"{side} is in check"
        else:
            side = "White" if board.turn == chess.WHITE else "Black"
            if (
                CONFIG.computer_color is not None
                and board.turn == CONFIG.computer_color
            ):
                status = f"{side} computer is thinking..."
            else:
                status = f"{side} to move"

        return board_component, history_component, error_status or status
