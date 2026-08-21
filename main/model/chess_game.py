from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import chess


@dataclass
class ChessConfig:
    computer_color: Optional[chess.Color] = None
    # How many half-moves the white piece looks ahead, if PC is playing
    depth: int = 2

    light_square: str = "#F0E3DF"  # "#f0d9b5"
    dark_square: str = "#BE9B89"  # "#b58863"
    selected_square: str = "#f6f669"
    legal_move_square: str = "#a9d18e"


PIECE_UNICODE = {
    (chess.WHITE, chess.KING): ("2654", "white-chess-king", "king", "king"),
    (chess.WHITE, chess.QUEEN): ("2655", "white-chess-queen", "queen", "queen"),
    (chess.WHITE, chess.ROOK): ("2656", "white-chess-rook", "rook", "rook"),
    (chess.WHITE, chess.BISHOP): ("2657", "white-chess-bishop", "bishop", "bishop"),
    (chess.WHITE, chess.KNIGHT): ("2658", "white-chess-knight", "knight", "horse"),
    (chess.WHITE, chess.PAWN): ("2659", "white-chess-pawn", "pawn", "pawn"),
    (chess.BLACK, chess.KING): ("265A", "black-chess-king", "black-king", "black-king"),
    (chess.BLACK, chess.QUEEN): (
        "265B",
        "black-chess-queen",
        "black-queen",
        "black-queen",
    ),
    (chess.BLACK, chess.ROOK): ("265C", "black-chess-rook", "black-rook", "black-rook"),
    (chess.BLACK, chess.BISHOP): (
        "265D",
        "black-chess-bishop",
        "black-bishop",
        "black-bishop",
    ),
    (chess.BLACK, chess.KNIGHT): (
        "265E",
        "black-chess-knight",
        "black-knight",
        "black-horse",
    ),
    (chess.BLACK, chess.PAWN): ("265F", "chess-pawn", "black-pawn", "black-pawn"),
}

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20_000,
}
