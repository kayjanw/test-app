import dash_mantine_components as dmc
from dash import dcc, html

from common.layouts.main import content_header
from common.layouts.modal import info_button, modal_popup
from main.components.poker import Poker, render_amount
from main.model.poker.poker import ButtonColour
from main.model.poker.profile import PROFILE_DESCRIPTION


def poker_table(state):
    return dmc.Paper(
        [
            dmc.Group(
                [
                    dmc.Text(
                        [
                            "Stage: ",
                            dmc.Text(
                                state["stage"], span=True, fw=700, id="poker-stage"
                            ),
                        ],
                        size="xl",
                    ),
                    dmc.Text(
                        [
                            "Pot: ",
                            dmc.Text(
                                render_amount(state["pot"]),
                                span=True,
                                fw=700,
                                id="poker-pot",
                            ),
                        ],
                        size="xl",
                    ),
                    dmc.Text(
                        [
                            "To Call: ",
                            dmc.Text(
                                render_amount(state["to_call"]),
                                span=True,
                                fw=700,
                                id="poker-call",
                            ),
                        ],
                        size="xl",
                    ),
                ],
                justify="center",
                gap="xl",
            ),
            dmc.Center(
                dmc.Group(gap="sm", id="poker-board-cards"),
                style={
                    "minHeight": "220px",
                },
            ),
            dmc.Center(
                dmc.Text(
                    state["result"],
                    size="xl",
                    fw=600,
                    ta="center",
                    id="poker-output",
                ),
            ),
        ],
        radius="xl",
        shadow="lg",
        p="xl",
        style={
            "backgroundColor": "#287a3e",
            "minHeight": "350px",
            "border": "8px solid #174d27",
        },
    )


def player_cards(state):
    return dmc.Paper(
        [
            dmc.Text(
                "PLAYER",
                fw=700,
                size="xl",
                mb="sm",
            ),
            dmc.Group(gap="sm", mb="md", id="poker-user-cards"),
            dmc.Text(
                render_amount(state["chips_user"]),
                size="lg",
                fw=700,
                mb="xl",
                id="poker-user-chips",
            ),
            html.Div(
                [
                    html.Button(
                        "New Hand",
                        style={"backgroundColor": ButtonColour.NEW_HAND},
                        className="button-outline",
                        id="button-poker-newhandfold",
                    ),
                    html.Button(
                        "Check",
                        style={"display": "none"},
                        className="button-outline",
                        id="button-poker-checkcall",
                    ),
                    html.Br(),
                    html.Button(
                        "Raise",
                        style={"display": "none"},
                        className="button-outline",
                        id="button-poker-betraise",
                    ),
                    dcc.Input(
                        id="poker-raise",
                        type="number",
                        value=20,
                        min=0,
                        step=10,
                        style={"display": "none"},
                    ),
                ],
                className="custom-div-flex-only custom-div-small-space-below",
            ),
            dmc.Text(
                size="lg",
                fw=700,
                mb="xl",
                id="poker-user-profile",
            ),
        ],
        style={
            "flex": 1,
            "textAlign": "left",
        },
    )


def cpu_cards(state):
    return dmc.Paper(
        [
            dmc.Text(
                "CPU",
                fw=700,
                size="xl",
                mb="sm",
            ),
            # CPU cards
            dmc.Group(
                gap="sm",
                mb="md",
                id="poker-cpu-cards",
            ),
            dmc.Text(
                render_amount(state["chips_cpu"]),
                size="xl",
                fw=700,
                mb="md",
                id="poker-cpu-chips",
            ),
        ],
        style={
            "flex": 1,
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "flex-end",
        },
    )


def poker_tab(app):
    poker_game = Poker()
    state = poker_game.state

    def modal_help():
        return [
            html.P(
                "How to Play (1 player)",
                className="p-short p-bold neucha-font",
            ),
            html.P(
                [
                    "The game is played on a single device. Select ",
                    html.Span("New Hand", className="p-short p-bold"),
                    " to start a new game.",
                ],
            ),
            html.P(
                "Player Statistics",
                style={"margin-top": "20px"},
                className="p-short p-bold neucha-font",
            ),
            html.P(
                "After 10 rounds, player statistics will be available.",
            ),
            html.P(
                [
                    item
                    for stat_name, stat_desc in PROFILE_DESCRIPTION.items()
                    for item in [
                        html.Span(stat_name, className="p-bold"),
                        f": {stat_desc}",
                        html.Br(),
                    ]
                ],
                className="p-indent",
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
            content_header(["Poker", info_button(app, "modal-poker")]),
            html.Div(
                [
                    dmc.Container(
                        [
                            dmc.Stack(
                                [
                                    poker_table(state),
                                    dmc.Group(
                                        [
                                            player_cards(state),
                                            cpu_cards(state),
                                        ],
                                        align="start",
                                        grow=True,
                                        gap="xl",
                                    ),
                                ],
                                gap="xl",
                            ),
                        ],
                        size="xl",
                        py="xl",
                    )
                ],
                className="custom-container custom-div-space-above custom-div-space-below",
                style={
                    "text-align": "center",
                    "margin-bottom": 0,
                },
            ),
            dcc.Store(
                id="poker-state",
                storage_type="memory",
                data=state,
            ),
            dcc.Store(id="poker-move", storage_type="memory", data=""),
            modal_popup(modal_help(), "modal-poker"),
        ]
    )
