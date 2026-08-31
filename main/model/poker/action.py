from enum import StrEnum, auto


class Action(StrEnum):
    FOLD = auto()
    CALL = auto()
    CHECK = auto()
    RAISE = auto()
