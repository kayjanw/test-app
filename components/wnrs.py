import dash_html_components as html
import pandas as pd
import random

from functools import reduce


class WNRS:
    def __init__(self):
        """
        Read and initalize the card game
        """
        file = pd.ExcelFile("data/WNRS.xlsx")
        decks = file.sheet_names
        self.information = {}

        # Needed for game play
        self.playing_cards = None
        self.pointer = 0
        self.index = []

        for deck in decks:
            deck_data = file.parse(deck, header=None)
            deck_type = deck_data.iloc[0, 1]
            deck_description = deck_data.iloc[1, 1]
            deck_summary = deck_data.iloc[2, 1]

            if deck_type in self.information:
                self.information[deck_type][deck] = dict(
                    description=deck_description, summary=deck_summary)
            else:
                self.information[deck_type] = {deck: dict(
                    description=deck_description, summary=deck_summary)}

            deck_cards = pd.DataFrame(file.parse(deck, skiprows=4))
            if "Level" in deck_cards.columns:
                self.information[deck_type][deck]["levels"] = list(
                    map(str, deck_cards.Level.unique()))
            else:
                self.information[deck_type][deck]["levels"] = [1]

    def get_information(self):
        """
        Get information (type, description, summary) of all card deck

        Returns:
            (dict)
        """
        return self.information

    @staticmethod
    def get_all_cards():
        """
        Get all cards to retrieve playable cards

        Returns:
            (dict)
        """
        file = pd.ExcelFile("data/WNRS.xlsx")
        decks = file.sheet_names
        cards = {}

        for deck in decks:
            deck_cards = pd.DataFrame(file.parse(deck, skiprows=4))
            deck_cards_dict = {}
            if "Level" in deck_cards.columns:
                for level in deck_cards.Level.unique():
                    deck_cards_level = deck_cards[deck_cards["Level"] == level].copy()
                    deck_cards_level["Deck"] = f"{deck} {level}"
                    deck_cards_dict[str(level)] = deck_cards_level[[
                        "Deck", "Card", "Prompt"]].to_dict()
            else:
                deck_cards["Deck"] = deck
                deck_cards_dict[str(1)] = deck_cards[[
                    "Deck", "Card", "Prompt"]].to_dict()
            cards[deck] = deck_cards_dict
        return cards

    def get_all_playable_cards(self, list_of_deck):
        """
        Initialize playing cards and index from list of deck for gameplay

        Args:
            list_of_deck (list): List of all selected games to play
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

    def initialize_game(self, list_of_deck=None):
        """
        Initialize new game

        Args:
            list_of_deck (list): List of all selected games to play
        """
        if list_of_deck is None:
            list_of_deck = ["Main Deck 1"]
        self.get_all_playable_cards(list_of_deck)
        index = list(self.playing_cards["Deck"].keys())
        random.shuffle(index)
        self.index = index

    def load_game(self, list_of_deck, pointer, index):
        """
        Load existing game from deck selection

        Args:
            list_of_deck (list): List of all selected games to play
            pointer (int): Current pointer of card
            index (list): Order of cards to play
        """
        self.get_all_playable_cards(list_of_deck)
        self.pointer = pointer
        self.index = index

    def load_game_from_dict(self, game_dict):
        """
        Load existing game from dictionary

        Args:
            game_dict (dict): Dictionary of existing game, called with WNRS().__dict__
        """
        self.playing_cards = game_dict['playing_cards']
        self.pointer = game_dict['pointer']
        self.index = game_dict['index']

    def get_next_card(self):
        """
        Get next card

        Returns:
            (str, list, dict, str): Card deck, prompt, style, counter
        """
        if self.pointer < len(self.index) - 1:
            self.pointer += 1
        return self.get_current_card()

    def get_previous_card(self):
        """
        Get previous card

        Returns:
            (str, list, dict, str): Card deck, prompt, style, counter
        """
        if self.pointer > 0:
            self.pointer -= 1
        return self.get_current_card()

    def get_current_card(self):
        """
        Get current card

        Returns:
            (str, list, dict, str): Card deck, prompt, style, counter
        """
        color_map = {
            'B1': ('#000000', '#FFFFFF'),  # black card white font (race edition)
            'B2': ('#FAFAEE', '#000000'),  # white card black font (race, bumble, voting edition)
            'Bl': ('#4598BA', '#000000'),  # blue card black font (bumble edition)
            'Br1': ('#4D1015', '#FFFFFF'),  # brown card white font (valentino edition)
            'Br2': ('#FAFAEE', '#4D1015'),  # white card brown font (valentino edition)
            'N': ('#282C69', '#FAFAEE'),  # navy card white font (voting edition)
            'O': ('#EB744C', '#000000'),  # orange card black font (bumble edition)
            'R': ('#BE001C', '#FAFAEE'),  # red (default)
            'P': ('#EEC4C5', '#BE001C'),  # pink (self-love edition)
            'V1': ('#EAD2E0', '#1695C8'),  # violet card blue font (cann edition)
            'V2': ('#FAFAEE', '#1695C8'),  # white card blue font (cann edition)
            'W': ('#FAFAEE', '#BE001C'),  # white (default)
            'Y': ('#F6CA69', '#FAFAEE'),  # yellow card white font (bumble edition)
        }

        idx = str(self.index[self.pointer])
        card_deck = self.playing_cards["Deck"][idx]
        card_type = self.playing_cards["Card"][idx]
        card_prompt = self.playing_cards["Prompt"][idx]

        # Post-processing
        card_deck2 = ["We're Not Really Strangers", html.Br(), card_deck]
        card_prompt = card_prompt \
            .replace("\\'", "'") \
            .replace('\\"', '"') \
            .replace('Wild Card ', 'Wild Card:\\n') \
            .replace('Reminder ', 'Reminder:\\n') \
            .split('\\n')
        card_prompt2 = []
        for line in card_prompt:
            card_prompt2.append(line)
            card_prompt2.append(html.Br())
        card_prompt2.pop()
        background_color, font_color = color_map[card_type]
        card_style = {'background-color': background_color, 'color': font_color}
        card_counter = f"{self.pointer + 1} / {len(self.index)}"
        return card_deck2, card_prompt2, card_style, card_counter

    def shuffle_remaining_cards(self):
        """
        Shuffle remaining cards, return next card

        Returns:
            (str, list, dict, str): Card deck, prompt, style, counter
        """
        past_index = self.index[:self.pointer + 1].copy()
        remaining_index = self.index[self.pointer + 1:].copy()
        random.shuffle(remaining_index)
        new_index = [*past_index, *remaining_index]
        self.index = new_index
        return self.get_next_card()
