from dash import dcc, html

from layouts.main import content_header, style_contact_textarea


def contact_tab():
    image_src_linkedin = "https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"
    return html.Div(
        [
            content_header("Contact Me"),
            html.Div(
                [
                    html.P(
                        [
                            "If you have any questions, feedback or suggestions, please feel free to drop me an email.",
                            html.Br(),
                            "Alternatively, you can reach me on ",
                            html.A(
                                html.Img(src=image_src_linkedin),
                                href="https://www.linkedin.com/in/kayjan/",
                                target="_blank",
                            ),
                        ],
                        className="div-with-image div-with-small-image-right",
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
                ],
                className="custom-div-instruction custom-div-left",
            ),
        ]
    )
