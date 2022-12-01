from dash import html

from layouts.main import content_header


def keyboard_tab():
    return html.Div(
        [
            content_header("Keyboard", "Play music on the flyyyyy"),
            html.Div([
                html.P("Ideally, users can play the keyboard here. Im still figuring out how to make it work."),
            ],
                className="custom-div-instruction custom-div-left"
            ),
            # html.Button('C note', id='button_music')
        ]
    )
