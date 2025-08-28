from dash import html
from dash_iconify import DashIconify


def about_me_component(
    icon_name: str, component_name: str, component_description: str
) -> html.Div:
    """Component for about-me tab

    Args:
        icon_name: component icon
        component_name: component title
        component_description: component description

    Returns:
        Component for about-me tab
    """
    return html.Div(
        [
            DashIconify(icon=f"openmoji:{icon_name}", height=40),
            html.P(component_name, className="p-short p-bold"),
            html.P(f": {component_description}", className="p-short"),
        ],
        className="custom-div-small-space-below",
    )


def about_me_links(icon_name: str, link_title: str, link_url: str) -> html.Span:
    """Link component for about-me tab

    Args:
        icon_name: link icon
        link_title: link title
        link_url: link URL

    Returns:
        Link component for about-me tab
    """
    return html.Span(
        html.A(
            [
                DashIconify(icon=f"openmoji:{icon_name}", height=40),
                link_title,
            ],
            href=link_url,
            target="_blank",
        ),
        title=link_title,
    )
