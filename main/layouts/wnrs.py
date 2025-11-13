from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_mantine_components as dmc
from dash import dcc, html

from common.components.helper import colour_palette, encode_dict
from common.layouts.main import content_header
from main.components import WNRS
from main.layouts.main import style_hidden, style_wnrs_text


def modal_palette():
    # swatches = [
    #     "#25262b", "#868e96", "#fa5252", "#e64980", "#be4bdb", "#7950f2", "#4c6ef5",
    #     "#228be6", "#15aabf", "#12b886", "#40c057", "#82c91e", "#fab005", "#fd7e14"
    # ]
    swatches_text = [
        "#FFFFFF",
        "#FAFAEE",
        "#F6CA69",
        "#BE001C",
        "#1695C8",
        "#4D1015",
        "#000000",
    ]
    swatches_background = [
        "#FAFAEE",
        "#F6CA69",
        "#EAD2E0",
        "#EEC4C5",
        "#EB744C",
        "#BE001C",
        "#AF2637",
        "#275835",
        "#4598BA",
        "#5F86b5",
        "#282C69",
        "#4D1015",
        "#000000",
    ]
    return [
        html.Div(
            [
                daq.ColorPicker(
                    id="colorpicker-wnrs-text",
                    label="Text Colour",
                    value=dict(),
                    className="p-bold",
                ),
                dmc.ColorPicker(
                    id="swatches-wnrs-text",
                    swatches=swatches_text,
                    swatchesPerRow=9,
                    withPicker=False,
                    format="hex",
                    value="",
                    className="custom-div-inline",
                    fullWidth=True,
                    styles={
                        "swatches": {"justifyContent": "center"},
                    },
                ),
            ],
            className="custom-div-inline custom-margin-bottom custom-margin-left custom-margin-right",
        ),
        html.Div(
            [
                daq.ColorPicker(
                    id="colorpicker-wnrs-background",
                    label="Background Colour",
                    value=dict(),
                    className="p-bold",
                ),
                dmc.ColorPicker(
                    id="swatches-wnrs-background",
                    swatches=swatches_background,
                    swatchesPerRow=9,
                    withPicker=False,
                    format="hex",
                    value="",
                    className="custom-div-inline",
                    styles={
                        "swatches": {"justifyContent": "center"},
                    },
                ),
            ],
            className="custom-div-inline custom-margin-bottom custom-margin-left custom-margin-right",
        ),
    ]


def modal_contribute():
    return [
        html.P(
            "You can contribute too! Suggest prompts that you would like to see in the game, "
            "or contribute a card game!",
        ),
        html.P(
            dcc.Input(
                id="input-wnrs-suggestion",
                type="text",
                placeholder="Your prompt(s)",
                style={
                    "width": "100%",
                    "margin-bottom": "3px",
                },
            ),
        ),
        html.P(
            dcc.Textarea(
                id="input-wnrs-suggestion2",
                value="",
                placeholder="(Optional) Additional comments or feedback, include your "
                "contact details if you expect a reply!",
                style={"width": "100%"},
            ),
        ),
        html.Button("Send", id="button-wnrs-send-ok"),
        html.P(id="wnrs-suggestion-reply"),
        html.Br(),
    ]


@dataclass
class Deck:
    button_text: str
    button_id: str
    button_style: Optional[Dict[str, str]] = None


def create_deck_rows(app, decks_data, wnrs_information, deck_type) -> List[html.Div]:
    """Create rows of deck for a single deck type"""
    return [
        html.Div(
            [
                html.Span(
                    [
                        deck_name,
                        html.Sup(deck_info.get("blinker", ""), className="blinker"),
                    ],
                    className="span-short",
                ),
                html.Img(
                    src=app.get_asset_url("info.svg"),
                    id=deck_name + "-help",
                ),
                dbc.Tooltip(
                    wnrs_information[deck_type][deck_name]["description"],
                    placement="right",
                    target=deck_name + "-help",
                    className="tooltip",
                ),
                html.Div(
                    [
                        dbc.Button(
                            deck.button_text,
                            id={"type": "wnrs-deck-button", "id": deck.button_id},
                            style=deck.button_style,
                            className="button-wnrs",
                        )
                        for deck in deck_info["decks"]
                    ],
                    className="wnrs-level",
                ),
            ],
            className="custom-div-flex div-with-image div-with-image-left small-image",
        )
        for deck_name, deck_info in decks_data.items()
    ]


def create_decks_div(
    app, all_decks_data, wnrs_information
) -> List[Union[html.P, html.Div, html.Br]]:
    """Create rows of deck for all deck types"""
    return [
        _item
        for _deck_type_data in [
            [
                html.P(
                    [
                        deck_type,
                        html.Sup(decks_data.get("blinker", ""), className="blinker"),
                    ],
                    style=style_wnrs_text,
                ),
                *create_deck_rows(app, decks_data["data"], wnrs_information, deck_type),
            ]
            for deck_type, decks_data in all_decks_data.items()
        ]
        for _item in _deck_type_data
    ] + [html.Br()]


def wnrs_tab(app):
    wnrs_game = WNRS()
    list_of_deck = ["Main Deck 1"]
    wnrs_game.initialize_game(list_of_deck)
    wnrs_information = wnrs_game.get_information()
    data_store = wnrs_game.convert_to_store_format()
    data_save = wnrs_game.convert_to_save_format()

    # sample_data = {
    #     "deck_name": {
    #         "decks": [
    #             Deck("Level 1", "gagG Edition 1"),
    #             Deck("Level 2", "gagag Edition 2"),
    #             Deck("Level 3", "gaga Edition 3"),
    #         ],
    #     },
    # }

    def modal_deck():
        all_decks_data = {
            "Main Deck": {
                "data": {
                    "Main Deck": {
                        "decks": [
                            Deck(
                                "Level 1",
                                "Main Deck 1",
                                {"background-color": colour_palette["dark_pink"]},
                            ),
                            Deck("Level 2", "Main Deck 2"),
                            Deck("Level 3", "Main Deck 3"),
                            Deck("Final Card", "Main Deck Final"),
                        ],
                    },
                }
            },
            "Crossover": {
                "data": {
                    "Bumble x BFF Edition": {
                        "decks": [
                            Deck("Level 1", "Bumble x BFF Edition 1"),
                            Deck("Level 2", "Bumble x BFF Edition 2"),
                            Deck("Level 3", "Bumble x BFF Edition 3"),
                        ],
                    },
                    "Bumble Bizz Edition": {
                        "decks": [
                            Deck("Level 1", "Bumble Bizz Edition 1"),
                            Deck("Level 2", "Bumble Bizz Edition 2"),
                            Deck("Level 3", "Bumble Bizz Edition 3"),
                        ],
                    },
                    "Bumble Date Edition": {
                        "decks": [
                            Deck("Level 1", "Bumble Date Edition 1"),
                            Deck("Level 2", "Bumble Date Edition 2"),
                            Deck("Level 3", "Bumble Date Edition 3"),
                        ],
                    },
                    "Cann Edition": {
                        "blinker": "Drinking",
                        "decks": [
                            Deck("Level 1", "Cann Edition 1"),
                            Deck("Level 2", "Cann Edition 2"),
                            Deck("Level 3", "Cann Edition 3"),
                        ],
                    },
                    "Valentino Edition": {
                        "blinker": "Reflect",
                        "decks": [
                            Deck("Level 1", "Valentino Edition 1"),
                        ],
                    },
                }
            },
            "Expansion": {
                "data": {
                    "Honest Dating Edition": {
                        "decks": [
                            Deck("Level 1", "Honest Dating Edition 1"),
                            Deck("Level 2", "Honest Dating Edition 2"),
                            Deck("Level 3", "Honest Dating Edition 3"),
                        ],
                    },
                    "Inner Circle Edition": {
                        "decks": [
                            Deck("Level 1", "Inner Circle Edition 1"),
                            Deck("Level 2", "Inner Circle Edition 2"),
                            Deck("Level 3", "Inner Circle Edition 3"),
                        ],
                    },
                    "Own It Edition": {
                        "decks": [
                            Deck("Level 1", "Own It Edition 1"),
                        ],
                    },
                    "Relationship Edition": {
                        "decks": [
                            Deck("Level 1", "Relationship Edition 1"),
                            Deck("Level 2", "Relationship Edition 2"),
                            Deck("Level 3", "Relationship Edition 3"),
                        ],
                    },
                }
            },
            "Online": {
                "data": {
                    "Race and Privilege Edition": {
                        "decks": [
                            Deck("Level 1", "Race and Privilege Edition 1"),
                            Deck("Level 2", "Race and Privilege Edition 2"),
                            Deck("Level 3", "Race and Privilege Edition 3"),
                        ],
                    },
                    "Quarantine Edition": {
                        "decks": [
                            Deck("Level 1", "Quarantine Edition 1"),
                            Deck("Level 2", "Quarantine Edition 2"),
                            Deck("Level 3", "Quarantine Edition 3"),
                            Deck("Final Card", "Quarantine Edition Final"),
                        ],
                    },
                    "Voting Edition": {
                        "decks": [
                            Deck("Level 1", "Voting Edition 1"),
                        ],
                    },
                }
            },
            "Single-Player": {
                "data": {
                    "Breakup Edition": {
                        "decks": [
                            Deck("Level 1", "Breakup Edition 1"),
                            Deck("ChatGPT", "Breakup Edition ChatGPT"),
                            Deck("Final Card", "Breakup Edition Final"),
                        ],
                    },
                    "Existential Crisis Edition": {
                        "blinker": "Mine",
                        "decks": [
                            Deck("Level 1", "Existential Crisis Edition 1"),
                        ],
                    },
                    "Forgiveness Edition": {
                        "decks": [
                            Deck("Level 1", "Forgiveness Edition 1"),
                            Deck("ChatGPT", "Forgiveness Edition ChatGPT"),
                        ],
                    },
                    "Healing Edition": {
                        "decks": [
                            Deck("Level 1", "Healing Edition 1"),
                        ],
                    },
                    "Self-Love Edition": {
                        "decks": [
                            Deck("Level 1", "Self-Love Edition 1"),
                            Deck("Final Card", "Self-Love Edition Final"),
                        ],
                    },
                    "Self-Reflection Edition": {
                        "decks": [
                            Deck("Level 1", "Self-Reflection Edition 1"),
                        ],
                    },
                }
            },
            "Gotmann": {
                "blinker": "improve relationship",
                "data": {
                    "Love Maps": {
                        "decks": [
                            Deck("Level 1", "Love Maps 1"),
                        ],
                    },
                    "Open Ended Questions": {
                        "decks": [
                            Deck("Level 1", "Open Ended Questions 1"),
                        ],
                    },
                    "Rituals of Connection": {
                        "decks": [
                            Deck("Level 1", "Rituals of Connection 1"),
                        ],
                    },
                    "Opportunity": {
                        "decks": [
                            Deck("Level 1", "Opportunity 1"),
                        ],
                    },
                    "Couple Questions": {
                        "decks": [
                            Deck("Ice Breaker", "Couple Questions IceBreaker"),
                            Deck("Family and Childhood", "Couple Questions Childhood"),
                            Deck("Relationship", "Couple Questions Relationship"),
                            Deck("Sex and Kids", "Couple Questions Sex&Kids"),
                            Deck("Marriage", "Couple Questions Marriage"),
                        ],
                    },
                    "Work Questions": {
                        "decks": [
                            Deck("Creative", "Work Questions Creative"),
                        ],
                    },
                },
            },
        }
        return create_decks_div(app, all_decks_data, wnrs_information)

    def modal_help():
        return [
            html.P(
                "How to Play (2-6 players)",
                className="p-short p-bold neucha-font",
            ),
            html.P(
                [
                    "The game is played on a single device. Sit in a circle with device in "
                    "middle of all players. Select the decks",
                    html.Img(src=app.get_asset_url("game.png")),
                    "you want to play with and the levels. Players take turn to answer "
                    "questions shown on the screen and tap on the right side of card to "
                    "proceed to next question. Feel free to shuffle",
                    html.Img(src=app.get_asset_url("shuffle.png")),
                    "the cards if needed.",
                ],
                className="div-with-image div-with-small-image-left div-with-small-image-right small-image",
            ),
            html.Br(),
            html.P(
                "Wildcards",
                style={"margin-top": "20px"},
                className="p-short p-bold neucha-font",
            ),
            html.P(
                [
                    "If you're presented with a wildcard you must complete the instructions "
                    "otherwise stated. These cards can appear at any moment during the game!"
                ],
            ),
            html.Br(),
            html.P(
                "Save your Progress",
                style={"margin-top": "20px"},
                className="p-short p-bold neucha-font",
            ),
            html.P(
                [
                    "Couldn't manage to go through all the cards in one session? Save your "
                    "progress",
                    html.Img(src=app.get_asset_url("download.svg")),
                    "and load the game next time to pick up "
                    "exactly where you left off.",
                ],
                className="div-with-image div-with-small-image-left div-with-small-image-right small-image",
            ),
            html.Br(),
            html.P(
                "Customize Theme",
                style={"margin-top": "20px"},
                className="p-short p-bold neucha-font",
            ),
            html.P(
                [
                    "Change the card background and font colour",
                    html.Img(src=app.get_asset_url("palette.png")),
                    "to customize it to your liking! You can change and reset the theme "
                    "anytime during the game.",
                ],
                className="div-with-image div-with-small-image-left div-with-small-image-right small-image",
            ),
            html.Br(),
            html.P(
                "Want to Contribute?",
                style={"margin-top": "20px"},
                className="p-short p-bold neucha-font",
            ),
            html.P(
                [
                    "If you have prompts to suggest or a card deck you want to contribute, "
                    "do not hesitate to reach out",
                    html.Img(src=app.get_asset_url("idea.png")),
                ],
                className="div-with-image div-with-small-image-left div-with-small-image-right small-image",
            ),
            html.P(
                html.P("Have fun!", className="rainbow"),
                style={"margin-top": "20px"},
                className="custom-div-center p-short p-bold",
            ),
            html.Br(),
        ]

    return html.Div(
        [
            content_header(
                [
                    "We're Not Really Strangers",
                    html.Button(
                        html.Span(
                            html.Img(src=app.get_asset_url("help.png")),
                            title="How to play",
                        ),
                        id={"type": "button-modal-wnrs", "index": "modal-help"},
                        className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                    ),
                ],
                "",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.P(id="wnrs-prompt"),
                                            html.P(id="wnrs-reminder-text"),
                                            html.P(id="wnrs-reminder"),
                                            html.P(
                                                [
                                                    "We're Not Really Strangers",
                                                    html.Br(),
                                                    html.Br(),
                                                ],
                                                id="wnrs-deck",
                                            ),
                                        ],
                                        style={
                                            "position": "relative",
                                            "height": "100%",
                                            "text-transform": "uppercase",
                                        },
                                    )
                                ],
                                id="wnrs-card",
                                style={},
                            ),
                            html.Button(
                                html.P("👆 Tap here for previous card"),
                                id="button-wnrs2-back",
                                style={},
                            ),
                            html.Button(
                                html.P("👆 Tap here for next card"),
                                id="button-wnrs2-next",
                                style={},
                            ),
                        ],
                        id="div-wnrs",
                        className="custom-div-center div-with-invisible-button",
                    ),
                    html.Div(
                        [
                            html.P("- / -", id="wnrs-counter"),
                        ]
                    ),
                    html.Div(
                        [
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("next.png")),
                                    title="Back",
                                ),
                                id="button-wnrs-back",
                                className="div-with-image small-image image-dark-blue invisible-button image-horizontal-flip vertical-center",
                            ),
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("game.png")),
                                    title="Select deck",
                                ),
                                id={
                                    "type": "button-modal-wnrs",
                                    "index": "modal-select",
                                },
                                className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("shuffle.png")),
                                    title="Shuffle remaining cards",
                                ),
                                id="button-wnrs-shuffle-ok",
                                className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
                            html.Form(
                                [
                                    dcc.Input(
                                        value=encode_dict(data_save),
                                        name="result",
                                        type="text",
                                        style=style_hidden,
                                        id="input-wnrs",
                                    ),
                                    html.Button(
                                        html.Span(
                                            html.Img(
                                                src=app.get_asset_url("download.svg")
                                            ),
                                            title="Save progress",
                                        ),
                                        type="submit",
                                        id="button-wnrs-download-ok",
                                        className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                                    ),
                                ],
                                method="POST",
                                action="/download_dict/",
                                style={"display": "inline-block"},
                            ),
                            html.A(
                                [
                                    dcc.Upload(
                                        [
                                            html.Span(
                                                html.Img(
                                                    src=app.get_asset_url("upload.svg")
                                                ),
                                                title="Upload past progress",
                                            ),
                                        ],
                                        id="uploadwnrs-button",
                                        multiple=False,
                                    )
                                ],
                                className="custom-div-center div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("palette.png")),
                                    title="Customize theme",
                                ),
                                id={
                                    "type": "button-modal-wnrs",
                                    "index": "modal-palette",
                                },
                                className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("idea.png")),
                                    title="Send in your card prompt ideas",
                                ),
                                id={
                                    "type": "button-modal-wnrs",
                                    "index": "modal-contribute",
                                },
                                className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("next.png")),
                                    title="Next",
                                ),
                                id="button-wnrs-next",
                                className="div-with-image small-image image-dark-blue invisible-button vertical-center",
                            ),
                        ]
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Instructions")),
                            dbc.ModalBody(
                                modal_help(),
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close",
                                    id={
                                        "type": "button-close-modal-wnrs",
                                        "index": "modal-help",
                                    },
                                )
                            ),
                        ],
                        id={"type": "modal-wnrs", "index": "modal-help"},
                        is_open=False,
                        centered=True,
                        size="lg",
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Select Deck")),
                            dbc.ModalBody(modal_deck()),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close",
                                    id={
                                        "type": "button-close-modal-wnrs",
                                        "index": "modal-select",
                                    },
                                )
                            ),
                        ],
                        id={"type": "modal-wnrs", "index": "modal-select"},
                        is_open=False,
                        centered=True,
                        size="lg",
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Customize Theme")),
                            dbc.ModalBody(
                                modal_palette(), className="custom-div-center"
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button(
                                        "Reset",
                                        id="button-reset-style",
                                    ),
                                    dbc.Button(
                                        "Close",
                                        id={
                                            "type": "button-close-modal-wnrs",
                                            "index": "modal-palette",
                                        },
                                    ),
                                ]
                            ),
                        ],
                        id={"type": "modal-wnrs", "index": "modal-palette"},
                        is_open=False,
                        centered=True,
                        size="lg",
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Contribute")),
                            dbc.ModalBody(modal_contribute()),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close",
                                    id={
                                        "type": "button-close-modal-wnrs",
                                        "index": "modal-contribute",
                                    },
                                )
                            ),
                        ],
                        id={"type": "modal-wnrs", "index": "modal-contribute"},
                        is_open=False,
                        centered=True,
                        size="lg",
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
                style={
                    "text-align": "center",
                    "margin-bottom": 0,
                },
            ),
            dcc.Store(id="intermediate-wnrs", storage_type="memory", data=data_store),
            dcc.Store(id="theme-wnrs", storage_type="memory", data=False),
        ]
    )
