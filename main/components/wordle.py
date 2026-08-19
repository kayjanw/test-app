import random

import pandas as pd
from dash import html

from main.model.wordle import N_GUESSES, N_LETTERS, Guess


def create_grid(n_guesses: int = N_GUESSES, n_letters: int = N_LETTERS):
    grid = []
    for r in range(n_guesses):
        row = []
        for c in range(n_letters):
            row.append(
                html.Div(
                    id={"type": "wordle-tile", "id": f"{r}-{c}"},
                    className="wordle-tile",
                )
            )
        grid.append(
            html.Div(
                row,
                id={"type": "wordle-row", "id": r},
                style={},
                className="wordle-row",
            )
        )
    return grid


def get_guess_result(word, guess) -> list[str]:
    """Get results from a guess

    Args:
        word: correct word
        guess: guess word

    Returns:
        colour of the results
    """
    result = []
    for letter, guess_letter in zip(word, guess):
        if letter == guess_letter:
            result.append(Guess.correct)
        elif guess_letter in word:
            result.append(Guess.present)
        else:
            result.append(Guess.absent)
    return result


def get_tile_style(result_colour: str) -> dict[str, str]:
    return {
        "backgroundColor": result_colour,
        "border": f"2px solid {result_colour}",
        "color": "#ffffff",
    }


class Wordle:
    """Wordle game.
    Word bank retrieved from Kaggle https://www.kaggle.com/datasets/rtatman/english-word-frequency
    """

    def __init__(
        self, word: str = "", n_letters: int = N_LETTERS, attempts: int = N_GUESSES
    ):
        self.n_letters = n_letters
        self.attempts = attempts
        self.word = word or self.get_random_word()
        self.guesses = []

    @property
    def is_gameover(self) -> bool:
        return self.attempts == len(self.guesses) or self.is_win

    @property
    def is_win(self) -> bool:
        return self.guesses and self.guesses[-1] == self.word

    @classmethod
    def from_store(cls, store: dict[str, str | list[str]], n_letters: int = N_LETTERS):
        """Recreate wordle game state from dict

        Args:
            store: wordle game state
            n_letters: number of letters in word
        """
        if n_letters != len(store["word"]):
            # Create new game
            instance = cls(n_letters=n_letters)
        else:
            instance = cls(n_letters=n_letters, word=store["word"])
            instance.guesses = store["guesses"]
        return instance

    def to_store(self) -> dict[str, str | list[str]]:
        """Store wordle game state to dict"""
        return {
            "word": self.word,
            "guesses": self.guesses,
        }

    @staticmethod
    def _get_words():
        words = pd.read_csv("data/unigram_freq.csv").sort_values(
            "count", ascending=False
        )
        common_words = list(
            words.loc[(words["count"] >= 1_000_000)].astype(str).word.values
        )
        english_5chars_words = [
            i.upper() for i in common_words if isinstance(i, str) and len(i) == 5
        ]
        english_6chars_words = [
            i.upper() for i in common_words if isinstance(i, str) and len(i) == 6
        ]
        with open("data/wordle_5letters.txt", "w") as file:
            file.write(",".join(english_5chars_words))
        with open("data/wordle_6letters.txt", "w") as file:
            file.write(",".join(english_6chars_words))

    def get_random_word(self) -> str:
        """Get random word for Wordle from the word bank

        Returns:
            random word for Wordle
        """
        with open(f"data/wordle_{self.n_letters}letters.txt", "r") as file:
            content = file.read()
        word_bank = content.split(",")
        return random.choice(word_bank)

    def make_guess(self, guess: str) -> list[str]:
        """Get results from a guess, with error exception and updates self.guesses

        Args:
            guess: guess word

        Returns:
            colour of the results
        """
        guess = str(guess).strip().upper()
        if len(guess) != self.n_letters:
            raise ValueError(f"Word must be exactly {self.n_letters} letters long")
        result = get_guess_result(self.word, guess)
        self.guesses.append(guess)
        return result
