from __future__ import annotations

import random
from typing import Any, Optional, Union

import chess
import chess.polyglot
from dash import html
from dash_iconify import DashIconify

from common.components.helper import encode_dict
from main.model.chess_game import PIECE_UNICODE, PIECE_VALUES, ChessConfig

CONFIG = ChessConfig(computer_color=chess.BLACK, depth=2)


class ChessGame:
    def __init__(self, state: dict[str, Any] | None = None, computer: bool = False):
        self.board = chess.Board(state["fen"]) if state else chess.Board()
        self.state = state or self.get_initial_state()
        self.computer_playing = computer

    @classmethod
    def from_state(cls, state: dict[str, Any] | None = None, computer: bool = False):
        """Recreate chess game state from state, and implement moves"""
        if state:
            instance = cls.from_moves(cls._get_moves(state), computer)
            instance.state = state
            return instance
        return cls(state, computer)

    @classmethod
    def from_moves(cls, moves: list[str], computer: bool):
        """Recreate chess game state from list of moves

        Args:
            moves: list of moves in uci format
            computer: whether computer is playing

        Returns:
            reconstructed state of chess game
        """
        instance = ChessGame(computer=computer)
        for move_uci in moves:
            move = chess.Move.from_uci(move_uci)
            instance._move(move)
        return instance

    @property
    def status(self) -> str:
        """Get status of gameplay"""
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            status = f"Checkmate — {winner} wins"
        elif self.board.is_game_over():
            status = "Draw"
        elif self.board.is_stalemate():
            status = "Stalemate"
        elif self.board.is_check():
            side = "White" if self.board.turn == chess.WHITE else "Black"
            status = f"{side} is in check"
        else:
            side = "White" if self.board.turn == chess.WHITE else "Black"
            if self.computer_playing and self.board.turn == CONFIG.computer_color:
                status = "Computer is thinking..."
            else:
                status = f"{side} to move"
        return status

    def get_initial_state(self) -> dict:
        """Get initial chess game

        Returns:
            initial state of chess game
        """
        return {
            "fen": self.board.fen(),
            "selected_square": None,
            "history": [],
        }

    @staticmethod
    def _get_moves(state: dict[str, Any]) -> list[str]:
        return [history["uci"] for history in state.get("history", [])]

    def move(self, clicked_square: chess.Square) -> None:
        """Handles selecting a piece, moving a selected piece, computer response (if applicable)

        Args:
            clicked_square: current clicked square

        Returns:
            update state to new state of chess game
        """
        if self.board.is_game_over():
            return

        # Nothing is selected yet - colour the square yellow
        selected_square = self.state.get("selected_square")
        if selected_square is None:
            piece = self.board.piece_at(clicked_square)
            if piece is None or piece.color != self.board.turn:
                return
            self.state["selected_square"] = clicked_square
            return

        # Something is selected
        move = chess.Move(
            from_square=selected_square,
            to_square=clicked_square,
        )

        # Promote to queen
        if (
            self.board.piece_at(selected_square)
            and self.board.piece_at(selected_square).piece_type == chess.PAWN
            and chess.square_rank(clicked_square) in (0, 7)
        ):
            move = chess.Move(
                from_square=selected_square,
                to_square=clicked_square,
                promotion=chess.QUEEN,
            )

        if move not in self.board.legal_moves:
            clicked_piece = self.board.piece_at(clicked_square)
            # Clicking another own piece selects that piece instead
            if clicked_piece is not None and clicked_piece.color == self.board.turn:
                self.state["selected_square"] = clicked_square
            else:
                self.state["selected_square"] = None
            return

        # Human move
        self._move(move)

        # Computer move
        if (
            self.computer_playing
            and not self.board.is_game_over()
            and self.board.turn == CONFIG.computer_color
        ):
            computer_move = choose_move(
                board=self.board,
                player=CONFIG.computer_color,
                depth=CONFIG.depth,
            )
            self._move(computer_move)

    def _move(self, move: chess.Move):
        """Handle chess move"""
        san = self.board.san(move)
        captured_piece = self.board.piece_at(move.to_square)
        self.board.push(move)
        history_entry = {
            "san": san,
            "uci": move.uci(),
            "from": chess.square_name(move.from_square),
            "to": chess.square_name(move.to_square),
            "captured": (
                captured_piece.symbol() if captured_piece is not None else None
            ),
            "fen": self.board.fen(),
        }
        history = [
            *self.state.get("history", []),
            history_entry,
        ]
        self.state = {
            **self.state,
            "fen": self.board.fen(),
            "selected_square": None,
            "history": history,
        }

    def undo(self) -> None:
        """Handle undo

        Returns:
            update state to previous state of chess game
        """
        history = self.state.get("history", [])
        if history:
            history.pop()
            if self.computer_playing and self.board.turn != CONFIG.computer_color:
                # Edge case when player wins or draw; only undo twice if it is the players turn
                history.pop()
        board = chess.Board()
        for move in history:
            board.push_san(move["uci"])
        self.board = board
        self.state = {
            **self.state,
            "fen": self.board.fen(),
            "selected_square": None,
            "history": history,
        }

    def render(self, selected_square: Optional[int] = None) -> html.Div:
        """Render the chessboard from White's perspective"""
        legal_targets = set()
        if selected_square is not None:
            for legal_move in self.board.legal_moves:
                if legal_move.from_square == selected_square:
                    legal_targets.add(legal_move.to_square)

        squares = []
        for rank in range(7, -1, -1):
            for file in range(8):
                square = chess.square(file, rank)
                squares.append(
                    ChessGame._render_square(
                        board=self.board,
                        square=square,
                        selected_square=selected_square,
                        legal_targets=legal_targets,
                    )
                )

        return html.Div(squares, className="chess-squares")

    @staticmethod
    def _render_square(
        board: chess.Board,
        square: chess.Square,
        selected_square: Optional[int],
        legal_targets: set[int],
    ) -> html.Button:
        """Render one square of the board"""
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        is_dark = (rank + file) % 2 == 1
        background = CONFIG.dark_square if is_dark else CONFIG.light_square

        if square == selected_square:
            background = CONFIG.selected_square
        elif square in legal_targets:
            background = CONFIG.legal_move_square

        piece = board.piece_at(square)
        children = []
        if piece is not None:
            children.append(ChessGame._get_piece_icon(piece))
        return html.Button(
            children=children,
            id={"type": "chess-square", "square": square},
            n_clicks=0,
            style={"backgroundColor": background},
            className="chess-square",
        )

    @staticmethod
    def _get_piece_icon(
        piece: chess.Piece, use_html: bool = False
    ) -> Union[DashIconify, html.Img]:
        unicode, unicode_name = PIECE_UNICODE[(piece.color, piece.piece_type)]
        if use_html:
            openmoji_base_url = (
                "https://cdn.jsdelivr.net/gh/hfg-gmuend/openmoji/color/svg"
            )
            return html.Img(
                src=f"{openmoji_base_url}/{unicode}.svg",
                style={
                    "width": "78%",
                    "height": "78%",
                    "objectFit": "contain",
                    "pointerEvents": "none",
                },
            )
        return DashIconify(icon=f"openmoji:{unicode_name}", height=35)

    @staticmethod
    def history_to_components(history: list[dict]) -> html.Div | list[html.Div]:
        """Display the captured moves. Each history entry contains:
        {
            "move": "e4",
            "uci": "e2e4",
            "from": "e2",
            "to": "e4",
            "captured": None,
            "fen": "...",
        }
        """
        if not history:
            return html.Div(
                "No moves yet.",
                style={"opacity": 0.6},
                className="chess-cell",
            )

        rows = []

        for index in range(0, len(history), 2):
            white_move = history[index]["san"]
            black_move = history[index + 1]["san"] if index + 1 < len(history) else ""
            rows.append(
                html.Div(
                    [
                        html.Span(f"{index // 2 + 1}.", className="p-bold chess-cell"),
                        html.Span(white_move, className="chess-cell"),
                        html.Span(black_move, className="chess-cell"),
                    ],
                    className="chess-row",
                )
            )

        return rows

    def convert_to_save_format(self) -> str:
        return encode_dict(
            {
                "moves": ",".join(ChessGame._get_moves(self.state)),
                "computer": self.computer_playing,
            }
        )


def evaluate_board(board: chess.Board) -> int:
    """Evaluate board for a score based on checkmate, pieces remaining, and mobility. Positive score is good for
    White."""

    # Terminal positions
    if board.is_checkmate():
        # Side to move is checkmated
        return -1_000_000 if board.turn == chess.WHITE else 1_000_000

    if (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.is_fifty_moves()
    ):
        return 0

    # Repetition
    if board.is_repetition(2):
        return 0

    # Material
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    # Mobility (bonus)
    mobility = board.legal_moves.count()
    if board.turn == chess.WHITE:
        score += mobility * 2
    else:
        score -= mobility * 2

    # Check (bonus)
    if board.is_check():
        if board.turn == chess.WHITE:
            score -= 50
        else:
            score += 50
    return score


def minimax(
    board: chess.Board,
    depth: int,
    alpha: int | float,
    beta: int | float,
    maximizing_player: bool,
) -> int:
    """Standard minimax with alpha-beta pruning. The depth is measured in half-moves / plies. The first move is
    computed as computer move, the second step is human reply, and so on.
    """

    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        value = -float("inf")

        for move in board.legal_moves:
            board.push(move)
            value = max(
                value,
                minimax(board, depth - 1, alpha, beta, False),
            )
            board.pop()
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value

    value = float("inf")

    for move in board.legal_moves:
        board.push(move)
        value = min(
            value,
            minimax(board, depth - 1, alpha, beta, True),
        )
        board.pop()
        beta = min(beta, value)
        if beta <= alpha:
            break
    return value


def choose_move(
    board: chess.Board,
    player: chess.Color,
    depth: int,
) -> chess.Move:
    """
    Choose the best move
    """
    best_moves = []

    if player == chess.WHITE:
        best_score = -float("inf")
    else:
        best_score = float("inf")

    for move in board.legal_moves:
        board.push(move)

        score = minimax(
            board=board,
            depth=max(depth - 1, 0),
            alpha=-float("inf"),
            beta=float("inf"),
            maximizing_player=(player == chess.BLACK),
        )

        board.pop()

        if player == chess.WHITE:
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        else:
            if score < best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
    if not best_moves:
        raise ValueError("No best move found")
    return random.choice(best_moves)
