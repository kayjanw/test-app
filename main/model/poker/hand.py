from main.model.poker.action import Action
from main.model.poker.stage import Stage


class Hand:
    def __init__(
        self,
        chips_start: int,
        chips_end: int = 0,
        actions: dict[Stage, list[Action]] = None,
        showdown_strength: int = -1,
    ):
        self.chips_start = chips_start
        self.chips_end = chips_end
        self.actions = actions or {}
        self.showdown_strength = showdown_strength

    def record_action(self, stage: Stage, action: Action) -> None:
        if stage not in self.actions:
            self.actions[stage] = [action]
        else:
            self.actions[stage].append(action)
