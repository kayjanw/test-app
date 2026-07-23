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
    def __init__(self, state: dict[str, Any] | None = None, computer: int = 0):
        if state:
            self.board = chess.Board(state["fen"])
            self.state = state
        else:
            self.board = chess.Board()
            self.state = ChessGame.get_initial_state(computer)
        self.computer_difficulty = computer

    @classmethod
    def from_state(cls, state: dict[str, Any] | None, computer: int):
        """Recreate chess game state from initial state, and implement moves

        Args:
            state: chess state, if applicable
            computer: whether computer is playing
        """
        if state:
            instance = cls.from_moves(
                state["original_fen"], cls._get_moves(state), computer
            )
            instance.state = state
            return instance
        return cls(state, computer)

    @classmethod
    def from_moves(cls, fen: str, moves: list[str], computer: int = 0):
        """Recreate chess game state from original fen, and implement moves

        Args:
            fen: original chess fen
            moves: list of moves in uci format
            computer: whether computer is playing

        Returns:
            reconstructed state of chess game
        """
        instance = cls(
            state={**ChessGame.get_initial_state(computer), "fen": fen},
            computer=computer,
        )
        for move_uci in moves:
            from_square = chess.parse_square(move_uci[:2])
            to_square = chess.parse_square(move_uci[2:4])
            instance._move(instance._get_move(from_square, to_square))
        return instance

    @property
    def fen(self) -> chess.Square | None:
        return self.state.get("fen")

    @fen.setter
    def fen(self, fen: str) -> None:
        self.state["fen"] = fen

    @property
    def selected_square(self) -> chess.Square | None:
        return self.state.get("selected_square")

    @selected_square.setter
    def selected_square(self, selected_square: chess.Square | None) -> None:
        self.state["selected_square"] = selected_square

    @property
    def history(self) -> list[dict[str, Any]]:
        return self.state.get("history")

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
            if self.computer_difficulty and self.board.turn == CONFIG.computer_color:
                status = "Computer is thinking..."
            else:
                status = f"{side} to move"
        return status

    @staticmethod
    def get_initial_state(computer: int) -> dict:
        """Get initial chess game

        Returns:
            initial state of chess game
        """
        return {
            "original_fen": chess.Board().fen(),
            "fen": chess.Board().fen(),
            "selected_square": None,
            "history": [],
            "computer": computer,
        }

    def move(
        self, selected_square: chess.Square | None, clicked_square: chess.Square
    ) -> None:
        """Handles selecting a piece, moving a selected piece, computer response (if applicable)

        Args:
            selected_square: from square, previously selected square
            clicked_square: to square, current clicked square

        Returns:
            update state to new state of chess game
        """
        if self.board.is_game_over():
            return

        # Nothing is selected yet - colour the square yellow
        if selected_square is None:
            piece = self.board.piece_at(clicked_square)
            if piece is None or piece.color != self.board.turn:
                return
            self.selected_square = clicked_square
            return

        # Something is selected
        move = self._get_move(selected_square, clicked_square)

        if move not in self.board.legal_moves:
            clicked_piece = self.board.piece_at(clicked_square)
            # Clicking another own piece selects that piece instead
            if clicked_piece is not None and clicked_piece.color == self.board.turn:
                self.selected_square = clicked_square
            else:
                self.selected_square = None
            return

        # Human move
        self._move(move)

        # Computer move
        if (
            self.computer_difficulty
            and not self.board.is_game_over()
            and self.board.turn == CONFIG.computer_color
        ):
            computer_move = choose_move(
                board=self.board,
                player=CONFIG.computer_color,
                depth=CONFIG.depth,
                difficulty=self.computer_difficulty,
            )
            self._move(computer_move)

    def _get_move(
        self, selected_square: chess.Square, clicked_square: chess.Square
    ) -> chess.Move:
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
        return move

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
            "captured": (captured_piece.color, captured_piece.piece_type)
            if captured_piece
            else None,
            "fen": self.board.fen(),
        }
        self.fen = self.board.fen()
        self.selected_square = None
        self.history.append(history_entry)

    def undo(self) -> None:
        """Handle undo

        Returns:
            update state to previous state of chess game
        """
        history = self.history
        if history:
            history.pop()
            if self.computer_difficulty and self.board.turn != CONFIG.computer_color:
                # Edge case when player wins or draw; only undo twice if it is the players turn
                history.pop()
        board = chess.Board()
        for move in history:
            board.push_san(move["uci"])
        self.board = board
        self.fen = self.board.fen()
        self.selected_square = None

    def render(self) -> html.Div:
        """Render the chessboard from White's perspective"""
        selected_square = self.selected_square
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
            children.append(ChessGame._get_piece_icon(piece.color, piece.piece_type))
        return html.Button(
            children=children,
            id={"type": "chess-square", "square": square},
            n_clicks=0,
            style={"backgroundColor": background},
            className="chess-square",
        )

    @staticmethod
    def _get_piece_icon(
        color: chess.Piece.color,
        piece_type: chess.Piece.piece_type,
        use_html: bool = False,
    ) -> Union[DashIconify, html.Img]:
        """Get piece icon to add to chess board"""
        unicode, unicode_name = PIECE_UNICODE[(color, piece_type)]
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

    def history_to_components(self) -> html.Div | list[html.Div]:
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
        history = self.history

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

    def render_captured_pieces(self) -> html.Div:
        """Render white captured pieces and black captured pieces"""
        captured_pieces = self._get_captured_pieces()
        captured_pieces_white = [
            self._get_piece_icon(color, piece_type)
            for color, piece_type in captured_pieces
            if color == chess.WHITE
        ]
        captured_pieces_black = [
            self._get_piece_icon(color, piece_type)
            for color, piece_type in captured_pieces
            if color == chess.BLACK
        ]
        if captured_pieces_white or captured_pieces_black:
            return html.Div(
                [
                    "Captured pieces:",
                    html.Div(captured_pieces_white),
                    html.Div(captured_pieces_black),
                ]
            )
        return html.Div()

    def _get_captured_pieces(
        self,
    ) -> list[tuple[chess.Piece.color, chess.Piece.piece_type]]:
        """Get tuple of white captured pieces and black captured pieces"""
        return [history["captured"] for history in self.history if history["captured"]]

    def convert_to_save_format(self) -> str:
        """Convert data to save format"""
        return encode_dict(
            {
                "fen": self.state["original_fen"],
                "moves": ",".join(ChessGame._get_moves(self.state)),
                "computer": self.computer_difficulty,
            }
        )

    @staticmethod
    def _get_moves(state: dict[str, Any]) -> list[str]:
        return [history["uci"] for history in state.get("history", [])]


DEVELOPMENT = 15
TOLERANCE = 5


def evaluate_board(board: chess.Board, difficulty: int) -> int:
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

    # Development (bonus - only for difficulty >= 2)
    if difficulty >= 2:
        if board.piece_at(chess.F3) == chess.Piece(chess.KNIGHT, chess.WHITE):
            score += DEVELOPMENT
        if board.piece_at(chess.C3) == chess.Piece(chess.KNIGHT, chess.WHITE):
            score += DEVELOPMENT
        if board.piece_at(chess.F6) == chess.Piece(chess.KNIGHT, chess.BLACK):
            score -= DEVELOPMENT
        if board.piece_at(chess.C6) == chess.Piece(chess.KNIGHT, chess.BLACK):
            score -= DEVELOPMENT

    # Check (bonus - only for difficulty >= 3)
    if difficulty >= 3:
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
    difficulty: int,
) -> int:
    """Standard minimax with alpha-beta pruning. The depth is measured in half-moves / plies. The first move is
    computed as computer move, the second step is human reply, and so on.
    """

    if depth == 0 or board.is_game_over():
        return evaluate_board(board, difficulty)

    if maximizing_player:
        value = -float("inf")

        for move in board.legal_moves:
            board.push(move)
            value = max(
                value,
                minimax(board, depth - 1, alpha, beta, False, difficulty),
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
            minimax(board, depth - 1, alpha, beta, True, difficulty),
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
    difficulty: int,
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
            difficulty=difficulty,
        )

        board.pop()

        if player == chess.WHITE:
            if score > best_score + TOLERANCE:
                best_score = score
                best_moves = [move]
            elif score >= best_score - TOLERANCE:
                best_moves.append(move)
        else:
            if score < best_score - TOLERANCE:
                best_score = score
                best_moves = [move]
            elif score <= best_score + TOLERANCE:
                best_moves.append(move)
    if not best_moves:
        raise ValueError("No best move found")
    return random.choice(best_moves)
