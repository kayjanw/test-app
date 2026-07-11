import dash_mantine_components as dmc
from dash import dcc, html

from version import __version__


def main_layout():
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dmc.MantineProvider(html.Div(id="page-content")),
            html.Div(id="blank-output"),
            html.Div(id="resize-trigger", style={"display": "none"}),
            html.H6(
                [
                    html.H6("If you like this, "),
                    html.A(
                        "buy me a coffee ☕ ",
                        href="https://www.buymeacoffee.com/kayjan",
                        target="_blank",
                    ),
                    "! ",
                    html.H6(f"(v{__version__})"),
                ],
                className="footer",
            ),
        ]
    )


def banner():
    return html.Div(
        [
            html.Button("☰", id="button-sidebar"),
            html.Div(html.H1(dcc.Link("KJ Wong", href="/")), className="banner-center"),
        ],
    )


def sidebar_header():
    return html.Div(html.H1(dcc.Link("KJ Wong", href="/")))


def content_header(title, subtitle=None):
    return html.Div(
        [
            html.H2(title, className="content-header"),
            html.H3(subtitle),
            html.H4("————————"),
        ]
    )
