import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

from components import WNRS
from components.helper import colour_palette, encode_dict
from layouts.main import content_header, style_hidden, style_wnrs_text


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


def wnrs_tab(app):
    wnrs_game = WNRS()
    list_of_deck = ["Main Deck 1"]
    wnrs_game.initialize_game(list_of_deck)
    wnrs_information = wnrs_game.get_information()
    data_store = wnrs_game.convert_to_store_format()
    data_save = wnrs_game.convert_to_save_format()

    main_deck = html.Div(
        [
            html.Span("Main Deck", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="main-deck-help",
            ),
            dbc.Tooltip(
                wnrs_information["Main Deck"]["Main Deck"]["description"],
                placement="right",
                target="main-deck-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Main Deck 1"},
                        style={"background-color": colour_palette["dark_pink"]},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={"type": "wnrs-deck-button", "id": "Main Deck 2"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={"type": "wnrs-deck-button", "id": "Main Deck 3"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Final Card",
                        id={"type": "wnrs-deck-button", "id": "Main Deck Final"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    crossover_bumble_bff = html.Div(
        [
            html.Span("Bumble x BFF Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="bumble-bff-help",
            ),
            dbc.Tooltip(
                wnrs_information["Crossover"]["Bumble x BFF Edition"]["description"],
                placement="right",
                target="bumble-bff-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Bumble x BFF Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={"type": "wnrs-deck-button", "id": "Bumble x BFF Edition 2"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={"type": "wnrs-deck-button", "id": "Bumble x BFF Edition 3"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    crossover_bumble_bizz = html.Div(
        [
            html.Span("Bumble Bizz Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="bumble-bizz-help",
            ),
            dbc.Tooltip(
                wnrs_information["Crossover"]["Bumble Bizz Edition"]["description"],
                placement="right",
                target="bumble-bizz-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Bumble Bizz Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={"type": "wnrs-deck-button", "id": "Bumble Bizz Edition 2"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={"type": "wnrs-deck-button", "id": "Bumble Bizz Edition 3"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    crossover_bumble_date = html.Div(
        [
            html.Span("Bumble Date Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="bumble-date-help",
            ),
            dbc.Tooltip(
                wnrs_information["Crossover"]["Bumble Date Edition"]["description"],
                placement="right",
                target="bumble-date-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Bumble Date Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={"type": "wnrs-deck-button", "id": "Bumble Date Edition 2"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={"type": "wnrs-deck-button", "id": "Bumble Date Edition 3"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    crossover_cann = html.Div(
        [
            html.Span(
                [
                    "Cann Edition",
                    html.Sup("Drinking", className="blinker"),
                ],
                className="span-short",
            ),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="cann-help",
            ),
            dbc.Tooltip(
                wnrs_information["Crossover"]["Cann Edition"]["description"],
                placement="right",
                target="cann-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Cann Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={"type": "wnrs-deck-button", "id": "Cann Edition 2"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={"type": "wnrs-deck-button", "id": "Cann Edition 3"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    crossover_valentino = html.Div(
        [
            html.Span(
                [
                    "Valentino Edition",
                    html.Sup("Reflect", className="blinker"),
                ],
                className="span-short",
            ),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="valentino-help",
            ),
            dbc.Tooltip(
                wnrs_information["Crossover"]["Valentino Edition"]["description"],
                placement="right",
                target="valentino-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Valentino Edition 1"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    expansion_honest_dating = html.Div(
        [
            html.Span("Honest Dating Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="dating-help",
            ),
            dbc.Tooltip(
                wnrs_information["Expansion"]["Honest Dating Edition"]["description"],
                placement="right",
                target="dating-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Honest Dating Edition 1",
                        },
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Honest Dating Edition 2",
                        },
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Honest Dating Edition 3",
                        },
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    expansion_inner_circle = html.Div(
        [
            html.Span("Inner Circle Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="inner-circle-help",
            ),
            dbc.Tooltip(
                wnrs_information["Expansion"]["Inner Circle Edition"]["description"],
                placement="right",
                target="inner-circle-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Inner Circle Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={"type": "wnrs-deck-button", "id": "Inner Circle Edition 2"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={"type": "wnrs-deck-button", "id": "Inner Circle Edition 3"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    expansion_own_it = html.Div(
        [
            html.Span("Own It Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="own-it-help",
            ),
            dbc.Tooltip(
                wnrs_information["Expansion"]["Own It Edition"]["description"],
                placement="right",
                target="own-it-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Own It Edition 1"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    expansion_relationship = html.Div(
        [
            html.Span("Relationship Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="relationship-help",
            ),
            dbc.Tooltip(
                wnrs_information["Expansion"]["Relationship Edition"]["description"],
                placement="right",
                target="relationship-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Relationship Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={"type": "wnrs-deck-button", "id": "Relationship Edition 2"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={"type": "wnrs-deck-button", "id": "Relationship Edition 3"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    online_race_privilege = html.Div(
        [
            html.Span(
                "Race and Privilege Edition",
                className="span-short",
            ),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="race-help",
            ),
            dbc.Tooltip(
                wnrs_information["Online"]["Race and Privilege Edition"]["description"],
                placement="right",
                target="race-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Race and Privilege Edition 1",
                        },
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Race and Privilege Edition 2",
                        },
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Race and Privilege Edition 3",
                        },
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    online_quarantine = html.Div(
        [
            html.Span("Quarantine Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="quarantine-help",
            ),
            dbc.Tooltip(
                wnrs_information["Online"]["Quarantine Edition"]["description"],
                placement="right",
                target="quarantine-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Quarantine Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 2",
                        id={"type": "wnrs-deck-button", "id": "Quarantine Edition 2"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Level 3",
                        id={"type": "wnrs-deck-button", "id": "Quarantine Edition 3"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Final Card",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Quarantine Edition Final",
                        },
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    online_voting = html.Div(
        [
            html.Span("Voting Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="voting-help",
            ),
            dbc.Tooltip(
                wnrs_information["Online"]["Voting Edition"]["description"],
                placement="right",
                target="voting-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Voting Edition 1"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    single_breakup = html.Div(
        [
            html.Span("Breakup Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="breakup-help",
            ),
            dbc.Tooltip(
                wnrs_information["Single-Player"]["Breakup Edition"]["description"],
                placement="right",
                target="breakup-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Breakup Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "ChatGPT",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Breakup Edition ChatGPT",
                        },
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Final Card",
                        id={"type": "wnrs-deck-button", "id": "Breakup Edition Final"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    single_existential = html.Div(
        [
            html.Span(
                [
                    "Existential Crisis Edition",
                    html.Sup("Mine", className="blinker"),
                ],
                className="span-short",
            ),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="crisis-help",
            ),
            dbc.Tooltip(
                wnrs_information["Single-Player"]["Existential Crisis Edition"][
                    "description"
                ],
                placement="right",
                target="crisis-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Existential Crisis Edition 1",
                        },
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    single_forgiveness = html.Div(
        [
            html.Span("Forgiveness Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="forgiveness-help",
            ),
            dbc.Tooltip(
                wnrs_information["Single-Player"]["Forgiveness Edition"]["description"],
                placement="right",
                target="forgiveness-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Forgiveness Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "ChatGPT",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Forgiveness Edition ChatGPT",
                        },
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    single_healing = html.Div(
        [
            html.Span("Healing Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="healing-help",
            ),
            dbc.Tooltip(
                wnrs_information["Single-Player"]["Healing Edition"]["description"],
                placement="right",
                target="healing-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Healing Edition 1"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    single_self_love = html.Div(
        [
            html.Span("Self-Love Edition", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="love-help",
            ),
            dbc.Tooltip(
                wnrs_information["Single-Player"]["Self-Love Edition"]["description"],
                placement="right",
                target="love-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Self-Love Edition 1"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Final Card",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Self-Love Edition Final",
                        },
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    single_self_reflection = html.Div(
        [
            html.Span(
                "Self-Reflection Edition",
                className="span-short",
            ),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="reflection-help",
            ),
            dbc.Tooltip(
                wnrs_information["Single-Player"]["Self-Reflection Edition"][
                    "description"
                ],
                placement="right",
                target="reflection-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Self-Reflection Edition 1",
                        },
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    gottman_love_maps = html.Div(
        [
            html.Span("Love Maps", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="love-maps-help",
            ),
            dbc.Tooltip(
                wnrs_information["Gotmann"]["Love Maps"]["description"],
                placement="right",
                target="love-maps-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Love Maps 1"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    gottman_open_ended = html.Div(
        [
            html.Span("Open Ended Questions", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="open-ended-help",
            ),
            dbc.Tooltip(
                wnrs_information["Gotmann"]["Open Ended Questions"]["description"],
                placement="right",
                target="open-ended-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Open Ended Questions 1"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    gottman_rituals = html.Div(
        [
            html.Span("Rituals of Connection", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="rituals-help",
            ),
            dbc.Tooltip(
                wnrs_information["Gotmann"]["Rituals of Connection"]["description"],
                placement="right",
                target="rituals-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={
                            "type": "wnrs-deck-button",
                            "id": "Rituals of Connection 1",
                        },
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    gottman_opportunity = html.Div(
        [
            html.Span("Opportunity", className="span-short"),
            html.Img(
                src=app.get_asset_url("info.svg"),
                id="opportunity-help",
            ),
            dbc.Tooltip(
                wnrs_information["Gotmann"]["Opportunity"]["description"],
                placement="right",
                target="opportunity-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Level 1",
                        id={"type": "wnrs-deck-button", "id": "Opportunity 1"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    gottman_couple = html.Div(
        [
            html.Span("Couple Questions", className="span-short"),
            html.Img(src=app.get_asset_url("info.svg"), id="rs-help"),
            dbc.Tooltip(
                wnrs_information["Relationship Edition"]["Couple"]["description"],
                placement="right",
                target="rs-help",
                className="tooltip",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Ice Breaker",
                        id={"type": "wnrs-deck-button", "id": "Couple IceBreaker"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Family and Childhood",
                        id={"type": "wnrs-deck-button", "id": "Couple Childhood"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Relationship",
                        id={"type": "wnrs-deck-button", "id": "Couple Relationship"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Sex and Kids",
                        id={"type": "wnrs-deck-button", "id": "Couple Sex&Kids"},
                        className="button-wnrs",
                    ),
                    dbc.Button(
                        "Marriage",
                        id={"type": "wnrs-deck-button", "id": "Couple Marriage"},
                        className="button-wnrs",
                    ),
                ],
                className="wnrs-level",
            ),
        ],
        className="custom-div-flex div-with-image div-with-image-left small-image",
    )

    def modal_deck():
        return [
            html.P("Main Deck", style=style_wnrs_text),
            main_deck,
            html.P("Crossover", style=style_wnrs_text),
            crossover_bumble_bff,
            crossover_bumble_bizz,
            crossover_bumble_date,
            crossover_cann,
            crossover_valentino,
            html.P("Expansion", style=style_wnrs_text),
            expansion_honest_dating,
            expansion_inner_circle,
            expansion_own_it,
            expansion_relationship,
            html.P("Online", style=style_wnrs_text),
            online_race_privilege,
            online_quarantine,
            online_voting,
            html.P("Single-Player", style=style_wnrs_text),
            single_breakup,
            single_existential,
            single_forgiveness,
            single_healing,
            single_self_love,
            single_self_reflection,
            html.P(
                [
                    "Gotmann Card Deck",
                    html.Sup("improve relationship", className="blinker"),
                ],
                style=style_wnrs_text,
            ),
            gottman_love_maps,
            gottman_open_ended,
            gottman_rituals,
            gottman_opportunity,
            gottman_couple,
            html.Br(),
        ]

    def modal_help():
        return [
            html.P(
                "How to Play (2-6 players)",
                className="p-short p-bold",
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
                className="p-short p-bold",
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
                className="p-short p-bold",
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
                className="p-short p-bold",
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
                className="p-short p-bold",
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
            html.Button(
                "Select deck",
                id="button-wnrs-show-ok",
                title="Show/hide deck selection",
                style={"display": "none"},
            ),
            html.Button(
                " + Instructions",
                id="button-wnrs-instruction-ok",
                title="How to play",
                style={"display": "none"},
            ),
            html.Div(
                id="div-wnrs-instruction",
                className="custom-div-full custom-div-dark image-dark-bg",
                style={"display": "none", "width": "90%", "margin-top": "20px"},
            ),
            html.Div(
                id="div-wnrs-selection",
                className="custom-div-full custom-div-dark image-dark-bg",
                style={"display": "none", "width": "90%", "margin-top": "20px"},
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
                                [
                                    html.P("Previous card"),
                                    DashIconify(icon="openmoji:tap", height=40),
                                ],
                                id="button-wnrs2-back",
                                style={},
                            ),
                            html.Button(
                                [
                                    DashIconify(icon="openmoji:tap", height=40),
                                    html.P("Next card"),
                                ],
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
