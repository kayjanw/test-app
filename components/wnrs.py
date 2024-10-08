import os
import random
import re
from functools import reduce
from typing import Any, Dict, List, Optional

import pandas as pd
from dash import html

from components.helper import decrypt_workbook


class WNRS:
    """The WNRS object contains functions used for We're Not Really Strangers tab"""

    def __init__(self):
        """Read and initalize the card game"""
        try:
            self.WNRS_KEY = ENV["WNRS_KEY"]
        except NameError:
            try:
                self.WNRS_KEY = os.environ["WNRS_KEY"]
            except KeyError:
                print("No WNRS_KEY found")
                self.WNRS_KEY = ""

        self.data_path = (
            "data/"  # "https://github.com/kayjanw/test-app/raw/master/data/"
        )
        file = pd.ExcelFile(
            decrypt_workbook(f"{self.data_path}wnrs-game.xlsx", self.WNRS_KEY)
        )
        decks = file.sheet_names
        self.information = {}

        # Needed for game play
        self.playing_cards = None
        self.list_of_deck = []
        self.pointer = 0
        self.index = []

        for deck in decks:
            deck_data = file.parse(deck, header=None)
            deck_type = deck_data.iloc[1, 1]
            deck_description = deck_data.iloc[2, 1]
            deck_summary = deck_data.iloc[3, 1]

            if deck_type in self.information:
                self.information[deck_type][deck] = dict(
                    description=deck_description, summary=deck_summary
                )
            else:
                self.information[deck_type] = {
                    deck: dict(description=deck_description, summary=deck_summary)
                }

            deck_cards = pd.DataFrame(file.parse(deck, skiprows=5))
            if "Level" in deck_cards.columns:
                self.information[deck_type][deck]["levels"] = list(
                    map(str, deck_cards.Level.unique())
                )
            else:
                self.information[deck_type][deck]["levels"] = [1]

    def get_information(self) -> Dict[str, str]:
        """Get information (type, description, summary) of all card deck"""
        return self.information

    def get_all_cards(self) -> Dict[str, str]:
        """Get all cards to retrieve playable cards"""
        file = pd.ExcelFile(
            decrypt_workbook(f"{self.data_path}wnrs-game.xlsx", self.WNRS_KEY)
        )
        decks = file.sheet_names
        cards = {}

        for deck in decks:
            deck_data = file.parse(deck, header=None)
            deck_name = deck_data.iloc[0, 1]

            deck_cards = pd.DataFrame(file.parse(deck, skiprows=5))
            deck_cards_dict = {}
            if "Level" in deck_cards.columns:
                for level in deck_cards.Level.unique():
                    deck_cards_level = deck_cards[deck_cards["Level"] == level].copy()
                    deck_cards_level["Deck Name"] = deck_name
                    deck_cards_level["Deck"] = f"{deck} {level}"
                    deck_cards_dict[str(level)] = deck_cards_level[
                        ["Deck Name", "Deck", "Card", "Prompt"]
                    ].to_dict()
            else:
                deck_cards["Deck Name"] = deck_name
                deck_cards["Deck"] = deck
                deck_cards_dict[str(1)] = deck_cards[
                    ["Deck Name", "Deck", "Card", "Prompt"]
                ].to_dict()
            cards[deck] = deck_cards_dict
        return cards

    def get_all_playable_cards(self, list_of_deck: List[str]):
        """Initialize playing cards and index from list of deck for game play

        Args:
            list_of_deck: list of all selected games to play
        """
        assert list_of_deck, "Please select at least one deck to start with"
        cards = self.get_all_cards()
        playing_cards = []
        for selected_deck in list_of_deck:
            deck = " ".join(selected_deck.split(" ")[:-1])
            level = selected_deck.split(" ")[-1]
            playing_cards.append(pd.DataFrame(cards[deck][level]))
        playing_cards = reduce(lambda x, y: x.merge(y, how="outer"), playing_cards)
        playing_cards.index = playing_cards.index.map(str)
        self.playing_cards = playing_cards.to_dict()

    def initialize_game(self, list_of_deck: Optional[List[str]] = None):
        """Initialize new game

        Args:
            list_of_deck: list of all selected games to play
        """
        if list_of_deck is None:
            list_of_deck = ["Main Deck 1"]
        self.list_of_deck = list_of_deck
        self.get_all_playable_cards(list_of_deck)
        index = list(self.playing_cards["Deck"].keys())
        index = self.shuffle(index)
        self.index = index

    def load_game(self, list_of_deck: List[str], pointer: int, index: List[int]):
        """Load existing game from deck selection

        Args:
            list_of_deck: list of all selected games to play
            pointer: current pointer of card
            index: order of cards to play
        """
        self.get_all_playable_cards(list_of_deck)
        self.list_of_deck = list_of_deck
        self.pointer = pointer
        self.index = index

    def load_game_from_dict(self, game_dict: Dict[str, Any]):
        """Load existing game from dictionary

        Args:
            game_dict (dict): dictionary of existing game
        """
        self.playing_cards = game_dict["playing_cards"]
        self.list_of_deck = game_dict["list_of_deck"]
        self.pointer = game_dict["pointer"]
        self.index = game_dict["index"]

    def get_next_card(self):
        """Get next card

        Returns:
            (str, list, dict, str): card deck, prompt, style, counter
        """
        if self.pointer < len(self.index) - 1:
            self.pointer += 1
        return self.get_current_card()

    def get_previous_card(self):
        """Get previous card

        Returns:
            (str, list, dict, str): card deck, prompt, style, counter
        """
        if self.pointer > 0:
            self.pointer -= 1
        return self.get_current_card()

    def get_current_card(self):
        """Get current card

        Returns:
            (list, list, dict, str): card deck, prompt, style, counter
        """
        color_map = {
            "B1": ("#000000", "#FFFFFF"),  # black card white font (race edition)
            # white card black font (race, bumble, voting, own it edition)
            "B2": ("#FAFAEE", "#000000"),
            "Bl": ("#4598BA", "#000000"),  # blue card black font (bumble edition)
            "Br1": ("#4D1015", "#FFFFFF"),  # brown card white font (valentino edition)
            "Br2": ("#FAFAEE", "#4D1015"),  # white card brown font (valentino edition)
            "N": ("#282C69", "#FAFAEE"),  # navy card white font (voting edition)
            "O": ("#EB744C", "#000000"),  # orange card black font (bumble edition)
            "R": ("#BE001C", "#FAFAEE"),  # red (default)
            "P": ("#EEC4C5", "#BE001C"),  # pink (self-love edition)
            "S1": (
                "#5F86B5",
                "#FAFAEE",
            ),  # special blue card white font (own it edition)
            "S2": (
                "#AF2637",
                "#FAFAEE",
            ),  # special maroon card white font (own it edition)
            "S3": (
                "#275835",
                "#FAFAEE",
            ),  # special green card white font (own it edition)
            "V1": ("#EAD2E0", "#1695C8"),  # violet card blue font (cann edition)
            "V2": ("#FAFAEE", "#1695C8"),  # white card blue font (cann edition)
            "W": ("#FAFAEE", "#BE001C"),  # white (default)
            "Y": ("#F6CA69", "#FAFAEE"),  # yellow card white font (bumble edition)
        }

        index = str(self.index[self.pointer])
        card_deck_name = self.playing_cards["Deck Name"][index]
        card_deck = self.playing_cards["Deck"][index]
        card_type = self.playing_cards["Card"][index]
        card_prompt = self.playing_cards["Prompt"][index]

        # Post-processing
        card_bottom = [card_deck_name, html.Br(), card_deck]
        background_color, font_color = color_map[card_type]
        card_style = {"background-color": background_color, "color": font_color}
        card_counter = f"{self.pointer + 1} / {len(self.index)}"

        def append_line(current_list, current_sentence, current_style=None, pattern=0):
            if current_style is None:
                current_style = {}
            inline_style = {"display": "inline"}
            current_sentence = (
                current_sentence.replace("\\'", "'")
                .replace('\\"', '"')
                .replace("Wild Card ", "Wild Card:\\n")
                .replace("Reminder ", "Reminder:\\n")
                .split("\\n")
            )
            for idx, line in enumerate(current_sentence):
                if (
                    (pattern == 1 and idx == len(current_sentence) - 1)
                    or (pattern == 2)
                    or (pattern == 3 and idx == 0)
                ):
                    current_list.append(
                        html.P(line, style={**current_style, **inline_style})
                    )
                else:
                    current_list.append(html.P(line, style=current_style))
            return current_list

        # Different card style for reminder cards
        card_prompt1, card_prompt2, card_prompt3 = [], [], []
        if card_prompt.startswith("Reminder"):
            card_prompt = card_prompt.replace("Reminder ", "")
            card_prompt2 = html.P(["Reminder"])
            card_prompt_used = card_prompt3
        else:
            card_prompt_used = card_prompt1

        # Different card style for word colour
        word_colour = re.findall(r"\[(#\w+)\]\((.+?)\)", card_prompt)
        if len(word_colour):
            assert (
                len(word_colour) == 1
            ), "There are more than one word that need special formatting"
            _colour, _sentence = word_colour[0]
            a, b = card_prompt.split(f"[{_colour}]({_sentence})")
            card_prompt_used = append_line(card_prompt_used, a, pattern=1)
            card_prompt_used = append_line(
                card_prompt_used, _sentence, {"color": _colour}, pattern=2
            )
            card_prompt_used = append_line(card_prompt_used, b, pattern=3)
        else:
            card_prompt_used = append_line(card_prompt_used, card_prompt)

        return (
            card_bottom,
            [card_prompt1, card_prompt2, card_prompt3],
            card_style,
            card_counter,
        )

    def shuffle_remaining_cards(self):
        """Shuffle remaining cards, return next card

        Returns:
            (str, list, dict, str): card deck, prompt, style, counter
        """
        next_pointer = self.pointer + 1
        past_index = self.index[:next_pointer].copy()
        remaining_index = self.index[next_pointer:].copy()
        remaining_index = self.shuffle(remaining_index)
        new_index = [*past_index, *remaining_index]
        self.index = new_index
        return self.get_next_card()

    def shuffle(self, index: List[int]) -> List[int]:
        """Shuffle algorithm to preserve 'final' cards location

        Args:
            index: list of index to be shuffled

        Returns:
            shuffled index
        """
        index_final_cards = [
            k for k, v in self.playing_cards["Deck"].items() if v.endswith("Final")
        ]
        index_final_cards = list(set(index_final_cards).intersection(set(index)))
        index_without_final = list(set(index) - set(index_final_cards))
        random.shuffle(index_final_cards)
        random.shuffle(index_without_final)
        index = index_without_final + index_final_cards
        return index

    def convert_to_store_format(self) -> Dict[str, Any]:
        """Convert data to save format"""
        data_store = dict(
            playing_cards=self.playing_cards,
        )
        return data_store

    def convert_to_save_format(self) -> Dict[str, Any]:
        """Convert data to save format"""
        data_save = dict(
            list_of_deck=self.list_of_deck,
            index=self.index,
            pointer=self.pointer,
        )
        return data_save
