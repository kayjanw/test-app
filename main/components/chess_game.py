from __future__ import annotations

from typing import Any, Optional, Union

import chess
import chess.polyglot
from dash import html
from dash_iconify import DashIconify

from common.components.helper import encode_dict
from main.model.chess_game import PIECE_UNICODE, PIECE_VALUES, ChessConfig

CONFIG = ChessConfig(depth=2)


class ChessGame:
    def __init__(self, state: dict[str, Any] | None = None):
        self.board = chess.Board(state["fen"]) if state else chess.Board()
        self.state = state or self.get_initial_state()

    @classmethod
    def from_moves(cls, moves: list[str]):
        """Recreate chess game state from list of moves

        Args:
            moves: list of moves in uci format

        Returns:
            reconstructed state of chess game
        """
        instance = ChessGame()
        for move_uci in moves:
            move = chess.Move.from_uci(move_uci)
            instance._move(move)
        return instance

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

    def move(self, clicked_square: chess.Square) -> None:
        """Handles selecting a piece, moving a selected piece, PC response

        Args:
            clicked_square: current clicked square

        Returns:
            update state to new state of chess game
        """
        if self.board.is_game_over():
            return

        # If the computer controls the current side, human should not be able to move
        if (
            CONFIG.computer_color is not None
            and self.board.turn == CONFIG.computer_color
        ):
            # TODO: Compute next step for computer
            return

        # Nothing is selected yet - colour the square yellow
        selected_square = self.state.get("selected_square")
        if selected_square is None:
            piece = self.board.piece_at(clicked_square)
            if piece is None:
                return
            if CONFIG.computer_color is not None:
                if piece.color == CONFIG.computer_color:
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
        else:
            self._move(move)

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

        # # Computer move
        # if (
        #         CONFIG.computer_color is not None
        #         and not board.is_game_over()
        #         and board.turn == CONFIG.computer_color
        # ):
        #     print("computer move!")
        #
        #     computer_move = choose_computer_move(
        #         board=board,
        #         computer_color=CONFIG.computer_color,
        #         depth=CONFIG.computer_depth,
        #     )
        #
        #     if computer_move is not None:
        #         computer_san = board.san(computer_move)
        #
        #         captured_piece = board.piece_at(
        #             computer_move.to_square
        #         )
        #
        #         board.push(computer_move)
        #
        #         computer_history_entry = {
        #             "san": computer_san,
        #             "uci": computer_move.uci(),
        #             "from": chess.square_name(
        #                 computer_move.from_square
        #             ),
        #             "to": chess.square_name(
        #                 computer_move.to_square
        #             ),
        #             "captured": (
        #                 captured_piece.symbol()
        #                 if captured_piece is not None
        #                 else None
        #             ),
        #             "fen": board.fen(),
        #         }
        #
        #         new_state = {
        #             **new_state,
        #             "fen": board.fen(),
        #             "history": [
        #                 *history,
        #                 computer_history_entry,
        #             ],
        #         }

    def undo(self) -> None:
        """Handle undo

        Returns:
            update state to previous state of chess game
        """
        history = self.state.get("history", [])
        if history:
            history.pop()
        board = chess.Board()
        for move in history:
            board.push_san(move["uci"])
        self.board = board
        self.state = {
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
    def history_to_components(history: list[dict]) -> list:
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
            return [
                html.Div(
                    "No moves yet.",
                    style={"opacity": 0.6},
                )
            ]

        rows = []

        for index in range(0, len(history), 2):
            white_move = history[index]
            black_move = history[index + 1] if index + 1 < len(history) else None
            rows.append(
                html.Div(
                    [
                        html.Span(
                            f"{index // 2 + 1}.",
                            style={"width": "32px"},
                            className="p-bold",
                        ),
                        html.Span(
                            white_move["san"],
                            style={"width": "80px"},
                        ),
                        html.Span(
                            black_move["san"] if black_move else "",
                            style={"width": "80px"},
                        ),
                    ],
                    className="chess-history",
                )
            )

        return rows

    def convert_to_save_format(self) -> dict:
        return encode_dict(
            {
                "moves": ",".join(
                    history["uci"] for history in self.state.get("history", [])
                )
            }
        )


def evaluate_board(board: chess.Board) -> int:
    """Evaluate board for a score based on checkmate, pieces remaining, and mobility. Positive score is good for White."""

    if board.is_checkmate():
        # Side to move is checkmated.
        # If White is to move and checkmated: Black wins.
        return -1_000_000 if board.turn == chess.WHITE else 1_000_000

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0

    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    # Small bonus for mobility.
    # This is optional but makes the engine slightly less material-only.
    mobility = board.legal_moves.count()

    board.push(chess.Move.null())
    opponent_mobility = board.legal_moves.count()
    board.pop()

    score += (mobility - opponent_mobility) * 2

    return score


def minimax(
    board: chess.Board,
    depth: int,
    alpha: int,
    beta: int,
    maximizing_player: bool,
) -> int:
    """Standard minimax with alpha-beta pruning. The depth is measured in half-moves / plies. The first move is computed
    as computer move, second step is human reply, and so on.
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


def choose_computer_move(
    board: chess.Board,
    computer_color: chess.Color,
    depth: int,
) -> Optional[chess.Move]:
    """
    Choose the best move for the configured computer side.
    """
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return None

    best_move = None

    if computer_color == chess.WHITE:
        best_score = -float("inf")
    else:
        best_score = float("inf")

    for move in legal_moves:
        board.push(move)

        score = minimax(
            board=board,
            depth=max(depth - 1, 0),
            alpha=-float("inf"),
            beta=float("inf"),
            maximizing_player=(computer_color == chess.BLACK),
        )

        board.pop()

        if computer_color == chess.WHITE:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    return best_move
