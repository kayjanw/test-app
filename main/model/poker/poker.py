from dataclasses import dataclass

from main.model.poker.card import Card
from main.model.poker.stage import Stage


@dataclass
class ButtonColour:
    NEW_HAND = "#2ecc71"
    FOLD = "#e74c3c"


BLIND = 10
SUITS = ["s", "h", "d", "c"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
DECK = [Card(suit, rank) for rank in RANKS for suit in SUITS]
HAND_STRENGTH = {
    "HIGHCARD": 15,
    "ONEPAIR": 35,
    "TWOPAIR": 55,
    "THREEOFAKIND": 70,
    "STRAIGHT": 80,
    "FLUSH": 85,
    "FULLHOUSE": 93,
    "FOUROFAKIND": 98,
    "STRAIGHTFLUSH": 100,
}
STAGES = [
    Stage.NEWGAME,
    Stage.PREFLOP,
    Stage.FLOP,
    Stage.TURN,
    Stage.RIVER,
    Stage.SHOWDOWN,
]
