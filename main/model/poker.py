from dataclasses import dataclass

from pokerlib.enums import Rank, Suit


@dataclass
class ButtonColour:
    NEW_HAND = "#2ecc71"
    FOLD = "#e74c3c"


@dataclass
class CardSuit:
    s = "♠"
    h = "♥"
    d = "♦"
    c = "♣"

    @classmethod
    def __getitem__(cls, key: str) -> str:
        return getattr(cls, key)

    @classmethod
    def get(cls, key: str) -> str:
        return getattr(cls, key)


@dataclass
class Card:
    suit: str
    rank: str

    @property
    def pokerlib(self) -> tuple[Rank, Suit]:
        return RANK_MAP[self.rank], SUIT_MAP[self.suit]

    @property
    def colour(self) -> str:
        return "red" if self.suit in {"h", "d"} else "black"

    def to_str(self):
        return f"{self.suit}-{self.rank}"

    @classmethod
    def from_str(cls, card: str):
        return cls(*card.split("-"))

    def __repr__(self):
        return f"{self.rank}{CardSuit.get(self.suit)}"


BLIND = 10
SUITS = ["s", "h", "d", "c"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
STAGES = ["", "Pre-flop", "Flop", "Turn", "River", "Showdown"]
DECK = [Card(suit, rank) for rank in RANKS for suit in SUITS]

RANK_MAP = {
    "2": Rank.TWO,
    "3": Rank.THREE,
    "4": Rank.FOUR,
    "5": Rank.FIVE,
    "6": Rank.SIX,
    "7": Rank.SEVEN,
    "8": Rank.EIGHT,
    "9": Rank.NINE,
    "10": Rank.TEN,
    "J": Rank.JACK,
    "Q": Rank.QUEEN,
    "K": Rank.KING,
    "A": Rank.ACE,
}
SUIT_MAP = {
    "s": Suit.SPADE,
    "h": Suit.HEART,
    "d": Suit.DIAMOND,
    "c": Suit.CLUB,
}
STRONG_HANDS = {
    "TWO_PAIR",
    "THREE_OF_A_KIND",
    "STRAIGHT",
    "FLUSH",
    "FULL_HOUSE",
    "FOUR_OF_A_KIND",
    "STRAIGHT_FLUSH",
}
