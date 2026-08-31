from main.model.poker.action import Action
from main.model.poker.hand import Hand
from main.model.poker.stage import Stage


def to_dict(obj):
    """Recursively converts objects to dictionaries."""
    if hasattr(obj, "__dict__"):
        return {key: to_dict(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [to_dict(item) for item in obj]
    return obj


class Profile:
    def __init__(
        self,
        # Complicated profile
        current_hand: dict = None,
        hand_history: list[dict] = None,
        # Simple profile
        opportunities_to_fold: int = 0,
        folds: int = 0,
        opportunities_to_call: int = 0,
        calls: int = 0,
        opportunities_to_check: int = 0,
        checks: int = 0,
        opportunities_to_raise: int = 0,
        raises: int = 0,
    ):
        self.current_hand = to_dict(current_hand)
        self.hand_history = to_dict(hand_history or [])

        self.opportunities_to_fold = opportunities_to_fold
        self.folds = folds
        self.opportunities_to_call = opportunities_to_call
        self.calls = calls
        self.opportunities_to_check = opportunities_to_check
        self.checks = checks
        self.opportunities_to_raise = opportunities_to_raise
        self.raises = raises

    @property
    def vpip(self) -> float | None:
        """Voluntarily put in pot: percentage of hands where user called or made a raise preflop.
        This statistic determines whether the user is a loose or tight player.

        Good players have a wide range of VPIP figures - within the range of 15-27% in a 9 player game.
        """
        vpip_hands = len(
            [
                hand
                for hand in self.hand_history
                if Action.CALL in hand["actions"][Stage.PREFLOP]
                or Action.RAISE in hand["actions"][Stage.PREFLOP]
            ]
        )
        total_hands = len(self.hand_history)
        if total_hands:
            return round(vpip_hands / total_hands, 2)

    @property
    def pfr(self) -> float | None:
        """Pre-Flop Raise: The percent of hands user raised preflop (to call another player's raise does not count).
        This statistic determines whether the user is a passive or aggressive player.

        A good rule of thumb is that this value should be 1/2 of VPIP figure or more.
        """
        pfr_hands = len(
            [
                hand
                for hand in self.hand_history
                if Action.RAISE in hand["actions"][Stage.PREFLOP]
            ]
        )
        total_hands = len(self.hand_history)
        if total_hands:
            return round(pfr_hands / total_hands, 2)

    @property
    def wts(self) -> float | None:
        """Went to showdown: The percent of times user went to the showdown after seeing the flop.

        Average figure is 20%, with a range of 17-25%. This statistic helps define tight/loose play after the flop.
        It is good for determining the effectiveness of a bluff against a player.
        """
        hands_seen_flop = len(
            [hand for hand in self.hand_history if Stage.FLOP in hand["actions"]]
        )
        hands_went_showdown = len(
            [hand for hand in self.hand_history if hand["showdown_strength"] > 0]
        )
        if hands_seen_flop:
            return round(hands_went_showdown / hands_seen_flop, 2)

    @property
    def wsd(self) -> float | None:
        """Won showdown: The percent of times user won money at the showdown, out of those times user went to the showdown.

        This number shows how often the user is showing down the best hand. Winning is defined as ending the hand with
        more chips than the user started with.
        """
        showdowns_won = len(
            [
                hand
                for hand in self.hand_history
                if hand["showdown_strength"] and hand["chips_start"] < hand["chips_end"]
            ]
        )
        hands_went_showdown = len(
            [hand for hand in self.hand_history if hand["showdown_strength"]]
        )
        if hands_went_showdown:
            return round(showdowns_won / hands_went_showdown, 2)

    @property
    def af(self) -> float | None:
        """Aggression factor: The percentage of total bets and raises after flop, divided by the number of calls.

        The average factor of aggression for winning players in a 9-player game is 2.5 (range 1.7-3.5)"""
        actions_after_flop = [
            action
            for hand in self.hand_history
            for stage, actions in hand["actions"].items()
            if stage in [Stage.FLOP, Stage.TURN, Stage.RIVER]
            for action in actions
        ]
        total_raise = actions_after_flop.count(Action.RAISE)
        total_call = actions_after_flop.count(Action.CALL)
        if total_call:
            return total_raise / total_call

    @property
    def showdown_average_strength(self) -> float:
        """Average hand strength at showdown"""
        showdown_hands = [
            hand["showdown_strength"]
            for hand in self.hand_history
            if hand["showdown_strength"]
        ]
        if len(showdown_hands):
            return round(sum(showdown_hands) / len(showdown_hands), 2)

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

    def start_hand(self, chips_user: int):
        self.current_hand = to_dict(Hand(chips_user))

    def record_action(self, stage: Stage, action: Action, to_call: int):
        """Every round: record action"""
        hand = Hand(**self.current_hand)
        hand.record_action(stage, action)
        self.current_hand = to_dict(hand)

        if action == Action.FOLD:
            self.folds += 1
            self.opportunities_to_fold += 1
            self.opportunities_to_raise += 1
            if to_call:
                self.opportunities_to_call += 1
            else:
                self.opportunities_to_check += 1

        elif action == Action.CALL:
            self.calls += 1
            self.opportunities_to_fold += 1
            self.opportunities_to_raise += 1
            self.opportunities_to_call += 1

        elif action == Action.CHECK:
            self.checks += 1
            self.opportunities_to_fold += 1
            self.opportunities_to_raise += 1
            self.opportunities_to_check += 1

        elif action == Action.RAISE:
            self.raises += 1
            self.opportunities_to_fold += 1
            self.opportunities_to_raise += 1
            if to_call:
                self.opportunities_to_call += 1
            else:
                self.opportunities_to_check += 1

    def end_hand(self, chips_user: int, showdown_strength: int = -1):
        hand = Hand(**self.current_hand)
        hand.chips_end = chips_user
        hand.showdown_strength = showdown_strength
        self.hand_history.append(to_dict(hand))
        self.current_hand = to_dict(None)

    @property
    def profile_type(self):
        vpip = self.vpip  # measure loose/tight
        pfr = self.pfr  # measure passive/aggressive
        profile = ""
        if vpip is None or pfr is None:
            return ""

        if 0.22 <= vpip <= 0.27 and 0.18 <= pfr <= 0.23:
            profile = "Solid regular"
        elif 0.28 <= vpip <= 0.38 and 0.22 <= pfr <= 0.3:
            # Tight and aggressive
            # Strategy: Respect their preflop raises
            profile = "Aggressive"
        elif 0.35 <= vpip <= 0.6 and pfr <= 0.12:
            # Loose and passive; the calling station
            # Strategy: never bluff them, value bet strong hands and size your bets larger
            profile = "Loose-passive caller"
        elif vpip <= 0.18 and pfr <= 0.14:
            # Tight and passive, they fold too much
            # Strategy: steal their blind, fold when they are aggressive
            profile = "Rock"
        elif vpip >= 0.45 and pfr >= 0.35:
            # Loose and aggressive, frequent bets, raises, and bluffs
            # Strategy: Let their aggression work against them by trapping with strong hands, avoid bluffing
            profile = "Maniac"

        res = f"Profile: {profile}\n" if profile else "Profile: "
        res += (
            f"VPIP: {vpip}, PFR: {pfr}, AF: {self.af}, WTS: {self.wts}, WSD: {self.wsd}"
        )
        return res
