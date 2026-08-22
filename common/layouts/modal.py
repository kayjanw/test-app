import dash_bootstrap_components as dbc
from dash import html


def info_button(app, model_id: str):
    return html.Button(
        html.Span(
            html.Img(src=app.get_asset_url("help.png")),
            title="How to play",
        ),
        id={"type": f"button-{model_id}", "index": "modal-help"},
        className="div-with-image small-image image-dark-blue invisible-button vertical-center",
    )


def modal_popup(
    body,
    model_id: str,
    title: str = "Instructions",
    model_index: str = "modal-help",
):
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(title)),
            dbc.ModalBody(body),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id={
                        "type": f"button-close-{model_id}",
                        "index": model_index,
                    },
                )
            ),
        ],
        id={"type": model_id, "index": model_index},
        is_open=False,
        centered=True,
        size="lg",
    )
