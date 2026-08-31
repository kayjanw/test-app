import random

import dash_mantine_components as dmc
from pokerlib import HandParser

from common.components.helper import return_message
from main.model.poker import Action, Card, Profile, Stage
from main.model.poker.poker import BLIND, DECK, HAND_STRENGTH, STAGES


class Poker:
    def __init__(
        self,
        stage: Stage = STAGES[0],
        pot: int = 0,
        to_call: int = 0,
        card_user: list[Card] = None,
        card_cpu: list[Card] = None,
        card_board: list[Card] = None,
        chips_user: int = 1000,
        chips_cpu: int = 1000,
        result: str = "",
        player_moved: bool = False,
        game_over: bool = False,
        aggression: float = None,
        deception: float = None,
        profile_user: Profile = None,
    ):
        self.stage = stage
        self.pot = pot
        self.to_call = to_call
        self.card_user = card_user or []
        self.card_cpu = card_cpu or []
        self.card_board = card_board or []
        self.chips_user = chips_user
        self.chips_cpu = chips_cpu
        self.result = result
        self.player_moved = player_moved
        self.game_over = game_over

        # for CPU optimization
        self.aggression = aggression
        self.deception = deception
        if not aggression:
            self.set_seed()

        # For user profile
        self.profile_user = profile_user or Profile()

    def set_seed(self) -> tuple[float, float]:
        self.aggression = random.uniform(0.85, 1.15)
        self.deception = random.random()

    @property
    def state(self):
        return dict(
            stage=self.stage,
            pot=self.pot,
            to_call=self.to_call,
            card_user=",".join([card.to_str() for card in self.card_user]),
            card_cpu=",".join([card.to_str() for card in self.card_cpu]),
            card_board=",".join([card.to_str() for card in self.card_board]),
            chips_user=self.chips_user,
            chips_cpu=self.chips_cpu,
            result=self.result,
            player_moved=self.player_moved,
            game_over=self.game_over,
            aggression=self.aggression,
            deception=self.deception,
            profile_user=self.profile_user.__dict__,
        )

    @property
    def hand_user(self):
        visible_cards = self.get_visible_card_board()
        parser = self.get_parser(self.card_user + visible_cards)
        return parser.handenum.name

    @property
    def hand_cpu(self):
        visible_cards = self.get_visible_card_board()
        parser = self.get_parser(self.card_cpu + visible_cards)
        return parser.handenum.name

    @property
    def total_hands(self):
        return len(self.profile_user.hand_history)

    @property
    def is_user_bet(self) -> bool:
        if self.profile_user.current_hand and not len(
            self.profile_user.current_hand["actions"].get(self.stage, [])
        ):
            return True
        return False

    @property
    def is_cpu_bet(self) -> bool:
        if Action.RAISE not in self.profile_user.current_hand["actions"].get(
            self.stage, []
        ):
            return True
        return False

    @classmethod
    def from_state(cls, state):
        state = state.copy()
        for k in ["card_user", "card_cpu", "card_board"]:
            state[k] = [Card.from_str(card) for card in state[k].split(",") if card]
        for k in ["profile_user"]:
            state[k] = Profile(**state[k])
        return cls(**state)

    def get_visible_card_board(self) -> list[Card]:
        """Get visible card on board based on stage"""
        if self.stage in STAGES[:2]:
            visible_cards = []
        elif self.stage in STAGES[:3]:
            visible_cards = self.card_board[:3]
        elif self.stage in STAGES[:4]:
            visible_cards = self.card_board[:4]
        else:
            visible_cards = self.card_board
        return visible_cards

    def render_cards(self) -> tuple[list[dmc.Paper], list[dmc.Paper], list[dmc.Paper]]:
        """Render cards on board, returns card elements"""
        visible_cards = self.get_visible_card_board()
        return (
            render_card(self.card_user),
            render_card(
                self.card_cpu, hidden=True if self.stage in STAGES[:-1] else False
            ),
            render_card(visible_cards),
        )

    def advance_stage(self, announce: bool = False):
        """Advance to next stage"""
        self.stage = STAGES[STAGES.index(self.stage) + 1]
        if announce:
            self.result += f"\nMoving to {self.stage}."

    def new_game(self) -> str:
        """Create new game"""
        if not self.chips_user:
            self.result = "You do not have any chips left to play."
            self.game_over = True
            return
        if not self.chips_cpu:
            self.result = "CPU does not have any chips left to play."
            self.game_over = True
            return
        deck = DECK.copy()
        random.shuffle(deck)

        # Update card
        self.card_user = [deck.pop(), deck.pop()]
        self.card_cpu = [deck.pop(), deck.pop()]
        self.card_board = [deck.pop() for _ in range(5)]

        # Update pot
        user_blind = min(self.chips_user, BLIND)
        cpu_blind = min(self.chips_cpu, BLIND)
        self.pot = user_blind + cpu_blind
        self.chips_user -= user_blind
        self.chips_cpu -= cpu_blind

        # Update interface
        self.stage = STAGES[1]
        self.to_call = 0
        self.result = return_message["poker_new_game"].format(blind=BLIND)
        self.player_moved = False
        self.game_over = False

        # Reset seed values each game
        self.set_seed()

        # Update user profile
        self.profile_user.start_hand(self.chips_user)

    def fold(self):
        """Implement player fold move, update user profile"""
        # Record user actions
        self.profile_user.record_action(self.stage, Action.FOLD, self.to_call)

        self.chips_cpu += self.pot
        self.pot = 0
        self.to_call = 0
        self.result = return_message["poker_fold"].format(p1="You", p2="CPU")
        self.player_moved = True
        self.game_over = True

        # Record user actions
        self.profile_user.end_hand(self.chips_user)

    def check_or_call(self):
        """Implement player check or call move, update user profile"""
        # Record user actions
        if self.to_call:
            self.profile_user.record_action(self.stage, Action.CALL, self.to_call)
            self.to_call = min(self.to_call, self.chips_user)
            self.chips_user -= self.to_call
            self.pot += self.to_call
            self.result = return_message["poker_call"].format(
                p1="You", amount=self.to_call
            )
            self.to_call = 0
            self.advance_stage(announce=True)
        else:
            self.profile_user.record_action(self.stage, Action.CHECK, self.to_call)
            self.result = return_message["poker_check"].format(p1="You")
            self.player_moved = True

    def bet_or_raise(self, raise_by: int):
        """Implement player raise move, update user profile"""
        if raise_by <= 0:
            self.result = return_message["poker_zero_raise"]
            return
        total_amount = self.to_call + raise_by
        if total_amount > self.chips_user:
            self.result = return_message["poker_insufficient_raise"]
            return

        self.chips_user -= total_amount
        self.pot += total_amount
        self.to_call = raise_by
        if self.is_user_bet:
            self.result = return_message["poker_bet"].format(p1="You", amount=raise_by)
        else:
            self.result = return_message["poker_raise"].format(
                p1="You", amount=raise_by
            )
        self.player_moved = True

        # Record user actions
        self.profile_user.record_action(self.stage, Action.RAISE, self.to_call)

    @staticmethod
    def get_parser(cards: list[Card]) -> HandParser:
        """Create and parse a pokerlib HandParser."""
        parser = HandParser([card.pokerlib for card in cards])
        parser.parse()
        return parser

    @staticmethod
    def hand_name(parser) -> str:
        return parser.handenum.name.replace("_", " ").title()

    def choose_move(self) -> tuple[str, int]:
        """Rule-based CPU.

        Returns:
            ("fold" | "check" | "call" | "raise", raise_by)
        """
        visible_cards = self.get_visible_card_board()

        # Pre-flop
        if not visible_cards:
            r1, r2 = (card.rank_strength for card in self.card_cpu)
            strength = evaluate_strength_preflop(r1, r2)
            # print("preflop", self.card_cpu, visible_cards, strength, self.deception)
            return choose_move_preflop(
                strength,
                self.to_call,
                self.aggression,
                self.deception,
            )
        # Post-flop
        strength = evaluate_strength_postflop(visible_cards, self.hand_cpu)
        # print("postflop", self.card_cpu, visible_cards, hand_type, strength, self.deception)
        return choose_move_postflop(
            strength,
            self.to_call,
            self.aggression,
            self.deception,
        )

    def cpu_fold(self):
        """Implement CPU fold action"""
        self.chips_user += self.pot
        self.pot = 0
        self.to_call = 0
        self.result += return_message["poker_fold"].format(p1="CPU", p2="You")
        self.game_over = True

        # Record user actions
        self.profile_user.end_hand(self.chips_user)

    def cpu_check(self):
        """Implement CPU check action"""
        self.result += return_message["poker_check"].format(p1="CPU")
        self.advance_stage()

    def cpu_call(self):
        """Implement CPU call action"""
        self.to_call = min(self.to_call, self.chips_cpu)
        self.chips_cpu -= self.to_call
        self.pot += self.to_call
        self.result += return_message["poker_call"].format(
            p1="CPU", amount=self.to_call
        )
        self.to_call = 0
        self.advance_stage()

    def cpu_raise(self, raise_by):
        """Implement CPU raise action"""
        if not self.chips_cpu:
            self.cpu_check()
            return
        if self.to_call >= self.chips_cpu:
            self.cpu_call()
            return
        total_amount = min(self.to_call + raise_by, self.chips_cpu)
        raise_by = total_amount - self.to_call
        self.chips_cpu -= total_amount
        self.pot += total_amount
        self.to_call = raise_by
        if self.is_cpu_bet:
            self.result += return_message["poker_bet"].format(p1="CPU", amount=raise_by)
        else:
            self.result += return_message["poker_raise"].format(
                p1="CPU", amount=raise_by
            )

    def cpu_move(self):
        """Plan and implement CPU move"""
        self.player_moved = False
        cpu_action, cpu_amount = self.choose_move()
        if cpu_action == "fold":
            self.cpu_fold()
        elif cpu_action == "check":
            self.cpu_check()
        elif cpu_action == "call":
            self.cpu_call()
        elif cpu_action == "raise":
            self.cpu_raise(cpu_amount)
        else:
            raise ValueError(f"Invalid CPU move {cpu_action=}")

    def evaluate_winner(self):
        """Return (winner, message) at showdown"""
        player_parser = self.get_parser(self.card_user + self.card_board)
        cpu_parser = self.get_parser(self.card_cpu + self.card_board)
        player_hand = self.hand_name(player_parser)
        cpu_hand = self.hand_name(cpu_parser)

        if player_parser > cpu_parser:
            return "player", f"You win with a {player_hand}! CPU had a {cpu_hand}."
        if cpu_parser > player_parser:
            return "cpu", f"CPU wins with a {cpu_hand}. You had a {player_hand}."
        return "split", f"Split pot! Both players have a {player_hand}."

    def showdown(self):
        """Evaluate winner and implement move, update user profile"""
        strength = evaluate_strength_postflop(self.card_board, self.hand_cpu)

        winner, result = self.evaluate_winner()
        self.result += f"\n{result}"
        if winner == "player":
            self.chips_user += self.pot
        elif winner == "cpu":
            self.chips_cpu += self.pot
        else:
            half_pot = self.pot // 2
            self.chips_user += half_pot
            self.chips_cpu += self.pot - half_pot
        self.pot = 0
        self.game_over = True

        # Record user actions
        self.profile_user.end_hand(self.chips_user, strength)


def render_card(cards: list[Card], hidden: bool = False) -> list[dmc.Paper]:
    if hidden:
        return [dmc.Paper("🂠", className="poker-card poker-card-hidden") for _ in cards]
    return [
        dmc.Paper(str(card), style={"color": card.colour}, className="poker-card")
        for card in cards
    ]


def render_amount(amount: int) -> str:
    return "${:,}".format(amount)


check_return = "check", 0
call_return = "call", 0
fold_return = "fold", 0


def round_up(value: int):
    if value % 10:
        return (int(value // 10) + 1) * 10
    return value


def evaluate_strength_preflop(r1: int, r2: int) -> int:
    """Used during preflop, evaluate strength from 0-100"""
    pair = r1 == r2
    high_card = max(r1, r2) >= 9
    ace = 12 in (r1, r2)
    connected = abs(r1 - r2) <= 2

    if pair:
        strength = 55 + r1 * 3
        if r1 >= 9:
            strength += 15
    else:
        strength = max(r1, r2) * 2
        if high_card:
            strength += 10
        if ace:
            strength += 10
        if connected:
            strength += 8
    return min(strength, 100)


def choose_move_preflop(
    strength: int, to_call: int, aggression: float, deception: float
) -> tuple[str, int]:
    """Choose move for preflop"""

    def raise_return(
        multiplier: int, max_raise: int = float("-inf")
    ) -> tuple[str, int]:
        return "raise", round_up(max(max_raise, int(multiplier * aggression)))

    if not to_call:
        # Strong hands: raise, occasionally check (slow play)
        if strength >= 50:
            if deception < 0.4:
                return check_return
            return raise_return(20)

        # Medium hands: check, occasionally raise (steal the pot)
        if strength >= 20:
            if deception < 0.4:
                return raise_return(15)
            return check_return

        # Weak hands: check, occasionally raise (bluff)
        if deception < 0.2:
            return raise_return(15)
        return check_return

    # Facing a bet; expensive calls should require stronger hands
    # Very strong hands: raise, occasionally call (trap)
    if strength >= 50:
        if deception < 0.25:
            return call_return
        return raise_return(to_call, 20)

    # Medium strong hands: call, occasionally raise (semi-bluff/value bet)
    if strength >= 30:
        if deception < 0.15:
            return raise_return(to_call, 15)
        return call_return

    # Medium hands: call or fold, occasionally raise (semi-bluff/value bet)
    if strength >= 20:
        if deception < 0.1:
            return raise_return(to_call, 20)
        if deception < 0.5:
            return call_return
        return fold_return

    # Weak hands: fold, sometimes call/raise
    if deception < 0.1:
        return raise_return(to_call, 15)
    if deception < 0.3:
        return call_return
    return fold_return


def evaluate_strength_postflop(visible_cards: list[Card], hand_type: str) -> int:
    """Used during postflop, evaluate strength from 0-100"""
    strength = HAND_STRENGTH.get(hand_type, 20)

    # Board texture: A wet board means there are more possible draws / strong hands
    suits = [card.suit for card in visible_cards]
    flush_possible = max((suits.count(suit) for suit in set(suits)), default=0) >= 3
    board_is_wet = flush_possible
    if board_is_wet:
        strength -= 5
    return strength


def choose_move_postflop(
    strength: int,
    to_call: int,
    aggression: float,
    deception: float,
) -> tuple[str, int]:
    def raise_random_return(min_raise: int, max_raise: int) -> tuple[str, int]:
        return "raise", round_up(random.randint(min_raise, max_raise))

    def raise_return(
        multiplier: float, max_raise: int = float("-inf")
    ) -> tuple[str, int]:
        return "raise", round_up(max(max_raise, int(multiplier * to_call)))

    # Bluff deception probability
    slow_play = random.random() < 0.5  # for strong hands
    semi_bluff = random.random() < 0.20  # for medium hands

    if not to_call:
        # Strong hands: raise, occasionally check (slow play)
        if strength >= 60:
            if slow_play:
                return check_return
            if random.random() < 0.70 * aggression:
                return raise_random_return(20, 40)
            return check_return

        # Medium hands: check, occasionally raise (steal the pot)
        if strength >= 30:
            if semi_bluff:
                return raise_random_return(15, 30)
            if deception < 0.25:
                return raise_random_return(15, 25)
            return check_return

        # Weak hands: check, occasionally raise (bluff)
        if deception < 0.12:
            return raise_random_return(15, 30)
        return check_return

    # Facing a bet; expensive calls should require stronger hands
    # Monster: raise, occasionally call (trap)
    if strength >= 90:
        if slow_play or deception < 0.30:
            return call_return
        return raise_return(random.uniform(1.0, 1.8), 20)

    # Medium strong hands: raise, occasionally call (semi-bluff/value bet)
    if strength >= 50:
        # Sometimes call to disguise strength.
        if deception < 0.40:
            return call_return
        return raise_return(random.uniform(0.8, 1.5), 20)

    # Medium hands: call or fold, occasionally raise (semi-bluff/value bet)
    if strength >= 30:
        if semi_bluff:
            return raise_return(random.uniform(1.0, 1.5), 20)
        if deception < 0.5:
            return call_return
        return fold_return

    # Weak hands: fold, sometimes call/raise
    if deception < 0.12:
        return raise_return(random.uniform(1.0, 1.5), 20)
    if deception < 0.3:
        return call_return
    return fold_return
