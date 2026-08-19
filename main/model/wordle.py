from dataclasses import dataclass

N_GUESSES = 6
N_LETTERS = 5


@dataclass
class Guess:
    correct = "#6aaa64"  # Green
    present = "#c9b458"  # Yellow
    absent = "#787c7e"  # Gray
    default = "#ffffff"  # White
