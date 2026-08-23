import json
import random
import time
from typing import Union

import chess
from dash import ctx, no_update
from dash.dependencies import ALL, MATCH, Input, Output, State

from common.components.helper import parse_data, print_callback, return_message
from main.components.chess_game import ChessGame
from main.model.chess_game import CHESS_THEMES

ORIGINAL_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def register_callbacks_chess(app, print_function):
    @app.callback(
        Output({"type": "modal-chess", "index": MATCH}, "is_open"),
        [
            Input({"type": "button-modal-chess", "index": MATCH}, "n_clicks"),
            Input({"type": "button-close-modal-chess", "index": MATCH}, "n_clicks"),
        ],
        State({"type": "modal-chess", "index": MATCH}, "is_open"),
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
            Output("chess-state", "data", allow_duplicate=True),
            Output("chess-status", "children", allow_duplicate=True),
            Output("chess-move", "data", allow_duplicate=True),
            Output("input-chess", "value"),
            Output("chess-difficulty", "value"),
        ],
        Input({"type": "chess-square", "square": ALL}, "n_clicks"),
        Input("chess-new-game", "n_clicks"),
        Input("chess-style", "n_clicks"),
        Input("chess-random-game", "n_clicks"),
        Input("chess-undo", "n_clicks"),
        Input("chess-difficulty", "value"),
        Input("uploadchess-button", "contents"),
        State("uploadchess-button", "filename"),
        State({"type": "chess-square", "square": ALL}, "id"),
        State("chess-state", "data"),
        State("chess-move", "data"),
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def handle_move(
        square_clicks,
        new_game_clicks,
        style_clicks,
        random_game_clicks,
        undo_clicks,
        computer_difficulty: int,
        contents: str,
        filename: str,
        square_ids: list[dict[str, Union[str, int]]],
        state: dict,
        chess_move,
    ):
        """Board is always reconstructed from the FEN stored in dcc.Store. There are 5 triggers

        - Click on board
        - New game
        - Undo
        - Toggle play with computer
        - Upload

        Returns:
            game data, status of game, computer move, game save format, updated computer toggle
        """
        if chess_move:
            return no_update, no_update, no_update, no_update, no_update

        is_random = False
        current_style = state["style"]
        computer_move = ""

        if ctx.triggered_id == "chess-new-game":
            state = None

        if ctx.triggered_id == "chess-random-game":
            state = None
            is_random = True

        if ctx.triggered_id == "chess-difficulty":
            if (state["computer"] or computer_difficulty) and not (
                state["computer"] and computer_difficulty
            ):
                state = None

        if ctx.triggered_id == "uploadchess-button":
            if "json" not in filename:
                error_message = return_message["file_not_uploaded_json"]
                return (
                    {"error": error_message, "style": current_style},
                    error_message,
                    computer_move,
                    "",
                    computer_difficulty,
                )
            try:
                data = parse_data(contents, filename)
                data = json.loads(data.decode("utf-8"))
                chess_game = ChessGame.from_moves(
                    data.get("fen", ORIGINAL_FEN),
                    data["moves"].split(","),
                    data["computer"],
                    data.get("style", "normal"),
                )
            except (KeyError, chess.InvalidMoveError):
                error_message = return_message["wrong_format_json"]
                return (
                    {"error": error_message, "style": current_style},
                    error_message,
                    computer_move,
                    "",
                    computer_difficulty,
                )
        else:
            # Game in error state
            if state and "error" in state:
                return state, "", state["error"], computer_difficulty
            chess_game = ChessGame.from_state(
                state,
                computer=computer_difficulty,
                style=current_style,
                is_random=is_random,
            )

        if ctx.triggered_id == "chess-undo":
            chess_game.undo()
        if ctx.triggered_id == "chess-style":
            styles = CHESS_THEMES
            current_style = chess_game.state["style"]
            chess_game.state["style"] = styles[styles.index(current_style) + 1]
        if isinstance(ctx.triggered_id, dict):
            clicked_square = ctx.triggered_id["square"]
            computer_move = chess_game.move(chess_game.selected_square, clicked_square)
        return (
            chess_game.state,
            chess_game.status,
            str(computer_move) if computer_move else "",
            chess_game.convert_to_save_format(),
            chess_game.computer_difficulty,
        )

    @app.callback(
        [
            Output("chess-state", "data", allow_duplicate=True),
            Output("chess-status", "children", allow_duplicate=True),
            Output("chess-move", "data", allow_duplicate=True),
        ],
        Input("chess-move", "data"),
        State("chess-state", "data"),
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def handle_computer_move(
        chess_move,
        state,
    ):
        if chess_move:
            time.sleep(random.random())
            chess_game = ChessGame.from_state(
                state,
                computer=state["computer"],
                style=state["style"],
            )
            chess_game._move(chess_move)
            return state, chess_game.status, ""
        return no_update, no_update, no_update

    @app.callback(
        Output("chess-container", "children"),
        Output("chess-history", "children"),
        Output("chess-captured", "children"),
        Input("chess-state", "data"),
    )
    @print_callback(print_function)
    def update_display(state):
        """Update display of UI components that does not rely on game move history

        Args:
            state: updated state of chess game

        Returns:
            board display, history, captured pieces
        """
        current_style = state["style"]
        if "error" in state:
            state = None

        chess_game = ChessGame(state)
        chess_game.state["style"] = current_style
        board_component = chess_game.render(app)
        history_component = chess_game.history_to_components()
        captured_pieces_component = chess_game.render_captured_pieces(app)
        return board_component, history_component, captured_pieces_component

    @app.callback(
        Output("chess-difficulty", "color"),
        Input("chess-difficulty", "value"),
    )
    @print_callback(print_function)
    def update_difficulty_color(value):
        return {
            0: "black",
            1: "green",
            2: "#FFAA33",
            3: "#FF0000",
        }[value]
