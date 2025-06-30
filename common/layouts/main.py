from dash import dcc, html


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
