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
