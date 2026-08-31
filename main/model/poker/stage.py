from dataclasses import dataclass


@dataclass
class Stage:
    NEWGAME = ""
    PREFLOP = "Pre-flop"
    FLOP = "Flop"
    TURN = "Turn"
    RIVER = "River"
    SHOWDOWN = "Showdown"
