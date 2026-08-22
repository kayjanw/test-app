import random

import dash_mantine_components as dmc
from pokerlib import HandParser

from common.components.helper import return_message
from main.model.poker import BLIND, DECK, STAGES, STRONG_HANDS, Card


class Poker:
    def __init__(
        self,
        stage: str = STAGES[0],
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
    ):
        self.stage = stage
        self.pot = pot
        self.to_call = to_call
        self.card_user = card_user or []
        self.card_cpu = card_cpu or []
        self.card_board = card_board or []
        self.chips_user = chips_user
        self.chips_cpu = chips_cpu
        self.game_over = game_over
        self.player_moved = player_moved
        self.result = result

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
        )

    @classmethod
    def from_state(cls, state):
        state = state.copy()
        for k in ["card_user", "card_cpu", "card_board"]:
            state[k] = [Card.from_str(card) for card in state[k].split(",") if card]
        return cls(**state)

    def render_cards(self) -> tuple[list[dmc.Paper], list[dmc.Paper], list[dmc.Paper]]:
        if self.stage in STAGES[:2]:
            visible_cards = []
        elif self.stage in STAGES[:3]:
            visible_cards = self.card_board[:3]
        elif self.stage in STAGES[:4]:
            visible_cards = self.card_board[:4]
        else:
            visible_cards = self.card_board

        return (
            render_card(self.card_user),
            render_card(
                self.card_cpu, hidden=True if self.stage in STAGES[:-1] else False
            ),
            render_card(visible_cards),
        )

    def advance_stage(self):
        self.stage = STAGES[STAGES.index(self.stage) + 1]

    def new_game(self) -> str:
        if not self.chips_user:
            self.result = "You do not have any chips left to play."
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

    def fold(self):
        self.chips_cpu += self.pot
        self.pot = 0
        self.to_call = 0
        self.result = return_message["poker_fold"].format(p1="You", p2="CPU")
        self.player_moved = True
        self.game_over = True

    def check_or_call(self):
        if self.to_call:
            self.to_call = min(self.to_call, self.chips_user)
            self.chips_user -= self.to_call
            self.pot += self.to_call
            self.result = return_message["poker_call"].format(
                p1="You", amount=self.to_call
            )
            self.to_call = 0
            self.advance_stage()
        else:
            self.result = return_message["poker_check"].format(p1="You")
            self.player_moved = True

    def bet_or_raise(self, raise_by: int):
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
        self.result = return_message["poker_raise"].format(p1="You", amount=raise_by)
        self.player_moved = True

    @staticmethod
    def get_parser(cards: list[Card]):
        """Create and parse a pokerlib HandParser."""
        parser = HandParser([card.pokerlib for card in cards])
        parser.parse()
        return parser

    def choose_move(self) -> tuple[str, int]:
        """Rule-based CPU.

        Returns:
            ("fold" | "check" | "call" | "raise", raise_by)
        """
        # Pre-flop
        if self.stage in STAGES[:2]:
            rank1, rank2 = self.card_cpu[0].rank, self.card_cpu[1].rank
            pair = rank1 == rank2
            high_card = rank1 in {"10", "J", "Q", "K", "A"} or rank2 in {
                "10",
                "J",
                "Q",
                "K",
                "A",
            }

            if pair:
                return (
                    ("raise", 20)
                    if random.random() < 0.65
                    else (("call", 0) if self.to_call else ("check", 0))
                )

            if high_card:
                if self.to_call:
                    return "call", 0
                return ("raise", 20) if random.random() < 0.35 else ("check", 0)

            if self.to_call == 0:
                return "check", 0
            return ("call", 0) if self.to_call <= 15 else ("fold", 0)

        # Post-flop
        parser = self.get_parser(self.card_cpu + self.card_board)
        hand_type = parser.handenum.name

        if hand_type in STRONG_HANDS:
            if random.random() < 0.55:
                return "raise", 30
            return ("call", 0) if self.to_call else ("check", 0)

        if hand_type == "PAIR":
            if self.to_call > 50:
                return "fold", 0
            if self.to_call:
                return "call", 0
            return ("raise", 20) if random.random() < 0.25 else ("check", 0)

        if self.to_call == 0:
            return "check", 0

        return ("call", 0) if self.to_call <= 15 else ("fold", 0)

    def cpu_fold(self):
        self.chips_user += self.pot
        self.pot = 0
        self.to_call = 0
        self.result += return_message["poker_fold"].format(p1="CPU", p2="You")
        self.game_over = True

    def cpu_check(self):
        self.result += return_message["poker_check"].format(p1="CPU")
        self.advance_stage()

    def cpu_call(self):
        self.to_call = min(self.to_call, self.chips_cpu)
        self.chips_cpu -= self.to_call
        self.pot += self.to_call
        self.result += return_message["poker_call"].format(
            p1="CPU", amount=self.to_call
        )
        self.to_call = 0
        self.advance_stage()

    def cpu_raise(self, raise_by):
        if self.to_call >= self.chips_cpu:
            self.cpu_call()
            return
        total_amount = min(self.to_call + raise_by, self.chips_cpu)
        raise_by = total_amount - self.to_call
        self.chips_cpu -= total_amount
        self.pot += raise_by
        self.to_call = raise_by
        self.result = return_message["poker_raise"].format(p1="CPU", amount=raise_by)

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

    @staticmethod
    def hand_name(parser):
        return parser.handenum.name.replace("_", " ").title()

    def evaluate_winner(self):
        """Return (winner, message) at showdown"""
        player_parser = self.get_parser(self.card_user + self.card_board)
        ai_parser = self.get_parser(self.card_cpu + self.card_board)

        player_hand = self.hand_name(player_parser)
        cpu_hand = self.hand_name(ai_parser)

        if player_parser > ai_parser:
            return "player", f"You win with a {player_hand}! CPU had a {cpu_hand}."
        if ai_parser > player_parser:
            return "cpu", f"CPU wins with a {cpu_hand}. You had a {player_hand}."
        return "split", f"Split pot! Both players have a {player_hand}."

    def showdown(self):
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


def render_card(cards: list[Card], hidden: bool = False) -> list[dmc.Paper]:
    if hidden:
        return [dmc.Paper("🂠", className="poker-card poker-card-hidden") for _ in cards]
    return [
        dmc.Paper(str(card), style={"color": card.colour}, className="poker-card")
        for card in cards
    ]


def render_amount(amount: int) -> str:
    return "${:,}".format(amount)
