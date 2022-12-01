import dash_bootstrap_components as dbc
from dash import dcc, html

from components import WNRS
from components.helper import colour_palette, encode_dict
from layouts.main import content_header, style_hidden, style_wnrs_text


def wnrs_tab(app):
    wnrs_game = WNRS()
    list_of_deck = ["Main Deck 1"]
    wnrs_game.initialize_game(list_of_deck)
    wnrs_information = wnrs_game.get_information()
    data_default = dict(list_of_deck=list_of_deck, wnrs_game_dict=wnrs_game.__dict__)
    return html.Div(
        [
            content_header("We're Not Really Strangers", ""),
            html.Button(
                "Select deck",
                id="button-wnrs-show-ok",
                title="Show/hide deck selection",
            ),
            html.A(
                [
                    dcc.Upload(
                        [
                            html.Span(
                                "Upload past progress", title="Upload past progress"
                            )
                        ],
                        id="uploadbutton-wnrs",
                        multiple=False,
                    )
                ]
            ),
            html.Button(
                " + Instructions", id="button-wnrs-instruction-ok", title="How to play"
            ),
            html.Button(
                " + Suggest prompts",
                id="button-wnrs-suggestion-ok",
                title="Send in your card prompt ideas",
            ),
            html.Br(),
            html.Div(
                [
                    html.P("How to Play (2-6 players)", className="p-short p-bold"),
                    html.P(
                        "The game is played on a single device. Sit in a circle with device in middle of all "
                        "players. Select the decks you want to play with and the levels. Players take turn to "
                        "answer questions shown on the screen and tap on the right side of card to proceed to next "
                        "question."
                    ),
                    html.P(
                        "Wildcards",
                        style={"margin-top": "20px"},
                        className="p-short p-bold",
                    ),
                    html.P(
                        "If you're presented with a wildcard you must complete the instructions otherwise stated. "
                        "These cards can appear at any moment during the game!"
                    ),
                    html.P(
                        "Save your progress!",
                        style={"margin-top": "20px"},
                        className="p-short p-bold",
                    ),
                    html.P(
                        "Couldn't manage to go through all the cards in one session? Save your progress by clicking "
                        "on the 'Save progress' button at the bottom of the page and load the game next time to "
                        "pick up exactly where you left off."
                    ),
                    html.P(
                        "Have fun!",
                        style={"margin-top": "20px"},
                        className="p-short p-bold",
                    ),
                ],
                id="div-wnrs-instruction",
                className="custom-div-full custom-div-dark image-dark-bg",
                style={"display": "none", "width": "90%", "margin-top": "20px"},
            ),
            html.Div(
                [
                    html.P(
                        "You can contribute too! Suggest prompts that you would like to see in the game",
                    ),
                    html.P(
                        dcc.Input(
                            id="input-wnrs-suggestion",
                            type="text",
                            placeholder="Your prompt(s)",
                            style={"width": "100%", "margin-bottom": "3px"},
                        ),
                    ),
                    html.P(
                        dcc.Textarea(
                            id="input-wnrs-suggestion2",
                            value="",
                            placeholder="(Optional) Additional comments or feedback, include your contact details if you "
                            "expect a reply!",
                            style={"width": "100%"},
                        ),
                    ),
                    html.Br(),
                    html.Button("Send", id="button-wnrs-send-ok"),
                    html.P(id="wnrs-suggestion-reply"),
                ],
                id="div-wnrs-suggestion",
                className="custom-div-full custom-div-dark image-dark-bg",
                style={"display": "none", "width": "90%", "margin-top": "20px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Main Deck"),
                            html.Div(
                                [
                                    html.Span("Main Deck", className="span-short"),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="main-deck-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Main Deck"]["Main Deck"][
                                            "description"
                                        ],
                                        placement="right",
                                        target="main-deck-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Main Deck 1",
                                                style={
                                                    "background-color": colour_palette[
                                                        "dark_pink"
                                                    ]
                                                },
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Main Deck 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Main Deck 3",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Final Card",
                                                id="Main Deck Final",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.P("Crossover", style=style_wnrs_text),
                            html.Div(
                                [
                                    html.Span(
                                        "Bumble x BFF Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="bumble-bff-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"][
                                            "Bumble x BFF Edition"
                                        ]["description"],
                                        placement="right",
                                        target="bumble-bff-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Bumble x BFF Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Bumble x BFF Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Bumble x BFF Edition 3",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Bumble Bizz Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="bumble-bizz-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"][
                                            "Bumble Bizz Edition"
                                        ]["description"],
                                        placement="right",
                                        target="bumble-bizz-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Bumble Bizz Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Bumble Bizz Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Bumble Bizz Edition 3",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Bumble Date Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="bumble-date-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"][
                                            "Bumble Date Edition"
                                        ]["description"],
                                        placement="right",
                                        target="bumble-date-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Bumble Date Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Bumble Date Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Bumble Date Edition 3",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
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
                                        wnrs_information["Crossover"]["Cann Edition"][
                                            "description"
                                        ],
                                        placement="right",
                                        target="cann-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Cann Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Cann Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Cann Edition 3",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        [
                                            "Valentino Edition",
                                            html.Sup("Reflection", className="blinker"),
                                        ],
                                        className="span-short",
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="valentino-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Crossover"][
                                            "Valentino Edition"
                                        ]["description"],
                                        placement="right",
                                        target="valentino-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Valentino Edition 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.P("Expansion", style=style_wnrs_text),
                            html.Div(
                                [
                                    html.Span(
                                        "Honest Dating Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="dating-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Expansion"][
                                            "Honest Dating Edition"
                                        ]["description"],
                                        placement="right",
                                        target="dating-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Honest Dating Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Honest Dating Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Honest Dating Edition 3",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Inner Circle Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="inner-circle-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Expansion"][
                                            "Inner Circle Edition"
                                        ]["description"],
                                        placement="right",
                                        target="inner-circle-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Inner Circle Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Inner Circle Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Inner Circle Edition 3",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Own It Edition", className="span-short"),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="own-it-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Expansion"]["Own It Edition"][
                                            "description"
                                        ],
                                        placement="right",
                                        target="own-it-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Own It Edition 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Relationship Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="relationship-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Expansion"][
                                            "Relationship Edition"
                                        ]["description"],
                                        placement="right",
                                        target="relationship-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Relationship Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Relationship Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Relationship Edition 3",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.P("Online", style=style_wnrs_text),
                            html.Div(
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
                                        wnrs_information["Online"][
                                            "Race and Privilege Edition"
                                        ]["description"],
                                        placement="right",
                                        target="race-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Race and Privilege Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Race and Privilege Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Race and Privilege Edition 3",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Quarantine Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="quarantine-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Online"][
                                            "Quarantine Edition"
                                        ]["description"],
                                        placement="right",
                                        target="quarantine-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Quarantine Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Quarantine Edition 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Quarantine Edition 3",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Final Card",
                                                id="Quarantine Edition Final",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Voting Edition", className="span-short"),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="voting-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Online"]["Voting Edition"][
                                            "description"
                                        ],
                                        placement="right",
                                        target="voting-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Voting Edition 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.P("Single-Player", style=style_wnrs_text),
                            html.Div(
                                [
                                    html.Span(
                                        "Breakup Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="breakup-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"][
                                            "Breakup Edition"
                                        ]["description"],
                                        placement="right",
                                        target="breakup-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Breakup Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Final Card",
                                                id="Breakup Edition Final",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
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
                                        wnrs_information["Single-Player"][
                                            "Existential Crisis Edition"
                                        ]["description"],
                                        placement="right",
                                        target="crisis-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Existential Crisis Edition 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Forgiveness Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="forgiveness-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"][
                                            "Forgiveness Edition"
                                        ]["description"],
                                        placement="right",
                                        target="forgiveness-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Forgiveness Edition 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Healing Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="healing-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"][
                                            "Healing Edition"
                                        ]["description"],
                                        placement="right",
                                        target="healing-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Healing Edition 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Self-Love Edition", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="love-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Single-Player"][
                                            "Self-Love Edition"
                                        ]["description"],
                                        placement="right",
                                        target="love-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Self-Love Edition 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Final Card",
                                                id="Self-Love Edition Final",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
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
                                        wnrs_information["Single-Player"][
                                            "Self-Reflection Edition"
                                        ]["description"],
                                        placement="right",
                                        target="reflection-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Self-Reflection Edition 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.P(
                                [
                                    "Gotmann Card Deck",
                                    html.Sup(
                                        "improve relationship", className="blinker"
                                    ),
                                ],
                                style=style_wnrs_text,
                            ),
                            html.Div(
                                [
                                    html.Span("Love Maps", className="span-short"),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="love-maps-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Gotmann"]["Love Maps"][
                                            "description"
                                        ],
                                        placement="right",
                                        target="love-maps-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Love Maps 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Open Ended Questions", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="open-ended-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Gotmann"][
                                            "Open Ended Questions"
                                        ]["description"],
                                        placement="right",
                                        target="open-ended-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Open Ended Questions 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Rituals of Connection", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="rituals-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Gotmann"][
                                            "Rituals of Connection"
                                        ]["description"],
                                        placement="right",
                                        target="rituals-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Rituals of Connection 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span("Opportunity", className="span-short"),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"),
                                        id="opportunity-help",
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Gotmann"]["Opportunity"][
                                            "description"
                                        ],
                                        placement="right",
                                        target="opportunity-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Opportunity 1",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Couple Questions", className="span-short"
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("info.svg"), id="rs-help"
                                    ),
                                    dbc.Tooltip(
                                        wnrs_information["Relationship Edition"][
                                            "Couple"
                                        ]["description"],
                                        placement="right",
                                        target="rs-help",
                                        className="tooltip",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Level 1",
                                                id="Couple 1",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 2",
                                                id="Couple 2",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 3",
                                                id="Couple 3",
                                                className="button-wnrs",
                                            ),
                                            dbc.Button(
                                                "Level 4",
                                                id="Couple 4",
                                                className="button-wnrs",
                                            ),
                                        ],
                                        className="wnrs-level",
                                    ),
                                ],
                                className="custom-div-flex div-with-image div-with-image-left small-image",
                            ),
                        ]
                    ),
                ],
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
                            ),
                            html.Button(id="button-wnrs2-back"),
                            html.Button(id="button-wnrs2-next"),
                            html.Span("Previous card", id="wnrs-text-back"),
                            html.Span("Next card", id="wnrs-text-next"),
                        ],
                        id="div-wnrs",
                        className="custom-div-center div-with-invisible-button",
                    ),
                    html.Div(
                        [
                            html.P("- / -", id="wnrs-counter"),
                            html.Button(
                                "Previous", id="button-wnrs-back", style=style_hidden
                            ),
                            html.Button(
                                "Next", id="button-wnrs-next", style=style_hidden
                            ),
                            html.Button(
                                "Shuffle Remaining Cards", id="button-wnrs-shuffle-ok"
                            ),
                            html.Form(
                                [
                                    dcc.Input(
                                        value=encode_dict(data_default),
                                        name="result",
                                        type="text",
                                        style=style_hidden,
                                        id="input-wnrs",
                                    ),
                                    html.Button(
                                        [
                                            html.Img(
                                                src=app.get_asset_url("download.svg")
                                            ),
                                            html.Span("Save Progress"),
                                        ],
                                        type="submit",
                                        id="button-wnrs-download-ok",
                                        className="div-with-image div-with-image-left small-image",
                                    ),
                                ],
                                method="POST",
                                action="/download_dict/",
                                style={"display": "inline-block"},
                            ),
                        ]
                    ),
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
                style={
                    "text-align": "center",
                    "margin-bottom": 0,
                },
            ),
            dcc.Store(id="intermediate-wnrs", storage_type="memory", data=data_default),
        ]
    )
