import dash_mantine_components as dmc
from dash import dcc, html

from common.layouts.main import content_header
from main.components.poker import Poker, render_amount
from main.model.poker.poker import ButtonColour


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

    return html.Div(
        [
            content_header("Poker"),
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
        ]
    )
