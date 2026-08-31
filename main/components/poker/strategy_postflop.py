import random

from main.components.poker.strategy_preflop import (
    call_return,
    check_return,
    fold_return,
    round_up,
)
from main.model.poker import Card
from main.model.poker.poker import HAND_STRENGTH


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
