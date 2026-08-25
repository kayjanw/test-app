from enum import StrEnum, auto


class Action(StrEnum):
    FOLD = auto()
    CALL = auto()
    CHECK = auto()
    RAISE = auto()


class Profile:
    def __init__(
        self,
        opportunities_to_fold: int = 0,
        folds: int = 0,
        opportunities_to_call: int = 0,
        calls: int = 0,
        opportunities_to_check: int = 0,
        checks: int = 0,
        opportunities_to_raise: int = 0,
        raises: int = 0,
        showdown_history: list[tuple[int, str]] = None,
    ):
        self.opportunities_to_fold = opportunities_to_fold
        self.folds = folds
        self.opportunities_to_call = opportunities_to_call
        self.calls = calls
        self.opportunities_to_check = opportunities_to_check
        self.checks = checks
        self.opportunities_to_raise = opportunities_to_raise
        self.raises = raises

        # Showdown hand records to back-calculate range
        # Stores tuples of (hand_strength_at_showdown, action taken)
        self.showdown_history = showdown_history or []

    @property
    def total_moves(self) -> int:
        return self.folds + self.calls + self.checks + self.raises

    @property
    def fold_rate(self) -> float | None:
        if self.opportunities_to_fold:
            return self.folds / self.opportunities_to_fold

    @property
    def call_rate(self) -> float | None:
        if self.opportunities_to_call:
            return self.calls / self.opportunities_to_call

    @property
    def check_rate(self) -> float | None:
        if self.opportunities_to_check:
            return self.checks / self.opportunities_to_check

    @property
    def raise_rate(self) -> float | None:
        if self.opportunities_to_raise:
            return self.raises / self.opportunities_to_raise

    def record_action(self, action_type: Action, legal_actions: list[Action]):
        """Every round: record action"""
        if Action.FOLD in legal_actions:
            self.opportunities_to_fold += 1
        if Action.CALL in legal_actions:
            self.opportunities_to_call += 1
        if Action.CHECK in legal_actions:
            self.opportunities_to_check += 1
        if Action.RAISE in legal_actions:
            self.opportunities_to_raise += 1

        if action_type == Action.FOLD:
            self.folds += 1
        elif action_type == Action.CALL:
            self.calls += 1
        elif action_type == Action.CHECK:
            self.checks += 1
        elif action_type == Action.RAISE:
            self.raises += 1

    def record_showdown(self, strength: int, actions: list[Action]):
        """At showdown: back-calculate play style"""
        self.showdown_history.append((strength, "-".join(actions)))

    def get_showdown_average_strength(self) -> float:
        """Average hand strength at showdown"""
        if self.showdown_history:
            return sum(h[0] for h in self.showdown_history) / len(self.showdown_history)
