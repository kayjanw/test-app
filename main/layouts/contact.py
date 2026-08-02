from dash import dcc, html

from common.layouts.about_me import about_me_links
from common.layouts.main import content_header
from main.layouts.main import style_contact_textarea


def contact_tab():
    return html.Div(
        [
            content_header("Contact Me"),
            html.Div(
                [
                    html.P(
                        "If you have any questions, feedback or suggestions, please feel free to drop me an email."
                    ),
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
                    about_me_links(
                        "openmoji:linkedin",
                        "LinkedIn",
                        "https://www.linkedin.com/in/kayjan/",
                    ),
                    about_me_links(
                        "openmoji:github", "GitHub", "https://www.github.com/kayjan/"
                    ),
                    about_me_links(
                        "material-icon-theme:github-sponsors",
                        "Support me!",
                        "https://buymeacoffee.com/kayjan/",
                        size=35,
                    ),
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
