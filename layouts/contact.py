from dash import html, dcc

from layouts.main import content_header, style_contact_textarea


def contact_tab():
    return html.Div(
        [
            content_header("Contact Me"),
            html.Div([
                html.P("If you have any questions, feedback or suggestions, please feel free to drop me an email."),
                html.P(
                        dcc.Input(
                        id="input-contact-name",
                        type="text",
                        placeholder="Name",
                        style=style_contact_textarea,
                    ),
                ),
                html.P(
                    dcc.Input(
                        id="input-contact-email",
                        type="text",
                        placeholder="Email Address",
                        style=style_contact_textarea,
                    ),
                ),
                html.P(
                    dcc.Textarea(
                        id="input-contact-content",
                        value="",
                        placeholder="Email body",
                        style=style_contact_textarea,
                    ),
                ),
                html.Br(),
                html.Button("Send", id="button-contact-ok"),
                html.P(id="contact-reply"),
            ],
                className="custom-div-instruction custom-div-left"
            )
        ]
    )
