import chess
from dash import ctx
from dash.dependencies import ALL, Input, Output, State

from common.components.helper import print_callback
from main.components.chess_game import CONFIG, ChessGame


def register_callbacks_chess(app, print_function):
    @app.callback(
        Output("chess-state", "data"),
        Input({"type": "chess-square", "square": ALL}, "n_clicks"),
        Input("chess-new-game", "n_clicks"),
        State({"type": "chess-square", "square": ALL}, "id"),
        State("chess-state", "data"),
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def handle_move(square_clicks, new_game_clicks, square_ids, state):
        """Board is always reconstructed from the FEN stored in dcc.Store"""
        if ctx.triggered_id == "chess-new-game":
            return ChessGame().get_initial_state()

        if not isinstance(ctx.triggered_id, dict):
            return state

        chess_game = ChessGame(state)
        clicked_square = ctx.triggered_id["square"]
        return chess_game.compute_new_state(clicked_square)

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
        chess_game = ChessGame(state)
        board = chess_game.board
        board_component = chess_game.render(
            selected_square=state.get("selected_square")
        )
        history_component = chess_game.history_to_components(state.get("history", []))

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

        return board_component, history_component, status
