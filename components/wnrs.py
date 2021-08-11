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
        self.cards = {}

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
                self.information[deck_type][deck] = dict(description=deck_description, summary=deck_summary)
            else:
                self.information[deck_type] = {deck: dict(description=deck_description, summary=deck_summary)}

            deck_cards = pd.DataFrame(file.parse(deck, skiprows=4))
            deck_cards_dict = {}
            if 'Level' in deck_cards.columns:
                self.information[deck_type][deck]["levels"] = list(map(str, deck_cards.Level.unique()))
                for level in deck_cards.Level.unique():
                    deck_cards_level = deck_cards[deck_cards["Level"] == level].copy()
                    deck_cards_level["Deck"] = f"{deck} {level}"
                    deck_cards_dict[str(level)] = deck_cards_level[["Deck", "Card", "Prompt"]].to_dict()
            else:
                self.information[deck_type][deck]["levels"] = [1]
                deck_cards["Deck"] = deck
                deck_cards_dict[str(1)] = deck_cards[["Deck", "Card", "Prompt"]].to_dict()
            self.cards[deck] = deck_cards_dict

    def get_information(self):
        """
        Get information (type, description, summary) of all card deck

        Returns:
            (dict)
        """
        return self.information

    def get_all_cards(self, list_of_deck):
        """
        Initialize playing cards and index from list of deck for gameplay

        Args:
            list_of_deck (list): List of all selected games to play
        """
        assert list_of_deck, "Please select at least one deck to start with"
        playing_cards = []
        for selected_deck in list_of_deck:
            deck = " ".join(selected_deck.split(" ")[:-1])
            level = selected_deck.split(" ")[-1]
            playing_cards.append(pd.DataFrame(self.cards[deck][level]))
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
        self.get_all_cards(list_of_deck)
        index = list(self.playing_cards['Deck'].keys())
        random.shuffle(index)
        self.index = index

    def load_game(self, list_of_deck, pointer, index):
        """
        Load existing game

        Args:
            list_of_deck (list): List of all selected games to play
            pointer (int): Current pointer of card
            index (list): Order of cards to play
        """
        self.get_all_cards(list_of_deck)
        self.pointer = pointer
        self.index = index

    def get_next_card(self):
        """
        Get next card

        Returns:
            (str, str, str): Card deck, type, card prompt
        """
        if self.pointer < len(self.index) - 1:
            self.pointer += 1
        idx = str(self.index[self.pointer])
        card_deck = self.playing_cards['Deck'][idx]
        card_type = self.playing_cards['Card'][idx]
        card_prompt = self.playing_cards['Prompt'][idx]
        return card_deck, card_type, card_prompt

    def get_previous_card(self):
        """
        Get previous card

        Returns:
            (str, str, str): Card deck, type, card prompt
        """
        if self.pointer > 0:
            self.pointer -= 1
        idx = str(self.index[self.pointer])
        card_deck = self.playing_cards['Deck'][idx]
        card_type = self.playing_cards['Card'][idx]
        card_prompt = self.playing_cards['Prompt'][idx]
        return card_deck, card_type, card_prompt

    def get_current_card(self):
        """
        Get current card

        Returns:
            (str, str, str): Card deck, type, card prompt
        """
        idx = str(self.index[self.pointer])
        card_deck = self.playing_cards['Deck'][idx]
        card_type = self.playing_cards['Card'][idx]
        card_prompt = self.playing_cards['Prompt'][idx]
        return card_deck, card_type, card_prompt
